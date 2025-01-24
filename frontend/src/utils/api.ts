import axios from 'axios';
import config from '../config';

// Create an axios instance with default config
const api = axios.create({
  baseURL: config.apiBaseUrl,
  headers: {
    'X-API-Key': config.apiKey,
    'Content-Type': 'application/json',
  },
  withCredentials: true, // Enable sending cookies with requests
});

// Add request interceptor for logging and header consistency
api.interceptors.request.use(request => {
  // Ensure API key is set for all requests including HEAD
  if (!request.headers['X-API-Key']) {
    request.headers['X-API-Key'] = config.apiKey;
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

// Add response interceptor for error handling
api.interceptors.response.use(
  response => response,
  error => {
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

export const fetchProfessors = () => api.get('/api/professors/');
export const fetchDepartments = () => api.get('/api/departments/');
export const fetchCourses = () => api.get('/api/courses/');

export default api;
