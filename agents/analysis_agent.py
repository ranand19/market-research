"""
Analysis Agent
A truly agentic analyzer that autonomously decides which analyses to perform.
Uses LangGraph's create_react_agent for autonomous tool selection.
"""

import json
import logging
from typing import Dict, Any, List

from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


# =============================================================================
# SHARED STATE FOR TOOLS
# =============================================================================

class AnalysisContext:
    """Shared context for analysis tools."""
    raw_data: List[Dict] = []
    context: Dict[str, Any] = {}
    llm = None
    analyses_performed: List[str] = []


_analysis_context = AnalysisContext()


def _format_data_for_analysis(data: List[Dict]) -> str:
    """Format raw data for LLM analysis."""
    if not data:
        return "No data available."

    formatted = []
    for i, item in enumerate(data[:20], 1):
        if isinstance(item, dict) and "error" not in item:
            entry = f"[{i}] {item.get('title', 'Untitled')}"
            if item.get('snippet'):
                entry += f"\n    {item.get('snippet')[:200]}"
            if item.get('url'):
                entry += f"\n    Source: {item.get('url')}"
            formatted.append(entry)

    return "\n\n".join(formatted) if formatted else "No valid data found."


# =============================================================================
# ANALYSIS TOOLS
# =============================================================================

@tool
def analyze_market_size(query: str) -> str:
    """
    Analyze market size and growth data from the research.
    Use this to understand how big the market is and how fast it's growing.

    Args:
        query: The market or topic to analyze
    """
    logger.info(f"Tool: analyze_market_size - {query}")

    formatted_data = _format_data_for_analysis(_analysis_context.raw_data)

    prompt = f"""Analyze the following data to extract market size and growth information for: {query}

DATA:
{formatted_data}

Extract and return a JSON object with:
{{
    "market_size_current": "Current market size estimate with currency",
    "market_size_projected": "Projected market size with timeline",
    "growth_rate_cagr": "Compound annual growth rate if available",
    "growth_drivers": ["List of factors driving growth"],
    "market_maturity": "emerging/growing/mature/declining",
    "confidence": "high/medium/low based on data quality"
}}

Return ONLY valid JSON."""

    response = _analysis_context.llm.invoke([
        SystemMessage(content="You are a market sizing analyst. Extract quantitative market data."),
        HumanMessage(content=prompt)
    ])

    _analysis_context.analyses_performed.append("market_size")
    return response.content


@tool
def analyze_market_segments(query: str) -> str:
    """
    Identify and analyze market segments from the research data.
    Use to understand different categories, customer types, or product segments.

    Args:
        query: The market to segment
    """
    logger.info(f"Tool: analyze_market_segments - {query}")

    formatted_data = _format_data_for_analysis(_analysis_context.raw_data)

    prompt = f"""Analyze the following data to identify market segments for: {query}

DATA:
{formatted_data}

Return a JSON object with:
{{
    "segments": [
        {{
            "name": "Segment name",
            "description": "What this segment includes",
            "size_share": "Percentage or size if available",
            "growth_outlook": "Growing/stable/declining"
        }}
    ],
    "largest_segment": "Which segment is largest",
    "fastest_growing": "Which segment is growing fastest"
}}

Return ONLY valid JSON."""

    response = _analysis_context.llm.invoke([
        SystemMessage(content="You are a market segmentation analyst."),
        HumanMessage(content=prompt)
    ])

    _analysis_context.analyses_performed.append("market_segments")
    return response.content


@tool
def analyze_competitive_landscape(query: str) -> str:
    """
    Analyze the competitive landscape including key players and their positions.
    Use for understanding who the players are and how they compete.

    Args:
        query: The market or industry to analyze
    """
    logger.info(f"Tool: analyze_competitive_landscape - {query}")

    formatted_data = _format_data_for_analysis(_analysis_context.raw_data)
    competitors = _analysis_context.context.get('competitors', [])
    company = _analysis_context.context.get('company', '')

    prompt = f"""Analyze the competitive landscape for: {query}
Company of interest: {company or 'Not specified'}
Known competitors: {', '.join(competitors) if competitors else 'To be identified from data'}

DATA:
{formatted_data}

Return a JSON object with:
{{
    "market_leaders": [
        {{
            "company": "Company name",
            "market_share": "Percentage if available",
            "position": "Leader/Challenger/Follower/Niche",
            "key_strengths": ["Top 2-3 strengths"]
        }}
    ],
    "competitive_intensity": "high/medium/low",
    "barriers_to_entry": ["Key barriers"]
}}

Return ONLY valid JSON."""

    response = _analysis_context.llm.invoke([
        SystemMessage(content="You are a competitive intelligence analyst."),
        HumanMessage(content=prompt)
    ])

    _analysis_context.analyses_performed.append("competitive_landscape")
    return response.content


@tool
def perform_swot_analysis(query: str) -> str:
    """
    Generate a SWOT analysis (Strengths, Weaknesses, Opportunities, Threats).
    Use when you need a strategic assessment.

    Args:
        query: The company or topic for SWOT
    """
    logger.info(f"Tool: perform_swot_analysis - {query}")

    formatted_data = _format_data_for_analysis(_analysis_context.raw_data)
    company = _analysis_context.context.get('company', query)

    prompt = f"""Perform a SWOT analysis for: {company}

Based on this data:
{formatted_data}

Return a JSON object with:
{{
    "strengths": ["List of strengths"],
    "weaknesses": ["List of weaknesses"],
    "opportunities": ["List of opportunities"],
    "threats": ["List of threats"],
    "strategic_implications": "Key takeaway from this SWOT"
}}

Return ONLY valid JSON."""

    response = _analysis_context.llm.invoke([
        SystemMessage(content="You are a strategic analyst."),
        HumanMessage(content=prompt)
    ])

    _analysis_context.analyses_performed.append("swot")
    return response.content


@tool
def identify_trends(query: str) -> str:
    """
    Identify emerging trends and patterns from the research data.
    Use for forward-looking analysis.

    Args:
        query: The industry or topic to analyze trends for
    """
    logger.info(f"Tool: identify_trends - {query}")

    formatted_data = _format_data_for_analysis(_analysis_context.raw_data)

    prompt = f"""Identify emerging trends for: {query}

DATA:
{formatted_data}

Return a JSON object with:
{{
    "trends": [
        {{
            "trend": "Trend name/description",
            "category": "Technology/Consumer/Regulatory/Economic",
            "impact_level": "High/Medium/Low",
            "timeline": "When this will peak/mature"
        }}
    ],
    "mega_trends": ["Overarching trends shaping the industry"],
    "disruption_risks": ["Trends that could disrupt the market"]
}}

Return ONLY valid JSON."""

    response = _analysis_context.llm.invoke([
        SystemMessage(content="You are a trend analyst."),
        HumanMessage(content=prompt)
    ])

    _analysis_context.analyses_performed.append("trends")
    return response.content


@tool
def extract_key_statistics(query: str) -> str:
    """
    Extract key statistics and data points from the research.
    Use when you need concrete figures.

    Args:
        query: What statistics to look for
    """
    logger.info(f"Tool: extract_key_statistics - {query}")

    formatted_data = _format_data_for_analysis(_analysis_context.raw_data)

    prompt = f"""Extract key statistics and data points about: {query}

DATA:
{formatted_data}

Return a JSON object with:
{{
    "statistics": [
        {{
            "metric": "What is being measured",
            "value": "The number/percentage",
            "context": "What this means"
        }}
    ],
    "data_quality": "Assessment of data reliability",
    "data_gaps": ["Important metrics that were not found"]
}}

Return ONLY valid JSON."""

    response = _analysis_context.llm.invoke([
        SystemMessage(content="You are a data analyst."),
        HumanMessage(content=prompt)
    ])

    _analysis_context.analyses_performed.append("statistics")
    return response.content


def get_analysis_tools() -> List:
    """Get the list of analysis tools."""
    return [
        analyze_market_size,
        analyze_market_segments,
        analyze_competitive_landscape,
        perform_swot_analysis,
        identify_trends,
        extract_key_statistics
    ]


def create_analysis_agent(llm):
    """Create the analysis agent using LangGraph."""
    tools = get_analysis_tools()

    system_prompt = """You are an expert market analyst. Your job is to analyze research data and produce comprehensive insights.

You have access to several analysis tools. Based on the research type and data available, decide which analyses to perform:

- For MARKET OVERVIEW: Use analyze_market_size, analyze_market_segments, identify_trends, extract_key_statistics
- For COMPETITOR ANALYSIS: Use analyze_competitive_landscape, perform_swot_analysis, extract_key_statistics
- For TREND ANALYSIS: Use identify_trends, analyze_market_segments, extract_key_statistics
- For FULL REPORT: Use ALL available tools to build a comprehensive picture

Run 2-3 of the most relevant analyses. Actually USE the tools."""

    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent


def run_analysis_agent(llm, research_data: Dict[str, Any], research_type: str,
                       company: str = None, competitors: List[str] = None,
                       industry: str = None) -> Dict[str, Any]:
    """
    Run the analysis agent to autonomously analyze gathered research data.
    """
    logger.info(f"Running analysis agent for: {research_type}")

    search_results = research_data.get("search_results", [])
    query = research_data.get("query", "")

    if not search_results:
        logger.warning("No search results to analyze")
        return {"error": "No data to analyze", "research_type": research_type}

    # Set up shared context for tools
    _analysis_context.raw_data = search_results
    _analysis_context.context = {
        "company": company or "",
        "competitors": competitors or [],
        "industry": industry or "",
        "query": query
    }
    _analysis_context.llm = llm
    _analysis_context.analyses_performed = []

    # Create and run the agent
    agent = create_analysis_agent(llm)

    # Build the analysis prompt
    if research_type == "market_overview":
        prompt = f"""Analyze the research data for a MARKET OVERVIEW of: {query}
Industry: {industry or 'General'}

Perform comprehensive market analysis:
1. Use analyze_market_size to understand market size and growth
2. Use analyze_market_segments to identify key segments
3. Use identify_trends to find emerging trends
4. Use extract_key_statistics for important data points"""

    elif research_type == "competitor_analysis":
        prompt = f"""Analyze the research data for COMPETITOR ANALYSIS of: {company or query}
Competitors: {', '.join(competitors) if competitors else 'Identify from data'}

Perform comprehensive competitive analysis:
1. Use analyze_competitive_landscape to map competitors
2. Use perform_swot_analysis for strategic assessment
3. Use extract_key_statistics for market shares"""

    elif research_type == "trend_analysis":
        prompt = f"""Analyze the research data for TREND ANALYSIS in: {industry or query}

Perform comprehensive trend analysis:
1. Use identify_trends to find emerging trends
2. Use analyze_market_segments for segment trends
3. Use extract_key_statistics for supporting data"""

    else:  # full_report
        prompt = f"""Analyze the research data for a FULL COMPREHENSIVE REPORT on: {query}
Company: {company or 'N/A'}
Industry: {industry or 'General'}

Use ALL available analysis tools:
1. analyze_market_size
2. analyze_market_segments
3. analyze_competitive_landscape
4. perform_swot_analysis
5. identify_trends
6. extract_key_statistics

Focus on the 3-4 most important tools for a comprehensive picture."""

    try:
        result = agent.invoke(
            {"messages": [HumanMessage(content=prompt)]},
            {"recursion_limit": 10},
        )

        # Extract analyses from tool messages
        analyses = {}
        for message in result.get("messages", []):
            if hasattr(message, 'type') and message.type == "tool":
                tool_name = getattr(message, 'name', 'unknown')
                try:
                    content = message.content
                    # Clean up JSON
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0]
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0]
                    parsed = json.loads(content.strip())
                    analyses[tool_name] = parsed
                except (json.JSONDecodeError, IndexError):
                    analyses[tool_name] = {"raw": message.content}

        # Get agent summary
        final_message = result["messages"][-1] if result.get("messages") else None
        agent_summary = final_message.content if final_message else ""

        return {
            "research_type": research_type,
            "analyses": analyses,
            "agent_summary": agent_summary,
            "tools_used": _analysis_context.analyses_performed.copy(),
            "data_points_analyzed": len(search_results)
        }

    except Exception as e:
        logger.error(f"Analysis agent failed: {e}")
        return {
            "error": str(e),
            "research_type": research_type
        }
