import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  profile: () => api.get('/auth/profile'),
};

export const groupAPI = {
  list: () => api.get('/groups'),
  create: (data) => api.post('/groups', data),
  members: (groupId) => api.get(`/groups/${groupId}/members`),
  addMember: (groupId, data) => api.post(`/groups/${groupId}/members`, data),
};

export const billAPI = {
  list: () => api.get('/bills'),
  create: (data) => api.post('/bills', data),
  get: (billId) => api.get(`/bills/${billId}`),
  addItem: (billId, data) => api.post(`/bills/${billId}/items`, data),
};

export const settlementAPI = {
  get: (billId) => api.get(`/settlement/${billId}`),
};

export const receiptAPI = {
  upload: (file) => {
    const formData = new FormData();
    formData.append('image', file);
    return api.post('/receipt/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
};

export const notificationAPI = {
  list: () => api.get('/notifications'),
};

export const formatRupiah = (amount) =>
  new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(amount);
