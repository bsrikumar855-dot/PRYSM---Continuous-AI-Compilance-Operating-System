export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8001";

async function requestJson<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);

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

export async function downloadReport(reportId: string) {
  const response = await fetch(`${API_BASE_URL}/api/v1/reports/${reportId}/download`);

  if (!response.ok) {
    throw new Error(`Download failed with status ${response.status}`);
  }

  return response.blob();
}

// Backward-compatible aliases for old imports
export const fetchRisks = fetchRiskOverview;
export const fetchSampleReport = fetchReports;
