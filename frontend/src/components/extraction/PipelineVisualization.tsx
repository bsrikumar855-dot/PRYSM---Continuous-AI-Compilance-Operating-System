"use client";

import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { 
  FileText, 
  ScanLine, 
  BrainCircuit, 
  ShieldAlert, 
  CheckCircle2,
  Loader2
} from "lucide-react";
import { cn } from "@/lib/utils";

const stages = [
  { id: 1, name: "Uploading", icon: FileText, delay: 0 },
  { id: 2, name: "OCR Processing", icon: ScanLine, delay: 2000 },
  { id: 3, name: "AI Extraction", icon: BrainCircuit, delay: 5000 },
  { id: 4, name: "Risk Detection", icon: ShieldAlert, delay: 9000 },
  { id: 5, name: "Compliance Mapping", icon: FileText, delay: 12000 },
  { id: 6, name: "Final Analysis", icon: CheckCircle2, delay: 15000 },
];

export function PipelineVisualization() {
  const [activeStage, setActiveStage] = useState(1);
  const [progress, setProgress] = useState(0);
  const [detectedEntities, setDetectedEntities] = useState<{name: string, value: string, confidence: number}[]>([]);

  useEffect(() => {
    let currentProgress = 0;
    const progressInterval = setInterval(() => {
      currentProgress += 1;
      setProgress(Math.min(currentProgress, 100));
      
      if (currentProgress > 15 && currentProgress <= 100) {
        const currentStageIndex = Math.floor((currentProgress / 100) * stages.length);
        setActiveStage(Math.min(currentStageIndex + 1, stages.length));
      }
      
      if (currentProgress === 100) clearInterval(progressInterval);
    }, 150); // total 15 seconds

    const entityTimers = [
      setTimeout(() => setDetectedEntities(prev => [...prev, { name: "Vendor Name", value: "Acme Corp", confidence: 98 }]), 6000),
      setTimeout(() => setDetectedEntities(prev => [...prev, { name: "Invoice Date", value: "Oct 24, 2026", confidence: 95 }]), 7000),
      setTimeout(() => setDetectedEntities(prev => [...prev, { name: "Total Amount", value: "$45,200.00", confidence: 99 }]), 7500),
      setTimeout(() => setDetectedEntities(prev => [...prev, { name: "GSTIN", value: "29GGGGG1314R9Z6", confidence: 85 }]), 8500),
    ];

    return () => {
      clearInterval(progressInterval);
      entityTimers.forEach(clearTimeout);
    };
  }, []);

  return (
    <div className="grid gap-6 md:grid-cols-3">
      <div className="md:col-span-2 space-y-6">
        <Card className="bg-card">
          <CardHeader>
            <CardTitle className="text-lg font-medium flex items-center gap-2">
              <ScanLine className="h-5 w-5 text-primary" />
              Processing Pipeline
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-8">
            <div className="space-y-2">
              <div className="flex justify-between text-sm font-medium">
                <span className="text-muted-foreground">Overall Progress</span>
                <span className="text-primary">{progress}%</span>
              </div>
              <Progress value={progress} className="h-2" />
            </div>

            <div className="space-y-4 relative before:absolute before:inset-0 before:ml-5 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
              {stages.map((stage) => {
                const isActive = activeStage === stage.id;
                const isCompleted = activeStage > stage.id;
                
                return (
                  <div key={stage.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div className={cn(
                      "flex items-center justify-center w-10 h-10 rounded-full border-2 shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 transition-all",
                      isActive ? "bg-primary border-primary text-primary-foreground animate-pulse" :
                      isCompleted ? "bg-primary border-primary text-primary-foreground" :
                      "bg-muted border-border text-muted-foreground"
                    )}>
                      {isActive ? <Loader2 className="w-5 h-5 animate-spin" /> : 
                       isCompleted ? <CheckCircle2 className="w-5 h-5" /> :
                       <stage.icon className="w-5 h-5" />}
                    </div>
                    <div className={cn(
                      "w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] p-4 rounded-xl border transition-all",
                      isActive ? "border-primary bg-primary/5" :
                      isCompleted ? "border-border bg-muted/30" :
                      "border-transparent opacity-50"
                    )}>
                      <h3 className={cn(
                        "font-medium",
                        isActive ? "text-primary" : "text-foreground"
                      )}>{stage.name}</h3>
                      {isActive && (
                        <p className="text-xs text-muted-foreground mt-1">
                          Analyzing document structure and layout...
                        </p>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>
      
      <div className="space-y-6">
        <Card className="h-full flex flex-col">
          <CardHeader>
            <CardTitle className="text-lg font-medium flex items-center gap-2">
              <BrainCircuit className="h-5 w-5 text-primary" />
              Live Entities
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1">
            <ScrollArea className="h-[400px] pr-4">
              {detectedEntities.length === 0 ? (
                <div className="h-full flex items-center justify-center text-sm text-muted-foreground italic">
                  Waiting for extraction...
                </div>
              ) : (
                <div className="space-y-4">
                  {detectedEntities.map((entity, i) => (
                    <div key={i} className="flex flex-col gap-2 p-3 border rounded-lg bg-card animate-in fade-in slide-in-from-bottom-2">
                      <div className="flex justify-between items-start">
                        <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">{entity.name}</span>
                        <Badge variant="outline" className={cn(
                          "text-[10px] px-1.5 py-0",
                          entity.confidence > 90 ? "text-emerald-500 border-emerald-500/30 bg-emerald-500/10" : "text-amber-500 border-amber-500/30 bg-amber-500/10"
                        )}>
                          {entity.confidence}% Conf
                        </Badge>
                      </div>
                      <span className="font-medium">{entity.value}</span>
                    </div>
                  ))}
                </div>
              )}
            </ScrollArea>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
