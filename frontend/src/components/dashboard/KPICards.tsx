"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ShieldAlert, CheckCircle, AlertTriangle, Activity } from "lucide-react";
import { KPIDetailsModal } from "./KPIDetailsModal";

type KPIType = "readiness" | "risks" | "gaps" | "documents";

export function KPICards({ risks = [], documents = [], reports = [] }: { risks?: any[], documents?: any[], reports?: any[] }) {
  const [selectedKPI, setSelectedKPI] = useState<KPIType | null>(null);

  const criticalCount = risks.filter(r => (r.severity || "").toLowerCase() === "critical").length || 0;
  const warningCount = risks.filter(r => (r.severity || "").toLowerCase() === "warning").length || 0;
  const infoCount = risks.filter(r => (r.severity || "").toLowerCase() === "info").length || 0;

  const calculatedReadinessScore = Math.max(0, 100 - (criticalCount * 20) - (warningCount * 5));
  const calculatedComplianceGaps = criticalCount + warningCount + infoCount;

  const readinessScore = reports?.[0]?.metrics?.readinessScore !== undefined
    ? reports[0].metrics.readinessScore
    : (documents.length > 0 ? calculatedReadinessScore : "-");

  const criticalRisksCount = criticalCount;

  const complianceGapsCount = reports?.[0]?.metrics?.complianceGaps !== undefined
    ? reports[0].metrics.complianceGaps
    : (documents.length > 0 ? calculatedComplianceGaps : "-");

  const documentsCount = documents.length || 0;

  return (
    <>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card 
          className="border-t-4 border-t-emerald-500 hover:shadow-lg hover:shadow-emerald-500/10 transition-all duration-300 hover:-translate-y-1 cursor-pointer bg-gradient-to-b from-background to-emerald-500/5 dark:to-emerald-500/10"
          onClick={() => setSelectedKPI("readiness")}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-semibold text-emerald-700 dark:text-emerald-400">Audit Readiness Score</CardTitle>
            <div className="p-2 bg-emerald-100 dark:bg-emerald-500/20 rounded-full">
              <CheckCircle className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-extrabold bg-gradient-to-br from-emerald-600 to-emerald-400 bg-clip-text text-transparent">
              {readinessScore !== "-" ? `${readinessScore}/100` : "-"}
            </div>
            <p className="text-sm text-muted-foreground mt-2">{documents.length} accepted document(s) analyzed</p>
          </CardContent>
        </Card>
        
        <Card 
          className="border-t-4 border-t-red-900 ring-red-950/20 hover:shadow-lg hover:shadow-red-950/30 transition-all duration-300 hover:-translate-y-1 cursor-pointer bg-gradient-to-b from-background to-red-950/10 dark:to-red-950/40"
          onClick={() => setSelectedKPI("risks")}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-semibold text-red-900 dark:text-red-500">Critical Risks</CardTitle>
            <div className="p-2 bg-red-950/15 dark:bg-red-950/70 rounded-full">
              <ShieldAlert className="h-5 w-5 text-red-800 dark:text-red-400" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-extrabold bg-gradient-to-br from-red-700 to-red-950 dark:from-red-500 dark:to-red-800 bg-clip-text text-transparent">{criticalRisksCount}</div>
            <p className="text-sm text-muted-foreground mt-2">{warningCount} warning finding(s) active</p>
          </CardContent>
        </Card>

        <Card 
          className="border-t-4 border-t-amber-500 hover:shadow-lg hover:shadow-amber-500/10 transition-all duration-300 hover:-translate-y-1 cursor-pointer bg-gradient-to-b from-background to-amber-500/5 dark:to-amber-500/10"
          onClick={() => setSelectedKPI("gaps")}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-semibold text-amber-700 dark:text-amber-400">Compliance Gaps</CardTitle>
            <div className="p-2 bg-amber-100 dark:bg-amber-500/20 rounded-full">
              <AlertTriangle className="h-5 w-5 text-amber-600 dark:text-amber-400" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-extrabold bg-gradient-to-br from-amber-600 to-amber-400 bg-clip-text text-transparent">{complianceGapsCount}</div>
            <p className="text-sm text-muted-foreground mt-2">Calculated from current findings</p>
          </CardContent>
        </Card>

        <Card 
          className="border-t-4 border-t-emerald-500 hover:shadow-lg hover:shadow-emerald-500/10 transition-all duration-300 hover:-translate-y-1 cursor-pointer bg-gradient-to-b from-background to-emerald-500/5 dark:to-emerald-500/10"
          onClick={() => setSelectedKPI("documents")}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-semibold text-emerald-700 dark:text-emerald-400">Documents Processed</CardTitle>
            <div className="p-2 bg-emerald-100 dark:bg-emerald-500/20 rounded-full">
              <Activity className="h-5 w-5 text-emerald-600 dark:text-emerald-400" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-extrabold bg-gradient-to-br from-emerald-600 to-emerald-400 bg-clip-text text-transparent">{documentsCount}</div>
            <p className="text-sm text-muted-foreground mt-2">Eligible audit evidence only</p>
          </CardContent>
        </Card>
      </div>

      <KPIDetailsModal 
        isOpen={!!selectedKPI}
        onClose={() => setSelectedKPI(null)}
        type={selectedKPI || "readiness"}
        risks={risks}
        documents={documents}
        reports={reports}
      />
    </>
  );
}
