"use client";

import { useEffect, useRef } from "react";

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  size: number;
  hue: number;
  opacity: number;
}

interface TrailPoint {
  x: number;
  y: number;
  age: number;
}

export default function CursorTrail() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mouseRef = useRef({ x: -999, y: -999, active: false });
  const particles = useRef<Particle[]>([]);
  const trail = useRef<TrailPoint[]>([]);
  const rafRef = useRef<number>(0);
  const frameRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Size canvas to full window
    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener("resize", resize);

    // Mouse tracking (global)
    const onMove = (e: MouseEvent) => {
      mouseRef.current = { x: e.clientX, y: e.clientY, active: true };

      // Add to trail
      trail.current.push({ x: e.clientX, y: e.clientY, age: 0 });
      if (trail.current.length > 16) trail.current.shift();
    };
    const onLeave = () => { mouseRef.current.active = false; };

    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseleave", onLeave);

    const spawnParticles = (x: number, y: number) => {
      const count = 1 + Math.floor(Math.random() * 2);
      for (let i = 0; i < count; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 1.8 + 0.3;
        particles.current.push({
          x: x + (Math.random() - 0.5) * 10,
          y: y + (Math.random() - 0.5) * 10,
          vx: Math.cos(angle) * speed * 0.6,
          vy: Math.sin(angle) * speed - 0.8, // slight upward bias
          life: 0,
          maxLife: 30 + Math.random() * 40,
          size: Math.random() * 1.5 + 0.5,
          hue: 42 + Math.random() * 18, // gold range
          opacity: 0.35 + Math.random() * 0.35,
        });
      }
    };

    const draw = () => {
      const ctx = canvas.getContext("2d");
      if (!ctx) { rafRef.current = requestAnimationFrame(draw); return; }

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      frameRef.current++;

      const { x, y, active } = mouseRef.current;

      // Spawn particles on every other frame when mouse is moving
      if (active && x > 0 && frameRef.current % 4 === 0) {
        spawnParticles(x, y);
      }

      // Draw trail glow
      if (trail.current.length > 1) {
        trail.current.forEach((pt, i) => {
          pt.age++;
          const progress = i / trail.current.length;
          const alpha = progress * 0.18 * (1 - pt.age / 80);
          if (alpha <= 0) return;
          ctx.beginPath();
          ctx.arc(pt.x, pt.y, 12 * progress, 0, Math.PI * 2);
          ctx.fillStyle = `hsla(45, 90%, 65%, ${alpha})`;
          ctx.fill();
        });
        // Remove old trail points
        trail.current = trail.current.filter(pt => pt.age < 80);
      }

      // Cursor orb — glowing disc at cursor
      if (active && x > 0) {
        const pulse = 0.7 + 0.3 * Math.sin(frameRef.current * 0.06);

        // Outer soft aura
        const grad = ctx.createRadialGradient(x, y, 0, x, y, 24 * pulse);
        grad.addColorStop(0, "rgba(232, 200, 96, 0.12)");
        grad.addColorStop(0.4, "rgba(212, 168, 48, 0.05)");
        grad.addColorStop(1, "transparent");
        ctx.beginPath();
        ctx.arc(x, y, 24 * pulse, 0, Math.PI * 2);
        ctx.fillStyle = grad;
        ctx.fill();

        // Inner bright dot
        const innerGrad = ctx.createRadialGradient(x, y, 0, x, y, 3);
        innerGrad.addColorStop(0, "rgba(255, 248, 225, 0.95)");
        innerGrad.addColorStop(0.5, "rgba(232, 200, 96, 0.7)");
        innerGrad.addColorStop(1, "transparent");
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, Math.PI * 2);
        ctx.fillStyle = innerGrad;
        ctx.fill();
      }

      // Update + draw particles
      particles.current = particles.current.filter(p => {
        p.life++;
        p.x += p.vx;
        p.y += p.vy;
        p.vx *= 0.97;
        p.vy *= 0.97;
        p.vy -= 0.018; // float upward

        const t = p.life / p.maxLife;
        const alpha = p.opacity * (1 - t) * Math.min(t * 6, 1);
        if (alpha <= 0.005) return false;

        const radius = p.size * (1 - t * 0.5);

        // Glow halo
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, radius * 3);
        g.addColorStop(0, `hsla(${p.hue}, 90%, 72%, ${alpha * 0.5})`);
        g.addColorStop(1, `hsla(${p.hue}, 90%, 72%, 0)`);
        ctx.beginPath();
        ctx.arc(p.x, p.y, radius * 3, 0, Math.PI * 2);
        ctx.fillStyle = g;
        ctx.fill();

        // Core
        ctx.beginPath();
        ctx.arc(p.x, p.y, radius, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${p.hue + 10}, 95%, 82%, ${alpha})`;
        ctx.fill();

        return true;
      });

      rafRef.current = requestAnimationFrame(draw);
    };

    rafRef.current = requestAnimationFrame(draw);

    return () => {
      cancelAnimationFrame(rafRef.current);
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseleave", onLeave);
      window.removeEventListener("resize", resize);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "fixed",
        inset: 0,
        zIndex: 9999,
        pointerEvents: "none",
        mixBlendMode: "screen",
      }}
    />
  );
}
