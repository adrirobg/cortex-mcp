"""Universal Response Schema for Strategy Library MCP Server.

This module implements the core StrategyResponse schema that ALL tools must return.
Following Principio Rector #1: Dogmatismo con Universal Response Schema.
"""

from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from pydantic import BaseModel, Field
from enum import Enum


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