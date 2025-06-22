"""Tests for Phase 2.8.1 Stage-Based Workflow Execution.

This module tests the enhanced stage-based workflow capabilities including:
- Individual stage execution (analysis, decomposition, task_graph, mission_map)
- Stage transition validation
- Payload structure enhancements
- Backward compatibility with monolithic execution
- Error handling for invalid stage transitions
- Suggested next state guidance
"""

import pytest
from typing import Dict, Any

from tools.architect_unified import (
    execute_architect_workflow
)
from schemas.universal_response import (
    CollaborativeStrategyResponse,
    ExecutionType
)
from schemas.architect_payloads import (
    ArchitectPayload, 
    WorkflowStage, 
    StageCompletionStatus,
    AnalysisResult,
    DecompositionResult,
    TaskGraphResult,
    MissionMapResult
)


# Module-level fixtures available to all test classes
@pytest.fixture
def sample_task_description() -> str:
    """Sample task description for testing."""
    return "Create a web application with user authentication and database integration"

@pytest.fixture
def sample_analysis_result() -> Dict[str, Any]:
    """Sample analysis result for testing stage continuation."""
    return {
        "keywords": ["web", "application", "authentication", "database"],
        "patterns": ["mvc", "authentication"],
        "complexity": "Media",
        "requirements_implicit": ["user management", "data persistence"],
        "domain": "web_application",
        "technology_stack": ["frontend", "backend", "database"]
    }

@pytest.fixture
def sample_decomposition_result() -> Dict[str, Any]:
    """Sample decomposition result for testing stage continuation."""
    return {
        "phases": [
            {
                "id": "setup",
                "name": "Project Setup",
                "description": "Initialize project structure",
                "estimated_duration": "1 day",
                "dependencies": [],
                "deliverables": ["project_structure"]
            },
            {
                "id": "development", 
                "name": "Development",
                "description": "Implement core features",
                "estimated_duration": "5 days",
                "dependencies": ["setup"],
                "deliverables": ["application", "authentication"]
            }
        ],
        "total_estimated_duration": "6 days",
        "critical_path": ["setup", "development"],
        "parallel_opportunities": []
    }


class TestStageBasedExecution:
    """Test stage-based workflow execution functionality."""
    
    def test_analysis_stage_execution(self, sample_task_description):
        """Test analysis stage executes independently and returns correct structure."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            workflow_stage="analysis",
            collaboration_mode="disabled"
        )
        
        # Verify response structure
        assert isinstance(result, CollaborativeStrategyResponse)
        assert isinstance(result.payload, ArchitectPayload)
        
        # Verify stage-specific content
        payload = result.payload
        assert payload.workflow_stage == WorkflowStage.ANALYSIS
        assert payload.analysis is not None
        assert payload.decomposition is None
        assert payload.task_graph is None
        assert payload.mission_map is None
        
        # Verify stage completion status
        assert payload.current_stage == "analysis"
        assert payload.stage_completion_status == StageCompletionStatus.COMPLETED
        assert payload.next_stage_requirements == ["analysis_result"]
        
        # Verify workflow continuation guidance
        assert payload.continue_workflow is True
        assert payload.next_step == "decomposition"
        assert payload.suggested_next_state is not None
        assert payload.suggested_next_state["workflow_stage"] == "decomposition"
        assert "analysis_result" in payload.suggested_next_state
        
        # Verify Claude instructions
        assert result.claude_instructions.execution_type == ExecutionType.IMMEDIATE
        assert len(result.claude_instructions.actions) > 0
        assert result.claude_instructions.actions[0].type == "continue_workflow"
    
    def test_decomposition_stage_execution(self, sample_task_description, sample_analysis_result):
        """Test decomposition stage executes with analysis results."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            analysis_result=sample_analysis_result,
            workflow_stage="decomposition",
            collaboration_mode="disabled"
        )
        
        # Verify response structure
        assert isinstance(result, CollaborativeStrategyResponse)
        payload = result.payload
        
        # Verify stage-specific content
        assert payload.workflow_stage == WorkflowStage.DECOMPOSITION
        assert payload.analysis is not None
        assert payload.decomposition is not None
        assert payload.task_graph is None
        assert payload.mission_map is None
        
        # Verify stage completion status
        assert payload.current_stage == "decomposition"
        assert payload.stage_completion_status == StageCompletionStatus.COMPLETED
        assert payload.next_stage_requirements == ["analysis_result", "decomposition_result"]
        
        # Verify workflow continuation guidance
        assert payload.continue_workflow is True
        assert payload.next_step == "task_graph"
        assert payload.suggested_next_state["workflow_stage"] == "task_graph"
        assert "decomposition_result" in payload.suggested_next_state
        
        # Verify decomposition content
        decomposition = payload.decomposition
        assert isinstance(decomposition, DecompositionResult)
        assert len(decomposition.phases) > 0
        assert decomposition.total_estimated_duration is not None
    
    def test_task_graph_stage_execution(self, sample_task_description, sample_analysis_result, sample_decomposition_result):
        """Test task graph stage executes with previous results."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            analysis_result=sample_analysis_result,
            decomposition_result=sample_decomposition_result,
            workflow_stage="task_graph",
            collaboration_mode="disabled"
        )
        
        # Verify response structure
        payload = result.payload
        
        # Verify stage-specific content
        assert payload.workflow_stage == WorkflowStage.TASK_GRAPH
        assert payload.analysis is not None
        assert payload.decomposition is not None
        assert payload.task_graph is not None
        assert payload.mission_map is None
        
        # Verify stage completion status
        assert payload.current_stage == "task_graph"
        assert payload.stage_completion_status == StageCompletionStatus.COMPLETED
        assert payload.next_stage_requirements == ["analysis_result", "decomposition_result", "task_graph_result"]
        
        # Verify workflow continuation guidance
        assert payload.continue_workflow is True
        assert payload.next_step == "mission_map"
        assert payload.suggested_next_state["workflow_stage"] == "mission_map"
        
        # Verify task graph content
        task_graph = payload.task_graph
        assert isinstance(task_graph, TaskGraphResult)
        assert task_graph.task_count > 0
        assert len(task_graph.tasks) > 0
    
    def test_mission_map_stage_execution(self, sample_task_description, sample_analysis_result, sample_decomposition_result):
        """Test mission map stage executes and completes workflow."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            analysis_result=sample_analysis_result,
            decomposition_result=sample_decomposition_result,
            workflow_stage="mission_map",
            collaboration_mode="disabled"
        )
        
        # Verify response structure
        payload = result.payload
        
        # Verify stage-specific content
        assert payload.workflow_stage == WorkflowStage.MISSION_MAP
        assert payload.analysis is not None
        assert payload.decomposition is not None
        assert payload.task_graph is not None
        assert payload.mission_map is not None
        
        # Verify stage completion status
        assert payload.current_stage == "mission_map"
        assert payload.stage_completion_status == StageCompletionStatus.COMPLETED
        assert payload.next_stage_requirements is None  # Workflow complete
        
        # Verify workflow completion
        assert payload.continue_workflow is False
        assert payload.next_step is None
        assert payload.suggested_next_state is None
        
        # Verify Claude instructions for completion
        assert result.claude_instructions.execution_type == ExecutionType.USER_CONFIRMATION
        
        # Verify mission map content
        mission_map = payload.mission_map
        assert isinstance(mission_map, MissionMapResult)
        assert len(mission_map.resource_assignments) > 0
        assert len(mission_map.execution_order) > 0
    
    def test_complete_stage_execution(self, sample_task_description):
        """Test complete stage executes full workflow."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            workflow_stage="complete",
            collaboration_mode="disabled"
        )
        
        # Should execute complete workflow
        payload = result.payload
        assert payload.workflow_stage == WorkflowStage.COMPLETE
        assert payload.analysis is not None
        assert payload.decomposition is not None
        assert payload.task_graph is not None
        assert payload.mission_map is not None
    
    def test_multi_stage_workflow_continuation(self, sample_task_description):
        """Test multi-stage workflow execution with continuation."""
        # Stage 1: Analysis
        analysis_result = execute_architect_workflow(
            task_description=sample_task_description,
            workflow_stage="analysis",
            collaboration_mode="disabled"
        )
        
        # Extract analysis for next stage
        analysis_data = analysis_result.payload.suggested_next_state["analysis_result"]
        
        # Stage 2: Decomposition
        decomposition_result = execute_architect_workflow(
            task_description=sample_task_description,
            analysis_result=analysis_data,
            workflow_stage="decomposition",
            collaboration_mode="disabled"
        )
        
        # Extract data for next stage
        decomposition_data = decomposition_result.payload.suggested_next_state["decomposition_result"]
        
        # Stage 3: Task Graph
        task_graph_result = execute_architect_workflow(
            task_description=sample_task_description,
            analysis_result=analysis_data,
            decomposition_result=decomposition_data,
            workflow_stage="task_graph",
            collaboration_mode="disabled"
        )
        
        # Stage 4: Mission Map
        final_result = execute_architect_workflow(
            task_description=sample_task_description,
            analysis_result=analysis_data,
            decomposition_result=decomposition_data,
            workflow_stage="mission_map",
            collaboration_mode="disabled"
        )
        
        # Verify final result completeness
        assert final_result.payload.workflow_stage == WorkflowStage.MISSION_MAP
        assert final_result.payload.continue_workflow is False
        assert final_result.payload.stage_completion_status == StageCompletionStatus.COMPLETED


class TestStageValidationAndErrorHandling:
    """Test stage validation and error handling."""
    
    def test_invalid_workflow_stage(self):
        """Test error handling for invalid workflow stage."""
        with pytest.raises(ValueError, match="Invalid workflow_stage"):
            execute_architect_workflow(
                task_description="Test task",
                workflow_stage="invalid_stage",
                collaboration_mode="disabled"
            )
    
    def test_decomposition_without_analysis(self):
        """Test error when decomposition stage lacks required analysis."""
        with pytest.raises(ValueError, match="analysis_result is required for decomposition stage"):
            execute_architect_workflow(
                task_description="Test task",
                workflow_stage="decomposition",
                collaboration_mode="disabled"
            )
    
    def test_task_graph_without_decomposition(self, sample_analysis_result):
        """Test error when task graph stage lacks required decomposition."""
        with pytest.raises(ValueError, match="decomposition_result is required for task_graph stage"):
            execute_architect_workflow(
                task_description="Test task",
                analysis_result=sample_analysis_result,
                workflow_stage="task_graph",
                collaboration_mode="disabled"
            )
    
    def test_mission_map_without_decomposition(self, sample_analysis_result):
        """Test error when mission map stage lacks required decomposition."""
        with pytest.raises(ValueError, match="decomposition_result is required for mission_map stage"):
            execute_architect_workflow(
                task_description="Test task",
                analysis_result=sample_analysis_result,
                workflow_stage="mission_map",
                collaboration_mode="disabled"
            )
    
    def test_empty_task_description_with_stage(self):
        """Test error handling for empty task description with stage."""
        with pytest.raises(ValueError, match="task_description cannot be empty"):
            execute_architect_workflow(
                task_description="",
                workflow_stage="analysis",
                collaboration_mode="disabled"
            )


class TestBackwardCompatibility:
    """Test backward compatibility with existing monolithic execution."""
    
    def test_backward_compatibility_no_workflow_stage(self, sample_task_description="Create a simple web app"):
        """Test that None workflow_stage executes complete workflow (backward compatibility)."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            workflow_stage=None,  # Backward compatibility mode
            collaboration_mode="disabled"
        )
        
        # Should execute complete workflow
        assert isinstance(result, CollaborativeStrategyResponse)
        payload = result.payload
        
        # Should have complete results
        assert payload.workflow_stage == WorkflowStage.COMPLETE
        assert payload.analysis is not None
        assert payload.decomposition is not None
        assert payload.task_graph is not None
        assert payload.mission_map is not None
    
    def test_existing_api_compatibility(self, sample_task_description="Create a mobile app"):
        """Test compatibility with existing API calls."""
        # Test with no stage parameter (should work as before)
        result = execute_architect_workflow(
            task_description=sample_task_description,
            collaboration_mode="disabled"
        )
        
        # Should have all expected fields from original StrategyResponse
        assert hasattr(result, 'strategy')
        assert hasattr(result, 'user_facing')
        assert hasattr(result, 'claude_instructions')
        assert hasattr(result, 'payload')
        assert hasattr(result, 'metadata')
        
        # Payload should have all expected analysis results
        payload = result.payload
        assert payload.analysis is not None
        assert payload.decomposition is not None
        assert payload.task_graph is not None
        assert payload.mission_map is not None


class TestPayloadStructureEnhancements:
    """Test enhanced payload structure with stage-specific fields."""
    
    def test_stage_specific_fields_present(self, sample_task_description="Test project"):
        """Test that new stage-specific fields are present."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            workflow_stage="analysis",
            collaboration_mode="disabled"
        )
        
        payload = result.payload
        
        # Test new Phase 2.8.1 fields
        assert hasattr(payload, 'current_stage')
        assert hasattr(payload, 'stage_completion_status')
        assert hasattr(payload, 'next_stage_requirements')
        
        # Test values
        assert payload.current_stage == "analysis"
        assert payload.stage_completion_status == StageCompletionStatus.COMPLETED
        assert isinstance(payload.next_stage_requirements, list)
        assert len(payload.next_stage_requirements) > 0
    
    def test_suggested_next_state_structure(self, sample_task_description="Test project"):
        """Test enhanced suggested_next_state structure."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            workflow_stage="analysis",
            collaboration_mode="disabled"
        )
        
        next_state = result.payload.suggested_next_state
        assert next_state is not None
        
        # Test required fields according to blueprint
        assert "workflow_stage" in next_state
        assert "continue_workflow" in next_state
        assert "next_stage" in next_state
        assert "required_inputs" in next_state
        assert "estimated_duration" in next_state
        
        # Test values
        assert next_state["workflow_stage"] == "decomposition"
        assert next_state["continue_workflow"] is True
        assert next_state["next_stage"] == "decomposition"
        assert isinstance(next_state["required_inputs"], dict)
    
    def test_stage_completion_status_enum(self, sample_task_description="Test project"):
        """Test StageCompletionStatus enum functionality."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            workflow_stage="analysis",
            collaboration_mode="disabled"
        )
        
        status = result.payload.stage_completion_status
        assert status in [StageCompletionStatus.COMPLETED, StageCompletionStatus.PARTIAL, StageCompletionStatus.ERROR]
        assert status == StageCompletionStatus.COMPLETED


class TestPerformanceAndMetadata:
    """Test performance preservation and metadata accuracy."""
    
    def test_stage_execution_performance(self, sample_task_description="Performance test project"):
        """Test that stage-based execution maintains good performance."""
        import time
        
        start_time = time.time()
        result = execute_architect_workflow(
            task_description=sample_task_description,
            workflow_stage="analysis",
            collaboration_mode="disabled"
        )
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Should complete quickly (< 2 seconds for analysis stage)
        assert execution_time < 2.0
        assert isinstance(result, CollaborativeStrategyResponse)
    
    def test_metadata_confidence_scores(self, sample_task_description="Metadata test project"):
        """Test metadata confidence scores for different stages."""
        # Analysis stage
        analysis_result = execute_architect_workflow(
            task_description=sample_task_description,
            workflow_stage="analysis",
            collaboration_mode="disabled"
        )
        assert 0.0 <= analysis_result.metadata.confidence_score <= 1.0
        
        # Decomposition stage (should have similar or higher confidence)
        decomp_result = execute_architect_workflow(
            task_description=sample_task_description,
            analysis_result=analysis_result.payload.suggested_next_state["analysis_result"],
            workflow_stage="decomposition",
            collaboration_mode="disabled"
        )
        assert 0.0 <= decomp_result.metadata.confidence_score <= 1.0
    
    def test_version_tracking(self, sample_task_description="Version test project"):
        """Test that stage-based execution updates version appropriately."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            workflow_stage="analysis",
            collaboration_mode="disabled"
        )
        
        # Should use updated version for staged execution
        assert result.strategy.name == "motor-de-estrategias-staged"
        assert result.strategy.version == "2.8.0"


if __name__ == "__main__":
    # Run specific tests for debugging
    pytest.main([__file__, "-v", "-s"])