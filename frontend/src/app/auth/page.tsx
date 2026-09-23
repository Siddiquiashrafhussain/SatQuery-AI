"use client";
import { useState } from 'react';
import { API_BASE_URL } from '@/lib/api';

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setMessage('');
    
    try {
      if (isLogin) {
        const formData = new URLSearchParams();
        formData.append('username', email); // OAuth2 expects username
        formData.append('password', password);
        
        const res = await fetch(`${API_BASE_URL}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: formData.toString()
        });
        
        if (!res.ok) {
           const err = await res.json();
           throw new Error(err.detail || 'Login failed');
        }
        const data = await res.json();
        localStorage.setItem('access_token', data.access_token);
        document.cookie = `token=${data.access_token}; path=/; max-age=604800`; // 1 week
        setMessage('Logged in successfully!');
        window.location.href = '/dashboard';
      } else {
        const res = await fetch(`${API_BASE_URL}/auth/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password })
        });
        
        if (!res.ok) {
           const err = await res.json();
           throw new Error(err.detail || 'Registration failed');
        }
        setMessage('Registered successfully! You can now log in.');
        setIsLogin(true);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4 bg-black text-white">
      <div className="w-full max-w-md p-8 bg-zinc-900 border border-zinc-800 rounded-lg shadow-xl">
        <h1 className="text-2xl font-bold text-center mb-6">{isLogin ? 'Login' : 'Register'}</h1>
        
        {error && <div className="p-3 mb-4 text-sm text-red-500 bg-red-900/20 border border-red-900 rounded">{error}</div>}
        {message && <div className="p-3 mb-4 text-sm text-green-500 bg-green-900/20 border border-green-900 rounded">{message}</div>}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Email</label>
            <input 
              type="email" 
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full p-2 bg-zinc-950 border border-zinc-800 rounded focus:ring focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full p-2 bg-zinc-950 border border-zinc-800 rounded focus:ring focus:ring-blue-500"
            />
          </div>
          <button type="submit" className="w-full py-2 bg-white text-black font-semibold rounded hover:bg-zinc-200">
            {isLogin ? 'Log In' : 'Sign Up'}
          </button>
        </form>
        
        <p className="mt-4 text-center text-sm text-zinc-400">
          {isLogin ? "Don't have an account? " : "Already have an account? "}
          <button onClick={() => setIsLogin(!isLogin)} className="text-white underline">
            {isLogin ? 'Register here' : 'Login here'}
          </button>
        </p>
      </div>
    </div>
  );
}
