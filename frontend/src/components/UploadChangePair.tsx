"use client";

import { useState } from "react";

interface UploadChangePairProps {
  onPairSuccess: (pair: any) => void;
}

export default function UploadChangePair({ onPairSuccess }: UploadChangePairProps) {
  const [beforeFile, setBeforeFile] = useState<File | null>(null);
  const [afterFile, setAfterFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const handleUpload = async () => {
    if (!beforeFile || !afterFile) {
      setError("Please select both Before and After scenes");
      return;
    }

    setUploading(true);
    setProgress(10);
    setError(null);

    const token = localStorage.getItem("access_token");
    const headers = { Authorization: `Bearer ${token}` };

    try {
      // 1. Upload Before
      const formDataBefore = new FormData();
      formDataBefore.append("file", beforeFile);
      const resBefore = await fetch("http://localhost:8000/api/v1/imagery/upload", {
        method: "POST",
        headers,
        body: formDataBefore,
      });
      if (!resBefore.ok) throw new Error("Failed to upload Before scene");
      const beforeScene = await resBefore.json();
      setProgress(40);

      // 2. Upload After
      const formDataAfter = new FormData();
      formDataAfter.append("file", afterFile);
      const resAfter = await fetch("http://localhost:8000/api/v1/imagery/upload", {
        method: "POST",
        headers,
        body: formDataAfter,
      });
      if (!resAfter.ok) throw new Error("Failed to upload After scene");
      const afterScene = await resAfter.json();
      setProgress(80);

      // 3. Create Scene Pair
      const resPair = await fetch("http://localhost:8000/api/v1/imagery/pairs", {
        method: "POST",
        headers: { ...headers, "Content-Type": "application/json" },
        body: JSON.stringify({
          before_scene_id: beforeScene.id,
          after_scene_id: afterScene.id,
        }),
      });

      if (!resPair.ok) {
        const errData = await resPair.json();
        throw new Error(errData.detail || "Failed to create scene pair");
      }
      
      const pair = await resPair.json();
      setProgress(100);
      onPairSuccess({ ...pair, beforeScene, afterScene });
    } catch (err: any) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="w-full">
      <div className="space-y-4">
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">Before Scene (GeoTIFF)</label>
          <input 
            type="file" 
            accept=".tif,.tiff" 
            onChange={(e) => setBeforeFile(e.target.files?.[0] || null)}
            className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 border border-gray-200 rounded-md p-1"
          />
        </div>
        <div>
          <label className="block text-xs font-medium text-gray-700 mb-1">After Scene (GeoTIFF)</label>
          <input 
            type="file" 
            accept=".tif,.tiff" 
            onChange={(e) => setAfterFile(e.target.files?.[0] || null)}
            className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 border border-gray-200 rounded-md p-1"
          />
        </div>
        
        <button
          onClick={handleUpload}
          disabled={uploading || !beforeFile || !afterFile}
          className="w-full py-2 px-4 bg-blue-600 text-white rounded shadow text-sm font-medium disabled:opacity-50"
        >
          {uploading ? `Uploading & Processing...` : 'Upload Pair for Analysis'}
        </button>
      </div>

      {uploading && (
        <div className="mt-4">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-50 text-red-700 text-xs rounded border border-red-100">
          {error}
        </div>
      )}
    </div>
  );
}
