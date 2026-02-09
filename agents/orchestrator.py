"""
Research Orchestrator
Coordinates the multi-agent workflow using LangGraph.
"""

import logging
from typing import Dict, Any, Callable, List, Optional, TypedDict, Annotated
from datetime import datetime

from langchain_core.callbacks import BaseCallbackHandler
from langgraph.graph import StateGraph, END

from .research_agent import run_research_agent
from .analysis_agent import run_analysis_agent
from .strategy_agent import run_strategy_agent, generate_final_report

logger = logging.getLogger(__name__)


class ResearchState(TypedDict):
    """State that flows through the research workflow."""
    # Input
    query: str
    research_type: str
    company: str
    competitors: List[str]
    industry: str

    # Agent outputs
    research_data: Dict[str, Any]
    analysis_data: Dict[str, Any]
    strategy_data: Dict[str, Any]

    # Final output
    final_report: Dict[str, Any]

    # Metadata
    status: str
    error: str
    current_agent: str


class IterationProgressHandler(BaseCallbackHandler):
    """LangChain callback handler that reports tool-call progress."""

    def __init__(self, agent_name: str, callback: Callable, max_iterations: int = 3):
        self.agent_name = agent_name
        self.callback = callback
        self.iteration = 0
        self.max_iterations = max_iterations

    def on_tool_end(self, output, **kwargs):
        self.iteration += 1
        self.callback({
            "agent": self.agent_name,
            "status": "progress",
            "iteration": self.iteration,
            "max_iterations": self.max_iterations,
        })


def create_research_node(llm, progress_callback=None):
    """Create the research agent node."""

    def research_node(state: ResearchState) -> Dict[str, Any]:
        logger.info(f"Research node: Starting research for '{state['query']}'")

        callbacks = None
        if progress_callback:
            callbacks = [IterationProgressHandler("research", progress_callback)]

        research_data = run_research_agent(
            llm=llm,
            query=state["query"],
            research_type=state["research_type"],
            company=state.get("company"),
            competitors=state.get("competitors", []),
            industry=state.get("industry"),
            callbacks=callbacks,
        )

        if research_data.get("error"):
            return {
                "research_data": research_data,
                "status": "research_failed",
                "error": research_data["error"],
                "current_agent": "research"
            }

        return {
            "research_data": research_data,
            "status": "research_complete",
            "current_agent": "research"
        }

    return research_node


def create_analysis_node(llm, progress_callback=None):
    """Create the analysis agent node."""

    def analysis_node(state: ResearchState) -> Dict[str, Any]:
        logger.info(f"Analysis node: Analyzing data for '{state['query']}'")

        research_data = state.get("research_data", {})

        if not research_data or research_data.get("error"):
            return {
                "analysis_data": {"error": "No research data to analyze"},
                "status": "analysis_failed",
                "error": "No research data available",
                "current_agent": "analysis"
            }

        callbacks = None
        if progress_callback:
            callbacks = [IterationProgressHandler("analyze", progress_callback)]

        analysis_data = run_analysis_agent(
            llm=llm,
            research_data=research_data,
            research_type=state["research_type"],
            company=state.get("company"),
            competitors=state.get("competitors", []),
            industry=state.get("industry"),
            callbacks=callbacks,
        )

        if analysis_data.get("error"):
            return {
                "analysis_data": analysis_data,
                "status": "analysis_failed",
                "error": analysis_data["error"],
                "current_agent": "analysis"
            }

        return {
            "analysis_data": analysis_data,
            "status": "analysis_complete",
            "current_agent": "analysis"
        }

    return analysis_node


def create_strategy_node(llm, progress_callback=None):
    """Create the strategy agent node."""

    def strategy_node(state: ResearchState) -> Dict[str, Any]:
        logger.info(f"Strategy node: Generating recommendations for '{state['query']}'")

        analysis_data = state.get("analysis_data", {})

        if not analysis_data or analysis_data.get("error"):
            return {
                "strategy_data": {"error": "No analysis data for strategy"},
                "status": "strategy_failed",
                "error": "No analysis data available",
                "current_agent": "strategy"
            }

        callbacks = None
        if progress_callback:
            callbacks = [IterationProgressHandler("strategize", progress_callback)]

        strategy_data = run_strategy_agent(
            llm=llm,
            analysis_data=analysis_data,
            query=state["query"],
            company=state.get("company"),
            research_type=state.get("research_type", "general"),
            callbacks=callbacks,
        )

        if strategy_data.get("error"):
            return {
                "strategy_data": strategy_data,
                "status": "strategy_failed",
                "error": strategy_data["error"],
                "current_agent": "strategy"
            }

        return {
            "strategy_data": strategy_data,
            "status": "strategy_complete",
            "current_agent": "strategy"
        }

    return strategy_node


def compile_report_node(state: ResearchState) -> Dict[str, Any]:
    """Compile the final report from all agent outputs."""
    logger.info("Compile node: Generating final report")

    research_data = state.get("research_data", {})
    analysis_data = state.get("analysis_data", {})
    strategy_data = state.get("strategy_data", {})

    final_report = generate_final_report(
        analysis_data=analysis_data,
        strategy_data=strategy_data,
        research_data=research_data
    )

    return {
        "final_report": final_report,
        "status": "completed",
        "current_agent": "complete"
    }


def should_continue(state: ResearchState) -> str:
    """Determine if workflow should continue or end due to error."""
    status = state.get("status", "")

    if "failed" in status:
        return "end"

    return "continue"


def _wrap_node_with_callback(node_fn, agent_name, callback):
    """Wrap a graph node function to emit progress events before and after execution."""
    def wrapped(state):
        callback({"agent": agent_name, "status": "started"})
        try:
            result = node_fn(state)
            callback({"agent": agent_name, "status": "completed"})
            return result
        except Exception as e:
            callback({"agent": agent_name, "status": "error", "error": str(e)})
            raise
    return wrapped


def create_research_workflow(llm, progress_callback: Optional[Callable] = None):
    """
    Create the LangGraph workflow for market research.

    Args:
        llm: Language model instance
        progress_callback: Optional callback for progress events

    Returns:
        Compiled LangGraph workflow
    """
    logger.info("Creating research workflow graph")

    # Create the graph
    workflow = StateGraph(ResearchState)

    # Create node functions (pass callback for iteration-level progress)
    research_fn = create_research_node(llm, progress_callback)
    analyze_fn = create_analysis_node(llm, progress_callback)
    strategize_fn = create_strategy_node(llm, progress_callback)
    compile_fn = compile_report_node

    # Wrap with progress callback if provided
    if progress_callback:
        research_fn = _wrap_node_with_callback(research_fn, "research", progress_callback)
        analyze_fn = _wrap_node_with_callback(analyze_fn, "analyze", progress_callback)
        strategize_fn = _wrap_node_with_callback(strategize_fn, "strategize", progress_callback)
        compile_fn = _wrap_node_with_callback(compile_fn, "compile", progress_callback)

    # Add nodes
    workflow.add_node("research", research_fn)
    workflow.add_node("analyze", analyze_fn)
    workflow.add_node("strategize", strategize_fn)
    workflow.add_node("compile", compile_fn)

    # Set entry point
    workflow.set_entry_point("research")

    # Add edges - linear flow with error handling
    workflow.add_conditional_edges(
        "research",
        should_continue,
        {
            "continue": "analyze",
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "analyze",
        should_continue,
        {
            "continue": "strategize",
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "strategize",
        should_continue,
        {
            "continue": "compile",
            "end": END
        }
    )

    workflow.add_edge("compile", END)

    # Compile the graph
    return workflow.compile()


def run_research(llm, query: str, research_type: str, company: str = None,
                 competitors: List[str] = None, industry: str = None,
                 progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
    """
    Run the complete research workflow.

    Args:
        llm: Language model instance
        query: Research query
        research_type: Type of research
        company: Optional company name
        competitors: Optional list of competitors
        industry: Optional industry name
        progress_callback: Optional callback for progress events

    Returns:
        Complete research results
    """
    logger.info(f"Starting research workflow: {query} ({research_type})")

    # Create the workflow
    workflow = create_research_workflow(llm, progress_callback=progress_callback)

    # Initialize state
    initial_state: ResearchState = {
        "query": query,
        "research_type": research_type,
        "company": company or "",
        "competitors": competitors or [],
        "industry": industry or "",
        "research_data": {},
        "analysis_data": {},
        "strategy_data": {},
        "final_report": {},
        "status": "starting",
        "error": "",
        "current_agent": "init"
    }

    try:
        # Run the workflow
        result = workflow.invoke(initial_state)

        # Check for errors
        if result.get("error"):
            logger.warning(f"Workflow completed with error: {result['error']}")

        return {
            "status": result.get("status", "unknown"),
            "results": result.get("final_report", {}),
            "summary": result.get("final_report", {}).get("executive_summary", "Research complete."),
            "workflow_trace": {
                "research_completed": bool(result.get("research_data")),
                "analysis_completed": bool(result.get("analysis_data")),
                "strategy_completed": bool(result.get("strategy_data")),
                "final_agent": result.get("current_agent", "unknown")
            }
        }

    except Exception as e:
        logger.error(f"Research workflow failed: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "results": {},
            "summary": f"Research failed: {str(e)}"
        }
