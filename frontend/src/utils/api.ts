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

export const fetchProfessors = () => api.get('/api/professors/');
export const fetchDepartments = () => api.get('/api/departments/');
export const fetchCourses = () => api.get('/api/courses/');

export default api;
