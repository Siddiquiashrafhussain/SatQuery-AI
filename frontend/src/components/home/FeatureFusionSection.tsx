import { AnalyticsPreviewWidget } from "./AnalyticsPreviewWidget";

export function FeatureFusionSection() {
  return (
    <section className="py-24 bg-sat-bg-primary border-t border-sat-border relative overflow-hidden">
      {/* Decorative Grid */}
      <div 
        className="absolute inset-0 pointer-events-none opacity-[0.03]" 
        style={{ backgroundImage: 'linear-gradient(to right, #ffffff 1px, transparent 1px), linear-gradient(to bottom, #ffffff 1px, transparent 1px)', backgroundSize: '40px 40px' }}
      />
      
      <div className="max-w-[1200px] mx-auto px-6 relative z-10">
        <div className="text-center max-w-2xl mx-auto mb-20">
          <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-6">Multi-Modal Fusion</h2>
          <p className="text-text-muted text-lg">
            Harness the combined power of optical imagery and Synthetic Aperture Radar (SAR) to penetrate cloud cover and extract robust, verified intelligence.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          
          <div className="space-y-10">
            <div className="flex gap-4">
              <div className="flex-shrink-0 mt-1">
                <div className="w-8 h-8 rounded bg-sat-surface border border-sat-border flex items-center justify-center text-sat-accent">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                </div>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">Optical Analysis</h3>
                <p className="text-text-muted leading-relaxed">
                  Deep semantic understanding of land-cover, identifying subtle changes in vegetation, construction, and infrastructure over time using multispectral bands.
                </p>
              </div>
            </div>
            
            <div className="flex gap-4">
              <div className="flex-shrink-0 mt-1">
                <div className="w-8 h-8 rounded bg-sat-surface border border-sat-border flex items-center justify-center text-amber-500">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 22h14a2 2 0 0 0 2-2V7.5L14.5 2H6a2 2 0 0 0-2 2v4"/><polyline points="14 2 14 8 20 8"/><path d="m3 15 2 2 4-4"/></svg>
                </div>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">SAR Penetration</h3>
                <p className="text-text-muted leading-relaxed">
                  All-weather, day-and-night capability. Detect structural and volumetric changes even through heavy cloud cover or dense canopy using C-band backscatter data.
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <div className="flex-shrink-0 mt-1">
                <div className="w-8 h-8 rounded bg-sat-surface border border-sat-border flex items-center justify-center text-purple-500">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
                </div>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">Cross-Modal Validation</h3>
                <p className="text-text-muted leading-relaxed">
                  Our evidence engine fuses assertions from multiple models, cross-validating claims to drastically reduce hallucinations and guarantee high-confidence intelligence.
                </p>
              </div>
            </div>
          </div>

          <div className="relative">
            <div className="absolute -inset-4 bg-sat-accent/5 rounded-xl blur-2xl pointer-events-none" />
            <AnalyticsPreviewWidget className="w-full max-w-md ml-auto mr-auto lg:mr-0 relative z-10" />
          </div>

        </div>
      </div>
    </section>
  );
}
