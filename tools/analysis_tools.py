"""
Analysis Tools for Market Research
LLM-powered tools for analyzing gathered data.
"""

import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def format_search_results(results: List[Dict[str, Any]]) -> str:
    """Format search results into a readable string for LLM analysis."""
    if not results:
        return "No data available."

    formatted = []
    for i, r in enumerate(results, 1):
        if "error" in r:
            continue
        entry = f"[{i}] {r.get('title', 'No title')}\n"
        entry += f"    Source: {r.get('url', r.get('source', 'Unknown'))}\n"
        entry += f"    {r.get('snippet', 'No description')}\n"
        if r.get('date'):
            entry += f"    Date: {r.get('date')}\n"
        formatted.append(entry)

    return "\n".join(formatted) if formatted else "No valid data found."


def analyze_market_data(llm, search_results: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
    """
    Analyze market data using LLM.

    Args:
        llm: The language model instance
        search_results: Raw search results to analyze
        query: Original research query for context

    Returns:
        Structured market analysis
    """
    logger.info(f"Analyzing market data for: {query}")

    formatted_data = format_search_results(search_results)

    prompt = f"""Based on the following search results about "{query}", provide a comprehensive market analysis.

SEARCH RESULTS:
{formatted_data}

Analyze this data and provide a JSON response with:
{{
    "market_size": "Estimated market size with source if available",
    "growth_rate": "Historical and projected growth rates",
    "key_trends": ["List of 5-7 major market trends identified"],
    "market_segments": "Key market segments and their characteristics",
    "opportunities": ["List of growth opportunities"],
    "challenges": ["List of market challenges and barriers"],
    "key_players": ["Major companies in this market"],
    "data_sources": ["Sources used for this analysis"]
}}

Return ONLY valid JSON, no markdown formatting."""

    from langchain_core.messages import HumanMessage, SystemMessage

    response = llm.invoke([
        SystemMessage(content="You are a market research analyst. Analyze data and return structured JSON insights. Always base your analysis on the provided data."),
        HumanMessage(content=prompt)
    ])

    try:
        # Clean response
        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        return json.loads(content)
    except json.JSONDecodeError:
        logger.warning("Failed to parse market analysis as JSON, returning raw response")
        return {"raw_analysis": response.content, "parse_error": True}


def analyze_competitors(llm, search_results: List[Dict[str, Any]], company: str, competitors: List[str]) -> Dict[str, Any]:
    """
    Analyze competitor data using LLM.

    Args:
        llm: The language model instance
        search_results: Raw search results about competitors
        company: The main company being analyzed
        competitors: List of competitor names

    Returns:
        Structured competitor analysis
    """
    logger.info(f"Analyzing competitors for: {company}")

    formatted_data = format_search_results(search_results)
    competitor_list = ", ".join(competitors) if competitors else "industry competitors"

    prompt = f"""Based on the following search results, analyze the competitive landscape for {company} against {competitor_list}.

SEARCH RESULTS:
{formatted_data}

Provide a JSON response with:
{{
    "company_profile": {{
        "name": "{company}",
        "market_position": "Description of market position",
        "key_strengths": ["List of strengths"],
        "key_weaknesses": ["List of weaknesses"]
    }},
    "competitors": [
        {{
            "name": "Competitor name",
            "market_position": "Their market position",
            "strengths": ["Their strengths"],
            "weaknesses": ["Their weaknesses"],
            "strategy": "Their apparent strategy"
        }}
    ],
    "market_share_analysis": "Analysis of market share distribution",
    "competitive_advantages": ["Key competitive advantages identified"],
    "threats": ["Competitive threats"],
    "recommendations": ["Strategic recommendations"],
    "data_sources": ["Sources used"]
}}

Return ONLY valid JSON, no markdown formatting."""

    from langchain_core.messages import HumanMessage, SystemMessage

    response = llm.invoke([
        SystemMessage(content="You are a competitive intelligence analyst. Provide structured competitor analysis based on the provided data."),
        HumanMessage(content=prompt)
    ])

    try:
        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        return json.loads(content)
    except json.JSONDecodeError:
        logger.warning("Failed to parse competitor analysis as JSON")
        return {"raw_analysis": response.content, "parse_error": True}


def identify_trends(llm, search_results: List[Dict[str, Any]], industry: str) -> Dict[str, Any]:
    """
    Identify and analyze trends from search data.

    Args:
        llm: The language model instance
        search_results: Raw search results about industry trends
        industry: The industry being analyzed

    Returns:
        Structured trend analysis
    """
    logger.info(f"Identifying trends for: {industry}")

    formatted_data = format_search_results(search_results)

    prompt = f"""Based on the following search results about {industry}, identify and analyze emerging trends.

SEARCH RESULTS:
{formatted_data}

Provide a JSON response with:
{{
    "emerging_trends": [
        {{
            "trend": "Trend name",
            "description": "What this trend is about",
            "impact": "Potential business impact",
            "timeline": "When this is expected to peak/mature"
        }}
    ],
    "technology_trends": ["Technology-related trends"],
    "consumer_trends": ["Consumer behavior trends"],
    "regulatory_trends": ["Regulatory and policy trends"],
    "predictions": {{
        "short_term": "1-2 year outlook",
        "medium_term": "3-5 year outlook",
        "long_term": "5+ year outlook"
    }},
    "opportunities": ["Trend-driven opportunities"],
    "risks": ["Trend-related risks"],
    "data_sources": ["Sources used"]
}}

Return ONLY valid JSON, no markdown formatting."""

    from langchain_core.messages import HumanMessage, SystemMessage

    response = llm.invoke([
        SystemMessage(content="You are a trend analyst specializing in market forecasting. Identify trends from data and provide structured analysis."),
        HumanMessage(content=prompt)
    ])

    try:
        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        return json.loads(content)
    except json.JSONDecodeError:
        logger.warning("Failed to parse trend analysis as JSON")
        return {"raw_analysis": response.content, "parse_error": True}


def generate_swot(llm, market_data: Dict, competitor_data: Dict, trend_data: Dict, company: str) -> Dict[str, Any]:
    """
    Generate a SWOT analysis from combined research data.

    Args:
        llm: The language model instance
        market_data: Market analysis results
        competitor_data: Competitor analysis results
        trend_data: Trend analysis results
        company: Company name for the SWOT

    Returns:
        Structured SWOT analysis
    """
    logger.info(f"Generating SWOT for: {company}")

    prompt = f"""Based on the following research data, generate a comprehensive SWOT analysis for {company}.

MARKET DATA:
{json.dumps(market_data, indent=2)}

COMPETITOR DATA:
{json.dumps(competitor_data, indent=2)}

TREND DATA:
{json.dumps(trend_data, indent=2)}

Provide a JSON response with:
{{
    "strengths": [
        {{
            "item": "Strength description",
            "evidence": "Supporting evidence from data"
        }}
    ],
    "weaknesses": [
        {{
            "item": "Weakness description",
            "evidence": "Supporting evidence from data"
        }}
    ],
    "opportunities": [
        {{
            "item": "Opportunity description",
            "source": "Where this opportunity comes from (market trend, competitor gap, etc.)"
        }}
    ],
    "threats": [
        {{
            "item": "Threat description",
            "source": "Source of this threat"
        }}
    ],
    "strategic_implications": "Overall strategic implications of this SWOT",
    "priority_actions": ["Top 3-5 recommended actions based on SWOT"]
}}

Return ONLY valid JSON, no markdown formatting."""

    from langchain_core.messages import HumanMessage, SystemMessage

    response = llm.invoke([
        SystemMessage(content="You are a strategic analyst. Generate SWOT analysis based on research data."),
        HumanMessage(content=prompt)
    ])

    try:
        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        return json.loads(content)
    except json.JSONDecodeError:
        logger.warning("Failed to parse SWOT analysis as JSON")
        return {"raw_analysis": response.content, "parse_error": True}
