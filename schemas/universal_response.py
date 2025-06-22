"""Universal Response Schema for Strategy Library MCP Server.

This module implements the core StrategyResponse schema that ALL tools must return.
Following Principio Rector #1: Dogmatismo con Universal Response Schema.
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime


class StrategyType(str, Enum):
    """Types of strategies that can be executed."""
    ANALYSIS = "analysis"
    EXECUTION = "execution"
    COORDINATION = "coordination"
    LEARNING = "learning"


class ExecutionType(str, Enum):
    """Types of execution patterns for Claude instructions."""
    IMMEDIATE = "immediate"
    USER_CONFIRMATION = "user_confirmation"
    MULTI_STEP = "multi_step"
    DELEGATED = "delegated"
    COLLABORATIVE = "collaborative"  # NEW: Multi-step with Claude interaction


class Strategy(BaseModel):
    """Strategy identification and metadata."""
    name: str = Field(..., min_length=1, description="Unique identifier for the strategy")
    version: str = Field(..., min_length=1, description="Semantic version of the strategy")
    type: StrategyType = Field(..., description="Type of strategy being executed")


class Action(BaseModel):
    """Individual action within a strategy execution."""
    type: str = Field(..., description="Type of action to perform")
    description: str = Field(..., description="Human-readable description of the action")
    priority: int = Field(..., ge=1, le=10, description="Priority level (1-10)")
    validation_criteria: Optional[str] = Field(None, description="Success criteria for this action")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Action-specific parameters")


class DecisionPoint(BaseModel):
    """Decision point requiring Claude's judgment."""
    id: str = Field(..., description="Unique identifier for the decision point")
    question: str = Field(..., description="Question to be resolved")
    options: List[Dict[str, Any]] = Field(..., description="Available options")
    recommendation: Optional[str] = Field(None, description="Recommended choice")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in recommendation")


class ContextRequirements(BaseModel):
    """Context requirements for strategy execution."""
    required_tools: Optional[List[str]] = Field(None, description="Required MCP tools")
    required_info: Optional[List[str]] = Field(None, description="Required information to gather")


class UserFacing(BaseModel):
    """User-facing communication section."""
    summary: str = Field(..., description="Summary in natural language")
    visualization: Optional[str] = Field(None, description="Optional diagrams (Mermaid/ASCII)")
    key_points: Optional[List[str]] = Field(None, description="Important points to highlight")
    next_steps: Optional[List[str]] = Field(None, description="Suggested next actions")


class ClaudeInstructions(BaseModel):
    """Instructions for Claude Code execution."""
    execution_type: ExecutionType = Field(..., description="Type of execution pattern")
    actions: List[Action] = Field(..., description="Ordered list of actions to execute")
    context_requirements: Optional[ContextRequirements] = Field(None, description="Required context")
    decision_points: Optional[List[DecisionPoint]] = Field(None, description="Decision points requiring judgment")
    fallback_strategy: Optional[str] = Field(None, description="Fallback strategy if primary fails")


class ErrorScenario(BaseModel):
    """Potential error scenario."""
    type: str = Field(..., description="Type of error")
    description: str = Field(..., description="Error description")
    probability: float = Field(..., ge=0.0, le=1.0, description="Probability of occurrence")


class RecoveryStrategy(BaseModel):
    """Recovery strategy for error handling."""
    trigger: str = Field(..., description="Error type that triggers this recovery")
    action: str = Field(..., description="Recovery action to take")
    fallback: Optional[str] = Field(None, description="Fallback if recovery fails")


class ErrorHandling(BaseModel):
    """Error handling configuration."""
    potential_errors: List[ErrorScenario] = Field(..., description="Potential error scenarios")
    recovery_strategies: List[RecoveryStrategy] = Field(..., description="Recovery strategies")


class Metadata(BaseModel):
    """Execution metadata for learning and optimization."""
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence in strategy (0-1)")
    complexity_score: int = Field(..., ge=1, le=10, description="Task complexity (1-10)")
    estimated_duration: Optional[str] = Field(None, description="Human-readable duration estimate")
    performance_hints: Optional[List[str]] = Field(None, description="Optimization suggestions")
    learning_opportunities: Optional[List[str]] = Field(None, description="Learning opportunities")


# Generic type for payload
PayloadType = TypeVar('PayloadType', bound=BaseModel)


class StrategyResponse(BaseModel, Generic[PayloadType]):
    """Universal Response Schema for all Strategy Library MCP tools.
    
    This is the core schema that ALL tools must return without exception.
    Following the Dogmatismo con Universal Response Schema principle.
    """
    
    strategy: Strategy = Field(..., description="Strategy identification")
    user_facing: UserFacing = Field(..., description="User communication")
    claude_instructions: ClaudeInstructions = Field(..., description="Claude execution instructions")
    payload: PayloadType = Field(..., description="Tool-specific structured data")
    metadata: Metadata = Field(..., description="Execution metadata")
    error_handling: Optional[ErrorHandling] = Field(None, description="Error handling configuration")
    debug_payload: Optional[Dict[str, Any]] = Field(None, description="Debug information (populated when debug_mode=true)")

    model_config = {
        "extra": "forbid",  # No additional fields allowed
        "validate_assignment": True,  # Validate on assignment
        "use_enum_values": True  # Use enum values in serialization
    }


# Base payload class for tools that don't need specific payloads
class BasePayload(BaseModel):
    """Base payload class with common fields."""
    workflow_stage: Optional[str] = Field(None, description="Current workflow stage")
    suggested_next_state: Optional[Dict[str, Any]] = Field(None, description="Suggested state for next call")
    
    model_config = {"extra": "allow"}


# ========================================
# PHASE 2.7: COLLABORATIVE ENHANCEMENTS
# ========================================

class DelegationType(str, Enum):
    """Types of delegation to Claude for collaborative refinement."""
    REFINE_ANALYSIS = "refine_analysis"
    VALIDATE_DEPENDENCIES = "validate_dependencies"
    OPTIMIZE_ASSIGNMENT = "optimize_assignment"
    CRITICAL_REVIEW = "critical_review"
    ARCHITECTURE_ALTERNATIVES = "architecture_alternatives"
    EVALUATE_OPTIONS = "evaluate_options"  # Phase 2.8.2: Domain Intelligence


class CollaborationPoint(BaseModel):
    """Definition of a point where Claude collaboration adds value."""
    point_id: str = Field(..., description="Unique identifier for collaboration point")
    stage: str = Field(..., description="Workflow stage where collaboration occurs")
    delegation_type: DelegationType = Field(..., description="Type of delegation needed")
    confidence_threshold: float = Field(default=0.75, description="Confidence threshold for triggering")
    description: str = Field(..., description="Description of collaboration value")


class DelegationContext(BaseModel):
    """Context for delegating analysis refinement to Claude."""
    delegation_id: str = Field(..., description="Unique delegation identifier")
    delegation_type: DelegationType = Field(..., description="Type of delegation")
    
    preliminary_result: Dict[str, Any] = Field(..., description="Preliminary analysis result")
    refinement_prompt: str = Field(..., description="Specific prompt for Claude refinement")
    expected_improvements: List[str] = Field(default_factory=list, description="Expected improvement areas")
    
    validation_criteria: str = Field(..., description="Criteria for validating refinement quality")
    confidence_threshold: float = Field(default=0.75, ge=0.0, le=1.0, description="Confidence threshold")
    continuation_state: Dict[str, Any] = Field(default_factory=dict, description="State for workflow continuation")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Creation timestamp")


class RefinementRecord(BaseModel):
    """Record of a collaborative refinement interaction."""
    refinement_id: str = Field(..., description="Unique refinement identifier")
    delegation_type: DelegationType = Field(..., description="Type of delegation performed")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="When refinement occurred")
    
    original_confidence: float = Field(..., description="Original confidence score")
    refined_confidence: float = Field(..., description="Post-refinement confidence score")
    quality_improvement: float = Field(..., description="Measured quality improvement")
    duration_ms: Optional[float] = Field(None, description="Refinement duration in milliseconds")


# Enhanced Action for Collaborative Workflows
class CollaborativeAction(Action):
    """Enhanced action supporting collaborative delegation."""
    # Collaborative-specific fields
    delegation_context: Optional[DelegationContext] = Field(None, description="Delegation context if applicable")
    requires_claude_input: bool = Field(default=False, description="Whether action requires Claude input")
    collaboration_stage: Optional[str] = Field(None, description="Collaboration stage identifier")


# Enhanced StrategyResponse for Collaborative Intelligence
class CollaborativeStrategyResponse(BaseModel, Generic[PayloadType]):
    """Enhanced StrategyResponse supporting collaborative intelligence workflows.
    
    Extends the Universal Response Schema with Phase 2.7 collaborative capabilities
    while maintaining 100% backward compatibility.
    """
    
    # Core Universal Response Schema (unchanged for compatibility)
    strategy: Strategy = Field(..., description="Strategy identification")
    user_facing: UserFacing = Field(..., description="User communication")
    claude_instructions: ClaudeInstructions = Field(..., description="Claude execution instructions")
    payload: PayloadType = Field(..., description="Tool-specific structured data")
    metadata: Metadata = Field(..., description="Execution metadata")
    error_handling: Optional[ErrorHandling] = Field(None, description="Error handling configuration")
    debug_payload: Optional[Dict[str, Any]] = Field(None, description="Debug information")
    
    # NEW: Collaborative Intelligence Extensions (Phase 2.7)
    collaboration_mode: bool = Field(default=False, description="Whether collaborative mode is active")
    delegation_context: Optional[DelegationContext] = Field(None, description="Active delegation context")
    collaboration_points: Optional[List[CollaborationPoint]] = Field(None, description="Available collaboration points")
    refinement_history: Optional[List[RefinementRecord]] = Field(None, description="History of refinements")
    
    # Workflow continuation support
    requires_claude_refinement: bool = Field(default=False, description="Whether Claude refinement is needed")
    collaboration_stage: Optional[str] = Field(None, description="Current collaboration stage")
    
    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True
    }


# Type alias for backward compatibility
# Existing code can continue using StrategyResponse
# New collaborative code can use CollaborativeStrategyResponse
EnhancedStrategyResponse = CollaborativeStrategyResponse