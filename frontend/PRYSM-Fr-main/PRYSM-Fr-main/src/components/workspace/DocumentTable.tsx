"use client";

import { useState } from "react";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Search, Filter, Download, MoreHorizontal, FileText, CheckCircle2, AlertCircle, Clock } from "lucide-react";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { cn } from "@/lib/utils";

const MOCK_DOCS = [
  { id: "DOC-1042", name: "Acme_Q3_Invoice_Final.pdf", type: "Invoice", uploadedBy: "Aiden Judge", date: "2 mins ago", status: "Processed", confidence: 98, entities: 14 },
  { id: "DOC-1043", name: "Vendor_Agreement_TechFlow.pdf", type: "Contract", uploadedBy: "Sarah Chen", date: "1 hr ago", status: "Processed", confidence: 92, entities: 28 },
  { id: "DOC-1044", name: "Tax_Return_2025.pdf", type: "Tax Return", uploadedBy: "Aiden Judge", date: "3 hrs ago", status: "Review Required", confidence: 75, entities: 42 },
  { id: "DOC-1045", name: "Employee_Roster_Oct.csv", type: "Payroll", uploadedBy: "Mike Ross", date: "1 day ago", status: "Processing", confidence: null, entities: 0 },
  { id: "DOC-1046", name: "Insurance_Cert_Global.pdf", type: "Certificate", uploadedBy: "Sarah Chen", date: "2 days ago", status: "Failed", confidence: 0, entities: 0 },
];

export function DocumentTable() {
  const [searchTerm, setSearchTerm] = useState("");

  const filteredDocs = MOCK_DOCS.filter(doc => 
    doc.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    doc.type.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
          <Button variant="outline" size="icon">
            <Filter className="h-4 w-4" />
          </Button>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" className="gap-2">
            <Download className="h-4 w-4" /> Export List
          </Button>
        </div>
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
            {filteredDocs.map((doc) => (
              <TableRow key={doc.id} className="hover:bg-muted/50 transition-colors group">
                <TableCell className="font-medium">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-muted rounded flex items-center justify-center shrink-0">
                      <FileText className="h-4 w-4 text-primary" />
                    </div>
                    <div className="flex flex-col">
                      <span className="truncate max-w-[200px]">{doc.name}</span>
                      <span className="text-xs text-muted-foreground">{doc.id}</span>
                    </div>
                  </div>
                </TableCell>
                <TableCell>
                  <Badge variant="outline" className="bg-background">{doc.type}</Badge>
                </TableCell>
                <TableCell>
                  <div className="flex items-center gap-1.5">
                    {doc.status === "Processed" && <CheckCircle2 className="h-4 w-4 text-emerald-500" />}
                    {doc.status === "Review Required" && <AlertCircle className="h-4 w-4 text-amber-500" />}
                    {doc.status === "Processing" && <Clock className="h-4 w-4 text-blue-500" />}
                    {doc.status === "Failed" && <AlertCircle className="h-4 w-4 text-destructive" />}
                    <span className="text-sm font-medium">{doc.status}</span>
                  </div>
                </TableCell>
                <TableCell>
                  {doc.confidence !== null ? (
                    <div className="flex items-center gap-2">
                      <div className="w-16 h-1.5 rounded-full bg-muted overflow-hidden">
                        <div 
                          className={cn(
                            "h-full rounded-full",
                            doc.confidence >= 90 ? "bg-emerald-500" : 
                            doc.confidence >= 70 ? "bg-amber-500" : "bg-destructive"
                          )} 
                          style={{ width: `${doc.confidence}%` }}
                        />
                      </div>
                      <span className="text-xs font-medium">{doc.confidence}%</span>
                    </div>
                  ) : (
                    <span className="text-muted-foreground text-sm">-</span>
                  )}
                </TableCell>
                <TableCell className="text-muted-foreground">{doc.entities || "-"}</TableCell>
                <TableCell>
                  <div className="flex flex-col">
                    <span className="text-sm">{doc.date}</span>
                    <span className="text-xs text-muted-foreground">by {doc.uploadedBy}</span>
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
                      <DropdownMenuItem>View details</DropdownMenuItem>
                      <DropdownMenuItem>Re-process extraction</DropdownMenuItem>
                      <DropdownMenuSeparator />
                      <DropdownMenuItem className="text-destructive">Delete document</DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
