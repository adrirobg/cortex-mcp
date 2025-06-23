"""Base Tool Class for Strategy Library MCP Server.

This module implements the base class that ALL tools must inherit from.
Following Principio Rector #1: Dogmatismo con Universal Response Schema.
Every tool MUST return a valid StrategyResponse without exception.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, TypeVar
from pydantic import ValidationError
import logging

from schemas.universal_response import (
    StrategyResponse,
    Strategy,
    StrategyType,
    ExecutionType,
    UserFacing,
    ClaudeInstructions,
    Action,
    Metadata,
    BasePayload
)

logger = logging.getLogger(__name__)

# Generic type for tool-specific payloads
PayloadType = TypeVar('PayloadType', bound=BasePayload)


class BaseTool(ABC, Generic[PayloadType]):
    """Base class for all Strategy Library MCP tools.
    
    Following Principio Rector #1: Dogmatismo con Universal Response Schema.
    This class enforces that ALL tools return valid StrategyResponse objects.
    
    Following Principio Rector #3: Estado en Claude, NO en Servidor.
    Tools are stateless and receive all context via parameters.
    """
    
    def __init__(self, tool_name: str, tool_version: str = "1.0.0"):
        """Initialize base tool.
        
        Args:
            tool_name: Unique identifier for the tool
            tool_version: Semantic version of the tool
        """
        self.tool_name = tool_name
        self.tool_version = tool_version
        logger.info(f"Initialized tool: {tool_name} v{tool_version}")
    
    @abstractmethod
    async def execute(self, **kwargs) -> StrategyResponse[PayloadType]:
        """Execute the tool with given parameters.
        
        This method MUST be implemented by all subclasses and MUST return
        a valid StrategyResponse object. No exceptions allowed.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            StrategyResponse[PayloadType]: Valid response following Universal Schema
            
        Raises:
            ValidationError: If the response doesn't validate against schema
        """
        pass
    
    @abstractmethod
    def get_strategy_type(self) -> StrategyType:
        """Get the strategy type for this tool.
        
        Returns:
            StrategyType: The type of strategy this tool implements
        """
        pass
    
    async def validate_and_execute(self, **kwargs) -> Dict[str, Any]:
        """Validate input and execute tool, ensuring valid StrategyResponse.
        
        This is the main entry point that guarantees schema compliance.
        Following Principio Rector #1: Sin excepciones en formato de respuesta.
        
        Args:
            **kwargs: Tool parameters
            
        Returns:
            Dict[str, Any]: Serialized StrategyResponse
            
        Raises:
            ValidationError: If response validation fails
            Exception: If tool execution fails
        """
        try:
            # Execute the tool
            logger.info(f"Executing tool: {self.tool_name}")
            response = await self.execute(**kwargs)
            
            # Validate response is a StrategyResponse
            if not isinstance(response, StrategyResponse):
                raise ValidationError(
                    f"Tool {self.tool_name} must return StrategyResponse, got {type(response)}"
                )
            
            # Validate response follows schema by checking it's already valid
            # (since it was created by Pydantic, it should be valid)
            
            logger.info(f"Tool {self.tool_name} executed successfully")
            return response.model_dump()
            
        except ValidationError as e:
            logger.error(f"Schema validation failed for tool {self.tool_name}: {e}")
            # Return error as valid StrategyResponse
            return self._create_error_response(str(e), "validation_error").model_dump()
            
        except Exception as e:
            logger.error(f"Tool execution failed for {self.tool_name}: {e}")
            # Return error as valid StrategyResponse
            return self._create_error_response(str(e), "execution_error").model_dump()
    
    def _create_error_response(self, error_message: str, error_type: str) -> StrategyResponse[BasePayload]:
        """Create a valid StrategyResponse for error cases.
        
        Following Principio Rector #1: Even errors must follow Universal Response Schema.
        
        Args:
            error_message: Description of the error
            error_type: Type of error that occurred
            
        Returns:
            StrategyResponse[BasePayload]: Valid error response
        """
        return StrategyResponse(
            strategy=Strategy(
                name=f"{self.tool_name}-error",
                version=self.tool_version,
                type=StrategyType.ANALYSIS
            ),
            user_facing=UserFacing(
                summary=f"Error executing {self.tool_name}: {error_message}",
                key_points=[
                    f"Tool: {self.tool_name}",
                    f"Error type: {error_type}",
                    "Please check input parameters and try again"
                ],
                next_steps=[
                    "Review the error message",
                    "Check input parameters",
                    "Retry with corrected input"
                ]
            ),
            claude_instructions=ClaudeInstructions(
                execution_type=ExecutionType.USER_CONFIRMATION,
                actions=[
                    Action(
                        type="handle_error",
                        description=f"Handle {error_type} in {self.tool_name}",
                        priority=1,
                        validation_criteria="Error resolved and tool retried",
                        parameters={"error_type": error_type, "error_message": error_message}
                    )
                ]
            ),
            payload=BasePayload(
                workflow_stage="error",
                suggested_next_state={
                    "error_occurred": True,
                    "error_type": error_type,
                    "tool_name": self.tool_name,
                    "retry_suggested": True
                }
            ),
            metadata=Metadata(
                confidence_score=0.0,
                complexity_score=1,
                estimated_duration="immediate",
                performance_hints=[
                    "Check tool input parameters",
                    "Verify required fields are provided"
                ],
                learning_opportunities=[
                    "Error handling validation",
                    "Tool input parameter validation"
                ]
            )
        )
    
    def create_success_response(
        self,
        summary: str,
        payload: PayloadType,
        execution_type: ExecutionType = ExecutionType.IMMEDIATE,
        actions: list[Action] = None,
        confidence_score: float = 0.9,
        complexity_score: int = 5,
        **kwargs
    ) -> StrategyResponse[PayloadType]:
        """Helper method to create successful StrategyResponse.
        
        Following Principio Rector #1: Enforce consistent response structure.
        
        Args:
            summary: Human-readable summary of results
            payload: Tool-specific payload data
            execution_type: Type of execution for Claude
            actions: List of actions for Claude to execute
            confidence_score: Confidence in the results (0-1)
            complexity_score: Complexity of the task (1-10)
            **kwargs: Additional fields for user_facing, metadata, etc.
            
        Returns:
            StrategyResponse[PayloadType]: Valid success response
        """
        if actions is None:
            actions = [
                Action(
                    type="process_results",
                    description=f"Process results from {self.tool_name}",
                    priority=1,
                    validation_criteria="Results processed successfully"
                )
            ]
        
        return StrategyResponse(
            strategy=Strategy(
                name=self.tool_name,
                version=self.tool_version,
                type=self.get_strategy_type()
            ),
            user_facing=UserFacing(
                summary=summary,
                key_points=kwargs.get('key_points', []),
                next_steps=kwargs.get('next_steps', []),
                visualization=kwargs.get('visualization')
            ),
            claude_instructions=ClaudeInstructions(
                execution_type=execution_type,
                actions=actions,
                context_requirements=kwargs.get('context_requirements'),
                decision_points=kwargs.get('decision_points'),
                fallback_strategy=kwargs.get('fallback_strategy')
            ),
            payload=payload,
            metadata=Metadata(
                confidence_score=confidence_score,
                complexity_score=complexity_score,
                estimated_duration=kwargs.get('estimated_duration'),
                performance_hints=kwargs.get('performance_hints', []),
                learning_opportunities=kwargs.get('learning_opportunities', [])
            ),
            error_handling=kwargs.get('error_handling')
        )


class MockTool(BaseTool[BasePayload]):
    """Mock tool implementation for testing base tool functionality.
    
    This validates that the base tool class works correctly and enforces
    the Universal Response Schema.
    """
    
    def __init__(self):
        """Initialize mock tool."""
        super().__init__("mock-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        """Get strategy type for mock tool."""
        return StrategyType.ANALYSIS
    
    async def execute(self, **kwargs) -> StrategyResponse[BasePayload]:
        """Execute mock tool.
        
        Args:
            test_input: Test input parameter
            should_fail: Whether to simulate failure
            
        Returns:
            StrategyResponse[BasePayload]: Mock response
        """
        test_input = kwargs.get('test_input', 'default')
        should_fail = kwargs.get('should_fail', False)
        
        if should_fail:
            raise ValueError("Mock tool failure simulation")
        
        payload = BasePayload(
            workflow_stage="complete",
            suggested_next_state={
                "mock_executed": True,
                "test_input": test_input,
                "result": "success"
            }
        )
        
        return self.create_success_response(
            summary=f"Mock tool executed successfully with input: {test_input}",
            payload=payload,
            key_points=[
                "Mock tool validation successful",
                "Base tool class working correctly",
                "Universal Response Schema enforced"
            ],
            next_steps=[
                "Proceed with actual tool implementation",
                "Validate against real use cases"
            ],
            confidence_score=0.95,
            complexity_score=1,
            estimated_duration="immediate",
            performance_hints=[
                "Mock tool demonstrates proper schema compliance"
            ],
            learning_opportunities=[
                "Base tool class validation",
                "Universal Response Schema enforcement"
            ]
        )