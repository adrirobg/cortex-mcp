"""Tests for Architect Payloads.

Following Principio Rector #1: Dogmatismo con Universal Response Schema.
Tests validate architect-specific payload schemas.
"""

import pytest
from typing import Dict, Any
from pydantic import ValidationError

from schemas.architect_payloads import (
    ArchitectPayload,
    WorkflowStage,
    AnalysisResult,
    DecompositionResult,
    TaskGraphResult,
    MissionMapResult,
    Phase,
    Task,
    ResourceAssignment,
    ArchitectDiagrams
)
from schemas.universal_response import StrategyResponse


class TestWorkflowStage:
    """Test WorkflowStage enum."""
    
    def test_workflow_stages(self):
        """Test all workflow stages are valid."""
        assert WorkflowStage.ANALYSIS == "analysis"
        assert WorkflowStage.DECOMPOSITION == "decomposition"
        assert WorkflowStage.TASK_GRAPH == "task_graph"
        assert WorkflowStage.MISSION_MAP == "mission_map"
        assert WorkflowStage.COMPLETE == "complete"
        assert WorkflowStage.READY_FOR_EXECUTION == "ready_for_execution"


class TestAnalysisResult:
    """Test AnalysisResult schema."""
    
    def test_valid_analysis_result(self):
        """Test valid analysis result creation."""
        analysis = AnalysisResult(
            keywords=["web", "api", "backend"],
            patterns=["REST API", "Database CRUD"],
            complexity="Medium",
            requirements_implicit=["Authentication", "Validation"],
            domain="Web Development",
            technology_stack=["Python", "FastAPI", "PostgreSQL"]
        )
        
        assert len(analysis.keywords) == 3
        assert "web" in analysis.keywords
        assert analysis.complexity == "Medium"
        assert analysis.domain == "Web Development"
        assert len(analysis.technology_stack) == 3
    
    def test_minimal_analysis_result(self):
        """Test analysis result with minimal required fields."""
        analysis = AnalysisResult(
            keywords=["test"],
            patterns=["test pattern"],
            complexity="Low",
            requirements_implicit=["test requirement"]
        )
        
        assert analysis.keywords == ["test"]
        assert analysis.domain is None
        assert analysis.technology_stack is None


class TestPhase:
    """Test Phase schema."""
    
    def test_valid_phase(self):
        """Test valid phase creation."""
        phase = Phase(
            id="phase_1",
            name="Backend Development",
            description="Develop the backend API",
            estimated_duration="2 weeks",
            dependencies=["phase_0"],
            deliverables=["API endpoints", "Database schema"]
        )
        
        assert phase.id == "phase_1"
        assert phase.name == "Backend Development"
        assert len(phase.dependencies) == 1
        assert len(phase.deliverables) == 2
    
    def test_phase_minimal(self):
        """Test phase with minimal fields."""
        phase = Phase(
            id="phase_min",
            name="Minimal Phase",
            description="Test phase"
        )
        
        assert phase.id == "phase_min"
        assert phase.dependencies == []
        assert phase.deliverables == []


class TestTask:
    """Test Task schema."""
    
    def test_valid_task(self):
        """Test valid task creation."""
        task = Task(
            id="task_1",
            name="Create User Model",
            description="Create the user database model",
            phase_id="phase_1",
            dependencies=["task_0"],
            estimated_effort="4 hours",
            complexity_score=3,
            agent_profile="agent:python-orm",
            artifacts_output=["user_model.py", "migration.sql"],
            validation_criteria=["Model validates correctly", "Migration runs"],
            human_checkpoint=False
        )
        
        assert task.id == "task_1"
        assert task.name == "Create User Model"
        assert task.phase_id == "phase_1"
        assert task.complexity_score == 3
        assert task.agent_profile == "agent:python-orm"
        assert len(task.artifacts_output) == 2
        assert len(task.validation_criteria) == 2
        assert task.human_checkpoint is False
    
    def test_task_complexity_bounds(self):
        """Test task complexity score validation."""
        # Valid complexity scores
        Task(
            id="task_valid_1",
            name="Test",
            description="Test",
            phase_id="phase_1",
            complexity_score=1
        )
        
        Task(
            id="task_valid_10",
            name="Test",
            description="Test",
            phase_id="phase_1",
            complexity_score=10
        )
        
        # Invalid complexity scores
        with pytest.raises(ValidationError):
            Task(
                id="task_invalid_0",
                name="Test",
                description="Test",
                phase_id="phase_1",
                complexity_score=0
            )
        
        with pytest.raises(ValidationError):
            Task(
                id="task_invalid_11",
                name="Test",
                description="Test",
                phase_id="phase_1",
                complexity_score=11
            )


class TestResourceAssignment:
    """Test ResourceAssignment schema."""
    
    def test_valid_resource_assignment(self):
        """Test valid resource assignment."""
        assignment = ResourceAssignment(
            task_id="task_1",
            agent_profile="agent:python-fastapi",
            estimated_effort="2 days",
            priority=5,
            parallel_group="backend_group"
        )
        
        assert assignment.task_id == "task_1"
        assert assignment.agent_profile == "agent:python-fastapi"
        assert assignment.priority == 5
        assert assignment.parallel_group == "backend_group"
    
    def test_resource_assignment_priority_bounds(self):
        """Test priority validation."""
        with pytest.raises(ValidationError):
            ResourceAssignment(
                task_id="task_1",
                agent_profile="agent:test",
                estimated_effort="1 day",
                priority=0
            )
        
        with pytest.raises(ValidationError):
            ResourceAssignment(
                task_id="task_1",
                agent_profile="agent:test",
                estimated_effort="1 day",
                priority=11
            )


class TestArchitectPayload:
    """Test complete ArchitectPayload schema."""
    
    def create_valid_architect_payload(self) -> Dict[str, Any]:
        """Helper to create valid architect payload data."""
        return {
            "workflow_stage": "analysis",
            "analysis": {
                "keywords": ["web", "api"],
                "patterns": ["REST API"],
                "complexity": "Medium",
                "requirements_implicit": ["Authentication"]
            },
            "implementation_order": ["setup", "backend", "frontend"],
            "suggested_next_state": {
                "continue_workflow": True,
                "next_step": "decomposition"
            },
            "continue_workflow": True,
            "next_step": "decomposition",
            "estimated_completion": "2 weeks"
        }
    
    def test_valid_architect_payload(self):
        """Test valid architect payload creation."""
        data = self.create_valid_architect_payload()
        payload = ArchitectPayload(**data)
        
        assert payload.workflow_stage == WorkflowStage.ANALYSIS
        assert payload.analysis is not None
        assert payload.analysis.keywords == ["web", "api"]
        assert payload.continue_workflow is True
        assert payload.next_step == "decomposition"
        assert len(payload.implementation_order) == 3
    
    def test_architect_payload_minimal(self):
        """Test architect payload with minimal fields."""
        payload = ArchitectPayload(workflow_stage=WorkflowStage.ANALYSIS)
        
        assert payload.workflow_stage == WorkflowStage.ANALYSIS
        assert payload.analysis is None
        assert payload.decomposition is None
        assert payload.task_graph is None
        assert payload.mission_map is None
    
    def test_architect_payload_with_all_stages(self):
        """Test architect payload with all workflow stages."""
        data = {
            "workflow_stage": "complete",
            "analysis": {
                "keywords": ["test"],
                "patterns": ["test pattern"],
                "complexity": "Low",
                "requirements_implicit": ["test req"]
            },
            "decomposition": {
                "phases": [
                    {
                        "id": "phase_1",
                        "name": "Test Phase",
                        "description": "Test phase description"
                    }
                ]
            },
            "task_graph": {
                "tasks": [
                    {
                        "id": "task_1",
                        "name": "Test Task",
                        "description": "Test task description",
                        "phase_id": "phase_1"
                    }
                ],
                "task_count": 1
            },
            "mission_map": {
                "resource_assignments": [
                    {
                        "task_id": "task_1",
                        "agent_profile": "agent:test",
                        "estimated_effort": "1 hour",
                        "priority": 5
                    }
                ],
                "execution_order": ["task_1"]
            }
        }
        
        payload = ArchitectPayload(**data)
        
        assert payload.workflow_stage == WorkflowStage.COMPLETE
        assert payload.analysis is not None
        assert payload.decomposition is not None
        assert payload.task_graph is not None
        assert payload.mission_map is not None
        assert len(payload.decomposition.phases) == 1
        assert len(payload.task_graph.tasks) == 1
        assert len(payload.mission_map.resource_assignments) == 1
    
    def test_architect_payload_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        data = self.create_valid_architect_payload()
        data["extra_field"] = "not allowed"
        
        with pytest.raises(ValidationError):
            ArchitectPayload(**data)


class TestStrategyResponseWithArchitectPayload:
    """Test StrategyResponse with ArchitectPayload integration."""
    
    def test_strategy_response_with_architect_payload(self):
        """Test complete integration of StrategyResponse with ArchitectPayload."""
        data = {
            "strategy": {
                "name": "implement-phase-1-strategy-library-mcp",
                "version": "1.0.0",
                "type": "execution"
            },
            "user_facing": {
                "summary": "Architect analysis complete",
                "key_points": ["Analysis performed", "Next steps identified"],
                "next_steps": ["Proceed to decomposition"]
            },
            "claude_instructions": {
                "execution_type": "multi_step",
                "actions": [
                    {
                        "type": "analyze_project",
                        "description": "Analyze project requirements",
                        "priority": 1,
                        "validation_criteria": "Analysis contains all required fields"
                    }
                ]
            },
            "payload": {
                "workflow_stage": "analysis",
                "analysis": {
                    "keywords": ["MCP", "Pydantic", "JSON-RPC"],
                    "patterns": ["MCP Server", "Schema validation"],
                    "complexity": "Medium",
                    "requirements_implicit": ["Testing", "Validation"]
                },
                "suggested_next_state": {
                    "continue_workflow": True,
                    "next_step": "decomposition",
                    "context_to_maintain": {
                        "architecture_decisions": "Universal Response Schema"
                    }
                }
            },
            "metadata": {
                "confidence_score": 0.92,
                "complexity_score": 6,
                "estimated_duration": "2-3 days"
            }
        }
        
        response = StrategyResponse[ArchitectPayload](**data)
        
        assert response.strategy.name == "implement-phase-1-strategy-library-mcp"
        assert response.payload.workflow_stage == WorkflowStage.ANALYSIS
        assert response.payload.analysis is not None
        assert response.payload.analysis.keywords == ["MCP", "Pydantic", "JSON-RPC"]
        assert response.payload.suggested_next_state is not None
        assert response.metadata.confidence_score == 0.92


if __name__ == "__main__":
    pytest.main([__file__, "-v"])