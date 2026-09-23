"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import MapViewer from "@/components/MapViewer";
import UploadScene from "@/components/UploadScene";
import UploadChangePair from "@/components/UploadChangePair";
import QueryPanel from "@/components/QueryPanel";

export default function DashboardPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"single" | "change">("single");
  const [activeScene, setActiveScene] = useState<any>(null);
  const [activePair, setActivePair] = useState<any>(null);
  const [activeQueryResult, setActiveQueryResult] = useState<any>(null);

  useEffect(() => {
    // Basic unauthenticated redirect for client-side
    const token = localStorage.getItem("access_token");
    if (!token) {
      router.push("/auth");
    }
  }, [router]);

  return (
    <div className="flex h-full w-full">
      {/* Left Sidebar */}
      <aside className="w-80 border-r border-gray-200 bg-white flex flex-col z-10 shadow-sm overflow-y-auto">
        <div className="flex border-b border-gray-200">
          <button 
            onClick={() => setMode("single")} 
            className={`flex-1 py-3 text-xs font-semibold uppercase tracking-wider ${mode === "single" ? "bg-blue-50 text-blue-700 border-b-2 border-blue-600" : "text-gray-500 hover:bg-gray-50"}`}
          >
            Single Image
          </button>
          <button 
            onClick={() => setMode("change")} 
            className={`flex-1 py-3 text-xs font-semibold uppercase tracking-wider ${mode === "change" ? "bg-blue-50 text-blue-700 border-b-2 border-blue-600" : "text-gray-500 hover:bg-gray-50"}`}
          >
            Change Analysis
          </button>
        </div>
        
        <div className="p-4 border-b border-gray-200">
          {mode === "single" ? (
            <UploadScene onUploadSuccess={(scene) => { setActiveScene(scene); setActivePair(null); setActiveQueryResult(null); }} />
          ) : (
            <UploadChangePair onPairSuccess={(pair) => { setActivePair(pair); setActiveScene(null); setActiveQueryResult(null); }} />
          )}
        </div>
        
        <div className="p-4 flex-1 flex flex-col">
          <h2 className="text-sm font-semibold text-gray-700 uppercase tracking-wider mb-4">Query</h2>
          {mode === "single" ? (
            activeScene ? (
              <QueryPanel sceneId={activeScene.id} onQueryResult={(res) => setActiveQueryResult(res)} />
            ) : (
              <div className="text-sm text-gray-500 italic bg-gray-50 p-4 rounded-md border border-gray-100">
                Upload and select a scene to start querying.
              </div>
            )
          ) : (
            activePair ? (
               <QueryPanel scenePairId={activePair.id} onQueryResult={(res) => setActiveQueryResult(res)} />
            ) : (
              <div className="text-sm text-gray-500 italic bg-gray-50 p-4 rounded-md border border-gray-100">
                Upload a Before and After pair to run change detection.
              </div>
            )
          )}
        </div>
      </aside>

      {/* Main Map Area */}
      <main className="flex-1 relative bg-gray-100">
        <MapViewer activeScene={activeScene} activePair={activePair} activeQueryResult={activeQueryResult} />
      </main>
    </div>
  );
}
