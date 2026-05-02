// API Client - fetch wrapper with JWT
const API_BASE = '/api';

async function apiRequest(endpoint, options = {}) {
    const token = localStorage.getItem('token');
    const headers = { 'Content-Type': 'application/json', ...options.headers };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
    const data = await response.json();

    if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login.html';
        return;
    }

    if (!response.ok) throw new Error(data.error || 'Something went wrong');
    return data;
}

const api = {
    get: (endpoint) => apiRequest(endpoint),
    post: (endpoint, body) => apiRequest(endpoint, { method: 'POST', body: JSON.stringify(body) }),
    put: (endpoint, body) => apiRequest(endpoint, { method: 'PUT', body: JSON.stringify(body) }),
    delete: (endpoint) => apiRequest(endpoint, { method: 'DELETE' }),
};
