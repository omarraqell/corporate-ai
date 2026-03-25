"use client";

import { useRef, useState } from "react";

interface ChatInputProps {
  onSend: (message: string) => void;
  isLoading: boolean;
}

export default function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [text, setText] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    if (!text.trim() || isLoading) return;
    onSend(text.trim());
    setText("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  };

  return (
    <div
      className="relative"
      style={{
        background: "var(--bg-secondary)",
        borderTop: "1px solid var(--border-subtle)",
      }}
    >
      <div className="max-w-4xl mx-auto px-4 py-4">
        <div
          className="flex items-end gap-3 rounded-2xl px-4 py-3 transition-all duration-200"
          style={{
            background: "var(--bg-tertiary)",
            border: "1px solid var(--border-medium)",
          }}
        >
          <textarea
            ref={textareaRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            onInput={handleInput}
            placeholder="Message the system..."
            disabled={isLoading}
            rows={1}
            className="flex-1 bg-transparent resize-none outline-none text-[14.5px] leading-relaxed placeholder:opacity-40"
            style={{
              color: "var(--text-primary)",
              fontFamily: "var(--font-body)",
              maxHeight: "160px",
            }}
          />

          <button
            onClick={handleSubmit}
            disabled={!text.trim() || isLoading}
            className="flex-shrink-0 w-9 h-9 flex items-center justify-center rounded-xl transition-all duration-200 hover:scale-105 active:scale-95 disabled:opacity-30 disabled:hover:scale-100"
            style={{
              background:
                text.trim() && !isLoading
                  ? "var(--accent-gold)"
                  : "var(--bg-elevated)",
              color: text.trim() && !isLoading ? "var(--bg-primary)" : "var(--text-tertiary)",
            }}
          >
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          </button>
        </div>

        <div
          className="text-center mt-2 text-[10px] tracking-widest uppercase"
          style={{
            color: "var(--text-muted)",
            fontFamily: "var(--font-mono)",
          }}
        >
          Enter to send · Shift+Enter for new line
        </div>
      </div>
    </div>
  );
}
