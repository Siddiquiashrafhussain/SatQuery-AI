"use client";

import { ReactNode } from "react";
import { useRouter } from "next/navigation";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  const router = useRouter();
  
  const handleLogout = () => {
    localStorage.removeItem("access_token");
    document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    router.push("/auth");
  };

  return (
    <div className="flex h-screen w-full flex-col bg-gray-50 text-gray-900">
      <header className="flex items-center justify-between bg-white px-6 py-4 shadow-sm border-b border-gray-200">
        <h1 className="text-xl font-bold text-gray-800">🛰️ SatQuery AI</h1>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-500">Workspace</span>
          <button 
            onClick={handleLogout}
            className="text-sm font-medium text-red-600 hover:text-red-700 transition-colors"
          >
            Logout
          </button>
        </div>
      </header>
      <main className="flex-1 overflow-hidden relative">{children}</main>
    </div>
  );
}
