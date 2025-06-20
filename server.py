#!/usr/bin/env python3
"""Strategy Library MCP Server.

A Model Context Protocol server providing strategic cognition capabilities
for Claude Code. Implements JSON-RPC 2.0 over stdio transport.

Following the 4 Principios Rectores:
1. Dogmatismo con Universal Response Schema
2. Servidor como Ejecutor Fiable
3. Estado en Claude, NO en Servidor  
4. Testing Concurrente
"""

import json
import sys
import logging
from typing import Any, Dict, List, Optional
from schemas.universal_response import StrategyResponse, BasePayload

# Configure logging
logger = logging.getLogger(__name__)


class MCPServer:
    """Strategy Library MCP Server implementation.
    
    Stateless JSON-RPC 2.0 server over stdio transport.
    Following Principio Rector #3: Servidor 100% stateless.
    """
    
    def __init__(self):
        """Initialize MCP server."""
        self.tools: Dict[str, Any] = {}
        self._register_tools()
    
    def _register_tools(self):
        """Register available MCP tools.
        
        Following Principio Rector #2: Heurísticas deterministas.
        """
        self.tools = {
            "strategy-architect": {
                "name": "strategy-architect",
                "description": "Strategic planning and architecture tool that transforms project ideas into structured plans",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "task_description": {
                            "type": "string",
                            "description": "Description of the project or task to analyze and plan"
                        },
                        "analysis_result": {
                            "type": "object",
                            "description": "Previous analysis result (for workflow continuation)",
                            "default": None
                        },
                        "decomposition_result": {
                            "type": "object", 
                            "description": "Previous decomposition result (for workflow continuation)",
                            "default": None
                        },
                        "workflow_stage": {
                            "type": "string",
                            "enum": ["analysis", "decomposition", "task_graph", "mission_map", "complete"],
                            "description": "Current workflow stage (for continuation)",
                            "default": None
                        }
                    },
                    "required": ["task_description"]
                }
            }
        }
    
    def handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP initialize request."""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "strategy-library-mcp",
                "version": "0.1.0"
            }
        }
    
    def handle_tools_list(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/list request.
        
        This is the validation criteria for Fase 1.3.
        """
        tools_list = []
        for tool_name, tool_info in self.tools.items():
            tools_list.append({
                "name": tool_info["name"],
                "description": tool_info["description"],
                "inputSchema": tool_info["inputSchema"]
            })
        
        return {
            "tools": tools_list
        }
    
    def handle_tools_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request.
        
        Following Principio Rector #1: All tools must return StrategyResponse.
        """
        tool_name = params.get("name")
        if not tool_name:
            raise ValueError("Missing required field: name")
        
        arguments = params.get("arguments")
        if arguments is None:
            raise ValueError("Missing required field: arguments")
        
        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        # For now, return a mock response that validates StrategyResponse schema
        # This will be replaced with actual tool implementation in next phase
        if tool_name == "strategy-architect":
            return self._mock_strategy_architect_response(arguments)
        
        raise ValueError(f"Tool {tool_name} not yet implemented")
    
    def _mock_strategy_architect_response(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Mock strategy-architect response for server validation.
        
        Following Principio Rector #1: Must return valid StrategyResponse.
        This is a temporary implementation for server testing.
        """
        task_description = arguments.get("task_description", "")
        
        # Create a valid StrategyResponse following Universal Response Schema
        mock_response = StrategyResponse[BasePayload](
            strategy={
                "name": "mock-strategy-architect",
                "version": "0.1.0",
                "type": "analysis"
            },
            user_facing={
                "summary": f"Mock analysis of: {task_description[:50]}...",
                "key_points": [
                    "Server is responding correctly",
                    "StrategyResponse schema validation working",
                    "Ready for actual tool implementation"
                ],
                "next_steps": [
                    "Implement actual strategy-architect logic",
                    "Add internal workflow functions"
                ]
            },
            claude_instructions={
                "execution_type": "immediate",
                "actions": [
                    {
                        "type": "mock_analysis",
                        "description": "Mock analysis action for server validation",
                        "priority": 1,
                        "validation_criteria": "Server responds with valid StrategyResponse"
                    }
                ]
            },
            payload=BasePayload(
                workflow_stage="analysis",
                suggested_next_state={
                    "continue_workflow": False,
                    "next_step": "implement_actual_tool",
                    "context_to_maintain": {
                        "server_validation": "successful",
                        "schema_compliance": "verified"
                    }
                }
            ),
            metadata={
                "confidence_score": 0.95,
                "complexity_score": 1,
                "estimated_duration": "immediate",
                "performance_hints": [
                    "Server is functioning correctly",
                    "Schema validation working"
                ],
                "learning_opportunities": [
                    "Server implementation validated",
                    "Ready for tool development"
                ]
            }
        )
        
        # Return as dict for JSON-RPC response
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(mock_response.model_dump(), indent=2)
                }
            ]
        }
    
    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Handle incoming JSON-RPC request.
        
        Following JSON-RPC 2.0 specification.
        """
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            if method == "initialize":
                result = self.handle_initialize(params)
            elif method == "tools/list":
                result = self.handle_tools_list(params)
            elif method == "tools/call":
                result = self.handle_tools_call(params)
            else:
                raise ValueError(f"Unknown method: {method}")
            
            # Return JSON-RPC 2.0 response
            if request_id is not None:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": result
                }
            
            # Notification (no response required)
            return None
            
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            if request.get("id") is not None:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32603,
                        "message": "Internal error",
                        "data": str(e)
                    }
                }
            return None
    
    def run(self):
        """Run the MCP server with stdio transport.
        
        Following MCP stdio transport specification.
        """
        logger.info("Starting Strategy Library MCP Server")
        
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                
                try:
                    request = json.loads(line)
                    response = self.handle_request(request)
                    
                    if response:
                        print(json.dumps(response), flush=True)
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Invalid JSON received: {e}")
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    print(json.dumps(error_response), flush=True)
                    
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")
            raise


def main():
    """Main entry point for the MCP server."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stderr)]  # Log to stderr to avoid stdio interference
    )
    
    server = MCPServer()
    server.run()


if __name__ == "__main__":
    main()