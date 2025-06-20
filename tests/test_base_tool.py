"""Tests for Base Tool Class.

Following Principio Rector #1: Dogmatismo con Universal Response Schema.
Tests validate that base tool enforces StrategyResponse compliance.

CRITICAL TEST: Validates "Tool base retorna StrategyResponse válido".
"""

import pytest
from typing import Dict, Any
from pydantic import ValidationError

from tools.base_tool import BaseTool, MockTool
from schemas.universal_response import (
    StrategyResponse,
    StrategyType,
    ExecutionType,
    BasePayload
)
from schemas.architect_payloads import ArchitectPayload


class TestBaseTool:
    """Test BaseTool abstract base class."""
    
    def test_base_tool_initialization(self):
        """Test base tool initialization."""
        mock_tool = MockTool()
        assert mock_tool.tool_name == "mock-tool"
        assert mock_tool.tool_version == "1.0.0"
    
    def test_mock_tool_execute_success(self):
        """Test MockTool successful execution.
        
        CRITICAL TEST: Validates "Tool base retorna StrategyResponse válido".
        """
        mock_tool = MockTool()
        
        response = mock_tool.execute(test_input="test_value")
        
        # Validate it's a StrategyResponse
        assert isinstance(response, StrategyResponse)
        
        # Validate schema compliance
        assert response.strategy.name == "mock-tool"
        assert response.strategy.version == "1.0.0"
        assert response.strategy.type == StrategyType.ANALYSIS
        
        assert "Mock tool executed successfully" in response.user_facing.summary
        assert len(response.user_facing.key_points) > 0
        assert len(response.user_facing.next_steps) > 0
        
        assert response.claude_instructions.execution_type == ExecutionType.IMMEDIATE
        assert len(response.claude_instructions.actions) > 0
        
        assert response.payload.workflow_stage == "complete"
        assert response.payload.suggested_next_state is not None
        assert response.payload.suggested_next_state["mock_executed"] is True
        assert response.payload.suggested_next_state["test_input"] == "test_value"
        
        assert 0.0 <= response.metadata.confidence_score <= 1.0
        assert 1 <= response.metadata.complexity_score <= 10
    
    def test_mock_tool_execute_failure(self):
        """Test MockTool failure handling."""
        mock_tool = MockTool()
        
        with pytest.raises(ValueError):
            mock_tool.execute(should_fail=True)
    
    def test_validate_and_execute_success(self):
        """Test validate_and_execute with successful execution.
        
        CRITICAL TEST: Validates wrapper method returns valid StrategyResponse.
        """
        mock_tool = MockTool()
        
        result = mock_tool.validate_and_execute(test_input="wrapper_test")
        
        # Should return dict (serialized StrategyResponse)
        assert isinstance(result, dict)
        
        # Validate dict can be reconstructed as StrategyResponse
        response = StrategyResponse[BasePayload](**result)
        
        assert response.strategy.name == "mock-tool"
        assert "Mock tool executed successfully" in response.user_facing.summary
        assert response.payload.suggested_next_state["test_input"] == "wrapper_test"
    
    def test_validate_and_execute_tool_failure(self):
        """Test validate_and_execute with tool execution failure."""
        mock_tool = MockTool()
        
        result = mock_tool.validate_and_execute(should_fail=True)
        
        # Should still return valid dict (error response)
        assert isinstance(result, dict)
        
        # Validate error response structure
        response = StrategyResponse[BasePayload](**result)
        
        assert response.strategy.name == "mock-tool-error"
        assert "Error executing mock-tool" in response.user_facing.summary
        assert response.claude_instructions.execution_type == ExecutionType.USER_CONFIRMATION
        assert response.payload.workflow_stage == "error"
        assert response.payload.suggested_next_state["error_occurred"] is True
        assert response.metadata.confidence_score == 0.0
    
    def test_create_error_response(self):
        """Test error response creation."""
        mock_tool = MockTool()
        
        error_response = mock_tool._create_error_response("Test error", "test_error")
        
        assert isinstance(error_response, StrategyResponse)
        assert error_response.strategy.name == "mock-tool-error"
        assert "Error executing mock-tool: Test error" in error_response.user_facing.summary
        assert error_response.claude_instructions.execution_type == ExecutionType.USER_CONFIRMATION
        assert error_response.payload.workflow_stage == "error"
        assert error_response.payload.suggested_next_state["error_type"] == "test_error"
        assert error_response.metadata.confidence_score == 0.0
    
    def test_create_success_response(self):
        """Test success response creation helper."""
        mock_tool = MockTool()
        
        payload = BasePayload(
            workflow_stage="test",
            suggested_next_state={"test": "data"}
        )
        
        response = mock_tool.create_success_response(
            summary="Test summary",
            payload=payload,
            execution_type=ExecutionType.MULTI_STEP,
            confidence_score=0.8,
            complexity_score=7,
            key_points=["Point 1", "Point 2"],
            next_steps=["Step 1", "Step 2"]
        )
        
        assert isinstance(response, StrategyResponse)
        assert response.strategy.name == "mock-tool"
        assert response.user_facing.summary == "Test summary"
        assert response.user_facing.key_points == ["Point 1", "Point 2"]
        assert response.user_facing.next_steps == ["Step 1", "Step 2"]
        assert response.claude_instructions.execution_type == ExecutionType.MULTI_STEP
        assert response.payload.workflow_stage == "test"
        assert response.metadata.confidence_score == 0.8
        assert response.metadata.complexity_score == 7


class CustomTestTool(BaseTool[ArchitectPayload]):
    """Custom tool for testing BaseTool inheritance."""
    
    def __init__(self):
        super().__init__("custom-test-tool", "2.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        return StrategyType.EXECUTION
    
    def execute(self, **kwargs) -> StrategyResponse[ArchitectPayload]:
        from schemas.architect_payloads import ArchitectPayload, WorkflowStage
        
        payload = ArchitectPayload(workflow_stage=WorkflowStage.ANALYSIS)
        
        return self.create_success_response(
            summary="Custom tool executed",
            payload=payload,
            confidence_score=0.7,
            complexity_score=3
        )


class TestCustomTool:
    """Test custom tool implementation using BaseTool."""
    
    def test_custom_tool_inheritance(self):
        """Test that custom tools can inherit from BaseTool properly."""
        custom_tool = CustomTestTool()
        
        assert custom_tool.tool_name == "custom-test-tool"
        assert custom_tool.tool_version == "2.0.0"
        assert custom_tool.get_strategy_type() == StrategyType.EXECUTION
    
    def test_custom_tool_execute(self):
        """Test custom tool execution with ArchitectPayload.
        
        This validates that BaseTool works with different payload types.
        """
        custom_tool = CustomTestTool()
        
        response = custom_tool.execute()
        
        # Validate it's a StrategyResponse with ArchitectPayload
        assert isinstance(response, StrategyResponse)
        assert response.strategy.name == "custom-test-tool"
        assert response.strategy.type == StrategyType.EXECUTION
        
        # Validate payload is ArchitectPayload
        from schemas.architect_payloads import ArchitectPayload, WorkflowStage
        assert isinstance(response.payload, ArchitectPayload)
        assert response.payload.workflow_stage == WorkflowStage.ANALYSIS
    
    def test_custom_tool_validate_and_execute(self):
        """Test custom tool through validate_and_execute wrapper."""
        custom_tool = CustomTestTool()
        
        result = custom_tool.validate_and_execute()
        
        # Should return serialized dict
        assert isinstance(result, dict)
        
        # Should be reconstructable as StrategyResponse[ArchitectPayload]
        from schemas.architect_payloads import ArchitectPayload
        response = StrategyResponse[ArchitectPayload](**result)
        
        assert response.strategy.name == "custom-test-tool"
        assert response.payload.workflow_stage == "analysis"


class TestBaseToolValidation:
    """Test BaseTool validation and error handling."""
    
    def test_base_tool_enforces_strategy_response(self):
        """Test that BaseTool enforces StrategyResponse return type."""
        # This test would require a tool that doesn't return StrategyResponse
        # Since all proper implementations should return StrategyResponse,
        # we test this through the validation in validate_and_execute
        
        mock_tool = MockTool()
        
        # Test that proper responses pass validation
        result = mock_tool.validate_and_execute(test_input="validation_test")
        response = StrategyResponse[BasePayload](**result)
        
        assert response.strategy.name == "mock-tool"
        assert isinstance(response, StrategyResponse)
    
    def test_base_tool_schema_compliance(self):
        """Test that all BaseTool responses comply with Universal Response Schema."""
        mock_tool = MockTool()
        
        # Test successful execution
        success_result = mock_tool.validate_and_execute(test_input="schema_test")
        success_response = StrategyResponse[BasePayload](**success_result)
        
        # Validate all required fields are present
        assert success_response.strategy is not None
        assert success_response.user_facing is not None
        assert success_response.claude_instructions is not None
        assert success_response.payload is not None
        assert success_response.metadata is not None
        
        # Test error execution
        error_result = mock_tool.validate_and_execute(should_fail=True)
        error_response = StrategyResponse[BasePayload](**error_result)
        
        # Validate error response also complies with schema
        assert error_response.strategy is not None
        assert error_response.user_facing is not None
        assert error_response.claude_instructions is not None
        assert error_response.payload is not None
        assert error_response.metadata is not None
    
    def test_base_tool_confidence_bounds(self):
        """Test that confidence scores are within valid bounds."""
        mock_tool = MockTool()
        
        result = mock_tool.validate_and_execute()
        response = StrategyResponse[BasePayload](**result)
        
        assert 0.0 <= response.metadata.confidence_score <= 1.0
    
    def test_base_tool_complexity_bounds(self):
        """Test that complexity scores are within valid bounds."""
        mock_tool = MockTool()
        
        result = mock_tool.validate_and_execute()
        response = StrategyResponse[BasePayload](**result)
        
        assert 1 <= response.metadata.complexity_score <= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])