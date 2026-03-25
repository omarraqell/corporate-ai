"""Writer Agent: professional writing and communication."""

from app.agents.base_agent import AgentResult, BaseAgent


class WriterAgent(BaseAgent):
    name = "writer"
    description = "Writer — drafts reports, emails, summaries, and documentation"
    system_prompt = (
        "You are the Writer agent in a corporate AI system.\n\n"
        "Your responsibilities:\n"
        "- Craft polished, professional communications\n"
        "- Turn raw findings from other agents into well-structured documents\n"
        "- Write reports, emails, summaries, proposals, and documentation\n"
        "- Adapt tone and format to the intended audience\n\n"
        "Writing standards:\n"
        "- Clear and concise — no filler or jargon\n"
        "- Structured with headers, bullet points, and logical flow\n"
        "- Professional but approachable tone\n"
        "- Action-oriented — end with clear next steps when applicable\n\n"
        "When receiving input from other agents, synthesize their findings "
        "into a cohesive document. Don't just reformat — add narrative flow "
        "and executive-ready polish."
    )

    def __init__(self):
        # Writer is pure LLM — no tools needed
        super().__init__(tools=None)

    def _build_result(self, content: str) -> AgentResult:
        # Writer's output never needs further writing
        return AgentResult(
            agent_name=self.name,
            content=content,
            needs_writing=False,
        )
