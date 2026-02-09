"""
Market Research & Competitor Tracking API Backend
Powered by Multi-Agent System with LangGraph for intelligent market analysis
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LangChain imports
from langchain_openai import ChatOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Market Research & Competitor Tracking API",
    description="AI-powered market research using multi-agent system with real web search",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check if static directory exists (for production deployment)
static_dir = Path("static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="static", html=True), name="static")

    @app.get("/")
    async def serve_frontend():
        """Serve React frontend"""
        return FileResponse("static/index.html")


# Request/Response models
class ResearchRequest(BaseModel):
    query: str
    research_type: str  # "market_overview", "competitor_analysis", "trend_analysis", "full_report"
    company_name: Optional[str] = None
    competitors: Optional[List[str]] = None
    industry: Optional[str] = None


class ResearchResponse(BaseModel):
    research_id: str
    status: str
    research_type: str
    results: Dict[str, Any]
    timestamp: str
    summary: str
    workflow_trace: Optional[Dict[str, Any]] = None


# =============================================================================
# LLM AND AGENT INITIALIZATION
# =============================================================================

# Initialize LLM
llm = None
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    logger.warning("OPENAI_API_KEY not set in environment. LLM will be unavailable.")
else:
    try:
        llm = ChatOpenAI(
            model=os.environ.get("LLM_MODEL", "gpt-5"),
            temperature=float(os.environ.get("LLM_TEMPERATURE", "0.7")),
            max_tokens=int(os.environ.get("LLM_MAX_TOKENS", "4000")),
            api_key=api_key,
        )
        logger.info(f"Successfully initialized LLM with {os.environ.get('LLM_MODEL', 'gpt-5')}")
    except Exception as e:
        logger.warning(f"OpenAI initialization warning: {e}")
        llm = None


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Market Research & Competitor Tracking API",
        "version": "2.0.0",
        "architecture": "multi-agent",
        "timestamp": datetime.now().isoformat(),
        "llm_available": llm is not None,
        "agents": ["research", "analysis", "strategy"]
    }


@app.post("/research/execute", response_model=ResearchResponse)
async def execute_research(request: ResearchRequest):
    """
    Execute market research using the multi-agent workflow.

    The workflow:
    1. Research Agent: Gathers data via web search
    2. Analysis Agent: Analyzes the gathered data
    3. Strategy Agent: Generates recommendations
    """
    try:
        logger.info(f"Received research request: {request.research_type}")

        # Generate unique research ID
        research_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        if not llm:
            raise HTTPException(
                status_code=503,
                detail="LLM not available. Please check OPENAI_API_KEY."
            )

        # Import and run the multi-agent workflow
        from agents.orchestrator import run_research

        result = run_research(
            llm=llm,
            query=request.query,
            research_type=request.research_type,
            company=request.company_name,
            competitors=request.competitors,
            industry=request.industry
        )

        # Handle workflow result
        if result.get("status") == "failed":
            raise HTTPException(
                status_code=500,
                detail=f"Research workflow failed: {result.get('error', 'Unknown error')}"
            )

        return ResearchResponse(
            research_id=research_id,
            status=result.get("status", "completed"),
            research_type=request.research_type,
            results=result.get("results", {}),
            timestamp=datetime.now().isoformat(),
            summary=result.get("summary", "Research complete."),
            workflow_trace=result.get("workflow_trace")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Research execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Research execution failed: {str(e)}")


@app.get("/research/types")
async def get_research_types():
    """Get available research types"""
    return {
        "research_types": [
            {
                "id": "market_overview",
                "name": "Market Overview",
                "description": "Comprehensive market size, trends, and opportunities analysis using real-time web data"
            },
            {
                "id": "competitor_analysis",
                "name": "Competitor Analysis",
                "description": "Detailed competitor profiling, SWOT, and positioning analysis with current market data"
            },
            {
                "id": "trend_analysis",
                "name": "Trend Analysis",
                "description": "Emerging trends, patterns, and future predictions from real-time sources"
            },
            {
                "id": "full_report",
                "name": "Full Research Report",
                "description": "Comprehensive report combining all research dimensions with strategic recommendations"
            }
        ]
    }


@app.get("/agents/status")
async def get_agents_status():
    """Get status of the multi-agent system"""
    return {
        "architecture": "multi-agent with LangGraph",
        "agents": [
            {
                "name": "Research Agent",
                "role": "Data gathering via web search",
                "tools": ["web_search", "news_search", "company_search", "market_search"],
                "status": "active" if llm else "inactive"
            },
            {
                "name": "Analysis Agent",
                "role": "Data analysis and insight extraction",
                "capabilities": ["market_analysis", "competitor_analysis", "trend_analysis", "swot_analysis"],
                "status": "active" if llm else "inactive"
            },
            {
                "name": "Strategy Agent",
                "role": "Strategic recommendations and executive summary",
                "capabilities": ["recommendations", "executive_summary", "risk_assessment"],
                "status": "active" if llm else "inactive"
            }
        ],
        "workflow": "research -> analyze -> strategize -> compile",
        "llm_available": llm is not None
    }


@app.get("/tools/list")
async def list_tools():
    """List available research tools"""
    return {
        "tools": [
            {
                "name": "web_search",
                "description": "Search the web for general information using DuckDuckGo",
                "agent": "Research Agent"
            },
            {
                "name": "news_search",
                "description": "Search for recent news articles",
                "agent": "Research Agent"
            },
            {
                "name": "company_search",
                "description": "Comprehensive company research including overview, news, financials",
                "agent": "Research Agent"
            },
            {
                "name": "market_search",
                "description": "Search for market and industry data",
                "agent": "Research Agent"
            },
            {
                "name": "analyze_market_data",
                "description": "LLM-powered market data analysis",
                "agent": "Analysis Agent"
            },
            {
                "name": "analyze_competitors",
                "description": "Competitor profiling and comparison",
                "agent": "Analysis Agent"
            },
            {
                "name": "identify_trends",
                "description": "Trend extraction and prediction",
                "agent": "Analysis Agent"
            },
            {
                "name": "generate_swot",
                "description": "SWOT analysis generation",
                "agent": "Analysis Agent"
            }
        ]
    }


# Catch-all route for React frontend (must be registered AFTER all API routes)
if static_dir.exists():
    @app.get("/{path:path}")
    async def serve_frontend_routes(path: str):
        """Serve React frontend for all non-API routes"""
        return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    logger.info(f"Starting Market Research API (Multi-Agent v2.0) on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
