"use client";

import { useRef, useState, useEffect, MouseEvent } from "react";

interface LetterState {
  dx: number;
  dy: number;
  scale: number;
  brightness: number;
}

const LETTERS = ["P", "R", "Y", "S", "M"];
const SPRING = 0.08;
const DAMPING = 0.72;
const MAX_PULL = 28;
const INFLUENCE = 200;

export default function SmokeText() {
  const containerRef = useRef<HTMLDivElement>(null);
  const mouseRef = useRef({ x: -999, y: -999, active: false });
  const letterRefs = useRef<(HTMLSpanElement | null)[]>([]);
  const velocitiesRef = useRef<{ vx: number; vy: number }[]>(
    LETTERS.map(() => ({ vx: 0, vy: 0 }))
  );
  const [letterStates, setLetterStates] = useState<LetterState[]>(
    LETTERS.map(() => ({ dx: 0, dy: 0, scale: 1, brightness: 1 }))
  );
  const [isHovered, setIsHovered] = useState(false);
  const [sweepPos, setSweepPos] = useState(-30);

  /* ── Magnetic letter spring physics ────────────────────────────── */
  useEffect(() => {
    let raf: number;
    const statesRef = { current: letterStates };

    const step = () => {
      const mouse = mouseRef.current;
      const newStates = LETTERS.map((_, i) => {
        const el = letterRefs.current[i];
        if (!el || !containerRef.current) return statesRef.current[i];

        const rect = el.getBoundingClientRect();
        const cRect = containerRef.current.getBoundingClientRect();
        const lx = rect.left - cRect.left + rect.width / 2;
        const ly = rect.top - cRect.top + rect.height / 2;

        let targetDx = 0, targetDy = 0, targetScale = 1, targetBrightness = 1;

        if (mouse.active) {
          const dx = mouse.x - lx;
          const dy = mouse.y - ly;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < INFLUENCE) {
            const strength = Math.pow(1 - dist / INFLUENCE, 2);
            targetDx = Math.max(-MAX_PULL, Math.min(MAX_PULL, dx * strength * 0.22));
            targetDy = Math.max(-MAX_PULL, Math.min(MAX_PULL, dy * strength * 0.18));
            targetScale = 1 + strength * 0.1;
            targetBrightness = 1 + strength * 0.7;
          }
        }

        const vel = velocitiesRef.current[i];
        vel.vx = vel.vx * DAMPING + (targetDx - statesRef.current[i].dx) * SPRING;
        vel.vy = vel.vy * DAMPING + (targetDy - statesRef.current[i].dy) * SPRING;

        return {
          dx: statesRef.current[i].dx + vel.vx,
          dy: statesRef.current[i].dy + vel.vy,
          scale: statesRef.current[i].scale + (targetScale - statesRef.current[i].scale) * 0.12,
          brightness: statesRef.current[i].brightness + (targetBrightness - statesRef.current[i].brightness) * 0.12,
        };
      });

      statesRef.current = newStates;
      setLetterStates([...newStates]);
      raf = requestAnimationFrame(step);
    };

    raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  /* ── Periodic light sweep ──────────────────────────────────────── */
  useEffect(() => {
    const runSweep = () => {
      let pos = -30;
      const interval = setInterval(() => {
        pos += 2.8;
        setSweepPos(pos);
        if (pos > 130) clearInterval(interval);
      }, 16);
    };
    const t = setTimeout(runSweep, 1400);
    const sw = setInterval(runSweep, 5500);
    return () => { clearTimeout(t); clearInterval(sw); };
  }, []);

  const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
    if (!containerRef.current) return;
    const rect = containerRef.current.getBoundingClientRect();
    mouseRef.current = { x: e.clientX - rect.left, y: e.clientY - rect.top, active: true };
  };

  return (
    <div
      ref={containerRef}
      className="relative flex w-full items-center justify-center select-none"
      style={{ height: "clamp(120px, 22vw, 240px)" }}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => { setIsHovered(true); mouseRef.current.active = true; }}
      onMouseLeave={() => {
        setIsHovered(false);
        mouseRef.current = { x: -999, y: -999, active: false };
      }}
    >
      {/* Ambient breathing halo */}
      <div
        className="absolute inset-0 pointer-events-none transition-all duration-700"
        style={{
          background: isHovered
            ? "radial-gradient(ellipse 90% 70% at 50% 50%, rgba(232,200,96,0.11) 0%, transparent 70%)"
            : "radial-gradient(ellipse 60% 40% at 50% 50%, rgba(212,168,48,0.05) 0%, transparent 70%)",
          animation: "prysm-halo-breathe 4s ease-in-out infinite",
        }}
      />

      {/* Letter row */}
      <h1
        className="relative flex items-center justify-center z-10"
        style={{
          fontFamily: '"GFS Didot", serif',
          fontSize: "clamp(60px, 22vw, 180px)",
          fontWeight: 400,
          lineHeight: 1,
        }}
      >
        {/* Travelling light sweep overlay */}
        <span
          aria-hidden
          className="absolute inset-0 pointer-events-none flex items-center justify-center overflow-hidden"
          style={{
            fontFamily: '"GFS Didot", serif',
            fontSize: "clamp(60px, 22vw, 180px)",
            fontWeight: 400,
            color: "transparent",
            backgroundImage: `linear-gradient(105deg, transparent ${sweepPos - 14}%, rgba(255,248,225,0.55) ${sweepPos}%, rgba(255,255,255,0.78) ${sweepPos + 4}%, rgba(255,248,225,0.45) ${sweepPos + 9}%, transparent ${sweepPos + 22}%), linear-gradient(180deg, #E8C860 0%, #D4A830 40%, #A07018 100%)`,
            WebkitBackgroundClip: "text",
            backgroundClip: "text",
            WebkitTextFillColor: "transparent",
            userSelect: "none",
            zIndex: 2,
          }}
        >
          PRYSM
        </span>

        {/* Magnetic letters */}
        {LETTERS.map((letter, i) => (
          <span
            key={letter}
            ref={(el) => { letterRefs.current[i] = el; }}
            className="prysm-letter inline-block"
            style={{
              "--letter-delay": `${0.28 + i * 0.11}s`,
              transform: `translate(${letterStates[i].dx}px, ${letterStates[i].dy}px) scale(${letterStates[i].scale})`,
              filter: `brightness(${letterStates[i].brightness}) drop-shadow(0 0 ${isHovered ? 26 : 8}px rgba(212,168,48,${isHovered ? 0.5 : 0.12}))`,
              transition: "filter 0.35s ease",
              willChange: "transform, filter",
            } as React.CSSProperties}
          >
            {letter}
          </span>
        ))}
      </h1>
    </div>
  );
}
