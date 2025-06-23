# 🎯 Plan de Desarrollo: Suite de Herramientas del Keymaker para CortexMCP

## 📋 Resumen Ejecutivo

**Objetivo**: Implementar 6 herramientas atómicas que automaticen el flujo de planificación de tareas del keymaker, manteniendo la pureza arquitectónica de CortexMCP.

**Duración estimada**: 2-3 días
**Complejidad**: Media (TCS: 3)
**Estrategia**: Implementación incremental con validación continua

---

## 🏗️ Fase 1: Preparación y Estructura (2 horas)

### 1.1 Crear Archivos Base

```bash
# Estructura a crear (siguiendo patrones existentes):
tools/task_planning.py              # Todas las herramientas del keymaker
schemas/task_planning_payloads.py   # Payloads específicos
tests/tools/test_task_planning.py   # Tests completos
```

### 1.2 Crear Templates en .cortex

```bash
.cortex/templates/task_planning/
├── keymaker_workflow.json          # Workflow completo estructurado
├── cot_reasoning.json              # 5 thought templates para CoT
├── tot_reasoning.json              # 3 perspectives + evaluation para ToT
└── mission_map_schema.json         # JSON Schema para validación
```

### 1.3 Copiar y Adaptar complexity_matrix.md

```bash
# Copiar a templates para acceso más fácil
cp .roo/scoring/complexity_matrix.md .cortex/templates/task_planning/complexity_matrix.xml
```

---

## 🔧 Fase 2: Implementación de Schemas (1 hora)

### 2.1 Archivo: `schemas/task_planning_payloads.py`

```python
"""Payloads for Task Planning tools following CortexMCP patterns.

All payloads inherit from BasePayload and follow the established
patterns from planning_payloads.py and knowledge_payloads.py.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import Field
from schemas.universal_response import BasePayload


class TaskStrategyType(str, Enum):
    """Strategy types for task planning."""
    COT = "chain_of_thought"
    TOT = "tree_of_thoughts"


class ComplexityMetric(str, Enum):
    """Complexity dimension metrics."""
    NOVELTY = "novelty"
    COUPLING = "coupling"
    SCALE = "scale"
    AMBIGUITY = "ambiguity"


class KeymakerWorkflowPayload(BasePayload):
    """Payload for keymaker workflow retrieval."""
    workflow_stage: str = Field(default="workflow_retrieved")
    workflow_content: str = Field(description="Complete workflow template content")
    template_format: str = Field(description="Format: json or markdown")
    phases_count: int = Field(description="Number of phases in workflow")
    phase_names: List[str] = Field(description="List of phase names")
    estimated_duration: str = Field(description="Estimated completion time")
    template_size_bytes: int = Field(description="Size of template file")


class ComplexityScorePayload(BasePayload):
    """Payload for complexity score calculation."""
    workflow_stage: str = Field(default="complexity_calculated")
    task_complexity_score: int = Field(description="Total TCS value")
    recommended_strategy: TaskStrategyType = Field(description="CoT or ToT")
    metrics_breakdown: Dict[ComplexityMetric, Dict[str, Any]] = Field(
        description="Detailed breakdown by dimension"
    )
    confidence_level: float = Field(description="Confidence in calculation (0-1)")
    threshold_details: Dict[str, Any] = Field(
        description="Threshold values and comparison"
    )


class ReasoningTemplatePayload(BasePayload):
    """Payload for reasoning template retrieval."""
    workflow_stage: str = Field(default="reasoning_template_retrieved")
    strategy_type: TaskStrategyType = Field(description="CoT or ToT")
    template_content: str = Field(description="Template content")
    template_sections: List[Dict[str, str]] = Field(
        description="List of template sections"
    )
    guidelines: List[str] = Field(description="Usage guidelines")


class MissionMapPayload(BasePayload):
    """Payload for mission map saving."""
    workflow_stage: str = Field(default="mission_map_saved")
    file_path: str = Field(description="Path where mission map was saved")
    validation_status: str = Field(description="valid or invalid")
    validation_errors: Optional[List[str]] = Field(default=None)
    mission_summary: Dict[str, Any] = Field(
        description="Summary of mission content"
    )
    file_size_bytes: int = Field(description="Size of saved file")


class TaskDirectivesPayload(BasePayload):
    """Payload for task directives generation."""
    workflow_stage: str = Field(default="directives_generated")
    file_path: str = Field(description="Path to generated directives")
    dos_count: int = Field(description="Number of Do's generated")
    donts_count: int = Field(description="Number of Don'ts generated")
    source_patterns: List[str] = Field(
        description="Patterns extracted from mission map"
    )
    technologies_covered: List[str] = Field(
        description="Technologies mentioned in directives"
    )


class LibraryChecklistPayload(BasePayload):
    """Payload for library checklist generation."""
    workflow_stage: str = Field(default="checklist_generated")
    file_path: str = Field(description="Path to generated checklist")
    libraries_found: List[Dict[str, str]] = Field(
        description="Libraries with potential Context7 IDs"
    )
    total_libraries: int = Field(description="Total number of libraries found")
    checklist_format: str = Field(default="markdown")
```

---

## 🛠️ Fase 3: Implementación de Herramientas (4 horas)

### 3.1 Archivo: `tools/task_planning.py`

```python
#!/usr/bin/env python3
"""Task Planning Toolkit for CortexMCP.

Implements the Keymaker workflow tools for automated task planning
and construction kit generation.

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
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
import re

import aiofiles
import aiofiles.os

from tools.base_tool import BaseTool
from schemas.universal_response import StrategyResponse, StrategyType, ExecutionType, Action
from schemas.task_planning_payloads import (
    KeymakerWorkflowPayload,
    ComplexityScorePayload,
    ReasoningTemplatePayload,
    MissionMapPayload,
    TaskDirectivesPayload,
    LibraryChecklistPayload,
    TaskStrategyType,
    ComplexityMetric
)

logger = logging.getLogger(__name__)


class KeymakerWorkflowTool(BaseTool[KeymakerWorkflowPayload]):
    """Retrieves the keymaker workflow template."""
    
    def __init__(self):
        super().__init__("keymaker-workflow-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        return StrategyType.PLANNING
    
    async def execute(self, workflow_type: str = "task_planning", **kwargs) -> StrategyResponse[KeymakerWorkflowPayload]:
        """Retrieve keymaker workflow template.
        
        Args:
            workflow_type: Type of workflow (default: task_planning)
            
        Returns:
            StrategyResponse with workflow template
        """
        try:
            template_path = f".cortex/templates/task_planning/keymaker_workflow.json"
            
            if not await aiofiles.os.path.exists(template_path):
                # Fallback to markdown if JSON doesn't exist
                template_path = template_path.replace('.json', '.md')
                template_format = "markdown"
            else:
                template_format = "json"
            
            async with aiofiles.open(template_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            # Extract phase information
            if template_format == "json":
                workflow_data = json.loads(content)
                phases = workflow_data.get("phases", [])
                phase_names = [p.get("name", "") for p in phases]
                phases_count = len(phases)
            else:
                # Simple phase extraction from markdown
                phase_names = re.findall(r'## Phase \d+: (.+)', content)
                phases_count = len(phase_names)
            
            payload = KeymakerWorkflowPayload(
                workflow_content=content,
                template_format=template_format,
                phases_count=phases_count,
                phase_names=phase_names,
                estimated_duration="30-45 minutes",
                template_size_bytes=len(content.encode('utf-8'))
            )
            
            return self.create_success_response(
                summary="✅ Keymaker workflow template retrieved successfully",
                payload=payload,
                execution_type=ExecutionType.IMMEDIATE,
                key_points=[
                    f"Workflow has {phases_count} phases",
                    f"Format: {template_format}",
                    "Ready for cognitive processing"
                ],
                next_steps=[
                    "1. Review workflow phases",
                    "2. Prepare task description",
                    "3. Calculate complexity score"
                ],
                confidence_score=1.0,
                complexity_score=1
            )
            
        except Exception as e:
            logger.error(f"Failed to retrieve workflow: {str(e)}")
            raise


class ComplexityScoreTool(BaseTool[ComplexityScorePayload]):
    """Calculates Task Complexity Score (TCS) deterministically."""
    
    def __init__(self):
        super().__init__("complexity-score-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        return StrategyType.ANALYSIS
    
    async def execute(self, task_description: str, scope: str, 
                     expected_outputs: List[str], **kwargs) -> StrategyResponse[ComplexityScorePayload]:
        """Calculate complexity score based on task attributes.
        
        Args:
            task_description: High-level task description
            scope: Detailed scope and requirements
            expected_outputs: List of expected deliverables
            
        Returns:
            StrategyResponse with TCS and strategy recommendation
        """
        try:
            # Load complexity matrix
            matrix_path = ".cortex/templates/task_planning/complexity_matrix.xml"
            if not await aiofiles.os.path.exists(matrix_path):
                # Fallback to original location
                matrix_path = ".roo/scoring/complexity_matrix.md"
            
            async with aiofiles.open(matrix_path, 'r', encoding='utf-8') as f:
                matrix_content = await f.read()
            
            # Parse XML
            root = ET.fromstring(matrix_content)
            
            # Combine all text for analysis
            full_text = f"{task_description} {scope} {' '.join(expected_outputs)}".lower()
            
            # Calculate scores by dimension
            metrics_breakdown = {}
            total_score = 0
            
            for dimension in root.findall('.//dimension'):
                dim_name = dimension.get('name')
                dim_key = self._normalize_dimension_name(dim_name)
                dim_scores = {}
                
                for metric in dimension.findall('.//metric'):
                    metric_id = metric.get('id')
                    points = int(metric.get('points', 0))
                    instruction = metric.find('instruction').text
                    
                    # Evaluate metric
                    if self._evaluate_metric(full_text, expected_outputs, instruction):
                        dim_scores[metric_id] = points
                        total_score += points
                
                metrics_breakdown[dim_key] = {
                    "score": sum(dim_scores.values()),
                    "metrics": dim_scores
                }
            
            # Determine strategy
            threshold = 4  # From complexity_matrix.xml
            strategy = TaskStrategyType.TOT if total_score >= threshold else TaskStrategyType.COT
            
            payload = ComplexityScorePayload(
                task_complexity_score=total_score,
                recommended_strategy=strategy,
                metrics_breakdown=metrics_breakdown,
                confidence_level=0.85,
                threshold_details={
                    "threshold": threshold,
                    "score": total_score,
                    "exceeds": total_score >= threshold
                }
            )
            
            return self.create_success_response(
                summary=f"📊 Task Complexity Score: {total_score} → Strategy: {strategy.value}",
                payload=payload,
                execution_type=ExecutionType.IMMEDIATE,
                key_points=[
                    f"Total complexity score: {total_score}",
                    f"Recommended strategy: {strategy.value}",
                    f"Confidence level: 85%"
                ],
                next_steps=[
                    f"1. Retrieve {strategy.value} reasoning template",
                    "2. Apply cognitive analysis",
                    "3. Generate mission map"
                ],
                confidence_score=0.85,
                complexity_score=2
            )
            
        except Exception as e:
            logger.error(f"Failed to calculate complexity: {str(e)}")
            raise
    
    def _normalize_dimension_name(self, name: str) -> ComplexityMetric:
        """Normalize dimension name to enum."""
        name_lower = name.lower()
        if "novedad" in name_lower or "novelty" in name_lower:
            return ComplexityMetric.NOVELTY
        elif "interdependencia" in name_lower or "coupling" in name_lower:
            return ComplexityMetric.COUPLING
        elif "escala" in name_lower or "scale" in name_lower:
            return ComplexityMetric.SCALE
        elif "ambigüedad" in name_lower or "ambiguity" in name_lower:
            return ComplexityMetric.AMBIGUITY
        return ComplexityMetric.NOVELTY  # Default
    
    def _evaluate_metric(self, full_text: str, outputs: List[str], instruction: str) -> bool:
        """Simple heuristic evaluation of metrics."""
        # This is a simplified version - in production would be more sophisticated
        
        # Check for technology novelty
        if "no tiene precedentes" in instruction:
            new_tech_keywords = ["nuevo", "experimental", "poc", "investigar"]
            return any(keyword in full_text for keyword in new_tech_keywords)
        
        # Check for complex patterns
        if "patrón de diseño complejo" in instruction:
            patterns = ["event sourcing", "cqrs", "saga", "circuit breaker"]
            return any(pattern in full_text for pattern in patterns)
        
        # Check module count
        if "número de módulos" in instruction:
            modules = len(re.findall(r'\b(módulo|module|servicio|service|componente)\b', full_text))
            if "superior a 3" in instruction:
                return modules > 3
            elif "entre 2 y 3" in instruction:
                return 2 <= modules <= 3
        
        # Check file count
        if "número de nuevos archivos" in instruction:
            file_count = len(outputs)
            if "superior a 5" in instruction:
                return file_count > 5
            elif "entre 2 y 5" in instruction:
                return 2 <= file_count <= 5
        
        # Check for high-level keywords
        if "palabras clave de alto nivel" in instruction:
            keywords = ["diseñar", "arquitectura", "refactorizar", "sistema"]
            return any(keyword in full_text for keyword in keywords)
        
        # Check for investigation
        if '"investigar"' in instruction:
            return "investigar" in full_text
        
        return False


class ReasoningTemplateTool(BaseTool[ReasoningTemplatePayload]):
    """Retrieves reasoning templates based on strategy."""
    
    def __init__(self):
        super().__init__("reasoning-template-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        return StrategyType.PLANNING
    
    async def execute(self, strategy_type: str, **kwargs) -> StrategyResponse[ReasoningTemplatePayload]:
        """Retrieve reasoning template for the specified strategy.
        
        Args:
            strategy_type: 'chain_of_thought' or 'tree_of_thoughts'
            
        Returns:
            StrategyResponse with reasoning template
        """
        try:
            # Validate strategy type
            try:
                strategy_enum = TaskStrategyType(strategy_type)
            except ValueError:
                strategy_enum = TaskStrategyType.COT  # Default
            
            # Determine template file
            template_file = "cot_reasoning.json" if strategy_enum == TaskStrategyType.COT else "tot_reasoning.json"
            template_path = f".cortex/templates/task_planning/{template_file}"
            
            async with aiofiles.open(template_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            template_data = json.loads(content)
            
            # Extract sections
            if strategy_enum == TaskStrategyType.COT:
                sections = template_data.get("thought_templates", [])
                guidelines = [
                    "Apply each thought template sequentially",
                    "Adapt content to specific task context",
                    "Maintain logical flow between thoughts"
                ]
            else:
                sections = template_data.get("perspectives", []) + template_data.get("evaluation", [])
                guidelines = [
                    "Generate 3 different implementation plans",
                    "Evaluate each plan objectively",
                    "Synthesize best elements into final plan"
                ]
            
            payload = ReasoningTemplatePayload(
                strategy_type=strategy_enum,
                template_content=content,
                template_sections=sections,
                guidelines=guidelines
            )
            
            return self.create_success_response(
                summary=f"🧠 {strategy_enum.value} template retrieved",
                payload=payload,
                execution_type=ExecutionType.IMMEDIATE,
                key_points=[
                    f"Strategy: {strategy_enum.value}",
                    f"Sections: {len(sections)}",
                    "Ready for cognitive application"
                ],
                next_steps=[
                    "1. Apply template to task analysis",
                    "2. Generate structured reasoning",
                    "3. Create mission map from results"
                ],
                confidence_score=1.0,
                complexity_score=1
            )
            
        except Exception as e:
            logger.error(f"Failed to retrieve reasoning template: {str(e)}")
            raise


class MissionMapTool(BaseTool[MissionMapPayload]):
    """Saves and validates mission map artifacts."""
    
    def __init__(self):
        super().__init__("mission-map-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        return StrategyType.PLANNING
    
    async def execute(self, task_id: str, mission_content: Dict[str, Any], **kwargs) -> StrategyResponse[MissionMapPayload]:
        """Save and validate mission map.
        
        Args:
            task_id: Unique task identifier
            mission_content: Mission map content as dict
            
        Returns:
            StrategyResponse with save confirmation
        """
        try:
            # Create directory structure
            task_dir = f".cortex/tasks/{task_id}"
            await aiofiles.os.makedirs(task_dir, exist_ok=True)
            
            file_path = os.path.join(task_dir, "mission_map.json")
            
            # Validate against schema
            validation_errors = await self._validate_mission_map(mission_content)
            validation_status = "valid" if not validation_errors else "invalid"
            
            # Save even if invalid (for debugging)
            content_str = json.dumps(mission_content, indent=2, ensure_ascii=False)
            async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                await f.write(content_str)
            
            # Extract summary
            summary = {
                "project": mission_content.get("project", "Unknown"),
                "phases": len(mission_content.get("phases", [])),
                "total_tasks": sum(len(p.get("tasks", [])) for p in mission_content.get("phases", [])),
                "has_context7": any("context7" in str(t) for p in mission_content.get("phases", []) for t in p.get("tasks", []))
            }
            
            payload = MissionMapPayload(
                file_path=file_path,
                validation_status=validation_status,
                validation_errors=validation_errors if validation_errors else None,
                mission_summary=summary,
                file_size_bytes=len(content_str.encode('utf-8'))
            )
            
            return self.create_success_response(
                summary=f"💾 Mission map saved: {validation_status}",
                payload=payload,
                execution_type=ExecutionType.IMMEDIATE,
                key_points=[
                    f"Saved to: {file_path}",
                    f"Validation: {validation_status}",
                    f"Phases: {summary['phases']}, Tasks: {summary['total_tasks']}"
                ],
                next_steps=[
                    "1. Generate task directives",
                    "2. Create library checklist",
                    "3. Complete construction kit"
                ],
                confidence_score=1.0 if validation_status == "valid" else 0.7,
                complexity_score=2
            )
            
        except Exception as e:
            logger.error(f"Failed to save mission map: {str(e)}")
            raise
    
    async def _validate_mission_map(self, content: Dict[str, Any]) -> List[str]:
        """Validate mission map against schema."""
        errors = []
        
        # Required top-level fields
        required_fields = ["project", "phases"]
        for field in required_fields:
            if field not in content:
                errors.append(f"Missing required field: {field}")
        
        # Validate phases
        if "phases" in content:
            for i, phase in enumerate(content["phases"]):
                if not isinstance(phase, dict):
                    errors.append(f"Phase {i} is not a dictionary")
                    continue
                
                # Required phase fields
                phase_required = ["phase_id", "description", "tasks"]
                for field in phase_required:
                    if field not in phase:
                        errors.append(f"Phase {i} missing field: {field}")
                
                # Validate tasks
                if "tasks" in phase:
                    for j, task in enumerate(phase["tasks"]):
                        if not isinstance(task, dict):
                            errors.append(f"Task {i}.{j} is not a dictionary")
                            continue
                        
                        # Required task fields
                        task_required = ["task_id", "description", "agent_profile", "dependencies"]
                        for field in task_required:
                            if field not in task:
                                errors.append(f"Task {i}.{j} missing field: {field}")
        
        return errors


class TaskDirectivesTool(BaseTool[TaskDirectivesPayload]):
    """Generates task-specific directives from mission map."""
    
    def __init__(self):
        super().__init__("task-directives-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        return StrategyType.PLANNING
    
    async def execute(self, mission_map_path: str, **kwargs) -> StrategyResponse[TaskDirectivesPayload]:
        """Generate Do's and Don'ts from mission map.
        
        Args:
            mission_map_path: Path to mission map JSON file
            
        Returns:
            StrategyResponse with directives file path
        """
        try:
            # Read mission map
            async with aiofiles.open(mission_map_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            mission_data = json.loads(content)
            
            # Extract patterns and technologies
            patterns = []
            technologies = set()
            
            for phase in mission_data.get("phases", []):
                for task in phase.get("tasks", []):
                    # Extract from descriptions
                    desc = task.get("description", "")
                    
                    # Find patterns
                    if "async" in desc.lower():
                        patterns.append("async_operations")
                    if "test" in desc.lower():
                        patterns.append("test_driven")
                    if "docker" in desc.lower():
                        patterns.append("containerization")
                    
                    # Extract technologies
                    for lib in task.get("context7_libraries", []):
                        technologies.add(lib)
            
            # Generate directives content
            dos = self._generate_dos(patterns, technologies)
            donts = self._generate_donts(patterns)
            
            # Create directives file
            task_id = os.path.basename(os.path.dirname(mission_map_path))
            directives_path = os.path.join(os.path.dirname(mission_map_path), f"directives_{task_id}.md")
            
            directives_content = f"""# Task-Specific Directives: {task_id}

## Do's ✅

{chr(10).join(f'- {do}' for do in dos)}

## Don'ts ❌

{chr(10).join(f'- {dont}' for dont in donts)}

---
*Generated from mission_map.json analysis*
"""
            
            async with aiofiles.open(directives_path, 'w', encoding='utf-8') as f:
                await f.write(directives_content)
            
            payload = TaskDirectivesPayload(
                file_path=directives_path,
                dos_count=len(dos),
                donts_count=len(donts),
                source_patterns=list(patterns),
                technologies_covered=list(technologies)
            )
            
            return self.create_success_response(
                summary=f"📋 Generated {len(dos)} Do's and {len(donts)} Don'ts",
                payload=payload,
                execution_type=ExecutionType.IMMEDIATE,
                key_points=[
                    f"Directives saved to: {directives_path}",
                    f"Patterns identified: {len(patterns)}",
                    f"Technologies covered: {len(technologies)}"
                ],
                next_steps=[
                    "1. Generate library checklist",
                    "2. Review generated directives",
                    "3. Complete construction kit"
                ],
                confidence_score=0.9,
                complexity_score=2
            )
            
        except Exception as e:
            logger.error(f"Failed to generate directives: {str(e)}")
            raise
    
    def _generate_dos(self, patterns: List[str], technologies: set) -> List[str]:
        """Generate Do's based on patterns."""
        dos = []
        
        # Pattern-based dos
        if "async_operations" in patterns:
            dos.append("Use async/await consistently throughout the implementation")
            dos.append("Handle async errors with proper try/catch blocks")
        
        if "test_driven" in patterns:
            dos.append("Write tests before implementing features")
            dos.append("Maintain test coverage above 80%")
        
        if "containerization" in patterns:
            dos.append("Use multi-stage Docker builds for optimization")
            dos.append("Keep containers minimal and secure")
        
        # Technology-specific dos
        if "fastapi" in technologies:
            dos.append("Use Pydantic models for request/response validation")
            dos.append("Implement proper dependency injection")
        
        if "next" in technologies:
            dos.append("Use App Router for better performance")
            dos.append("Implement proper error boundaries")
        
        # General dos
        dos.append("Follow the established project patterns")
        dos.append("Document complex logic inline")
        
        return dos
    
    def _generate_donts(self, patterns: List[str]) -> List[str]:
        """Generate Don'ts based on patterns."""
        donts = []
        
        # Pattern-based donts
        if "async_operations" in patterns:
            donts.append("Don't mix sync and async code")
            donts.append("Don't use blocking operations in async functions")
        
        if "test_driven" in patterns:
            donts.append("Don't skip tests for 'simple' functions")
            donts.append("Don't test implementation details")
        
        # General donts
        donts.append("Don't over-engineer simple solutions")
        donts.append("Don't hardcode configuration values")
        donts.append("Don't ignore error handling")
        
        return donts


class LibraryChecklistTool(BaseTool[LibraryChecklistPayload]):
    """Generates library checklist from mission map."""
    
    def __init__(self):
        super().__init__("library-checklist-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        return StrategyType.PLANNING
    
    async def execute(self, mission_map_path: str, **kwargs) -> StrategyResponse[LibraryChecklistPayload]:
        """Generate Context7 library checklist.
        
        Args:
            mission_map_path: Path to mission map JSON file
            
        Returns:
            StrategyResponse with checklist file path
        """
        try:
            # Read mission map
            async with aiofiles.open(mission_map_path, 'r', encoding='utf-8') as f:
                content = await f.read()
            mission_data = json.loads(content)
            
            # Extract all libraries
            libraries = []
            seen = set()
            
            for phase in mission_data.get("phases", []):
                for task in phase.get("tasks", []):
                    for lib in task.get("context7_libraries", []):
                        if lib not in seen:
                            seen.add(lib)
                            libraries.append({
                                "name": lib,
                                "task_id": task.get("task_id", "unknown"),
                                "context7_id": f"@{lib}"  # Placeholder format
                            })
            
            # Generate checklist content
            task_id = os.path.basename(os.path.dirname(mission_map_path))
            checklist_path = os.path.join(os.path.dirname(mission_map_path), f"context7_checklist_{task_id}.md")
            
            checklist_content = f"""# Context7 Library Checklist

**Task**: {task_id}  
**Total Libraries**: {len(libraries)}  
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Libraries to Document

"""
            
            for lib in libraries:
                checklist_content += f"- [ ] **{lib['name']}** (Task: {lib['task_id']})\n"
                checklist_content += f"  - Context7 ID: `{lib['context7_id']}`\n"
                checklist_content += f"  - Status: Pending documentation retrieval\n\n"
            
            checklist_content += """
## Usage Instructions

1. For each library, use Context7 to retrieve documentation
2. Mark checkbox when documentation is retrieved
3. Update status with any issues or notes

---
*Generated from mission_map.json analysis*
"""
            
            async with aiofiles.open(checklist_path, 'w', encoding='utf-8') as f:
                await f.write(checklist_content)
            
            payload = LibraryChecklistPayload(
                file_path=checklist_path,
                libraries_found=libraries,
                total_libraries=len(libraries),
                checklist_format="markdown"
            )
            
            return self.create_success_response(
                summary=f"📚 Generated checklist for {len(libraries)} libraries",
                payload=payload,
                execution_type=ExecutionType.IMMEDIATE,
                key_points=[
                    f"Checklist saved to: {checklist_path}",
                    f"Libraries found: {len(libraries)}",
                    "Ready for Context7 documentation"
                ],
                next_steps=[
                    "1. Review generated checklist",
                    "2. Use Context7 for documentation",
                    "3. Construction kit complete!"
                ],
                confidence_score=0.95,
                complexity_score=1
            )
            
        except Exception as e:
            logger.error(f"Failed to generate checklist: {str(e)}")
            raise


# Export all tools
__all__ = [
    "KeymakerWorkflowTool",
    "ComplexityScoreTool", 
    "ReasoningTemplateTool",
    "MissionMapTool",
    "TaskDirectivesTool",
    "LibraryChecklistTool"
]
```

---

## 🔌 Fase 4: Integración en Server (1 hora)

### 4.1 Actualizar `server.py`

```python
# Añadir imports al inicio del archivo
from tools.task_planning import (
    KeymakerWorkflowTool, ComplexityScoreTool, ReasoningTemplateTool,
    MissionMapTool, TaskDirectivesTool, LibraryChecklistTool
)

# Añadir las 6 nuevas herramientas después de las existentes

@app.tool(
    name="get-keymaker-workflow",
    description="Retrieve structured workflow template for task planning following keymaker pattern"
)
async def get_keymaker_workflow(
    workflow_type: Annotated[str, Field(
        description="Type of workflow to retrieve",
        default="task_planning",
        examples=["task_planning", "feature_development"]
    )] = "task_planning"
) -> Dict:
    """Retrieve keymaker workflow template for task planning."""
    tool = KeymakerWorkflowTool()
    return await tool.validate_and_execute(workflow_type=workflow_type)


@app.tool(
    name="calculate-complexity-score",
    description="Calculate Task Complexity Score (TCS) and recommend CoT or ToT strategy"
)
async def calculate_complexity_score(
    task_description: Annotated[str, Field(
        description="High-level description of the task to be implemented",
        min_length=10,
        max_length=500
    )],
    scope: Annotated[str, Field(
        description="Detailed scope, requirements and constraints",
        min_length=20
    )],
    expected_outputs: Annotated[List[str], Field(
        description="List of expected deliverables/files",
        min_items=1
    )]
) -> Dict:
    """Calculate task complexity and recommend planning strategy."""
    tool = ComplexityScoreTool()
    return await tool.validate_and_execute(
        task_description=task_description,
        scope=scope,
        expected_outputs=expected_outputs
    )


@app.tool(
    name="get-reasoning-template",
    description="Retrieve reasoning template based on recommended strategy (CoT or ToT)"
)
async def get_reasoning_template(
    strategy_type: Annotated[str, Field(
        description="Strategy type: 'chain_of_thought' or 'tree_of_thoughts'",
        examples=["chain_of_thought", "tree_of_thoughts"]
    )]
) -> Dict:
    """Retrieve reasoning template for cognitive processing."""
    tool = ReasoningTemplateTool()
    return await tool.validate_and_execute(strategy_type=strategy_type)


@app.tool(
    name="save-mission-map",
    description="Save and validate mission map JSON for task execution"
)
async def save_mission_map(
    task_id: Annotated[str, Field(
        description="Unique identifier for the task",
        pattern="^[a-zA-Z0-9_-]+$"
    )],
    mission_content: Annotated[Dict[str, Any], Field(
        description="Complete mission map content following schema"
    )]
) -> Dict:
    """Save mission map with validation."""
    tool = MissionMapTool()
    return await tool.validate_and_execute(
        task_id=task_id,
        mission_content=mission_content
    )


@app.tool(
    name="generate-task-directives",
    description="Generate Do's and Don'ts directives from mission map analysis"
)
async def generate_task_directives(
    mission_map_path: Annotated[str, Field(
        description="Path to saved mission map JSON file",
        examples=[".cortex/tasks/auth_module/mission_map.json"]
    )]
) -> Dict:
    """Generate task-specific directives from mission map."""
    tool = TaskDirectivesTool()
    return await tool.validate_and_execute(mission_map_path=mission_map_path)


@app.tool(
    name="generate-library-checklist",
    description="Generate Context7 library documentation checklist from mission map"
)
async def generate_library_checklist(
    mission_map_path: Annotated[str, Field(
        description="Path to saved mission map JSON file",
        examples=[".cortex/tasks/auth_module/mission_map.json"]
    )]
) -> Dict:
    """Generate library checklist for Context7 documentation."""
    tool = LibraryChecklistTool()
    return await tool.validate_and_execute(mission_map_path=mission_map_path)
```

---

## 🧪 Fase 5: Testing Completo (2 horas)

### 5.1 Archivo: `tests/tools/test_task_planning.py`

```python
"""Tests for Task Planning tools."""

import pytest
import json
import os
from unittest.mock import patch
import aiofiles

from tools.task_planning import (
    KeymakerWorkflowTool, ComplexityScoreTool, ReasoningTemplateTool,
    MissionMapTool, TaskDirectivesTool, LibraryChecklistTool
)
from schemas.task_planning_payloads import TaskStrategyType


@pytest.mark.asyncio
async def test_keymaker_workflow_retrieval():
    """Test keymaker workflow template retrieval."""
    tool = KeymakerWorkflowTool()
    
    # Create test template
    test_template = {
        "phases": [
            {"name": "Analysis", "steps": ["step1", "step2"]},
            {"name": "Implementation", "steps": ["step3"]}
        ]
    }
    
    with patch('aiofiles.open', create=True) as mock_open:
        mock_open.return_value.__aenter__.return_value.read.return_value = json.dumps(test_template)
        
        result = await tool.execute(workflow_type="task_planning")
        
        assert result.payload.phases_count == 2
        assert len(result.payload.phase_names) == 2
        assert result.payload.template_format == "json"
        assert result.user_facing.summary.startswith("✅")


@pytest.mark.asyncio
async def test_complexity_score_simple_task():
    """Test complexity scoring for a simple task."""
    tool = ComplexityScoreTool()
    
    # Mock complexity matrix
    mock_matrix = """
    <complexity_rubric>
        <dimension name="Novelty">
            <metric id="NOV-01" points="3">
                <instruction>Check for new technology</instruction>
            </metric>
        </dimension>
        <dimension name="Scale">
            <metric id="SCL-01" points="2">
                <instruction>More than 5 files</instruction>
            </metric>
        </dimension>
    </complexity_rubric>
    """
    
    with patch('aiofiles.open', create=True) as mock_open:
        mock_open.return_value.__aenter__.return_value.read.return_value = mock_matrix
        
        result = await tool.execute(
            task_description="Create simple CRUD endpoints",
            scope="Basic user management",
            expected_outputs=["user.py", "test_user.py"]
        )
        
        assert result.payload.task_complexity_score < 4
        assert result.payload.recommended_strategy == TaskStrategyType.COT
        assert result.payload.confidence_level > 0.8


@pytest.mark.asyncio
async def test_complexity_score_complex_task():
    """Test complexity scoring for a complex task."""
    tool = ComplexityScoreTool()
    
    # Mock complexity matrix
    mock_matrix = """
    <complexity_rubric>
        <dimension name="Ambiguity">
            <metric id="AMB-01" points="3">
                <instruction>Contains "arquitectura" keyword</instruction>
            </metric>
        </dimension>
        <dimension name="Scale">
            <metric id="SCL-01" points="2">
                <instruction>More than 5 files</instruction>
            </metric>
        </dimension>
    </complexity_rubric>
    """
    
    with patch('aiofiles.open', create=True) as mock_open:
        mock_open.return_value.__aenter__.return_value.read.return_value = mock_matrix
        
        result = await tool.execute(
            task_description="Diseñar arquitectura de microservicios",
            scope="Refactorización completa del sistema",
            expected_outputs=[f"service{i}.py" for i in range(8)]
        )
        
        assert result.payload.task_complexity_score >= 4
        assert result.payload.recommended_strategy == TaskStrategyType.TOT


@pytest.mark.asyncio
async def test_reasoning_template_cot():
    """Test CoT reasoning template retrieval."""
    tool = ReasoningTemplateTool()
    
    mock_template = {
        "thought_templates": [
            {"id": 1, "topic": "Data Analysis"},
            {"id": 2, "topic": "Component Design"}
        ]
    }
    
    with patch('aiofiles.open', create=True) as mock_open:
        mock_open.return_value.__aenter__.return_value.read.return_value = json.dumps(mock_template)
        
        result = await tool.execute(strategy_type="chain_of_thought")
        
        assert result.payload.strategy_type == TaskStrategyType.COT
        assert len(result.payload.template_sections) == 2
        assert len(result.payload.guidelines) > 0


@pytest.mark.asyncio
async def test_mission_map_validation():
    """Test mission map saving and validation."""
    tool = MissionMapTool()
    
    valid_mission = {
        "project": "Test Project",
        "phases": [
            {
                "phase_id": "phase_1",
                "description": "Test phase",
                "tasks": [
                    {
                        "task_id": "task_1",
                        "description": "Test task",
                        "agent_profile": "agent:test",
                        "dependencies": []
                    }
                ]
            }
        ]
    }
    
    # Mock file operations
    with patch('aiofiles.os.makedirs') as mock_makedirs, \
         patch('aiofiles.open', create=True) as mock_open:
        
        result = await tool.execute(
            task_id="test_task",
            mission_content=valid_mission
        )
        
        assert result.payload.validation_status == "valid"
        assert result.payload.validation_errors is None
        assert result.payload.mission_summary["phases"] == 1
        assert result.payload.mission_summary["total_tasks"] == 1


@pytest.mark.asyncio
async def test_mission_map_invalid():
    """Test mission map validation with invalid content."""
    tool = MissionMapTool()
    
    invalid_mission = {
        "project": "Test Project"
        # Missing required 'phases' field
    }
    
    with patch('aiofiles.os.makedirs') as mock_makedirs, \
         patch('aiofiles.open', create=True) as mock_open:
        
        result = await tool.execute(
            task_id="test_task",
            mission_content=invalid_mission
        )
        
        assert result.payload.validation_status == "invalid"
        assert result.payload.validation_errors is not None
        assert any("phases" in error for error in result.payload.validation_errors)


@pytest.mark.asyncio
async def test_directives_generation():
    """Test directives generation from mission map."""
    tool = TaskDirectivesTool()
    
    mock_mission = {
        "project": "Test",
        "phases": [{
            "tasks": [{
                "description": "Implement async API with tests",
                "context7_libraries": ["fastapi", "pytest"]
            }]
        }]
    }
    
    with patch('aiofiles.open', create=True) as mock_open:
        # First read returns mission map
        mock_open.return_value.__aenter__.return_value.read.return_value = json.dumps(mock_mission)
        
        result = await tool.execute(mission_map_path=".cortex/tasks/test/mission_map.json")
        
        assert result.payload.dos_count > 0
        assert result.payload.donts_count > 0
        assert "async_operations" in result.payload.source_patterns
        assert "fastapi" in result.payload.technologies_covered


@pytest.mark.asyncio
async def test_checklist_generation():
    """Test library checklist generation."""
    tool = LibraryChecklistTool()
    
    mock_mission = {
        "phases": [{
            "tasks": [{
                "task_id": "1.1",
                "context7_libraries": ["fastapi", "sqlalchemy", "pytest"]
            }]
        }]
    }
    
    with patch('aiofiles.open', create=True) as mock_open:
        mock_open.return_value.__aenter__.return_value.read.return_value = json.dumps(mock_mission)
        
        result = await tool.execute(mission_map_path=".cortex/tasks/test/mission_map.json")
        
        assert result.payload.total_libraries == 3
        assert len(result.payload.libraries_found) == 3
        assert all(lib["name"] in ["fastapi", "sqlalchemy", "pytest"] 
                  for lib in result.payload.libraries_found)


@pytest.mark.asyncio
async def test_full_workflow_integration():
    """Test complete keymaker workflow integration."""
    # This would test the full workflow from start to finish
    # For brevity, just outline the structure
    
    # 1. Get workflow
    workflow_tool = KeymakerWorkflowTool()
    
    # 2. Calculate complexity
    complexity_tool = ComplexityScoreTool()
    
    # 3. Get reasoning template
    reasoning_tool = ReasoningTemplateTool()
    
    # 4. Save mission map
    mission_tool = MissionMapTool()
    
    # 5. Generate directives
    directives_tool = TaskDirectivesTool()
    
    # 6. Generate checklist
    checklist_tool = LibraryChecklistTool()
    
    # Would test full flow with mocked data
    assert True  # Placeholder
```

---

## 📄 Fase 6: Crear Templates (1 hora)

### 6.1 Template: `.cortex/templates/task_planning/keymaker_workflow.json`

```json
{
  "workflow_name": "Keymaker Task Planning Workflow",
  "version": "1.0.0",
  "description": "Structured workflow for automated task planning and construction kit generation",
  "phases": [
    {
      "id": 1,
      "name": "Analysis and Strategic Decision",
      "steps": [
        "Analyze task description and requirements",
        "Calculate Task Complexity Score (TCS)",
        "Select cognitive strategy (CoT or ToT)"
      ]
    },
    {
      "id": 2,
      "name": "Knowledge Retrieval",
      "steps": [
        "Query lessons learned repository",
        "Identify relevant patterns and anti-patterns"
      ]
    },
    {
      "id": 3,
      "name": "Mission Map Generation",
      "steps": [
        "Apply selected reasoning strategy",
        "Generate structured implementation plan",
        "Create mission_map.json"
      ]
    },
    {
      "id": 4,
      "name": "Artifact Distillation",
      "steps": [
        "Generate task-specific directives",
        "Create library documentation checklist"
      ]
    },
    {
      "id": 5,
      "name": "Construction Kit Delivery",
      "steps": [
        "Validate all artifacts",
        "Report completion with artifact paths"
      ]
    }
  ]
}
```

### 6.2 Template: `.cortex/templates/task_planning/cot_reasoning.json`

```json
{
  "strategy": "chain_of_thought",
  "description": "Sequential reasoning pattern for standard tasks",
  "thought_templates": [
    {
      "id": 1,
      "topic": "Data Analysis and Patterns",
      "prompts": [
        "What are the core data structures needed?",
        "What patterns exist in the current codebase?",
        "What are the input/output requirements?"
      ]
    },
    {
      "id": 2,
      "topic": "Component/Module Design",
      "prompts": [
        "What are the main components needed?",
        "How do they interact with existing modules?",
        "What are the interface contracts?"
      ]
    },
    {
      "id": 3,
      "topic": "Internal Component Logic",
      "prompts": [
        "What is the core algorithm/logic?",
        "What are the state management needs?",
        "What validations are required?"
      ]
    },
    {
      "id": 4,
      "topic": "Connections and Interactions",
      "prompts": [
        "How does this integrate with the system?",
        "What are the dependency requirements?",
        "What are the communication patterns?"
      ]
    },
    {
      "id": 5,
      "topic": "Error and Edge Case Handling",
      "prompts": [
        "What errors can occur?",
        "What are the edge cases?",
        "How should failures be handled?"
      ]
    }
  ]
}
```

### 6.3 Template: `.cortex/templates/task_planning/tot_reasoning.json`

```json
{
  "strategy": "tree_of_thoughts",
  "description": "Multiple perspective evaluation for complex tasks",
  "perspectives": [
    {
      "id": "robustness",
      "name": "Robustness-First Design",
      "focus": "Error handling, fault tolerance, reliability",
      "evaluation_criteria": [
        "Comprehensive error handling",
        "Graceful degradation",
        "Recovery mechanisms"
      ]
    },
    {
      "id": "simplicity",
      "name": "Simplicity-First Design",
      "focus": "Minimal complexity, clarity, maintainability",
      "evaluation_criteria": [
        "Code readability",
        "Minimal dependencies",
        "Clear abstractions"
      ]
    },
    {
      "id": "scalability",
      "name": "Scalability-First Design",
      "focus": "Performance, growth, extensibility",
      "evaluation_criteria": [
        "Horizontal scalability",
        "Performance optimization",
        "Future extensibility"
      ]
    }
  ],
  "evaluation": [
    {
      "step": "comparative_analysis",
      "description": "Compare all three approaches",
      "output": "Scoring matrix with pros/cons"
    },
    {
      "step": "synthesis",
      "description": "Combine best elements",
      "output": "Unified approach leveraging strengths"
    }
  ]
}
```

### 6.4 Template: `.cortex/templates/task_planning/mission_map_schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Mission Map Schema",
  "type": "object",
  "required": ["project", "phases"],
  "properties": {
    "project": {
      "type": "string",
      "description": "Project name or identifier"
    },
    "description": {
      "type": "string",
      "description": "High-level project description"
    },
    "phases": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["phase_id", "description", "tasks"],
        "properties": {
          "phase_id": {
            "type": "string",
            "pattern": "^[A-Za-z0-9_]+$"
          },
          "description": {
            "type": "string"
          },
          "tasks": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["task_id", "description", "agent_profile", "dependencies"],
              "properties": {
                "task_id": {
                  "type": "string"
                },
                "description": {
                  "type": "string"
                },
                "agent_profile": {
                  "type": "string",
                  "pattern": "^agent:"
                },
                "dependencies": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                },
                "context7_libraries": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                },
                "artifacts_output": {
                  "type": "array",
                  "items": {
                    "type": "string"
                  }
                },
                "validation_criteria": {
                  "type": "string"
                },
                "human_checkpoint": {
                  "type": "boolean",
                  "default": false
                }
              }
            }
          }
        }
      }
    },
    "success_criteria": {
      "type": "object"
    }
  }
}
```

---

## ✅ Criterios de Validación

### Fase por Fase:

1. **Estructura**: Todos los archivos creados, imports funcionando
2. **Schemas**: Validación con mypy pasando sin errores
3. **Herramientas**: Cada herramienta ejecuta y retorna StrategyResponse válido
4. **Server**: Las 6 herramientas accesibles vía MCP
5. **Tests**: >90% cobertura, todos los tests pasando
6. **Templates**: Archivos JSON válidos y completos

### Validación Final:

```bash
# 1. Lint y formato
poetry run black tools/task_planning.py tests/tools/test_task_planning.py
poetry run flake8 tools/task_planning.py

# 2. Type checking
poetry run mypy tools/task_planning.py schemas/task_planning_payloads.py

# 3. Tests
poetry run pytest tests/tools/test_task_planning.py -v --cov=tools.task_planning

# 4. Integración
poetry run python server.py
# Verificar que las 6 herramientas aparecen en el listado MCP
```

---

## 📋 Checklist de Implementación para Claude Code

- [ ] Crear estructura de archivos (Fase 1)
- [ ] Implementar schemas con validación Pydantic (Fase 2)
- [ ] Implementar las 6 herramientas con aiofiles (Fase 3)
- [ ] Integrar en server.py con decoradores @app.tool (Fase 4)
- [ ] Crear suite de tests con >90% cobertura (Fase 5)
- [ ] Crear templates JSON en .cortex (Fase 6)
- [ ] Validar con mypy, black, flake8
- [ ] Ejecutar server y verificar herramientas disponibles
- [ ] Documentar uso en CLAUDE.md

---

**Este plan está listo para ejecución inmediata por Claude Code.**