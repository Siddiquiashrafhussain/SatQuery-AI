'use client';

interface Props {
  complete: boolean;
}

export default function AnalysisStatus({ complete }: Props) {
  const steps = [
    { name: "Input Validated", done: complete },
    { name: "Task Detected", done: complete },
    { name: "Model Selected", done: complete },
    { name: "Analysis Done", done: complete },
  ];

  return (
    <div className="glass-panel p-5 flex flex-col gap-4">
      <h3 className="text-sm font-semibold text-gray-400 tracking-wider">ANALYSIS STATUS</h3>
      <ul className="flex flex-col gap-2">
        {steps.map((step, i) => (
          <li key={i} className={`flex items-center gap-3 text-sm font-medium ${step.done ? 'text-green-400' : 'text-gray-400'}`}>
            <div className={`w-5 h-5 rounded-full flex items-center justify-center border ${step.done ? 'border-green-400 bg-green-400/20' : 'border-gray-600 bg-gray-800'}`}>
                {step.done ? (
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                ) : (
                    <span className="w-1.5 h-1.5 bg-gray-500 rounded-full" />
                )}
            </div>
            {step.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
