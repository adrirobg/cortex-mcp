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


# Export main functions
__all__ = [
    "get_planning_template",
    "save_planning_artifact"
]