import { DocumentTable } from "@/components/workspace/DocumentTable";

export default function WorkspacePage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="mb-2">
          <h1 className="bg-gradient-to-r from-[#A07018] via-[#D4A830] to-[#FDE983] bg-clip-text pb-1 text-4xl font-extrabold tracking-tight text-transparent drop-shadow-sm">
            Document Workspace
          </h1>
          <p className="text-muted-foreground mt-2 text-lg">
            Centralized operations center for all ingested compliance documents.
          </p>
        </div>
      </div>
      
      <DocumentTable />
    </div>
  );
}
