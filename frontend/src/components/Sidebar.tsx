"use client";

interface SidebarProps {
  sessionId: string;
  onNewChat: () => void;
}

export default function Sidebar({ sessionId, onNewChat }: SidebarProps) {
  return (
    <div
      className="w-[280px] flex-shrink-0 flex flex-col h-full"
      style={{
        background: "var(--bg-secondary)",
        borderRight: "1px solid var(--border-subtle)",
      }}
    >
      {/* Header */}
      <div className="px-5 pt-6 pb-4">
        <div className="flex items-center gap-3 mb-6">
          <div
            className="w-9 h-9 rounded-lg flex items-center justify-center"
            style={{
              background: "var(--accent-gold-glow)",
              border: "1px solid var(--accent-gold-dim)",
            }}
          >
            <span className="text-base">👑</span>
          </div>
          <div>
            <div
              className="text-sm font-semibold"
              style={{ color: "var(--text-primary)" }}
            >
              Corporate AI
            </div>
            <div
              className="text-[10px] tracking-widest uppercase"
              style={{
                color: "var(--accent-gold-dim)",
                fontFamily: "var(--font-mono)",
              }}
            >
              Command Center
            </div>
          </div>
        </div>

        {/* New Chat button */}
        <button
          onClick={onNewChat}
          className="w-full flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm transition-all duration-200 hover:scale-[1.01] active:scale-[0.99]"
          style={{
            background: "var(--bg-tertiary)",
            color: "var(--text-secondary)",
            border: "1px solid var(--border-subtle)",
            fontFamily: "var(--font-body)",
          }}
        >
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
          >
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          New Conversation
        </button>
      </div>

      {/* Sessions list */}
      <div className="flex-1 overflow-y-auto px-3">
        <div
          className="text-[10px] tracking-[0.15em] uppercase px-2 mb-2"
          style={{
            color: "var(--text-muted)",
            fontFamily: "var(--font-mono)",
          }}
        >
          Sessions
        </div>

        <div
          className="flex items-center gap-3 px-3 py-2.5 rounded-lg"
          style={{
            background: "var(--bg-tertiary)",
            border: "1px solid var(--border-subtle)",
          }}
        >
          <div
            className="w-2 h-2 rounded-full flex-shrink-0"
            style={{ background: "var(--accent-green)" }}
          />
          <div className="min-w-0">
            <div
              className="text-xs truncate"
              style={{ color: "var(--text-primary)" }}
            >
              Current Session
            </div>
            <div
              className="text-[10px] truncate"
              style={{
                color: "var(--text-muted)",
                fontFamily: "var(--font-mono)",
              }}
            >
              {sessionId.slice(0, 20)}...
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <div
        className="px-5 py-4"
        style={{ borderTop: "1px solid var(--border-subtle)" }}
      >
        <div className="flex items-center gap-2">
          <div
            className="w-2 h-2 rounded-full"
            style={{ background: "var(--accent-green)" }}
          />
          <span
            className="text-[10px] tracking-widest uppercase"
            style={{
              color: "var(--text-muted)",
              fontFamily: "var(--font-mono)",
            }}
          >
            System Online · 6 Agents Ready
          </span>
        </div>
      </div>
    </div>
  );
}
