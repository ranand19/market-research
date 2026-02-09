"""
Strategy Agent
A truly agentic strategist that autonomously decides what recommendations to generate.
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

class StrategyContext:
    """Shared context for strategy tools."""
    analysis_data: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    llm = None
    strategies_generated: List[str] = []


_strategy_context = StrategyContext()


def _get_analysis_summary() -> str:
    """Get a formatted summary of available analysis data."""
    parts = []
    data = _strategy_context.analysis_data

    if "analyses" in data:
        for tool_name, result in data["analyses"].items():
            parts.append(f"=== {tool_name.upper()} ===\n{json.dumps(result, indent=2)[:1500]}")

    if "agent_summary" in data:
        parts.append(f"=== ANALYST SUMMARY ===\n{data['agent_summary']}")

    return "\n\n".join(parts) if parts else json.dumps(data, indent=2)[:3000]


# =============================================================================
# STRATEGY TOOLS
# =============================================================================

@tool
def generate_strategic_recommendations(focus_area: str) -> str:
    """
    Generate strategic recommendations based on analysis.
    Use for specific focus areas like 'growth', 'cost reduction', 'market entry'.

    Args:
        focus_area: The focus area for recommendations
    """
    logger.info(f"Tool: generate_strategic_recommendations - {focus_area}")

    analysis_summary = _get_analysis_summary()

    prompt = f"""Based on the following analysis, generate strategic recommendations focused on: {focus_area}

ANALYSIS DATA:
{analysis_summary}

Return a JSON object with:
{{
    "recommendations": [
        {{
            "recommendation": "Specific, actionable recommendation",
            "rationale": "Why this is recommended based on analysis",
            "priority": "high/medium/low",
            "timeframe": "immediate/short-term/medium-term/long-term"
        }}
    ],
    "focus_area": "{focus_area}",
    "key_success_factors": ["Critical factors for success"]
}}

Return ONLY valid JSON."""

    response = _strategy_context.llm.invoke([
        SystemMessage(content="You are a senior strategy consultant. Provide specific, actionable recommendations."),
        HumanMessage(content=prompt)
    ])

    _strategy_context.strategies_generated.append("recommendations")
    return response.content


@tool
def assess_risks(context: str) -> str:
    """
    Assess risks and threats with mitigation strategies.
    Use to identify what could go wrong.

    Args:
        context: Context for risk assessment
    """
    logger.info(f"Tool: assess_risks - {context}")

    analysis_summary = _get_analysis_summary()

    prompt = f"""Based on the following analysis, assess risks and threats for: {context}

ANALYSIS DATA:
{analysis_summary}

Return a JSON object with:
{{
    "risks": [
        {{
            "risk": "Description of the risk",
            "category": "Market/Competitive/Operational/Financial/Regulatory",
            "likelihood": "high/medium/low",
            "impact": "high/medium/low",
            "mitigation": "How to reduce or manage this risk"
        }}
    ],
    "overall_risk_level": "high/medium/low",
    "most_critical_risks": ["Top 2-3 risks requiring immediate attention"]
}}

Return ONLY valid JSON."""

    response = _strategy_context.llm.invoke([
        SystemMessage(content="You are a risk management expert."),
        HumanMessage(content=prompt)
    ])

    _strategy_context.strategies_generated.append("risk_assessment")
    return response.content


@tool
def identify_opportunities(context: str) -> str:
    """
    Identify strategic opportunities for growth or improvement.
    Use to find actionable opportunities.

    Args:
        context: Context for opportunity identification
    """
    logger.info(f"Tool: identify_opportunities - {context}")

    analysis_summary = _get_analysis_summary()

    prompt = f"""Based on the following analysis, identify strategic opportunities for: {context}

ANALYSIS DATA:
{analysis_summary}

Return a JSON object with:
{{
    "opportunities": [
        {{
            "opportunity": "Description of the opportunity",
            "category": "Growth/Innovation/Efficiency/Partnership/Market Entry",
            "potential_value": "Estimated impact or value",
            "feasibility": "high/medium/low",
            "action_required": "First steps to pursue this"
        }}
    ],
    "quick_wins": ["Opportunities that can be pursued immediately"],
    "strategic_bets": ["Larger opportunities requiring significant investment"]
}}

Return ONLY valid JSON."""

    response = _strategy_context.llm.invoke([
        SystemMessage(content="You are a growth strategist."),
        HumanMessage(content=prompt)
    ])

    _strategy_context.strategies_generated.append("opportunities")
    return response.content


@tool
def create_action_plan(objective: str) -> str:
    """
    Create a phased action plan with specific steps.
    Use when you need a roadmap for implementation.

    Args:
        objective: The objective for the action plan
    """
    logger.info(f"Tool: create_action_plan - {objective}")

    analysis_summary = _get_analysis_summary()

    prompt = f"""Based on the following analysis, create an action plan for: {objective}

ANALYSIS DATA:
{analysis_summary}

Return a JSON object with:
{{
    "objective": "{objective}",
    "phases": [
        {{
            "phase": "Phase 1",
            "goal": "What this phase achieves",
            "actions": ["List of specific actions"],
            "timeline": "Duration"
        }}
    ],
    "critical_path": ["Actions that must happen in sequence"],
    "success_metrics": ["How to measure success"]
}}

Return ONLY valid JSON."""

    response = _strategy_context.llm.invoke([
        SystemMessage(content="You are a program manager. Create practical action plans."),
        HumanMessage(content=prompt)
    ])

    _strategy_context.strategies_generated.append("action_plan")
    return response.content


@tool
def generate_executive_summary(context: str) -> str:
    """
    Generate an executive-level summary of findings and recommendations.
    Use to synthesize everything into a concise overview.

    Args:
        context: Context for the summary
    """
    logger.info(f"Tool: generate_executive_summary - {context}")

    analysis_summary = _get_analysis_summary()

    prompt = f"""Based on the following analysis, create an executive summary for: {context}

ANALYSIS DATA:
{analysis_summary}

Return a JSON object with:
{{
    "executive_summary": "A concise 4-6 sentence summary covering: situation, key findings, main opportunities/risks, and recommended direction",
    "key_findings": [
        {{
            "finding": "Important insight",
            "implication": "What this means for the business"
        }}
    ],
    "bottom_line": "The single most important takeaway",
    "recommended_next_steps": ["Top 3 immediate actions"]
}}

Return ONLY valid JSON."""

    response = _strategy_context.llm.invoke([
        SystemMessage(content="You are an executive advisor. Create a clear, concise summary."),
        HumanMessage(content=prompt)
    ])

    _strategy_context.strategies_generated.append("executive_summary")
    return response.content


@tool
def competitive_response_strategy(context: str) -> str:
    """
    Develop strategies to respond to competitive threats.
    Use when competition is a key concern.

    Args:
        context: Context for competitive strategy
    """
    logger.info(f"Tool: competitive_response_strategy - {context}")

    analysis_summary = _get_analysis_summary()

    prompt = f"""Based on the following analysis, develop competitive response strategies for: {context}

ANALYSIS DATA:
{analysis_summary}

Return a JSON object with:
{{
    "competitive_position": "Current position assessment",
    "response_strategies": [
        {{
            "competitor_threat": "What to address",
            "response": "Recommended response",
            "type": "Defensive/Offensive/Differentiation"
        }}
    ],
    "differentiation_opportunities": ["Ways to stand out"],
    "competitive_moats": ["Advantages to build or protect"]
}}

Return ONLY valid JSON."""

    response = _strategy_context.llm.invoke([
        SystemMessage(content="You are a competitive strategist."),
        HumanMessage(content=prompt)
    ])

    _strategy_context.strategies_generated.append("competitive_strategy")
    return response.content


def get_strategy_tools() -> List:
    """Get the list of strategy tools."""
    return [
        generate_strategic_recommendations,
        assess_risks,
        identify_opportunities,
        create_action_plan,
        generate_executive_summary,
        competitive_response_strategy
    ]


def create_strategy_agent(llm):
    """Create the strategy agent using LangGraph."""
    tools = get_strategy_tools()

    system_prompt = """You are a senior strategy consultant at a top-tier consulting firm.

You have access to several strategy tools. Based on the research type, decide which outputs to generate:

- For MARKET OVERVIEW: Generate recommendations, identify opportunities, create executive summary
- For COMPETITOR ANALYSIS: Assess risks, develop competitive response strategy, generate recommendations
- For TREND ANALYSIS: Identify opportunities, generate recommendations, create executive summary
- For FULL REPORT: Use ALL tools to provide comprehensive strategic guidance

Always:
1. Generate an executive summary (clients always need this)
2. Provide actionable recommendations
3. Address both opportunities and risks

Be strategic and insightful. Use 2-3 of the most relevant tools."""

    agent = create_react_agent(llm, tools, prompt=system_prompt)
    return agent


def run_strategy_agent(llm, analysis_data: Dict[str, Any], query: str,
                       company: str = None, research_type: str = "general",
                       callbacks=None) -> Dict[str, Any]:
    """
    Run the strategy agent to autonomously generate strategic outputs.
    """
    logger.info(f"Running strategy agent for: {query}")

    if not analysis_data or analysis_data.get("error"):
        logger.warning("No analysis data for strategy")
        return {"error": "No analysis data available", "research_type": research_type}

    # Set up shared context for tools
    _strategy_context.analysis_data = analysis_data
    _strategy_context.context = {
        "query": query,
        "company": company or "",
        "research_type": research_type
    }
    _strategy_context.llm = llm
    _strategy_context.strategies_generated = []

    # Create and run the agent
    agent = create_strategy_agent(llm)

    # Build the strategy prompt
    if research_type == "market_overview":
        prompt = f"""Based on the market analysis for "{query}", develop strategic guidance.

Generate:
1. Use generate_strategic_recommendations for market participation
2. Use identify_opportunities for growth opportunities
3. Use generate_executive_summary for findings overview"""

    elif research_type == "competitor_analysis":
        prompt = f"""Based on the competitive analysis for "{company or query}", develop strategic guidance.

Generate:
1. Use assess_risks for competitive threats
2. Use competitive_response_strategy for response plans
3. Use generate_strategic_recommendations
4. Use generate_executive_summary"""

    elif research_type == "trend_analysis":
        prompt = f"""Based on the trend analysis for "{query}", develop strategic guidance.

Generate:
1. Use identify_opportunities from trends
2. Use generate_strategic_recommendations for trend response
3. Use generate_executive_summary"""

    else:  # full_report
        prompt = f"""Based on the comprehensive analysis for "{query}", develop full strategic guidance.

Use ALL strategy tools:
1. generate_strategic_recommendations
2. assess_risks
3. identify_opportunities
4. competitive_response_strategy
5. create_action_plan
6. generate_executive_summary

Focus on the 3-4 most impactful tools for a complete strategic perspective."""

    try:
        invoke_config = {"recursion_limit": 25}
        if callbacks:
            invoke_config["callbacks"] = callbacks
        result = agent.invoke(
            {"messages": [HumanMessage(content=prompt)]},
            invoke_config,
        )

        # Extract strategies from tool messages
        strategies = {}
        for message in result.get("messages", []):
            if hasattr(message, 'type') and message.type == "tool":
                tool_name = getattr(message, 'name', 'unknown')
                try:
                    content = message.content
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0]
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0]
                    parsed = json.loads(content.strip())
                    strategies[tool_name] = parsed
                except (json.JSONDecodeError, IndexError):
                    strategies[tool_name] = {"raw": message.content}

        # Extract executive summary
        exec_summary = ""
        if "generate_executive_summary" in strategies:
            summary_data = strategies["generate_executive_summary"]
            if isinstance(summary_data, dict):
                exec_summary = summary_data.get("executive_summary", "")

        # Get agent synthesis
        final_message = result["messages"][-1] if result.get("messages") else None
        agent_synthesis = final_message.content if final_message else ""

        return {
            "research_type": research_type,
            "strategies": strategies,
            "agent_synthesis": agent_synthesis,
            "executive_summary": exec_summary,
            "tools_used": _strategy_context.strategies_generated.copy()
        }

    except Exception as e:
        logger.error(f"Strategy agent failed: {e}")
        return {
            "error": str(e),
            "research_type": research_type
        }


def generate_final_report(analysis_data: Dict[str, Any], strategy_data: Dict[str, Any],
                          research_data: Dict[str, Any]) -> Dict[str, Any]:
    """Compile the final research report from all agent outputs."""
    logger.info("Generating final report")

    report = {
        "executive_summary": strategy_data.get("executive_summary", ""),
        "research_type": analysis_data.get("research_type", "general"),
        "data_sources": {
            "searches_performed": research_data.get("num_searches", 0),
            "data_points_analyzed": analysis_data.get("data_points_analyzed", 0)
        },
        "agent_workflow": {
            "research_agent": {
                "searches": research_data.get("num_searches", 0),
                "results_gathered": len(research_data.get("search_results", []))
            },
            "analysis_agent": {
                "tools_used": analysis_data.get("tools_used", []),
                "analyses_performed": list(analysis_data.get("analyses", {}).keys())
            },
            "strategy_agent": {
                "tools_used": strategy_data.get("tools_used", []),
                "outputs_generated": list(strategy_data.get("strategies", {}).keys())
            }
        }
    }

    if "analyses" in analysis_data:
        report["analysis"] = analysis_data["analyses"]

    if "agent_summary" in analysis_data:
        report["analyst_summary"] = analysis_data["agent_summary"]

    if "strategies" in strategy_data:
        report["strategic_guidance"] = strategy_data["strategies"]

    if "agent_synthesis" in strategy_data:
        report["strategist_synthesis"] = strategy_data["agent_synthesis"]

    return report
