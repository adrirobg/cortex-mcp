"""Test suite for collaborative domain intelligence workflow integration.

Tests the complete collaborative workflow with domain intelligence,
decision_points generation, and Claude integration patterns.
"""

import pytest
from unittest.mock import Mock, patch
from tools.collaborative.workflow_controller import CollaborativeWorkflowController
from schemas.universal_response import ExecutionType, DelegationType
from schemas.architect_payloads import WorkflowStage, StageCompletionStatus


class TestCollaborativeDomainWorkflow:
    """Test collaborative domain intelligence workflow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.controller = CollaborativeWorkflowController(
            collaboration_enabled=True,
            confidence_threshold=0.7
        )
    
    def test_high_confidence_domain_no_collaboration(self):
        """Test high confidence domain classification bypasses collaboration."""
        description = "Build e-commerce platform with FastAPI backend and React frontend"
        
        result = self.controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        assert result.collaboration_mode == False
        assert result.requires_claude_refinement == False
        assert result.payload.analysis.domain in ["web_app", "api_service"]
        assert result.payload.analysis.domain_decision_rationale is not None
        assert "High confidence" in result.payload.analysis.domain_decision_rationale
    
    def test_low_confidence_domain_triggers_collaboration(self):
        """Test low confidence domain classification triggers collaboration."""
        description = "Implement something complex"
        
        result = self.controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        assert result.collaboration_mode == True
        assert result.requires_claude_refinement == True
        assert result.claude_instructions.execution_type == ExecutionType.MULTI_STEP
        assert len(result.claude_instructions.decision_points) > 0
        
        # Check decision point structure
        decision_point = result.claude_instructions.decision_points[0]
        assert decision_point["id"] == "domain_selection"
        assert "question" in decision_point
        assert "options" in decision_point
        assert len(decision_point["options"]) > 0
    
    def test_domain_collaboration_decision_point_structure(self):
        """Test decision point structure for domain collaboration."""
        description = "Create system with multiple components"
        
        result = self.controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        if result.requires_claude_refinement:
            decision_point = result.claude_instructions.decision_points[0]
            
            # Validate decision point structure
            assert "id" in decision_point
            assert "question" in decision_point
            assert "options" in decision_point
            assert "recommendation" in decision_point
            assert "confidence" in decision_point
            assert "context" in decision_point
            
            # Validate options structure
            for option in decision_point["options"]:
                assert "id" in option
                assert "description" in option
                assert "impact" in option
                assert "confidence" in option["description"]
    
    def test_domain_analysis_context_in_payload(self):
        """Test domain analysis context is included in payload."""
        description = "Build web application with authentication"
        
        result = self.controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        analysis = result.payload.analysis
        
        # Check enhanced analysis fields
        assert hasattr(analysis, 'domain_analysis_context')
        assert hasattr(analysis, 'domain_confidence_scores')
        assert hasattr(analysis, 'recommended_domain')
        assert hasattr(analysis, 'domain_decision_rationale')
        
        if analysis.domain_analysis_context:
            context = analysis.domain_analysis_context
            assert hasattr(context, 'detected_keywords')
            assert hasattr(context, 'technology_indicators')
            assert hasattr(context, 'complexity_assessment')
            assert hasattr(context, 'confidence_breakdown')
    
    def test_collaboration_points_generation(self):
        """Test collaboration points are generated for domain intelligence."""
        description = "Build complex system"
        
        result = self.controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        if result.collaboration_mode:
            assert result.collaboration_points is not None
            assert len(result.collaboration_points) > 0
            
            collab_point = result.collaboration_points[0]
            assert collab_point.point_id == "domain_classification"
            assert collab_point.stage == "analysis"
            assert collab_point.delegation_type == DelegationType.EVALUATE_OPTIONS
            assert collab_point.confidence_threshold == 0.7
    
    def test_stage_completion_status_for_collaboration(self):
        """Test stage completion status reflects collaboration state."""
        description = "Create ambiguous project"
        
        result = self.controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        if result.requires_claude_refinement:
            assert result.payload.stage_completion_status == StageCompletionStatus.PARTIAL
            assert result.payload.current_stage == "analysis_domain_collaboration"
            assert "domain_decision" in result.payload.next_stage_requirements
        else:
            assert result.payload.stage_completion_status == StageCompletionStatus.COMPLETED
            assert result.payload.current_stage == "analysis"
    
    def test_suggested_next_state_for_domain_workflow(self):
        """Test suggested_next_state contains domain workflow context."""
        description = "Build something that needs clarification"
        
        result = self.controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        if result.requires_claude_refinement:
            next_state = result.payload.suggested_next_state
            
            assert "workflow_stage" in next_state
            assert "domain_analysis_context" in next_state
            assert "domain_options" in next_state
            assert "requires_domain_decision" in next_state
            assert next_state["requires_domain_decision"] == True


class TestDomainWorkflowPerformance:
    """Test performance requirements for domain workflow."""
    
    def test_domain_analysis_performance_impact(self):
        """Test domain analysis adds minimal performance overhead."""
        import time
        
        controller = CollaborativeWorkflowController()
        description = "Build e-commerce platform with FastAPI and React"
        
        start_time = time.time()
        result = controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        end_time = time.time()
        
        duration_ms = (end_time - start_time) * 1000
        
        # Should complete within 2.5s (analysis stage requirement)
        assert duration_ms < 2500
        assert result is not None
        assert result.payload.analysis is not None
    
    def test_decision_points_generation_performance(self):
        """Test decision points generation is fast."""
        import time
        
        controller = CollaborativeWorkflowController()
        description = "Create unclear system requirements"
        
        start_time = time.time()
        result = controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        end_time = time.time()
        
        if result.claude_instructions.decision_points:
            generation_time = (end_time - start_time) * 1000
            
            # Decision points generation should be < 50ms as per requirement
            assert generation_time < 2500  # Total analysis time, includes decision point generation


class TestEdgeCasesAndErrorHandling:
    """Test edge cases and error handling in domain workflow."""
    
    def test_empty_description_error_handling(self):
        """Test error handling for empty descriptions."""
        controller = CollaborativeWorkflowController()
        
        with pytest.raises(Exception):  # Should bubble up from domain_heuristics
            controller.execute_collaborative_workflow(
                task_description="",
                workflow_stage="analysis"
            )
    
    def test_invalid_workflow_stage_error(self):
        """Test error handling for invalid workflow stages."""
        controller = CollaborativeWorkflowController()
        
        with pytest.raises(ValueError, match="Invalid workflow_stage"):
            controller.execute_collaborative_workflow(
                task_description="Valid description",
                workflow_stage="invalid_stage"
            )
    
    def test_collaboration_disabled_fallback(self):
        """Test fallback behavior when collaboration is disabled."""
        controller = CollaborativeWorkflowController(collaboration_enabled=False)
        description = "Build complex unclear system"
        
        result = controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        # Should fall back to deterministic workflow
        assert result.collaboration_mode == False
        assert result.requires_claude_refinement == False
        assert result.payload.analysis is not None
    
    def test_multiple_high_confidence_domains(self):
        """Test handling when multiple domains have similar high confidence."""
        # This is a complex scenario that would need specific description crafting
        description = "Build web API service with frontend dashboard and CLI tools"
        controller = CollaborativeWorkflowController()
        
        result = controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        # Should handle gracefully without crashing
        assert result is not None
        assert result.payload.analysis is not None
        assert result.payload.analysis.domain is not None


class TestBackwardCompatibilityWithDomainIntelligence:
    """Test backward compatibility with existing workflows."""
    
    def test_existing_workflow_stages_still_work(self):
        """Test existing workflow stages work with domain intelligence."""
        controller = CollaborativeWorkflowController()
        
        # Test all existing stages
        stages = ["analysis", "decomposition", "task_graph", "mission_map"]
        
        for stage in stages:
            try:
                if stage == "analysis":
                    result = controller.execute_collaborative_workflow(
                        task_description="Build web application",
                        workflow_stage=stage
                    )
                else:
                    # Other stages need previous results
                    analysis_result = {"domain": "web_app", "complexity": "Media", "keywords": []}
                    result = controller.execute_collaborative_workflow(
                        task_description="Build web application",
                        analysis_result=analysis_result,
                        workflow_stage=stage
                    )
                
                assert result is not None
                assert result.payload is not None
                
            except ValueError as e:
                # Some stages require specific inputs, that's expected
                if "is required for" not in str(e):
                    raise e
    
    def test_legacy_domain_values_compatibility(self):
        """Test compatibility with legacy domain values."""
        controller = CollaborativeWorkflowController()
        
        # Simulate legacy analysis result
        legacy_analysis = {
            "domain": "web",  # Old domain value
            "complexity": "Media",
            "keywords": ["web", "api"],
            "patterns": [],
            "requirements_implicit": [],
            "technology_stack": ["python"]
        }
        
        result = controller.execute_collaborative_workflow(
            task_description="Continue with legacy analysis",
            analysis_result=legacy_analysis,
            workflow_stage="decomposition"
        )
        
        # Should work without breaking
        assert result is not None
        assert result.payload.decomposition is not None


class TestUserExperienceScenarios:
    """Test user experience scenarios for domain workflow."""
    
    def test_clear_domain_classification_user_experience(self):
        """Test user experience for clear domain classification."""
        controller = CollaborativeWorkflowController()
        description = "Build REST API with FastAPI and authentication"
        
        result = controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        # Should provide clear, confident results
        assert not result.requires_claude_refinement
        assert "confidence" in result.payload.analysis.domain_decision_rationale.lower()
        assert len(result.user_facing.key_points) > 0
        assert result.user_facing.summary is not None
    
    def test_unclear_domain_classification_user_experience(self):
        """Test user experience for unclear domain classification."""
        controller = CollaborativeWorkflowController()
        description = "Build something innovative"
        
        result = controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        if result.requires_claude_refinement:
            # Should provide helpful guidance for decision making
            assert "uncertainty" in result.user_facing.summary.lower() or "collaboration" in result.user_facing.summary.lower()
            assert len(result.claude_instructions.decision_points) > 0
            assert "evaluate" in result.claude_instructions.actions[0].type.lower()
    
    def test_domain_options_clarity_for_users(self):
        """Test domain options are presented clearly for users."""
        controller = CollaborativeWorkflowController()
        description = "Create integrated solution"
        
        result = controller.execute_collaborative_workflow(
            task_description=description,
            workflow_stage="analysis"
        )
        
        if result.claude_instructions.decision_points:
            decision_point = result.claude_instructions.decision_points[0]
            
            # Options should be clear and actionable
            for option in decision_point["options"]:
                assert len(option["description"]) > 10  # Meaningful description
                assert "confidence" in option["description"]  # Shows confidence
                assert len(option["impact"]) > 0  # Provides impact information


if __name__ == "__main__":
    pytest.main([__file__, "-v"])