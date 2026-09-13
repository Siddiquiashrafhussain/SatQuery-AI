'use client';
import { useState } from 'react';

interface Props {
  onAnalyze: () => void;
  disabled: boolean;
  isAnalyzing: boolean;
}

export default function QueryBox({ onAnalyze, disabled, isAnalyzing }: Props) {
  const [query, setQuery] = useState('');

  return (
    <div className="glass-panel p-5 flex flex-col gap-3">
      <h3 className="text-sm font-semibold text-gray-400 tracking-wider">ASK YOUR QUESTION</h3>
      <textarea 
        className="w-full bg-black/30 border border-white/10 rounded-lg p-3 text-white placeholder:text-gray-500 focus:outline-none focus:border-sat-accent resize-none h-24"
        placeholder="e.g. What objects are visible near the road?"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={disabled && !isAnalyzing}
      />
      <button 
        onClick={onAnalyze}
        disabled={disabled || query.trim() === ''}
        className={`w-full py-3 rounded-lg font-bold transition-all ${
            disabled || query.trim() === '' 
            ? 'bg-gray-800 text-gray-500 cursor-not-allowed' 
            : 'bg-sat-accent hover:bg-sat-accent-hover text-white shadow-[0_0_15px_rgba(59,130,246,0.3)]'
        }`}
      >
        {isAnalyzing ? (
            <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                Analyzing...
            </span>
        ) : 'Analyse'}
      </button>
    </div>
  );
}
