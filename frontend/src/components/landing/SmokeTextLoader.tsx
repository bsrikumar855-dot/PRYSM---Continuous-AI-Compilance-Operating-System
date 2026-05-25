"use client";

import dynamic from "next/dynamic";

const SmokeText = dynamic(() => import("@/components/landing/SmokeText"), {
  ssr: false,
  loading: () => (
    <div className="flex h-[clamp(120px,22vw,240px)] w-full items-center justify-center">
      <h1 className="text-[18vw] font-black leading-none text-white/20 sm:text-[8.5rem] md:text-[11rem]">
        PRYSM
      </h1>
    </div>
  ),
});

export default function SmokeTextLoader() {
  return <SmokeText />;
}
