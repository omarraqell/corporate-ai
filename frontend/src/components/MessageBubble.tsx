"use client";

import { Message } from "@/hooks/useChat";
import AgentBadge from "./AgentBadge";

interface MessageBubbleProps {
  message: Message;
  index: number;
}

export default function MessageBubble({ message, index }: MessageBubbleProps) {
  const isUser = message.role === "user";

  if (message.isLoading) {
    return (
      <div
        className="animate-fade-in-up flex justify-start"
        style={{ animationDelay: `${index * 50}ms` }}
      >
        <div
          className="max-w-[75%] px-5 py-4 rounded-2xl"
          style={{
            background: "var(--bg-tertiary)",
            borderRadius: "var(--radius-lg)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <div className="flex items-center gap-3">
            <div className="flex gap-1">
              <span
                className="w-2 h-2 rounded-full animate-pulse"
                style={{
                  background: "var(--accent-gold)",
                  animationDelay: "0ms",
                }}
              />
              <span
                className="w-2 h-2 rounded-full animate-pulse"
                style={{
                  background: "var(--accent-gold)",
                  animationDelay: "300ms",
                }}
              />
              <span
                className="w-2 h-2 rounded-full animate-pulse"
                style={{
                  background: "var(--accent-gold)",
                  animationDelay: "600ms",
                }}
              />
            </div>
            <span
              className="text-xs"
              style={{
                color: "var(--text-tertiary)",
                fontFamily: "var(--font-mono)",
              }}
            >
              Processing...
            </span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`animate-fade-in-up flex ${isUser ? "justify-end" : "justify-start"}`}
      style={{ animationDelay: `${index * 50}ms` }}
    >
      <div className={`max-w-[75%] ${isUser ? "" : ""}`}>
        {/* Agent badges for assistant messages */}
        {!isUser && message.agentName && (
          <div className="mb-2 ml-1">
            <AgentBadge
              agentName={message.agentName}
              classification={message.classification}
            />
          </div>
        )}

        {/* Message bubble */}
        <div
          className="px-5 py-3.5 relative"
          style={{
            background: isUser ? "var(--accent-gold)" : "var(--bg-tertiary)",
            color: isUser ? "var(--bg-primary)" : "var(--text-primary)",
            borderRadius: isUser
              ? "var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg)"
              : "var(--radius-sm) var(--radius-lg) var(--radius-lg) var(--radius-lg)",
            border: isUser ? "none" : "1px solid var(--border-subtle)",
          }}
        >
          <div
            className="text-[14.5px] leading-relaxed whitespace-pre-wrap break-words"
            style={{
              fontFamily: "var(--font-body)",
              fontWeight: isUser ? 500 : 400,
            }}
          >
            {message.content}
          </div>
        </div>

        {/* Timestamp */}
        <div
          className={`mt-1.5 text-[10px] ${isUser ? "text-right mr-1" : "ml-1"}`}
          style={{
            color: "var(--text-muted)",
            fontFamily: "var(--font-mono)",
          }}
        >
          {message.timestamp.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </div>
      </div>
    </div>
  );
}
