import { RiskTable } from "@/components/dashboard/RiskTable";

export default function RisksPage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="bg-gradient-to-r from-[#A07018] via-[#D4A830] to-[#FDE983] bg-clip-text text-3xl font-bold tracking-tight text-transparent">
          Risks
        </h1>
        <p className="mt-2 text-muted-foreground">
          Review, filter, and investigate active compliance risks.
        </p>
      </div>

      <RiskTable />
    </div>
  );
}
