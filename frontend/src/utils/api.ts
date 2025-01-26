import axios from 'axios';
import config from '../config';

const api = axios.create({
    baseURL: config.apiBaseUrl,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
});

// Export API functions
export const fetchCourses = () => api.get('/api/courses/');
export const fetchProfessors = () => api.get('/api/professors/');
export const fetchDepartments = () => api.get('/api/departments/');

export default api;
