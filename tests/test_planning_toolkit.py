"""Tests for Planning Toolkit Tools.

Tests the async planning tools: PlanningTemplateTool and PlanningArtifactTool.
"""

import pytest
import os
import tempfile
import shutil
from tools.planning_toolkit import PlanningTemplateTool, PlanningArtifactTool
from schemas.universal_response import StrategyResponse
from schemas.planning_payloads import PlanningTemplatePayload, PlanningArtifactPayload


@pytest.mark.asyncio
class TestPlanningTemplateTool:
    """Test PlanningTemplateTool async functionality."""
    
    async def test_template_tool_initialization(self):
        """Test planning template tool initialization."""
        tool = PlanningTemplateTool()
        assert tool.tool_name == "planning-template-tool"
        assert tool.tool_version == "1.0.0"
    
    async def test_nonexistent_template_handling(self):
        """Test handling of nonexistent template."""
        tool = PlanningTemplateTool()
        
        result = await tool.validate_and_execute(template_name="nonexistent_template")
        
        assert isinstance(result, dict)
        assert "strategy" in result
        assert "Planning template 'nonexistent_template' not found" in result["user_facing"]["summary"]


@pytest.mark.asyncio
class TestPlanningArtifactTool:
    """Test PlanningArtifactTool async functionality."""
    
    async def test_artifact_tool_initialization(self):
        """Test planning artifact tool initialization."""
        tool = PlanningArtifactTool()
        assert tool.tool_name == "planning-artifact-tool"
        assert tool.tool_version == "1.0.0"
    
    async def test_artifact_save_success(self):
        """Test successful artifact saving."""
        tool = PlanningArtifactTool()
        
        # Use temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            test_content = "Test planning artifact content"
            test_filename = "test_artifact.md"
            
            result = await tool.validate_and_execute(
                file_name=test_filename,
                file_content=test_content,
                directory=temp_dir
            )
            
            assert isinstance(result, dict)
            assert "strategy" in result
            assert "Planning artifact 'test_artifact.md' saved successfully" in result["user_facing"]["summary"]
            
            # Verify file was actually created
            file_path = os.path.join(temp_dir, test_filename)
            assert os.path.exists(file_path)
            
            # Verify content
            with open(file_path, 'r', encoding='utf-8') as f:
                saved_content = f.read()
            assert saved_content == test_content