# CortexMCP Observability Strategy

*Comprehensive debugging and monitoring framework aligned with official MCP standards*

## Executive Summary

This document outlines the implementation strategy for a comprehensive observability framework for CortexMCP, ensuring full compliance with official Model Context Protocol debugging standards while maintaining our established architectural principles.

## Official MCP Standards Compliance

### Logging Standards (Per MCP Documentation)

Based on the official MCP debugging guide at `https://modelcontextprotocol.io/docs/tools/debugging`, our implementation must adhere to:

1. **Logging Destination Requirements**
   - ✅ **MANDATORY**: Local MCP servers must NOT log to stdout
   - ✅ **MANDATORY**: Use stderr for automatic host application capture
   - ✅ **OPTIONAL**: Use `send_log_message()` method for client-side logging

2. **Structured Logging Requirements**
   - ✅ Consistent log formats across all components
   - ✅ Include contextual information (trace IDs, request context)
   - ✅ Add timestamps to all log entries
   - ✅ Track request IDs for correlation
   - ✅ Sanitize sensitive data before logging

3. **Critical Events to Log**
   - ✅ Initialization steps
   - ✅ Resource access (strategy-architect tool calls)
   - ✅ Tool execution phases (Motor de Estrategias workflow stages)
   - ✅ Error conditions with stack traces
   - ✅ Performance metrics and timing data

## Implementation Architecture

### Core Components

#### 1. Structured Logger (`utils/logger.py`)

**Purpose**: MCP-compliant JSON logging utility
**Output**: stderr (following MCP requirement)
**Format**: Structured JSON with consistent schema

```python
# Target Log Format
{
  "timestamp": "2025-01-21T10:30:15.123Z",
  "level": "INFO|DEBUG|WARNING|ERROR",
  "trace_id": "uuid4-generated-id",
  "component": "strategy-architect|analyze-project|decompose-phases|...",
  "event": "workflow_started|phase_completed|error_occurred|...",
  "message": "Human-readable description",
  "context": {
    "task_description": "sanitized version",
    "workflow_stage": "analysis|decomposition|task_graph|mission_map",
    "duration_ms": 1234,
    "additional_context": "..."
  },
  "error": {  // Only present for error logs
    "type": "ValueError|Exception|...",
    "message": "Error description",
    "stack_trace": "sanitized stack trace"
  }
}
```

#### 2. Workflow Trace ID System

**Purpose**: Request correlation across Motor de Estrategias workflow
**Implementation**: UUID4-based trace IDs propagated through all functions
**Scope**: From `strategy_architect` entry point through all internal functions

```python
# Function Signature Pattern
def execute_architect_workflow(
    task_description: str,
    trace_id: Optional[str] = None,
    ...
) -> StrategyResponse[ArchitectPayload]:
    if not trace_id:
        trace_id = str(uuid.uuid4())
    
    logger.info("Workflow started", trace_id=trace_id, ...)
```

#### 3. Debug Payload Extension

**Purpose**: Conditional detailed debugging information in responses
**Trigger**: `debug_mode=true` parameter in tool calls
**Content**: Intermediate workflow results, timing data, internal state

```python
# Extended StrategyResponse Schema
class StrategyResponse(BaseModel):
    strategy: Strategy
    user_facing: UserFacing
    claude_instructions: ClaudeInstructions
    payload: T
    metadata: Metadata
    debug_payload: Optional[Dict[str, Any]] = None  # NEW FIELD
```

#### 4. Debug Mode Flag

**Purpose**: Enable/disable debug payload generation
**Location**: strategy-architect tool inputSchema
**Default**: false (no performance impact by default)

```python
# Tool Definition Update
@app.tool(name="strategy-architect")
def strategy_architect(
    task_description: Annotated[str, Field(...)],
    debug_mode: Annotated[Optional[bool], Field(
        default=False,
        description="Enable debug payload with intermediate workflow results"
    )] = False,
    ...
) -> str:
```

## Performance Considerations

### Minimal Overhead Design

1. **Lazy Debug Payload Generation**
   - Debug information only collected when `debug_mode=true`
   - No performance impact for normal operations

2. **Efficient Logging**
   - Structured logger with minimal formatting overhead
   - Asynchronous logging consideration for high-volume scenarios

3. **Memory Management**
   - Debug payloads cleared after response generation
   - No persistent state maintained (following Principio Rector #3)

### Performance Monitoring

Track key metrics:
- Workflow execution times per stage
- Memory usage during complex workflows
- Logging overhead measurement
- Debug mode performance impact

## Security and Privacy

### Data Sanitization

Following MCP requirements for sensitive data handling:

1. **Task Description Sanitization**
   - Remove potential PII from logs
   - Truncate overly long descriptions
   - Mask sensitive patterns (emails, tokens, etc.)

2. **Error Information Sanitization**
   - Stack traces cleaned of file paths
   - Error messages sanitized
   - No internal state exposure

3. **Debug Payload Security**
   - No sensitive intermediate data in debug payloads
   - Client-side filtering of debug information

## Integration with Existing Architecture

### Compatibility with Principios Rectores

1. **Principio Rector #1: Dogmatismo con Universal Response Schema**
   - ✅ Debug payload is optional extension, maintains schema compliance
   - ✅ All responses remain valid StrategyResponse objects

2. **Principio Rector #2: Servidor como Ejecutor Fiable**
   - ✅ Structured logging enhances reliability monitoring
   - ✅ Error tracking improves failure detection

3. **Principio Rector #3: Estado en Claude, NO en Servidor**
   - ✅ No persistent logging state maintained
   - ✅ Trace IDs generated per request, not stored

4. **Principio Rector #4: Testing Concurrente**
   - ✅ Thread-safe logging implementation
   - ✅ Comprehensive test coverage for observability features

### FastMCP Framework Integration

- ✅ No modifications to FastMCP server structure required
- ✅ Logging happens within tool execution, not framework level
- ✅ Compatible with existing error handling patterns

## Implementation Timeline

### Phase 1: Foundation (90 minutes)
1. **Structured Logger Implementation** (45 min)
   - Create `utils/logger.py` with MCP-compliant JSON format
   - Configure stderr output following MCP requirements
   - Implement log level management

2. **Architecture Verification** (15 min)
   - Confirm `execute_architect_workflow` orchestrator structure
   - Verify modular function call patterns

3. **Initial Integration** (30 min)
   - Add basic logging to main workflow entry points
   - Test stderr output compliance

### Phase 2: Trace System (60 minutes)
1. **Trace ID Generation** (20 min)
   - UUID4-based trace ID system
   - Function signature updates

2. **Workflow Instrumentation** (40 min)
   - Propagate trace IDs through all Motor de Estrategias functions
   - Add structured logging at key workflow points

### Phase 3: Debug Features (60 minutes)
1. **Schema Extension** (30 min)
   - Add optional `debug_payload` to StrategyResponse
   - Maintain backward compatibility

2. **Debug Mode Implementation** (30 min)
   - Add `debug_mode` parameter to tool inputSchema
   - Implement conditional debug payload population

### Phase 4: Testing & Validation (45 minutes)
1. **Test Suite Creation** (30 min)
   - Comprehensive observability tests
   - Debug mode behavior validation

2. **Integration Testing** (15 min)
   - End-to-end workflow testing with observability
   - Performance impact measurement

## Success Criteria

### Functional Requirements
- ✅ All logs output to stderr in structured JSON format
- ✅ Trace IDs correlate requests across all workflow stages
- ✅ Debug mode conditionally populates debug_payload
- ✅ No breaking changes to existing API
- ✅ 100% test coverage for new observability features

### Performance Requirements
- ✅ <5% performance overhead when debug_mode=false
- ✅ <20% performance overhead when debug_mode=true
- ✅ Memory usage remains within current baselines

### Compliance Requirements
- ✅ Full alignment with official MCP debugging standards
- ✅ Structured logging follows MCP format requirements
- ✅ Sensitive data sanitization implemented
- ✅ Error handling patterns follow MCP best practices

## Future Enhancements

### Phase 2 Considerations
1. **Metrics Collection**
   - Prometheus-style metrics export
   - Performance analytics dashboard

2. **Advanced Debugging**
   - Interactive debugging modes
   - Real-time workflow visualization

3. **Monitoring Integration**
   - CloudWatch/DataDog integration
   - Alerting on error patterns

---

**Document Status**: Ready for Implementation  
**MCP Compliance**: Verified against official documentation  
**Next Action**: Proceed with Phase 1 implementation  

*This strategy ensures CortexMCP maintains its world-class reliability while gaining comprehensive observability capabilities aligned with official MCP standards.*