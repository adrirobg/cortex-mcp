"""Tests for Universal Response Schema.

Following Principio Rector #1: Dogmatismo con Universal Response Schema.
All tests ensure strict Pydantic validation of the core StrategyResponse.
"""

import pytest
from typing import Dict, Any
from pydantic import ValidationError

from schemas.universal_response import (
    StrategyResponse,
    Strategy,
    StrategyType,
    ExecutionType,
    UserFacing,
    ClaudeInstructions,
    Action,
    Metadata,
    BasePayload,
    DecisionPoint,
    ContextRequirements,
    ErrorHandling,
    ErrorScenario,
    RecoveryStrategy
)


class TestStrategy:
    """Test Strategy schema validation."""
    
    def test_valid_strategy(self):
        """Test valid strategy creation."""
        strategy = Strategy(
            name="test-strategy",
            version="1.0.0",
            type=StrategyType.ANALYSIS
        )
        assert strategy.name == "test-strategy"
        assert strategy.version == "1.0.0"
        assert strategy.type == StrategyType.ANALYSIS
    
    def test_strategy_validation_errors(self):
        """Test strategy validation errors."""
        with pytest.raises(ValidationError):
            Strategy(name="", version="1.0.0", type=StrategyType.ANALYSIS)
        
        with pytest.raises(ValidationError):
            Strategy(name="test", version="", type=StrategyType.ANALYSIS)


class TestAction:
    """Test Action schema validation."""
    
    def test_valid_action(self):
        """Test valid action creation."""
        action = Action(
            type="create_file",
            description="Create a new file",
            priority=1,
            validation_criteria="File exists and is valid"
        )
        assert action.type == "create_file"
        assert action.priority == 1
        assert action.validation_criteria == "File exists and is valid"
    
    def test_action_priority_validation(self):
        """Test action priority bounds."""
        with pytest.raises(ValidationError):
            Action(type="test", description="test", priority=0)
        
        with pytest.raises(ValidationError):
            Action(type="test", description="test", priority=11)
        
        # Valid priorities
        Action(type="test", description="test", priority=1)
        Action(type="test", description="test", priority=10)


class TestDecisionPoint:
    """Test DecisionPoint schema validation."""
    
    def test_valid_decision_point(self):
        """Test valid decision point creation."""
        dp = DecisionPoint(
            id="dp_1",
            question="Which approach to use?",
            options=[
                {"id": "option1", "description": "First option"},
                {"id": "option2", "description": "Second option"}
            ],
            recommendation="option1",
            confidence=0.8
        )
        assert dp.id == "dp_1"
        assert dp.confidence == 0.8
        assert len(dp.options) == 2
    
    def test_confidence_bounds(self):
        """Test confidence score validation."""
        with pytest.raises(ValidationError):
            DecisionPoint(
                id="dp_1",
                question="Test?",
                options=[],
                confidence=-0.1
            )
        
        with pytest.raises(ValidationError):
            DecisionPoint(
                id="dp_1",
                question="Test?",
                options=[],
                confidence=1.1
            )


class TestMetadata:
    """Test Metadata schema validation."""
    
    def test_valid_metadata(self):
        """Test valid metadata creation."""
        metadata = Metadata(
            confidence_score=0.9,
            complexity_score=5,
            estimated_duration="2 hours",
            performance_hints=["Use caching"],
            learning_opportunities=["Pattern recognition"]
        )
        assert metadata.confidence_score == 0.9
        assert metadata.complexity_score == 5
        assert metadata.estimated_duration == "2 hours"
    
    def test_metadata_bounds(self):
        """Test metadata validation bounds."""
        with pytest.raises(ValidationError):
            Metadata(confidence_score=-0.1, complexity_score=5)
        
        with pytest.raises(ValidationError):
            Metadata(confidence_score=1.1, complexity_score=5)
        
        with pytest.raises(ValidationError):
            Metadata(confidence_score=0.9, complexity_score=0)
        
        with pytest.raises(ValidationError):
            Metadata(confidence_score=0.9, complexity_score=11)


class TestStrategyResponse:
    """Test complete StrategyResponse schema validation."""
    
    def create_valid_strategy_response(self) -> Dict[str, Any]:
        """Helper to create valid strategy response data."""
        return {
            "strategy": {
                "name": "test-strategy",
                "version": "1.0.0",
                "type": "analysis"
            },
            "user_facing": {
                "summary": "Test strategy executed successfully",
                "key_points": ["Point 1", "Point 2"],
                "next_steps": ["Step 1", "Step 2"]
            },
            "claude_instructions": {
                "execution_type": "immediate",
                "actions": [
                    {
                        "type": "analyze",
                        "description": "Analyze the input",
                        "priority": 1,
                        "validation_criteria": "Analysis complete"
                    }
                ]
            },
            "payload": {
                "workflow_stage": "analysis",
                "result": "Analysis completed successfully"
            },
            "metadata": {
                "confidence_score": 0.9,
                "complexity_score": 5,
                "estimated_duration": "1 hour"
            }
        }
    
    def test_valid_strategy_response(self):
        """Test valid complete strategy response."""
        data = self.create_valid_strategy_response()
        response = StrategyResponse[BasePayload](**data)
        
        assert response.strategy.name == "test-strategy"
        assert response.user_facing.summary == "Test strategy executed successfully"
        assert response.claude_instructions.execution_type == ExecutionType.IMMEDIATE
        assert len(response.claude_instructions.actions) == 1
        assert response.metadata.confidence_score == 0.9
        assert response.payload.workflow_stage == "analysis"
    
    def test_strategy_response_validation_errors(self):
        """Test strategy response validation errors."""
        data = self.create_valid_strategy_response()
        
        # Missing required field
        del data["strategy"]
        with pytest.raises(ValidationError):
            StrategyResponse[BasePayload](**data)
        
        # Invalid execution type
        data = self.create_valid_strategy_response()
        data["claude_instructions"]["execution_type"] = "invalid_type"
        with pytest.raises(ValidationError):
            StrategyResponse[BasePayload](**data)
        
        # Invalid confidence score
        data = self.create_valid_strategy_response()
        data["metadata"]["confidence_score"] = 1.5
        with pytest.raises(ValidationError):
            StrategyResponse[BasePayload](**data)
    
    def test_strategy_response_extra_fields_forbidden(self):
        """Test that extra fields are forbidden."""
        data = self.create_valid_strategy_response()
        data["extra_field"] = "not allowed"
        
        with pytest.raises(ValidationError):
            StrategyResponse[BasePayload](**data)
    
    def test_strategy_response_with_decision_points(self):
        """Test strategy response with decision points."""
        data = self.create_valid_strategy_response()
        data["claude_instructions"]["decision_points"] = [
            {
                "id": "dp_1",
                "question": "Which approach?",
                "options": [{"id": "opt1", "desc": "Option 1"}],
                "confidence": 0.7
            }
        ]
        
        response = StrategyResponse[BasePayload](**data)
        assert len(response.claude_instructions.decision_points) == 1
        assert response.claude_instructions.decision_points[0].id == "dp_1"
    
    def test_strategy_response_with_error_handling(self):
        """Test strategy response with error handling."""
        data = self.create_valid_strategy_response()
        data["error_handling"] = {
            "potential_errors": [
                {
                    "type": "validation_error",
                    "description": "Input validation failed",
                    "probability": 0.1
                }
            ],
            "recovery_strategies": [
                {
                    "trigger": "validation_error",
                    "action": "retry_with_cleaned_input",
                    "fallback": "manual_review"
                }
            ]
        }
        
        response = StrategyResponse[BasePayload](**data)
        assert response.error_handling is not None
        assert len(response.error_handling.potential_errors) == 1
        assert len(response.error_handling.recovery_strategies) == 1


class TestErrorHandling:
    """Test error handling schemas."""
    
    def test_error_scenario_validation(self):
        """Test error scenario validation."""
        error = ErrorScenario(
            type="network_error",
            description="Network connection failed",
            probability=0.05
        )
        assert error.type == "network_error"
        assert error.probability == 0.05
        
        with pytest.raises(ValidationError):
            ErrorScenario(
                type="test",
                description="test",
                probability=1.5
            )
    
    def test_recovery_strategy_validation(self):
        """Test recovery strategy validation."""
        recovery = RecoveryStrategy(
            trigger="network_error",
            action="retry_connection",
            fallback="use_cached_data"
        )
        assert recovery.trigger == "network_error"
        assert recovery.action == "retry_connection"
        assert recovery.fallback == "use_cached_data"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])