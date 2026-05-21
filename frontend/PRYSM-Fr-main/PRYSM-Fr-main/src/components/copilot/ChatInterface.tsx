"use client";

import { FormEvent, KeyboardEvent, useEffect, useMemo, useRef, useState } from "react";
import Image from "next/image";
import { Bot, FileCheck2, Loader2, MessageSquareText, Send, ShieldCheck, Sparkles, UserRound } from "lucide-react";
import { cn } from "@/lib/utils";

type MessageRole = "user" | "assistant";

type Message = {
  id: string;
  role: MessageRole;
  content: string;
  createdAt: Date;
};

type SuggestedPrompt = {
  title: string;
  prompt: string;
  icon: typeof ShieldCheck;
};

const suggestedPrompts: SuggestedPrompt[] = [
  {
    icon: ShieldCheck,
    title: "Review audit readiness",
    prompt: "Review our audit readiness and call out the most important gaps.",
  },
  {
    icon: FileCheck2,
    title: "Find evidence gaps",
    prompt: "What evidence should I collect before sign-off?",
  },
  {
    icon: MessageSquareText,
    title: "Draft a summary",
    prompt: "Draft a concise executive audit summary.",
  },
  {
    icon: Sparkles,
    title: "Plan next actions",
    prompt: "Recommend the next compliance actions for this week.",
  },
];

function createMessage(role: MessageRole, content: string): Message {
  return {
    id: `${role}-${Date.now()}-${Math.random().toString(36).slice(2)}`,
    role,
    content,
    createdAt: new Date(),
  };
}

function isGreeting(input: string) {
  return /^(hi|hello|hey|good morning|good afternoon|good evening|yo)\b/i.test(input.trim());
}

function buildAssistantReply(input: string) {
  const normalized = input.toLowerCase();

  if (isGreeting(input)) {
    return "Hi, I am here. What would you like to work through today?";
  }

  if (normalized.includes("help") || normalized.includes("what can you do")) {
    return "I can help with audit readiness, compliance gap analysis, evidence checklists, risk triage, remediation plans, vendor review, and concise wording for reports or executive updates.";
  }

  if (normalized.includes("risk") || normalized.includes("critical") || normalized.includes("vendor")) {
    return [
      "Here is how I would approach it:",
      "",
      "1. Prioritize items with high business impact, overdue remediation, and weak supporting evidence.",
      "2. Separate control failures from documentation gaps so escalation stays focused.",
      "3. Ask each owner for remediation evidence, a target date, and any compensating controls.",
      "",
      "A good next step is to rank the findings by severity, age, owner, and materiality.",
    ].join("\n");
  }

  if (
    normalized.includes("gst") ||
    normalized.includes("tax") ||
    normalized.includes("invoice") ||
    normalized.includes("tds")
  ) {
    return [
      "For tax and invoice review, I would validate the basics first:",
      "",
      "1. Confirm extracted values match the source document and purchase records.",
      "2. Check tax IDs, GSTIN formats, rates, invoice totals, and period alignment.",
      "3. Group exceptions by vendor, period, and materiality so the audit team can act quickly.",
      "",
      "Share the discrepancy type and I can help structure a tighter review.",
    ].join("\n");
  }

  if (
    normalized.includes("evidence") ||
    normalized.includes("document") ||
    normalized.includes("signature") ||
    normalized.includes("approval")
  ) {
    return [
      "For evidence review, focus on completeness, authority, and traceability.",
      "",
      "Recommended checks:",
      "1. Confirm every control has current supporting evidence.",
      "2. Flag missing signatures, expired approvals, and incomplete vendor files.",
      "3. Link each exception to an owner, remediation deadline, and source record.",
      "",
      "I can also turn this into an audit workpaper format.",
    ].join("\n");
  }

  if (
    normalized.includes("audit") ||
    normalized.includes("compliance") ||
    normalized.includes("control") ||
    normalized.includes("readiness") ||
    normalized.includes("remediation")
  ) {
    return [
      "A professional compliance answer should be evidence-led and action-oriented.",
      "",
      "I would frame the response around:",
      "1. Current control posture and audit readiness.",
      "2. Material gaps or exceptions blocking sign-off.",
      "3. Evidence required to close each gap.",
      "4. Owners, timelines, and escalation points.",
      "",
      "Send me the control area or finding and I will make the response more specific.",
    ].join("\n");
  }

  if (
    normalized.includes("summary") ||
    normalized.includes("brief") ||
    normalized.includes("report") ||
    normalized.includes("board")
  ) {
    return [
      "A strong summary should stay concise and decision-ready.",
      "",
      "Suggested structure:",
      "1. Overall readiness and trend.",
      "2. Top material risks and affected domains.",
      "3. Evidence gaps that block sign-off.",
      "4. Decisions or resources needed from leadership.",
      "",
      "Send the findings you want included and I can draft the final wording.",
    ].join("\n");
  }

  return [
    "I can help with that. To make the answer useful, I would first clarify the process, evidence source, owner, and business impact.",
    "",
    "Try asking: \"Review this control for risk and evidence gaps\" or paste the finding you want cleaned up.",
  ].join("\n");
}

function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";

  return (
    <article className={cn("mx-auto flex w-full max-w-3xl gap-4 px-4 py-5", isUser && "justify-end")}>
      {!isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-[#A07018] via-[#D4A830] to-[#FDE983] text-[#0a0908] shadow-[0_0_24px_rgba(212,168,48,0.18)]">
          <Bot className="h-4 w-4" />
        </div>
      )}

      <div className={cn("min-w-0 text-sm leading-7", isUser ? "max-w-[78%]" : "max-w-[calc(100%-3rem)] flex-1")}>
        <div
          className={cn(
            "whitespace-pre-wrap",
            isUser
              ? "rounded-3xl bg-[#2a2d36] px-4 py-2.5 text-slate-100"
              : "pt-0.5 text-slate-200"
          )}
        >
          {message.content}
        </div>
      </div>

      {isUser && (
        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-[#D4A830]/20 bg-[#D4A830]/10 text-[#FDE983]">
          <UserRound className="h-4 w-4" />
        </div>
      )}
    </article>
  );
}

function TypingIndicator() {
  return (
    <div className="mx-auto flex w-full max-w-3xl gap-4 px-4 py-5">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-[#A07018] via-[#D4A830] to-[#FDE983] text-[#0a0908] shadow-[0_0_24px_rgba(212,168,48,0.18)]">
        <Bot className="h-4 w-4" />
      </div>
      <div className="flex items-center gap-2 pt-1 text-sm text-slate-400">
        <Loader2 className="h-4 w-4 animate-spin text-[#D4A830]" />
        Thinking
      </div>
    </div>
  );
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const canSend = input.trim().length > 0 && !isTyping;
  const isEmpty = messages.length === 0;

  const placeholder = useMemo(() => {
    if (isTyping) return "PRYSM Copilot is responding...";
    return "Message PRYSM Copilot";
  }, [isTyping]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, isTyping]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  function sendMessage(rawText: string) {
    const text = rawText.trim();
    if (!text || isTyping) return;

    setMessages((current) => [...current, createMessage("user", text)]);
    setInput("");
    setIsTyping(true);

    window.setTimeout(() => {
      setMessages((current) => [...current, createMessage("assistant", buildAssistantReply(text))]);
      setIsTyping(false);
    }, Math.min(1000, 360 + text.length * 10));
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    sendMessage(input);
  }

  function handleKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage(input);
    }
  }

  return (
    <div className="flex h-[calc(100vh-4rem)] min-h-[640px] flex-col bg-background text-slate-100">
      <section className="relative flex-1 overflow-y-auto bg-background">
        {isEmpty ? (
          <div className="mx-auto flex min-h-full w-full max-w-3xl flex-col items-center justify-center px-4 py-10 text-center">
            <div className="mb-5 flex h-14 w-14 items-center justify-center">
              <Image
                src="/prysm-logo-transparent.png"
                alt="PRYSM"
                width={56}
                height={42}
                className="h-auto w-14 object-contain"
                priority
              />
            </div>
            <h1 className="bg-gradient-to-r from-[#A07018] via-[#D4A830] to-[#FDE983] bg-clip-text text-2xl font-semibold tracking-normal text-transparent md:text-3xl">
              How can I help?
            </h1>
            <p className="mt-3 max-w-xl text-sm leading-6 text-[#FFF8E1]/62">
              Ask naturally about audits, evidence, controls, risks, reports, vendors, or remediation.
            </p>

            <div className="mt-8 grid w-full gap-3 sm:grid-cols-2">
              {suggestedPrompts.map(({ icon: Icon, title, prompt }) => (
                <button
                  key={title}
                  type="button"
                  onClick={() => sendMessage(prompt)}
                  className="group min-h-24 rounded-2xl border border-[#D4A830]/12 bg-[#141216] p-4 text-left transition hover:border-[#D4A830]/35 hover:bg-[#18140e]"
                >
                  <div className="flex items-start gap-3">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#D4A830]/10 text-[#FDE983] transition group-hover:bg-[#D4A830]/16">
                      <Icon className="h-4 w-4" />
                    </div>
                    <div>
                      <div className="text-sm font-medium text-slate-100">{title}</div>
                      <div className="mt-1 line-clamp-2 text-xs leading-5 text-[#FFF8E1]/42">{prompt}</div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="pb-4">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}
            {isTyping && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </div>
        )}
      </section>

      <footer className="sticky bottom-0 z-20 bg-gradient-to-t from-background via-background to-background/80 px-4 pb-4 pt-3">
        <form onSubmit={handleSubmit} className="mx-auto max-w-3xl">
          <div className="relative rounded-[1.65rem] border border-[#D4A830]/18 bg-[#121013] shadow-2xl shadow-black/30 transition focus-within:border-[#D4A830]/55 focus-within:ring-4 focus-within:ring-[#D4A830]/10">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
              disabled={isTyping}
              placeholder={placeholder}
              className="max-h-36 min-h-14 w-full resize-none bg-transparent py-4 pl-5 pr-16 text-sm leading-6 text-slate-100 outline-none placeholder:text-[#FFF8E1]/35 disabled:cursor-not-allowed disabled:opacity-70"
            />
            <button
              type="submit"
              disabled={!canSend}
              aria-label="Send message"
              className="absolute bottom-2.5 right-2.5 flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-[#A07018] via-[#D4A830] to-[#FDE983] text-[#0a0908] transition hover:shadow-[0_0_24px_rgba(212,168,48,0.28)] disabled:cursor-not-allowed disabled:bg-none disabled:bg-white/[0.08] disabled:text-slate-500 disabled:shadow-none"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
          <p className="mt-2 text-center text-[11px] leading-5 text-slate-600">
            PRYSM Copilot can help draft and reason, but high-impact findings should be verified against source evidence.
          </p>
        </form>
      </footer>
    </div>
  );
}
