import { UploadZone } from "@/components/upload/UploadZone";

export default function UploadPage() {
  return (
    <div className="flex flex-col gap-6 max-w-4xl mx-auto w-full">
      <div>
        <h1 className="bg-gradient-to-r from-[#A07018] via-[#D4A830] to-[#FDE983] bg-clip-text text-3xl font-bold tracking-tight text-transparent">
          Document Ingestion
        </h1>
        <p className="text-muted-foreground mt-2">
          Securely upload compliance documents for AI extraction and risk analysis.
        </p>
      </div>
      <div className="mt-4">
        <UploadZone />
      </div>
    </div>
  );
}
