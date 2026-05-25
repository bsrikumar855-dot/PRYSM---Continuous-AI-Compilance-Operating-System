"use client";

import { useEffect, useMemo, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Download, Printer, Share2, FileText, CheckCircle2, AlertTriangle, ShieldAlert, Loader2, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";
import { downloadReport, fetchReports, generateSessionReport } from "@/lib/api";
import type { ReportsResponse } from "@/types/api";

type ReportRisk = {
  id?: string;
  issue?: string;
  entity?: string;
  impact?: string;
};

type ReportMetrics = {
  readinessScore?: number;
  readinessTotal?: number;
  evidenceQualityScore?: number;
  criticalRisks?: number;
  complianceGaps?: number;
};

type BackendReport = {
  id: string;
  title: string;
  fileName?: string;
  date?: string;
  status?: string;
  generatedBy?: string;
  preparedFor?: string;
  period?: string;
  summary?: string;
  metrics?: ReportMetrics;
  topRisks?: ReportRisk[];
  pdfUrl?: string;
  exportUrl?: string;
  downloadUrl?: string;
  pdf_generation?: string;
};

type RawReport = BackendReport & {
  report_id?: string;
  name?: string;
  filename?: string;
};

function isBackendReport(value: unknown): value is RawReport {
  return typeof value === "object" && value !== null;
}

function getReports(payload: ReportsResponse | BackendReport[]): BackendReport[] {
  const reports = Array.isArray(payload) ? payload : payload.reports ?? payload.data ?? [];

  return reports.filter(isBackendReport).map((report, index) => ({
    ...report,
    id: report.id ?? String(report.report_id ?? index),
    title: report.title ?? report.name ?? report.filename ?? `Report ${index + 1}`,
    fileName: report.fileName ?? report.filename,
  }));
}

function formatReportDate(date?: string) {
  if (!date) return "Date unavailable";

  const parsedDate = new Date(date);
  if (Number.isNaN(parsedDate.getTime())) {
    return date;
  }

  return new Intl.DateTimeFormat("en", {
    month: "long",
    day: "numeric",
    year: "numeric",
  }).format(parsedDate);
}

export function ReportViewer() {
  const [reports, setReports] = useState<BackendReport[]>([]);
  const [selectedReportId, setSelectedReportId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadReports() {
      try {
        setIsLoading(true);
        setError(null);

        const payload = await fetchReports() as ReportsResponse | BackendReport[];
        const backendReports = getReports(payload);

        if (!isMounted) return;

        setReports(backendReports);
        setSelectedReportId(backendReports[0]?.id ?? null);
      } catch {
        if (!isMounted) return;

        setReports([]);
        setSelectedReportId(null);
        setError("Reports are unavailable because the backend is offline.");
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadReports();

    return () => {
      isMounted = false;
    };
  }, []);

  const selectedReport = useMemo(
    () => reports.find((report) => report.id === selectedReportId) ?? reports[0] ?? null,
    [reports, selectedReportId]
  );

  const handleGenerate = async () => {
    try {
      setIsGenerating(true);
      setError(null);
      const generated = getReports([await generateSessionReport() as BackendReport]);
      const payload = await fetchReports() as ReportsResponse | BackendReport[];
      const refreshed = getReports(payload);
      const report = generated[0];

      setReports(refreshed);
      setSelectedReportId(report?.id ?? refreshed[0]?.id ?? null);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Could not generate the audit report.");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleExport = async () => {
    if (!selectedReport) return;

    if (!selectedReport.downloadUrl) {
      setError("This older report is a summary only. Generate a new audit PDF to download a PDF file.");
      return;
    }

    try {
      setError(null);
      const blob = await downloadReport(selectedReport.id);
      const objectUrl = URL.createObjectURL(blob);
      const anchor = document.createElement("a");
      const suggestedName = selectedReport.fileName ?? `${selectedReport.id}.pdf`;
      anchor.href = objectUrl;
      anchor.download = suggestedName.toLowerCase().endsWith(".pdf") ? suggestedName : `${suggestedName}.pdf`;
      document.body.appendChild(anchor);
      anchor.click();
      anchor.remove();
      URL.revokeObjectURL(objectUrl);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Could not download the PDF report.");
    }
  };

  const handleShare = async () => {
    if (!selectedReport) return;

    const shareUrl = selectedReport.pdfUrl ?? selectedReport.exportUrl ?? window.location.href;

    if (navigator.share) {
      await navigator.share({ title: selectedReport.title, url: shareUrl });
      return;
    }

    await navigator.clipboard.writeText(shareUrl);
  };

  if (isLoading) {
    return (
      <div className="flex h-[calc(100vh-12rem)] items-center justify-center rounded-xl border bg-card text-sm text-muted-foreground">
        Loading reports from backend...
      </div>
    );
  }

  if (error && reports.length === 0) {
    return (
      <div className="flex h-[calc(100vh-12rem)] flex-col items-center justify-center gap-3 rounded-xl border border-destructive/30 bg-destructive/5 p-6 text-center">
        <ShieldAlert className="h-8 w-8 text-destructive" />
        <div>
          <h2 className="font-semibold text-destructive">Reports backend unavailable</h2>
          <p className="mt-1 text-sm text-muted-foreground">{error}</p>
          <Button className="mt-4 gap-2" onClick={handleGenerate} disabled={isGenerating}>
            {isGenerating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
            Generate Audit PDF
          </Button>
        </div>
      </div>
    );
  }

  if (!selectedReport) {
    return (
      <div className="flex h-[calc(100vh-12rem)] flex-col items-center justify-center gap-3 rounded-xl border bg-card p-6 text-center">
        <FileText className="h-8 w-8 text-muted-foreground" />
        <div>
          <h2 className="font-semibold">No reports generated yet.</h2>
          <p className="mt-1 text-sm text-muted-foreground">Create a branded audit-session PDF from your accepted documents and risk findings.</p>
          <Button className="mt-5 gap-2" onClick={handleGenerate} disabled={isGenerating}>
            {isGenerating ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
            {isGenerating ? "Generating PDF..." : "Generate Audit PDF"}
          </Button>
        </div>
      </div>
    );
  }

  const metrics = selectedReport.metrics ?? {};
  const risks = selectedReport.topRisks ?? [];

  return (
    <div className="grid gap-6 md:grid-cols-4 h-[calc(100vh-12rem)]">
      <div className="md:col-span-1 space-y-4">
        <div className="flex items-center justify-between px-1">
          <div className="font-medium">Available Reports</div>
          <Button size="sm" variant="outline" onClick={handleGenerate} disabled={isGenerating}>
            {isGenerating ? <Loader2 className="h-3.5 w-3.5 animate-spin" /> : "New PDF"}
          </Button>
        </div>
        <div className="space-y-2">
          {reports.map((report) => {
            const isActive = report.id === selectedReport.id;

            return (
              <button
                key={report.id}
                type="button"
                onClick={() => setSelectedReportId(report.id)}
                className={cn(
                  "w-full p-3 rounded-lg border text-left cursor-pointer transition-all",
                  isActive ? "bg-primary/10 border-primary shadow-sm" : "bg-card hover:bg-muted/50 border-border"
                )}
              >
                <h4 className={cn("text-sm font-medium", isActive && "text-primary")}>{report.title}</h4>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-xs text-muted-foreground">{formatReportDate(report.date)}</span>
                  {report.status && (
                    <Badge variant={isActive ? "default" : "secondary"} className="text-[10px] px-1.5 py-0">
                      {report.status}
                    </Badge>
                  )}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      <div className="md:col-span-3 flex flex-col bg-muted/30 rounded-xl border overflow-hidden">
        {error && (
          <div className="border-b border-destructive/30 bg-destructive/10 px-4 py-2 text-sm text-destructive">
            {error}
          </div>
        )}
        <div className="h-14 bg-card border-b flex items-center justify-between px-4">
          <div className="flex min-w-0 items-center gap-2">
            {selectedReport.status && (
              <Badge variant="outline" className="shrink-0 bg-emerald-500/10 text-emerald-500 border-emerald-500/20">
                {selectedReport.status}
              </Badge>
            )}
            <span className="truncate text-sm font-medium">{selectedReport.fileName ?? selectedReport.title}</span>
            {selectedReport.pdf_generation && (
              <Badge variant="outline" className="hidden shrink-0 text-[10px] sm:inline-flex">
                LaTeX source
              </Badge>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" onClick={handleShare}>
              <Share2 className="w-4 h-4" />
            </Button>
            <Button variant="ghost" size="icon" onClick={() => window.print()}>
              <Printer className="w-4 h-4" />
            </Button>
            <Button size="sm" className="gap-2" onClick={handleExport}>
              <Download className="w-4 h-4" /> Export PDF
            </Button>
          </div>
        </div>

        <div className="flex-1 overflow-auto p-4 md:p-8 flex justify-center bg-[#525659] dark:bg-background/90">
          <Card className="w-full max-w-[800px] bg-white text-black min-h-[1056px] shadow-2xl rounded-sm p-12 print:shadow-none print:p-0">
            <div className="border-b-2 border-slate-200 pb-8 mb-8 flex justify-between items-start">
              <div>
                <div className="w-12 h-12 bg-slate-900 text-white rounded-lg flex items-center justify-center font-bold text-xl mb-4">
                  P
                </div>
                <h1 className="text-3xl font-bold text-slate-900 tracking-tight">{selectedReport.title}</h1>
                {selectedReport.generatedBy && <p className="text-slate-500 mt-1">Generated by {selectedReport.generatedBy}</p>}
              </div>
              <div className="text-right text-sm text-slate-500 space-y-1">
                {selectedReport.date && <p>Date: {formatReportDate(selectedReport.date)}</p>}
                {selectedReport.preparedFor && <p>Prepared for: {selectedReport.preparedFor}</p>}
                {selectedReport.period && <p>Period: {selectedReport.period}</p>}
              </div>
            </div>

            {selectedReport.summary && (
              <div className="space-y-4 mb-10">
                <h2 className="text-xl font-bold text-slate-900 border-b border-slate-100 pb-2">Executive Summary</h2>
                <p className="text-slate-600 leading-relaxed text-sm">{selectedReport.summary}</p>
              </div>
            )}

            <div className="grid grid-cols-3 gap-6 mb-10">
              <div className="bg-slate-50 p-4 rounded-lg border border-slate-100">
                <div className="flex items-center gap-2 text-emerald-600 mb-2">
                  <CheckCircle2 className="w-4 h-4" />
                  <span className="font-semibold text-sm">Evidence Quality</span>
                </div>
                <div className="text-3xl font-bold text-slate-900">
                  {metrics.evidenceQualityScore ?? metrics.readinessScore ?? "-"}
                  {metrics.readinessTotal && <span className="text-lg text-slate-500">/{metrics.readinessTotal}</span>}
                </div>
              </div>
              <div className="bg-red-50 p-4 rounded-lg border border-red-100">
                <div className="flex items-center gap-2 text-red-600 mb-2">
                  <ShieldAlert className="w-4 h-4" />
                  <span className="font-semibold text-sm">Critical Risks</span>
                </div>
                <div className="text-3xl font-bold text-slate-900">{metrics.criticalRisks ?? "-"}</div>
              </div>
              <div className="bg-amber-50 p-4 rounded-lg border border-amber-100">
                <div className="flex items-center gap-2 text-amber-600 mb-2">
                  <AlertTriangle className="w-4 h-4" />
                  <span className="font-semibold text-sm">Compliance Gaps</span>
                </div>
                <div className="text-3xl font-bold text-slate-900">{metrics.complianceGaps ?? "-"}</div>
              </div>
            </div>

            <div className="space-y-4">
              <h2 className="text-xl font-bold text-slate-900 border-b border-slate-100 pb-2">Actionable Exceptions</h2>
              {risks.length > 0 ? (
                <div className="space-y-3">
                  {risks.map((risk, index) => (
                    <div key={risk.id ?? index} className="flex gap-4 p-4 border border-slate-200 rounded-lg">
                      <div className="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center shrink-0">
                        <ShieldAlert className="w-5 h-5 text-red-600" />
                      </div>
                      <div>
                        {risk.issue && <h4 className="font-bold text-slate-900 text-sm">{risk.issue}</h4>}
                        {risk.entity && (
                          <p className="text-sm text-slate-600 mt-1">
                            Entity: <span className="font-medium text-slate-900">{risk.entity}</span>
                          </p>
                        )}
                        {risk.impact && <p className="text-xs text-red-600 mt-2 font-medium">Impact: {risk.impact}</p>}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-slate-500">No actionable exceptions identified by the automated checks. Source evidence still requires reviewer sign-off.</p>
              )}
            </div>

            <div className="mt-16 pt-8 border-t border-slate-200 flex justify-between items-center text-xs text-slate-400">
              <span>PRYSM Audit Intelligence</span>
              <span>{selectedReport.fileName ?? selectedReport.id}</span>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
