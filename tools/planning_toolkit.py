#!/usr/bin/env python3
"""Planning Toolkit for CortexMCP.

Implements the Planning Toolkit MVP with get-planning-template and 
save-planning-artifact tools for Claude-controlled artifact generation.

Following the 4 Principios Rectores:
1. Dogmatismo con Universal Response Schema ✅
2. Servidor como Ejecutor Fiable ✅ 
3. Estado en Claude, NO en Servidor ✅
4. Testing Concurrente ✅

Anti-Over-Engineering Implementation:
- Zero cognitive capabilities - pure deterministic utilities
- Simple file operations with proper error handling
- Complete separation: MCP = tools, Claude = cognition
"""

import json
import os
import logging
from typing import Optional
from datetime import datetime

from tools.base_tool import BaseTool
from schemas.universal_response import StrategyResponse, StrategyType, ExecutionType, Action
from schemas.planning_payloads import (
    PlanningTemplatePayload,
    PlanningArtifactPayload,
    TemplateType,
    TemplateStatus,
    ArtifactStatus,
    PlanningWorkflowStage
)

# Configure logging
logger = logging.getLogger(__name__)


def get_planning_template(template_name: str) -> str:
    """Retrieve blank planning template structure for Claude's cognitive work.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - simple deterministic utility.
    Following Principio Rector #3: Zero cognition, zero state.
    
    Args:
        template_name: Name of the template to retrieve
        
    Returns:
        JSON string with template content or error message
    """
    try:
        # Construct template path - try JSON first, then markdown
        json_template_path = f".cortex/templates/{template_name}.json"
        md_template_path = f".cortex/templates/{template_name}.md"
        
        # Check for JSON template first
        if os.path.exists(json_template_path):
            with open(json_template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            return json.dumps({
                "status": "success",
                "template_type": "json",
                "template_name": template_name,
                "content": template_content
            })
        
        # Check for markdown template
        elif os.path.exists(md_template_path):
            with open(md_template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            return json.dumps({
                "status": "success", 
                "template_type": "markdown",
                "template_name": template_name,
                "content": template_content
            })
        
        # Template not found
        else:
            return json.dumps({
                "status": "error",
                "message": f"Template '{template_name}' not found in .cortex/templates/ directory",
                "available_extensions": ["json", "md"]
            })
            
    except Exception as e:
        logger.error(f"Template retrieval failed: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": f"Template retrieval failed: {str(e)}"
        })


def save_planning_artifact(file_name: str, file_content: str, directory: str = ".cortex/planning/") -> str:
    """Save Claude's planning artifact to specified location.
    
    Following Principio Rector #2: Servidor como Ejecutor Fiable - simple file storage utility.
    Following Principio Rector #3: Zero cognition, pure storage operation.
    
    Args:
        file_name: Name of the file to save
        file_content: Content to write to the file
        directory: Directory path to save the file (default: .cortex/planning/)
        
    Returns:
        JSON string with save status and file path
    """
    try:
        # Ensure directory exists
        os.makedirs(directory, exist_ok=True)
        
        # Full path construction
        file_path = os.path.join(directory, file_name)
        
        # Write file with UTF-8 encoding
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
            
        return json.dumps({
            "status": "success",
            "message": f"Planning artifact saved successfully",
            "file_path": file_path,
            "file_name": file_name,
            "directory": directory,
            "file_size_bytes": len(file_content.encode('utf-8'))
        })
        
    except Exception as e:
        logger.error(f"Artifact save failed: {str(e)}")
        return json.dumps({
            "status": "error", 
            "message": f"Failed to save planning artifact: {str(e)}",
            "file_name": file_name,
            "directory": directory
        })


# ========================================
# MODERN BASETOOL ARCHITECTURE
# Following Principio Rector #1: Universal Response Schema
# ========================================

class PlanningTemplateTool(BaseTool[PlanningTemplatePayload]):
    """Planning Template Tool - Modern BaseTool implementation.
    
    Retrieves planning templates with full schema validation and MCP compliance.
    Following the CortexMCP-Plus architecture pattern.
    """
    
    def __init__(self):
        """Initialize planning template tool."""
        super().__init__("planning-template-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        """Get strategy type for planning template tool."""
        return StrategyType.PLANNING
    
    def execute(self, template_name: str, **kwargs) -> StrategyResponse[PlanningTemplatePayload]:
        """Execute planning template retrieval.
        
        Args:
            template_name: Name of the template to retrieve
            **kwargs: Additional parameters (unused in MVP)
            
        Returns:
            StrategyResponse[PlanningTemplatePayload]: Structured response with template data
        """
        try:
            # Construct template paths
            json_template_path = f".cortex/templates/{template_name}.json"
            md_template_path = f".cortex/templates/{template_name}.md"
            
            # Check for JSON template first
            if os.path.exists(json_template_path):
                with open(json_template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                
                payload = PlanningTemplatePayload(
                    workflow_stage="template_retrieval",
                    template_name=template_name,
                    template_type=TemplateType.JSON,
                    template_status=TemplateStatus.SUCCESS,
                    template_content=template_content,
                    template_size_bytes=len(template_content.encode('utf-8')),
                    template_path_attempted=json_template_path,
                    suggested_next_state={
                        "template_retrieved": True,
                        "template_name": template_name,
                        "template_type": "json",
                        "ready_for_processing": True
                    }
                )
                
                return self.create_success_response(
                    summary=f"✅ Planning template '{template_name}' retrieved successfully (JSON format)",
                    payload=payload,
                    execution_type=ExecutionType.IMMEDIATE,
                    actions=[
                        Action(
                            type="process_template",
                            description=f"Process retrieved template: {template_name}",
                            priority=1,
                            validation_criteria="Template content is valid and ready for cognitive processing",
                            parameters={"template_name": template_name, "template_type": "json"}
                        )
                    ],
                    key_points=[
                        f"Template '{template_name}' found and loaded",
                        "JSON format provides structured cognitive scaffolding",
                        "Template ready for Claude intelligence processing",
                        f"Template size: {len(template_content.encode('utf-8'))} bytes"
                    ],
                    next_steps=[
                        "1. Parse template structure for cognitive guidance",
                        "2. Fill template sections with strategic analysis",
                        "3. Apply domain expertise to complete planning",
                        "4. Generate planning artifact when complete"
                    ],
                    confidence_score=1.0,
                    complexity_score=1,
                    estimated_duration="immediate",
                    performance_hints=[
                        "Template retrieval is deterministic and fast",
                        "Cognitive processing time depends on template complexity"
                    ],
                    learning_opportunities=[
                        "Template-guided cognitive processing",
                        "Structured planning methodology"
                    ]
                )
            
            # Check for markdown template
            elif os.path.exists(md_template_path):
                with open(md_template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                
                payload = PlanningTemplatePayload(
                    workflow_stage="template_retrieval",
                    template_name=template_name,
                    template_type=TemplateType.MARKDOWN,
                    template_status=TemplateStatus.SUCCESS,
                    template_content=template_content,
                    template_size_bytes=len(template_content.encode('utf-8')),
                    template_path_attempted=md_template_path,
                    suggested_next_state={
                        "template_retrieved": True,
                        "template_name": template_name,
                        "template_type": "markdown",
                        "ready_for_processing": True
                    }
                )
                
                return self.create_success_response(
                    summary=f"✅ Planning template '{template_name}' retrieved successfully (Markdown format)",
                    payload=payload,
                    execution_type=ExecutionType.IMMEDIATE,
                    actions=[
                        Action(
                            type="process_template",
                            description=f"Process retrieved template: {template_name}",
                            priority=1,
                            validation_criteria="Template content is valid and ready for cognitive processing",
                            parameters={"template_name": template_name, "template_type": "markdown"}
                        )
                    ],
                    key_points=[
                        f"Template '{template_name}' found and loaded",
                        "Markdown format provides human-readable guidance",
                        "Template ready for Claude intelligence processing",
                        f"Template size: {len(template_content.encode('utf-8'))} bytes"
                    ],
                    next_steps=[
                        "1. Parse template structure for cognitive guidance",
                        "2. Fill template sections with strategic analysis",
                        "3. Apply domain expertise to complete planning",
                        "4. Generate planning artifact when complete"
                    ],
                    confidence_score=1.0,
                    complexity_score=1,
                    estimated_duration="immediate",
                    performance_hints=[
                        "Template retrieval is deterministic and fast",
                        "Cognitive processing time depends on template complexity"
                    ],
                    learning_opportunities=[
                        "Template-guided cognitive processing",
                        "Structured planning methodology"
                    ]
                )
            
            # Template not found
            else:
                # Check what templates are available
                templates_dir = ".cortex/templates"
                available_templates = []
                if os.path.exists(templates_dir):
                    for file in os.listdir(templates_dir):
                        if file.endswith(('.json', '.md')):
                            available_templates.append(file.replace('.json', '').replace('.md', ''))
                
                payload = PlanningTemplatePayload(
                    workflow_stage="error",
                    template_name=template_name,
                    template_status=TemplateStatus.NOT_FOUND,
                    error_message=f"Template '{template_name}' not found in .cortex/templates/ directory",
                    template_path_attempted=f"{json_template_path} or {md_template_path}",
                    available_templates=list(set(available_templates)),
                    available_extensions=["json", "md"],
                    suggested_next_state={
                        "template_retrieved": False,
                        "template_name": template_name,
                        "error_occurred": True,
                        "available_templates": list(set(available_templates))
                    }
                )
                
                return self.create_success_response(
                    summary=f"❌ Planning template '{template_name}' not found",
                    payload=payload,
                    execution_type=ExecutionType.USER_CONFIRMATION,
                    actions=[
                        Action(
                            type="select_alternative_template",
                            description="Select from available templates or create new one",
                            priority=1,
                            validation_criteria="Valid template selected or new template created",
                            parameters={"available_templates": list(set(available_templates))}
                        )
                    ],
                    key_points=[
                        f"Template '{template_name}' not found",
                        f"Available templates: {', '.join(set(available_templates)) if available_templates else 'None'}",
                        "Supported formats: JSON, Markdown",
                        "Templates stored in .cortex/templates/ directory"
                    ],
                    next_steps=[
                        "1. Choose from available templates if suitable",
                        "2. Create new template if needed",
                        "3. Verify template directory structure",
                        "4. Retry with correct template name"
                    ],
                    confidence_score=1.0,
                    complexity_score=1,
                    estimated_duration="immediate",
                    performance_hints=[
                        "Check template name spelling",
                        "Verify .cortex/templates/ directory exists"
                    ],
                    learning_opportunities=[
                        "Template naming conventions",
                        "Planning template structure"
                    ]
                )
                
        except Exception as e:
            logger.error(f"Template retrieval failed: {str(e)}")
            
            payload = PlanningTemplatePayload(
                workflow_stage="error",
                template_name=template_name,
                template_status=TemplateStatus.ERROR,
                error_message=f"Template retrieval failed: {str(e)}",
                template_path_attempted="unknown",
                suggested_next_state={
                    "template_retrieved": False,
                    "template_name": template_name,
                    "error_occurred": True,
                    "error_type": "execution_error"
                }
            )
            
            return self.create_success_response(
                summary=f"❌ Error retrieving planning template '{template_name}'",
                payload=payload,
                execution_type=ExecutionType.USER_CONFIRMATION,
                actions=[
                    Action(
                        type="retry_template_retrieval",
                        description="Retry template retrieval after fixing error",
                        priority=1,
                        validation_criteria="Error resolved and template retrieved",
                        parameters={"template_name": template_name, "error": str(e)}
                    )
                ],
                key_points=[
                    f"Template retrieval failed: {str(e)}",
                    "Check file system permissions",
                    "Verify .cortex/templates/ directory exists",
                    "Template name may contain invalid characters"
                ],
                next_steps=[
                    "1. Check error message for specific issue",
                    "2. Verify file system permissions",
                    "3. Ensure template directory exists",
                    "4. Retry with corrected parameters"
                ],
                confidence_score=0.8,
                complexity_score=2,
                estimated_duration="immediate",
                performance_hints=[
                    "Check file system permissions",
                    "Verify directory structure"
                ],
                learning_opportunities=[
                    "Error handling in template retrieval",
                    "File system operations debugging"
                ]
            )


class PlanningArtifactTool(BaseTool[PlanningArtifactPayload]):
    """Planning Artifact Tool - Modern BaseTool implementation.
    
    Saves planning artifacts with full schema validation and MCP compliance.
    Following the CortexMCP-Plus architecture pattern.
    """
    
    def __init__(self):
        """Initialize planning artifact tool."""
        super().__init__("planning-artifact-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        """Get strategy type for planning artifact tool."""
        return StrategyType.PLANNING
    
    def execute(self, file_name: str, file_content: str, directory: str = ".cortex/planning/", **kwargs) -> StrategyResponse[PlanningArtifactPayload]:
        """Execute planning artifact saving.
        
        Args:
            file_name: Name of the file to save
            file_content: Content to write to the file
            directory: Directory path to save the file
            **kwargs: Additional parameters (unused in MVP)
            
        Returns:
            StrategyResponse[PlanningArtifactPayload]: Structured response with save result
        """
        try:
            # Ensure directory exists
            directory_created = False
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                directory_created = True
            
            # Full path construction
            file_path = os.path.join(directory, file_name)
            
            # Write file with UTF-8 encoding
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            # Generate content preview
            content_preview = file_content[:200] + "..." if len(file_content) > 200 else file_content
            file_size_bytes = len(file_content.encode('utf-8'))
            
            payload = PlanningArtifactPayload(
                workflow_stage="artifact_saved",
                file_name=file_name,
                file_path=file_path,
                directory=directory,
                artifact_status=ArtifactStatus.SUCCESS,
                file_size_bytes=file_size_bytes,
                content_preview=content_preview,
                directory_created=directory_created,
                directory_exists=True,
                encoding_used="utf-8",
                operation_timestamp=datetime.now().isoformat(),
                suggested_next_state={
                    "artifact_saved": True,
                    "file_path": file_path,
                    "file_name": file_name,
                    "workflow_complete": True
                }
            )
            
            return self.create_success_response(
                summary=f"✅ Planning artifact '{file_name}' saved successfully",
                payload=payload,
                execution_type=ExecutionType.IMMEDIATE,
                actions=[
                    Action(
                        type="artifact_saved",
                        description=f"Planning artifact saved: {file_path}",
                        priority=1,
                        validation_criteria="File saved successfully and is accessible",
                        parameters={"file_path": file_path, "file_size": file_size_bytes}
                    )
                ],
                key_points=[
                    f"Artifact saved: {file_path}",
                    f"File size: {file_size_bytes} bytes",
                    f"Directory: {directory}" + (" (created)" if directory_created else " (existing)"),
                    "Encoding: UTF-8",
                    "External memory preserved for future sessions"
                ],
                next_steps=[
                    "1. Verify file was saved correctly",
                    "2. File is now part of .cortex knowledge base",
                    "3. Artifact can be referenced in future planning sessions",
                    "4. Consider creating additional artifacts if needed"
                ],
                confidence_score=1.0,
                complexity_score=1,
                estimated_duration="immediate",
                performance_hints=[
                    "File saving is atomic and deterministic",
                    "Large files may take longer to write"
                ],
                learning_opportunities=[
                    "Artifact persistence for external memory",
                    "Structured planning documentation"
                ]
            )
            
        except Exception as e:
            logger.error(f"Artifact save failed: {str(e)}")
            
            payload = PlanningArtifactPayload(
                workflow_stage="error",
                file_name=file_name,
                file_path="unknown",
                directory=directory,
                artifact_status=ArtifactStatus.ERROR,
                file_size_bytes=0,
                directory_created=False,
                directory_exists=os.path.exists(directory),
                encoding_used="utf-8",
                operation_timestamp=datetime.now().isoformat(),
                error_message=f"Failed to save planning artifact: {str(e)}",
                suggested_next_state={
                    "artifact_saved": False,
                    "file_name": file_name,
                    "directory": directory,
                    "error_occurred": True,
                    "error_type": "save_failure"
                }
            )
            
            return self.create_success_response(
                summary=f"❌ Error saving planning artifact '{file_name}'",
                payload=payload,
                execution_type=ExecutionType.USER_CONFIRMATION,
                actions=[
                    Action(
                        type="retry_artifact_save",
                        description="Retry artifact saving after fixing error",
                        priority=1,
                        validation_criteria="Error resolved and artifact saved",
                        parameters={"file_name": file_name, "directory": directory, "error": str(e)}
                    )
                ],
                key_points=[
                    f"Artifact save failed: {str(e)}",
                    f"Target directory: {directory}",
                    f"Target file: {file_name}",
                    "Check file system permissions and disk space"
                ],
                next_steps=[
                    "1. Check error message for specific issue",
                    "2. Verify file system permissions",
                    "3. Ensure directory is writable",
                    "4. Check available disk space",
                    "5. Retry with corrected parameters"
                ],
                confidence_score=0.8,
                complexity_score=2,
                estimated_duration="immediate",
                performance_hints=[
                    "Check file system permissions",
                    "Verify directory exists and is writable"
                ],
                learning_opportunities=[
                    "Error handling in file operations",
                    "File system permissions debugging"
                ]
            )


# ========================================
# BACKWARD COMPATIBILITY WRAPPER FUNCTIONS
# Maintain legacy API while using modern BaseTool internally
# ========================================

def get_planning_template_modern(template_name: str) -> StrategyResponse[PlanningTemplatePayload]:
    """Modern wrapper for planning template retrieval.
    
    Returns full StrategyResponse for tools that support it.
    """
    tool = PlanningTemplateTool()
    return tool.execute(template_name=template_name)


def save_planning_artifact_modern(file_name: str, file_content: str, directory: str = ".cortex/planning/") -> StrategyResponse[PlanningArtifactPayload]:
    """Modern wrapper for planning artifact saving.
    
    Returns full StrategyResponse for tools that support it.
    """
    tool = PlanningArtifactTool()
    return tool.execute(file_name=file_name, file_content=file_content, directory=directory)


# Export main functions - Legacy + Modern
__all__ = [
    "get_planning_template",
    "save_planning_artifact",
    "get_planning_template_modern",
    "save_planning_artifact_modern",
    "PlanningTemplateTool",
    "PlanningArtifactTool"
]