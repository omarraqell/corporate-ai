"use client";

import { useCallback, useEffect } from "react";
import ChatInput from "@/components/ChatInput";
import ChatWindow from "@/components/ChatWindow";
import Sidebar from "@/components/Sidebar";
import { useChat } from "@/hooks/useChat";

export default function ChatPage() {
  const { messages, isLoading, sessionId, send, clearMessages } = useChat();

  // Handle suggestion chip clicks from ChatWindow
  const handleSuggestion = useCallback(
    (e: Event) => {
      const detail = (e as CustomEvent).detail;
      if (detail) send(detail);
    },
    [send]
  );

  useEffect(() => {
    window.addEventListener("suggestion-click", handleSuggestion);
    return () =>
      window.removeEventListener("suggestion-click", handleSuggestion);
  }, [handleSuggestion]);

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar sessionId={sessionId} onNewChat={clearMessages} />

      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <div
          className="flex-shrink-0 flex items-center justify-between px-6 py-3"
          style={{
            background: "var(--bg-secondary)",
            borderBottom: "1px solid var(--border-subtle)",
          }}
        >
          <div className="flex items-center gap-3">
            <h2
              className="text-lg"
              style={{
                fontFamily: "var(--font-display)",
                color: "var(--text-primary)",
              }}
            >
              Conversation
            </h2>
            {isLoading && (
              <div className="flex items-center gap-2">
                <div
                  className="w-1.5 h-1.5 rounded-full animate-pulse"
                  style={{ background: "var(--accent-gold)" }}
                />
                <span
                  className="text-[10px] tracking-widest uppercase"
                  style={{
                    color: "var(--accent-gold-dim)",
                    fontFamily: "var(--font-mono)",
                  }}
                >
                  Agents Working
                </span>
              </div>
            )}
          </div>

          <div
            className="text-[10px] tracking-wider"
            style={{
              color: "var(--text-muted)",
              fontFamily: "var(--font-mono)",
            }}
          >
            {messages.filter((m) => m.role === "user").length} messages
          </div>
        </div>

        {/* Messages area */}
        <ChatWindow messages={messages} isLoading={isLoading} />

        {/* Input */}
        <ChatInput onSend={send} isLoading={isLoading} />
      </div>
    </div>
  );
}
