"""
Web Search Tools for Market Research
Uses Tavily for reliable, AI-optimized web search.
"""

import logging
import os
from typing import List, Dict, Any

from tavily import TavilyClient

logger = logging.getLogger(__name__)

_client = None


def _get_client() -> TavilyClient:
    """Lazily initialize the Tavily client."""
    global _client
    if _client is None:
        api_key = os.environ.get("TAVILY_API_KEY")
        if not api_key:
            raise RuntimeError("TAVILY_API_KEY is not set in environment")
        _client = TavilyClient(api_key=api_key)
    return _client


def web_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search the web for general information.

    Args:
        query: The search query
        max_results: Maximum number of results to return

    Returns:
        List of search results with title, url, and snippet
    """
    logger.info(f"Web search: {query}")
    try:
        response = _get_client().search(
            query=query,
            max_results=max_results,
            search_depth="basic",
        )
        formatted_results = []
        for r in response.get("results", []):
            formatted_results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content", ""),
                "source": "web_search",
            })
        logger.info(f"Found {len(formatted_results)} web results")
        return formatted_results
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return [{"error": str(e), "source": "web_search"}]


def news_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for recent news articles.

    Args:
        query: The search query
        max_results: Maximum number of results to return

    Returns:
        List of news results with title, url, snippet, and date
    """
    logger.info(f"News search: {query}")
    try:
        response = _get_client().search(
            query=query,
            max_results=max_results,
            search_depth="basic",
            topic="news",
        )
        formatted_results = []
        for r in response.get("results", []):
            formatted_results.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("content", ""),
                "date": r.get("published_date", ""),
                "source": "news_search",
                "type": "news",
            })
        logger.info(f"Found {len(formatted_results)} news results")
        return formatted_results
    except Exception as e:
        logger.error(f"News search failed: {e}")
        return [{"error": str(e), "source": "news_search"}]


def company_search(company_name: str) -> List[Dict[str, Any]]:
    """
    Search for company-specific information including overview and market data.

    Args:
        company_name: Name of the company to research

    Returns:
        List of search results about the company
    """
    logger.info(f"Company search: {company_name}")
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
        topic: Specific topic to search for

    Returns:
        List of search results about the market/industry
    """
    logger.info(f"Market search: {industry} - {topic}")
    query = f"{industry} {topic} 2024 2025"
    results = web_search(query, max_results=5)
    for r in results:
        r["category"] = "market_data"
    logger.info(f"Found {len(results)} market results")
    return results
