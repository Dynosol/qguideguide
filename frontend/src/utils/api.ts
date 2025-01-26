import axios from 'axios';
import config from '../config';

const api = axios.create({
    baseURL: config.apiBaseUrl,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    },
    withCredentials: true  // Important for session cookies
});

// Handle session token management
let sessionToken: string | null = localStorage.getItem('session_token');

// Add token to requests if available
api.interceptors.request.use(config => {
    if (sessionToken) {
        config.headers['X-Session-Token'] = sessionToken;
    }
    return config;
});

// Store session token from response headers
api.interceptors.response.use(response => {
    const newToken = response.headers['x-session-token'];
    if (newToken) {
        sessionToken = newToken;
        localStorage.setItem('session_token', newToken);
    }
    return response;
}, error => {
    if (error.response?.status === 401) {
        // Clear invalid token
        sessionToken = null;
        localStorage.removeItem('session_token');
    }
    return Promise.reject(error);
});

// Export API functions
export const fetchCourses = () => api.get('/api/courses/');
export const fetchProfessors = () => api.get('/api/professors/');
export const fetchDepartments = () => api.get('/api/departments/');

export default api;
