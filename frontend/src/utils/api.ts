import axios from 'axios';
import config from '../config';
import AuthService from './auth';

// Create an axios instance with default config
const api = axios.create({
  baseURL: config.apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
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
  
  // Log request for debugging
  console.log('API Request:', {
    url: request.url,
    method: request.method,
    headers: request.headers,
    baseURL: request.baseURL
  });
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

    console.error('API Error:', {
      url: error.config?.url,
      method: error.config?.method,
      headers: error.config?.headers,
      status: error.response?.status,
      data: error.response?.data
    });
    return Promise.reject(error);
  }
);

// Initialize auth service when the app starts
const initializeAuth = async () => {
  const auth = AuthService.getInstance();
  await auth.initialize();
};

initializeAuth().catch(console.error);

export const fetchProfessors = () => api.get('/api/professors/');
export const fetchDepartments = () => api.get('/api/departments/');
export const fetchCourses = () => api.get('/api/courses/');

export default api;
