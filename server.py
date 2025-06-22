#!/usr/bin/env python3
"""CortexMCP Server.

A Model Context Protocol server providing strategic cognition capabilities
for Claude Code. Uses official FastMCP framework.

Following the 4 Principios Rectores:
1. Dogmatismo con Universal Response Schema
2. Servidor como Ejecutor Fiable
3. Estado en Claude, NO en Servidor  
4. Testing Concurrente
"""

import json
import logging
from typing import Any, Dict, Optional, Literal, Annotated

from pydantic import Field
from mcp.server.fastmcp import FastMCP
from schemas.universal_response import StrategyResponse, BasePayload

# Configure logging
logger = logging.getLogger(__name__)

# Initialize FastMCP server
app = FastMCP("cortex-mcp", "1.0.0")


@app.tool(
    name="strategy-architect",
    description="Strategic planning and architecture tool that transforms project ideas into structured plans"
)
def strategy_architect(
    task_description: Annotated[str, Field(
        description="Description of the project or task to analyze and plan. Should be a clear, comprehensive description of what you want to build or accomplish.",
        min_length=5,
        max_length=2000,
        examples=["Build an e-commerce platform with payment integration", "Create a task management web application with user authentication"]
    )],
    analysis_result: Annotated[Optional[Dict[str, Any]], Field(
        description="Previous analysis result from a workflow continuation. Only provide this when continuing from a previous strategy-architect execution. Contains project analysis data."
    )] = None,
    decomposition_result: Annotated[Optional[Dict[str, Any]], Field(
        description="Previous decomposition result from a workflow continuation. Only provide this when continuing from a previous strategy-architect execution. Contains project phase breakdown."
    )] = None,
    workflow_stage: Annotated[Optional[Literal["analysis", "decomposition", "task_graph", "mission_map", "complete"]], Field(
        description="Current workflow stage for continuation. Use 'analysis' to start from analysis phase, 'decomposition' to start from decomposition phase, etc. Leave empty for complete workflow execution from the beginning."
    )] = None,
    debug_mode: Annotated[Optional[bool], Field(
        description="Enable debug mode to include intermediate workflow results in debug_payload. Default: false. Only enable when debugging workflow execution."
    )] = False
) -> str:
    """Execute strategy-architect workflow with Motor de Estrategias integration.
    
    Following Principio Rector #1: Must return valid StrategyResponse.
    Following Principio Rector #3: Servidor 100% stateless.
    
    Args:
        task_description: Description of the project or task to analyze and plan
        analysis_result: Previous analysis result (for workflow continuation)
        decomposition_result: Previous decomposition result (for workflow continuation)  
        workflow_stage: Current workflow stage (analysis, decomposition, task_graph, mission_map, complete)
        debug_mode: Enable debug payload with intermediate workflow results
        
    Returns:
        JSON string containing StrategyResponse with Motor de Estrategias results
    """
    try:
        # Validate input parameters following inputSchema constraints
        if len(task_description) < 5:
            raise ValueError("task_description must be at least 5 characters long")
        if len(task_description) > 2000:
            raise ValueError("task_description must be at most 2000 characters long")
        
        if workflow_stage and workflow_stage not in ["analysis", "decomposition", "task_graph", "mission_map", "complete"]:
            raise ValueError(f"Invalid workflow_stage: {workflow_stage}. Must be one of: analysis, decomposition, task_graph, mission_map, complete")
        
        # Execute collaborative workflow (Phase 2.7)
        from tools.architect_unified import execute_architect_workflow
        response = execute_architect_workflow(
            task_description=task_description,
            analysis_result=analysis_result,
            decomposition_result=decomposition_result,
            workflow_stage=workflow_stage,
            debug_mode=debug_mode
        )
        
        # Return StrategyResponse as JSON string
        return response.model_dump_json(indent=2)
        
    except Exception as e:
        # Proper error handling following JSON-RPC 2.0
        logger.error(f"Strategy-architect execution failed: {str(e)}")
        raise ValueError(f"Strategy-architect execution failed: {str(e)}")


@app.tool(
    name="start-retrospective",
    description="Create structured retrospective draft for knowledge capture and analysis"
)
def start_retrospective(
    task_name: Annotated[str, Field(
        description="Name/description of the completed task or milestone",
        min_length=3,
        max_length=200,
        examples=["IA-IA Collaborative Architecture Analysis", "Phase 2.7 Implementation", "Strategy-Architect Refactoring"]
    )],
    phase_context: Annotated[Optional[str], Field(
        description="Phase or project context for the retrospective"
    )] = None,
    duration_estimate: Annotated[Optional[str], Field(
        description="How long the task took (for learning purposes)"
    )] = None
) -> str:
    """Create structured retrospective draft for knowledge capture.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - delegates to tools module.
    """
    try:
        from tools.knowledge_management import start_retrospective as km_start_retrospective
        return km_start_retrospective(task_name, phase_context, duration_estimate)
    except Exception as e:
        logger.error(f"start-retrospective delegation failed: {str(e)}")
        raise ValueError(f"start-retrospective delegation failed: {str(e)}")


@app.tool(
    name="process-retrospective", 
    description="Extract insights from completed retrospective and integrate into knowledge base"
)
def process_retrospective(
    retrospective_file: Annotated[str, Field(
        description="Path to the completed retrospective Markdown file",
        examples=[".cortex/retrospectives/2025-06-21_ia_ia_collaboration.md"]
    )]
) -> str:
    """Process completed retrospective and integrate insights into knowledge base.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - delegates to tools module.
    """
    try:
        from tools.knowledge_management import process_retrospective as km_process_retrospective
        return km_process_retrospective(retrospective_file)
    except Exception as e:
        logger.error(f"process-retrospective delegation failed: {str(e)}")
        raise ValueError(f"process-retrospective delegation failed: {str(e)}")


def main():
    """Main entry point for the CortexMCP server."""
    import sys
    import os
    
    # Configure strategy logger for MCP compatibility
    log_level = os.getenv("STRATEGY_LOG_LEVEL", "WARNING").upper()
    if log_level not in ["DEBUG", "INFO"]:
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='🤖 CortexMCP [%(asctime)s] %(levelname)s: %(message)s',
            handlers=[logging.StreamHandler(sys.stderr)]
        )
    else:
        # Disable logging in MCP mode to avoid stderr noise
        logging.basicConfig(level=logging.CRITICAL)
    
    # Only log startup info in debug/info modes
    if log_level in ["DEBUG", "INFO"]:
        logger.info("🚀 Starting CortexMCP Server v2.7.0 - Collaborative Intelligence Edition")
        logger.info(f"📊 Collaboration Mode: {os.getenv('CORTEX_COLLABORATION_MODE', 'auto')}")
        logger.info(f"🔍 Log Level: {log_level}")
    
    # Run FastMCP server
    app.run()


if __name__ == "__main__":
    main()