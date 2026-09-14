"use client";

import { useEffect, useState } from "react";
import { cn } from "@/lib/utils";

export function AnalyticsPreviewWidget({ className }: { className?: string }) {
  const [dataPoints, setDataPoints] = useState<number[]>(Array(20).fill(10));
  const [activeAoi, setActiveAoi] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setDataPoints(Array.from({ length: 20 }, () => Math.floor(Math.random() * 80) + 10));
      setActiveAoi((prev) => (prev + 1) % 3);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className={cn("p-6 bg-sat-surface border border-sat-border rounded-lg shadow-xl", className)}>
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-sm font-semibold tracking-wider text-sat-accent">SPECTRAL PROFILE</h3>
        <span className="text-xs text-text-muted font-mono bg-sat-bg-secondary px-2 py-1 rounded">
          AOI-0{activeAoi + 1}
        </span>
      </div>

      {/* Simulated Line Chart */}
      <div className="relative h-32 w-full border-b border-l border-sat-border-alt mb-6 flex items-end">
        <svg
          className="absolute inset-0 h-full w-full overflow-visible transition-all duration-700 ease-in-out"
          preserveAspectRatio="none"
          viewBox="0 0 100 100"
        >
          <path
            d={`M 0,${100 - dataPoints[0] || 0} ` + dataPoints.map((val, i) => `L ${i * 5.26},${100 - val}`).join(" ")}
            fill="none"
            stroke="var(--accent)"
            strokeWidth="2"
            vectorEffect="non-scaling-stroke"
            className="transition-all duration-700 ease-in-out"
          />
          <path
            d={`M 0,100 L 0,${100 - dataPoints[0] || 0} ` + dataPoints.map((val, i) => `L ${i * 5.26},${100 - val}`).join(" ") + ` L 100,100 Z`}
            fill="url(#gradient-accent)"
            className="transition-all duration-700 ease-in-out opacity-20"
          />
          <defs>
            <linearGradient id="gradient-accent" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="var(--accent)" stopOpacity="1" />
              <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
            </linearGradient>
          </defs>
        </svg>
      </div>

      {/* Simulated Histogram / Confidence Stats */}
      <div className="space-y-3">
        <div className="flex items-center justify-between text-xs font-mono">
          <span className="text-text-muted">Vegetation Index (NDVI)</span>
          <span className="text-text">{(dataPoints[5] / 100).toFixed(2)}</span>
        </div>
        <div className="h-2 w-full bg-sat-bg-primary overflow-hidden rounded">
          <div
            className="h-full bg-sat-accent transition-all duration-700 ease-in-out"
            style={{ width: `${dataPoints[5]}%` }}
          />
        </div>

        <div className="flex items-center justify-between text-xs font-mono">
          <span className="text-text-muted">Water Stress</span>
          <span className="text-text">{(dataPoints[15] / 100).toFixed(2)}</span>
        </div>
        <div className="h-2 w-full bg-sat-bg-primary overflow-hidden rounded">
          <div
            className="h-full bg-amber-500 transition-all duration-700 ease-in-out"
            style={{ width: `${dataPoints[15]}%` }}
          />
        </div>
      </div>
      
      <div className="mt-6 pt-4 border-t border-sat-border-alt flex gap-2 justify-end">
         <div className="h-2 w-2 rounded-full bg-sat-accent animate-pulse" />
         <span className="text-[10px] text-text-muted uppercase tracking-widest font-mono">Real-time sync</span>
      </div>
    </div>
  );
}
