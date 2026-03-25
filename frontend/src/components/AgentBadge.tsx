"use client";

const AGENT_CONFIG: Record<
  string,
  { emoji: string; label: string; color: string }
> = {
  secretary: {
    emoji: "📋",
    label: "Secretary",
    color: "rgba(52, 211, 153, 0.15)",
  },
  research_analyst: {
    emoji: "🔍",
    label: "Research",
    color: "rgba(74, 158, 255, 0.15)",
  },
  data_analyst: {
    emoji: "📊",
    label: "Data",
    color: "rgba(167, 139, 250, 0.15)",
  },
  writer: {
    emoji: "✍️",
    label: "Writer",
    color: "rgba(251, 191, 36, 0.15)",
  },
  code_dev: {
    emoji: "💻",
    label: "Code Dev",
    color: "rgba(248, 113, 113, 0.15)",
  },
  qa_reviewer: {
    emoji: "🔎",
    label: "QA",
    color: "rgba(212, 168, 83, 0.15)",
  },
  ceo_direct: {
    emoji: "👑",
    label: "CEO",
    color: "rgba(212, 168, 83, 0.15)",
  },
};

interface AgentBadgeProps {
  agentName: string;
  classification?: string | null;
}

export default function AgentBadge({
  agentName,
  classification,
}: AgentBadgeProps) {
  const agents = agentName.split(",").map((a) => a.trim());

  return (
    <div className="flex items-center gap-2 flex-wrap">
      {agents.map((agent) => {
        const config = AGENT_CONFIG[agent] || {
          emoji: "🤖",
          label: agent,
          color: "rgba(255,255,255,0.08)",
        };
        return (
          <span
            key={agent}
            className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] tracking-wide uppercase"
            style={{
              background: config.color,
              color: "var(--text-secondary)",
              fontFamily: "var(--font-mono)",
            }}
          >
            <span>{config.emoji}</span>
            {config.label}
          </span>
        );
      })}
      {classification && (
        <span
          className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] tracking-widest uppercase"
          style={{
            background: "var(--border-subtle)",
            color: "var(--text-tertiary)",
            fontFamily: "var(--font-mono)",
          }}
        >
          {classification}
        </span>
      )}
    </div>
  );
}
