// Document service
import { api } from './api';

export const documentService = {
  upload: (file: File) => api.upload('/documents/upload', file),
  list: () => api.get('/documents/'),
  get: (id: string) => api.get(`/documents/${id}`),
  delete: (id: string) => api.delete(`/documents/${id}`),
};
