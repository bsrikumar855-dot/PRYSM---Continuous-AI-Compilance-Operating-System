"use client";

import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { 
  UploadCloud, 
  CheckCircle2, 
  AlertCircle, 
  X,
  File
} from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";
import { uploadDocuments } from "@/lib/api";
import type { UploadedDocument } from "@/types/api";

type UploadStatus = "idle" | "uploading" | "success" | "review_required" | "excluded" | "error";

interface FileWithStatus {
  file: File;
  id: string;
  progress: number;
  status: UploadStatus;
  parsedDocuments?: UploadedDocument[];
  message?: string;
  error?: string;
}

export function UploadZone() {
  const [files, setFiles] = useState<FileWithStatus[]>([]);

  const uploadFile = useCallback(async (id: string, file: File) => {
    setFiles((prev) => 
        prev.map(f => f.id === id ? { ...f, progress: 50, status: "uploading", error: undefined, message: undefined } : f)
    );

    try {
      const result = await uploadDocuments([file]) as {
        documents?: UploadedDocument[];
        document?: UploadedDocument;
      };
      const docs = result.documents || (result.document ? [result.document] : []);
      const screeningStatus = docs[0]?.status;
      const uploadStatus: UploadStatus =
        screeningStatus === "excluded" || screeningStatus === "review_required"
          ? screeningStatus
          : "success";

      setFiles((prev) =>
        prev.map(f => f.id === id ? {
          ...f,
          progress: 100,
          status: uploadStatus,
          parsedDocuments: docs,
          message: docs.length === 0 ? "Upload completed, but no parsed documents were returned." : undefined,
        } : f)
      );
    } catch (error) {
      console.error("Upload failed:", error);

      setFiles((prev) =>
        prev.map(f => f.id === id ? {
          ...f,
          progress: 0,
          status: "error",
          error: error instanceof Error ? error.message : "Upload failed. Please make sure the backend server is running at http://127.0.0.1:8001.",
        } : f)
      );
    }
  }, []);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const newFiles = acceptedFiles.map((file) => ({
      file,
      id: Math.random().toString(36).substring(7),
      progress: 0,
      status: "idle" as UploadStatus,
    }));
    
    setFiles((prev) => [...prev, ...newFiles]);
    
    newFiles.forEach((fileObj) => {
      uploadFile(fileObj.id, fileObj.file);
    });
  }, [uploadFile]);

  const removeFile = (id: string) => {
    setFiles((prev) => prev.filter(f => f.id !== id));
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png']
    },
  });

  return (
    <div className="w-full space-y-6">
      <div 
        {...getRootProps()} 
        className={cn(
          "relative flex flex-col items-center justify-center w-full h-64 px-4 py-8 border-2 border-dashed rounded-xl transition-all duration-200 cursor-pointer bg-card",
          isDragActive 
            ? "border-primary bg-primary/5" 
            : "border-border hover:border-primary/50 hover:bg-muted/50"
        )}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center space-y-4 text-center">
          <div className={cn(
            "p-4 rounded-full transition-colors",
            isDragActive ? "bg-primary/20 text-primary" : "bg-muted text-muted-foreground"
          )}>
            <UploadCloud className="w-8 h-8" />
          </div>
          <div className="space-y-1">
            <p className="text-sm font-semibold text-foreground">
              Click to upload or drag and drop
            </p>
            <p className="text-xs text-muted-foreground">
              PDF, JPEG, or PNG (max. 50MB)
            </p>
          </div>
        </div>
      </div>

      {files.length > 0 && (
        <div className="space-y-3">
          <h3 className="text-sm font-medium text-foreground">Uploading files</h3>
          <div className="space-y-3">
            {files.map((fileObj) => (
              <div 
                key={fileObj.id} 
                className="flex flex-col gap-2 p-4 border border-border rounded-lg bg-card shadow-sm transition-all"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-muted rounded-md text-muted-foreground">
                      <File className="w-4 h-4" />
                    </div>
                    <div>
                      <p className="text-sm font-medium text-foreground truncate max-w-[200px] sm:max-w-xs">
                        {fileObj.file.name}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {(fileObj.file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3">
                    {fileObj.status === "uploading" && (
                      <span className="text-xs font-medium text-muted-foreground">
                        {fileObj.progress}%
                      </span>
                    )}
                    {fileObj.status === "success" && (
                      <CheckCircle2 className="w-5 h-5 text-emerald-500" />
                    )}
                    {(fileObj.status === "excluded" || fileObj.status === "review_required") && (
                      <AlertCircle className="w-5 h-5 text-amber-500" />
                    )}
                    {fileObj.status === "error" && (
                      <AlertCircle className="w-5 h-5 text-destructive" />
                    )}
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        removeFile(fileObj.id);
                      }}
                      className="p-1 text-muted-foreground hover:text-foreground hover:bg-muted rounded-md transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                {fileObj.status === "uploading" && (
                  <Progress value={fileObj.progress || 50} className="h-1.5" />
                )}

                {fileObj.status === "error" && fileObj.error && (
                  <p className="text-xs text-destructive">{fileObj.error}</p>
                )}

                {fileObj.status !== "error" && fileObj.status !== "uploading" && fileObj.parsedDocuments && fileObj.parsedDocuments.length > 0 && (
                  <div className="rounded-md border bg-muted/30 p-3 text-xs text-muted-foreground">
                    {fileObj.parsedDocuments.map((document, index) => (
                      <div key={document.id ?? document.document_id ?? index} className="space-y-1">
                        <p className="font-medium text-foreground">{document.filename ?? document.id ?? document.document_id ?? fileObj.file.name}</p>
                        {document.status && <p>Status: {document.status}</p>}
                        {document.screening?.reason && <p>{document.screening.reason}</p>}
                        {document.raw_text_preview && <p className="line-clamp-2">Preview: {document.raw_text_preview}</p>}
                      </div>
                    ))}
                  </div>
                )}

                {fileObj.status === "success" && fileObj.message && (
                  <p className="text-xs text-muted-foreground">{fileObj.message}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
