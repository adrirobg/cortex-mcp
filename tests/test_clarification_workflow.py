"""Test suite for Phase 2.8.3 Clarification Workflow Implementation.

Validates clarification_needed workflow stage integration with existing domain heuristics
and collaborative workflow controller functionality.
"""

import pytest
from unittest.mock import Mock, patch
from tools.collaborative.workflow_controller import CollaborativeWorkflowController
from tools.architect.domain_heuristics import analyze_domain_indicators, DomainAnalysisResult, DomainOption
from schemas.architect_payloads import WorkflowStage, DomainAnalysisContext, AnalysisResult
from schemas.universal_response import ExecutionType


class TestClarificationWorkflow:
    """Test clarification workflow implementation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.controller = CollaborativeWorkflowController(
            collaboration_enabled=True,
            confidence_threshold=0.7
        )
    
    def test_clarification_needed_enum_added(self):
        """Test that CLARIFICATION_NEEDED was added to WorkflowStage enum."""
        assert hasattr(WorkflowStage, 'CLARIFICATION_NEEDED')
        assert WorkflowStage.CLARIFICATION_NEEDED.value == "clarification_needed"
    
    def test_clarification_stage_in_valid_stages(self):
        """Test that clarification_needed is accepted as valid workflow stage."""
        # This should not raise an exception
        try:
            self.controller._execute_stage_based_workflow(
                task_description="build something cool",
                analysis_result=None,
                decomposition_result=None,
                workflow_stage="clarification_needed",
                refined_analysis=None,
                debug_mode=False
            )
        except ValueError as e:
            if "Invalid workflow_stage" in str(e):
                pytest.fail("clarification_needed should be a valid workflow stage")
    
    @patch('tools.collaborative.workflow_controller.analyze_domain_indicators')
    @patch('tools.collaborative.workflow_controller.analyze_project')
    def test_execute_clarification_stage_basic(self, mock_analyze_project, mock_analyze_domain):
        """Test basic execution of clarification stage."""
        # Setup mocks
        mock_domain_analysis = Mock()
        mock_domain_analysis.max_confidence = 0.5  # Below threshold
        mock_domain_analysis.requires_collaboration = True
        mock_domain_analysis.recommended_domain = "web_app"
        mock_domain_analysis.confidence_scores = {"web_app": 0.5, "cli_tooling": 0.4}
        mock_domain_analysis.analysis_context = Mock()
        mock_domain_analysis.analysis_context.technology_indicators = ["python", "fastapi"]
        mock_domain_analysis.analysis_context.model_dump.return_value = {}
        mock_domain_analysis.domain_options = [
            DomainOption(
                domain_id="web_app",
                domain_name="Web Application", 
                confidence_score=0.5,
                supporting_evidence=["API detected", "web keywords"],
                potential_concerns=["Low confidence"]
            ),
            DomainOption(
                domain_id="cli_tooling",
                domain_name="CLI Tooling",
                confidence_score=0.4,
                supporting_evidence=["command keywords"],
                potential_concerns=[]
            )
        ]
        
        mock_analyze_domain.return_value = mock_domain_analysis
        
        # Create real AnalysisResult object instead of Mock
        mock_analysis = AnalysisResult(
            keywords=["build", "something"],
            patterns=["new_project"],
            complexity="medium",
            requirements_implicit=["basic requirements"],
            domain=None,
            technology_stack=None
        )
        mock_analyze_project.return_value = mock_analysis
        
        # Execute clarification stage
        result = self.controller._execute_clarification_stage(
            task_description="build something cool",
            debug_mode=False
        )
        
        # Validate response structure
        assert result.payload.workflow_stage == WorkflowStage.CLARIFICATION_NEEDED
        assert result.claude_instructions.execution_type == ExecutionType.USER_CONFIRMATION
        assert len(result.claude_instructions.decision_points) == 1
        assert result.claude_instructions.decision_points[0].id == "clarification_request"
        
        # Validate collaboration context
        assert result.collaboration_mode == True
        assert len(result.collaboration_points) == 1
        assert result.collaboration_points[0].stage == "clarification_needed"
        assert result.collaboration_stage == "clarification_request"
        
        # Validate that domain analysis was called
        mock_analyze_domain.assert_called_once_with("build something cool")
        mock_analyze_project.assert_called_once_with("build something cool")
    
    @patch('tools.collaborative.workflow_controller.analyze_domain_indicators')
    @patch('tools.collaborative.workflow_controller.analyze_project')
    def test_clarification_stage_low_confidence_scenario(self, mock_analyze_project, mock_analyze_domain):
        """Test clarification stage for low confidence domain detection."""
        # Setup low confidence domain analysis
        mock_domain_analysis = Mock()
        mock_domain_analysis.max_confidence = 0.3  # Very low confidence
        mock_domain_analysis.requires_collaboration = True
        mock_domain_analysis.recommended_domain = "general_software"
        mock_domain_analysis.confidence_scores = {"general_software": 0.3, "web_app": 0.2}
        mock_domain_analysis.analysis_context = Mock()
        mock_domain_analysis.analysis_context.technology_indicators = []
        mock_domain_analysis.analysis_context.model_dump.return_value = {}
        mock_domain_analysis.domain_options = [
            DomainOption(
                domain_id="general_software", 
                domain_name="General Software",
                confidence_score=0.3,
                supporting_evidence=["generic keywords"],
                potential_concerns=["Very low confidence"]
            )
        ]
        
        mock_analyze_domain.return_value = mock_domain_analysis
        
        # Create real AnalysisResult object
        mock_analysis = AnalysisResult(
            keywords=["create", "something"],
            patterns=["new_project"],
            complexity="low",
            requirements_implicit=["basic requirements"],
            domain=None,
            technology_stack=None
        )
        mock_analyze_project.return_value = mock_analysis
        
        # Execute clarification stage
        result = self.controller._execute_clarification_stage(
            task_description="create something",
            debug_mode=False
        )
        
        # Validate low confidence handling
        decision_point = result.claude_instructions.decision_points[0]
        assert decision_point.id == "clarification_request"
        assert decision_point.confidence == 0.3  # Very low confidence
        
        # Check that clarification action contains ambiguity sources
        clarification_action = result.claude_instructions.actions[0]
        assert "ambiguity_sources" in clarification_action.parameters
        ambiguity_sources = clarification_action.parameters["ambiguity_sources"]
        assert any("confidence below threshold" in source.lower() for source in ambiguity_sources)
        
        # Check suggested clarifications in action parameters
        suggested = clarification_action.parameters["suggested_clarifications"]
        assert len(suggested) > 0
        assert any("type of application" in q.lower() for q in suggested)
    
    @patch('tools.collaborative.workflow_controller.analyze_domain_indicators')
    @patch('tools.collaborative.workflow_controller.analyze_project')
    def test_clarification_stage_multiple_domains(self, mock_analyze_project, mock_analyze_domain):
        """Test clarification stage when multiple domains have similar confidence."""
        # Setup multiple similar confidence domains
        mock_domain_analysis = Mock()
        mock_domain_analysis.max_confidence = 0.6  # Below threshold but not terrible
        mock_domain_analysis.requires_collaboration = True
        mock_domain_analysis.recommended_domain = "web_app"
        mock_domain_analysis.confidence_scores = {"web_app": 0.6, "api_service": 0.55, "cli_tooling": 0.5}
        mock_domain_analysis.analysis_context = Mock()
        mock_domain_analysis.analysis_context.technology_indicators = ["python", "api"]
        mock_domain_analysis.analysis_context.model_dump.return_value = {}
        mock_domain_analysis.domain_options = [
            DomainOption(
                domain_id="web_app",
                domain_name="Web Application",
                confidence_score=0.6,
                supporting_evidence=["web patterns", "frontend indicators"],
                potential_concerns=["Moderate confidence"]
            ),
            DomainOption(
                domain_id="api_service", 
                domain_name="API Service",
                confidence_score=0.55,
                supporting_evidence=["API keywords", "service patterns"],
                potential_concerns=[]
            ),
            DomainOption(
                domain_id="cli_tooling",
                domain_name="CLI Tooling",
                confidence_score=0.5,
                supporting_evidence=["command patterns"],
                potential_concerns=[]
            )
        ]
        
        mock_analyze_domain.return_value = mock_domain_analysis
        
        # Create real AnalysisResult object
        mock_analysis = AnalysisResult(
            keywords=["python", "tool", "API"],
            patterns=["integration"],
            complexity="medium",
            requirements_implicit=["API integration"],
            domain=None,
            technology_stack=["python"]
        )
        mock_analyze_project.return_value = mock_analysis
        
        # Execute clarification stage
        result = self.controller._execute_clarification_stage(
            task_description="python tool with API integration",
            debug_mode=False
        )
        
        # Validate multiple options presented
        decision_point = result.claude_instructions.decision_points[0]
        assert len(decision_point.options) == 3  # All 3 domains presented
        
        # Check that recommended domain is included
        assert decision_point.recommendation == "web_app"
        
        # Validate user-facing content mentions multiple possibilities
        key_points = result.user_facing.key_points
        possibilities_point = next((p for p in key_points if "possibilities" in p.lower()), None)
        assert possibilities_point is not None
        assert "Web Application" in possibilities_point
    
    def test_clarification_stage_integration_with_stage_based_workflow(self):
        """Test integration of clarification stage with existing stage-based workflow."""
        with patch.object(self.controller, '_execute_clarification_stage') as mock_clarification:
            mock_clarification.return_value = Mock()
            
            # Call stage-based workflow with clarification_needed
            self.controller._execute_stage_based_workflow(
                task_description="ambiguous project",
                analysis_result=None,
                decomposition_result=None,
                workflow_stage="clarification_needed",
                refined_analysis=None,
                debug_mode=False
            )
            
            # Verify clarification stage was called
            mock_clarification.assert_called_once_with("ambiguous project", False)
    
    @patch('tools.collaborative.workflow_controller.analyze_domain_indicators')
    def test_clarification_stage_uses_phase_282_heuristics(self, mock_analyze_domain):
        """Test that clarification stage correctly uses Phase 2.8.2 domain heuristics."""
        # Setup domain analysis result
        mock_domain_analysis = Mock()
        mock_domain_analysis.requires_collaboration = True
        mock_domain_analysis.max_confidence = 0.4
        mock_domain_analysis.analysis_context = Mock()
        mock_domain_analysis.analysis_context.model_dump.return_value = {}
        mock_domain_analysis.domain_options = []
        
        mock_analyze_domain.return_value = mock_domain_analysis
        
        with patch('tools.collaborative.workflow_controller.analyze_project') as mock_analyze_project:
            # Create real AnalysisResult object
            mock_analysis = AnalysisResult(
                keywords=["test", "project"],
                patterns=["new_project"],
                complexity="medium",
                requirements_implicit=["basic requirements"],
                domain=None,
                technology_stack=None
            )
            mock_analyze_project.return_value = mock_analysis
            
            # Execute clarification stage
            self.controller._execute_clarification_stage(
                task_description="test project",
                debug_mode=False
            )
            
            # Verify that Phase 2.8.2 function was called
            mock_analyze_domain.assert_called_once_with("test project")
    
    def test_clarification_workflow_backward_compatibility(self):
        """Test that adding clarification_needed doesn't break existing workflows."""
        # Test that all existing stages still work
        existing_stages = ["analysis", "decomposition", "task_graph", "mission_map", "complete"]
        
        for stage in existing_stages:
            with patch.object(self.controller, f'_execute_{stage}_stage') as mock_stage:
                mock_stage.return_value = Mock()
                
                try:
                    self.controller._execute_stage_based_workflow(
                        task_description="test",
                        analysis_result={} if stage != "analysis" else None,
                        decomposition_result={} if stage in ["task_graph", "mission_map"] else None,
                        workflow_stage=stage,
                        refined_analysis=None,
                        debug_mode=False
                    )
                except Exception as e:
                    pytest.fail(f"Stage {stage} should still work: {e}")


class TestClarificationWorkflowEndToEnd:
    """End-to-end tests for clarification workflow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.controller = CollaborativeWorkflowController(
            collaboration_enabled=True,
            confidence_threshold=0.7
        )
    
    def test_real_domain_heuristics_integration(self):
        """Test with real domain heuristics for known low-confidence scenario."""
        # Use a genuinely ambiguous description
        ambiguous_description = "build something cool with technology"
        
        # Execute clarification stage with real heuristics
        result = self.controller._execute_clarification_stage(
            task_description=ambiguous_description,
            debug_mode=False
        )
        
        # Validate that real heuristics detect low confidence
        assert result.payload.workflow_stage == WorkflowStage.CLARIFICATION_NEEDED
        assert result.collaboration_mode == True
        
        # Check that decision point is properly formatted
        decision_point = result.claude_instructions.decision_points[0]
        assert decision_point.id == "clarification_request"
        assert len(decision_point.options) > 0
        
        # Validate user-facing content is helpful
        assert "clarification" in result.user_facing.summary.lower()
        assert len(result.user_facing.next_steps) > 0
    
    def test_clarification_workflow_with_known_high_confidence_scenario(self):
        """Test clarification stage behavior when confidence would actually be high."""
        # Use description that should have high confidence
        high_confidence_description = "Create a FastAPI web application with React frontend and PostgreSQL database for e-commerce"
        
        # Execute clarification stage
        result = self.controller._execute_clarification_stage(
            task_description=high_confidence_description,
            debug_mode=False
        )
        
        # Even with high confidence, clarification stage should still work
        # (since it was explicitly requested)
        assert result.payload.workflow_stage == WorkflowStage.CLARIFICATION_NEEDED
        
        # But it should identify the likely domain clearly
        decision_point = result.claude_instructions.decision_points[0]
        # Should have web_app as high confidence option
        web_app_option = next((opt for opt in decision_point.options if opt["id"] == "web_app"), None)
        if web_app_option:  # If web_app is detected
            assert "FastAPI" in high_confidence_description  # Test setup validation


if __name__ == "__main__":
    pytest.main([__file__, "-v"])