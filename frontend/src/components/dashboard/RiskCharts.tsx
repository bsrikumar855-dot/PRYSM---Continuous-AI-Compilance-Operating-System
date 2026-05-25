"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from "recharts";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Maximize2 } from "lucide-react";

export function RiskCharts({ risks = [] }: { risks?: any[] }) {
  const [expandedChart, setExpandedChart] = useState<"severity" | "domain" | null>(null);
  const chartSurfaceClassName = "[&_.recharts-wrapper]:outline-none [&_.recharts-surface]:outline-none [&_.recharts-layer]:outline-none [&_.recharts-rectangle]:outline-none [&_*:focus]:outline-none [&_*:focus-visible]:outline-none focus:outline-none";
  const chartTextColor = "var(--foreground)";

  const severityCounts = risks.reduce((acc, risk) => {
    const sev = (risk.severity || "Low").toLowerCase();
    acc[sev] = (acc[sev] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const severityData = [
    { name: 'Critical', value: severityCounts['critical'] || 0, color: '#ef4444', gradient: 'url(#pieCritical)' },
    { name: 'High', value: severityCounts['high'] || 0, color: '#f97316', gradient: 'url(#pieHigh)' },
    { name: 'Warning', value: severityCounts['warning'] || 0, color: '#f97316', gradient: 'url(#pieHigh)' },
    { name: 'Medium', value: severityCounts['medium'] || 0, color: '#eab308', gradient: 'url(#pieMedium)' },
    { name: 'Low', value: severityCounts['low'] || 0, color: '#3b82f6', gradient: 'url(#pieLow)' },
    { name: 'Info', value: severityCounts['info'] || 0, color: '#3b82f6', gradient: 'url(#pieLow)' },
  ].filter(d => d.value > 0);

  const domainCounts = risks.reduce((acc, risk) => {
    const dom = risk.domain || risk.category || risk.type || "General";
    acc[dom] = (acc[dom] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const domainData = Object.keys(domainCounts).map(name => ({
    name,
    risks: domainCounts[name]
  })).sort((a, b) => b.risks - a.risks).slice(0, 5);

  const renderSeverityChart = (isExpanded = false) => (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <defs>
          <linearGradient id="pieCritical" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#ef4444" />
            <stop offset="100%" stopColor="#991b1b" />
          </linearGradient>
          <linearGradient id="pieHigh" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#f97316" />
            <stop offset="100%" stopColor="#9a3412" />
          </linearGradient>
          <linearGradient id="pieMedium" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#eab308" />
            <stop offset="100%" stopColor="#854d0e" />
          </linearGradient>
          <linearGradient id="pieLow" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="100%" stopColor="#1e3a8a" />
          </linearGradient>
        </defs>
        <Pie
          data={severityData}
          cx="50%"
          cy="50%"
          innerRadius={isExpanded ? 120 : 80}
          outerRadius={isExpanded ? 160 : 110}
          paddingAngle={5}
          dataKey="value"
          stroke="none"
          activeShape={false}
        >
          {severityData.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.gradient} />
          ))}
        </Pie>
        <RechartsTooltip 
          contentStyle={{ backgroundColor: 'rgba(0, 0, 0, 0.8)', border: 'none', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }}
          itemStyle={{ color: '#fff' }}
        />
        <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ color: chartTextColor }} />
      </PieChart>
    </ResponsiveContainer>
  );

  const renderDomainChart = () => (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart data={domainData} margin={{ top: 20, right: 30, left: -20, bottom: 5 }}>
        <defs>
          <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#F5D76A" stopOpacity={1} />
            <stop offset="55%" stopColor="#C89528" stopOpacity={1} />
            <stop offset="100%" stopColor="#7A4F0B" stopOpacity={1} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(212, 168, 48, 0.22)" />
        <XAxis 
          dataKey="name" 
          axisLine={false} 
          tickLine={false} 
          tick={{ fill: chartTextColor, fontSize: 12, opacity: 0.85 }} 
          dy={10} 
        />
        <YAxis 
          axisLine={false} 
          tickLine={false} 
          tick={{ fill: chartTextColor, fontSize: 12, opacity: 0.85 }} 
        />
        <RechartsTooltip 
          cursor={false}
          contentStyle={{ backgroundColor: 'rgba(0, 0, 0, 0.8)', border: 'none', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }}
          itemStyle={{ color: '#fff' }}
        />
        <Bar dataKey="risks" fill="url(#barGradient)" radius={[6, 6, 0, 0]} maxBarSize={50} activeBar={false} />
      </BarChart>
    </ResponsiveContainer>
  );

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Card 
        className="group relative cursor-pointer border-t-4 border-t-[#D4A830] bg-gradient-to-b from-background to-[#D4A830]/10 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-[#D4A830]/10"
        onClick={() => setExpandedChart("severity")}
      >
        <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
          <Maximize2 className="h-4 w-4 text-[#D4A830]" />
        </div>
        <CardHeader>
          <CardTitle className="text-[#FDE983]">Risk Severity Distribution</CardTitle>
          <CardDescription>Breakdown of active risks by severity level.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className={`h-[300px] w-full pointer-events-none ${chartSurfaceClassName}`}>
            {renderSeverityChart()}
          </div>
        </CardContent>
      </Card>

      <Card 
        className="group relative cursor-pointer border-t-4 border-t-[#E8C860] bg-gradient-to-b from-background to-[#D4A830]/10 transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:shadow-[#D4A830]/10"
        onClick={() => setExpandedChart("domain")}
      >
        <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity">
          <Maximize2 className="h-4 w-4 text-[#E8C860]" />
        </div>
        <CardHeader>
          <CardTitle className="text-[#FDE983]">Risks by Domain</CardTitle>
          <CardDescription>Number of identified risks across business domains.</CardDescription>
        </CardHeader>
        <CardContent>
          <div className={`h-[300px] w-full pointer-events-none ${chartSurfaceClassName}`}>
            {renderDomainChart()}
          </div>
        </CardContent>
      </Card>

      <Dialog open={!!expandedChart} onOpenChange={(open) => !open && setExpandedChart(null)}>
        <DialogContent className="sm:max-w-[800px] h-[600px] flex flex-col !border-none !ring-0 !outline-none shadow-none bg-background/95 backdrop-blur-xl p-0 overflow-hidden">
          <div className="flex flex-col h-full p-6">
            <DialogHeader className="border-none mb-4">
              <DialogTitle className="bg-gradient-to-r from-[#A07018] via-[#D4A830] to-[#FDE983] bg-clip-text text-2xl font-bold text-transparent">
                {expandedChart === "severity" ? "Risk Severity Distribution" : "Risks by Domain"}
              </DialogTitle>
              <DialogDescription className="text-muted-foreground/70">
                Detailed view and interaction for {expandedChart === "severity" ? "severity distribution" : "domain-wide risks"}.
              </DialogDescription>
            </DialogHeader>
            <div className={`flex-1 w-full bg-muted/5 rounded-2xl p-6 border-none outline-none ${chartSurfaceClassName}`}>
              {expandedChart === "severity" ? renderSeverityChart(true) : renderDomainChart()}
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
