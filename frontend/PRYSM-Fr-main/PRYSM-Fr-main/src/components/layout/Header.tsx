"use client";

import { Bell, Search } from "lucide-react";
import { Input } from "@/components/ui/input";

export function Header() {
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
        <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors rounded-full hover:bg-muted">
          <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-destructive" />
          <Bell className="h-5 w-5" />
          <span className="sr-only">Notifications</span>
        </button>
      </div>
    </header>
  );
}
