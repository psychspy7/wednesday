"""
search.py — Real-time web search tool.

Search strategy:
  1. Try DuckDuckGo first (free, no API key needed)
  2. Fall back to SerpAPI if configured
  3. Return structured results that the summarizer can process

This module handles the raw searching. The summarizer (summarizer.py)
handles turning results into human-readable answers.
"""

import logging
from typing import Optional

import config

logger = logging.getLogger("buddy.tools.search")


class SearchResult:
    """A single search result."""

    def __init__(self, title: str, url: str, snippet: str):
        self.title = title
        self.url = url
        self.snippet = snippet

    def __repr__(self):
        return f"SearchResult(title='{self.title[:40]}...')"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
        }


class WebSearchTool:
    """
    Web search with automatic fallback.

    Priority: DuckDuckGo → SerpAPI → Error message
    """

    def __init__(self):
        self.serpapi_key = config.SERPAPI_KEY
        logger.info(
            f"WebSearchTool initialized | "
            f"SerpAPI: {'configured' if self.serpapi_key else 'not configured'}"
        )

    def search(self, query: str, max_results: int = 5) -> list[SearchResult]:
        """
        Search the web for a query.

        Args:
            query: The search query.
            max_results: Maximum number of results to return.

        Returns:
            List of SearchResult objects.
        """
        logger.info(f"Searching: '{query}' (max {max_results})")

        # Strategy 1: DuckDuckGo (free, no API key)
        results = self._search_duckduckgo(query, max_results)
        if results:
            logger.info(f"DuckDuckGo returned {len(results)} results")
            return results

        # Strategy 2: SerpAPI (paid, but more reliable)
        if self.serpapi_key:
            results = self._search_serpapi(query, max_results)
            if results:
                logger.info(f"SerpAPI returned {len(results)} results")
                return results

        logger.warning(f"All search strategies failed for: '{query}'")
        return []

    # ── DuckDuckGo ────────────────────────────────────────────────────────

    def _search_duckduckgo(
        self, query: str, max_results: int
    ) -> list[SearchResult]:
        """Search using DuckDuckGo (via duckduckgo-search library)."""
        try:
            from duckduckgo_search import DDGS

            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append(
                        SearchResult(
                            title=r.get("title", ""),
                            url=r.get("href", r.get("link", "")),
                            snippet=r.get("body", r.get("snippet", "")),
                        )
                    )
            return results

        except ImportError:
            logger.warning(
                "duckduckgo-search not installed. "
                "Install with: pip install duckduckgo-search"
            )
            return []
        except Exception as e:
            logger.error(f"DuckDuckGo search error: {e}")
            return []

    # ── SerpAPI ───────────────────────────────────────────────────────────

    def _search_serpapi(
        self, query: str, max_results: int
    ) -> list[SearchResult]:
        """Search using SerpAPI (Google results)."""
        try:
            import requests

            params = {
                "q": query,
                "api_key": self.serpapi_key,
                "num": max_results,
                "engine": "google",
            }

            resp = requests.get(
                "https://serpapi.com/search", params=params, timeout=10
            )
            resp.raise_for_status()
            data = resp.json()

            results = []
            for r in data.get("organic_results", [])[:max_results]:
                results.append(
                    SearchResult(
                        title=r.get("title", ""),
                        url=r.get("link", ""),
                        snippet=r.get("snippet", ""),
                    )
                )
            return results

        except ImportError:
            logger.warning("requests not installed for SerpAPI")
            return []
        except Exception as e:
            logger.error(f"SerpAPI error: {e}")
            return []

    # ── Utility ───────────────────────────────────────────────────────────

    def format_results(self, results: list[SearchResult]) -> str:
        """
        Format search results into a readable string for the LLM.

        Args:
            results: List of SearchResult objects.

        Returns:
            Formatted string with numbered results.
        """
        if not results:
            return "No results found."

        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"[{i}] {r.title}")
            lines.append(f"    URL: {r.url}")
            lines.append(f"    {r.snippet}")
            lines.append("")

        return "\n".join(lines)
