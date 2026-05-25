import type { CopilotResponse, CopilotTurn } from "@/types/api";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8001";

const REQUEST_TIMEOUT_MS = 5000;

async function requestJson<T>(url: string, options?: RequestInit, timeoutMs = REQUEST_TIMEOUT_MS): Promise<T> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

  const response = await fetch(url, {
    ...options,
    cache: "no-store",
    signal: options?.signal ?? controller.signal,
  }).finally(() => window.clearTimeout(timeoutId));

  if (!response.ok) {
    let errorMessage = `Request failed with status ${response.status}`;

    try {
      const errorBody = await response.json();
      errorMessage =
        errorBody.detail ||
        errorBody.message ||
        errorBody.error ||
        errorMessage;
    } catch {
      // ignore non-JSON errors
    }

    throw new Error(errorMessage);
  }

  return response.json() as Promise<T>;
}

export async function healthCheck() {
  return requestJson(`${API_BASE_URL}/health`);
}

export async function uploadDocuments(files: File[]) {
  const formData = new FormData();

  files.forEach((file) => {
    formData.append("files", file);
  });

  return requestJson(`${API_BASE_URL}/api/v1/upload`, {
    method: "POST",
    body: formData,
  });
}

export async function fetchDocuments() {
  return requestJson(`${API_BASE_URL}/api/v1/`);
}

export async function fetchDocument(documentId: string) {
  return requestJson(`${API_BASE_URL}/api/v1/${documentId}`);
}

export async function deleteDocument(documentId: string) {
  return requestJson(`${API_BASE_URL}/api/v1/${documentId}`, {
    method: "DELETE",
  });
}

export async function reprocessDocument(documentId: string) {
  return requestJson(`${API_BASE_URL}/api/v1/documents/${documentId}/reprocess`, {
    method: "POST",
  });
}

export async function downloadDocumentFile(documentId: string) {
  const response = await fetch(`${API_BASE_URL}/api/v1/documents/${documentId}/file`, {
    cache: "no-store",
  });

  if (!response.ok) {
    let message = `Source file request failed with status ${response.status}`;
    try {
      const errorBody = await response.json();
      message = errorBody.detail || message;
    } catch {
      // ignore non-JSON errors
    }
    throw new Error(message);
  }

  return response.blob();
}

export async function fetchRiskOverview() {
  return requestJson(`${API_BASE_URL}/api/v1/overview`);
}

export async function fetchDocumentFlags(documentId: string) {
  return requestJson(`${API_BASE_URL}/api/v1/flags/${documentId}`);
}

export async function fetchReports() {
  return requestJson(`${API_BASE_URL}/api/v1/reports/`);
}

export async function fetchReport(reportId: string) {
  return requestJson(`${API_BASE_URL}/api/v1/reports/${reportId}`);
}

export async function generateReport(documentId: string) {
  return requestJson(`${API_BASE_URL}/api/v1/reports/generate/${documentId}`, {
    method: "POST",
  });
}

export async function generateSessionReport() {
  return requestJson(`${API_BASE_URL}/api/v1/reports/generate`, {
    method: "POST",
  }, 45000);
}

export async function sendCopilotMessage(message: string, history: CopilotTurn[] = []) {
  return requestJson<CopilotResponse>(`${API_BASE_URL}/api/v1/copilot/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message, history }),
  }, 45000);
}

export async function downloadReport(reportId: string) {
  const response = await fetch(`${API_BASE_URL}/api/v1/reports/${reportId}/download`, {
    cache: "no-store",
  });

  if (!response.ok) {
    let message = `Download failed with status ${response.status}`;
    try {
      const errorBody = await response.json();
      message = errorBody.detail || message;
    } catch {
      // ignore non-JSON errors
    }
    throw new Error(message);
  }

  const blob = await response.blob();
  if (blob.type !== "application/pdf") {
    throw new Error("The server response is not a PDF file.");
  }
  return blob;
}

export function getReportDownloadUrl(reportId: string) {
  return `${API_BASE_URL}/api/v1/reports/${encodeURIComponent(reportId)}/download`;
}

// Backward-compatible aliases for old imports
export const fetchRisks = fetchRiskOverview;
export const fetchSampleReport = fetchReports;
