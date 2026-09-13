export default function ConfidenceCard() {
    return (
      <div className="glass-panel p-5 flex flex-col gap-4">
        <div className="flex justify-between items-center">
            <h3 className="text-sm font-semibold text-gray-400 tracking-wider">CONFIDENCE</h3>
            <span className="text-xl font-bold text-green-400">85%</span>
        </div>
        <div className="w-full bg-gray-800 rounded-full h-2">
            <div className="bg-green-400 h-2 rounded-full" style={{ width: '85%' }}></div>
        </div>
        <p className="text-xs text-gray-400">
            Evidence-based assessment derived from object clarity and shadow analysis.
        </p>
      </div>
    );
  }
