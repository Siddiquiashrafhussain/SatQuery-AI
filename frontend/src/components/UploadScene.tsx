"use client";
import { useState, useRef } from 'react';

interface UploadSceneProps {
  onUploadSuccess?: (scene: any) => void;
}

export default function UploadScene({ onUploadSuccess }: UploadSceneProps) {
  const [file, setFile] = useState<File | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');
  const [isUploading, setIsUploading] = useState<boolean>(false);
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateFile = (selectedFile: File) => {
    setError('');
    setSuccess('');
    const name = selectedFile.name.toLowerCase();
    if (!name.endsWith('.tif') && !name.endsWith('.tiff') && !name.endsWith('.geotiff')) {
      setError('Only GeoTIFF files (.tif, .tiff) are allowed.');
      return false;
    }
    // Warn if > 2GB (2 * 1024 * 1024 * 1024)
    if (selectedFile.size > 2147483648) {
      // Just a warning, not a block
      console.warn('File is larger than 2GB, upload may take a while.');
    }
    return true;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const selected = e.target.files[0];
      if (validateFile(selected)) setFile(selected);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const selected = e.dataTransfer.files[0];
      if (validateFile(selected)) setFile(selected);
    }
  };

  const uploadFile = async () => {
    if (!file) return;
    setIsUploading(true);
    setProgress(0);
    setError('');
    setSuccess('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
      
      const xhr = new XMLHttpRequest();
      xhr.open('POST', `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'}/imagery/upload`, true);
      if (token) {
        xhr.setRequestHeader('Authorization', `Bearer ${token}`);
      }

      xhr.upload.onprogress = (e) => {
        if (e.lengthComputable) {
          setProgress(Math.round((e.loaded / e.total) * 100));
        }
      };

      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          setSuccess('File uploaded successfully!');
          const data = JSON.parse(xhr.responseText);
          if (onUploadSuccess) onUploadSuccess(data.data || data);
          setFile(null);
        } else {
          try {
            const err = JSON.parse(xhr.responseText);
            setError(err.detail || 'Upload failed');
          } catch {
            setError('Upload failed');
          }
        }
        setIsUploading(false);
      };

      xhr.onerror = () => {
        setError('Network error occurred during upload');
        setIsUploading(false);
      };

      xhr.send(formData);
    } catch (err: any) {
      setError(err.message || 'Upload error');
      setIsUploading(false);
    }
  };

  return (
    <div className="w-full">
      <div 
        className={`border-2 border-dashed p-6 rounded-lg text-center cursor-pointer transition-colors ${
          file ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400 bg-white'
        }`}
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          className="hidden" 
          accept=".tif,.tiff,.geotiff" 
          onChange={handleFileChange} 
        />
        {file ? (
          <div className="text-sm">
            <p className="text-blue-600 font-medium truncate">{file.name}</p>
            <p className="text-gray-500">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
          </div>
        ) : (
          <p className="text-sm text-gray-500">Drag & drop a GeoTIFF here, or click to select</p>
        )}
      </div>

      {error && <p className="text-red-500 mt-2 text-xs font-medium">{error}</p>}
      {success && <p className="text-green-600 mt-2 text-xs font-medium">{success}</p>}

      {isUploading && (
        <div className="mt-3 w-full bg-gray-200 rounded-full h-1.5">
          <div className="bg-blue-600 h-1.5 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
        </div>
      )}

      <button 
        onClick={(e) => { e.stopPropagation(); uploadFile(); }}
        disabled={!file || isUploading}
        className={`mt-3 w-full py-2 text-sm rounded-md font-medium transition-colors ${
          !file || isUploading ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-blue-600 text-white hover:bg-blue-700'
        }`}
      >
        {isUploading ? `Uploading... ${progress}%` : 'Upload Scene'}
      </button>
    </div>
  );
}
