import Link from 'next/link';

export default function Home() {
  return (
    <main className="flex h-screen w-full justify-center items-center bg-sat-bg-primary text-white overflow-hidden relative">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-sat-bg-secondary to-sat-bg-primary opacity-80" />
      
      <div className="z-10 glass-panel p-16 max-w-2xl text-center flex flex-col items-center">
        <div className="w-20 h-20 rounded-2xl bg-sat-accent flex justify-center items-center mb-8 shadow-[0_0_40px_rgba(59,130,246,0.5)]">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2.5a2.5 2.5 0 0 0-2.5 2.5v14a2.5 2.5 0 0 0 5 0V5a2.5 2.5 0 0 0-2.5-2.5Z"/>
            <path d="M15 12h4a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-4"/>
            <path d="M9 12H5a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h4"/>
          </svg>
        </div>
        
        <h1 className="text-5xl font-extrabold mb-6 tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
          SatQuery AI
        </h1>
        
        <p className="text-xl text-gray-400 mb-10 leading-relaxed">
          Interactive Vision-Language Assistant for Multimodal Remote Sensing Image Analysis.
        </p>
        
        <Link 
          href="/analysis"
          className="bg-sat-accent hover:bg-sat-accent-hover text-white px-8 py-4 rounded-xl font-bold text-lg transition-all shadow-[0_4px_20px_0_rgba(59,130,246,0.4)] hover:-translate-y-[2px]"
        >
          Launch Workspace
        </Link>
      </div>
    </main>
  );
}
