"use client";

import { useState } from "react";
import { Sheet, SheetContent, SheetTitle, SheetDescription } from "@/components/ui/sheet";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, FileText, Bot, CheckCircle2, Info } from "lucide-react";
import { cn } from "@/lib/utils";
import { downloadDocumentFile } from "@/lib/api";

interface RiskDrilldownProps {
  isOpen: boolean;
  onClose: () => void;
  risk: {
    id: string;
    issue: string;
    entity: string;
    domain: string;
    severity: string;
    date: string;
    status: string;
    raw?: {
      id?: string;
      type?: string;
      title?: string;
      message?: string;
      source_document?: string;
      document_id?: string;
      recommendation?: string;
      extracted_value?: string;
      rule_id?: string;
      rule_description?: string;
      [key: string]: unknown;
    };
  } | null;
}

function getRiskType(risk: NonNullable<RiskDrilldownProps["risk"]>) {
  return risk.raw?.type || risk.domain || "GENERAL_RISK";
}

function getSummary(risk: NonNullable<RiskDrilldownProps["risk"]>) {
  return risk.raw?.message || `${risk.issue} was detected in ${risk.entity}.`;
}

function getRule(riskType: string) {
  const rules: Record<string, { id: string; description: string }> = {
    MISSING_GSTIN: {
      id: "TAX-GST-001",
      description: "Invoices should include a valid 15-character GSTIN where GST compliance review is required.",
    },
    MISSING_AMOUNT: {
      id: "FIN-INV-002",
      description: "Invoices and financial evidence should include a clearly extractable total or net amount.",
    },
    MISSING_DATE: {
      id: "DOC-DATE-001",
      description: "Audit evidence should include a document date or reporting period for traceability.",
    },
    HIGH_VALUE_INVOICE: {
      id: "FIN-APP-001",
      description: "High-value invoices should have supporting documentation and approval evidence.",
    },
    AUDIT_REPORT_UPLOADED: {
      id: "AUD-REP-001",
      description: "Uploaded audit reports should be reviewed and cross-referenced with internal records.",
    },
  };

  return rules[riskType] || {
    id: "GEN-RISK-001",
    description: "The selected item requires review against source evidence and internal control expectations.",
  };
}

function getActions(risk: NonNullable<RiskDrilldownProps["risk"]>) {
  const recommendation = risk.raw?.recommendation;
  const riskType = getRiskType(risk);

  if (riskType === "MISSING_GSTIN") {
    return [
      recommendation || "Request GSTIN from the vendor and update the invoice.",
      "Validate the GSTIN format and source record before sign-off.",
      "Document the resolution in the audit workpaper.",
    ];
  }

  if (riskType === "MISSING_AMOUNT") {
    return [
      recommendation || "Manually verify the invoice amount and enter it.",
      "Compare the amount against purchase records or supporting schedules.",
      "Flag the item for reviewer approval if the amount remains unclear.",
    ];
  }

  if (riskType === "MISSING_DATE") {
    return [
      recommendation || "Check the document for a valid date.",
      "Confirm the reporting period from surrounding evidence.",
      "Add the verified date to the review notes.",
    ];
  }

  if (riskType === "HIGH_VALUE_INVOICE") {
    return [
      recommendation || "Verify supporting documents and approval trail.",
      "Confirm the approval owner and threshold policy.",
      "Escalate if approval evidence is missing.",
    ];
  }

  if (riskType === "AUDIT_REPORT_UPLOADED") {
    return [
      recommendation || "Review findings and cross-reference with internal records.",
      "Identify key findings, periods, and affected controls.",
      "Generate or update the audit readiness report.",
    ];
  }

  return [
    recommendation || "Review the source evidence and assign an owner.",
    "Capture remediation notes and target date.",
    "Re-check after remediation evidence is uploaded.",
  ];
}

export function RiskDrilldown({ isOpen, onClose, risk }: RiskDrilldownProps) {
  const [fileError, setFileError] = useState<string | null>(null);
  if (!risk) return null;
  const riskType = getRiskType(risk);
  const rule = risk.raw?.rule_id && risk.raw?.rule_description
    ? { id: risk.raw.rule_id, description: risk.raw.rule_description }
    : getRule(riskType);
  const actions = getActions(risk);
  const extractedValue = risk.raw?.extracted_value;

  const handleViewEvidence = async () => {
    const documentId = risk.raw?.document_id;
    if (!documentId) {
      setFileError("This finding does not have a linked source file.");
      return;
    }

    try {
      setFileError(null);
      const blob = await downloadDocumentFile(documentId);
      const objectUrl = URL.createObjectURL(blob);
      window.open(objectUrl, "_blank", "noopener,noreferrer");
      window.setTimeout(() => URL.revokeObjectURL(objectUrl), 60000);
    } catch (err) {
      setFileError(err instanceof Error ? err.message : "Unable to open source file.");
    }
  };

  return (
    <Sheet open={isOpen} onOpenChange={(open) => !open && onClose()}>
      <SheetContent className="sm:max-w-xl w-[90vw] p-0 flex flex-col gap-0 border-l border-border bg-background">
        <div className="p-6 pb-4 border-b border-border">
          <div className="flex items-center gap-2 mb-2">
            <Badge variant="outline" className={cn(
              risk.severity === "Critical" ? "border-destructive text-destructive" :
              risk.severity === "High" ? "border-orange-500 text-orange-500" :
              risk.severity === "Medium" ? "border-yellow-500 text-yellow-500" :
              "border-blue-500 text-blue-500"
            )}>
              {risk.severity} Risk
            </Badge>
            <Badge variant="secondary">{riskType}</Badge>
          </div>
          <SheetTitle className="text-xl leading-tight mb-2">{risk.issue}</SheetTitle>
          <SheetDescription className="text-sm">
            Detected on {risk.date} in {risk.entity}
          </SheetDescription>
        </div>

        <ScrollArea className="flex-1 p-6">
          <div className="space-y-6">
            <div className="flex gap-4 p-4 rounded-lg bg-muted/50 border border-border">
              <Bot className="w-5 h-5 text-primary shrink-0 mt-0.5" />
              <div className="space-y-1">
                <h4 className="text-sm font-semibold">AI Summary</h4>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {getSummary(risk)}
                </p>
              </div>
            </div>

            <Tabs defaultValue="evidence">
              <TabsList className="w-full grid grid-cols-3 mb-4">
                <TabsTrigger value="evidence">Evidence</TabsTrigger>
                <TabsTrigger value="rules">Rules</TabsTrigger>
                <TabsTrigger value="remediation">Remediation</TabsTrigger>
              </TabsList>
              
              <TabsContent value="evidence" className="space-y-4">
                <h4 className="text-sm font-semibold flex items-center gap-2">
                  <FileText className="w-4 h-4" /> Affected Documents
                </h4>
                <div className="p-3 border rounded-md bg-card text-sm flex justify-between items-center gap-3">
                  <span className="font-medium">{risk.raw?.source_document || risk.entity}</span>
                  <Button type="button" variant="outline" size="sm" onClick={handleViewEvidence}>
                    View Source
                  </Button>
                </div>
                {fileError && <p className="text-xs text-destructive">{fileError}</p>}
                <div className="mt-4 p-3 border border-border bg-muted/30 rounded-md">
                  <h5 className="text-xs font-semibold uppercase tracking-wider mb-2">Evidence Note</h5>
                  <code className="text-sm font-mono text-muted-foreground">
                    {extractedValue ? String(extractedValue) : risk.issue}
                  </code>
                  <p className="text-xs text-muted-foreground mt-2 flex items-center gap-1">
                    <Info className="w-3 h-3" /> Source: {risk.entity}
                  </p>
                </div>
              </TabsContent>

              <TabsContent value="rules" className="space-y-4">
                <h4 className="text-sm font-semibold flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-amber-500" /> Compliance Rules Failed
                </h4>
                <ul className="space-y-2">
                  <li className="text-sm p-3 border rounded-md bg-card">
                    <span className="font-semibold block mb-1">Rule: {rule.id}</span>
                    <span className="text-muted-foreground">{rule.description}</span>
                  </li>
                </ul>
              </TabsContent>

              <TabsContent value="remediation" className="space-y-4">
                <h4 className="text-sm font-semibold flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" /> Suggested Actions
                </h4>
                <ul className="space-y-2 text-sm">
                  {actions.map((action, index) => (
                    <li key={action} className="flex items-start gap-2 p-3 border rounded-md bg-card">
                      <div className="w-5 h-5 rounded-full bg-muted flex items-center justify-center shrink-0 mt-0.5 text-xs font-medium">
                        {index + 1}
                      </div>
                      <span>{action}</span>
                    </li>
                  ))}
                </ul>
              </TabsContent>
            </Tabs>
          </div>
        </ScrollArea>
      </SheetContent>
    </Sheet>
  );
}
