"""Collaborative Strategy-Architect for Phase 2.7.

This module provides the enhanced strategy-architect interface that supports
hybrid collaborative intelligence workflows while maintaining 100% backward
compatibility with the existing deterministic Motor de Estrategias.

Key Features:
- Hybrid collaborative intelligence (Claude + deterministic analysis)
- Intelligent collaboration point detection
- Seamless workflow continuation
- Backward compatibility with existing API
- Enhanced analysis quality through Claude refinement
"""

import os
from typing import Optional, Dict, Any
from schemas.universal_response import CollaborativeStrategyResponse
from schemas.architect_payloads import ArchitectPayload
from tools.collaborative.workflow_controller import CollaborativeWorkflowController
from utils.logger import strategy_logger, generate_trace_id


def execute_architect_workflow(
    task_description: str,
    analysis_result: Optional[Dict[str, Any]] = None,
    decomposition_result: Optional[Dict[str, Any]] = None,
    workflow_stage: Optional[str] = None,
    refined_analysis: Optional[Dict[str, Any]] = None,
    trace_id: Optional[str] = None,
    debug_mode: bool = False
) -> CollaborativeStrategyResponse[ArchitectPayload]:
    """Execute unified strategy-architect workflow with collaborative intelligence.
    
    This is the unified entry point for CortexMCP strategy-architect that always
    uses collaborative intelligence. Traditional workflow system has been eliminated
    in Phase 2.8.4-Prep consolidation.
    
    Args:
        task_description: Project description to analyze
        analysis_result: Previous analysis results (for workflow continuation)
        decomposition_result: Previous decomposition results (for continuation) 
        workflow_stage: Specific stage to execute
        refined_analysis: Claude-refined analysis (for collaboration continuation)
        trace_id: Optional trace ID for request correlation
        debug_mode: Enable debug information in response
        
    Returns:
        CollaborativeStrategyResponse with workflow results and collaboration context
        
    Raises:
        ValueError: If task_description is empty or parameters are invalid
    """
    # Initialize trace ID
    if not trace_id:
        trace_id = generate_trace_id()
    
    # Validate input
    if not task_description or not task_description.strip():
        strategy_logger.error(
            "workflow_validation_failed", 
            "Empty task description", 
            trace_id=trace_id
        )
        raise ValueError("task_description cannot be empty")
    
    # Always use collaborative intelligence (Phase 2.8.4-Prep consolidation)
    collaboration_enabled = True
    
    # Log workflow initiation
    strategy_logger.info(
        "unified_architect_initiated",
        f"Unified strategy-architect initiated with collaborative intelligence",
        trace_id=trace_id,
        context={
            "collaboration_enabled": collaboration_enabled,
            "stage": workflow_stage or "auto_detect",
            "has_refined_analysis": bool(refined_analysis)
        }
    )
    
    try:
        # Initialize collaborative workflow controller
        controller = CollaborativeWorkflowController(
            collaboration_enabled=collaboration_enabled,
            confidence_threshold=0.75
        )
        
        # Execute collaborative workflow
        result = controller.execute_collaborative_workflow(
            task_description=task_description,
            analysis_result=analysis_result,
            decomposition_result=decomposition_result,
            workflow_stage=workflow_stage,
            refined_analysis=refined_analysis,
            trace_id=trace_id,
            debug_mode=debug_mode
        )
        
        # Log successful completion
        strategy_logger.info(
            "unified_architect_completed",
            f"Unified strategy-architect completed: {result.collaboration_stage or 'collaborative'}",
            trace_id=trace_id,
            context={
                "collaboration_used": result.collaboration_mode,
                "requires_refinement": result.requires_claude_refinement,
                "workflow_stage": result.payload.workflow_stage.value if hasattr(result.payload.workflow_stage, 'value') else str(result.payload.workflow_stage) if result.payload.workflow_stage else None
            }
        )
        
        return result
        
    except Exception as e:
        strategy_logger.error(
            "collaborative_architect_error",
            f"Enhanced strategy-architect failed: {str(e)}",
            trace_id=trace_id,
            exception=e
        )
        raise


# Function eliminated in Phase 2.8.4-Prep consolidation
# Collaboration is now always enabled


# Backward compatibility wrapper
def execute_architect_workflow_enhanced(
    task_description: str,
    analysis_result: Optional[Dict[str, Any]] = None,
    decomposition_result: Optional[Dict[str, Any]] = None,
    workflow_stage: Optional[str] = None,
    trace_id: Optional[str] = None,
    debug_mode: bool = False
) -> CollaborativeStrategyResponse[ArchitectPayload]:
    """Backward-compatible wrapper for enhanced strategy-architect.
    
    This function provides the same interface as the original strategy-architect
    but with enhanced collaborative capabilities. Existing code can use this
    as a drop-in replacement.
    
    Args:
        task_description: Project description to analyze
        analysis_result: Previous analysis results (for workflow continuation)
        decomposition_result: Previous decomposition results (for continuation)
        workflow_stage: Specific stage to execute
        trace_id: Optional trace ID for request correlation
        debug_mode: Enable debug information in response
        
    Returns:
        CollaborativeStrategyResponse (backward compatible with StrategyResponse)
    """
    return execute_architect_workflow(
        task_description=task_description,
        analysis_result=analysis_result,
        decomposition_result=decomposition_result,
        workflow_stage=workflow_stage,
        refined_analysis=None,
        trace_id=trace_id,
        debug_mode=debug_mode
    )


# Export main functions
__all__ = [
    "execute_architect_workflow",
    "execute_architect_workflow_enhanced"
]