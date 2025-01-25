import axios from 'axios';
import config from '../config';
import AuthService from './auth';

// Create an axios instance with default config
const api = axios.create({
  baseURL: config.apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  withCredentials: true, // Enable sending cookies with requests
});

// Add request interceptor for JWT token
api.interceptors.request.use(async request => {
  const auth = AuthService.getInstance();
  const token = auth.getAccessToken();
  
  if (token) {
    request.headers['Authorization'] = `Bearer ${token}`;
  }

  // Add API key if available
  if (config.apiKey) {
    request.headers['x-api-key'] = config.apiKey;
  }

  // Add CORS headers
  request.headers['Origin'] = window.location.origin;
  
  return request;
});

// Add response interceptor to handle errors
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      // Server responded with error status
      console.error('API Error:', {
        status: error.response.status,
        data: error.response.data,
        headers: error.response.headers,
      });
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', {
        url: error.config.url,
        method: error.config.method,
        error: error.message,
      });
    }
    return Promise.reject(error);
  }
);

// Initialize auth service when the app starts
const initializeAuth = async () => {
  const auth = AuthService.getInstance();
  await auth.initialize();
};

// Initialize API
const initializeAPI = async () => {
  try {
    await initializeAuth();
    // Only fetch professors and departments initially
    await Promise.all([
      fetchProfessors(),
      fetchDepartments()
    ]);
  } catch (error) {
    console.error('API initialization failed:', error);
  }
};

initializeAPI().catch(console.error);

export const fetchProfessors = (headers = {}) => api.get('/api/professors/', {
  headers: {
    'Cache-Control': 'public, max-age=3600',
    ...headers
  }
});

export const fetchDepartments = (headers = {}) => api.get('/api/departments/', {
  headers: {
    'Cache-Control': 'public, max-age=3600',
    ...headers
  }
});

export const fetchCourses = (headers = {}) => api.get('/api/courses/', {
  headers: {
    'Cache-Control': 'public, max-age=3600',
    ...headers
  }
});

export default api;
