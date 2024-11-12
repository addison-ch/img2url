const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function fetchData() {
  const response = await fetch(`${API_BASE_URL}/your-endpoint`);
  const data = await response.json();
  return data;
}