# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is **CortexMCP** - a fully operational Model Context Protocol server that provides Claude Code with sophisticated strategic cognition capabilities for software project planning and architecture. CortexMCP transforms ambiguous project ideas into structured plans through its advanced Motor de Estrategias (Strategy Engine), automating complex architectural workflows with production-ready reliability.

## Current Status: Phase 2.5 COMPLETED ✅

**CortexMCP is now fully functional and operational:**
- ✅ **Motor de Estrategias**: Complete 4-phase workflow (Analysis → Decomposition → Task Graph → Mission Map)
- ✅ **MCP Integration**: Production-ready strategy-architect tool accessible via Claude Code
- ✅ **Schema Compliance**: 100% StrategyResponse validation across all workflows  
- ✅ **Stateless Design**: Perfect workflow continuation via suggested_next_state pattern
- ✅ **TDD Enhancement**: Automatic test task pairing in mission maps
- ✅ **Quality Standards**: Comprehensive testing and validation completed

**Next Phase**: Phase 3 - Standards Alignment & Claude Code Optimization (Framework migration, slash commands, enhanced integration)

## Key Architecture Concepts

### Universal Response Schema
All MCP tools return a standardized `StrategyResponse` structure with:
- `user_facing`: Human-readable summaries and visualizations
- `claude_instructions`: Explicit execution directives with `execution_type` ("immediate", "user_confirmation", "multi_step", "delegated")
- `payload`: Tool-specific structured data with `suggested_next_state` for workflow continuation
- `metadata`: Confidence scores, complexity metrics, and learning opportunities

### Stateless Design
- The MCP server maintains **zero state** between calls
- Claude is responsible for maintaining context using `suggested_next_state` from responses
- Each tool call is independent and self-contained

### Motor de Estrategias Pattern (Fully Operational)
CortexMCP implements a sophisticated single `strategy-architect` endpoint that:
- **Automatically detects** workflow stage from input parameters
- **Executes complete** deterministic sequence: Analysis → Decomposition → Task Graph → Mission Map
- **Supports workflow continuation** via stateless state management
- **Uses proven internal** modular functions with unified API
- **Handles both** single-phase execution and complete 4-phase workflows
- **Includes TDD enhancement** with automatic test task pairing

## Development Commands

### Environment Setup
```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Add new dependency
poetry add package-name

# Add development dependency
poetry add --group dev package-name
```

### Server Execution
```bash
# Run CortexMCP server (stdio transport for Claude Code integration)
poetry run python server.py

# Run with debug logging
STRATEGY_LOG_LEVEL=debug poetry run python server.py

# Verify server functionality
poetry run python -c "from tools.strategy_architect import execute_architect_workflow; print('✅ CortexMCP operational')"
```

### Testing
```bash
# Run all tests
poetry run pytest tests/

# Run specific test module
poetry run pytest tests/test_universal_response.py

# Run with coverage
poetry run pytest --cov=. tests/

# Run tests with verbose output
poetry run pytest -v
```

### Schema Validation
```bash
# Validate response schemas
poetry run pytest tests/test_schemas.py -v

# Test specific tool response format
poetry run python scripts/validate_tool_response.py strategy-architect
```

### Linting and Formatting
```bash
# Run type checking
poetry run mypy .

# Format code
poetry run black .

# Check code style
poetry run flake8 .
```

## Project Structure

```
├── server.py                    # Main MCP server (JSON-RPC 2.0 + stdio)
├── schemas/
│   ├── universal_response.py    # Core StrategyResponse schema
│   └── architect_payloads.py    # Tool-specific payload types
├── tools/
│   ├── architect/               # Strategy-architect internal functions
│   │   ├── analyze_project.py
│   │   ├── decompose_phases.py
│   │   ├── task_graph.py
│   │   └── mission_map.py
│   └── base_tool.py            # Base class ensuring Universal Response
└── tests/                      # Comprehensive test suite
```

## Core Tool: strategy-architect (Production Ready)

### Primary Interface
```python
def execute_architect_workflow(
    task_description: str,
    analysis_result: Optional[dict] = None,
    decomposition_result: Optional[dict] = None,
    workflow_stage: Optional[str] = None
) -> StrategyResponse[ArchitectPayload]
```

### Workflow Stages (All Functional)
- **analysis**: Project idea analysis and pattern extraction ✅ OPERATIONAL
- **decomposition**: Phase breakdown with dependencies ✅ OPERATIONAL  
- **task_graph**: Dependency graph generation with metadata ✅ OPERATIONAL
- **mission_map**: Resource assignment and execution planning ✅ OPERATIONAL
- **complete**: Full workflow finished ✅ OPERATIONAL

### Current Capabilities
- **Response Time**: <1.5 seconds for complete workflows
- **Schema Compliance**: 100% StrategyResponse validation
- **Workflow Continuation**: Stateless multi-step execution
- **TDD Integration**: Automatic test task pairing
- **Error Handling**: JSON-RPC 2.0 compliant error responses

### Usage Patterns

**New Project Planning:**
```python
# Claude calls strategy-architect with just description
response = strategy_architect(task_description="e-commerce platform with payment integration")
# Returns complete plan with all workflow stages executed
```

**Workflow Continuation:**
```python
# Claude maintains state and continues from specific stage
response = strategy_architect(
    task_description="modify authentication to OAuth2",
    analysis_result=previous_analysis,
    workflow_stage="task_graph"
)
```

## Response Handling

### Execution Types
- **immediate**: Execute all actions autonomously
- **user_confirmation**: Present results, wait for user approval
- **multi_step**: Process actions sequentially with possible decision points
- **delegated**: Adopt specified role (e.g., 'architect', 'analyst') for specialized reasoning

### Decision Points
```python
# When encountering decision_point in response:
if decision_point["confidence"] > 0.8:
    # High confidence: decide automatically using recommendation
    choice = decision_point["recommendation"]
else:
    # Low confidence: present options to user
    choice = await get_user_choice(decision_point["options"])
```

### State Management
```python
# Extract and maintain workflow state
if response.payload.get("suggested_next_state"):
    workflow_context = response.payload["suggested_next_state"]
    # Use in subsequent calls to continue workflow
```

## Integration Rules for CortexMCP

### Auto-trigger Patterns (Production Ready)
- Keywords "planifica", "arquitectura", "diseña" → invoke strategy-architect
- Complex project descriptions (>50 words) → use strategy-architect  
- Follow-up modifications → continue with existing workflow state
- Project analysis requests → execute complete Motor de Estrategias workflow
- **Phase 3 Ready**: Custom slash commands coming in next phase

### Visualization Handling
- Mermaid diagrams in `user_facing.visualization` → render for user
- ASCII tables in payload → format for console display
- Task graphs → present as interactive breakdown
- **TDD Task Pairs**: Mission maps include both implementation and test tasks

### Performance Guidelines
- **Single Call Preferred**: Use complete workflow for comprehensive planning
- **State Management**: Always check for `suggested_next_state` in responses
- **Error Recovery**: Handle JSON-RPC errors gracefully with fallback options

## Development Principles

### Strict Schema Adherence
- Every tool output must validate against StrategyResponse schema
- Use Pydantic validation throughout the codebase
- No exceptions or shortcuts in response formatting

### Deterministic Operations
- Server functions use rule-based heuristics, not AI inference
- Predictable and testable behavior
- Intelligence resides in Claude's interpretation, not server logic

### Concurrent Testing
- Write unit tests alongside implementation
- Validate both individual functions and integrated workflows
- Test schema compliance for all response variants

## Project Setup Notes
- Para el proyecto quiero utilizar poetry, no python
- **Project Name**: CortexMCP (formerly Strategy Library MCP Server)
- **Current Phase**: 2.5 COMPLETED - Fully operational Motor de Estrategias
- **Next Phase**: 3.0 - Standards Alignment & Claude Code Optimization

## Phase 3 Preparation
CortexMCP is ready for Phase 3 enhancements:
- **Framework Migration**: Migrate to official MCP framework (`mcp.server.fastmcp`)
- **Slash Commands**: Implement `/project:architect-plan`, `/project:architect-continue`, `/project:architect-analyze`
- **Enhanced Integration**: Optimized CLAUDE.md with structured usage patterns
- **Standards Compliance**: 100% alignment with MCP specifications and Claude Code best practices

For Phase 3 implementation details, see: `docs/phase3_preparation.md`