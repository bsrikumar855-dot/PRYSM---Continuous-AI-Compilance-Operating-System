import { PipelineVisualization } from "@/components/extraction/PipelineVisualization";

export default function ExtractionPage() {
  return (
    <div className="flex flex-col gap-6 w-full max-w-5xl mx-auto">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">AI Extraction Pipeline</h1>
        <p className="text-muted-foreground mt-2">
          Real-time visualization of document processing and entity extraction.
        </p>
      </div>
      <PipelineVisualization />
    </div>
  );
}
