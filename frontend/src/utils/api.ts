import axios from 'axios';
import config from '../config';

// Create an axios instance with default config
const api = axios.create({
  baseURL: config.apiBaseUrl,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

// API functions
export const fetchCourses = () => {
  return api.get('/api/courses/');
};

export const fetchProfessors = () => {
  return api.get('/api/professors/');
};

export const fetchDepartments = () => {
  return api.get('/api/departments/');
};

export default api;
