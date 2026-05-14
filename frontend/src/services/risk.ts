// Risk service
import { api } from './api';

export const riskService = {
  getOverview: () => api.get('/risk/overview'),
  getFlags: (documentId: string) => api.get(`/risk/flags/${documentId}`),
};
