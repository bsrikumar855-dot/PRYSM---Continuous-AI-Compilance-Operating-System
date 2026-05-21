import { KPICards } from "@/components/dashboard/KPICards";
import { RiskCharts } from "@/components/dashboard/RiskCharts";
import { RiskTable } from "@/components/dashboard/RiskTable";

export default function DashboardPage() {
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
      
      <KPICards />
      <RiskCharts />
      <div className="mt-4">
        <h2 className="text-xl font-semibold mb-4 tracking-tight">Active Risks</h2>
        <RiskTable />
      </div>
    </div>
  );
}
