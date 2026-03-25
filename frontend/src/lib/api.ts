const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatResponse {
  message: string;
  session_id: string;
  classification: string | null;
  agent_name: string | null;
}

export interface ConversationMessage {
  role: "user" | "assistant";
  content: string;
  agent_name: string | null;
  created_at: string;
}

export async function sendMessage(
  message: string,
  sessionId: string,
  userId: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId, user_id: userId }),
  });
  if (!res.ok) throw new Error(`Chat failed: ${res.status}`);
  return res.json();
}

export async function getConversations(
  userId: string
): Promise<{ user_id: string; sessions: string[] }> {
  const res = await fetch(`${API_BASE}/api/conversations/${userId}`);
  if (!res.ok) throw new Error(`Failed to fetch conversations: ${res.status}`);
  return res.json();
}

export async function getConversationHistory(
  userId: string,
  sessionId: string
): Promise<{ session_id: string; messages: ConversationMessage[] }> {
  const res = await fetch(
    `${API_BASE}/api/conversations/${userId}/${sessionId}`
  );
  if (!res.ok) throw new Error(`Failed to fetch history: ${res.status}`);
  return res.json();
}

export async function classifyMessage(
  message: string
): Promise<{ label: string; confidence: number }> {
  const res = await fetch(`${API_BASE}/api/classify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error(`Classification failed: ${res.status}`);
  return res.json();
}
