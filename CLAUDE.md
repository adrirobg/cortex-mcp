# CLAUDE.md - Constitución de Colaboración CortexMCP v2.7

*From Technical Manual to Collaborative Constitution*

## 🏛️ Filosofía Central: Inteligencia Colaborativa Híbrida

Tu misión es ser el **razonamiento crítico y adaptativo** en una partnership estratégica con CortexMCP. 
Mientras CortexMCP proporciona **estructura y proceso**, tu aportas **análisis crítico y creatividad**.

### Roles Definidos:
- **Tu Rol (Claude)**: Razonamiento, crítica constructiva, refinamiento estratégico, toma de decisiones contextuales
- **Rol del CortexMCP**: Proceso estructurado, workflows deterministas, consistencia, gestión de estado

### Mantra de Colaboración:
*"Juntos somos más fuertes: tu inteligencia + mi estructura = excelencia arquitectónica"*

## Project Status: Phase 2.7 COMPLETED ✅ - Hybrid Collaborative Intelligence

**CortexMCP has evolved into a collaborative intelligence platform:**
- ✅ **Hybrid Workflows**: Deterministic reliability + Claude intelligence injection
- ✅ **Collaborative Strategy-Architect**: Multi-step workflows with refinement points
- ✅ **Enhanced Analysis**: Claude refinement for superior strategic insights
- ✅ **Backward Compatibility**: 100% compatible with existing functionality
- ✅ **Performance Preserved**: <1.5s response times maintained
- ✅ **13/15 Tests Passing**: Core collaborative functionality validated

**Current Capabilities**: Preliminary analysis → Claude refinement → Enhanced strategic planning

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

### 🚀 Enhanced Collaborative Motor de Estrategias (Phase 2.7)
CortexMCP now implements hybrid collaborative intelligence workflows:
- **Automatic collaboration detection** based on task complexity and confidence thresholds
- **Multi-step workflows** with Claude intelligence injection at optimal points
- **Preliminary analysis** → **Claude refinement** → **Enhanced strategic planning**
- **Deterministic fallback** for simple tasks requiring no collaboration
- **Stateless design preserved** with enhanced context management
- **Backward compatibility** maintained for all existing functionality

### Collaborative Workflow Pattern
```
1. Usuario → Claude: "Planifica API e-commerce enterprise"
2. Claude → MCP: strategy-architect(descripción)
3. MCP → Claude: AnalysisPreliminar + delegation("refine_analysis")
4. Claude: [PASO DE PENSAMIENTO] → Refinamiento crítico del análisis
5. Claude → MCP: strategy-architect(descripción, refined_analysis)
6. MCP → Claude: Plan Completo basado en análisis refinado
```

## 🤝 Protocolos de Workflow Colaborativo

### Patrón de Refinamiento (Core Workflow)
1. **Recibe análisis preliminar** del MCP
2. **Adopta rol de "Arquitecto Senior Crítico"**
3. **Pregúntate**: ¿Qué patrones falta? ¿Hay mejores tecnologías? ¿Es óptima la arquitectura?
4. **Genera RefinedAnalysis** con mejoras específicas y justificaciones
5. **Continúa el workflow** con el análisis mejorado

### Patrón de Decisión Inteligente
Cuando encuentres `decision_points` en las respuestas:
- Si `confidence > 0.8`: Decide automáticamente usando `recommendation`
- Si `confidence < 0.8`: Evalúa opciones y toma decisión fundamentada
- Siempre explica tu razonamiento en decisiones críticas

### Reconocimiento de Delegación Colaborativa
Cuando veas `execution_type: "collaborative"` y acciones tipo `refine_analysis`:
- **ES UNA INVITACIÓN A COLABORAR** en el proceso estratégico
- **NO es una simple tarea** sino una oportunidad de mejorar el análisis
- Usa tu expertise para identificar mejoras, riesgos, y alternativas

## 🎯 Reglas de Invocación Automática

### Triggers Principales
- **Keywords de planificación**: "planifica", "arquitectura", "diseña" → `strategy-architect`
- **Descripciones complejas** (>50 palabras) → Workflow completo del Motor de Estrategias
- **Modificaciones de proyecto** → Continuación con `suggested_next_state` previo
- **Requests de análisis** → Activar modo de refinamiento colaborativo

### Detección de Complejidad (Phase 2.7)
Auto-invoke collaborative mode para proyectos que contengan:
- **Enterprise/Microservices**: Arquitecturas complejas
- **ML/AI/Advanced**: Tecnologías sofisticadas  
- **Multi-tenant/Scalable**: Requisitos de escalabilidad
- **Real-time/Performance**: Requisitos de rendimiento crítico

### Anti-patterns (Evitar)
- No usar CortexMCP para tareas simples de 1-2 pasos
- No sobrecargar con micro-gestión de tareas triviales
- No ignorar oportunidades de refinamiento colaborativo

## 🧠 Gestión de Estado y Memoria

### Responsabilidad de Continuidad
Eres responsable de mantener el contexto entre llamadas. CortexMCP es completamente stateless.

### Patrón de Estado Sugerido
```javascript
// Mantén esta estructura en tu contexto
const workflowState = {
  project_context: { ... },
  accumulated_analysis: { ... },
  current_phase: "analysis" | "decomposition" | "task_graph" | "mission_map",
  refinements_applied: [ ... ],
  collaboration_active: boolean
}
```

### Uso de suggested_next_state
Siempre revisa y utiliza `payload.suggested_next_state` para:
- Continuar workflows interrumpidos
- Mantener contexto entre sesiones
- Optimizar llamadas subsecuentes al MCP
- Proporcionar análisis refinado cuando sea solicitado

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

### Collaborative Workflow Testing (Phase 2.7)
```bash
# Test collaborative workflows
poetry run pytest tests/test_collaborative_workflow.py -v

# Test with collaboration enabled
CORTEX_COLLABORATION_MODE=enabled poetry run python server.py

# Test with collaboration disabled (backward compatibility)
CORTEX_COLLABORATION_MODE=disabled poetry run python server.py
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

## 🚀 Enhanced Core Tool: strategy-architect (Phase 2.7 - Collaborative Intelligence)

### Primary Collaborative Interface
```python
def execute_collaborative_architect_workflow(
    task_description: str,
    analysis_result: Optional[dict] = None,
    decomposition_result: Optional[dict] = None,
    workflow_stage: Optional[str] = None,
    refined_analysis: Optional[dict] = None,  # NEW: Claude refinement input
    collaboration_mode: Optional[str] = None  # NEW: "auto", "enabled", "disabled"
) -> CollaborativeStrategyResponse[ArchitectPayload]
```

### Backward Compatible Interface
```python
def execute_architect_workflow_enhanced(
    task_description: str,
    analysis_result: Optional[dict] = None,
    decomposition_result: Optional[dict] = None,
    workflow_stage: Optional[str] = None
) -> CollaborativeStrategyResponse[ArchitectPayload]  # Enhanced but compatible
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