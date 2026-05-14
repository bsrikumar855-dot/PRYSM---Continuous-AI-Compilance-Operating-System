// Copilot service
import { api } from './api';

export const copilotService = {
  chat: (message: string, documentId?: string) =>
    api.post('/copilot/chat', { message, document_id: documentId }),
  getSuggestions: (documentId: string) =>
    api.get(`/copilot/suggestions/${documentId}`),
};
