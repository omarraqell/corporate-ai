"""
Web fetch tool for agents.

Fetches a URL and extracts readable text from HTML.
Interface designed for future Playwright swap.
"""

import html as html_module
import logging
import re

import httpx

logger = logging.getLogger(__name__)

MAX_CONTENT_LENGTH = 5000


async def web_fetch(url: str) -> str:
    """Fetch a URL and extract readable plain text."""
    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True,
            headers={"User-Agent": "CorporateAI-Agent/1.0"},
        ) as client:
            response = await client.get(url)
            response.raise_for_status()

        raw_html = response.text

        # Extract title
        title_match = re.search(r"<title[^>]*>(.*?)</title>", raw_html, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Untitled"

        # Remove script and style tags
        text = re.sub(r"<script[^>]*>.*?</script>", "", raw_html, flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)

        # Remove all HTML tags
        text = re.sub(r"<[^>]+>", " ", text)

        # Clean whitespace
        text = re.sub(r"\s+", " ", text).strip()

        # Decode HTML entities
        text = html_module.unescape(text)

        # Truncate
        if len(text) > MAX_CONTENT_LENGTH:
            text = text[:MAX_CONTENT_LENGTH] + "\n... (content truncated)"

        return f"Title: {title}\nURL: {url}\n\n{text}"

    except Exception as e:
        logger.error(f"Web fetch failed for {url}: {e}")
        return f"Failed to fetch {url}: {str(e)}"


WEB_FETCH_SCHEMA = {
    "type": "object",
    "properties": {
        "url": {
            "type": "string",
            "description": "The URL to fetch and extract text from",
        },
    },
    "required": ["url"],
}
