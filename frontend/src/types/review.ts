// Review types
export interface ReviewTask {
  id: string;
  document_id: string;
  assigned_to: string | null;
  status: 'pending' | 'in_progress' | 'approved' | 'rejected' | 'escalated';
  priority: string;
  notes: string | null;
  created_at: string;
  resolved_at: string | null;
}
