"""MCP-Compliant Structured Logger for CortexMCP.

Implements official MCP debugging standards:
- JSON-formatted structured logs to stderr only
- Trace ID correlation across workflow stages
- Sensitive data sanitization
- Configurable log levels with environment variable support

Per MCP docs: https://modelcontextprotocol.io/docs/tools/debugging
"""

import json
import sys
import uuid
import os
import traceback
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from enum import Enum


class LogLevel(Enum):
    """Log levels following standard Python logging conventions."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class MCPLogger:
    """MCP-compliant structured logger outputting JSON to stderr."""
    
    def __init__(self, component: str = "cortex-mcp"):
        """Initialize logger for specific component.
        
        Args:
            component: Component name for log identification
        """
        self.component = component
        self.log_level = self._get_log_level_from_env()
    
    def _get_log_level_from_env(self) -> LogLevel:
        """Get log level from STRATEGY_LOG_LEVEL environment variable."""
        env_level = os.getenv("STRATEGY_LOG_LEVEL", "INFO").upper()
        try:
            return LogLevel(env_level)
        except ValueError:
            return LogLevel.INFO
    
    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged based on current log level."""
        level_order = {
            LogLevel.DEBUG: 0,
            LogLevel.INFO: 1, 
            LogLevel.WARNING: 2,
            LogLevel.ERROR: 3
        }
        return level_order[level] >= level_order[self.log_level]
    
    def _sanitize_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize context data removing sensitive information.
        
        Args:
            context: Raw context dictionary
            
        Returns:
            Sanitized context dictionary
        """
        if not context:
            return {}
            
        sanitized = {}
        
        for key, value in context.items():
            if key.lower() in ['password', 'token', 'secret', 'key', 'auth']:
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, str):
                # Truncate very long strings and sanitize task descriptions
                if len(value) > 500:
                    sanitized[key] = value[:500] + "...[TRUNCATED]"
                else:
                    sanitized[key] = self._sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_context(value)
            elif isinstance(value, list):
                sanitized[key] = [self._sanitize_string(str(item)) if isinstance(item, str) else item for item in value[:10]]  # Limit list size
            else:
                sanitized[key] = value
                
        return sanitized
    
    def _sanitize_string(self, text: str) -> str:
        """Sanitize string content removing potential PII patterns.
        
        Args:
            text: Raw string content
            
        Returns:
            Sanitized string
        """
        import re
        
        # Pattern for email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        # Pattern for potential tokens (long alphanumeric strings)
        text = re.sub(r'\b[A-Za-z0-9]{32,}\b', '[TOKEN]', text)
        
        # Pattern for URLs with potential sensitive data
        text = re.sub(r'https?://[^\s]+', '[URL]', text)
        
        return text
    
    def _format_log_entry(
        self,
        level: LogLevel,
        event: str,
        message: str,
        trace_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        error: Optional[Dict[str, str]] = None,
        duration_ms: Optional[float] = None
    ) -> str:
        """Format log entry as MCP-compliant JSON.
        
        Args:
            level: Log level
            event: Event identifier
            message: Human-readable message
            trace_id: Optional trace ID for request correlation
            context: Optional context data
            error: Optional error information
            duration_ms: Optional duration in milliseconds
            
        Returns:
            JSON-formatted log entry
        """
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level.value,
            "component": self.component,
            "event": event,
            "message": message
        }
        
        if trace_id:
            log_entry["trace_id"] = trace_id
            
        if context:
            log_entry["context"] = self._sanitize_context(context)
            
        if duration_ms is not None:
            log_entry["duration_ms"] = round(duration_ms, 2)
            
        if error:
            log_entry["error"] = error
        
        return json.dumps(log_entry, separators=(',', ':'))
    
    def _write_log(self, log_entry: str) -> None:
        """Write log entry to stderr following MCP requirements.
        
        Args:
            log_entry: Formatted JSON log entry
        """
        # MCP REQUIREMENT: Use stderr only, never stdout
        sys.stderr.write(log_entry + '\n')
        sys.stderr.flush()
    
    def debug(
        self,
        event: str,
        message: str,
        trace_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        duration_ms: Optional[float] = None
    ) -> None:
        """Log debug message.
        
        Args:
            event: Event identifier
            message: Human-readable message
            trace_id: Optional trace ID
            context: Optional context data
            duration_ms: Optional duration in milliseconds
        """
        if self._should_log(LogLevel.DEBUG):
            log_entry = self._format_log_entry(
                LogLevel.DEBUG, event, message, trace_id, context, duration_ms=duration_ms
            )
            self._write_log(log_entry)
    
    def info(
        self,
        event: str,
        message: str,
        trace_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        duration_ms: Optional[float] = None
    ) -> None:
        """Log info message.
        
        Args:
            event: Event identifier
            message: Human-readable message
            trace_id: Optional trace ID
            context: Optional context data
            duration_ms: Optional duration in milliseconds
        """
        if self._should_log(LogLevel.INFO):
            log_entry = self._format_log_entry(
                LogLevel.INFO, event, message, trace_id, context, duration_ms=duration_ms
            )
            self._write_log(log_entry)
    
    def warning(
        self,
        event: str,
        message: str,
        trace_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        duration_ms: Optional[float] = None
    ) -> None:
        """Log warning message.
        
        Args:
            event: Event identifier
            message: Human-readable message
            trace_id: Optional trace ID
            context: Optional context data
            duration_ms: Optional duration in milliseconds
        """
        if self._should_log(LogLevel.WARNING):
            log_entry = self._format_log_entry(
                LogLevel.WARNING, event, message, trace_id, context, duration_ms=duration_ms
            )
            self._write_log(log_entry)
    
    def error(
        self,
        event: str,
        message: str,
        trace_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        exception: Optional[Exception] = None,
        duration_ms: Optional[float] = None
    ) -> None:
        """Log error message with optional exception details.
        
        Args:
            event: Event identifier
            message: Human-readable message
            trace_id: Optional trace ID
            context: Optional context data
            exception: Optional exception for stack trace
            duration_ms: Optional duration in milliseconds
        """
        if self._should_log(LogLevel.ERROR):
            error_info = None
            if exception:
                error_info = {
                    "type": type(exception).__name__,
                    "message": str(exception),
                    "stack_trace": self._sanitize_stack_trace(traceback.format_exc())
                }
            
            log_entry = self._format_log_entry(
                LogLevel.ERROR, event, message, trace_id, context, error_info, duration_ms
            )
            self._write_log(log_entry)
    
    def _sanitize_stack_trace(self, stack_trace: str) -> str:
        """Sanitize stack trace removing sensitive file paths.
        
        Args:
            stack_trace: Raw stack trace
            
        Returns:
            Sanitized stack trace
        """
        import re
        
        # Remove absolute file paths, keep relative ones
        stack_trace = re.sub(r'/[^/\s]*/', '.../', stack_trace)
        
        # Remove line numbers for security (optional)
        # stack_trace = re.sub(r', line \d+', ', line XXX', stack_trace)
        
        return stack_trace


# Global logger instances for common components
logger = MCPLogger("cortex-mcp")
strategy_logger = MCPLogger("strategy-architect")
analysis_logger = MCPLogger("analyze-project")
decomposition_logger = MCPLogger("decompose-phases")
task_graph_logger = MCPLogger("task-graph")
mission_map_logger = MCPLogger("mission-map")


def generate_trace_id() -> str:
    """Generate a new trace ID for request correlation.
    
    Returns:
        UUID4-based trace ID
    """
    return str(uuid.uuid4())


def log_workflow_start(
    trace_id: str,
    task_description: str,
    workflow_stage: Optional[str] = None
) -> None:
    """Log workflow start with sanitized task description.
    
    Args:
        trace_id: Trace ID for request correlation
        task_description: Project description (will be sanitized)
        workflow_stage: Optional specific workflow stage
    """
    context = {
        "task_description": task_description,
        "workflow_stage": workflow_stage or "complete"
    }
    
    strategy_logger.info(
        event="workflow_started",
        message=f"Motor de Estrategias workflow initiated",
        trace_id=trace_id,
        context=context
    )


def log_workflow_stage_complete(
    trace_id: str,
    stage: str,
    duration_ms: float,
    context: Optional[Dict[str, Any]] = None
) -> None:
    """Log completion of workflow stage.
    
    Args:
        trace_id: Trace ID for request correlation
        stage: Workflow stage name
        duration_ms: Stage execution duration
        context: Optional stage-specific context
    """
    stage_context = {"workflow_stage": stage}
    if context:
        stage_context.update(context)
    
    strategy_logger.info(
        event="stage_completed",
        message=f"Workflow stage '{stage}' completed successfully",
        trace_id=trace_id,
        context=stage_context,
        duration_ms=duration_ms
    )


def log_workflow_error(
    trace_id: str,
    stage: str,
    error: Exception,
    context: Optional[Dict[str, Any]] = None
) -> None:
    """Log workflow error with context.
    
    Args:
        trace_id: Trace ID for request correlation
        stage: Workflow stage where error occurred
        error: Exception that occurred
        context: Optional error context
    """
    error_context = {"workflow_stage": stage}
    if context:
        error_context.update(context)
    
    strategy_logger.error(
        event="workflow_error",
        message=f"Error in workflow stage '{stage}'",
        trace_id=trace_id,
        context=error_context,
        exception=error
    )


def log_workflow_complete(
    trace_id: str,
    total_duration_ms: float,
    stages_completed: List[str]
) -> None:
    """Log successful workflow completion.
    
    Args:
        trace_id: Trace ID for request correlation
        total_duration_ms: Total workflow duration
        stages_completed: List of completed stages
    """
    context = {
        "stages_completed": stages_completed,
        "total_stages": len(stages_completed)
    }
    
    strategy_logger.info(
        event="workflow_completed",
        message="Motor de Estrategias workflow completed successfully",
        trace_id=trace_id,
        context=context,
        duration_ms=total_duration_ms
    )