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

Your role is to:
1. Search for relevant, current information using the available tools
2. Gather comprehensive data from multiple sources
3. Focus on finding concrete data points: market size, growth rates, key players, trends
4. Use multiple searches to build a complete picture

For market research:
- Search for market size and growth data using search_market
- Search for key industry trends using search_web
- Search for major players and competitors using search_company
- Search for recent news and developments using search_news

For competitor analysis:
- Search for each competitor individually using search_company
- Look for market share data using search_web
- Find recent news about competitors using search_news

Be focused and efficient. Perform 2-3 targeted searches to gather the most important data."""

    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent


def run_research_agent(llm, query: str, research_type: str, company: str = None,
                       competitors: List[str] = None, industry: str = None) -> Dict[str, Any]:
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
        prompt = f"""Conduct comprehensive market research on: {query}
Industry: {industry or 'General'}

Please gather data by:
1. Use search_market to find market size and growth data
2. Use search_news to find recent market developments
3. Use search_web to find industry trends and key players
Keep it to 2-3 key searches for the most relevant data."""

    elif research_type == "competitor_analysis":
        competitor_list = ", ".join(competitors) if competitors else "major competitors"
        prompt = f"""Conduct competitor analysis for: {company or query}
Competitors to analyze: {competitor_list}
Industry: {industry or 'General'}

Please gather data by:
1. Use search_company for {company or 'the main company'}
2. Use search_company for each major competitor
3. Use search_web to find market share data
4. Use search_news for recent competitive news

Focus on 2-3 searches for the most important competitive data."""

    elif research_type == "trend_analysis":
        prompt = f"""Analyze emerging trends in: {industry or query}

Please gather data by:
1. Use search_market to find current industry trends
2. Use search_web to find technology and innovation trends
3. Use search_news for recent industry changes
4. Use search_web to find future predictions and forecasts

Perform 2-3 focused searches to identify the key trends."""

    else:  # full_report
        prompt = f"""Conduct comprehensive market research for a full report on: {query}
Company: {company or 'N/A'}
Industry: {industry or 'General'}
Competitors: {', '.join(competitors) if competitors else 'To be identified'}

Gather data for:
1. Market overview - size, growth, segments (use search_market)
2. Competitive landscape - key players (use search_company)
3. Industry trends - current and emerging (use search_web)
4. Recent developments and news (use search_news)

This is for a comprehensive report. Perform 3-4 focused searches covering the key areas."""

    try:
        # Run the agent
        result = agent.invoke(
            {"messages": [HumanMessage(content=prompt)]},
            {"recursion_limit": 10},
        )

        # Extract search results from the messages
        all_results = []
        tool_calls = 0

        for message in result.get("messages", []):
            # Check for tool messages (results from tool calls)
            if hasattr(message, 'content') and message.type == "tool":
                try:
                    # Try to parse the tool result
                    import ast
                    parsed = ast.literal_eval(message.content)
                    if isinstance(parsed, list):
                        all_results.extend(parsed)
                    else:
                        all_results.append(parsed)
                    tool_calls += 1
                except:
                    pass

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
