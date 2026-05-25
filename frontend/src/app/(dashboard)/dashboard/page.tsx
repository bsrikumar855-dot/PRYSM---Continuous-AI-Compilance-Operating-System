"use client";

import { useEffect, useState } from "react";
import { KPICards } from "@/components/dashboard/KPICards";
import { RiskCharts } from "@/components/dashboard/RiskCharts";
import { RiskTable } from "@/components/dashboard/RiskTable";
import { fetchRiskOverview, fetchDocuments, fetchReports } from "@/lib/api";

export default function DashboardPage() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [risks, setRisks] = useState<any[]>([]);
  const [documents, setDocuments] = useState<any[]>([]);
  const [reports, setReports] = useState<any[]>([]);

  useEffect(() => {
    let isMounted = true;
    const loadingFallback = window.setTimeout(() => {
      if (isMounted) {
        setLoading(false);
      }
    }, 6000);

    async function loadData() {
      try {
        setLoading(true);
        const [risksData, docsData, reportsData] = await Promise.all([
          fetchRiskOverview().catch(() => ({})),
          fetchDocuments().catch(() => ({})),
          fetchReports().catch(() => ({}))
        ]) as any[];
        
        console.log("Risk overview response:", risksData);
        console.log("Documents response:", docsData);
        console.log("Reports response:", reportsData);
        
        const risksArr = risksData.risks || risksData.flags || risksData.data || risksData.items || [];
        const docsArr = (docsData.documents || docsData.data || docsData.items || []).filter(
          (document: any) => document.screening?.audit_eligible !== false
        );
        const reportsArr = reportsData.reports || reportsData.data || reportsData.items || [];

        if (!isMounted) return;

        setRisks(risksArr);
        setDocuments(docsArr);
        setReports(reportsArr);
      } catch (err) {
        if (!isMounted) return;

        console.error(err);
        setError("Backend is not running. Please start FastAPI server.");
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }
    
    loadData();

    return () => {
      isMounted = false;
      window.clearTimeout(loadingFallback);
    };
  }, []);

  if (loading) {
    return <div className="p-6">Loading dashboard data from backend...</div>;
  }

  if (error) {
    return <div className="p-6 text-destructive">{error}</div>;
  }

  if (risks.length === 0 && documents.length === 0 && reports.length === 0) {
    return (
      <div className="flex flex-col gap-6">
        <div className="mb-2">
          <h1 className="bg-gradient-to-r from-[#A07018] via-[#D4A830] to-[#FDE983] bg-clip-text pb-1 text-4xl font-extrabold tracking-tight text-transparent drop-shadow-sm">
            Intelligence Dashboard
          </h1>
          <p className="text-muted-foreground mt-2 text-lg">
            Enterprise audit readiness and risk analytics overview.
          </p>
        </div>
        <div className="p-12 text-center text-muted-foreground border rounded-lg bg-card">
          No backend data available yet. Upload documents to begin.
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="mb-2">
        <h1 className="bg-gradient-to-r from-[#A07018] via-[#D4A830] to-[#FDE983] bg-clip-text pb-1 text-4xl font-extrabold tracking-tight text-transparent drop-shadow-sm">
          Intelligence Dashboard
        </h1>
        <p className="text-muted-foreground mt-2 text-lg">
          Enterprise audit readiness and risk analytics overview.
        </p>
      </div>
      
      <KPICards risks={risks} documents={documents} reports={reports} />
      <RiskCharts risks={risks} />
      <div className="mt-4">
        <h2 className="text-xl font-semibold mb-4 tracking-tight">Active Risks</h2>
        <RiskTable />
      </div>
    </div>
  );
}
