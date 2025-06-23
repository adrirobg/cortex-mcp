#!/usr/bin/env python3
"""Planning Prompts for CortexMCP.

Native MCP prompts for planning workflows, following the same modular 
architecture as tools but using MCP standard prompt structure.

Following the 4 Principios Rectores:
1. Dogmatismo con Universal Response Schema (adapted for prompts)
2. Servidor como Ejecutor Fiable 
3. Estado en Claude, NO en Servidor
4. Testing Concurrente
"""

from typing import Dict, Annotated
from pydantic import Field


def phase_preparation_simple_prompt(
    phase_name: Annotated[str, Field(
        description="Name of the phase to prepare",
        examples=["Phase 2.8.6", "Database Migration"]
    )],
    project_context: Annotated[str, Field(
        description="Context of the project or current situation", 
        examples=["CortexMCP Enhancement", "User Authentication System"]
    )],
    priority: Annotated[str, Field(
        description="Priority level for the phase",
        default="medium"
    )] = "medium",
    duration_hours: Annotated[int, Field(
        description="Estimated duration in hours",
        default=8
    )] = 8
) -> Dict:
    """Experimental native MCP prompt for phase preparation.
    
    This is a research experiment to compare native MCP prompts
    vs our current PlanningTemplateTool approach.
    
    Args:
        phase_name: Name of the phase to prepare
        project_context: Context of the project or current situation
        priority: Priority level for the phase (default: medium)
        duration_hours: Estimated duration in hours (default: 8)
        
    Returns:
        Dict: MCP standard prompt structure with messages
    """
    
    # Generate dynamic prompt content using MCP native structure
    prompt_text = f"""# Phase Preparation: {phase_name}

**Project Context**: {project_context}
**Priority**: {priority}
**Estimated Duration**: {duration_hours} hours
**Generated**: Native MCP Prompt (Experimental)

---

## 🎯 Phase Overview

Please complete this phase preparation plan:

1. **Core Problem Identified**: [Analyze and define the specific problem this phase solves]

2. **Solution Approach**: [Describe the methodology and approach to solve the problem]

3. **Technical Scope**: [Define what files, systems, or components will be affected]

---

## 🏗️ Implementation Plan

### Step 1: Analysis & Preparation
- **Objective**: [Define what this step accomplishes]
- **Technical Implementation**: [Specific actions to take]
- **Validation**: [How to verify success]

### Step 2: Core Implementation  
- **Objective**: [Define what this step accomplishes]
- **Technical Implementation**: [Specific actions to take]
- **Validation**: [How to verify success]

### Step 3: Testing & Validation
- **Objective**: [Define what this step accomplishes] 
- **Technical Implementation**: [Specific actions to take]
- **Validation**: [How to verify success]

---

## ✅ Success Criteria

### Functional Requirements
- [List specific, measurable functional success criteria]

### Quality Requirements
- [List quality gates that must be met]

### Strategic Requirements  
- [List strategic objectives that must be achieved]

---

## 🚨 Anti-Over-Engineering Guards

### Complexity Elimination
- [What complex approaches should be avoided and why]

### Simplicity Requirements
- [Principles to maintain to ensure simplicity]

---

## 📊 Expected Outcomes

- **Immediate Benefits**: [Direct benefits upon phase completion]
- **Strategic Positioning**: [How this phase positions future work]

---

*Phase preparation generated via Native MCP Prompt (Experimental)*
*Compare with PlanningTemplateTool output for research*"""

    return {
        "messages": [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": prompt_text
                }
            }
        ]
    }


# Export clean API
__all__ = [
    "phase_preparation_simple_prompt"
]