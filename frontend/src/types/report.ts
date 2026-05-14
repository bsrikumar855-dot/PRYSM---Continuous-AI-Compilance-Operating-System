// Report types
export interface ReportSummary {
  id: string;
  document_id: string;
  report_type: string;
  status: string;
  generated_at: string;
  download_url: string | null;
}

export interface ReportDetail extends ReportSummary {
  compliance_score: number;
  total_rules_checked: number;
  passed: number;
  failed: number;
  warnings: number;
  risk_score: number;
}
