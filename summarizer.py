"""
summarizer.py — Search result summarization.

Takes raw search results and uses the LLM to synthesize them
into a clear, personality-matched answer. This is the bridge
between "here are 5 web results" and "here's what you need to know."
"""

import logging

from personality.prompts import build_system_prompt
import config

logger = logging.getLogger("buddy.tools.summarizer")


class Summarizer:
    """
    Converts raw search results into natural language answers.
    Uses the LLM to synthesize information from multiple sources.
    """

    def summarize(
        self,
        query: str,
        results: list,
        brain,
        mood: str = "funny",
    ) -> str:
        """
        Summarize search results into a coherent answer.

        Args:
            query: The original search query.
            results: List of SearchResult objects.
            brain: The Brain instance to use for summarization.
            mood: Current mood mode.

        Returns:
            A synthesized, personality-flavored answer.
        """
        if not results:
            return "I searched everywhere and found absolutely nothing. The void stares back."

        # Format results for the LLM
        results_text = self._format_for_llm(results)

        # Build a summarization prompt
        system_prompt = build_system_prompt(
            mood=mood,
            buddy_name=config.BUDDY_NAME,
            user_name=config.USER_NAME,
        )

        summarize_instruction = f"""The user asked: "{query}"

I searched the web and found these results. Synthesize them into a clear,
helpful answer. Don't just list the results — combine the information into
a natural response. Include the most relevant facts and details.

If the results don't fully answer the question, say so honestly.
Mention sources briefly if relevant (e.g., "According to X...").

SEARCH RESULTS:
{results_text}

Now give a clear, synthesized answer to: "{query}"
"""

        messages = [{"role": "user", "content": summarize_instruction}]

        try:
            response = brain.think(system_prompt, messages)
            return response
        except Exception as e:
            logger.error(f"Summarization error: {e}")
            # Fallback: just format the raw results
            return self._fallback_format(query, results)

    def _format_for_llm(self, results: list) -> str:
        """Format search results into a string for the LLM."""
        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"Result {i}: {r.title}")
            lines.append(f"  Source: {r.url}")
            lines.append(f"  Content: {r.snippet}")
            lines.append("")
        return "\n".join(lines)

    def _fallback_format(self, query: str, results: list) -> str:
        """Simple fallback when LLM summarization fails."""
        lines = [f"Here's what I found for '{query}':\n"]
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. **{r.title}**")
            lines.append(f"   {r.snippet}")
            lines.append(f"   🔗 {r.url}")
            lines.append("")
        return "\n".join(lines)
