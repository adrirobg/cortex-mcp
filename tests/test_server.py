"""Tests for MCP Server implementation.

Following Principio Rector #2: Servidor como Ejecutor Fiable.
Tests validate FastMCP integration and tool functionality.
"""

import json
import pytest
import asyncio
from unittest.mock import patch
from pydantic import ValidationError

from server import app as mcp_app, strategy_architect
from schemas.universal_response import StrategyResponse, BasePayload


class TestMCPServer:
    """Test MCP Server core functionality."""
    
    def test_server_initialization(self):
        """Test server initializes correctly."""
        # Test that the FastMCP app is properly configured
        assert mcp_app.name == "cortex-mcp"
        # Test that strategy-architect tool is registered
        tools = asyncio.run(mcp_app.list_tools())
        tool_names = [tool.name for tool in tools]
        assert "strategy-architect" in tool_names
    
    def test_strategy_architect_tool_available(self):
        """Test strategy-architect tool is available and callable."""
        # Test that the strategy_architect function exists
        assert callable(strategy_architect)
        # Test tool metadata
        tools = asyncio.run(mcp_app.list_tools())
        strategy_tool = next((tool for tool in tools if tool.name == "strategy-architect"), None)
        assert strategy_tool is not None
        assert strategy_tool.description
        assert strategy_tool.inputSchema

    def test_handle_tools_list(self):
        """Test tools/list request handling.
        
        This is the CRITICAL validation criteria: 'Servidor responde a tools/list'
        """
        tools = asyncio.run(mcp_app.list_tools())
        
        assert len(tools) == 1
        
        tool = tools[0]
        assert tool.name == "strategy-architect"
        assert tool.description
        assert tool.inputSchema
        
        # Validate schema structure
        schema = tool.inputSchema
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "task_description" in schema["properties"]
        assert "required" in schema
        assert "task_description" in schema["required"]

    def test_strategy_architect_function_execution(self):
        """Test strategy-architect function executes successfully."""
        # Test with minimal valid input
        result = strategy_architect("Build a simple web application")
        
        # Should return JSON string
        assert isinstance(result, str)
        
        # Should be valid JSON
        parsed = json.loads(result)
        assert "user_facing" in parsed
        assert "claude_instructions" in parsed
        assert "payload" in parsed
        assert "metadata" in parsed

    def test_strategy_architect_with_optional_params(self):
        """Test strategy-architect with optional parameters."""
        result = strategy_architect(
            task_description="Build a REST API",
            workflow_stage="analysis"
        )
        
        # Should return valid StrategyResponse JSON
        parsed = json.loads(result)
        response = StrategyResponse[BasePayload](**parsed)
        assert response.user_facing.summary
        assert response.claude_instructions.actions
        assert response.metadata.confidence_score > 0

    def test_strategy_architect_response_schema_validation(self):
        """Test that strategy-architect returns valid StrategyResponse."""
        result = strategy_architect("Create a task management system")
        
        # Parse JSON and validate against schema
        response_data = json.loads(result)
        
        # This should not raise ValidationError
        strategy_response = StrategyResponse[BasePayload](**response_data)
        
        # Validate essential fields are present
        assert strategy_response.user_facing.summary
        assert strategy_response.claude_instructions.execution_type
        assert len(strategy_response.claude_instructions.actions) > 0
        assert strategy_response.metadata.confidence_score >= 0
        assert strategy_response.payload

    def test_tool_call_with_invalid_schema(self):
        """Test tool call with invalid schema validates correctly.
        
        This test validates that the inputSchema validation is active and working
        correctly by calling strategy-architect with an invalid task_description.
        """
        # Test with task_description that violates minLength=5
        with pytest.raises(ValueError, match="Strategy-architect execution failed: task_description must be at least 5 characters long"):
            strategy_architect("Hi")  # Only 2 characters, violates minLength=5
        
        # Test with task_description that violates maxLength=2000
        long_description = "A" * 2001  # Exceeds maxLength=2000
        with pytest.raises(ValueError, match="Strategy-architect execution failed: task_description must be at most 2000 characters long"):
            strategy_architect(long_description)

    def test_server_tools_schema_validation(self):
        """Test that registered tools have valid schemas."""
        tools = asyncio.run(mcp_app.list_tools())
        
        assert len(tools) == 1
        strategy_tool = tools[0]
        
        schema = strategy_tool.inputSchema
        assert "type" in schema
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "required" in schema
        
        # Validate strategy-architect specific schema
        props = schema["properties"]
        assert "task_description" in props
        assert props["task_description"]["type"] == "string"
        assert "task_description" in schema["required"]
        
        # Check min/max length constraints
        task_desc_schema = props["task_description"]
        assert task_desc_schema.get("minLength") == 5
        assert task_desc_schema.get("maxLength") == 2000

    def test_strategy_architect_workflow_continuation(self):
        """Test strategy-architect supports workflow continuation."""
        # First call to get analysis
        first_result = strategy_architect("Build an e-commerce platform")
        first_parsed = json.loads(first_result)
        
        # Extract analysis result for continuation
        analysis_result = first_parsed.get("payload", {}).get("analysis_result")
        
        if analysis_result:
            # Continue with decomposition stage
            second_result = strategy_architect(
                task_description="Build an e-commerce platform",
                analysis_result=analysis_result,
                workflow_stage="decomposition"
            )
            
            second_parsed = json.loads(second_result)
            assert "user_facing" in second_parsed
            assert "payload" in second_parsed

    def test_strategy_architect_error_handling(self):
        """Test strategy-architect handles errors gracefully."""
        # Test with empty string (should fail validation)
        with pytest.raises(ValueError):
            strategy_architect("")
        
        # Test with invalid workflow_stage
        with pytest.raises(ValueError):
            strategy_architect("Valid task", workflow_stage="invalid_stage")


class TestServerErrorHandling:
    """Test server error handling."""
    
    def test_strategy_architect_internal_error_handling(self):
        """Test internal error handling in strategy-architect."""
        # Mock the internal workflow to raise an exception
        with patch('tools.architect_unified.execute_architect_workflow') as mock_workflow:
            mock_workflow.side_effect = Exception("Internal workflow error")
            
            with pytest.raises(ValueError, match="Strategy-architect execution failed"):
                strategy_architect("Test task description")

    def test_mcp_app_configuration(self):
        """Test MCP app is properly configured."""
        assert mcp_app.name == "cortex-mcp"
        
        # Test that the app has the strategy-architect tool registered
        tools = asyncio.run(mcp_app.list_tools())
        assert len(tools) == 1
        assert tools[0].name == "strategy-architect"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])