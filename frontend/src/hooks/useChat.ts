"use client";

import { useCallback, useRef, useState } from "react";
import { ChatResponse, sendMessage } from "@/lib/api";

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  agentName?: string | null;
  classification?: string | null;
  timestamp: Date;
  isLoading?: boolean;
}

export function useChat(userId: string = "user_1") {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const [activeAgents, setActiveAgents] = useState<string[]>([]);
  const abortRef = useRef(false);

  const send = useCallback(
    async (text: string) => {
      if (!text.trim() || isLoading) return;
      abortRef.current = false;

      const userMsg: Message = {
        id: `msg_${Date.now()}_user`,
        role: "user",
        content: text,
        timestamp: new Date(),
      };

      const loadingMsg: Message = {
        id: `msg_${Date.now()}_loading`,
        role: "assistant",
        content: "",
        timestamp: new Date(),
        isLoading: true,
      };

      setMessages((prev) => [...prev, userMsg, loadingMsg]);
      setIsLoading(true);
      setActiveAgents(["Classifying..."]);

      try {
        const response: ChatResponse = await sendMessage(
          text,
          sessionId,
          userId
        );

        if (abortRef.current) return;

        const assistantMsg: Message = {
          id: `msg_${Date.now()}_assistant`,
          role: "assistant",
          content: response.message,
          agentName: response.agent_name,
          classification: response.classification,
          timestamp: new Date(),
        };

        setMessages((prev) =>
          prev.filter((m) => !m.isLoading).concat(assistantMsg)
        );
      } catch (error) {
        const errorMsg: Message = {
          id: `msg_${Date.now()}_error`,
          role: "assistant",
          content:
            "Connection failed. Please check that the backend is running.",
          timestamp: new Date(),
        };
        setMessages((prev) =>
          prev.filter((m) => !m.isLoading).concat(errorMsg)
        );
      } finally {
        setIsLoading(false);
        setActiveAgents([]);
      }
    },
    [isLoading, sessionId, userId]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return {
    messages,
    isLoading,
    sessionId,
    activeAgents,
    send,
    clearMessages,
  };
}
