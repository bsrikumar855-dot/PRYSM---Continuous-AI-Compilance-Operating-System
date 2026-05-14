// Risk types
export interface RiskFlag {
  id: string;
  document_id: string;
  risk_level: 'critical' | 'high' | 'medium' | 'low' | 'info';
  category: string;
  description: string;
  recommendation: string;
  evidence_ref: string | null;
}

export interface RiskOverview {
  total_flags: number;
  critical: number;
  high: number;
  medium: number;
  low: number;
  risk_score: number;
  flags: RiskFlag[];
}
