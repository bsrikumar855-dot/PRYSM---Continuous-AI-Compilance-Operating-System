// Document types
export interface Document {
  id: string;
  filename: string;
  document_type: string | null;
  status: string;
  page_count: number;
  file_size_bytes: number;
  uploaded_at: string;
  processed_at: string | null;
  extracted_entities: Record<string, unknown>;
}
