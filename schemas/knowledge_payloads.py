"""Knowledge Management-specific payload schemas for Strategy Library MCP Server.

These schemas define the structured data returned by the knowledge management tools.
Following the Universal Response Schema pattern with strict Pydantic validation.
"""

from typing import Any, Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from enum import Enum

from schemas.universal_response import BasePayload


class RetrospectiveStatus(str, Enum):
    """Status of retrospective operations."""
    DRAFT_CREATED = "draft_created"
    TEMPLATE_GENERATED = "template_generated"
    ANALYSIS_REQUIRED = "analysis_required"
    COMPLETED = "completed"
    ERROR = "error"


class KnowledgeIntegrationStatus(str, Enum):
    """Status of knowledge integration operations."""
    PROCESSING = "processing"
    INSIGHTS_EXTRACTED = "insights_extracted"
    KNOWLEDGE_UPDATED = "knowledge_updated"
    INTEGRATION_COMPLETE = "integration_complete"
    ERROR = "error"


class KnowledgeWorkflowStage(str, Enum):
    """Stages of the knowledge management workflow."""
    RETROSPECTIVE_CREATION = "retrospective_creation"
    RETROSPECTIVE_ANALYSIS = "retrospective_analysis"
    INSIGHT_EXTRACTION = "insight_extraction"
    KNOWLEDGE_INTEGRATION = "knowledge_integration"
    WORKFLOW_COMPLETE = "workflow_complete"
    ERROR = "error"


class RetrospectiveSection(BaseModel):
    """Individual section in a retrospective template."""
    name: str = Field(..., description="Name of the retrospective section")
    description: str = Field(..., description="Description of what should be in this section")
    completed: bool = Field(default=False, description="Whether this section is completed")


class RetrospectivePayload(BasePayload):
    """Payload for retrospective creation operations."""
    
    # Retrospective metadata
    task_name: str = Field(..., description="Name/description of the completed task")
    retrospective_file: str = Field(..., description="Path to the retrospective file")
    retrospective_status: RetrospectiveStatus = Field(..., description="Status of retrospective operation")
    
    # Optional context
    phase_context: Optional[str] = Field(None, description="Phase or project context")
    duration_estimate: Optional[str] = Field(None, description="Duration estimate for the task")
    
    # Template structure
    template_sections: List[str] = Field(default=[], description="List of template section names")
    sections_detail: Optional[List[RetrospectiveSection]] = Field(None, description="Detailed section information")
    
    # File metadata
    file_size_bytes: Optional[int] = Field(None, description="Size of retrospective file in bytes")
    timestamp: Optional[str] = Field(None, description="Creation timestamp")
    
    # Next steps
    next_tool: Optional[str] = Field(None, description="Next tool to use in workflow")
    analysis_guidance: Optional[List[str]] = Field(None, description="Guidance for completing analysis")
    
    # Error information
    error_message: Optional[str] = Field(None, description="Error message if operation failed")
    
    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True
    }


class ImprovementSuggestion(BaseModel):
    """Individual improvement suggestion extracted from retrospective."""
    id: str = Field(..., description="Unique improvement ID")
    title: str = Field(..., description="Short title for the improvement")
    description: str = Field(..., description="Full description of the improvement")
    category: str = Field(..., description="Category of improvement")
    source: str = Field(..., description="Source of the improvement (retrospective_analysis, etc.)")
    priority_score: float = Field(default=3.0, description="Priority score (1-5)")
    effort_estimate: int = Field(default=3, description="Effort estimate (1-5)")
    impact_estimate: int = Field(default=3, description="Impact estimate (1-5)")


class KnowledgeIntegrationPayload(BasePayload):
    """Payload for knowledge integration operations."""
    
    # Source information
    retrospective_file: str = Field(..., description="Path to processed retrospective file")
    integration_status: KnowledgeIntegrationStatus = Field(..., description="Status of integration")
    
    # Extraction results
    improvements_extracted: int = Field(default=0, description="Number of improvements extracted")
    new_improvement_ids: List[str] = Field(default=[], description="IDs of newly added improvements")
    extracted_improvements: Optional[List[ImprovementSuggestion]] = Field(None, description="Details of extracted improvements")
    
    # Knowledge artifacts updated
    knowledge_artifacts: List[str] = Field(default=[], description="Paths to updated knowledge artifacts")
    improvements_file: Optional[str] = Field(None, description="Path to improvements database file")
    
    # Integration metadata
    total_improvements: Optional[int] = Field(None, description="Total improvements in database after integration")
    integration_timestamp: Optional[str] = Field(None, description="Timestamp of integration operation")
    
    # Processing summary
    sections_processed: Optional[List[str]] = Field(None, description="Retrospective sections that were processed")
    parsing_success: bool = Field(default=True, description="Whether parsing was successful")
    
    # Recommendations
    next_recommendations: Optional[List[str]] = Field(None, description="Recommended next steps")
    prioritization_suggestions: Optional[List[str]] = Field(None, description="Suggestions for prioritizing improvements")
    
    # Error information
    error_message: Optional[str] = Field(None, description="Error message if integration failed")
    
    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True
    }


class KnowledgeMetrics(BaseModel):
    """Metrics about knowledge management operations."""
    total_retrospectives: int = Field(default=0, description="Total number of retrospectives processed")
    total_improvements: int = Field(default=0, description="Total improvements in knowledge base")
    recent_integrations: int = Field(default=0, description="Number of recent integrations")
    knowledge_growth_rate: Optional[float] = Field(None, description="Rate of knowledge base growth")
    
    
class KnowledgeWorkflowPayload(BasePayload):
    """Extended payload for complete knowledge workflows."""
    
    # Current workflow state
    workflow_stage: KnowledgeWorkflowStage = Field(..., description="Current stage of knowledge workflow")
    
    # Individual operation payloads (optional based on stage)
    retrospective_data: Optional[RetrospectivePayload] = Field(None, description="Retrospective operation data")
    integration_data: Optional[KnowledgeIntegrationPayload] = Field(None, description="Integration operation data")
    
    # Workflow metrics
    metrics: Optional[KnowledgeMetrics] = Field(None, description="Knowledge management metrics")
    
    # Workflow completion
    workflow_complete: bool = Field(default=False, description="Whether the workflow is complete")
    next_workflow_stage: Optional[KnowledgeWorkflowStage] = Field(None, description="Next stage in workflow")
    
    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True
    }