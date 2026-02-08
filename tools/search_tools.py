"""
Web Search Tools for Market Research
Uses DuckDuckGo for free, real-time web search capabilities.
"""

import logging
from typing import List, Dict, Any
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)


def web_search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search the web for general information.

    Args:
        query: The search query
        max_results: Maximum number of results to return

    Returns:
        List of search results with title, link, and snippet
    """
    logger.info(f"Web search: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))

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
        logger.error(f"Web search failed: {e}")
        return [{"error": str(e), "source": "web_search"}]


def news_search(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Search for recent news articles.

    Args:
        query: The search query
        max_results: Maximum number of results to return

    Returns:
        List of news articles with title, link, snippet, and date
    """
    logger.info(f"News search: {query}")
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))

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
        logger.error(f"News search failed: {e}")
        return [{"error": str(e), "source": "news_search"}]


def company_search(company_name: str) -> List[Dict[str, Any]]:
    """
    Search for company-specific information including financials, news, and overview.

    Args:
        company_name: Name of the company to research

    Returns:
        Combined results from multiple searches about the company
    """
    logger.info(f"Company search: {company_name}")

    results = []

    # Search for company overview
    overview_results = web_search(f"{company_name} company overview profile", max_results=5)
    for r in overview_results:
        r["category"] = "overview"
    results.extend(overview_results)

    # Search for recent news
    news_results = news_search(f"{company_name} company", max_results=5)
    for r in news_results:
        r["category"] = "news"
    results.extend(news_results)

    # Search for financial/market info
    financial_results = web_search(f"{company_name} market share revenue financials", max_results=5)
    for r in financial_results:
        r["category"] = "financial"
    results.extend(financial_results)

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

    query = f"{industry} {topic} 2024 2025"
    results = web_search(query, max_results=10)

    # Also get recent news
    news_results = news_search(f"{industry} market", max_results=5)

    for r in results:
        r["category"] = "market_data"
    for r in news_results:
        r["category"] = "market_news"

    all_results = results + news_results
    logger.info(f"Found {len(all_results)} market results")
    return all_results
