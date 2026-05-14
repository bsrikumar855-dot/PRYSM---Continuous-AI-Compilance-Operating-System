// Compliance service
import { api } from './api';

export const complianceService = {
  runCheck: (documentId: string) => api.post(`/compliance/run/${documentId}`),
  getResults: (documentId: string) => api.get(`/compliance/results/${documentId}`),
  listResults: () => api.get('/compliance/results'),
};
