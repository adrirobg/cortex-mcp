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
from typing import Optional, Annotated

from pydantic import Field
from mcp.server.fastmcp import FastMCP

# Configure logging
logger = logging.getLogger(__name__)

# Initialize FastMCP server
app = FastMCP("cortex-mcp", "1.0.0")


@app.tool(
    name="get-planning-template",
    description="Retrieve blank planning template structure for Claude's cognitive work"
)
def get_planning_template(
    template_name: Annotated[str, Field(
        description="Template to retrieve: 'phase_preparation', 'retrospective', etc.",
        examples=["phase_preparation", "retrospective"]
    )]
) -> str:
    """Retrieve blank planning template structure for Claude's cognitive work.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - delegates to tools module.
    """
    try:
        from tools.planning_toolkit import get_planning_template as pt_get_template
        return pt_get_template(template_name)
    except Exception as e:
        logger.error(f"get-planning-template delegation failed: {str(e)}")
        raise ValueError(f"get-planning-template delegation failed: {str(e)}")


@app.tool(
    name="save-planning-artifact",
    description="Save Claude's planning artifact to specified location"
)
def save_planning_artifact(
    file_name: Annotated[str, Field(
        description="Name of the artifact file to save",
        examples=["Phase2.8.5_Prep.json", "RetroAnalysis_2025-06-22.md"]
    )],
    file_content: Annotated[str, Field(
        description="Complete content of the artifact file"
    )],
    directory: Annotated[str, Field(
        description="Directory to save the artifact",
        default=".cortex/planning/"
    )] = ".cortex/planning/"
) -> str:
    """Save Claude's planning artifact to specified location.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - delegates to tools module.
    """
    try:
        from tools.planning_toolkit import save_planning_artifact as pt_save_artifact
        return pt_save_artifact(file_name, file_content, directory)
    except Exception as e:
        logger.error(f"save-planning-artifact delegation failed: {str(e)}")
        raise ValueError(f"save-planning-artifact delegation failed: {str(e)}")


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