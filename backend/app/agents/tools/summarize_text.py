"""
Text summarization tool for agents.

Uses the LLM to summarize long text in various styles.
"""

import logging

from openai import AsyncOpenAI

from app.config import settings

logger = logging.getLogger(__name__)

STYLE_PROMPTS = {
    "brief": "Summarize the following text in 2-3 concise sentences.",
    "detailed": "Summarize the following text in a detailed paragraph, preserving key points.",
    "bullet_points": "Summarize the following text as a bullet-point list of key points.",
}


async def summarize_text(text: str, style: str = "brief") -> str:
    """Summarize text using the LLM."""
    prompt = STYLE_PROMPTS.get(style, STYLE_PROMPTS["brief"])

    try:
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model=settings.llm_model_name,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text[:10000]},
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Summarization failed: {e}")
        return f"Summarization failed: {str(e)}"


SUMMARIZE_TEXT_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string",
            "description": "The text to summarize",
        },
        "style": {
            "type": "string",
            "description": "Summary style: 'brief' (2-3 sentences), 'detailed' (paragraph), or 'bullet_points'",
            "enum": ["brief", "detailed", "bullet_points"],
            "default": "brief",
        },
    },
    "required": ["text"],
}
