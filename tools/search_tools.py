"""
Web Search Tools for Market Research
Uses DuckDuckGo for free, real-time web search capabilities.
"""

import logging
import time
from typing import List, Dict, Any
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

# DuckDuckGo request timeout (seconds) and rate-limiting
_DDG_TIMEOUT = 10
_SEARCH_DELAY = 1.5  # seconds between DDG requests
_last_search_time = 0.0


def _rate_limit():
    """Enforce a minimum delay between DuckDuckGo requests."""
    global _last_search_time
    elapsed = time.time() - _last_search_time
    if elapsed < _SEARCH_DELAY:
        time.sleep(_SEARCH_DELAY - elapsed)
    _last_search_time = time.time()


def web_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search the web for general information.

    Args:
        query: The search query
        max_results: Maximum number of results to return

    Returns:
        List of search results with title, link, and snippet
    """
    logger.info(f"Web search: {query}")
    for attempt in range(2):
        try:
            _rate_limit()
            with DDGS(timeout=_DDG_TIMEOUT) as ddgs:
                results = list(ddgs.text(query, max_results=max_results))

            if not results and attempt < 1:
                logger.warning(f"Web search returned 0 results, retrying...")
                time.sleep(2)
                continue

            formatted_results = []
            for r in results:
                formatted_results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "snippet": r.get("body", ""),
                    "source": "web_search"
                })

            logger.info(f"Found {len(formatted_results)} web results")
            return formatted_results
        except Exception as e:
            logger.error(f"Web search failed (attempt {attempt + 1}): {e}")
            if attempt < 1:
                time.sleep(2)
                continue
            return [{"error": str(e), "source": "web_search"}]

    return [{"error": "Search returned no results after retries", "source": "web_search"}]


def news_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for recent news articles.

    Args:
        query: The search query
        max_results: Maximum number of results to return

    Returns:
        List of news articles with title, link, snippet, and date
    """
    logger.info(f"News search: {query}")
    for attempt in range(2):
        try:
            _rate_limit()
            with DDGS(timeout=_DDG_TIMEOUT) as ddgs:
                results = list(ddgs.news(query, max_results=max_results))

            if not results and attempt < 1:
                logger.warning(f"News search returned 0 results, retrying...")
                time.sleep(2)
                continue

            formatted_results = []
            for r in results:
                formatted_results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("body", ""),
                    "date": r.get("date", ""),
                    "source": r.get("source", ""),
                    "type": "news"
                })

            logger.info(f"Found {len(formatted_results)} news results")
            return formatted_results
        except Exception as e:
            logger.error(f"News search failed (attempt {attempt + 1}): {e}")
            if attempt < 1:
                time.sleep(2)
                continue
            return [{"error": str(e), "source": "news_search"}]

    return [{"error": "News search returned no results after retries", "source": "news_search"}]


def company_search(company_name: str) -> List[Dict[str, Any]]:
    """
    Search for company-specific information including overview and recent news.

    Args:
        company_name: Name of the company to research

    Returns:
        Combined results from searches about the company
    """
    logger.info(f"Company search: {company_name}")

    # Single broad search to minimize DDG calls
    results = web_search(
        f"{company_name} company overview market share revenue 2024 2025",
        max_results=5,
    )
    for r in results:
        r["category"] = "overview"

    logger.info(f"Found {len(results)} total results for {company_name}")
    return results


def market_search(industry: str, topic: str = "market size trends") -> List[Dict[str, Any]]:
    """
    Search for market and industry information.

    Args:
        industry: The industry or market to research
        topic: Specific topic to search for (e.g., "market size", "trends", "forecast")

    Returns:
        List of search results about the market/industry
    """
    logger.info(f"Market search: {industry} - {topic}")

    # Single broad search to minimize DDG calls
    query = f"{industry} {topic} 2024 2025"
    results = web_search(query, max_results=5)

    for r in results:
        r["category"] = "market_data"

    logger.info(f"Found {len(results)} market results")
    return results
