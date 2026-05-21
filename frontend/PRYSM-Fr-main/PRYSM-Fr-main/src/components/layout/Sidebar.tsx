"use client";

import { useState } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { 
  ChevronLeft,
  ChevronRight,
  LayoutDashboard, 
  UploadCloud, 
  FileText, 
  ShieldAlert, 
  Bot, 
  BarChart3,
  Settings
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Upload", href: "/upload", icon: UploadCloud },
  { name: "Workspace", href: "/workspace", icon: FileText },
  { name: "Risks", href: "/risks", icon: ShieldAlert },
  { name: "Chatbot", href: "/copilot", icon: Bot },
  { name: "Reports", href: "/reports", icon: BarChart3 },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div
      className={cn(
        "relative flex h-full shrink-0 flex-col border-r border-transparent bg-background transition-[width] duration-300",
        isCollapsed ? "w-20" : "w-64"
      )}
    >
      <div className={cn("relative flex h-16 shrink-0 items-center", isCollapsed ? "justify-center px-3" : "px-6 pr-12")}>
        <Link href="/" className="flex items-center gap-2 group">
          <Image
            src="/prysm-logo-transparent.png"
            alt="PRYSM Logo"
            width={32}
            height={24}
            className="object-contain"
          />
          {!isCollapsed && (
            <span className="font-bold text-xl tracking-wide text-transparent bg-clip-text" style={{ backgroundImage: "linear-gradient(160deg, #9A7016 0%, #B88D23 18%, #D3A932 36%, #EDC749 54%, #FDE983 72%, #DBB33B 86%, #9A7016 100%)" }}>PRYSM</span>
          )}
        </Link>
        <button
          type="button"
          onClick={() => setIsCollapsed((current) => !current)}
          className={cn(
            "absolute right-2 top-1/2 flex h-8 w-8 -translate-y-1/2 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-muted hover:text-foreground",
            isCollapsed && "right-1"
          )}
          aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {isCollapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </button>
      </div>
      {!isCollapsed && (
        <>
          <nav className="flex-1 space-y-1 px-3 py-4">
            {navigation.map((item) => {
              const isActive = pathname.startsWith(item.href);
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "group flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                    isActive
                      ? "bg-primary/10 text-primary"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  )}
                >
                  <item.icon
                    className={cn(
                      "h-5 w-5 shrink-0",
                      isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground"
                    )}
                    aria-hidden="true"
                  />
                  {item.name}
                </Link>
              );
            })}
          </nav>
          <div className="p-4 border-t border-transparent">
            <div className="flex items-center gap-3 rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-muted hover:text-foreground cursor-pointer transition-colors">
              <div className="h-8 w-8 rounded-full bg-secondary flex items-center justify-center text-secondary-foreground font-medium">
                AJ
              </div>
              <div className="flex flex-col">
                <span className="font-medium text-foreground text-xs">Aiden Judge</span>
                <span className="text-[10px]">Lead Auditor</span>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
