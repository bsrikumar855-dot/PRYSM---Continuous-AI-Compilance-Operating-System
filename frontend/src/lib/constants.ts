// Frontend constants
export const APP_NAME = 'PRYSM';
export const APP_DESCRIPTION = 'Continuous AI Compliance Operating System';

export const COMPLIANCE_STATUS_COLORS = {
  pass: 'text-green-500',
  fail: 'text-red-500',
  warning: 'text-amber-500',
  pending_review: 'text-blue-500',
} as const;

export const RISK_LEVEL_COLORS = {
  critical: 'text-red-600 bg-red-50',
  high: 'text-orange-600 bg-orange-50',
  medium: 'text-amber-600 bg-amber-50',
  low: 'text-green-600 bg-green-50',
  info: 'text-blue-600 bg-blue-50',
} as const;
