"""Tests for MCP Server implementation.

Following Principio Rector #2: Servidor como Ejecutor Fiable.
Tests validate JSON-RPC 2.0 compliance and tools/list response.
"""

import json
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

from server import MCPServer
from schemas.universal_response import StrategyResponse, BasePayload


class TestMCPServer:
    """Test MCP Server core functionality."""
    
    def test_server_initialization(self):
        """Test server initializes correctly."""
        server = MCPServer()
        assert "strategy-architect" in server.tools
        assert server.tools["strategy-architect"]["name"] == "strategy-architect"
        assert "description" in server.tools["strategy-architect"]
        assert "inputSchema" in server.tools["strategy-architect"]
    
    def test_handle_initialize(self):
        """Test initialize request handling."""
        server = MCPServer()
        response = server.handle_initialize({})
        
        assert "protocolVersion" in response
        assert response["protocolVersion"] == "2024-11-05"
        assert "capabilities" in response
        assert "serverInfo" in response
        assert response["serverInfo"]["name"] == "strategy-library-mcp"
        assert response["serverInfo"]["version"] == "0.1.0"
    
    def test_handle_tools_list(self):
        """Test tools/list request handling.
        
        This is the CRITICAL validation criteria: 'Servidor responde a tools/list'
        """
        server = MCPServer()
        response = server.handle_tools_list({})
        
        assert "tools" in response
        assert len(response["tools"]) == 1
        
        tool = response["tools"][0]
        assert tool["name"] == "strategy-architect"
        assert "description" in tool
        assert "inputSchema" in tool
        
        # Validate schema structure
        schema = tool["inputSchema"]
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "task_description" in schema["properties"]
        assert "required" in schema
        assert "task_description" in schema["required"]
    
    def test_handle_tools_call_unknown_tool(self):
        """Test tools/call with unknown tool."""
        server = MCPServer()
        
        with pytest.raises(ValueError, match="Unknown tool"):
            server.handle_tools_call({
                "name": "nonexistent-tool",
                "arguments": {}
            })
    
    def test_handle_tools_call_strategy_architect(self):
        """Test tools/call with strategy-architect tool."""
        server = MCPServer()
        
        response = server.handle_tools_call({
            "name": "strategy-architect",
            "arguments": {
                "task_description": "Test project description"
            }
        })
        
        assert "content" in response
        assert len(response["content"]) == 1
        assert response["content"][0]["type"] == "text"
        
        # Parse the response text as JSON to validate StrategyResponse
        response_data = json.loads(response["content"][0]["text"])
        
        # Validate it's a proper StrategyResponse
        strategy_response = StrategyResponse[BasePayload](**response_data)
        assert strategy_response.strategy.name == "mock-strategy-architect"
        assert strategy_response.strategy.type == "analysis"
        assert "Mock analysis of: Test project description" in strategy_response.user_facing.summary
        assert strategy_response.metadata.confidence_score == 0.95
        assert strategy_response.payload.workflow_stage == "analysis"
    
    def test_handle_request_initialize(self):
        """Test JSON-RPC request handling for initialize."""
        server = MCPServer()
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        
        response = server.handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 1
        assert "result" in response
        assert response["result"]["serverInfo"]["name"] == "strategy-library-mcp"
    
    def test_handle_request_tools_list(self):
        """Test JSON-RPC request handling for tools/list.
        
        CRITICAL TEST: This validates the Fase 1.3 success criteria.
        """
        server = MCPServer()
        
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        response = server.handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 2
        assert "result" in response
        assert "tools" in response["result"]
        assert len(response["result"]["tools"]) == 1
        assert response["result"]["tools"][0]["name"] == "strategy-architect"
    
    def test_handle_request_tools_call(self):
        """Test JSON-RPC request handling for tools/call."""
        server = MCPServer()
        
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "strategy-architect",
                "arguments": {
                    "task_description": "Build a web application"
                }
            }
        }
        
        response = server.handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 3
        assert "result" in response
        assert "content" in response["result"]
    
    def test_handle_request_unknown_method(self):
        """Test JSON-RPC error handling for unknown method."""
        server = MCPServer()
        
        request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "unknown/method",
            "params": {}
        }
        
        response = server.handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 4
        assert "error" in response
        assert response["error"]["code"] == -32603
        assert response["error"]["message"] == "Internal error"
    
    def test_handle_request_notification(self):
        """Test JSON-RPC notification (no id, no response)."""
        server = MCPServer()
        
        request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {}
            # No "id" field = notification
        }
        
        response = server.handle_request(request)
        
        # Notifications should not return a response
        assert response is None
    
    def test_mock_strategy_architect_response_validation(self):
        """Test that mock response validates against StrategyResponse schema."""
        server = MCPServer()
        
        arguments = {
            "task_description": "Create a REST API for user management"
        }
        
        response = server._mock_strategy_architect_response(arguments)
        
        # Extract and validate the StrategyResponse
        response_text = response["content"][0]["text"]
        response_data = json.loads(response_text)
        
        # This should not raise ValidationError
        strategy_response = StrategyResponse[BasePayload](**response_data)
        
        # Validate specific fields
        assert strategy_response.strategy.name == "mock-strategy-architect"
        assert strategy_response.user_facing.summary.startswith("Mock analysis of: Create a REST API")
        assert len(strategy_response.claude_instructions.actions) == 1
        assert strategy_response.metadata.confidence_score == 0.95
        assert strategy_response.payload.suggested_next_state is not None
    
    def test_server_tools_schema_validation(self):
        """Test that registered tools have valid schemas."""
        server = MCPServer()
        
        for tool_name, tool_info in server.tools.items():
            assert "name" in tool_info
            assert "description" in tool_info
            assert "inputSchema" in tool_info
            
            schema = tool_info["inputSchema"]
            assert "type" in schema
            assert schema["type"] == "object"
            assert "properties" in schema
            assert "required" in schema
            
            # Validate strategy-architect specific schema
            if tool_name == "strategy-architect":
                props = schema["properties"]
                assert "task_description" in props
                assert props["task_description"]["type"] == "string"
                assert "task_description" in schema["required"]
                
                # Optional fields should have defaults
                optional_fields = ["analysis_result", "decomposition_result", "workflow_stage"]
                for field in optional_fields:
                    if field in props:
                        assert "default" in props[field]


class TestServerErrorHandling:
    """Test server error handling."""
    
    def test_handle_request_exception(self):
        """Test exception handling in request processing."""
        server = MCPServer()
        
        request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "strategy-architect"
                # Missing required "arguments" field
            }
        }
        
        response = server.handle_request(request)
        
        assert response["jsonrpc"] == "2.0"
        assert response["id"] == 5
        assert "error" in response
        assert response["error"]["code"] == -32603


if __name__ == "__main__":
    pytest.main([__file__, "-v"])