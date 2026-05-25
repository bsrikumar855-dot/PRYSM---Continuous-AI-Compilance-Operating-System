import { Bell, Database, Shield, UserRound } from "lucide-react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const settings = [
  {
    title: "Profile",
    description: "Manage auditor details, role, and workspace identity.",
    icon: UserRound,
  },
  {
    title: "Notifications",
    description: "Control alerts for new risks, reports, and review requests.",
    icon: Bell,
  },
  {
    title: "Security",
    description: "Configure access controls and review authentication status.",
    icon: Shield,
  },
  {
    title: "Data Sources",
    description: "Connect document repositories and compliance evidence stores.",
    icon: Database,
  },
];

export default function SettingsPage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="bg-gradient-to-r from-[#A07018] via-[#D4A830] to-[#FDE983] bg-clip-text text-3xl font-bold tracking-tight text-transparent">
          Settings
        </h1>
        <p className="mt-2 text-muted-foreground">
          Configure workspace preferences and audit system controls.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {settings.map((item) => (
          <Card key={item.title}>
            <CardHeader className="flex flex-row items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-md bg-primary/10 text-primary">
                <item.icon className="h-5 w-5" aria-hidden="true" />
              </div>
              <CardTitle className="text-base">{item.title}</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground">
              {item.description}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
