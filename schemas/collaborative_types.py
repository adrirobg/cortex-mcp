"""Collaborative Intelligence Types for Phase 2.7 Enhancement.

This module defines the type system for hybrid collaborative intelligence,
enabling Claude to participate actively in strategic analysis refinement
while maintaining the deterministic reliability of the Motor de Estrategias.

Key concepts:
- DelegationType: Types of delegation to Claude intelligence
- CollaborativeWorkflowStage: Extended workflow stages for collaboration
- DelegationContext: Context management for Claude interactions
- RefinementRecord: History tracking for collaborative improvements
"""

from typing import Dict, Any, List, Optional, Union, Literal
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime

from schemas.universal_response import Action  # Import existing Action type


class DelegationType(str, Enum):
    """Types of delegation to Claude for collaborative refinement."""
    REFINE_ANALYSIS = "refine_analysis"
    VALIDATE_DEPENDENCIES = "validate_dependencies"
    OPTIMIZE_ASSIGNMENT = "optimize_assignment"
    CRITICAL_REVIEW = "critical_review"
    ARCHITECTURE_ALTERNATIVES = "architecture_alternatives"


class CollaborativeWorkflowStage(str, Enum):
    """Extended workflow stages supporting collaborative intelligence."""
    # Original stages (backward compatibility)
    ANALYSIS = "analysis"
    DECOMPOSITION = "decomposition"
    TASK_GRAPH = "task_graph"
    MISSION_MAP = "mission_map"
    COMPLETE = "complete"
    
    # New collaborative stages
    PRELIMINARY_ANALYSIS = "preliminary_analysis"
    CLAUDE_REFINEMENT = "claude_refinement"
    REFINED_ANALYSIS = "refined_analysis"
    COLLABORATIVE_DECOMPOSITION = "collaborative_decomposition"
    TASK_GRAPH_OPTIMIZATION = "task_graph_optimization"
    MISSION_MAP_FINALIZATION = "mission_map_finalization"


class CollaborativeExecutionType(str, Enum):
    """Enhanced execution types including collaborative workflows."""
    IMMEDIATE = "immediate"
    USER_CONFIRMATION = "user_confirmation"
    MULTI_STEP = "multi_step"
    DELEGATED = "delegated"
    COLLABORATIVE = "collaborative"  # NEW: Multi-step with Claude interaction


class RefinementQuality(BaseModel):
    """Assessment of refinement quality and improvements."""
    improvement_score: float = Field(..., ge=0.0, le=1.0, description="Quality improvement score")
    specific_improvements: List[str] = Field(default_factory=list, description="Specific areas improved")
    confidence_increase: Optional[float] = Field(None, description="Confidence score increase")
    risk_reduction: Optional[float] = Field(None, description="Risk reduction achieved")
    

class RefinementRecord(BaseModel):
    """Record of a collaborative refinement interaction."""
    refinement_id: str = Field(..., description="Unique refinement identifier")
    delegation_type: DelegationType = Field(..., description="Type of delegation performed")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="When refinement occurred")
    
    original_data: Dict[str, Any] = Field(..., description="Original data before refinement")
    refinement_input: Dict[str, Any] = Field(..., description="Input provided to Claude")
    claude_response: Dict[str, Any] = Field(..., description="Claude's refinement response")
    integrated_result: Dict[str, Any] = Field(..., description="Final integrated result")
    
    quality_assessment: RefinementQuality = Field(..., description="Quality improvement assessment")
    duration_ms: Optional[float] = Field(None, description="Refinement duration in milliseconds")


class DelegationContext(BaseModel):
    """Context for delegating analysis refinement to Claude."""
    delegation_id: str = Field(..., description="Unique delegation identifier")
    delegation_type: DelegationType = Field(..., description="Type of delegation")
    
    preliminary_result: Dict[str, Any] = Field(..., description="Preliminary analysis result")
    refinement_prompt: str = Field(..., description="Specific prompt for Claude refinement")
    expected_improvements: List[str] = Field(default_factory=list, description="Expected improvement areas")
    
    validation_criteria: str = Field(..., description="Criteria for validating refinement quality")
    confidence_threshold: float = Field(default=0.75, ge=0.0, le=1.0, description="Confidence threshold for auto-acceptance")
    max_iterations: int = Field(default=1, ge=1, le=3, description="Maximum refinement iterations")
    
    continuation_state: Dict[str, Any] = Field(default_factory=dict, description="State for workflow continuation")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="When delegation was created")


class CollaborationConfig(BaseModel):
    """Configuration for collaborative intelligence behavior."""
    enable_collaboration: bool = Field(default=True, description="Enable collaborative workflows")
    confidence_threshold: float = Field(default=0.75, ge=0.0, le=1.0, description="Threshold for triggering collaboration")
    max_refinement_iterations: int = Field(default=2, ge=1, le=5, description="Maximum refinement iterations")
    delegation_timeout_seconds: int = Field(default=30, ge=5, le=120, description="Timeout for delegation responses")
    auto_accept_high_confidence: bool = Field(default=True, description="Auto-accept high-confidence refinements")
    
    # Feature flags for specific collaboration points
    analysis_refinement_enabled: bool = Field(default=True, description="Enable analysis refinement")
    dependency_validation_enabled: bool = Field(default=True, description="Enable dependency validation")
    resource_optimization_enabled: bool = Field(default=True, description="Enable resource optimization")


# Enhanced Action Types for Collaborative Workflows

class RefineAnalysisAction(Action):
    """Action for refining preliminary analysis with Claude intelligence."""
    type: Literal["refine_analysis"] = "refine_analysis"
    delegation_context: DelegationContext = Field(..., description="Context for analysis refinement")
    
    class Config:
        schema_extra = {
            "example": {
                "type": "refine_analysis",
                "description": "Refine preliminary project analysis with critical review",
                "priority": 1,
                "validation_criteria": "Analysis includes comprehensive technology assessment",
                "delegation_context": {
                    "delegation_id": "ref_001",
                    "delegation_type": "refine_analysis",
                    "preliminary_result": {"domain": "e-commerce", "complexity": "Media"},
                    "refinement_prompt": "Critically review this e-commerce analysis for missing patterns...",
                    "expected_improvements": ["technology_assessment", "scalability_analysis"],
                    "validation_criteria": "Refined analysis shows improved technology recommendations"
                }
            }
        }


class ValidateDependenciesAction(Action):
    """Action for validating task dependencies with Claude review."""
    type: Literal["validate_dependencies"] = "validate_dependencies"
    task_graph_data: Dict[str, Any] = Field(..., description="Task graph data for validation")
    critical_paths: List[str] = Field(..., description="Critical paths requiring validation")
    
    class Config:
        schema_extra = {
            "example": {
                "type": "validate_dependencies",
                "description": "Validate critical task dependencies and potential bottlenecks",
                "priority": 2,
                "task_graph_data": {"tasks": [], "dependencies": []},
                "critical_paths": ["authentication_setup -> api_development -> frontend_integration"]
            }
        }


class OptimizeAssignmentAction(Action):
    """Action for optimizing resource assignments with Claude insight."""
    type: Literal["optimize_assignment"] = "optimize_assignment"
    resource_assignments: List[Dict[str, Any]] = Field(..., description="Current resource assignments")
    optimization_criteria: List[str] = Field(..., description="Criteria for optimization")
    
    class Config:
        schema_extra = {
            "example": {
                "type": "optimize_assignment",
                "description": "Optimize resource assignments for maximum efficiency",
                "priority": 3,
                "resource_assignments": [{"agent": "Frontend Developer", "tasks": ["UI", "Components"]}],
                "optimization_criteria": ["minimize_handoffs", "maximize_parallel_execution"]
            }
        }


# Union type for all collaborative actions
CollaborativeAction = Union[RefineAnalysisAction, ValidateDependenciesAction, OptimizeAssignmentAction]


class CollaborativeClaudeInstructions(BaseModel):
    """Enhanced Claude instructions supporting collaborative workflows."""
    execution_type: CollaborativeExecutionType = Field(..., description="Type of execution flow")
    actions: List[Union[Action, CollaborativeAction]] = Field(..., description="Actions to execute")
    
    # Collaborative workflow support
    collaboration_stage: Optional[CollaborativeWorkflowStage] = Field(None, description="Current collaboration stage")
    active_delegation: Optional[DelegationContext] = Field(None, description="Active delegation context")
    
    # Existing fields (backward compatibility)
    context_requirements: Optional[Dict[str, Any]] = Field(None, description="Required context")
    decision_points: Optional[List[Dict[str, Any]]] = Field(None, description="Decision points")
    fallback_strategy: Optional[str] = Field(None, description="Fallback strategy")


# Export key types for easy import
__all__ = [
    "DelegationType",
    "CollaborativeWorkflowStage", 
    "CollaborativeExecutionType",
    "RefinementQuality",
    "RefinementRecord",
    "DelegationContext",
    "CollaborationConfig",
    "RefineAnalysisAction",
    "ValidateDependenciesAction",
    "OptimizeAssignmentAction",
    "CollaborativeAction",
    "CollaborativeClaudeInstructions"
]