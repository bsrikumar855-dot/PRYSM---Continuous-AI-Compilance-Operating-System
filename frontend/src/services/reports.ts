// Report service
import { api } from './api';

export const reportService = {
  list: () => api.get('/reports/'),
  get: (id: string) => api.get(`/reports/${id}`),
  generate: (documentId: string) => api.post(`/reports/generate/${documentId}`),
};
