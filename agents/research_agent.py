"""
Research Agent
Responsible for gathering data via web search.
Uses LangGraph's create_react_agent for autonomous tool selection.
"""

import logging
from typing import Dict, Any, List

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from tools.search_tools import web_search, news_search, company_search, market_search

logger = logging.getLogger(__name__)


# =============================================================================
# TOOLS - Defined using @tool decorator for LangGraph
# =============================================================================

@tool
def search_web(query: str) -> str:
    """
    Search the web for general information. Use for market data, industry info, and general research.

    Args:
        query: The search query string
    """
    results = web_search(query, max_results=10)
    return str(results)


@tool
def search_news(query: str) -> str:
    """
    Search for recent news articles. Use for current events, announcements, and recent developments.

    Args:
        query: The search query string
    """
    results = news_search(query, max_results=10)
    return str(results)


@tool
def search_company(company_name: str) -> str:
    """
    Search for comprehensive company information including overview, news, and financials.

    Args:
        company_name: Name of the company to research
    """
    results = company_search(company_name)
    return str(results)


@tool
def search_market(query: str) -> str:
    """
    Search for market and industry data including market size, trends, and forecasts.

    Args:
        query: The market or industry to search for (e.g., 'organic food market size')
    """
    # Parse query - can include topic after |
    if "|" in query:
        parts = query.split("|")
        industry = parts[0].strip()
        topic = parts[1].strip() if len(parts) > 1 else "market size trends"
    else:
        industry = query
        topic = "market size trends"

    results = market_search(industry, topic)
    return str(results)


def get_research_tools() -> List:
    """Get the list of tools for the research agent."""
    return [search_web, search_news, search_company, search_market]


def create_research_agent(llm):
    """
    Create a research agent using LangGraph's create_react_agent.

    Args:
        llm: The language model to use

    Returns:
        Compiled LangGraph agent
    """
    tools = get_research_tools()

    system_prompt = """You are an expert research analyst specializing in gathering market intelligence.

Your role is to search for relevant, current information and find concrete data points: market size, growth rates, key players, trends.

IMPORTANT: You MUST make only 2-3 total tool calls, then immediately provide your final answer. Do NOT make more than 3 tool calls under any circumstances. Pick the 2-3 most impactful searches and combine results."""

    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent


def run_research_agent(llm, query: str, research_type: str, company: str = None,
                       competitors: List[str] = None, industry: str = None,
                       callbacks=None) -> Dict[str, Any]:
    """
    Run the research agent to gather data.

    Args:
        llm: Language model instance
        query: Research query
        research_type: Type of research (market_overview, competitor_analysis, etc.)
        company: Optional company name
        competitors: Optional list of competitors
        industry: Optional industry name

    Returns:
        Dictionary containing all gathered search results
    """
    logger.info(f"Running research agent for: {query} ({research_type})")

    agent = create_research_agent(llm)

    # Build the research prompt based on type
    if research_type == "market_overview":
        prompt = f"""Conduct market research on: {query}
Industry: {industry or 'General'}

Make exactly 2 tool calls: one search_market and one search_web. Then give your final answer."""

    elif research_type == "competitor_analysis":
        competitor_list = ", ".join(competitors) if competitors else "major competitors"
        prompt = f"""Conduct competitor analysis for: {company or query}
Competitors to analyze: {competitor_list}
Industry: {industry or 'General'}

Make exactly 2 tool calls: one search_company and one search_web. Then give your final answer."""

    elif research_type == "trend_analysis":
        prompt = f"""Analyze emerging trends in: {industry or query}

Make exactly 2 tool calls: one search_market and one search_news. Then give your final answer."""

    else:  # full_report
        prompt = f"""Conduct market research for a full report on: {query}
Company: {company or 'N/A'}
Industry: {industry or 'General'}
Competitors: {', '.join(competitors) if competitors else 'To be identified'}

Make exactly 3 tool calls: search_market, search_company, and search_web. Then give your final answer."""

    try:
        # Run the agent
        invoke_config = {"recursion_limit": 12}
        if callbacks:
            invoke_config["callbacks"] = callbacks
        result = agent.invoke(
            {"messages": [HumanMessage(content=prompt)]},
            invoke_config,
        )

        # Extract search results from the messages
        all_results = []
        tool_calls = 0

        for message in result.get("messages", []):
            # Check for tool messages (results from tool calls)
            if hasattr(message, 'content') and message.type == "tool":
                try:
                    # Try JSON first (tool results use true/false/null),
                    # fall back to ast.literal_eval for Python literals
                    import json as _json
                    parsed = _json.loads(message.content)
                    if isinstance(parsed, list):
                        all_results.extend(parsed)
                    else:
                        all_results.append(parsed)
                    tool_calls += 1
                except (ValueError, TypeError):
                    try:
                        import ast
                        parsed = ast.literal_eval(message.content)
                        if isinstance(parsed, list):
                            all_results.extend(parsed)
                        else:
                            all_results.append(parsed)
                        tool_calls += 1
                    except (ValueError, SyntaxError):
                        # Store raw content so results aren't silently dropped
                        all_results.append({"raw": message.content})
                        tool_calls += 1

        # Get the final agent response
        final_message = result["messages"][-1] if result.get("messages") else None
        agent_output = final_message.content if final_message else ""

        return {
            "query": query,
            "research_type": research_type,
            "search_results": all_results,
            "agent_output": agent_output,
            "num_searches": tool_calls
        }

    except Exception as e:
        logger.error(f"Research agent failed: {e}")
        return {
            "query": query,
            "research_type": research_type,
            "error": str(e),
            "search_results": []
        }
