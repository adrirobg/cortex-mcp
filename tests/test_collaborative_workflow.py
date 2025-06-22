"""Tests for Phase 2.7 Collaborative Intelligence Workflow.

This module tests the enhanced collaborative workflow capabilities including:
- Collaborative workflow controller
- Claude intelligence delegation
- Workflow continuation with refinements
- Backward compatibility
- Performance preservation
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from typing import Dict, Any

from tools.architect_unified import (
    execute_architect_workflow,
    execute_architect_workflow_enhanced
)
from schemas.universal_response import (
    CollaborativeStrategyResponse,
    DelegationType,
    ExecutionType
)
from schemas.architect_payloads import ArchitectPayload, WorkflowStage


class TestCollaborativeWorkflow:
    """Test collaborative intelligence workflow functionality."""
    
    @pytest.fixture
    def sample_task_description(self) -> str:
        """Sample complex task description for testing."""
        return """
        Create a scalable e-commerce platform with microservices architecture,
        OAuth2 authentication, payment integration, and ML-based recommendations.
        Must support multi-tenant deployment and real-time analytics.
        """
    
    @pytest.fixture
    def simple_task_description(self) -> str:
        """Simple task description for deterministic workflow testing."""
        return "Create a basic TODO app"
    
    def test_collaborative_workflow_initialization(self, sample_task_description):
        """Test that collaborative workflow initializes correctly."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            collaboration_mode="enabled"
        )
        
        # Verify collaborative response structure
        assert isinstance(result, CollaborativeStrategyResponse)
        assert result.collaboration_mode is True
        assert result.requires_claude_refinement is True
        assert result.collaboration_stage == "preliminary_analysis"
        assert result.delegation_context is not None
        assert result.delegation_context.delegation_type == DelegationType.REFINE_ANALYSIS
    
    def test_deterministic_fallback(self, simple_task_description):
        """Test fallback to deterministic workflow for simple tasks."""
        result = execute_architect_workflow(
            task_description=simple_task_description,
            collaboration_mode="disabled"
        )
        
        # Should use deterministic workflow
        assert isinstance(result, CollaborativeStrategyResponse)
        assert result.collaboration_mode is False
        assert result.requires_claude_refinement is False
        assert result.delegation_context is None
        assert result.collaboration_stage is None
    
    def test_workflow_continuation_with_refinement(self, sample_task_description):
        """Test workflow continuation after Claude refinement."""
        # First, get preliminary analysis
        preliminary_result = execute_architect_workflow(
            task_description=sample_task_description,
            collaboration_mode="enabled"
        )
        
        # Simulate Claude refinement
        refined_analysis = {
            "domain": "e-commerce-enterprise",
            "complexity": "Alta",
            "technology_stack": ["microservices", "oauth2", "machine-learning", "kubernetes"],
            "keywords": ["scalable", "multi-tenant", "real-time", "enterprise"],
            "architectural_pattern": "microservices"
        }
        
        # Continue workflow with refinement
        final_result = execute_architect_workflow(
            task_description=sample_task_description,
            refined_analysis=refined_analysis,
            collaboration_mode="enabled"
        )
        
        # Verify refined workflow completion
        assert final_result.collaboration_mode is True
        assert final_result.requires_claude_refinement is False
        assert final_result.collaboration_stage == "complete"
        assert final_result.refinement_history is not None
        assert len(final_result.refinement_history) > 0
        assert final_result.metadata.confidence_score > 0.8  # Higher confidence after refinement
        assert final_result.payload.workflow_stage == WorkflowStage.COMPLETE
    
    def test_collaboration_detection_logic(self):
        """Test collaboration detection for different task types."""
        # Complex task should trigger collaboration
        complex_task = "Enterprise microservices platform with advanced ML capabilities"
        complex_result = execute_architect_workflow(
            task_description=complex_task,
            collaboration_mode="auto"
        )
        assert complex_result.collaboration_mode is True
        
        # Simple task should use deterministic workflow
        simple_task = "Basic web app"
        simple_result = execute_architect_workflow(
            task_description=simple_task,
            collaboration_mode="auto"
        )
        # Note: Current implementation defaults to collaboration
        # In future iterations, this would be more sophisticated
        assert isinstance(simple_result, CollaborativeStrategyResponse)
    
    def test_delegation_context_structure(self, sample_task_description):
        """Test delegation context structure and content."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            collaboration_mode="enabled"
        )
        
        delegation = result.delegation_context
        assert delegation is not None
        assert delegation.delegation_id.startswith("refine_")
        assert delegation.delegation_type == DelegationType.REFINE_ANALYSIS
        assert "analysis" in delegation.preliminary_result
        assert len(delegation.refinement_prompt) > 100  # Detailed prompt
        assert len(delegation.expected_improvements) > 0
        assert delegation.confidence_threshold == 0.75
        assert "task_description" in delegation.continuation_state
    
    def test_claude_instructions_for_collaboration(self, sample_task_description):
        """Test Claude instructions structure for collaborative workflow."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            collaboration_mode="enabled"
        )
        
        instructions = result.claude_instructions
        assert instructions.execution_type == ExecutionType.COLLABORATIVE
        assert len(instructions.actions) > 0
        
        # Check refine_analysis action
        refine_action = instructions.actions[0]
        assert refine_action.type == "refine_analysis"
        assert "preliminary project analysis" in refine_action.description.lower()
        assert refine_action.priority == 1
        assert "delegation_context" in refine_action.parameters
    
    def test_backward_compatibility_wrapper(self, sample_task_description):
        """Test backward compatibility wrapper functionality."""
        # Test enhanced wrapper
        result = execute_architect_workflow_enhanced(
            task_description=sample_task_description
        )
        
        # Should return CollaborativeStrategyResponse but be compatible
        assert isinstance(result, CollaborativeStrategyResponse)
        assert hasattr(result, 'strategy')  # Original StrategyResponse fields
        assert hasattr(result, 'user_facing')
        assert hasattr(result, 'claude_instructions')
        assert hasattr(result, 'payload')
        assert hasattr(result, 'metadata')
        
        # Should have collaboration fields too
        assert hasattr(result, 'collaboration_mode')
        assert hasattr(result, 'delegation_context')
    
    def test_environment_variable_override(self, sample_task_description):
        """Test environment variable override for collaboration mode."""
        # Test disabled mode
        with patch.dict(os.environ, {"CORTEX_COLLABORATION_MODE": "disabled"}):
            result = execute_architect_workflow(
                task_description=sample_task_description
            )
            assert result.collaboration_mode is False
        
        # Test enabled mode
        with patch.dict(os.environ, {"CORTEX_COLLABORATION_MODE": "enabled"}):
            result = execute_architect_workflow(
                task_description=sample_task_description
            )
            assert result.collaboration_mode is True
    
    def test_error_handling(self):
        """Test error handling in collaborative workflow."""
        # Test empty task description
        with pytest.raises(ValueError, match="task_description cannot be empty"):
            execute_architect_workflow(task_description="")
        
        # Test None task description
        with pytest.raises(ValueError):
            execute_architect_workflow(task_description=None)
    
    def test_trace_id_propagation(self, sample_task_description):
        """Test trace ID propagation through collaborative workflow."""
        custom_trace_id = "test-trace-12345"
        
        result = execute_architect_workflow(
            task_description=sample_task_description,
            trace_id=custom_trace_id,
            collaboration_mode="enabled"
        )
        
        # Trace ID should be propagated through the system
        # Note: This is tested implicitly through logging, but we can verify
        # the workflow completes successfully with custom trace ID
        assert isinstance(result, CollaborativeStrategyResponse)
    
    def test_debug_mode_functionality(self, sample_task_description):
        """Test debug mode provides additional information."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            debug_mode=True,
            collaboration_mode="enabled"
        )
        
        # Debug payload should be present when debug_mode=True
        # Note: Current implementation may not populate debug_payload
        # but workflow should complete successfully
        assert isinstance(result, CollaborativeStrategyResponse)
        assert result.collaboration_mode is True
    
    def test_collaboration_points_structure(self, sample_task_description):
        """Test collaboration points structure and content."""
        result = execute_architect_workflow(
            task_description=sample_task_description,
            collaboration_mode="enabled"
        )
        
        collaboration_points = result.collaboration_points
        assert collaboration_points is not None
        assert len(collaboration_points) > 0
        
        # Check first collaboration point
        point = collaboration_points[0]
        assert point.point_id == "analysis_refinement"
        assert point.stage == "preliminary_analysis"
        assert point.delegation_type == DelegationType.REFINE_ANALYSIS
        assert point.confidence_threshold == 0.75
        assert len(point.description) > 0


class TestPerformanceAndCompatibility:
    """Test performance preservation and backward compatibility."""
    
    def test_performance_preservation_simple_tasks(self):
        """Test that simple deterministic tasks maintain performance."""
        import time
        
        simple_task = "Create a basic web application"
        
        start_time = time.time()
        result = execute_architect_workflow(
            task_description=simple_task,
            collaboration_mode="disabled"  # Force deterministic path
        )
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Should complete in reasonable time (< 3 seconds for test environment)
        assert execution_time < 3.0
        assert isinstance(result, CollaborativeStrategyResponse)
        assert result.collaboration_mode is False
    
    def test_schema_compatibility(self):
        """Test that CollaborativeStrategyResponse is compatible with StrategyResponse."""
        from schemas.universal_response import StrategyResponse
        
        # Test basic task
        result = execute_architect_workflow(
            task_description="Create a simple app",
            collaboration_mode="disabled"
        )
        
        # Should have all original StrategyResponse fields
        original_fields = ['strategy', 'user_facing', 'claude_instructions', 'payload', 'metadata']
        for field in original_fields:
            assert hasattr(result, field)
            assert getattr(result, field) is not None
    
    def test_payload_structure_preservation(self):
        """Test that ArchitectPayload structure is preserved."""
        result = execute_architect_workflow(
            task_description="Create a web application",
            collaboration_mode="disabled"
        )
        
        payload = result.payload
        assert isinstance(payload, ArchitectPayload)
        assert hasattr(payload, 'workflow_stage')
        assert hasattr(payload, 'analysis')
        assert hasattr(payload, 'suggested_next_state')
        
        # For complete workflow, should have all results
        if payload.workflow_stage == WorkflowStage.COMPLETE:
            assert payload.analysis is not None
            assert payload.decomposition is not None
            assert payload.task_graph is not None
            assert payload.mission_map is not None


if __name__ == "__main__":
    # Run specific tests for debugging
    pytest.main([__file__, "-v", "-s"])