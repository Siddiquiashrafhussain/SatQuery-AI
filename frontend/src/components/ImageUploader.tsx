'use client';

interface Props {
  onUpload: () => void;
  uploaded: boolean;
}

export default function ImageUploader({ onUpload, uploaded }: Props) {
  return (
    <div className="glass-panel p-5 flex flex-col gap-3">
      <h3 className="text-sm font-semibold text-gray-400 tracking-wider">UPLOAD SATELLITE IMAGE</h3>
      
      {!uploaded ? (
        <button 
            onClick={onUpload}
            className="w-full border-2 border-dashed border-gray-600 hover:border-sat-accent bg-black/20 hover:bg-sat-accent/10 transition-colors rounded-xl h-32 flex flex-col items-center justify-center gap-2 cursor-pointer group"
        >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-gray-400 group-hover:text-sat-accent transition-colors">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <span className="text-gray-400 font-medium text-sm">Drag & Drop or Click to Upload</span>
        </button>
      ) : (
        <div className="w-full border border-green-500/30 bg-green-500/10 rounded-xl h-24 flex items-center p-4 gap-4">
             <div className="w-16 h-16 bg-gray-800 rounded flex items-center justify-center border border-gray-700">
                <span className="text-xs text-gray-500">TIFF</span>
             </div>
             <div className="flex flex-col">
                 <span className="text-white font-medium">sample_optical_1.tif</span>
                 <span className="text-xs text-green-400 font-semibold mt-1 flex items-center gap-1">
                     <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                     Ready for Analysis
                 </span>
             </div>
        </div>
      )}
    </div>
  );
}
