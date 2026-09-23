import React, { useState, useEffect } from 'react';

interface TraceData {
  id: number;
  query_id: number;
  plan: any[];
  steps: any[];
  verification_result: any;
  total_latency_ms: number;
  created_at: string;
}

interface TracePanelProps {
  queryId: number;
  apiUrl: string;
}

export const TracePanel: React.FC<TracePanelProps> = ({ queryId, apiUrl }) => {
  const [trace, setTrace] = useState<TraceData | null>(null);
  const [expanded, setExpanded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!expanded || trace) return;
    
    setLoading(true);
    const token = localStorage.getItem('token');
    fetch(`${apiUrl}/api/v1/query/${queryId}/trace`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        if (!res.ok) throw new Error('Trace not found or error loading trace');
        return res.json();
      })
      .then(data => setTrace(data))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [expanded, queryId, apiUrl, trace]);

  return (
    <div className="mt-4 border border-gray-700 rounded-lg bg-gray-900 text-sm overflow-hidden">
      <button 
        onClick={() => setExpanded(!expanded)}
        className="w-full px-4 py-2 flex items-center justify-between text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
      >
        <div className="flex items-center space-x-2">
          <svg className={`w-4 h-4 transform transition-transform ${expanded ? 'rotate-90' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
          </svg>
          <span className="font-semibold tracking-wide">How I got this answer</span>
        </div>
      </button>

      {expanded && (
        <div className="p-4 border-t border-gray-700 space-y-4">
          {loading && <div className="text-gray-400">Loading trace...</div>}
          {error && <div className="text-red-400">{error}</div>}
          
          {trace && (
            <>
              {/* GIS Verification Callout */}
              <div className="bg-gray-800 p-3 rounded-md mb-4 border-l-4 border-blue-500">
                <h4 className="font-semibold text-blue-400 mb-2">GIS Verification Step</h4>
                {trace.verification_result?.verification === 'true' ? (
                  <div className="text-green-400 font-medium">✓ Verified: {trace.verification_result.reason}</div>
                ) : trace.verification_result?.verification === 'false' ? (
                  <div className="text-red-400 font-medium">
                    ✗ Mismatched: {trace.verification_result.reason}
                  </div>
                ) : (
                  <div className="text-gray-400">
                    Not Applicable: {trace.verification_result?.reason || "No spatial claims to verify."}
                  </div>
                )}
              </div>

              {/* Execution Steps */}
              <div>
                <h4 className="font-semibold text-gray-300 mb-2">Execution Steps ({trace.total_latency_ms}ms)</h4>
                <div className="space-y-3">
                  {trace.steps.map((step, idx) => (
                    <div key={idx} className="bg-gray-800 p-3 rounded-md">
                      <div className="flex justify-between mb-1">
                        <span className="font-mono text-purple-400">{step.tool}()</span>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${step.status === 'success' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`}>
                          {step.status} ({step.latency_ms}ms)
                        </span>
                      </div>
                      
                      {step.error && (
                        <div className="text-red-400 text-xs mt-2 p-2 bg-red-900/20 rounded">
                          {step.error}
                        </div>
                      )}
                      
                      {step.output && Object.keys(step.output).length > 0 && (
                        <div className="text-gray-400 text-xs mt-2 overflow-x-auto">
                          <pre className="whitespace-pre-wrap font-mono">
                            {JSON.stringify(step.output, null, 2)}
                          </pre>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};
