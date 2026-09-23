export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  // get token from somewhere, assume localStorage for simplicity in this phase
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;
  
  const headers = new Headers(options.headers || {});
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    if (response.status === 401) {
      if (typeof window !== 'undefined') {
         localStorage.removeItem('access_token');
         window.location.href = '/auth';
      }
    }
    const errorBody = await response.json().catch(() => ({}));
    throw new Error(errorBody.detail || 'API Error');
  }

  return response.json();
}
