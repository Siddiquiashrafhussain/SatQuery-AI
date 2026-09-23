"use client";
import { useState } from 'react';
import { TracePanel } from './TracePanel';

interface QueryPanelProps {
  sceneId?: number;
  scenePairId?: number;
  onQueryResult?: (result: any) => void;
}

export default function QueryPanel({ sceneId, scenePairId, onQueryResult }: QueryPanelProps) {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!scenePairId && !query.trim()) return;
    
    setIsLoading(true);
    setError('');
    
    try {
      const token = localStorage.getItem('access_token');
      
      let endpoint = '/query';
      let body: any = { scene_id: sceneId, query_text: query };
      
      if (scenePairId) {
        endpoint = '/query/change';
        body = { scene_pair_id: scenePairId };
      }
      
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { 'Authorization': `Bearer ${token}` } : {})
        },
        body: JSON.stringify(body)
      });
      
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || 'Analysis failed');
      }
      
      const data = await res.json();
      setResponse(data);
      if (onQueryResult) {
        onQueryResult(data);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto mb-4 bg-gray-50 rounded-md border border-gray-200 p-4">
        {response ? (
          <div className="space-y-3 text-sm">
            <div className="bg-white p-3 rounded shadow-sm border border-gray-100">
              <strong className="text-gray-500 uppercase text-xs tracking-wider block mb-1">Your Query</strong>
              <p className="text-gray-800">{query}</p>
            </div>
            <div className="bg-blue-50 p-3 rounded shadow-sm border border-blue-100 relative">
              <div className="flex justify-between items-start mb-2">
                <strong className="text-blue-600 uppercase text-xs tracking-wider">Analysis Result</strong>
                {response.confidence !== null ? (
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium text-white ${
                    response.confidence >= 0.75 ? 'bg-green-500' :
                    response.confidence >= 0.50 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}>
                    {Math.round(response.confidence * 100)}% Confidence
                  </span>
                ) : (
                  <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-gray-200 text-gray-600">
                    Unverified
                  </span>
                )}
              </div>
              <p className="text-gray-900">{response.answer || response.summary}</p>
            </div>
            {response.query_id && (
              <TracePanel queryId={response.query_id} apiUrl={process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'} />
            )}
          </div>
        ) : (
          <div className="h-full flex items-center justify-center text-gray-400 text-sm">
            Results will appear here
          </div>
        )}
        
        {error && (
          <div className="mt-4 p-3 bg-red-50 text-red-600 text-sm rounded border border-red-100">
            {error}
          </div>
        )}
      </div>
      
      <form onSubmit={handleSubmit} className="relative">
        {scenePairId ? (
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium text-sm flex justify-center items-center gap-2"
          >
            {isLoading ? (
              <>
                <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </>
            ) : (
              "Run Change Detection"
            )}
          </button>
        ) : (
          <>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask a question about this scene..."
              className="w-full h-24 p-3 pr-12 text-sm bg-white border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-none"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !query.trim()}
              className="absolute bottom-3 right-3 p-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? (
                <svg className="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              )}
            </button>
          </>
        )}
      </form>
    </div>
  );
}
