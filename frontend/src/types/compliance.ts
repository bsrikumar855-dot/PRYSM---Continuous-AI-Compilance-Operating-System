// Compliance types
export interface ComplianceRuleResult {
  rule_id: string;
  rule_name: string;
  domain: string;
  status: 'pass' | 'fail' | 'warning';
  severity: 'critical' | 'high' | 'medium' | 'low';
  message: string;
  evidence_ref: string | null;
}

export interface ComplianceCheckResponse {
  document_id: string;
  overall_status: string;
  score: number;
  results: ComplianceRuleResult[];
  checked_at: string;
}
