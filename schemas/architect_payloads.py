"""Architect-specific payload schemas for Strategy Library MCP Server.

These schemas define the structured data returned by the strategy-architect tool.
Following the Universal Response Schema pattern with strict Pydantic validation.
"""

from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from enum import Enum


class WorkflowStage(str, Enum):
    """Stages of the architect workflow."""
    ANALYSIS = "analysis"
    DECOMPOSITION = "decomposition"
    TASK_GRAPH = "task_graph"
    MISSION_MAP = "mission_map"
    COMPLETE = "complete"
    READY_FOR_EXECUTION = "ready_for_execution"
    CLARIFICATION_NEEDED = "clarification_needed"


class StageCompletionStatus(str, Enum):
    """Completion status for workflow stages."""
    COMPLETED = "completed"
    PARTIAL = "partial" 
    ERROR = "error"


class DomainAnalysisContext(BaseModel):
    """Context information from domain analysis."""
    detected_keywords: Dict[str, List[str]] = Field(..., description="Keywords detected per domain")
    technology_indicators: List[str] = Field(..., description="Technology stack indicators found")
    complexity_assessment: str = Field(..., description="Complexity level assessment")
    confidence_breakdown: Dict[str, float] = Field(..., description="Confidence scores per domain")


class DomainOption(BaseModel):
    """Domain classification option with confidence and evidence."""
    domain_id: str = Field(..., description="Domain identifier")
    domain_name: str = Field(..., description="Human-readable domain name")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")
    supporting_evidence: List[str] = Field(..., description="Evidence supporting this classification")
    potential_concerns: List[str] = Field(default=[], description="Potential concerns or limitations")


class AnalysisResult(BaseModel):
    """Result of project analysis phase with enhanced domain intelligence."""
    keywords: List[str] = Field(..., description="Extracted keywords from project description")
    patterns: List[str] = Field(..., description="Identified project patterns")
    complexity: str = Field(..., description="Assessed complexity level")
    requirements_implicit: List[str] = Field(..., description="Implicit requirements discovered")
    domain: Optional[str] = Field(None, description="Project domain classification")
    technology_stack: Optional[List[str]] = Field(None, description="Suggested technology stack")
    
    # Phase 2.8.2: Domain Intelligence Enhancement
    domain_analysis_context: Optional[DomainAnalysisContext] = Field(None, description="Multi-dimensional domain analysis context")
    domain_confidence_scores: Optional[Dict[str, float]] = Field(None, description="Confidence scores for each domain")
    recommended_domain: Optional[str] = Field(None, description="Recommended domain based on analysis")
    domain_decision_rationale: Optional[str] = Field(None, description="Rationale for domain decision")


class Phase(BaseModel):
    """Individual phase in project decomposition."""
    id: str = Field(..., description="Unique phase identifier")
    name: str = Field(..., description="Phase name")
    description: str = Field(..., description="Phase description")
    estimated_duration: Optional[str] = Field(None, description="Estimated time to complete")
    dependencies: List[str] = Field(default=[], description="Phase dependencies (phase IDs)")
    deliverables: List[str] = Field(default=[], description="Expected deliverables")


class Task(BaseModel):
    """Individual task within a phase."""
    id: str = Field(..., description="Unique task identifier")
    name: str = Field(..., description="Task name")
    description: str = Field(..., description="Detailed task description")
    phase_id: str = Field(..., description="Parent phase ID")
    dependencies: List[str] = Field(default=[], description="Task dependencies (task IDs)")
    estimated_effort: Optional[str] = Field(None, description="Estimated effort")
    complexity_score: Optional[int] = Field(None, ge=1, le=10, description="Complexity rating")
    agent_profile: Optional[str] = Field(None, description="Suggested agent profile")
    artifacts_output: List[str] = Field(default=[], description="Expected output artifacts")
    validation_criteria: List[str] = Field(default=[], description="Success criteria")
    human_checkpoint: bool = Field(default=False, description="Requires human review")


class DecompositionResult(BaseModel):
    """Result of project decomposition phase."""
    phases: List[Phase] = Field(..., description="Project phases")
    total_estimated_duration: Optional[str] = Field(None, description="Total project duration estimate")
    critical_path: Optional[List[str]] = Field(None, description="Critical path phase IDs")
    parallel_opportunities: Optional[List[List[str]]] = Field(None, description="Phases that can run in parallel")


class TaskGraphResult(BaseModel):
    """Result of task graph generation."""
    tasks: List[Task] = Field(..., description="All project tasks")
    task_count: int = Field(..., description="Total number of tasks")
    dependency_matrix: Optional[Dict[str, List[str]]] = Field(None, description="Task dependency mapping")
    critical_path: Optional[List[str]] = Field(None, description="Critical path task IDs")
    parallel_tasks: Optional[List[List[str]]] = Field(None, description="Tasks that can run in parallel")
    bottlenecks: Optional[List[str]] = Field(None, description="Potential bottleneck tasks")


class ResourceAssignment(BaseModel):
    """Resource assignment for mission map."""
    task_id: str = Field(..., description="Task ID")
    agent_profile: str = Field(..., description="Assigned agent profile")
    estimated_effort: str = Field(..., description="Effort estimate")
    priority: int = Field(..., ge=1, le=10, description="Priority level")
    parallel_group: Optional[str] = Field(None, description="Parallel execution group")


class MissionMapResult(BaseModel):
    """Result of mission map creation."""
    resource_assignments: List[ResourceAssignment] = Field(..., description="Task assignments")
    execution_order: List[str] = Field(..., description="Recommended execution order")
    parallel_groups: Optional[Dict[str, List[str]]] = Field(None, description="Parallel execution groups")
    total_effort_estimate: Optional[str] = Field(None, description="Total effort estimate")
    resource_utilization: Optional[Dict[str, str]] = Field(None, description="Resource utilization plan")


class ArchitectDiagrams(BaseModel):
    """Diagrams generated by the architect."""
    hierarchy_diagram: Optional[str] = Field(None, description="Project hierarchy (Mermaid)")
    task_graph_diagram: Optional[str] = Field(None, description="Task dependencies (Mermaid)")
    dependency_matrix: Optional[str] = Field(None, description="Dependency matrix (ASCII)")
    timeline_diagram: Optional[str] = Field(None, description="Project timeline (Mermaid)")


class ArchitectPayload(BaseModel):
    """Complete payload for strategy-architect tool responses."""
    
    # Workflow state
    workflow_stage: WorkflowStage = Field(..., description="Current workflow stage")
    
    # Accumulated results from each stage
    analysis: Optional[AnalysisResult] = Field(None, description="Analysis phase results")
    decomposition: Optional[DecompositionResult] = Field(None, description="Decomposition phase results")
    task_graph: Optional[TaskGraphResult] = Field(None, description="Task graph results")
    mission_map: Optional[MissionMapResult] = Field(None, description="Mission map results")
    
    # Implementation order for multi-step execution
    implementation_order: Optional[List[str]] = Field(None, description="Recommended implementation order")
    
    # State management (for Claude to maintain context)
    suggested_next_state: Optional[Dict[str, Any]] = Field(None, description="Suggested state for next call")
    
    # Generated visualizations
    diagrams: Optional[ArchitectDiagrams] = Field(None, description="Generated diagrams and visualizations")
    
    # Execution metadata
    continue_workflow: Optional[bool] = Field(None, description="Whether workflow should continue")
    next_step: Optional[str] = Field(None, description="Next step to execute")
    estimated_completion: Optional[str] = Field(None, description="Estimated completion time")
    
    # Phase 2.8.1: Stage-based execution enhancements
    current_stage: Optional[str] = Field(None, description="String indicating which stage was executed")
    stage_completion_status: Optional[StageCompletionStatus] = Field(None, description="Completion status of the current stage")
    next_stage_requirements: Optional[List[str]] = Field(None, description="List of required inputs for next stage")
    
    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True
    }