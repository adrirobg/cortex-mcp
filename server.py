#!/usr/bin/env python3
"""CortexMCP Server.

A Model Context Protocol server providing strategic cognition capabilities
for Claude Code. Uses official FastMCP framework.

"""

import json
import logging
from typing import Optional, Annotated, Dict

from pydantic import Field
from mcp.server.fastmcp import FastMCP

# Import BaseTool classes for direct instantiation
from tools.planning_toolkit import PlanningTemplateTool, PlanningArtifactTool
from tools.knowledge_management import RetrospectiveTool, KnowledgeIntegrationTool
from tools.task_planning import (
    KeymakerWorkflowTool,
    ComplexityScoreTool,
    ReasoningTemplateTool,
    MissionMapTool,
    TaskDirectivesTool,
    LibraryChecklistTool
)

# Import prompt functions for native MCP prompts
from prompts.planning_prompts import phase_preparation_simple_prompt

# Configure logging
logger = logging.getLogger(__name__)

# Initialize FastMCP server with prompts capability
app = FastMCP("cortex-mcp", "1.0.0")


@app.tool(
    name="get-planning-template",
    description="Retrieve blank planning template structure for Claude's cognitive work"
)
async def get_planning_template(
    template_name: Annotated[str, Field(
        description="Template to retrieve: 'phase_preparation', 'retrospective', etc.",
        examples=["phase_preparation", "retrospective"]
    )]
) -> Dict:
    """Retrieve blank planning template structure for Claude's cognitive work.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - uses BaseTool directly.
    """
    tool = PlanningTemplateTool()
    return await tool.validate_and_execute(template_name=template_name)


@app.tool(
    name="save-planning-artifact",
    description="Save Claude's planning artifact to specified location"
)
async def save_planning_artifact(
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
) -> Dict:
    """Save Claude's planning artifact to specified location.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - uses BaseTool directly.
    """
    tool = PlanningArtifactTool()
    return await tool.validate_and_execute(
        file_name=file_name,
        file_content=file_content,
        directory=directory
    )


@app.tool(
    name="start-retrospective",
    description="Create structured retrospective draft for knowledge capture and analysis"
)
async def start_retrospective(
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
) -> Dict:
    """Create structured retrospective draft for knowledge capture.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - uses BaseTool directly.
    """
    tool = RetrospectiveTool()
    return await tool.validate_and_execute(
        task_name=task_name,
        phase_context=phase_context,
        duration_estimate=duration_estimate
    )


@app.tool(
    name="process-retrospective", 
    description="Extract insights from completed retrospective and integrate into knowledge base"
)
async def process_retrospective(
    retrospective_file: Annotated[str, Field(
        description="Path to the completed retrospective Markdown file",
        examples=[".cortex/retrospectives/2025-06-21_ia_ia_collaboration.md"]
    )]
) -> Dict:
    """Process completed retrospective and integrate insights into knowledge base.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - uses BaseTool directly.
    """
    tool = KnowledgeIntegrationTool()
    return await tool.validate_and_execute(retrospective_file=retrospective_file)


# ========================================
# KEYMAKER TASK PLANNING TOOLS
# Following Principio Rector #2: Servidor como Ejecutor Fiable
# ========================================

@app.tool(
    name="get-keymaker-workflow",
    description="Retrieve structured workflow template for task planning automation"
)
async def get_keymaker_workflow() -> Dict:
    """Pure delegation to KeymakerWorkflowTool."""
    tool = KeymakerWorkflowTool()
    return await tool.validate_and_execute()


@app.tool(
    name="calculate-complexity-score",
    description="Calculate Task Complexity Score (TCS) to determine planning strategy"
)
async def calculate_complexity_score(
    task_description: Annotated[str, Field(
        description="Description of the task to analyze for complexity"
    )]
) -> Dict:
    """Pure delegation to ComplexityScoreTool."""
    tool = ComplexityScoreTool()
    return await tool.validate_and_execute(task_description=task_description)


@app.tool(
    name="get-reasoning-template",
    description="Retrieve Chain-of-Thought (CoT) or Tree-of-Thoughts (ToT) reasoning template"
)
async def get_reasoning_template(
    strategy_type: Annotated[str, Field(
        description="Type of reasoning strategy: 'cot' or 'tot'"
    )]
) -> Dict:
    """Pure delegation to ReasoningTemplateTool."""
    tool = ReasoningTemplateTool()
    return await tool.validate_and_execute(strategy_type=strategy_type)


@app.tool(
    name="save-mission-map",
    description="Save and validate structured mission map for task execution"
)
async def save_mission_map(
    task_id: Annotated[str, Field(
        description="Unique identifier for the task"
    )],
    mission_content: Annotated[str, Field(
        description="JSON content of the mission map"
    )]
) -> Dict:
    """Pure delegation to MissionMapTool."""
    tool = MissionMapTool()
    return await tool.validate_and_execute(
        task_id=task_id,
        mission_content=mission_content
    )


@app.tool(
    name="generate-task-directives",
    description="Generate task-specific Do's and Don'ts from mission map analysis"
)
async def generate_task_directives(
    mission_map_path: Annotated[str, Field(
        description="Path to the mission map JSON file"
    )]
) -> Dict:
    """Pure delegation to TaskDirectivesTool."""
    tool = TaskDirectivesTool()
    return await tool.validate_and_execute(mission_map_path=mission_map_path)


@app.tool(
    name="generate-library-checklist",
    description="Generate Context7 library documentation checklist from mission map"
)
async def generate_library_checklist(
    mission_map_path: Annotated[str, Field(
        description="Path to the mission map JSON file"
    )]
) -> Dict:
    """Pure delegation to LibraryChecklistTool."""
    tool = LibraryChecklistTool()
    return await tool.validate_and_execute(mission_map_path=mission_map_path)


# ========================================
# EXPERIMENTAL: MCP NATIVE PROMPTS
# Research & MVP comparing prompts vs templates
# Following Principio Rector #2: Servidor como Ejecutor Fiable
# ========================================

@app.prompt(
    name="phase-preparation-simple",
    description="Generate a simple phase preparation plan using native MCP prompts"
)
def phase_preparation_simple(
    phase_name: Annotated[str, Field(
        description="Name of the phase to prepare",
        examples=["Phase 2.8.6", "Database Migration"]
    )],
    project_context: Annotated[str, Field(
        description="Context of the project or current situation", 
        examples=["CortexMCP Enhancement", "User Authentication System"]
    )],
    priority: Annotated[str, Field(
        description="Priority level for the phase",
        default="medium"
    )] = "medium",
    duration_hours: Annotated[int, Field(
        description="Estimated duration in hours",
        default=8
    )] = 8
) -> Dict:
    """Experimental native MCP prompt for phase preparation.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - delegates to prompt function.
    This is a research experiment to compare native MCP prompts vs PlanningTemplateTool.
    """
    return phase_preparation_simple_prompt(
        phase_name=phase_name,
        project_context=project_context,
        priority=priority,
        duration_hours=duration_hours
    )


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