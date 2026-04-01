"""
Receptionist: LLM-based message classifier using GPT-4o-mini.

Classifies incoming user messages into route labels that determine
which sub-agent(s) should handle the request.

Hybrid approach: starts with LLM classification, logs every result
to build training data for a future BERT fine-tune.
"""

import json
import logging

from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)

ROUTE_LABELS = [
    "task_management",
    "research_query",
    "data_analysis",
    "writing_request",
    "code_request",
    "general_inquiry",
    "multi_agent",
    "escalation",
    "agent_management",
]

LABEL_DESCRIPTIONS = {
    "task_management": "Task tracking, deadlines, assignments, project status, sprints, priorities",
    "research_query": "Research, investigation, market analysis, competitor analysis, best practices",
    "data_analysis": "Data analysis, metrics, charts, KPIs, dashboards, statistics, SQL queries",
    "writing_request": "Writing reports, emails, summaries, proposals, documentation, blog posts",
    "code_request": "Writing code, debugging, deployment, APIs, scripts, automation, infrastructure",
    "general_inquiry": "Company policy questions, general info, procedures, HR questions",
    "multi_agent": "Complex requests requiring multiple capabilities (research + writing, data + code, etc.)",
    "escalation": "Urgent requests, emergencies, critical issues, system outages, immediate action needed",
    "agent_management": "Creating, listing, managing, or deleting custom AI agents",
}

SYSTEM_PROMPT = f"""You are a message classifier for a corporate AI system. Your job is to classify incoming user messages into exactly one route label.

Available labels and their descriptions:
{json.dumps(LABEL_DESCRIPTIONS, indent=2)}

Rules:
- Return ONLY valid JSON with "label" and "confidence" fields.
- "label" must be exactly one of: {", ".join(ROUTE_LABELS)}
- "confidence" is a float between 0.0 and 1.0 indicating your certainty.
- If the message clearly spans multiple domains (e.g., "research X and write a report"), use "multi_agent".
- If the message contains urgency signals (urgent, ASAP, critical, down, broken), use "escalation" regardless of the actual topic.
- For ambiguous messages, prefer "general_inquiry" with lower confidence.
- Do NOT include any explanation, only the JSON object."""

CLASSIFY_TEMPLATE = """Classify this user message:

"{message}"

Return JSON only:"""


class ReceptionistService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "gpt-4o-mini"

    async def classify(self, message: str) -> dict:
        """
        Classify a user message into a route label.

        Returns:
            {
                "label": str,        # one of ROUTE_LABELS
                "confidence": float,  # 0.0 to 1.0
            }
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": CLASSIFY_TEMPLATE.format(message=message)},
                ],
                temperature=0.0,
                max_tokens=100,
                response_format={"type": "json_object"},
            )

            raw = response.choices[0].message.content
            result = json.loads(raw)

            # Validate label
            label = result.get("label", "general_inquiry")
            if label not in ROUTE_LABELS:
                logger.warning(f"Invalid label from LLM: {label}. Falling back to general_inquiry.")
                label = "general_inquiry"

            confidence = float(result.get("confidence", 0.5))
            confidence = max(0.0, min(1.0, confidence))

            return {
                "label": label,
                "confidence": confidence,
            }

        except Exception as e:
            logger.error(f"Classification failed: {e}. Falling back to general_inquiry.")
            return {
                "label": "general_inquiry",
                "confidence": 0.0,
            }
