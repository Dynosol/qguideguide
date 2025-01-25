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

  return request;
});

// Add response interceptor for error handling and token refresh
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    // If error is 401 and we haven't tried refreshing token yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const auth = AuthService.getInstance();
        const newToken = await auth.handleTokenRefresh();
        
        // Update the failed request with new token and retry
        originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
        return axios(originalRequest);
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        return Promise.reject(refreshError);
      }
    }

    // Log CORS and other errors
    if (error.response) {
      console.error('API Error:', {
        url: error.config?.url,
        method: error.config?.method,
        status: error.response.status,
        statusText: error.response.statusText,
        headers: {
          request: error.config?.headers,
          response: error.response.headers
        },
        data: error.response.data
      });
    } else if (error.request) {
      console.error('Network Error:', {
        url: error.config?.url,
        method: error.config?.method,
        error: error.message
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
