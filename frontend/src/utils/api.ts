import axios from 'axios';
import config from '../config';

// Create an axios instance with default config
const api = axios.create({
  baseURL: config.apiBaseUrl,
  headers: {
    'X-API-Key': config.apiKey,
    'Content-Type': 'application/json',
  },
});

// Add request interceptor for logging
api.interceptors.request.use(request => {
  console.log('API Request:', {
    url: request.url,
    method: request.method,
    headers: request.headers,
    baseURL: request.baseURL
  });
  return request;
});

export const fetchProfessors = () => api.get('/api/professors/');
export const fetchDepartments = () => api.get('/api/departments/');
export const fetchCourses = () => api.get('/api/courses/');

export default api;
