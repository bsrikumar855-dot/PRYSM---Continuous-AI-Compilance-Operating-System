"use client";

import { useState, useEffect } from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search, Filter, Download, MoreHorizontal, FileText, CheckCircle2, AlertCircle, Clock } from "lucide-react";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { cn } from "@/lib/utils";
import { deleteDocument, downloadDocumentFile, fetchDocuments, reprocessDocument } from "@/lib/api";

type ScreeningFilter = "all" | "accepted" | "review_required" | "excluded";

export function DocumentTable() {
  const [searchTerm, setSearchTerm] = useState("");
  const [screeningFilter, setScreeningFilter] = useState<ScreeningFilter>("all");
  const [documents, setDocuments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<string | null>(null);

  async function loadDocs() {
    try {
      setLoading(true);
      const data = await fetchDocuments() as any;
      const docsArr = data.documents || data.data || data.items || [];
      setDocuments(docsArr);
      setError(null);
    } catch {
      setError("Backend is not running. Please start FastAPI server.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDocs();
  }, []);

  const filteredDocs = documents.filter(doc => {
    const name = doc.filename || doc.name || doc.id || "";
    const type = doc.document_type || doc.type || "Document";
    const decision = doc.screening?.decision || "accepted";
    const matchesSearch = name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      type.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = screeningFilter === "all" || decision === screeningFilter;
    return matchesSearch && matchesFilter;
  });

  const cycleFilter = () => {
    const options: ScreeningFilter[] = ["all", "accepted", "review_required", "excluded"];
    const nextIndex = (options.indexOf(screeningFilter) + 1) % options.length;
    setScreeningFilter(options[nextIndex]);
  };

  const openSourceFile = async (documentId: string) => {
    try {
      const blob = await downloadDocumentFile(documentId);
      const objectUrl = URL.createObjectURL(blob);
      window.open(objectUrl, "_blank", "noopener,noreferrer");
      window.setTimeout(() => URL.revokeObjectURL(objectUrl), 60000);
    } catch (err) {
      setFeedback(err instanceof Error ? err.message : "Unable to open source file.");
    }
  };

  const handleReprocess = async (documentId: string) => {
    try {
      await reprocessDocument(documentId);
      await loadDocs();
      setFeedback("Extraction was reprocessed from the uploaded source file.");
    } catch (err) {
      setFeedback(err instanceof Error ? err.message : "Unable to reprocess document.");
    }
  };

  const handleDelete = async (documentId: string) => {
    try {
      await deleteDocument(documentId);
      setDocuments(current => current.filter(doc => (doc.id || doc.document_id) !== documentId));
      setFeedback("Document removed from this audit session.");
    } catch (err) {
      setFeedback(err instanceof Error ? err.message : "Unable to delete document.");
    }
  };

  const exportList = () => {
    const rows = filteredDocs.map(doc => [
      doc.filename || doc.name || doc.id,
      doc.data?.document_type || "unknown",
      doc.screening?.decision || doc.status || "accepted",
      doc.uploaded_at || "",
    ]);
    const csv = [["Document Name", "Type", "Screening", "Uploaded"], ...rows]
      .map(row => row.map(value => `"${String(value).replaceAll("\"", "\"\"")}"`).join(","))
      .join("\r\n");
    const url = URL.createObjectURL(new Blob([csv], { type: "text/csv;charset=utf-8" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = "prysm-documents.csv";
    link.click();
    URL.revokeObjectURL(url);
  };

  if (loading) {
    return <div className="p-6">Loading documents from backend...</div>;
  }

  if (error) {
    return <div className="p-6 text-destructive">{error}</div>;
  }

  if (documents.length === 0) {
    return (
      <div className="p-6 text-center text-muted-foreground">
        No documents found.
      </div>
    );
  }

  return (
    <div className="space-y-4 bg-card border rounded-lg p-6">
      <div className="flex flex-col sm:flex-row justify-between gap-4">
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <div className="relative w-full sm:w-80">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search documents..."
              className="pl-9"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <Button variant="outline" size="icon" onClick={cycleFilter} title={`Filter: ${screeningFilter}`}>
            <Filter className="h-4 w-4" />
          </Button>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" className="gap-2" onClick={exportList}>
            <Download className="h-4 w-4" /> Export List
          </Button>
        </div>
      </div>
      <div className="flex items-center justify-between text-xs text-muted-foreground">
        <span>Showing {filteredDocs.length} document(s). Filter: {screeningFilter.replace("_", " ")}.</span>
        {feedback && <span>{feedback}</span>}
      </div>
      
      <div className="rounded-md border overflow-hidden">
        <Table>
          <TableHeader className="bg-muted/50">
            <TableRow>
              <TableHead className="w-[300px]">Document Name</TableHead>
              <TableHead>Type</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Confidence</TableHead>
              <TableHead>Entities</TableHead>
              <TableHead>Uploaded</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {filteredDocs.map((doc, index) => {
              const id = doc.id || doc.document_id || `DOC-${index}`;
              const name = doc.filename || doc.name || id;
              
              // Get document type from data.document_type
              const rawType = doc.data?.document_type || doc.document_type || doc.type || "unknown";
              const type = doc.status === "excluded" ? "Unsupported" :
                           rawType === "invoice" ? "Invoice" :
                           rawType === "audit_report" ? "Audit Report" :
                           rawType === "bank_statement" ? "Bank Statement" :
                           rawType === "gst_return" ? "GST Return" :
                           rawType === "unknown" ? "Document" :
                           rawType.charAt(0).toUpperCase() + rawType.slice(1);

              // Map status dynamically based on risks
              let status = doc.status || "Processed";
              if (status === "uploaded") {
                const hasReviewRisks = (doc.risks || []).some((r: any) => 
                  (r.severity || "").toLowerCase() === "critical" || 
                  (r.severity || "").toLowerCase() === "warning"
                );
                status = hasReviewRisks ? "Review Required" : "Processed";
              } else if (status === "failed") {
                status = "Failed";
              } else if (status === "excluded") {
                status = "Excluded";
              } else if (status === "review_required") {
                status = "Needs Review";
              }

              // Calculate extraction confidence based on how many fields are populated
              let confidence = 95;
              if (doc.screening?.confidence != null) {
                confidence = doc.screening.confidence;
              } else if (doc.confidence != null) {
                confidence = doc.confidence;
              } else if (doc.metrics?.confidence != null) {
                confidence = doc.metrics.confidence;
              } else if (status === "Failed") {
                confidence = 0;
              } else {
                const text = doc.raw_text_preview || "";
                const data = doc.data || {};
                const docType = data.document_type || "unknown";

                if (!text && docType === "unknown") {
                  confidence = 30; // OCR/Text extraction failed
                } else if (docType === "unknown") {
                  confidence = 65; // OCR succeeded but classification failed
                } else {
                  const fields = Object.keys(data).filter(key => key !== "document_type");
                  const relevantFields = fields.filter(key => data[key] !== "NOT_APPLICABLE");
                  if (relevantFields.length > 0) {
                    const knownFields = relevantFields.filter(key => data[key] && data[key] !== "UNKNOWN");
                    const ratio = knownFields.length / relevantFields.length;
                    confidence = Math.round(70 + ratio * 28);
                  } else {
                    confidence = 85;
                  }
                }
              }

              // Count parsed fields as entities
              const dataObj = doc.data || {};
              const extractedEntities = Object.keys(dataObj).filter(key => 
                key !== "document_type" && 
                dataObj[key] && 
                dataObj[key] !== "UNKNOWN" && 
                dataObj[key] !== "NOT_APPLICABLE"
              );
              const entitiesCount = extractedEntities.length;

              // Format date nicely from uploaded_at timestamp
              const dateStr = doc.uploaded_at || doc.date || doc.created_at;
              const formatDate = (str: string | undefined) => {
                if (!str) return "Just now";
                try {
                  const d = new Date(str);
                  if (isNaN(d.getTime())) return "Just now";
                  return d.toLocaleDateString(undefined, { 
                    month: 'short', 
                    day: 'numeric', 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  });
                } catch {
                  return "Just now";
                }
              };
              const date = formatDate(dateStr);
              const uploadedBy = doc.uploaded_by || doc.uploadedBy || "System";

              return (
              <TableRow key={id} className="hover:bg-muted/50 transition-colors group">
                <TableCell className="font-medium">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-muted rounded flex items-center justify-center shrink-0">
                      <FileText className="h-4 w-4 text-primary" />
                    </div>
                    <div className="flex flex-col">
                      <span className="truncate max-w-[200px]">{name}</span>
                      <span className="text-xs text-muted-foreground">{id}</span>
                      {doc.screening?.audit_eligible === false && doc.screening?.reason && (
                        <span className="max-w-[260px] text-xs text-muted-foreground">{doc.screening.reason}</span>
                      )}
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge variant="outline" className="bg-background">{type}</Badge>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-1.5">
                    {status === "Processed" && <CheckCircle2 className="h-4 w-4 text-emerald-500" />}
                    {status === "Review Required" && <AlertCircle className="h-4 w-4 text-amber-500" />}
                    {status === "Needs Review" && <AlertCircle className="h-4 w-4 text-amber-500" />}
                    {status === "Processing" && <Clock className="h-4 w-4 text-blue-500" />}
                    {status === "Failed" && <AlertCircle className="h-4 w-4 text-destructive" />}
                    {status === "Excluded" && <AlertCircle className="h-4 w-4 text-muted-foreground" />}
                    <span className="text-sm font-medium">{status}</span>
                  </div>
                </TableCell>
                <TableCell>
                  {confidence !== null ? (
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-1.5 rounded-full bg-muted overflow-hidden">
                        <div 
                          className={cn(
                            "h-full rounded-full",
                            confidence >= 90 ? "bg-emerald-500" : 
                            confidence >= 70 ? "bg-amber-500" : "bg-destructive"
                          )} 
                          style={{ width: `${confidence}%` }}
                        />
                      </div>
                      <span className="text-xs font-medium">{confidence}%</span>
                    </div>
                  ) : (
                    <span className="text-muted-foreground text-sm">-</span>
                  )}
                </TableCell>
                <TableCell className="text-muted-foreground">{entitiesCount || "-"}</TableCell>
                <TableCell>
                  <div className="flex flex-col">
                    <span className="text-sm">{date}</span>
                    <span className="text-xs text-muted-foreground">by {uploadedBy}</span>
                  </div>
                </TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger className="inline-flex h-8 w-8 items-center justify-center rounded-md p-0 text-sm font-medium transition-colors hover:bg-muted hover:text-foreground opacity-0 group-hover:opacity-100 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring">
                      <span className="sr-only">Open menu</span>
                      <MoreHorizontal className="h-4 w-4" />
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuLabel>Actions</DropdownMenuLabel>
                      <DropdownMenuItem onClick={() => openSourceFile(id)}>View source file</DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleReprocess(id)}>Re-process extraction</DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="text-destructive" onClick={() => handleDelete(id)}>Delete document</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
