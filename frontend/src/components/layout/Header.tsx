"use client";

import { useState, useEffect } from "react";
import { Bell, Search, Activity, AlertCircle } from "lucide-react";
import { Input } from "@/components/ui/input";
import { healthCheck } from "@/lib/api";

export function Header() {
  const [isBackendUp, setIsBackendUp] = useState<boolean | null>(null);

  useEffect(() => {
    async function checkBackend() {
      try {
        await healthCheck();
        setIsBackendUp(true);
      } catch (err) {
        setIsBackendUp(false);
      }
    }
    checkBackend();
    const interval = setInterval(checkBackend, 30000); // Check every 30s
    return () => clearInterval(interval);
  }, []);

  return (
    <header className="flex h-16 shrink-0 items-center gap-4 border-b border-border bg-background px-6">
      <div className="flex flex-1 items-center gap-4">
        <div className="w-full max-w-md relative">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search documents, entities, or risks..."
            className="w-full appearance-none bg-muted/50 pl-9 shadow-none focus-visible:ring-1 focus-visible:ring-primary h-9"
          />
        </div>
      </div>
      <div className="flex items-center gap-4">
        {isBackendUp === true && (
          <div className="flex items-center gap-1.5 text-xs font-medium text-emerald-500 bg-emerald-500/10 px-2 py-1 rounded-full">
            <Activity className="h-3.5 w-3.5" />
            Backend connected
          </div>
        )}
        {isBackendUp === false && (
          <div className="flex items-center gap-1.5 text-xs font-medium text-destructive bg-destructive/10 px-2 py-1 rounded-full">
            <AlertCircle className="h-3.5 w-3.5" />
            Backend offline
          </div>
        )}
        <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors rounded-full hover:bg-muted">
          <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-destructive" />
          <Bell className="h-5 w-5" />
          <span className="sr-only">Notifications</span>
        </button>
      </div>
    </header>
  );
}
