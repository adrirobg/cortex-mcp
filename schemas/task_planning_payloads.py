"""Task Planning payload schemas for Keymaker Suite Implementation.

Payloads for the 6 task planning tools following CortexMCP patterns.
All payloads inherit from BasePayload and follow the established
patterns from planning_payloads.py and knowledge_payloads.py.

Following the 4 Principios Rectores:
1. Dogmatismo con Universal Response Schema
2. Servidor como Ejecutor Fiable
3. Estado en Claude, NO en Servidor
4. Testing Concurrente
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import Field

from schemas.universal_response import BasePayload


class TaskStrategyType(str, Enum):
    """Strategy types for task planning and reasoning approaches."""

    COT = "chain_of_thought"
    TOT = "tree_of_thoughts"


class ComplexityMetric(str, Enum):
    """Complexity dimension metrics for Task Complexity Score calculation."""

    NOVELTY = "novelty"
    COUPLING = "coupling"
    SCALE = "scale"
    AMBIGUITY = "ambiguity"


class KeymakerWorkflowPayload(BasePayload):
    """Payload for keymaker workflow template retrieval operations.

    Returns the complete Keymaker workflow structure for task planning.
    Inherits workflow_stage from BasePayload.
    """

    workflow_stage: str = Field(
        default="complete", description="Current workflow stage"
    )
    workflow_content: str = Field(
        ..., description="Complete workflow template content as JSON string"
    )
    template_format: str = Field(
        default="json", description="Format of template: json or markdown"
    )
    phases_count: int = Field(..., ge=1, description="Number of phases in workflow")
    phase_names: List[str] = Field(..., description="List of phase names from workflow")
    estimated_duration: str = Field(
        ..., description="Estimated completion time for workflow"
    )
    template_size_bytes: int = Field(
        ..., ge=0, description="Size of template file in bytes"
    )

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True,
    }


class ComplexityScorePayload(BasePayload):
    """Payload for Task Complexity Score (TCS) calculation results.

    Contains deterministic complexity evaluation and strategy recommendation.
    Inherits workflow_stage from BasePayload.
    """

    workflow_stage: str = Field(
        default="complete", description="Current workflow stage"
    )
    task_complexity_score: float = Field(
        ..., ge=1.0, le=5.0, description="Total TCS value (1-5 scale)"
    )
    recommended_strategy: TaskStrategyType = Field(
        ..., description="Recommended reasoning strategy: CoT or ToT"
    )
    metrics_breakdown: Dict[ComplexityMetric, Dict[str, Any]] = Field(
        ..., description="Detailed breakdown by complexity dimension"
    )
    confidence_level: float = Field(
        default=0.85,
        ge=0.0,
        le=1.0,
        description="Confidence in calculation (fixed at 0.85)",
    )
    threshold_details: Dict[str, Any] = Field(
        ..., description="Threshold values and comparison details"
    )
    scoring_breakdown: Dict[str, Dict[str, Any]] = Field(
        ..., description="Detailed scoring breakdown with weights and factors"
    )

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True,
    }


class ReasoningTemplatePayload(BasePayload):
    """Payload for reasoning template retrieval based on strategy type.

    Returns appropriate reasoning template (CoT or ToT) with usage guidelines.
    Inherits workflow_stage from BasePayload.
    """

    workflow_stage: str = Field(
        default="complete", description="Current workflow stage"
    )
    strategy_type: TaskStrategyType = Field(
        ..., description="Reasoning strategy type: CoT or ToT"
    )
    template_content: str = Field(
        ..., description="Complete template content as JSON string"
    )
    template_sections: List[Dict[str, str]] = Field(
        ..., description="List of template sections with names and descriptions"
    )
    guidelines: List[str] = Field(..., description="Usage guidelines for the template")

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True,
    }


class MissionMapPayload(BasePayload):
    """Payload for mission map saving and validation operations.

    Handles mission map persistence with JSON schema validation.
    Inherits workflow_stage from BasePayload.
    """

    workflow_stage: str = Field(
        default="complete", description="Current workflow stage"
    )
    file_path: str = Field(..., description="Absolute path where mission map was saved")
    validation_status: str = Field(
        ..., description="Validation result: valid, invalid, or error"
    )
    validation_errors: Optional[List[str]] = Field(
        default=None, description="List of validation errors if invalid"
    )
    mission_summary: Dict[str, Any] = Field(
        ..., description="Summary of mission content including key metrics"
    )
    file_size_bytes: int = Field(
        ..., ge=0, description="Size of saved mission map file in bytes"
    )

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True,
    }


class TaskDirectivesPayload(BasePayload):
    """Payload for task-specific Do's and Don'ts generation.

    Contains extracted patterns and generated directives from mission map.
    Inherits workflow_stage from BasePayload.
    """

    workflow_stage: str = Field(
        default="complete", description="Current workflow stage"
    )
    file_path: str = Field(
        ..., description="Absolute path to generated directives file"
    )
    dos_count: int = Field(..., ge=0, description="Number of Do's generated")
    donts_count: int = Field(..., ge=0, description="Number of Don'ts generated")
    source_patterns: List[str] = Field(
        ..., description="Patterns extracted from mission map descriptions"
    )
    technologies_covered: List[str] = Field(
        ..., description="Technologies mentioned in generated directives"
    )
    directives_content: str = Field(
        ..., description="Generated directives content in markdown format"
    )

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True,
    }


class LibraryChecklistPayload(BasePayload):
    """Payload for Context7 library documentation checklist generation.

    Extracts unique libraries and generates markdown checklist with Context7.
    Inherits workflow_stage from BasePayload.
    """

    workflow_stage: str = Field(
        default="complete", description="Current workflow stage"
    )
    file_path: str = Field(..., description="Absolute path to generated checklist file")
    libraries_found: List[Dict[str, str]] = Field(
        ..., description="Libraries with extracted names and potential Context7 IDs"
    )
    total_libraries: int = Field(
        ..., ge=0, description="Total number of unique libraries found"
    )
    checklist_format: str = Field(
        default="markdown", description="Format of checklist file"
    )
    checklist_content: str = Field(
        ..., description="Generated checklist content in markdown format"
    )

    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True,
    }
