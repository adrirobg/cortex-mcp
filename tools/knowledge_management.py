#!/usr/bin/env python3
"""Knowledge Management Tools for CortexMCP.

Implements the Knowledge Management MVP with start-retrospective and 
process-retrospective tools for systematic organizational memory capture.

Following the 4 Principios Rectores:
1. Dogmatismo con Universal Response Schema ✅
2. Servidor como Ejecutor Fiable ✅ 
3. Estado en Claude, NO en Servidor ✅
4. Testing Concurrente ✅
"""

import json
import os
import re
from datetime import datetime
from typing import Optional
import aiofiles
import aiofiles.os

from tools.base_tool import BaseTool
from schemas.universal_response import StrategyResponse, StrategyType, ExecutionType, Action
from schemas.knowledge_payloads import (
    RetrospectivePayload,
    KnowledgeIntegrationPayload,
    RetrospectiveStatus,
    KnowledgeIntegrationStatus,
    RetrospectiveSection,
    ImprovementSuggestion
)



# ========================================
# MODERN BASETOOL ARCHITECTURE
# Following Principio Rector #1: Universal Response Schema
# ========================================

class RetrospectiveTool(BaseTool[RetrospectivePayload]):
    """Retrospective Tool - Modern BaseTool implementation.
    
    Creates structured retrospective drafts with full schema validation and MCP compliance.
    Following the CortexMCP-Plus architecture pattern.
    """
    
    def __init__(self):
        """Initialize retrospective tool."""
        super().__init__("retrospective-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        """Get strategy type for retrospective tool."""
        return StrategyType.LEARNING
    
    async def execute(
        self,
        task_name: str,
        phase_context: Optional[str] = None,
        duration_estimate: Optional[str] = None,
        **kwargs
    ) -> StrategyResponse[RetrospectivePayload]:
        """Execute retrospective creation.
        
        Args:
            task_name: Name/description of completed task
            phase_context: Optional phase or project context
            duration_estimate: Optional duration information
            **kwargs: Additional parameters (unused in MVP)
            
        Returns:
            StrategyResponse[RetrospectivePayload]: Structured response with retrospective data
        """
        try:
            # Validate inputs
            if len(task_name.strip()) < 3:
                raise ValueError("task_name must be at least 3 characters long")
            if len(task_name) > 200:
                raise ValueError("task_name must be at most 200 characters long")
            
            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y-%m-%d")
            safe_task_name = "".join(c for c in task_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_task_name = safe_task_name.replace(' ', '_').lower()
            filename = f"{timestamp}_{safe_task_name}.md"
            filepath = os.path.join(".cortex", "retrospectives", filename)
            
            # Define template sections
            template_sections = [
                "Executive Summary",
                "Process Efficiency Analysis",
                "Architecture Analysis", 
                "Bottlenecks and Friction Analysis",
                "Improvement Suggestions",
                "Key Learnings & Action Items"
            ]
            
            sections_detail = [
                RetrospectiveSection(name="Executive Summary", description="Brief overview of the task, objectives, and key outcomes"),
                RetrospectiveSection(name="Process Efficiency Analysis", description="Plan vs. reality comparison, achievements, and deviations"),
                RetrospectiveSection(name="Architecture Analysis", description="Adherence to core principles and code quality assessment"),
                RetrospectiveSection(name="Bottlenecks and Friction Analysis", description="Time distribution and process friction identification"),
                RetrospectiveSection(name="Improvement Suggestions", description="Specific, actionable improvement recommendations"),
                RetrospectiveSection(name="Key Learnings & Action Items", description="Successes, improvements, and specific next steps")
            ]
            
            # Create retrospective template
            template_content = f"""# Retrospective: {task_name}

**Date**: {datetime.now().strftime("%Y-%m-%d")}  
**Phase Context**: {phase_context or "Not specified"}  
**Duration**: {duration_estimate or "Not specified"}  
**Analysis Confidence**: [To be completed by Claude]  

---

## 🎯 Executive Summary

[Provide a brief overview of the task, its objectives, and key outcomes]

---

## 📊 Process Efficiency Analysis

### Plan vs. Reality Comparison
[Compare original expectations with actual execution]

### Achievements
[List what went well and was accomplished successfully]

### Deviations  
[Identify areas where execution differed from plan]

---

## 🏗️ Architecture Analysis

### Adherence to Core Principles
[Evaluate how well the implementation followed established principles]

### Code Quality Assessment
[Assess the quality of technical decisions and implementations]

---

## 🚧 Bottlenecks and Friction Analysis

### Time Distribution Analysis
[Break down where time was spent and identify inefficiencies]

### Process Friction Identified
[Identify specific obstacles and smooth processes]

---

## 📋 Improvement Suggestions

### Specific Recommendations
[Provide concrete, actionable improvement suggestions]

---

## 📊 Key Learnings & Action Items

### What Went Well
[Celebrate successes and effective practices]

### What Could Be Improved
[Honest assessment of areas for improvement]

### Action Items
[Specific next steps and follow-up tasks]

---

*Retrospective generated by RetrospectiveTool*  
*To be completed by Claude analysis*  
*File: {filepath}*
"""
            
            # Ensure directory exists
            await aiofiles.os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Write template to file
            async with aiofiles.open(filepath, 'w', encoding='utf-8') as f:
                await f.write(template_content)
            
            file_size = len(template_content.encode('utf-8'))
            
            payload = RetrospectivePayload(
                workflow_stage="retrospective_creation",
                task_name=task_name,
                retrospective_file=filepath,
                retrospective_status=RetrospectiveStatus.DRAFT_CREATED,
                phase_context=phase_context,
                duration_estimate=duration_estimate,
                template_sections=template_sections,
                sections_detail=sections_detail,
                file_size_bytes=file_size,
                timestamp=datetime.now().isoformat(),
                next_tool="process-retrospective",
                analysis_guidance=[
                    "Read the generated template carefully",
                    "Complete each section with thoughtful analysis",
                    "Focus on concrete insights and actionable improvements",
                    "Maintain honest assessment of both successes and challenges",
                    "Ensure analysis provides value for future planning"
                ],
                suggested_next_state={
                    "retrospective_created": True,
                    "retrospective_file": filepath,
                    "task_name": task_name,
                    "requires_analysis": True,
                    "workflow_stage": "analysis_required"
                }
            )
            
            return self.create_success_response(
                summary=f"📝 Retrospective draft created for '{task_name}'",
                payload=payload,
                execution_type=ExecutionType.IMMEDIATE,
                actions=[
                    Action(
                        type="complete_retrospective_analysis",
                        description=f"Complete the retrospective analysis in {filepath}",
                        priority=1,
                        validation_criteria="All sections completed with thoughtful analysis",
                        parameters={
                            "retrospective_file": filepath,
                            "task_name": task_name,
                            "sections": template_sections
                        }
                    )
                ],
                key_points=[
                    f"✅ Created structured template: {filepath}",
                    "📋 Template includes standard analysis sections",
                    "🧠 Ready for Claude intelligence completion",
                    "💾 Saved in .cortex/retrospectives/ knowledge base",
                    f"📊 Template size: {file_size} bytes"
                ],
                next_steps=[
                    "1. Review the generated template structure",
                    "2. Complete each section with detailed analysis",
                    "3. Focus on actionable insights and learnings",
                    "4. Use process-retrospective tool when complete"
                ],
                confidence_score=1.0,
                complexity_score=1,
                estimated_duration="immediate",
                performance_hints=[
                    "Template generation is deterministic and fast",
                    "Analysis completion time depends on task complexity"
                ],
                learning_opportunities=[
                    "Structured retrospective methodology",
                    "Systematic knowledge capture processes"
                ]
            )
            
        except Exception as e:
            payload = RetrospectivePayload(
                workflow_stage="error",
                task_name=task_name,
                retrospective_file="unknown",
                retrospective_status=RetrospectiveStatus.ERROR,
                phase_context=phase_context,
                duration_estimate=duration_estimate,
                error_message=f"Retrospective creation failed: {str(e)}",
                suggested_next_state={
                    "retrospective_created": False,
                    "task_name": task_name,
                    "error_occurred": True,
                    "error_type": "creation_failure"
                }
            )
            
            return self.create_success_response(
                summary=f"❌ Error creating retrospective for '{task_name}'",
                payload=payload,
                execution_type=ExecutionType.USER_CONFIRMATION,
                actions=[
                    Action(
                        type="retry_retrospective_creation",
                        description="Retry retrospective creation after fixing error",
                        priority=1,
                        validation_criteria="Error resolved and retrospective created",
                        parameters={"task_name": task_name, "error": str(e)}
                    )
                ],
                key_points=[
                    f"Retrospective creation failed: {str(e)}",
                    "Check file system permissions",
                    "Verify .cortex/retrospectives/ directory access",
                    "Task name may contain invalid characters"
                ],
                next_steps=[
                    "1. Check error message for specific issue",
                    "2. Verify file system permissions",
                    "3. Ensure retrospectives directory exists",
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
                    "Error handling in file operations",
                    "Retrospective creation debugging"
                ]
            )


class KnowledgeIntegrationTool(BaseTool[KnowledgeIntegrationPayload]):
    """Knowledge Integration Tool - Modern BaseTool implementation.
    
    Processes retrospectives and integrates insights with full schema validation and MCP compliance.
    Following the CortexMCP-Plus architecture pattern.
    """
    
    def __init__(self):
        """Initialize knowledge integration tool."""
        super().__init__("knowledge-integration-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        """Get strategy type for knowledge integration tool."""
        return StrategyType.LEARNING
    
    async def execute(self, retrospective_file: str, **kwargs) -> StrategyResponse[KnowledgeIntegrationPayload]:
        """Execute knowledge integration from retrospective.
        
        Args:
            retrospective_file: Path to completed retrospective file
            **kwargs: Additional parameters (unused in MVP)
            
        Returns:
            StrategyResponse[KnowledgeIntegrationPayload]: Structured response with integration results
        """
        try:
            # Validate file exists
            if not await aiofiles.os.path.exists(retrospective_file):
                raise ValueError(f"Retrospective file not found: {retrospective_file}")
            
            # Read retrospective content
            async with aiofiles.open(retrospective_file, 'r', encoding='utf-8') as f:
                content = await f.read()
            
            # Extract improvement suggestions (enhanced parsing)
            improvements_section = re.search(r'##.*Improvement Suggestions(.*?)(?=##|$)', content, re.DOTALL)
            action_items_section = re.search(r'##.*Key Learnings.*Action Items(.*?)(?=##|$)', content, re.DOTALL)
            
            extracted_improvements = []
            
            # Process improvement suggestions
            if improvements_section:
                suggestions = re.findall(r'[-*]\s*(.+)', improvements_section.group(1))
                for i, suggestion in enumerate(suggestions):
                    if len(suggestion.strip()) > 10:  # Filter meaningful suggestions
                        improvement = ImprovementSuggestion(
                            id=f"retro_{datetime.now().strftime('%Y%m%d')}_{i+1:03d}",
                            title=suggestion.strip()[:80] + "..." if len(suggestion.strip()) > 80 else suggestion.strip(),
                            description=suggestion.strip(),
                            category="workflow",
                            source="retrospective_analysis",
                            priority_score=3.0,
                            effort_estimate=3,
                            impact_estimate=3
                        )
                        extracted_improvements.append(improvement)
            
            # Process action items
            if action_items_section:
                actions = re.findall(r'[-*]\s*(.+)', action_items_section.group(1))
                for i, action in enumerate(actions):
                    if len(action.strip()) > 10:
                        improvement = ImprovementSuggestion(
                            id=f"action_{datetime.now().strftime('%Y%m%d')}_{i+1:03d}",
                            title=action.strip()[:80] + "..." if len(action.strip()) > 80 else action.strip(),
                            description=action.strip(),
                            category="action_item",
                            source="retrospective_action_items",
                            priority_score=4.0,  # Action items typically higher priority
                            effort_estimate=3,
                            impact_estimate=4
                        )
                        extracted_improvements.append(improvement)
            
            # Load existing improvements.json
            improvements_file = ".cortex/ideas/improvements.json"
            try:
                async with aiofiles.open(improvements_file, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    improvements_data = json.loads(content)
            except FileNotFoundError:
                # Create basic structure if file doesn't exist
                improvements_data = {
                    "improvements": [],
                    "metrics": {"total_improvements": 0}
                }
                # Ensure directory exists
                await aiofiles.os.makedirs(os.path.dirname(improvements_file), exist_ok=True)
            
            # Add new improvements
            new_improvement_ids = []
            for improvement in extracted_improvements:
                # Generate unique ID if needed
                existing_ids = [imp.get("id", "") for imp in improvements_data.get("improvements", [])]
                if improvement.id in existing_ids:
                    # Append counter to make unique
                    counter = 1
                    base_id = improvement.id
                    while f"{base_id}_{counter}" in existing_ids:
                        counter += 1
                    improvement.id = f"{base_id}_{counter}"
                
                # Add improvement entry (convert to dict for JSON serialization)
                new_improvement = {
                    "id": improvement.id,
                    "title": improvement.title,
                    "description": improvement.description,
                    "category": improvement.category,
                    "source": improvement.source,
                    "date_added": datetime.now().strftime("%Y-%m-%d"),
                    "priority": {
                        "effort": improvement.effort_estimate,
                        "impact": improvement.impact_estimate,
                        "score": improvement.priority_score
                    },
                    "status": "identified",
                    "implementation_plan": None,
                    "related_phases": [],
                    "tags": ["retrospective_analysis", "knowledge_management"]
                }
                
                improvements_data["improvements"].append(new_improvement)
                new_improvement_ids.append(improvement.id)
            
            # Update metrics
            improvements_data["metrics"]["total_improvements"] = len(improvements_data["improvements"])
            improvements_data["metrics"]["last_updated"] = datetime.now().isoformat()
            
            # Save updated improvements.json
            async with aiofiles.open(improvements_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(improvements_data, indent=2, ensure_ascii=False))
            
            # Prepare sections processed
            sections_processed = []
            if improvements_section:
                sections_processed.append("Improvement Suggestions")
            if action_items_section:
                sections_processed.append("Key Learnings & Action Items")
            
            payload = KnowledgeIntegrationPayload(
                workflow_stage="integration_complete",
                retrospective_file=retrospective_file,
                integration_status=KnowledgeIntegrationStatus.INTEGRATION_COMPLETE,
                improvements_extracted=len(extracted_improvements),
                new_improvement_ids=new_improvement_ids,
                extracted_improvements=extracted_improvements,
                knowledge_artifacts=[improvements_file, retrospective_file],
                improvements_file=improvements_file,
                total_improvements=improvements_data["metrics"]["total_improvements"],
                integration_timestamp=datetime.now().isoformat(),
                sections_processed=sections_processed,
                parsing_success=True,
                next_recommendations=[
                    "Review newly added improvements for prioritization",
                    "Consider using strategy-architect for implementation planning",
                    "Continue systematic knowledge capture for future tasks"
                ],
                prioritization_suggestions=[
                    "Focus on high-impact, low-effort improvements first",
                    "Group related improvements for batch implementation",
                    "Consider dependencies between improvements"
                ],
                suggested_next_state={
                    "knowledge_integrated": True,
                    "retrospective_file": retrospective_file,
                    "improvements_added": len(extracted_improvements),
                    "workflow_complete": True
                }
            )
            
            return self.create_success_response(
                summary=f"🧠 Knowledge integrated from retrospective: {os.path.basename(retrospective_file)}",
                payload=payload,
                execution_type=ExecutionType.IMMEDIATE,
                actions=[
                    Action(
                        type="knowledge_integration_complete",
                        description="Retrospective knowledge has been successfully integrated",
                        priority=1,
                        validation_criteria="All insights extracted and stored in knowledge base",
                        parameters={
                            "retrospective_file": retrospective_file,
                            "improvements_added": len(extracted_improvements),
                            "total_improvements": improvements_data["metrics"]["total_improvements"]
                        }
                    )
                ],
                key_points=[
                    f"📊 Extracted {len(extracted_improvements)} new insights",
                    f"💾 Updated improvements database: {len(new_improvement_ids)} additions",
                    f"🎯 Total improvements now: {improvements_data['metrics']['total_improvements']}",
                    "✅ Knowledge successfully institutionalized",
                    f"📁 Knowledge artifacts: {', '.join(os.path.basename(f) for f in [improvements_file, retrospective_file])}"
                ],
                next_steps=[
                    "1. Review newly added improvements in .cortex/ideas/improvements.json",
                    "2. Consider prioritizing high-impact improvements for implementation",
                    "3. Use strategy-architect for detailed implementation planning",
                    "4. Continue knowledge capture cycle for future tasks"
                ],
                confidence_score=0.9,
                complexity_score=2,
                estimated_duration="immediate",
                performance_hints=[
                    "Knowledge integration is automated and deterministic",
                    "Processing time depends on retrospective content size"
                ],
                learning_opportunities=[
                    "Systematic knowledge extraction from retrospectives",
                    "Automated improvement identification and categorization"
                ]
            )
            
        except Exception as e:
            payload = KnowledgeIntegrationPayload(
                workflow_stage="error",
                retrospective_file=retrospective_file,
                integration_status=KnowledgeIntegrationStatus.ERROR,
                improvements_extracted=0,
                parsing_success=False,
                error_message=f"Knowledge integration failed: {str(e)}",
                suggested_next_state={
                    "knowledge_integrated": False,
                    "retrospective_file": retrospective_file,
                    "error_occurred": True,
                    "error_type": "integration_failure"
                }
            )
            
            return self.create_success_response(
                summary=f"❌ Error integrating knowledge from retrospective",
                payload=payload,
                execution_type=ExecutionType.USER_CONFIRMATION,
                actions=[
                    Action(
                        type="retry_knowledge_integration",
                        description="Retry knowledge integration after fixing error",
                        priority=1,
                        validation_criteria="Error resolved and knowledge integrated",
                        parameters={"retrospective_file": retrospective_file, "error": str(e)}
                    )
                ],
                key_points=[
                    f"Knowledge integration failed: {str(e)}",
                    f"Source file: {retrospective_file}",
                    "Check file accessibility and format",
                    "Verify .cortex/ideas/ directory permissions"
                ],
                next_steps=[
                    "1. Check error message for specific issue",
                    "2. Verify retrospective file exists and is readable",
                    "3. Ensure .cortex/ideas/ directory is writable",
                    "4. Check retrospective file format and content",
                    "5. Retry with corrected parameters"
                ],
                confidence_score=0.8,
                complexity_score=3,
                estimated_duration="immediate",
                performance_hints=[
                    "Check file permissions and accessibility",
                    "Verify retrospective file format"
                ],
                learning_opportunities=[
                    "Error handling in knowledge integration",
                    "Retrospective parsing debugging"
                ]
            )




# Export clean API
__all__ = [
    "RetrospectiveTool", 
    "KnowledgeIntegrationTool"
]