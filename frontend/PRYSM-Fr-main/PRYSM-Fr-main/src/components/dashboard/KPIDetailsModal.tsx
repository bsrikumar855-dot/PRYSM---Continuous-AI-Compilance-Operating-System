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
}

const CONTENT = {
  readiness: {
    title: "Audit Readiness Breakdown",
    description: "Detailed analysis of your current compliance posture across all controls.",
    icon: <CheckCircle className="h-6 w-6 text-emerald-500" />,
    color: "text-emerald-500",
    stats: [
      { 
        label: "Technical Controls", 
        value: "92%",
        explanation: "Status of automated system checks including encryption, access logs, and firewall configurations." 
      },
      { 
        label: "Policy Documentation", 
        value: "78%",
        explanation: "Completeness of required corporate policies and internal operating procedures." 
      },
      { 
        label: "Operational Evidence", 
        value: "82%",
        explanation: "Verified artifacts proving that controls are consistently applied over time." 
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
        label: "P0 (Immediate)", 
        value: "3",
        explanation: "Severe vulnerabilities or missing critical controls that pose an immediate compliance breach risk." 
      },
      { 
        label: "P1 (24h)", 
        value: "5",
        explanation: "High-impact issues that must be addressed within the next business day to maintain certification." 
      },
      { 
        label: "P2 (48h)", 
        value: "4",
        explanation: "Important improvements needed in control effectiveness or documentation quality." 
      },
    ]
  },
  gaps: {
    title: "Compliance Gaps Analysis",
    description: "Missing requirements identified during the latest automated scan.",
    icon: <AlertTriangle className="h-6 w-6 text-amber-500" />,
    color: "text-amber-500",
    stats: [
      { 
        label: "ISO 27001", 
        value: "12 gaps",
        explanation: "Inconsistencies found in Annex A controls specifically related to asset management and physical security." 
      },
      { 
        label: "SOC2 Type II", 
        value: "8 gaps",
        explanation: "Failures in the Trust Services Criteria (TSC) for availability and confidentiality mapping." 
      },
      { 
        label: "GDPR", 
        value: "14 gaps",
        explanation: "Missing data processing agreements (DPA) and incomplete right-to-erasure workflows." 
      },
    ]
  },
  documents: {
    title: "Document Ingestion Pipeline",
    description: "Processing status of compliance evidence and operational logs.",
    icon: <Activity className="h-6 w-6 text-blue-500" />,
    color: "text-blue-500",
    stats: [
      { 
        label: "Queued", 
        value: "45",
        explanation: "Documents uploaded and waiting for the AI extraction engine to begin processing." 
      },
      { 
        label: "Processing", 
        value: "12",
        explanation: "Evidence currently being parsed for key compliance data points and cross-referenced." 
      },
      { 
        label: "Validated", 
        value: "1,147",
        explanation: "Successfully processed and verified documents that are now ready for audit submission." 
      },
    ]
  }
};

export function KPIDetailsModal({ isOpen, onClose, type }: KPIDetailsModalProps) {
  const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
  const content = CONTENT[type];

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
                This data is updated in real-time as your infrastructure and documentation are scanned. Click &quot;Full Report&quot; for a comprehensive drill-down.
              </p>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
