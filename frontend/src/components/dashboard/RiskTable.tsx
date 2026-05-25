"use client";

import { useEffect, useState } from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Search, ShieldAlert } from "lucide-react";
import { RiskDrilldown } from "./RiskDrilldown";
import { cn } from "@/lib/utils";
import { fetchRiskOverview } from "@/lib/api";
import type { RiskObject, RiskOverviewResponse } from "@/types/api";

type Risk = {
  id: string;
  issue: string;
  entity: string;
  domain: string;
  severity: string;
  date: string;
  status: string;
  raw: RiskObject;
};

function getString(value: unknown, fallback: string) {
  return typeof value === "string" && value.trim() ? value : fallback;
}

function normalizeRisk(risk: RiskObject, index: number): Risk {
  return {
    id: getString(risk.id, `RSK-${String(index + 1).padStart(3, "0")}`),
    issue: getString(risk.title ?? risk.message ?? risk.type, "Untitled risk"),
    entity: getString(risk.source_document ?? risk.document ?? risk.entity, "Unknown document"),
    domain: getString(risk.domain ?? risk.category ?? risk.type, "General"),
    severity: getString(risk.severity, "Info"),
    date: getString(risk.date ?? risk.created_at ?? risk.detected_at, "Date unavailable"),
    status: getString(risk.status, "Open"),
    raw: risk,
  };
}

export function RiskTable() {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedRisk, setSelectedRisk] = useState<Risk | null>(null);
  const [risks, setRisks] = useState<Risk[]>([]);
  const [summary, setSummary] = useState<RiskOverviewResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;

    async function loadRiskOverview() {
      try {
        setIsLoading(true);
        setError(null);

        const data = await fetchRiskOverview() as RiskOverviewResponse & {
          data?: RiskObject[];
        };
        const riskObjects = data.risks || data.flags || data.data || [];

        if (!isMounted) return;

        setSummary(data);
        setRisks(riskObjects.map(normalizeRisk));
      } catch {
        if (!isMounted) return;

        setRisks([]);
        setSummary(null);
        setError("Backend is not running. Start FastAPI at http://127.0.0.1:8001.");
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    loadRiskOverview();

    return () => {
      isMounted = false;
    };
  }, []);

  const filteredRisks = risks.filter(risk => 
    risk.issue.toLowerCase().includes(searchTerm.toLowerCase()) ||
    risk.entity.toLowerCase().includes(searchTerm.toLowerCase()) ||
    risk.domain.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <>
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="relative w-full max-w-sm">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Filter risks..."
              className="pl-9 bg-card"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        {isLoading && (
          <div className="border rounded-md bg-card p-6 text-center text-sm text-muted-foreground">
            Loading risks from backend...
          </div>
        )}

        {error && (
          <div className="flex items-center gap-3 rounded-md border border-destructive/30 bg-destructive/5 p-4 text-sm text-destructive">
            <ShieldAlert className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {!isLoading && !error && risks.length === 0 && summary && (
          <div className="rounded-md border bg-card p-4 text-sm text-muted-foreground">
            No risks found.
          </div>
        )}
        
        {!isLoading && !error && (
        <div className="border rounded-md bg-card">
          <Table>
            <TableHeader>
              <TableRow className="hover:bg-transparent">
                <TableHead>Risk ID</TableHead>
                <TableHead>Issue</TableHead>
                <TableHead>Entity</TableHead>
                <TableHead>Domain</TableHead>
                <TableHead>Severity</TableHead>
                <TableHead>Date</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredRisks.map((risk) => (
                <TableRow 
                  key={risk.id} 
                  className="cursor-pointer hover:bg-muted/50 transition-colors"
                  onClick={() => setSelectedRisk(risk)}
                >
                  <TableCell className="font-medium text-xs text-muted-foreground">{risk.id}</TableCell>
                  <TableCell className="font-medium">{risk.issue}</TableCell>
                  <TableCell>{risk.entity}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className="font-normal">{risk.domain}</Badge>
                  </TableCell>
                  <TableCell>
                    <Badge variant="secondary" className={cn(
                      "font-medium",
                      risk.severity === "Critical" ? "bg-destructive/10 text-destructive hover:bg-destructive/20" :
                      risk.severity === "High" ? "bg-orange-500/10 text-orange-500 hover:bg-orange-500/20" :
                      risk.severity === "Medium" ? "bg-yellow-500/10 text-yellow-500 hover:bg-yellow-500/20" :
                      "bg-blue-500/10 text-blue-500 hover:bg-blue-500/20"
                    )}>
                      {risk.severity}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-muted-foreground text-sm">{risk.date}</TableCell>
                  <TableCell>
                    <span className={cn(
                      "text-xs font-medium px-2 py-1 rounded-full",
                      risk.status === "Open" ? "bg-muted text-foreground" :
                      risk.status === "Investigating" ? "bg-blue-500/10 text-blue-500" :
                      "bg-emerald-500/10 text-emerald-500"
                    )}>
                      {risk.status}
                    </span>
                  </TableCell>
                </TableRow>
              ))}
              {filteredRisks.length === 0 && (
                <TableRow>
                  <TableCell colSpan={7} className="h-24 text-center text-muted-foreground">
                    No risks found matching your criteria.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
        )}
      </div>

      <RiskDrilldown 
        isOpen={!!selectedRisk} 
        onClose={() => setSelectedRisk(null)} 
        risk={selectedRisk} 
      />
    </>
  );
}
