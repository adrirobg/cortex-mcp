"""Strategy-Architect Integration Module - Phase 2.5 Implementation.

This module orchestrates the complete 4-phase Motor de Estrategias workflow:
analyze_project → decompose_phases → generate_task_graph → create_mission_map

Implements the unified strategy-architect MCP tool interface, replacing mock responses
with actual strategic cognition capabilities.

Following Principios Rectores:
1. Dogmatismo con Universal Response Schema - strict StrategyResponse validation
2. Servidor como Ejecutor Fiable - deterministic workflow orchestration
3. Estado en Claude, NO en Servidor - stateless design with workflow continuation
4. Testing Concurrente - comprehensive integration testing
"""

from typing import Optional, Dict, Any, List
from schemas.universal_response import (
    StrategyResponse, Strategy, StrategyType, UserFacing, ClaudeInstructions, 
    ExecutionType, Action, Metadata
)
from schemas.architect_payloads import (
    ArchitectPayload, WorkflowStage, AnalysisResult, DecompositionResult,
    TaskGraphResult, MissionMapResult, ArchitectDiagrams
)
from tools.architect.analyze_project import analyze_project
from tools.architect.decompose_phases import decompose_phases
from tools.architect.task_graph import generate_task_graph
from tools.architect.mission_map import create_mission_map
from utils.logger import strategy_logger, generate_trace_id


def execute_architect_workflow(
    task_description: str,
    analysis_result: Optional[Dict[str, Any]] = None,
    decomposition_result: Optional[Dict[str, Any]] = None,
    workflow_stage: Optional[str] = None,
    trace_id: Optional[str] = None,
    debug_mode: bool = False
) -> StrategyResponse[ArchitectPayload]:
    """Orchestrate complete 4-phase Motor de Estrategias workflow.
    
    Executes deterministic sequence: Analysis → Decomposition → Task Graph → Mission Map
    Supports stateless workflow continuation via suggested_next_state pattern.
    
    Args:
        task_description: Project description to analyze
        analysis_result: Previous analysis results (for workflow continuation)
        decomposition_result: Previous decomposition results (for continuation)
        workflow_stage: Specific stage to execute ("analysis", "decomposition", "task_graph", "mission_map")
        trace_id: Optional trace ID for request correlation (auto-generated if not provided)
        debug_mode: Enable debug payload population with intermediate results
        
    Returns:
        StrategyResponse[ArchitectPayload] with complete workflow results and continuation state
        
    Raises:
        ValueError: If task_description is empty or workflow parameters invalid
    """
    # Initialize trace ID for request correlation
    if not trace_id:
        trace_id = generate_trace_id()
    
    if not task_description or not task_description.strip():
        strategy_logger.error("workflow_validation_failed", "Empty task description", trace_id=trace_id)
        raise ValueError("task_description cannot be empty")
    
    # Log workflow start
    strategy_logger.info("workflow_started", f"Motor de Estrategias initiated", trace_id=trace_id, 
                        context={"stage": workflow_stage or "complete"})
    
    try:
        # Detect workflow stage and execute appropriate phases
        stage, results = _detect_and_execute_workflow_stage(
            task_description, analysis_result, decomposition_result, workflow_stage
        )
        
        # Extract individual results
        analysis = results.get("analysis")
        decomposition = results.get("decomposition") 
        task_graph = results.get("task_graph")
        mission_map = results.get("mission_map")
        
        # Determine next workflow state
        suggested_next_state, continue_workflow, next_step = _calculate_workflow_state(
            stage, analysis, decomposition, task_graph, mission_map
        )
        
        # Generate user-facing summary and visualizations
        user_facing = _generate_user_facing_content(stage, results, task_description)
        
        # Generate Claude execution instructions
        claude_instructions = _generate_claude_instructions(stage, continue_workflow, next_step)
        
        # Create ArchitectPayload
        payload = ArchitectPayload(
            workflow_stage=stage,
            analysis=analysis,
            decomposition=decomposition,
            task_graph=task_graph,
            mission_map=mission_map,
            suggested_next_state=suggested_next_state,
            continue_workflow=continue_workflow,
            next_step=next_step,
            estimated_completion=_estimate_completion_time(mission_map, task_graph)
        )
        
        # Create strategy metadata
        strategy = Strategy(
            name="motor-de-estrategias",
            version="2.5.0",
            type=StrategyType.ANALYSIS
        )
        
        # Generate metadata
        metadata = Metadata(
            confidence_score=_calculate_confidence_score(stage, results),
            complexity_score=_calculate_complexity_score(analysis),
            estimated_duration=_estimate_completion_time(mission_map, task_graph),
            learning_opportunities=_identify_learning_opportunities(stage, results)
        )
        
        # Generate debug payload if requested
        debug_payload = None
        if debug_mode:
            debug_payload = {
                "trace_id": trace_id,
                "workflow_stage": stage.value,
                "intermediate_results": {
                    "analysis_summary": analysis.domain if analysis else None,
                    "decomposition_phases": len(decomposition.phases) if decomposition else 0,
                    "task_count": task_graph.task_count if task_graph else 0,
                    "resource_assignments": len(mission_map.resource_assignments) if mission_map else 0
                },
                "execution_context": {
                    "input_stage": workflow_stage,
                    "continued_from": bool(analysis_result or decomposition_result)
                }
            }
        
        # Log workflow completion
        strategy_logger.info("workflow_completed", f"Motor de Estrategias completed: {stage.value}", 
                           trace_id=trace_id, context={"stages": len([k for k in results.keys()]), "debug_mode": debug_mode})
        
        return StrategyResponse[ArchitectPayload](
            strategy=strategy,
            user_facing=user_facing,
            claude_instructions=claude_instructions,
            payload=payload,
            metadata=metadata,
            debug_payload=debug_payload
        )
        
    except Exception as e:
        strategy_logger.error("workflow_error", f"Workflow failed: {str(e)}", trace_id=trace_id, exception=e)
        raise


def _detect_and_execute_workflow_stage(
    task_description: str,
    analysis_result: Optional[Dict[str, Any]],
    decomposition_result: Optional[Dict[str, Any]], 
    workflow_stage: Optional[str]
) -> tuple[WorkflowStage, Dict[str, Any]]:
    """Detect workflow stage and execute appropriate phases.
    
    Returns:
        Tuple of (workflow_stage, results_dict)
    """
    results = {}
    
    # Convert previous results to objects if provided
    analysis = None
    if analysis_result:
        analysis = AnalysisResult(**analysis_result)
        results["analysis"] = analysis
    
    decomposition = None    
    if decomposition_result:
        decomposition = DecompositionResult(**decomposition_result)
        results["decomposition"] = decomposition
    
    # Determine what stage to execute
    if workflow_stage:
        # Explicit stage specified
        if workflow_stage == "analysis":
            analysis = analyze_project(task_description)
            results["analysis"] = analysis
            return WorkflowStage.ANALYSIS, results
            
        elif workflow_stage == "decomposition":
            if not analysis:
                analysis = analyze_project(task_description)
                results["analysis"] = analysis
            decomposition = decompose_phases(analysis)
            results["decomposition"] = decomposition
            return WorkflowStage.DECOMPOSITION, results
            
        elif workflow_stage == "task_graph":
            if not analysis:
                analysis = analyze_project(task_description)
                results["analysis"] = analysis
            if not decomposition:
                decomposition = decompose_phases(analysis)
                results["decomposition"] = decomposition
            task_graph = generate_task_graph(decomposition, analysis)
            results["task_graph"] = task_graph
            return WorkflowStage.TASK_GRAPH, results
            
        elif workflow_stage == "mission_map":
            if not analysis:
                analysis = analyze_project(task_description)
                results["analysis"] = analysis
            if not decomposition:
                decomposition = decompose_phases(analysis)
                results["decomposition"] = decomposition
            if "task_graph" not in results:
                task_graph = generate_task_graph(decomposition, analysis)
                results["task_graph"] = task_graph
            else:
                task_graph = results["task_graph"]
            mission_map = create_mission_map(task_graph, analysis)
            results["mission_map"] = mission_map
            return WorkflowStage.MISSION_MAP, results
    
    else:
        # Auto-detect stage based on provided inputs
        if not analysis_result:
            # Start from beginning - execute complete workflow
            analysis = analyze_project(task_description)
            results["analysis"] = analysis
            
            decomposition = decompose_phases(analysis)
            results["decomposition"] = decomposition
            
            task_graph = generate_task_graph(decomposition, analysis)
            results["task_graph"] = task_graph
            
            mission_map = create_mission_map(task_graph, analysis)
            results["mission_map"] = mission_map
            
            return WorkflowStage.COMPLETE, results
            
        elif not decomposition_result:
            # Continue from decomposition
            decomposition = decompose_phases(analysis)
            results["decomposition"] = decomposition
            
            task_graph = generate_task_graph(decomposition, analysis)
            results["task_graph"] = task_graph
            
            mission_map = create_mission_map(task_graph, analysis)
            results["mission_map"] = mission_map
            
            return WorkflowStage.COMPLETE, results
            
        else:
            # Continue from task_graph and mission_map
            task_graph = generate_task_graph(decomposition, analysis)
            results["task_graph"] = task_graph
            
            mission_map = create_mission_map(task_graph, analysis)
            results["mission_map"] = mission_map
            
            return WorkflowStage.COMPLETE, results


def _calculate_workflow_state(
    stage: WorkflowStage,
    analysis: Optional[AnalysisResult],
    decomposition: Optional[DecompositionResult],
    task_graph: Optional[TaskGraphResult],
    mission_map: Optional[MissionMapResult]
) -> tuple[Optional[Dict[str, Any]], Optional[bool], Optional[str]]:
    """Calculate suggested next state for workflow continuation."""
    
    if stage == WorkflowStage.COMPLETE:
        return None, False, None
    
    suggested_state = {
        "task_description": "continue_workflow",
        "workflow_stage": None,
        "continue_workflow": True
    }
    
    if analysis:
        suggested_state["analysis_result"] = analysis.model_dump()
    if decomposition:
        suggested_state["decomposition_result"] = decomposition.model_dump()
    
    # Determine next step
    if stage == WorkflowStage.ANALYSIS:
        suggested_state["workflow_stage"] = "decomposition"
        return suggested_state, True, "decompose_phases"
    elif stage == WorkflowStage.DECOMPOSITION:
        suggested_state["workflow_stage"] = "task_graph"
        return suggested_state, True, "generate_task_graph"
    elif stage == WorkflowStage.TASK_GRAPH:
        suggested_state["workflow_stage"] = "mission_map"
        return suggested_state, True, "create_mission_map"
    else:
        return None, False, None


def _generate_user_facing_content(
    stage: WorkflowStage, 
    results: Dict[str, Any], 
    task_description: str
) -> UserFacing:
    """Generate user-facing summary and visualization."""
    
    if stage == WorkflowStage.COMPLETE:
        summary = f"✅ Complete strategic analysis completed for: {task_description[:100]}..."
        
        # Extract key metrics
        analysis = results.get("analysis")
        decomposition = results.get("decomposition")
        task_graph = results.get("task_graph") 
        mission_map = results.get("mission_map")
        
        key_points = []
        if analysis:
            key_points.append(f"🎯 Domain: {analysis.domain or 'General'}")
            key_points.append(f"📊 Complexity: {analysis.complexity}")
        if decomposition:
            key_points.append(f"⏱️ Duration: {decomposition.total_estimated_duration}")
            key_points.append(f"🔗 Phases: {len(decomposition.phases)}")
        if task_graph:
            key_points.append(f"📋 Tasks: {task_graph.task_count}")
        if mission_map:
            key_points.append(f"👥 Resources: {len(mission_map.resource_assignments)} assignments")
        
        next_steps = [
            "Review the complete strategic plan",
            "Begin execution with the mission map",
            "Monitor progress through task dependencies"
        ]
        
    else:
        stage_names = {
            WorkflowStage.ANALYSIS: "Project Analysis",
            WorkflowStage.DECOMPOSITION: "Phase Decomposition", 
            WorkflowStage.TASK_GRAPH: "Task Graph Generation",
            WorkflowStage.MISSION_MAP: "Mission Map Creation"
        }
        
        summary = f"📋 {stage_names.get(stage, 'Workflow')} completed for: {task_description[:100]}..."
        key_points = [f"Completed {stage.value} phase"]
        next_steps = ["Continue to next workflow stage"]
    
    return UserFacing(
        summary=summary,
        key_points=key_points,
        next_steps=next_steps
    )


def _generate_claude_instructions(
    stage: WorkflowStage, 
    continue_workflow: Optional[bool], 
    next_step: Optional[str]
) -> ClaudeInstructions:
    """Generate execution instructions for Claude."""
    
    if continue_workflow and next_step:
        execution_type = ExecutionType.MULTI_STEP
        actions = [
            Action(
                type="continue_workflow",
                description=f"Continue Motor de Estrategias workflow to {next_step}",
                priority=1,
                validation_criteria="Workflow stage completed successfully"
            )
        ]
    else:
        execution_type = ExecutionType.USER_CONFIRMATION
        actions = [
            Action(
                type="review_results",
                description="Review complete strategic analysis results",
                priority=1,
                validation_criteria="Strategic plan validated and approved"
            )
        ]
    
    return ClaudeInstructions(
        execution_type=execution_type,
        actions=actions
    )


def _calculate_confidence_score(stage: WorkflowStage, results: Dict[str, Any]) -> float:
    """Calculate confidence score based on workflow completeness."""
    stage_weights = {
        WorkflowStage.ANALYSIS: 0.25,
        WorkflowStage.DECOMPOSITION: 0.50,
        WorkflowStage.TASK_GRAPH: 0.75,
        WorkflowStage.MISSION_MAP: 0.90,
        WorkflowStage.COMPLETE: 1.0
    }
    return stage_weights.get(stage, 0.5)


def _calculate_complexity_score(analysis: Optional[AnalysisResult]) -> int:
    """Calculate complexity score from analysis results."""
    if not analysis:
        return 5
    
    complexity_map = {
        "Baja": 3,
        "Media": 5, 
        "Alta": 8
    }
    return complexity_map.get(analysis.complexity, 5)


def _estimate_completion_time(
    mission_map: Optional[MissionMapResult], 
    task_graph: Optional[TaskGraphResult]
) -> Optional[str]:
    """Estimate completion time from mission map or task graph."""
    if mission_map and mission_map.total_effort_estimate:
        return mission_map.total_effort_estimate
    return None


def _identify_learning_opportunities(stage: WorkflowStage, results: Dict[str, Any]) -> Optional[List[str]]:
    """Identify learning opportunities based on workflow results."""
    opportunities = []
    
    analysis = results.get("analysis")
    if analysis and analysis.technology_stack:
        for tech in analysis.technology_stack:
            opportunities.append(f"Technology deep-dive: {tech}")
    
    decomposition = results.get("decomposition")
    if decomposition and decomposition.parallel_opportunities:
        opportunities.append("Parallel execution optimization techniques")
    
    task_graph = results.get("task_graph")
    if task_graph and task_graph.bottlenecks:
        opportunities.append("Bottleneck analysis and resolution strategies")
    
    return opportunities if opportunities else None