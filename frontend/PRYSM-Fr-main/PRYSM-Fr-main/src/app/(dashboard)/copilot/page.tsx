import { ChatInterface } from "@/components/copilot/ChatInterface";

export default function CopilotPage() {
  return (
    <main className="-m-6 min-h-[calc(100vh-4rem)] bg-background text-slate-100 md:-m-8 lg:-m-10">
      <ChatInterface />
    </main>
  );
}
