"""Integration tests for Strategy Library MCP Server.

Following the simulated strategy-architect workflow and validating all 4 Principios Rectores:
1. Dogmatismo con Universal Response Schema
2. Servidor como Ejecutor Fiable  
3. Estado en Claude, NO en Servidor
4. Testing Concurrente

These tests validate the complete system integration as specified in the
implementationPlan.md learning opportunities.
"""

import json
import pytest
import asyncio
import subprocess
import sys
from typing import Dict, Any
from unittest.mock import patch

from server import app as mcp_app, strategy_architect
from tools.base_tool import MockTool
from schemas.universal_response import StrategyResponse, BasePayload
from schemas.architect_payloads import ArchitectPayload, WorkflowStage, AnalysisResult


class TestCompleteSystemIntegration:
    """Test complete system integration following all Principios Rectores."""
    
    def test_end_to_end_server_tool_integration(self):
        """Test complete end-to-end integration: Server → Tool → StrategyResponse.
        
        This validates the complete workflow from the simulated strategy-architect plan.
        """
        # Test tools/list returns all registered tools
        tools = asyncio.run(mcp_app.list_tools())
        assert len(tools) == 3  # strategy-architect, start-retrospective, process-retrospective
        tool_names = [tool.name for tool in tools]
        assert "strategy-architect" in tool_names
        assert "start-retrospective" in tool_names  
        assert "process-retrospective" in tool_names
        
        # Test strategy-architect tool execution
        response_json = strategy_architect(
            task_description="Build a complete e-commerce platform with payment integration"
        )
        
        # Parse and validate the StrategyResponse
        response_data = json.loads(response_json)
        
        # Validate it's a proper StrategyResponse following Universal Schema with real ArchitectPayload
        strategy_response = StrategyResponse[ArchitectPayload](**response_data)
        
        # Validate Principio Rector #1: Dogmatismo con Universal Response Schema
        assert strategy_response.strategy.name == "motor-de-estrategias"
        assert strategy_response.strategy.version == "2.5.0"
        assert strategy_response.strategy.type == "analysis"
        assert strategy_response.user_facing.summary is not None
        assert len(strategy_response.user_facing.key_points) > 0
        assert len(strategy_response.claude_instructions.actions) > 0
        assert 0.0 <= strategy_response.metadata.confidence_score <= 1.0
        assert strategy_response.payload.workflow_stage == WorkflowStage.COMPLETE
        
    def test_universal_response_schema_enforcement(self):
        """Test that Universal Response Schema is enforced across all tools.
        
        Validates Principio Rector #1: Sin excepciones en formato de respuesta.
        """
        # Test with MockTool through base tool class
        mock_tool = MockTool()
        
        # Execute tool and get response
        result = mock_tool.validate_and_execute(test_input="schema_validation_test")
        
        # Validate it's serializable dict
        assert isinstance(result, dict)
        
        # Validate it reconstructs to valid StrategyResponse
        response = StrategyResponse[BasePayload](**result)
        
        # Validate all required Universal Response Schema fields
        assert response.strategy is not None
        assert response.user_facing is not None
        assert response.claude_instructions is not None
        assert response.payload is not None
        assert response.metadata is not None
        
        # Validate strategy fields
        assert response.strategy.name == "mock-tool"
        assert response.strategy.version == "1.0.0"
        assert response.strategy.type == "analysis"
        
        # Validate user_facing fields
        assert response.user_facing.summary is not None
        assert isinstance(response.user_facing.key_points, list)
        assert isinstance(response.user_facing.next_steps, list)
        
        # Validate claude_instructions fields
        assert response.claude_instructions.execution_type is not None
        assert isinstance(response.claude_instructions.actions, list)
        assert len(response.claude_instructions.actions) > 0
        
        # Validate metadata bounds
        assert 0.0 <= response.metadata.confidence_score <= 1.0
        assert 1 <= response.metadata.complexity_score <= 10
    
    def test_server_stateless_behavior(self):
        """Test that server maintains no state between calls.
        
        Validates Principio Rector #3: Servidor 100% stateless.
        """
        # Test server stateless behavior with FastMCP
        
        # First call
        response1_json = strategy_architect(
            task_description="Build a social media platform"
        )
        response1 = json.loads(response1_json)
        
        # Second call with identical input
        response2_json = strategy_architect(
            task_description="Build a social media platform"
        )
        response2 = json.loads(response2_json)
        
        # Responses should be identical (deterministic behavior)
        # excluding any timestamps or random elements
        assert response1["strategy"]["name"] == response2["strategy"]["name"]
        assert response1["strategy"]["version"] == response2["strategy"]["version"]
        assert response1["payload"]["workflow_stage"] == response2["payload"]["workflow_stage"]
        
        # Third call with different input
        response3_json = strategy_architect(
            task_description="Build an enterprise CRM system"
        )
        response3 = json.loads(response3_json)
        
        # Should produce different results for different inputs
        # (even if framework is deterministic, content should differ)
        assert response1["user_facing"]["summary"] != response3["user_facing"]["summary"]
    
    def test_comprehensive_workflow_progression(self):
        """Test complete Motor de Estrategias workflow progression.
        
        Tests Principio Rector #3: Estado en Claude, NO en Servidor.
        Validates workflow continuation via suggested_next_state.
        """
        # Start with complete workflow 
        task_desc = "Build a microservices-based inventory management system"
        
        first_response_json = strategy_architect(task_description=task_desc)
        first_response = json.loads(first_response_json)
        
        # Should contain complete workflow results
        response = StrategyResponse[ArchitectPayload](**first_response)
        assert response.payload.workflow_stage == WorkflowStage.COMPLETE
        
        # Should contain all workflow components
        assert response.payload.analysis is not None
        assert response.payload.decomposition is not None
        assert response.payload.task_graph is not None
        assert response.payload.mission_map is not None
        
        # Test workflow continuation from analysis stage
        if response.payload.analysis:
            continued_response_json = strategy_architect(
                task_description=task_desc,
                analysis_result=response.payload.analysis.model_dump(),
                workflow_stage="decomposition"
            )
            continued_response = json.loads(continued_response_json)
            
            # Should successfully continue workflow
            assert "user_facing" in continued_response
            assert "payload" in continued_response
            
    def test_server_tool_registration(self):
        """Test server tool registration and schema compliance."""
        # Validate FastMCP tool registration
        tools = asyncio.run(mcp_app.list_tools())
        assert len(tools) == 1
        
        strategy_tool = tools[0]
        assert strategy_tool.name == "strategy-architect"
        assert strategy_tool.description
        assert strategy_tool.inputSchema
        
        # Validate schema compliance
        schema = strategy_tool.inputSchema
        assert schema["type"] == "object"
        assert "properties" in schema
        assert "required" in schema
        assert "task_description" in schema["required"]
        
        # Validate property constraints
        props = schema["properties"]
        task_desc_prop = props["task_description"]
        assert task_desc_prop["type"] == "string"
        assert task_desc_prop["minLength"] == 5
        assert task_desc_prop["maxLength"] == 2000

    def test_error_handling_and_validation(self):
        """Test error handling follows Principio Rector #2: Servidor como Ejecutor Fiable."""
        # Test input validation
        with pytest.raises(ValueError, match="Strategy-architect execution failed"):
            strategy_architect("")  # Empty string
            
        with pytest.raises(ValueError, match="Strategy-architect execution failed"):
            strategy_architect("Hi")  # Too short
            
        # Test invalid workflow stage
        with pytest.raises(ValueError, match="Strategy-architect execution failed"):
            strategy_architect("Valid task description", workflow_stage="invalid_stage")

    def test_response_deterministic_structure(self):
        """Test responses maintain deterministic structure.
        
        Validates Principio Rector #2: Servidor como Ejecutor Fiable.
        """
        response_json = strategy_architect(
            task_description="Build a document management system with version control"
        )
        response_data = json.loads(response_json)
        
        # Validate response structure is always the same
        required_keys = ["strategy", "user_facing", "claude_instructions", "payload", "metadata"]
        for key in required_keys:
            assert key in response_data, f"Missing required key: {key}"
        
        # Validate strategy response parses correctly
        strategy_response = StrategyResponse[ArchitectPayload](**response_data)
        
        # Validate deterministic strategy metadata
        assert strategy_response.strategy.name == "motor-de-estrategias"
        assert strategy_response.strategy.version == "2.5.0"
        assert strategy_response.strategy.type == "analysis"
        
        # Validate payload structure
        assert hasattr(strategy_response.payload, 'workflow_stage')
        assert hasattr(strategy_response.payload, 'analysis')
        assert hasattr(strategy_response.payload, 'decomposition')
        assert hasattr(strategy_response.payload, 'task_graph')
        assert hasattr(strategy_response.payload, 'mission_map')
        
    def test_concurrent_execution_safety(self):
        """Test concurrent tool execution maintains reliability.
        
        Validates Principio Rector #4: Testing Concurrente and stateless operation.
        """
        import threading
        import time
        
        results = []
        errors = []
        
        def execute_tool(task_id):
            try:
                response_json = strategy_architect(
                    task_description=f"Build a task management system - task {task_id}"
                )
                response = json.loads(response_json)
                results.append((task_id, response))
            except Exception as e:
                errors.append((task_id, str(e)))
        
        # Execute multiple concurrent calls
        threads = []
        for i in range(3):
            thread = threading.Thread(target=execute_tool, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Validate all executions succeeded
        assert len(errors) == 0, f"Concurrent execution errors: {errors}"
        assert len(results) == 3, f"Expected 3 results, got {len(results)}"
        
        # Validate all responses are valid StrategyResponse
        for task_id, response in results:
            assert "strategy" in response
            assert "user_facing" in response
            assert "claude_instructions" in response
            assert "payload" in response
            assert "metadata" in response
            
            # Validate response parses correctly
            strategy_response = StrategyResponse[ArchitectPayload](**response)
            assert strategy_response.payload.workflow_stage == WorkflowStage.COMPLETE


class TestMotorDeEstrategiasIntegration:
    """Test Motor de Estrategias specific integration patterns."""
    
    def test_complete_motor_workflow_execution(self):
        """Test complete Motor de Estrategias workflow execution."""
        response_json = strategy_architect(
            task_description="Create a comprehensive project management platform with advanced reporting"
        )
        
        response_data = json.loads(response_json)
        strategy_response = StrategyResponse[ArchitectPayload](**response_data)
        
        # Validate Motor de Estrategias completed full workflow
        assert strategy_response.payload.workflow_stage == WorkflowStage.COMPLETE
        
        # Validate all workflow phases completed
        assert strategy_response.payload.analysis is not None
        assert strategy_response.payload.decomposition is not None
        assert strategy_response.payload.task_graph is not None
        assert strategy_response.payload.mission_map is not None
        
        # Validate analysis structure
        analysis = strategy_response.payload.analysis
        assert hasattr(analysis, 'keywords')
        assert hasattr(analysis, 'patterns')
        assert hasattr(analysis, 'complexity')
        
        # Validate decomposition structure
        decomposition = strategy_response.payload.decomposition
        assert hasattr(decomposition, 'phases')
        assert len(decomposition.phases) > 0
        
        # Validate task graph structure
        task_graph = strategy_response.payload.task_graph
        assert hasattr(task_graph, 'tasks')
        assert len(task_graph.tasks) > 0
        
        # Validate mission map structure
        mission_map = strategy_response.payload.mission_map
        assert hasattr(mission_map, 'resource_assignments')
        assert len(mission_map.resource_assignments) > 0
        
    def test_workflow_stage_progression(self):
        """Test Motor de Estrategias workflow stage progression."""
        task_desc = "Develop a machine learning pipeline for predictive analytics"
        
        # Test complete workflow
        complete_response_json = strategy_architect(task_description=task_desc)
        complete_response = json.loads(complete_response_json)
        
        # Extract analysis for continuation
        analysis_result = complete_response["payload"]["analysis"]
        
        # Test continuation from decomposition stage
        decomp_response_json = strategy_architect(
            task_description=task_desc,
            analysis_result=analysis_result,
            workflow_stage="decomposition"
        )
        decomp_response = json.loads(decomp_response_json)
        
        # Validate continuation response
        assert "user_facing" in decomp_response
        assert "payload" in decomp_response
        
        # Should contain progression guidance
        assert decomp_response["payload"]["workflow_stage"] in [
            WorkflowStage.DECOMPOSITION.value,
            WorkflowStage.TASK_GRAPH.value,
            WorkflowStage.MISSION_MAP.value,
            WorkflowStage.COMPLETE.value
        ]
        
    def test_suggested_next_state_functionality(self):
        """Test suggested_next_state workflow continuation mechanism."""
        response_json = strategy_architect(
            task_description="Build a real-time collaborative editing platform"
        )
        
        response_data = json.loads(response_json)
        
        # Should contain suggested_next_state for workflow continuation
        payload = response_data["payload"]
        
        # Validate presence of workflow continuation data
        assert "workflow_stage" in payload
        
        # For complete workflows, should have all intermediate results
        if payload["workflow_stage"] == WorkflowStage.COMPLETE.value:
            assert payload["analysis"] is not None
            assert payload["decomposition"] is not None
            assert payload["task_graph"] is not None
            assert payload["mission_map"] is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])