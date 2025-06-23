"""Tests for Knowledge Management Tools.

Tests the async knowledge tools: RetrospectiveTool and KnowledgeIntegrationTool.
"""

import pytest
import os
import tempfile
import json
from tools.knowledge_management import RetrospectiveTool, KnowledgeIntegrationTool


@pytest.mark.asyncio
class TestRetrospectiveTool:
    """Test RetrospectiveTool async functionality."""
    
    async def test_retrospective_tool_initialization(self):
        """Test retrospective tool initialization."""
        tool = RetrospectiveTool()
        assert tool.tool_name == "retrospective-tool"
        assert tool.tool_version == "1.0.0"
    
    async def test_retrospective_creation_success(self):
        """Test successful retrospective creation."""
        tool = RetrospectiveTool()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create .cortex/retrospectives directory structure
            retrospectives_dir = os.path.join(temp_dir, ".cortex", "retrospectives")
            os.makedirs(retrospectives_dir, exist_ok=True)
            
            # Change to temp directory for the test
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                result = await tool.validate_and_execute(
                    task_name="Test Task",
                    phase_context="Test Phase",
                    duration_estimate="1 hour"
                )
                
                assert isinstance(result, dict)
                assert "strategy" in result
                assert "Retrospective draft created for 'Test Task'" in result["user_facing"]["summary"]
                
                # Verify file was created
                files_in_retro_dir = os.listdir(retrospectives_dir)
                assert len(files_in_retro_dir) == 1
                
                retro_file = files_in_retro_dir[0]
                assert retro_file.endswith("_test_task.md")
                
            finally:
                os.chdir(original_cwd)
    
    async def test_invalid_task_name(self):
        """Test handling of invalid task name."""
        tool = RetrospectiveTool()
        
        result = await tool.validate_and_execute(task_name="x")  # Too short
        
        assert isinstance(result, dict)
        assert "Error creating retrospective" in result["user_facing"]["summary"]


@pytest.mark.asyncio
class TestKnowledgeIntegrationTool:
    """Test KnowledgeIntegrationTool async functionality."""
    
    async def test_knowledge_integration_tool_initialization(self):
        """Test knowledge integration tool initialization."""
        tool = KnowledgeIntegrationTool()
        assert tool.tool_name == "knowledge-integration-tool"
        assert tool.tool_version == "1.0.0"
    
    async def test_nonexistent_file_handling(self):
        """Test handling of nonexistent retrospective file."""
        tool = KnowledgeIntegrationTool()
        
        result = await tool.validate_and_execute(retrospective_file="/nonexistent/file.md")
        
        assert isinstance(result, dict)
        assert "Error integrating knowledge" in result["user_facing"]["summary"]