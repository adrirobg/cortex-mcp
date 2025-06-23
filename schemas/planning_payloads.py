"""Planning-specific payload schemas for Strategy Library MCP Server.

These schemas define the structured data returned by the planning toolkit tools.
Following the Universal Response Schema pattern with strict Pydantic validation.
"""

from typing import List, Optional
from pydantic import Field
from enum import Enum

from schemas.universal_response import BasePayload


class TemplateType(str, Enum):
    """Types of planning templates."""
    JSON = "json"
    MARKDOWN = "markdown"


class TemplateStatus(str, Enum):
    """Status of template retrieval."""
    SUCCESS = "success"
    ERROR = "error"
    NOT_FOUND = "not_found"


class ArtifactStatus(str, Enum):
    """Status of artifact saving."""
    SUCCESS = "success"
    ERROR = "error"
    DIRECTORY_CREATED = "directory_created"


class PlanningTemplatePayload(BasePayload):
    """Payload for planning template retrieval operations."""
    
    # Template information
    template_name: str = Field(..., description="Name of the requested template")
    template_type: Optional[TemplateType] = Field(None, description="Type of template (json/markdown)")
    template_status: TemplateStatus = Field(..., description="Status of template retrieval")
    
    # Template content (if successful)
    template_content: Optional[str] = Field(None, description="Raw template content")
    template_size_bytes: Optional[int] = Field(None, description="Size of template in bytes")
    
    # Available options (if template not found)
    available_templates: Optional[List[str]] = Field(None, description="List of available templates")
    available_extensions: Optional[List[str]] = Field(None, description="Supported template extensions")
    
    # Error information (if failed)
    error_message: Optional[str] = Field(None, description="Error message if retrieval failed")
    template_path_attempted: Optional[str] = Field(None, description="Path that was attempted")
    
    model_config = {
        "extra": "forbid",
        "validate_assignment": True,
        "use_enum_values": True
    }


class PlanningArtifactPayload(BasePayload):
    """Payload for planning artifact saving operations."""
    
    # Save operation information
    file_name: str = Field(..., description="Name of the saved file")
    file_path: str = Field(..., description="Full path where file was saved")
    directory: str = Field(..., description="Directory where file was saved")
    artifact_status: ArtifactStatus = Field(..., description="Status of save operation")
    
    # File metadata
    file_size_bytes: int = Field(..., description="Size of saved file in bytes")
    content_preview: Optional[str] = Field(None, description="Preview of file content (first 200 chars)")
    
    # Directory information
    directory_created: bool = Field(default=False, description="Whether directory was created")
    directory_exists: bool = Field(default=True, description="Whether directory existed")
    
    # Operation metadata
    encoding_used: str = Field(default="utf-8", description="Encoding used for file writing")
    operation_timestamp: Optional[str] = Field(None, description="Timestamp of save operation")
    
    # Error information (if failed)
    error_message: Optional[str] = Field(None, description="Error message if save failed")
    
    model_config = {
        "extra": "forbid", 
        "validate_assignment": True,
        "use_enum_values": True
    }


class PlanningWorkflowStage(str, Enum):
    """Stages of the planning workflow."""
    TEMPLATE_RETRIEVAL = "template_retrieval"
    TEMPLATE_PROCESSING = "template_processing"
    ARTIFACT_CREATION = "artifact_creation"
    ARTIFACT_SAVED = "artifact_saved"
    WORKFLOW_COMPLETE = "workflow_complete"
    ERROR = "error"