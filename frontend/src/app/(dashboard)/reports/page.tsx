import { ReportViewer } from "@/components/reports/ReportViewer";

export default function ReportsPage() {
  return (
    <div className="flex flex-col gap-6 w-full h-full">
      <div>
        <h1 className="bg-gradient-to-r from-[#A07018] via-[#D4A830] to-[#FDE983] bg-clip-text text-3xl font-bold tracking-tight text-transparent">
          Audit Reports
        </h1>
        <p className="text-muted-foreground mt-2">
          Generate, view, and export comprehensive compliance audit reports.
        </p>
      </div>
      
      <ReportViewer />
    </div>
  );
}
