import Link from "next/link";
import Image from "next/image";
import { ArrowRight } from "lucide-react";

import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import SmokeTextLoader from "@/components/landing/SmokeTextLoader";

export default function Home() {
  return (
    <main className="prysm-landing relative min-h-screen overflow-clip bg-[#08070a] text-white">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_55%,rgba(255,255,255,0.12),transparent_18%),linear-gradient(180deg,rgba(255,255,255,0.04),transparent_34%,rgba(255,255,255,0.05))]" />
      <div className="prysm-grid absolute inset-0 opacity-50" />
      <div className="prysm-vignette absolute inset-0" />

      <div className="absolute left-1/2 top-1/2 h-[42rem] w-[42rem] -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/10 opacity-40" />
      <div className="prysm-orbit prysm-orbit-one absolute left-1/2 top-1/2 h-[34rem] w-[34rem] -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/10" />
      <div className="prysm-orbit prysm-orbit-two absolute left-1/2 top-1/2 h-[24rem] w-[24rem] -translate-x-1/2 -translate-y-1/2 rounded-full border border-white/10" />

      <div className="prysm-beam prysm-beam-left absolute left-[12%] top-[-18%] h-[82rem] w-24 rotate-[28deg] bg-white/20 blur-2xl" />
      <div className="prysm-beam prysm-beam-right absolute right-[10%] top-[-16%] h-[82rem] w-24 rotate-[-28deg] bg-[rgba(212,168,48,0.2)] blur-2xl" />

      <header className="absolute left-0 top-0 z-50 p-6">
        <Link href="/" className="flex items-center gap-2 group">
          <Image
            src="/prysm-logo-transparent.png"
            alt="PRYSM Logo"
            width={96}
            height={73}
            className="object-contain transition-all duration-300"
            priority
          />
        </Link>
      </header>

      <section className="relative z-10 mx-auto flex min-h-[calc(100vh-5.5rem)] w-full max-w-6xl flex-col items-center justify-center px-6 pb-20 text-center">
        <p className="prysm-kicker mb-8 text-xs font-medium uppercase tracking-[0.48em] text-[rgba(232,200,96,0.75)]">
          Continuous AI Compliance Operating System
        </p>

        <SmokeTextLoader />

        <div className="prysm-line mt-5 h-px w-full max-w-3xl bg-gradient-to-r from-transparent via-[rgba(212,168,48,0.7)] to-transparent" />

        <p className="prysm-copy mt-8 max-w-2xl text-base leading-8 text-white/64 md:text-lg">
          Businesses should never be surprised by compliance risk again.
        </p>

        <div className="prysm-actions mt-10 flex flex-col items-center gap-3 sm:flex-row">
          <Link
            href="/dashboard"
            className={cn(
              buttonVariants({ size: "lg" }),
              "h-11 rounded-full bg-gradient-to-r from-[#A07018] via-[#D4A830] to-[#FFF8E1] px-6 text-[#0a0908] font-semibold shadow-[0_0_40px_rgba(232,200,96,0.35)] hover:from-[#C8A030] hover:via-[#E8C860] hover:to-[#FFF8E1]"
            )}
          >
            Enter PRYSM
            <ArrowRight className="size-4" />
          </Link>
          <Link
            href="/upload"
            className={cn(
              buttonVariants({ variant: "outline", size: "lg" }),
              "h-11 rounded-full border-[rgba(212,168,48,0.25)] bg-[rgba(212,168,48,0.04)] px-6 text-[#FFF8E1] hover:bg-[rgba(212,168,48,0.12)] hover:border-[rgba(232,200,96,0.4)]"
            )}
          >
            Upload Evidence
          </Link>
        </div>
      </section>
    </main>
  );
}
