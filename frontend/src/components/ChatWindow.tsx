"use client";

import { useEffect, useRef } from "react";
import { Message } from "@/hooks/useChat";
import MessageBubble from "./MessageBubble";

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
}

export default function ChatWindow({ messages, isLoading }: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center px-6">
        <div className="text-center max-w-lg">
          {/* Logo mark */}
          <div
            className="w-20 h-20 mx-auto mb-8 rounded-2xl flex items-center justify-center animate-pulse-glow"
            style={{
              background:
                "linear-gradient(135deg, var(--accent-gold-glow), transparent)",
              border: "1px solid var(--accent-gold-dim)",
            }}
          >
            <span className="text-3xl">👑</span>
          </div>

          <h1
            className="text-4xl mb-3 tracking-tight"
            style={{
              fontFamily: "var(--font-display)",
              color: "var(--text-primary)",
            }}
          >
            Corporate AI
          </h1>

          <p
            className="text-sm leading-relaxed mb-10"
            style={{
              color: "var(--text-tertiary)",
              fontFamily: "var(--font-body)",
              maxWidth: "380px",
              margin: "0 auto 2.5rem",
            }}
          >
            Your multi-agent system is ready. Ask a question, request analysis,
            assign tasks, or get reports written.
          </p>

          {/* Suggestion chips */}
          <div className="flex flex-wrap justify-center gap-2">
            {[
              "What is our vacation policy?",
              "Analyze Q4 sales trends",
              "Write a project status report",
              "Debug the auth endpoint",
            ].map((suggestion) => (
              <button
                key={suggestion}
                className="px-4 py-2 rounded-full text-xs transition-all duration-200 hover:scale-[1.02] active:scale-[0.98]"
                style={{
                  background: "var(--bg-tertiary)",
                  color: "var(--text-secondary)",
                  border: "1px solid var(--border-subtle)",
                  fontFamily: "var(--font-mono)",
                }}
                onClick={() => {
                  // Dispatch custom event for parent to handle
                  window.dispatchEvent(
                    new CustomEvent("suggestion-click", {
                      detail: suggestion,
                    })
                  );
                }}
              >
                {suggestion}
              </button>
            ))}
          </div>

          {/* Agent roster */}
          <div
            className="mt-12 pt-8"
            style={{ borderTop: "1px solid var(--border-subtle)" }}
          >
            <div
              className="text-[10px] tracking-[0.2em] uppercase mb-4"
              style={{
                color: "var(--text-muted)",
                fontFamily: "var(--font-mono)",
              }}
            >
              Active Agents
            </div>
            <div className="flex justify-center gap-6">
              {[
                { emoji: "📋", name: "Secretary" },
                { emoji: "🔍", name: "Research" },
                { emoji: "📊", name: "Data" },
                { emoji: "✍️", name: "Writer" },
                { emoji: "💻", name: "Code Dev" },
                { emoji: "🔎", name: "QA" },
              ].map((agent) => (
                <div key={agent.name} className="text-center group">
                  <div
                    className="w-10 h-10 rounded-xl flex items-center justify-center mb-1.5 transition-all duration-200 group-hover:scale-110"
                    style={{
                      background: "var(--bg-tertiary)",
                      border: "1px solid var(--border-subtle)",
                    }}
                  >
                    <span className="text-lg">{agent.emoji}</span>
                  </div>
                  <div
                    className="text-[9px] tracking-wider uppercase"
                    style={{
                      color: "var(--text-muted)",
                      fontFamily: "var(--font-mono)",
                    }}
                  >
                    {agent.name}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-4xl mx-auto px-4 py-6 space-y-5">
        {messages.map((msg, i) => (
          <MessageBubble key={msg.id} message={msg} index={i} />
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
