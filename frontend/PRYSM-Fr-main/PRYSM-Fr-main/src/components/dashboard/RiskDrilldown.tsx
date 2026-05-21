"use client";

import { Sheet, SheetContent, SheetTitle, SheetDescription } from "@/components/ui/sheet";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AlertCircle, FileText, Bot, CheckCircle2, Info } from "lucide-react";
import { cn } from "@/lib/utils";

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
  } | null;
}

export function RiskDrilldown({ isOpen, onClose, risk }: RiskDrilldownProps) {
  if (!risk) return null;

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
            <Badge variant="secondary">{risk.domain}</Badge>
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
                  The uploaded invoice from {risk.entity} shows a discrepancy in the GSTIN format, which does not match the standard validation rules. This could lead to input tax credit loss.
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
                <div className="p-3 border rounded-md bg-card text-sm flex justify-between items-center cursor-pointer hover:bg-muted/50 transition-colors">
                  <span className="font-medium">INV-2026-1042.pdf</span>
                  <Badge variant="outline">View</Badge>
                </div>
                <div className="mt-4 p-3 border border-destructive/20 bg-destructive/5 rounded-md">
                  <h5 className="text-xs font-semibold text-destructive uppercase tracking-wider mb-2">Extracted Value</h5>
                  <code className="text-sm font-mono text-destructive">29GGGGG1314R9Z6</code>
                  <p className="text-xs text-muted-foreground mt-2 flex items-center gap-1">
                    <Info className="w-3 h-3" /> Confidence Score: 85%
                  </p>
                </div>
              </TabsContent>

              <TabsContent value="rules" className="space-y-4">
                <h4 className="text-sm font-semibold flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-amber-500" /> Compliance Rules Failed
                </h4>
                <ul className="space-y-2">
                  <li className="text-sm p-3 border rounded-md bg-card">
                    <span className="font-semibold block mb-1">Rule: TAX-GST-001</span>
                    <span className="text-muted-foreground">GSTIN must be a 15-character alphanumeric string following the state code and PAN structure.</span>
                  </li>
                </ul>
              </TabsContent>

              <TabsContent value="remediation" className="space-y-4">
                <h4 className="text-sm font-semibold flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500" /> Suggested Actions
                </h4>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-start gap-2 p-3 border rounded-md bg-card">
                    <div className="w-5 h-5 rounded-full bg-muted flex items-center justify-center shrink-0 mt-0.5 text-xs font-medium">1</div>
                    <span>Verify the GSTIN with the vendor directly or check the GST portal.</span>
                  </li>
                  <li className="flex items-start gap-2 p-3 border rounded-md bg-card">
                    <div className="w-5 h-5 rounded-full bg-muted flex items-center justify-center shrink-0 mt-0.5 text-xs font-medium">2</div>
                    <span>Update the vendor master data if the extracted value is a typo.</span>
                  </li>
                  <li className="flex items-start gap-2 p-3 border rounded-md bg-card">
                    <div className="w-5 h-5 rounded-full bg-muted flex items-center justify-center shrink-0 mt-0.5 text-xs font-medium">3</div>
                    <span>Hold invoice processing until resolution to prevent compliance penalties.</span>
                  </li>
                </ul>
              </TabsContent>
            </Tabs>
          </div>
        </ScrollArea>
      </SheetContent>
    </Sheet>
  );
}
