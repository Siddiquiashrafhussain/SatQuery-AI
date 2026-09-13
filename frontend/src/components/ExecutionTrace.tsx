export default function ExecutionTrace() {
    const traces = [
        "Input Validation ✓",
        "Query Understanding ✓",
        "Model Selection (RemoteSensingVQAModel) ✓",
        "Spatial Analysis (Rasterio) ✓",
        "Verification ✓"
    ];

    return (
      <div className="glass-panel p-5 flex flex-col gap-4">
        <h3 className="text-sm font-semibold text-gray-400 tracking-wider">EXECUTION TRACE</h3>
        <div className="flex flex-col gap-2 border-l-2 border-gray-700 ml-2 pl-4">
            {traces.map((trace, i) => (
                <div key={i} className="text-xs text-gray-300 relative">
                    <span className="absolute -left-[21px] top-1 w-2 h-2 bg-gray-500 rounded-full border border-gray-900" />
                    {trace}
                </div>
            ))}
        </div>
      </div>
    );
  }
