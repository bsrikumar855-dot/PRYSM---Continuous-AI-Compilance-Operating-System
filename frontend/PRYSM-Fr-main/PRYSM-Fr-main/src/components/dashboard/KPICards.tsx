"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ShieldAlert, CheckCircle, AlertTriangle, Activity } from "lucide-react";
import { KPIDetailsModal } from "./KPIDetailsModal";

type KPIType = "readiness" | "risks" | "gaps" | "documents";

export function KPICards() {
  const [selectedKPI, setSelectedKPI] = useState<KPIType | null>(null);

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
            <div className="text-3xl font-extrabold bg-gradient-to-br from-emerald-600 to-emerald-400 bg-clip-text text-transparent">84/100</div>
            <p className="text-sm text-muted-foreground mt-2 flex items-center">
              <span className="text-emerald-600 dark:text-emerald-400 font-bold bg-emerald-100 dark:bg-emerald-500/20 px-1.5 py-0.5 rounded text-xs mr-2">+2.5%</span> 
              from last scan
            </p>
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
            <div className="text-3xl font-extrabold bg-gradient-to-br from-red-700 to-red-950 dark:from-red-500 dark:to-red-800 bg-clip-text text-transparent">12</div>
            <p className="text-sm text-muted-foreground mt-2 flex items-center">
              <span className="text-red-800 dark:text-red-300 font-bold bg-red-950/15 dark:bg-red-950/70 px-1.5 py-0.5 rounded text-xs mr-2">+3</span> 
              new this week
            </p>
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
            <div className="text-3xl font-extrabold bg-gradient-to-br from-amber-600 to-amber-400 bg-clip-text text-transparent">34</div>
            <p className="text-sm text-muted-foreground mt-2 flex items-center">
              <span className="font-medium bg-secondary px-1.5 py-0.5 rounded text-xs">Across 5 domains</span>
            </p>
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
            <div className="text-3xl font-extrabold bg-gradient-to-br from-emerald-600 to-emerald-400 bg-clip-text text-transparent">1,204</div>
            <p className="text-sm text-muted-foreground mt-2 flex items-center">
              <span className="text-emerald-600 dark:text-emerald-400 font-bold bg-emerald-100 dark:bg-emerald-500/20 px-1.5 py-0.5 rounded text-xs mr-2">+142</span> 
              in last 24h
            </p>
          </CardContent>
        </Card>
      </div>

      <KPIDetailsModal 
        isOpen={!!selectedKPI}
        onClose={() => setSelectedKPI(null)}
        type={selectedKPI || "readiness"}
      />
    </>
  );
}
