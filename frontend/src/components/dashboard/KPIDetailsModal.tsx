"use client";

import { useState } from "react";
import { 
  Dialog, 
  DialogContent, 
  DialogHeader, 
  DialogTitle,
  DialogDescription
} from "@/components/ui/dialog";
import { ShieldAlert, CheckCircle, AlertTriangle, Activity, TrendingUp, Info, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";

interface KPIDetailsModalProps {
  isOpen: boolean;
  onClose: () => void;
  type: "readiness" | "risks" | "gaps" | "documents";
  risks: any[];
  documents: any[];
  reports: any[];
}

function buildContent(risks: any[], documents: any[], reports: any[]) {
  const countSeverity = (severity: string) =>
    risks.filter(risk => String(risk.severity || "").toLowerCase() === severity).length;
  const countType = (type: string) => risks.filter(risk => risk.type === type).length;
  const critical = countSeverity("critical");
  const warning = countSeverity("warning");
  const info = countSeverity("info");
  const readiness = reports[0]?.metrics?.readinessScore ??
    (documents.length > 0 ? Math.max(0, 100 - critical * 20 - warning * 5) : "-");
  const flaggedDocuments = new Set(risks.map(risk => risk.source_document).filter(Boolean)).size;

  return {
  readiness: {
    title: "Audit Readiness Breakdown",
    description: "Calculated from eligible evidence in the current audit session.",
    icon: <CheckCircle className="h-6 w-6 text-emerald-500" />,
    color: "text-emerald-500",
    stats: [
      { 
        label: "Readiness Score",
        value: readiness === "-" ? "-" : `${readiness}/100`,
        explanation: "Score derived from critical and warning findings in the accepted evidence set."
      },
      { 
        label: "Accepted Evidence",
        value: String(documents.length),
        explanation: "Documents screened as eligible for audit analysis in this session."
      },
      { 
        label: "Active Findings",
        value: String(risks.length),
        explanation: "Flags produced from the accepted source documents."
      },
    ]
  },
  risks: {
    title: "Critical Risks Overview",
    description: "High-priority items requiring immediate attention from the audit team.",
    icon: <ShieldAlert className="h-6 w-6 text-rose-500" />,
    color: "text-rose-500",
    stats: [
      { 
        label: "Critical",
        value: String(critical),
        explanation: "Findings marked critical by the current audit rules."
      },
      { 
        label: "Warnings",
        value: String(warning),
        explanation: "Review findings that require verification or remediation."
      },
      { 
        label: "Information",
        value: String(info),
        explanation: "Informational findings retained for audit traceability."
      },
    ]
  },
  gaps: {
    title: "Compliance Gaps Analysis",
    description: "Missing extracted evidence fields in the current document set.",
    icon: <AlertTriangle className="h-6 w-6 text-amber-500" />,
    color: "text-amber-500",
    stats: [
      { 
        label: "Missing GSTIN",
        value: String(countType("MISSING_GSTIN")),
        explanation: "Accepted documents where a GSTIN could not be extracted."
      },
      { 
        label: "Missing Amount",
        value: String(countType("MISSING_AMOUNT")),
        explanation: "Accepted documents where a monetary total could not be extracted."
      },
      { 
        label: "Missing Date",
        value: String(countType("MISSING_DATE")),
        explanation: "Accepted documents where a date could not be extracted."
      },
    ]
  },
  documents: {
    title: "Document Ingestion Pipeline",
    description: "Session documents and generated report output.",
    icon: <Activity className="h-6 w-6 text-blue-500" />,
    color: "text-blue-500",
    stats: [
      { 
        label: "Accepted Evidence",
        value: String(documents.length),
        explanation: "Documents presently included in audit calculations."
      },
      { 
        label: "Flagged Documents",
        value: String(flaggedDocuments),
        explanation: "Accepted documents that produced at least one audit finding."
      },
      { 
        label: "PDF Reports",
        value: String(reports.length),
        explanation: "Generated reports available in the Reports section."
      },
    ]
  }
  };
}

export function KPIDetailsModal({ isOpen, onClose, type, risks, documents, reports }: KPIDetailsModalProps) {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
  const content = buildContent(risks, documents, reports)[type];

  const handleToggle = (index: number) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  return (
    <Dialog open={isOpen} onOpenChange={(open) => {
      if (!open) {
        setExpandedIndex(null);
        onClose();
      }
    }}>
      <DialogContent className="sm:max-w-[425px] !border-none !ring-0 !outline-none shadow-none bg-background/95 backdrop-blur-xl">
        <DialogHeader>
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-muted rounded-lg">
              {content.icon}
            </div>
            <DialogTitle className="text-xl font-bold">{content.title}</DialogTitle>
          </div>
          <DialogDescription className="text-muted-foreground/70">
            {content.description}
          </DialogDescription>
        </DialogHeader>
        
        <div className="grid gap-4 py-4">
          <div className="space-y-4">
            <h4 className="font-medium text-sm text-muted-foreground flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              Key Performance Metrics
            </h4>
            <div className="grid grid-cols-1 gap-3">
              {content.stats.map((stat, i) => (
                <div key={i} className="flex flex-col rounded-xl border bg-muted/30 overflow-hidden transition-all duration-200">
                  <button 
                    onClick={() => handleToggle(i)}
                    className="flex items-center justify-between p-3 transition-colors hover:bg-muted/50 text-left w-full"
                  >
                    <div className="flex items-center gap-2">
                      <ChevronDown className={cn("h-4 w-4 text-muted-foreground transition-transform duration-200", expandedIndex === i && "rotate-180")} />
                      <span className="text-sm font-medium">{stat.label}</span>
                    </div>
                    <span className={`text-sm font-bold ${content.color}`}>{stat.value}</span>
                  </button>
                  {expandedIndex === i && (
                    <div className="px-3 pb-3 pt-0 animate-in fade-in slide-in-from-top-2 duration-200">
                      <div className="p-2 rounded-lg bg-background/50 border border-muted text-xs text-muted-foreground leading-relaxed">
                        {stat.explanation}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
            
            <div className="mt-6 p-4 rounded-xl bg-primary/5 border border-primary/10 flex gap-3">
              <Info className="h-5 w-5 text-primary shrink-0" />
              <p className="text-xs text-muted-foreground leading-relaxed">
                Values are calculated from documents, findings, and reports currently returned by the backend for this session.
              </p>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
