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


@pytest.mark.asyncio
class TestBaseTool:
    """Test BaseTool abstract base class."""
    
    async def test_base_tool_initialization(self):
        """Test base tool initialization."""
        mock_tool = MockTool()
        assert mock_tool.tool_name == "mock-tool"
        assert mock_tool.tool_version == "1.0.0"
    
    async def test_mock_tool_execute_success(self):
        """Test MockTool successful execution.
        
        CRITICAL TEST: Validates "Tool base retorna StrategyResponse válido".
        """
        mock_tool = MockTool()
        
        response = await mock_tool.execute(test_input="test_value")
        
        # Validate it's a StrategyResponse
        assert isinstance(response, StrategyResponse)
        
        # Validate schema compliance
        assert response.strategy.name == "mock-tool"
        assert response.strategy.version == "1.0.0"
        assert response.strategy.type == StrategyType.ANALYSIS
        
        assert "Mock tool executed successfully" in response.user_facing.summary
        assert len(response.user_facing.key_points) > 0
        
        # Validate payload
        assert response.payload.workflow_stage == "complete"
        assert response.payload.suggested_next_state["mock_executed"] is True
        assert response.payload.suggested_next_state["test_input"] == "test_value"
    
    async def test_mock_tool_execute_failure(self):
        """Test MockTool failure handling."""
        mock_tool = MockTool()
        
        with pytest.raises(ValueError):
            await mock_tool.execute(should_fail=True)
    
    async def test_validate_and_execute_success(self):
        """Test validate_and_execute with successful execution.
        
        CRITICAL TEST: Validates "validate_and_execute retorna Dict válido".
        """
        mock_tool = MockTool()
        
        result = await mock_tool.validate_and_execute(test_input="validate_test")
        
        # Must return Dict
        assert isinstance(result, dict)
        
        # Must contain StrategyResponse structure
        assert "strategy" in result
        assert "user_facing" in result
        assert "claude_instructions" in result
        assert "payload" in result
        assert "metadata" in result
        
        # Validate strategy section
        assert result["strategy"]["name"] == "mock-tool"
        assert result["strategy"]["version"] == "1.0.0"
        assert result["strategy"]["type"] == "analysis"
    
    async def test_validate_and_execute_tool_failure(self):
        """Test validate_and_execute handling tool failures."""
        mock_tool = MockTool()
        
        # Should not raise exception but return error response
        result = await mock_tool.validate_and_execute(should_fail=True)
        
        assert isinstance(result, dict)
        assert "Error executing mock-tool" in result["user_facing"]["summary"]


@pytest.mark.asyncio 
class TestBaseToolValidation:
    """Test base tool validation and schema compliance."""
    
    async def test_base_tool_enforces_strategy_response(self):
        """Test that base tool enforces StrategyResponse return type."""
        mock_tool = MockTool()
        
        result = await mock_tool.validate_and_execute()
        response = StrategyResponse[BasePayload](**result)
        
        # Should not raise ValidationError
        assert isinstance(response, StrategyResponse)
    
    async def test_base_tool_schema_compliance(self):
        """Test that returned data follows Universal Response Schema."""
        mock_tool = MockTool()
        
        result = await mock_tool.validate_and_execute(test_input="schema_test")
        
        # Validate required fields exist
        required_fields = ["strategy", "user_facing", "claude_instructions", "payload", "metadata"]
        for field in required_fields:
            assert field in result
        
        # Validate strategy structure
        strategy = result["strategy"]
        assert "name" in strategy
        assert "version" in strategy
        assert "type" in strategy
        
        # Validate user_facing structure
        user_facing = result["user_facing"]
        assert "summary" in user_facing
        assert "key_points" in user_facing
        assert "next_steps" in user_facing
    
    async def test_base_tool_confidence_bounds(self):
        """Test that confidence scores are within valid bounds."""
        mock_tool = MockTool()
        
        result = await mock_tool.validate_and_execute()
        response = StrategyResponse[BasePayload](**result)
        
        # Confidence should be between 0 and 1
        assert 0.0 <= response.metadata.confidence_score <= 1.0
    
    async def test_base_tool_complexity_bounds(self):
        """Test that complexity scores are within valid bounds."""
        mock_tool = MockTool()
        
        result = await mock_tool.validate_and_execute()
        response = StrategyResponse[BasePayload](**result)
        
        # Complexity should be between 1 and 10
        assert 1 <= response.metadata.complexity_score <= 10