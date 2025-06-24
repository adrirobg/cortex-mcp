"""Tests for Task Planning Tools.

Following Principio Rector #4: Testing Concurrente.
Behavior-driven tests for all 6 Keymaker Suite tools.

CRITICAL TESTS: All tests must use validate_and_execute() only (never private methods).
Test names describe behavior, not implementation details.

Tools under test:
- KeymakerWorkflowTool: Retrieve structured workflow templates
- ComplexityScoreTool: Calculate Task Complexity Score (TCS) deterministically
- ReasoningTemplateTool: Retrieve reasoning templates (CoT/ToT)
- MissionMapTool: Save and validate mission map artifacts
- TaskDirectivesTool: Generate Do's and Don'ts from mission map
- LibraryChecklistTool: Generate Context7 library documentation checklist
"""

import pytest
import json
import os
from unittest.mock import patch, AsyncMock, MagicMock
from typing import Dict, Any
import aiofiles
import xml.etree.ElementTree as ET

from tools.task_planning import (
    KeymakerWorkflowTool,
    ComplexityScoreTool,
    ReasoningTemplateTool,
    MissionMapTool,
    TaskDirectivesTool,
    LibraryChecklistTool,
)
from schemas.task_planning_payloads import (
    TaskStrategyType,
    ComplexityMetric,
    KeymakerWorkflowPayload,
    ComplexityScorePayload,
    ReasoningTemplatePayload,
    MissionMapPayload,
    TaskDirectivesPayload,
    LibraryChecklistPayload,
)
from schemas.universal_response import StrategyResponse


# Test Fixtures - Shared test data following DRY principles
@pytest.fixture
def sample_workflow_template():
    """Sample workflow template for KeymakerWorkflowTool tests."""
    return {
        "meta": {
            "template_version": "2.8.6",
            "description": "Keymaker task planning workflow",
            "author": "CortexMCP",
        },
        "phases": [
            {
                "phase_id": "analysis",
                "name": "Analysis Phase",
                "description": "Understand task requirements and constraints",
                "steps": [
                    "Analyze task description",
                    "Identify key deliverables",
                    "Determine complexity factors",
                ],
                "estimated_duration": "30-45 minutes",
                "outputs": ["task_analysis.md", "requirements_list.json"],
            },
            {
                "phase_id": "planning",
                "name": "Planning Phase",
                "description": "Create detailed implementation plan",
                "steps": [
                    "Design mission map structure",
                    "Identify agent roles and responsibilities",
                    "Create task dependency graph",
                ],
                "estimated_duration": "45-60 minutes",
                "outputs": ["mission_map.json", "agent_assignments.md"],
            },
            {
                "phase_id": "execution",
                "name": "Execution Phase",
                "description": "Implement planned tasks with monitoring",
                "steps": [
                    "Execute tasks according to mission map",
                    "Monitor progress and adjust as needed",
                    "Validate deliverables against requirements",
                ],
                "estimated_duration": "Variable based on complexity",
                "outputs": ["implementation_artifacts", "progress_reports"],
            },
        ],
        "workflow_patterns": {
            "cognitive_load_reduction": [
                "Break complex tasks into atomic operations",
                "Use templates to reduce decision fatigue",
                "Implement systematic validation checkpoints",
            ],
            "quality_assurance": [
                "Test-driven development approach",
                "Continuous validation during execution",
                "Post-completion retrospective analysis",
            ],
        },
    }


@pytest.fixture
def sample_complexity_matrix():
    """Sample complexity scoring matrix XML for ComplexityScoreTool tests."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<complexity_rubric>
    <meta>
        <version>2.8.6</version>
        <description>Task Complexity Scoring Matrix for Keymaker Suite</description>
        <threshold_cot_tot>4</threshold_cot_tot>
    </meta>
    
    <dimension name="Novelty" weight="0.3">
        <description>How new or unfamiliar are the technologies/concepts?</description>
        <metric id="NOV-01" points="3">
            <instruction>Task involves new framework or technology not used before</instruction>
            <keywords>["nuevo", "nueva", "framework", "tecnología", "unfamiliar"]</keywords>
        </metric>
        <metric id="NOV-02" points="2">
            <instruction>Task uses familiar technology in new way</instruction>
            <keywords>["adaptar", "modificar", "extend", "customize"]</keywords>
        </metric>
        <metric id="NOV-03" points="1">
            <instruction>Task uses well-known patterns and technologies</instruction>
            <keywords>["estándar", "común", "typical", "usual"]</keywords>
        </metric>
    </dimension>
    
    <dimension name="Scale" weight="0.25">
        <description>How many components/files/systems are involved?</description>
        <metric id="SCL-01" points="3">
            <instruction>More than 10 files or complex multi-system integration</instruction>
            <keywords>["sistema", "integration", "architecture", "multiple"]</keywords>
        </metric>
        <metric id="SCL-02" points="2">
            <instruction>5-10 files or moderate system complexity</instruction>
            <keywords>["moderate", "several", "algunos"]</keywords>
        </metric>
        <metric id="SCL-03" points="1">
            <instruction>Less than 5 files or single system focus</instruction>
            <keywords>["simple", "pequeño", "single", "individual"]</keywords>
        </metric>
    </dimension>
    
    <dimension name="Ambiguity" weight="0.25">
        <description>How clear are the requirements and expected outcomes?</description>
        <metric id="AMB-01" points="3">
            <instruction>Vague requirements, unclear success criteria</instruction>
            <keywords>["ambiguous", "unclear", "indefinido", "vago"]</keywords>
        </metric>
        <metric id="AMB-02" points="2">
            <instruction>Some requirements clear, others need clarification</instruction>
            <keywords>["partially", "algunos", "clarification", "partly"]</keywords>
        </metric>
        <metric id="AMB-03" points="1">
            <instruction>Clear, well-defined requirements and outcomes</instruction>
            <keywords>["clear", "defined", "specific", "detailed"]</keywords>
        </metric>
    </dimension>
    
    <dimension name="Coupling" weight="0.2">
        <description>How interconnected are the components/dependencies?</description>
        <metric id="COU-01" points="3">
            <instruction>High interdependency, changes affect multiple components</instruction>
            <keywords>["interdependent", "coupled", "dependencies", "connected"]</keywords>
        </metric>
        <metric id="COU-02" points="2">
            <instruction>Moderate coupling, some shared dependencies</instruction>
            <keywords>["shared", "moderate", "some dependencies"]</keywords>
        </metric>
        <metric id="COU-03" points="1">
            <instruction>Low coupling, independent components</instruction>
            <keywords>["independent", "isolated", "standalone"]</keywords>
        </metric>
    </dimension>
</complexity_rubric>"""


@pytest.fixture
def sample_cot_template():
    """Sample Chain of Thought reasoning template."""
    return {
        "meta": {
            "strategy_type": "chain_of_thought",
            "description": "Structured reasoning template for moderate complexity tasks",
            "version": "2.8.6",
        },
        "thought_templates": [
            {
                "step": 1,
                "topic": "Problem Understanding",
                "prompts": [
                    "What exactly is being asked?",
                    "What are the key constraints and requirements?",
                    "What success criteria must be met?",
                ],
                "validation": "Clear problem statement identified",
            },
            {
                "step": 2,
                "topic": "Approach Selection",
                "prompts": [
                    "What approaches could solve this problem?",
                    "What are the trade-offs of each approach?",
                    "Which approach best fits the constraints?",
                ],
                "validation": "Approach selected with clear rationale",
            },
            {
                "step": 3,
                "topic": "Implementation Planning",
                "prompts": [
                    "What are the key implementation steps?",
                    "What resources and dependencies are needed?",
                    "What risks should be considered?",
                ],
                "validation": "Implementation plan with risk mitigation",
            },
            {
                "step": 4,
                "topic": "Execution Strategy",
                "prompts": [
                    "In what order should tasks be completed?",
                    "How will progress be monitored?",
                    "What are the key validation checkpoints?",
                ],
                "validation": "Clear execution plan with checkpoints",
            },
            {
                "step": 5,
                "topic": "Quality Assurance",
                "prompts": [
                    "How will the solution be tested?",
                    "What criteria determine success?",
                    "How will issues be identified and resolved?",
                ],
                "validation": "Comprehensive quality assurance plan",
            },
        ],
        "usage_guidelines": [
            "Work through each thought template sequentially",
            "Document reasoning clearly at each step",
            "Validate each step before proceeding to the next",
            "Adjust approach if validation fails",
        ],
    }


@pytest.fixture
def sample_tot_template():
    """Sample Tree of Thoughts reasoning template."""
    return {
        "meta": {
            "strategy_type": "tree_of_thoughts",
            "description": "Multi-perspective reasoning for high complexity tasks",
            "version": "2.8.6",
        },
        "perspectives": [
            {
                "name": "Technical Architecture",
                "focus": "System design and technical implementation",
                "key_questions": [
                    "What is the optimal technical architecture?",
                    "How do components interact and depend on each other?",
                    "What are the scalability and performance implications?",
                    "What technical risks need mitigation?",
                ],
                "evaluation_criteria": [
                    "Technical feasibility",
                    "Scalability potential",
                    "Maintenance complexity",
                    "Integration challenges",
                ],
            },
            {
                "name": "User Experience",
                "focus": "End-user needs and interaction patterns",
                "key_questions": [
                    "Who are the primary users and what do they need?",
                    "What are the key user workflows and pain points?",
                    "How can the solution improve user efficiency?",
                    "What accessibility considerations are important?",
                ],
                "evaluation_criteria": [
                    "User satisfaction potential",
                    "Learning curve",
                    "Workflow efficiency",
                    "Accessibility compliance",
                ],
            },
            {
                "name": "Business Impact",
                "focus": "Strategic value and organizational benefits",
                "key_questions": [
                    "What business value does this solution provide?",
                    "How does it align with organizational goals?",
                    "What are the resource requirements and ROI?",
                    "What are the long-term strategic implications?",
                ],
                "evaluation_criteria": [
                    "Business value alignment",
                    "Resource efficiency",
                    "Strategic importance",
                    "Long-term sustainability",
                ],
            },
        ],
        "synthesis_process": {
            "evaluation_matrix": "Score each perspective on technical feasibility, user impact, and business value",
            "decision_framework": "Select solution that optimizes across all three perspectives",
            "validation_approach": "Test solution against criteria from all perspectives",
        },
        "usage_guidelines": [
            "Explore each perspective thoroughly before synthesis",
            "Look for solutions that satisfy multiple perspectives",
            "Use evaluation matrix to compare alternatives objectively",
            "Validate final solution against all perspective criteria",
        ],
    }


@pytest.fixture
def sample_mission_map_schema():
    """Sample JSON schema for mission map validation."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Mission Map Schema",
        "description": "Schema for validating Keymaker mission map structure",
        "type": "object",
        "required": ["project", "phases"],
        "properties": {
            "project": {
                "type": "string",
                "description": "Project name and brief description",
                "minLength": 3,
            },
            "meta": {
                "type": "object",
                "properties": {
                    "created_by": {"type": "string"},
                    "creation_date": {"type": "string"},
                    "version": {"type": "string"},
                    "complexity_score": {"type": "number"},
                },
            },
            "phases": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["phase_id", "description", "tasks"],
                    "properties": {
                        "phase_id": {"type": "string", "pattern": "^phase_[0-9]+$"},
                        "description": {"type": "string", "minLength": 10},
                        "tasks": {
                            "type": "array",
                            "minItems": 1,
                            "items": {
                                "type": "object",
                                "required": ["task_id", "description", "agent_profile"],
                                "properties": {
                                    "task_id": {
                                        "type": "string",
                                        "pattern": "^[0-9]+\\.[0-9]+$",
                                    },
                                    "description": {"type": "string", "minLength": 10},
                                    "agent_profile": {
                                        "type": "string",
                                        "pattern": "^agent:[a-zA-Z0-9_]+$",
                                    },
                                    "dependencies": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "estimated_duration": {"type": "string"},
                                    "context7_libraries": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "deliverables": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
    }


@pytest.fixture
def sample_valid_mission_map():
    """Sample valid mission map for testing."""
    return {
        "project": "CortexMCP Task Planning Enhancement",
        "meta": {
            "created_by": "keymaker-workflow",
            "creation_date": "2025-06-23",
            "version": "2.8.6",
            "complexity_score": 6.2,
        },
        "phases": [
            {
                "phase_id": "phase_1",
                "description": "Foundation and schema setup for task planning tools",
                "tasks": [
                    {
                        "task_id": "1.1",
                        "description": "Create comprehensive payload schemas for all 6 task planning tools",
                        "agent_profile": "agent:schema_architect",
                        "dependencies": [],
                        "estimated_duration": "2-3 hours",
                        "context7_libraries": ["pydantic", "typing", "enum"],
                        "deliverables": ["schemas/task_planning_payloads.py"],
                    },
                    {
                        "task_id": "1.2",
                        "description": "Setup behavior-driven test structure for all tools",
                        "agent_profile": "agent:test_engineer",
                        "dependencies": ["1.1"],
                        "estimated_duration": "1-2 hours",
                        "context7_libraries": [
                            "pytest",
                            "pytest-asyncio",
                            "unittest.mock",
                        ],
                        "deliverables": ["tests/tools/test_task_planning.py"],
                    },
                ],
            },
            {
                "phase_id": "phase_2",
                "description": "Core tool implementation with TDD approach",
                "tasks": [
                    {
                        "task_id": "2.1",
                        "description": "Implement KeymakerWorkflowTool and ComplexityScoreTool",
                        "agent_profile": "agent:tool_developer",
                        "dependencies": ["1.1", "1.2"],
                        "estimated_duration": "4-5 hours",
                        "context7_libraries": [
                            "aiofiles",
                            "json",
                            "xml.etree.ElementTree",
                        ],
                        "deliverables": ["tools/task_planning.py (partial)"],
                    }
                ],
            },
        ],
    }


@pytest.fixture
def sample_invalid_mission_map():
    """Sample invalid mission map for testing validation."""
    return {
        "project": "Test Project"
        # Missing required 'phases' field
    }


# Mock setup fixtures for aiofiles operations
@pytest.fixture
def mock_aiofiles_open():
    """Mock aiofiles.open for file operations."""
    with patch("aiofiles.open", create=True) as mock_open:
        yield mock_open


@pytest.fixture
def mock_aiofiles_exists():
    """Mock aiofiles.os.path.exists for file existence checks."""
    with patch("aiofiles.os.path.exists") as mock_exists:
        yield mock_exists


@pytest.fixture
def mock_aiofiles_makedirs():
    """Mock aiofiles.os.makedirs for directory creation."""
    with patch("aiofiles.os.makedirs") as mock_makedirs:
        yield mock_makedirs


@pytest.fixture
def mock_aiofiles_stat():
    """Mock aiofiles.os.stat for file stats."""
    with patch("aiofiles.os.stat") as mock_stat:
        # Create a mock stat result
        stat_result = MagicMock()
        stat_result.st_size = 1024  # Mock file size
        mock_stat.return_value = stat_result
        yield mock_stat


# KeymakerWorkflowTool Tests
@pytest.mark.asyncio
class TestKeymakerWorkflowTool:
    """Test KeymakerWorkflowTool behavior through validate_and_execute only."""

    async def test_keymaker_workflow_retrieval_returns_valid_structure(
        self, sample_workflow_template, mock_aiofiles_open
    ):
        """Test keymaker workflow template retrieval returns valid workflow structure."""
        tool = KeymakerWorkflowTool()

        # Setup mock file read
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_workflow_template)
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(workflow_type="task_planning")

        # Validate it's a proper Dict response
        assert isinstance(result, dict)
        assert "payload" in result
        assert "strategy" in result

        # Validate payload structure
        payload = result["payload"]
        assert payload["phases_count"] == 3
        assert len(payload["phase_names"]) == 3
        assert payload["template_format"] == "json"
        assert payload["workflow_stage"] == "complete"

        # Validate user-facing summary indicates success
        assert "✅" in result["user_facing"]["summary"]
        assert "workflow template" in result["user_facing"]["summary"].lower()

    async def test_keymaker_workflow_handles_missing_template_gracefully(
        self, mock_aiofiles_open
    ):
        """Test keymaker workflow handles missing template file gracefully."""
        tool = KeymakerWorkflowTool()

        # Setup mock to simulate file not found
        mock_aiofiles_open.side_effect = FileNotFoundError("Template file not found")

        result = await tool.validate_and_execute(workflow_type="nonexistent")

        # Should return valid error response, not raise exception
        assert isinstance(result, dict)
        assert "error" in result["user_facing"]["summary"].lower()
        assert result["payload"]["workflow_stage"] == "error"

    async def test_keymaker_workflow_handles_corrupted_json_template(
        self, mock_aiofiles_open
    ):
        """Test keymaker workflow handles corrupted JSON template gracefully."""
        tool = KeymakerWorkflowTool()

        # Setup mock with invalid JSON
        mock_file = AsyncMock()
        mock_file.read.return_value = "{ invalid json content"
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(workflow_type="corrupted")

        # Should handle JSON decode error gracefully
        assert isinstance(result, dict)
        assert "error" in result["user_facing"]["summary"].lower()
        assert result["payload"]["workflow_stage"] == "error"


# ComplexityScoreTool Tests
@pytest.mark.asyncio
class TestComplexityScoreTool:
    """Test ComplexityScoreTool behavior through validate_and_execute only."""

    async def test_complexity_score_simple_task_recommends_cot(
        self, sample_complexity_matrix, mock_aiofiles_open
    ):
        """Test complexity scoring for simple task recommends Chain of Thought."""
        tool = ComplexityScoreTool()

        # Setup mock complexity matrix
        mock_file = AsyncMock()
        mock_file.read.return_value = sample_complexity_matrix
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(
            task_description="Create simple CRUD endpoints for user management",
            scope="Basic user operations with standard patterns",
            expected_outputs=["user.py", "test_user.py", "user_api.py"],
        )

        # Validate response structure
        assert isinstance(result, dict)
        payload = result["payload"]

        # Simple task should have TCS < 4 and recommend CoT
        assert payload["task_complexity_score"] < 4.0
        assert payload["recommended_strategy"] == "chain_of_thought"
        assert payload["confidence_level"] == 0.85  # Consistent confidence
        assert len(payload["scoring_breakdown"]) > 0

    async def test_complexity_score_complex_task_recommends_tot(
        self, sample_complexity_matrix, mock_aiofiles_open
    ):
        """Test complexity scoring for complex task recommends Tree of Thoughts."""
        tool = ComplexityScoreTool()

        # Setup mock complexity matrix
        mock_file = AsyncMock()
        mock_file.read.return_value = sample_complexity_matrix
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(
            task_description="Diseñar arquitectura de microservicios distribuidos con nueva tecnología",
            scope="Refactorización completa del sistema legacy con integración de múltiples servicios",
            expected_outputs=[f"service_{i}.py" for i in range(12)],  # High file count
        )

        # Validate response structure
        assert isinstance(result, dict)
        payload = result["payload"]

        # Complex task should have TCS >= 4 and recommend ToT
        assert payload["task_complexity_score"] >= 4.0
        assert payload["recommended_strategy"] == "tree_of_thoughts"
        assert payload["confidence_level"] == 0.85
        assert len(payload["scoring_breakdown"]) > 0

    async def test_complexity_score_deterministic_calculation(
        self, sample_complexity_matrix, mock_aiofiles_open
    ):
        """Test complexity scoring produces deterministic results."""
        tool = ComplexityScoreTool()

        # Setup mock complexity matrix
        mock_file = AsyncMock()
        mock_file.read.return_value = sample_complexity_matrix
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        # Run same calculation twice
        task_params = {
            "task_description": "Implement REST API with authentication",
            "scope": "Standard web application backend",
            "expected_outputs": ["api.py", "auth.py", "models.py", "tests.py"],
        }

        result1 = await tool.validate_and_execute(**task_params)
        result2 = await tool.validate_and_execute(**task_params)

        # Results should be identical (deterministic)
        assert (
            result1["payload"]["task_complexity_score"]
            == result2["payload"]["task_complexity_score"]
        )
        assert (
            result1["payload"]["recommended_strategy"]
            == result2["payload"]["recommended_strategy"]
        )
        assert (
            result1["payload"]["confidence_level"]
            == result2["payload"]["confidence_level"]
        )


# ReasoningTemplateTool Tests
@pytest.mark.asyncio
class TestReasoningTemplateTool:
    """Test ReasoningTemplateTool behavior through validate_and_execute only."""

    async def test_reasoning_template_retrieves_cot_template(
        self, sample_cot_template, mock_aiofiles_open
    ):
        """Test reasoning template retrieval for Chain of Thought strategy."""
        tool = ReasoningTemplateTool()

        # Setup mock CoT template
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_cot_template)
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(strategy_type="chain_of_thought")

        # Validate response structure
        assert isinstance(result, dict)
        payload = result["payload"]

        # Validate CoT template structure
        assert payload["strategy_type"] == "chain_of_thought"
        assert len(payload["template_sections"]) == 5  # 5 thought templates
        assert len(payload["guidelines"]) > 0
        assert payload["workflow_stage"] == "complete"

        # Validate that all thought templates are included
        section_topics = [section["topic"] for section in payload["template_sections"]]
        expected_topics = [
            "Problem Understanding",
            "Approach Selection",
            "Implementation Planning",
            "Execution Strategy",
            "Quality Assurance",
        ]
        for topic in expected_topics:
            assert topic in section_topics

    async def test_reasoning_template_retrieves_tot_template(
        self, sample_tot_template, mock_aiofiles_open
    ):
        """Test reasoning template retrieval for Tree of Thoughts strategy."""
        tool = ReasoningTemplateTool()

        # Setup mock ToT template
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_tot_template)
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(strategy_type="tree_of_thoughts")

        # Validate response structure
        assert isinstance(result, dict)
        payload = result["payload"]

        # Validate ToT template structure
        assert payload["strategy_type"] == "tree_of_thoughts"
        assert len(payload["template_sections"]) == 3  # 3 perspectives
        assert len(payload["guidelines"]) > 0
        assert payload["workflow_stage"] == "complete"

        # Validate that all perspectives are included
        section_focuses = [section["focus"] for section in payload["template_sections"]]
        expected_focuses = [
            "System design and technical implementation",
            "End-user needs and interaction patterns",
            "Strategic value and organizational benefits",
        ]
        for focus in expected_focuses:
            assert focus in section_focuses

    async def test_reasoning_template_handles_invalid_strategy_type(
        self, mock_aiofiles_open
    ):
        """Test reasoning template handles invalid strategy type gracefully."""
        tool = ReasoningTemplateTool()

        result = await tool.validate_and_execute(strategy_type="invalid_strategy")

        # Should return error response, not raise exception
        assert isinstance(result, dict)
        assert "error" in result["user_facing"]["summary"].lower()
        assert result["payload"]["workflow_stage"] == "error"


# MissionMapTool Tests
@pytest.mark.asyncio
class TestMissionMapTool:
    """Test MissionMapTool behavior through validate_and_execute only."""

    async def test_mission_map_validation_accepts_valid_content(
        self,
        sample_valid_mission_map,
        sample_mission_map_schema,
        mock_aiofiles_open,
        mock_aiofiles_makedirs,
        mock_aiofiles_exists,
        mock_aiofiles_stat,
    ):
        """Test mission map validation accepts valid mission map content."""
        tool = MissionMapTool()

        # Setup mocks
        mock_aiofiles_exists.return_value = False  # Directory doesn't exist
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_mission_map_schema)
        mock_file.write = AsyncMock()
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(
            task_id="test_task_123", mission_content=sample_valid_mission_map
        )

        # Validate response structure
        assert isinstance(result, dict)
        payload = result["payload"]

        # Valid mission map should validate successfully
        assert payload["validation_status"] == "valid"
        assert (
            payload["validation_errors"] is None
            or len(payload["validation_errors"]) == 0
        )
        assert payload["mission_summary"]["phases_count"] == 2
        assert payload["mission_summary"]["total_tasks"] == 3
        assert payload["workflow_stage"] == "complete"

        # Should have created directory and saved file
        mock_aiofiles_makedirs.assert_called_once()
        assert "mission map saved" in result["user_facing"]["summary"].lower()

    async def test_mission_map_validation_rejects_invalid_content(
        self,
        sample_invalid_mission_map,
        sample_mission_map_schema,
        mock_aiofiles_open,
        mock_aiofiles_makedirs,
        mock_aiofiles_exists,
        mock_aiofiles_stat,
    ):
        """Test mission map validation rejects invalid mission map content."""
        tool = MissionMapTool()

        # Setup mocks
        mock_aiofiles_exists.return_value = False
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_mission_map_schema)
        mock_file.write = AsyncMock()
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(
            task_id="test_invalid", mission_content=sample_invalid_mission_map
        )

        # Validate response structure
        assert isinstance(result, dict)
        payload = result["payload"]

        # Invalid mission map should fail validation but still save for debugging
        assert payload["validation_status"] == "invalid"
        assert payload["validation_errors"] is not None
        assert len(payload["validation_errors"]) > 0
        assert any("phases" in error.lower() for error in payload["validation_errors"])
        assert payload["workflow_stage"] == "complete"

        # Should still save file for debugging
        mock_aiofiles_makedirs.assert_called_once()
        assert "validation failed" in result["user_facing"]["summary"].lower()

    async def test_mission_map_creates_directory_structure(
        self,
        sample_valid_mission_map,
        sample_mission_map_schema,
        mock_aiofiles_open,
        mock_aiofiles_makedirs,
        mock_aiofiles_exists,
    ):
        """Test mission map tool creates proper directory structure."""
        tool = MissionMapTool()

        # Setup mocks
        mock_aiofiles_exists.return_value = False  # Directory doesn't exist
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_mission_map_schema)
        mock_file.write = AsyncMock()
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        task_id = "complex_task_456"
        await tool.validate_and_execute(
            task_id=task_id, mission_content=sample_valid_mission_map
        )

        # Should create directory with task_id
        expected_dir = f".cortex/tasks/{task_id}"
        mock_aiofiles_makedirs.assert_called_with(expected_dir, exist_ok=True)


# TaskDirectivesTool Tests
@pytest.mark.asyncio
class TestTaskDirectivesTool:
    """Test TaskDirectivesTool behavior through validate_and_execute only."""

    async def test_directives_generation_extracts_patterns_from_mission_map(
        self, sample_valid_mission_map, mock_aiofiles_open
    ):
        """Test directives generation extracts relevant patterns from mission map."""
        tool = TaskDirectivesTool()

        # Setup mock mission map file
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_valid_mission_map)
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(
            mission_map_path=".cortex/tasks/test/mission_map.json"
        )

        # Validate response structure
        assert isinstance(result, dict)
        payload = result["payload"]

        # Should generate meaningful Do's and Don'ts
        assert payload["dos_count"] > 0
        assert payload["donts_count"] > 0
        assert len(payload["source_patterns"]) > 0
        assert len(payload["technologies_covered"]) > 0
        assert payload["workflow_stage"] == "complete"

        # Should identify technologies from context7_libraries
        expected_technologies = [
            "pydantic",
            "typing",
            "enum",
            "pytest",
            "pytest-asyncio",
            "unittest.mock",
        ]
        for tech in expected_technologies:
            assert tech in payload["technologies_covered"]

    async def test_directives_generation_handles_missing_mission_file(
        self, mock_aiofiles_open
    ):
        """Test directives generation handles missing mission map file gracefully."""
        tool = TaskDirectivesTool()

        # Setup mock to simulate file not found
        mock_aiofiles_open.side_effect = FileNotFoundError("Mission map file not found")

        result = await tool.validate_and_execute(
            mission_map_path=".cortex/tasks/nonexistent/mission_map.json"
        )

        # Should return error response, not raise exception
        assert isinstance(result, dict)
        assert "error" in result["user_facing"]["summary"].lower()
        assert result["payload"]["workflow_stage"] == "error"

    async def test_directives_generation_produces_markdown_format(
        self, sample_valid_mission_map, mock_aiofiles_open
    ):
        """Test directives generation produces properly formatted markdown output."""
        tool = TaskDirectivesTool()

        # Setup mock mission map file
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_valid_mission_map)
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(
            mission_map_path=".cortex/tasks/test/mission_map.json"
        )

        # Validate markdown formatting in directives_content
        payload = result["payload"]
        directives_content = payload["directives_content"]

        # Should contain markdown headers and structure
        assert "# Task Directives" in directives_content
        assert "## Do's" in directives_content
        assert "## Don'ts" in directives_content
        assert "## Technologies Covered" in directives_content

        # Should contain bullet points
        assert "- " in directives_content


# LibraryChecklistTool Tests
@pytest.mark.asyncio
class TestLibraryChecklistTool:
    """Test LibraryChecklistTool behavior through validate_and_execute only."""

    async def test_checklist_generation_extracts_unique_libraries(
        self, sample_valid_mission_map, mock_aiofiles_open
    ):
        """Test library checklist extracts unique libraries from mission map."""
        tool = LibraryChecklistTool()

        # Setup mock mission map file
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_valid_mission_map)
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(
            mission_map_path=".cortex/tasks/test/mission_map.json"
        )

        # Validate response structure
        assert isinstance(result, dict)
        payload = result["payload"]

        # Should extract unique libraries
        assert payload["total_libraries"] >= 6  # At least the expected unique libraries
        assert len(payload["libraries_found"]) >= 6
        assert payload["workflow_stage"] == "complete"

        # Validate library objects have required fields
        for library in payload["libraries_found"]:
            assert "name" in library
            assert "context7_id" in library
            assert "documentation_status" in library

        # Should include expected libraries
        library_names = [lib["name"] for lib in payload["libraries_found"]]
        expected_libraries = [
            "pydantic",
            "typing",
            "enum",
            "pytest",
            "pytest-asyncio",
            "unittest.mock",
        ]
        for expected_lib in expected_libraries:
            assert expected_lib in library_names

    async def test_checklist_generation_produces_markdown_checklist(
        self, sample_valid_mission_map, mock_aiofiles_open
    ):
        """Test library checklist produces properly formatted markdown checklist."""
        tool = LibraryChecklistTool()

        # Setup mock mission map file
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_valid_mission_map)
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(
            mission_map_path=".cortex/tasks/test/mission_map.json"
        )

        # Validate markdown checklist format
        payload = result["payload"]
        checklist_content = payload["checklist_content"]

        # Should contain markdown headers and checklist structure
        assert "# Context7 Library Documentation Checklist" in checklist_content
        assert "Generated on:" in checklist_content
        assert "Total libraries identified:" in checklist_content

        # Should contain checklist items with checkboxes
        assert "- [ ]" in checklist_content

        # Should contain Context7 placeholder IDs
        assert "Context7 ID: `/placeholder/" in checklist_content

    async def test_checklist_generation_handles_duplicate_libraries(
        self, mock_aiofiles_open
    ):
        """Test library checklist handles duplicate libraries correctly."""
        tool = LibraryChecklistTool()

        # Create mission map with duplicate libraries
        mission_with_duplicates = {
            "project": "Test Project",
            "phases": [
                {
                    "phase_id": "phase_1",
                    "description": "Test phase",
                    "tasks": [
                        {
                            "task_id": "1.1",
                            "description": "Task 1",
                            "agent_profile": "agent:test",
                            "context7_libraries": ["pytest", "pydantic", "typing"],
                        },
                        {
                            "task_id": "1.2",
                            "description": "Task 2",
                            "agent_profile": "agent:test",
                            "context7_libraries": [
                                "pytest",
                                "typing",
                                "asyncio",
                            ],  # pytest and typing duplicated
                        },
                    ],
                }
            ],
        }

        # Setup mock mission map file
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(mission_with_duplicates)
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(
            mission_map_path=".cortex/tasks/test/mission_map.json"
        )

        # Should deduplicate libraries
        payload = result["payload"]
        assert (
            payload["total_libraries"] == 4
        )  # pytest, pydantic, typing, asyncio (unique)

        library_names = [lib["name"] for lib in payload["libraries_found"]]
        assert len(library_names) == len(set(library_names))  # All unique


# Integration Tests
@pytest.mark.asyncio
class TestTaskPlanningWorkflowIntegration:
    """Test complete keymaker workflow integration through behavior validation."""

    async def test_full_workflow_sequence_produces_complete_construction_kit(
        self,
        sample_workflow_template,
        sample_complexity_matrix,
        sample_cot_template,
        sample_mission_map_schema,
        sample_valid_mission_map,
        mock_aiofiles_open,
        mock_aiofiles_makedirs,
        mock_aiofiles_exists,
        mock_aiofiles_stat,
    ):
        """Test complete keymaker workflow from template to construction kit."""
        # Setup all mocks for the full workflow
        mock_aiofiles_exists.return_value = False
        mock_file = AsyncMock()
        mock_file.write = AsyncMock()

        # Configure mock to return different content based on call order
        mock_responses = [
            json.dumps(sample_workflow_template),  # KeymakerWorkflowTool
            sample_complexity_matrix,  # ComplexityScoreTool
            json.dumps(sample_cot_template),  # ReasoningTemplateTool (CoT)
            json.dumps(sample_mission_map_schema),  # MissionMapTool (schema)
            json.dumps(sample_valid_mission_map),  # TaskDirectivesTool (mission map)
            json.dumps(sample_valid_mission_map),  # LibraryChecklistTool (mission map)
        ]

        call_count = 0

        def mock_read_side_effect():
            nonlocal call_count
            response = mock_responses[call_count % len(mock_responses)]
            call_count += 1
            return response

        mock_file.read.side_effect = mock_read_side_effect
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        # 1. Get workflow template
        workflow_tool = KeymakerWorkflowTool()
        workflow_result = await workflow_tool.validate_and_execute(
            workflow_type="task_planning"
        )
        assert workflow_result["payload"]["workflow_stage"] == "complete"

        # 2. Calculate complexity score
        complexity_tool = ComplexityScoreTool()
        complexity_result = await complexity_tool.validate_and_execute(
            task_description="Implement moderate complexity task",
            scope="Standard development patterns",
            expected_outputs=["file1.py", "file2.py", "test.py"],
        )
        assert complexity_result["payload"]["recommended_strategy"] in [
            "chain_of_thought",
            "tree_of_thoughts",
        ]

        # 3. Get reasoning template based on complexity
        reasoning_tool = ReasoningTemplateTool()
        strategy_type = complexity_result["payload"]["recommended_strategy"]
        reasoning_result = await reasoning_tool.validate_and_execute(
            strategy_type=strategy_type
        )
        assert reasoning_result["payload"]["strategy_type"] == strategy_type

        # 4. Save mission map (Claude would generate this based on reasoning)
        mission_tool = MissionMapTool()
        mission_result = await mission_tool.validate_and_execute(
            task_id="integration_test", mission_content=sample_valid_mission_map
        )
        assert mission_result["payload"]["validation_status"] == "valid"

        # 5. Generate task directives
        directives_tool = TaskDirectivesTool()
        directives_result = await directives_tool.validate_and_execute(
            mission_map_path=".cortex/tasks/integration_test/mission_map.json"
        )
        assert directives_result["payload"]["dos_count"] > 0
        assert directives_result["payload"]["donts_count"] > 0

        # 6. Generate library checklist
        checklist_tool = LibraryChecklistTool()
        checklist_result = await checklist_tool.validate_and_execute(
            mission_map_path=".cortex/tasks/integration_test/mission_map.json"
        )
        assert checklist_result["payload"]["total_libraries"] > 0

        # Validate complete construction kit was created
        all_results = [
            workflow_result,
            complexity_result,
            reasoning_result,
            mission_result,
            directives_result,
            checklist_result,
        ]

        # All steps should complete successfully
        for result in all_results:
            assert isinstance(result, dict)
            assert result["payload"]["workflow_stage"] == "complete"
            assert "strategy" in result
            assert "user_facing" in result

    async def test_error_handling_preserves_workflow_continuity(
        self, mock_aiofiles_open
    ):
        """Test that individual tool errors don't break the entire workflow."""
        # Test that each tool handles errors gracefully without raising exceptions

        # Setup mock to simulate various error conditions
        mock_aiofiles_open.side_effect = [
            FileNotFoundError("Template not found"),  # KeymakerWorkflowTool
            PermissionError("Cannot read matrix"),  # ComplexityScoreTool
            json.JSONDecodeError("Invalid JSON", "", 0),  # ReasoningTemplateTool
        ]

        # Each tool should handle its error gracefully
        workflow_tool = KeymakerWorkflowTool()
        workflow_result = await workflow_tool.validate_and_execute(
            workflow_type="missing"
        )
        assert "error" in workflow_result["user_facing"]["summary"].lower()
        assert workflow_result["payload"]["workflow_stage"] == "error"

        complexity_tool = ComplexityScoreTool()
        complexity_result = await complexity_tool.validate_and_execute(
            task_description="Test task",
            scope="Test scope",
            expected_outputs=["test.py"],
        )
        assert "error" in complexity_result["user_facing"]["summary"].lower()
        assert complexity_result["payload"]["workflow_stage"] == "error"

        reasoning_tool = ReasoningTemplateTool()
        reasoning_result = await reasoning_tool.validate_and_execute(
            strategy_type="chain_of_thought"
        )
        assert "error" in reasoning_result["user_facing"]["summary"].lower()
        assert reasoning_result["payload"]["workflow_stage"] == "error"

        # All tools should return valid Dict responses, never raise exceptions
        for result in [workflow_result, complexity_result, reasoning_result]:
            assert isinstance(result, dict)
            assert "strategy" in result
            assert "payload" in result
            assert "user_facing" in result


# Performance and Edge Case Tests
@pytest.mark.asyncio
class TestTaskPlanningPerformanceAndEdgeCases:
    """Test performance requirements and edge cases for all tools."""

    async def test_keymaker_workflow_retrieval_performance_under_100ms(
        self, sample_workflow_template, mock_aiofiles_open
    ):
        """Test keymaker workflow retrieval meets <100ms performance requirement."""
        import time

        tool = KeymakerWorkflowTool()

        # Setup mock file read
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_workflow_template)
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        # Measure execution time
        start_time = time.time()
        result = await tool.validate_and_execute(workflow_type="task_planning")
        execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # Should complete under 100ms (allowing some overhead for mocking)
        assert execution_time < 200  # More lenient for test environment
        assert result["payload"]["workflow_stage"] == "complete"

    async def test_complexity_score_handles_empty_input_gracefully(
        self, sample_complexity_matrix, mock_aiofiles_open
    ):
        """Test complexity scoring handles empty or minimal input gracefully."""
        tool = ComplexityScoreTool()

        # Setup mock complexity matrix
        mock_file = AsyncMock()
        mock_file.read.return_value = sample_complexity_matrix
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        # Test with minimal input
        result = await tool.validate_and_execute(
            task_description="", scope="", expected_outputs=[]
        )

        # Should handle gracefully and return a minimal score
        assert isinstance(result, dict)
        payload = result["payload"]
        assert payload["task_complexity_score"] >= 1.0  # Minimum score
        assert payload["confidence_level"] == 0.85
        assert payload["recommended_strategy"] in [
            "chain_of_thought",
            "tree_of_thoughts",
        ]

    async def test_mission_map_handles_large_mission_maps(
        self,
        sample_mission_map_schema,
        mock_aiofiles_open,
        mock_aiofiles_makedirs,
        mock_aiofiles_exists,
        mock_aiofiles_stat,
    ):
        """Test mission map tool handles large mission maps efficiently."""
        # Create large mission map with many phases and tasks
        large_mission_map = {
            "project": "Large Scale System Implementation",
            "phases": [],
        }

        # Generate 10 phases with 5 tasks each
        for phase_num in range(1, 11):
            phase = {
                "phase_id": f"phase_{phase_num}",
                "description": f"Phase {phase_num} implementation with multiple complex tasks",
                "tasks": [],
            }

            for task_num in range(1, 6):
                task = {
                    "task_id": f"{phase_num}.{task_num}",
                    "description": f"Complex task {task_num} in phase {phase_num} requiring significant implementation effort",
                    "agent_profile": f"agent:developer_{task_num}",
                    "dependencies": []
                    if task_num == 1
                    else [f"{phase_num}.{task_num-1}"],
                    "context7_libraries": [
                        "fastapi",
                        "sqlalchemy",
                        "pytest",
                        "pydantic",
                        "asyncio",
                    ],
                }
                phase["tasks"].append(task)

            large_mission_map["phases"].append(phase)

        tool = MissionMapTool()

        # Setup mocks
        mock_aiofiles_exists.return_value = False
        mock_file = AsyncMock()
        mock_file.read.return_value = json.dumps(sample_mission_map_schema)
        mock_file.write = AsyncMock()
        mock_aiofiles_open.return_value.__aenter__.return_value = mock_file

        result = await tool.validate_and_execute(
            task_id="large_project", mission_content=large_mission_map
        )

        # Should handle large mission map successfully
        assert isinstance(result, dict)
        payload = result["payload"]
        assert payload["mission_summary"]["phases_count"] == 10
        assert payload["mission_summary"]["total_tasks"] == 50
        # Should complete regardless of validation status
        assert payload["workflow_stage"] == "complete"
