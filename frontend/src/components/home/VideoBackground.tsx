"use client";

import { cn } from "@/lib/utils";

export function VideoBackground({ className }: { className?: string }) {
  return (
    <div className={cn("absolute inset-0 z-0 overflow-hidden bg-sat-bg-primary", className)}>
      <video
        autoPlay
        loop
        muted
        playsInline
        preload="auto"
        className="responsive-hero-banner__video"
        aria-hidden="true"
      >
        <source src="/earth-observation-loop.webm" type="video/webm" />
        <source src="/earth-observation-loop.mp4" type="video/mp4" />
      </video>
      {/* Noise overlay for texture */}
      <div 
        className="absolute inset-0 pointer-events-none opacity-20 mix-blend-overlay"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E")`,
        }}
      />
      {/* Vignette */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_center,_transparent_0%,_#0a0a0a_100%)] opacity-80" />
    </div>
  );
}
