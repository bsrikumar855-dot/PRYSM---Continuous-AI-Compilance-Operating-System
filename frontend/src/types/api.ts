export type Severity = "Critical" | "Warning" | "Info" | "High" | "Medium" | "Low" | string;

export interface DocumentData {
  document_type?: string;
  amount?: string;
  date?: string;
  gstin?: string;
  invoice_number?: string;
  vendor_name?: string;
  [key: string]: unknown;
}

export interface RiskObject {
  id?: string;
  type?: string;
  severity?: Severity;
  title?: string;
  message?: string;
  source_document?: string;
  recommendation?: string;
  [key: string]: unknown;
}

export interface DocumentScreening {
  decision?: "accepted" | "review_required" | "excluded" | string;
  audit_eligible?: boolean;
  category?: string;
  label?: string;
  confidence?: number;
  reason?: string;
}

export interface UploadedDocument {
  id?: string;
  document_id?: string;
  filename?: string;
  status?: string;
  data?: DocumentData;
  risks?: RiskObject[];
  screening?: DocumentScreening;
  screening_reason?: string;
  raw_text_preview?: string;
  error?: string | null;
  [key: string]: unknown;
}

export interface UploadResponse {
  status?: string;
  documents?: UploadedDocument[];
  document?: UploadedDocument;
  [key: string]: unknown;
}

export interface RiskOverviewResponse {
  status?: string;
  risks?: RiskObject[];
  flags?: RiskObject[];
  total_risks?: number;
  critical_count?: number;
  warning_count?: number;
  info_count?: number;
  [key: string]: unknown;
}

export interface ReportsResponse {
  status?: string;
  reports?: unknown[];
  data?: unknown[];
  [key: string]: unknown;
}

export interface HealthResponse {
  status?: string;
  service?: string;
  [key: string]: unknown;
}

export interface CopilotTurn {
  role: "user" | "assistant";
  content: string;
}

export interface CopilotResponse {
  status?: string;
  message?: string;
  powered_by?: "llm" | "fallback" | string;
  model?: string | null;
}
