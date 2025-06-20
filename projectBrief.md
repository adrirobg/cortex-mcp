# Strategy Library MCP Server - Project Brief

## Visión del Proyecto
Crear un MCP server que proporcione a Claude Code **cognición estratégica bajo demanda** para transformar ideas ambiguas en planes de proyecto estructurados, automatizando workflows de arquitectura de software.

Nuestra visión es posicionarnos como **"constructores de agentes"** dentro del ecosistema de Claude, creando una herramienta de alto nivel que extiende sus capacidades fundamentales y contribuye al ecosistema descentralizado de herramientas especializadas.

## Contexto y Motivación
La idea surge de la necesidad de elevar a Claude Code desde un simple programador a un arquitecto, gestor de proyectos e ingeniero de procesos. En lugar de darle herramientas para hacer el trabajo, le damos herramientas para **pensar sobre cómo hacer el trabajo**.

El MCP está diseñado para mitigar problemas comunes en los agentes de IA, como el **"Context Drift"** (pérdida de contexto en tareas largas) y el **tiempo de corrección que niega las ganancias de productividad**, al encapsular workflows complejos en llamadas a herramientas atómicas y fiables con respuestas estructuradas.

### Dominio Específico
- **Orquestación del desarrollo de software**: Automatización de workflows de desarrollo de principio a fin
- **Cognición estratégica**: Proveer capacidades de análisis y planificación de alto nivel
- **Meta-automatización**: No automatizar "escribir una función", sino "planificar la escritura de todas las funciones de un módulo"

## MVP: Strategy-Architect Component

### Funcionalidad Core
El strategy-architect automatiza la transición de una idea ambigua a un plan de proyecto estructurado mediante:

1. **Análisis de Requisitos**: Toma descripciones en lenguaje natural y extrae patrones, complejidad y requisitos implícitos
2. **Descomposición de Tareas**: Genera grafos de tareas con nodos (tareas) y aristas (dependencias)
3. **Estimación y Análisis de Riesgos**: Enriquece el grafo con metadatos de tiempo, complejidad y bloqueos potenciales
4. **Asignación de Recursos**: Mapea tareas a perfiles de agente apropiados

### Workflows a Automatizar

#### Workflow 1: Architect (Basado en .roo/rules-architect/rules.md)
- **Fase 1**: Inicialización y Planificación de la Definición
- **Fase 2**: Diseño del Grafo de Tareas (Diálogo Guiado por Morfeo)
- **Fase 3**: Ensamblaje del Prompt Final para El Oráculo
- **Fase 4**: Finalización

#### Workflow 2: Project Overview (Basado en recurso web analizado)
- Project Basics (nombre, tagline, identidad)
- Vision Statement (objetivos a largo plazo)
- Problem Statement (problemas específicos)
- Solution (enfoque de implementación)
- Target Audience (segmentos de audiencia)
- Success Metrics (objetivos medibles)
- Project Scope (conjunto de características)
- Risk Assessment (desafíos potenciales)
- Success Criteria (condiciones de finalización)

## Innovación Clave: Universal Response Schema

### Arquitectura del Sistema de Respuesta Universal
Toda herramienta del MCP retorna respuestas siguiendo un esquema universal que garantiza:
- **Comunicación consistente** con Claude Code
- **Flujos de ejecución predecibles** 
- **Gestión de estado robusta**
- **Manejo de errores estructurado**

#### Schema Universal `StrategyResponse`
```typescript
interface StrategyResponse {
  // Identificación de estrategia
  strategy: {
    name: string;                    // Identificador único
    version: string;                 // Versionado semántico
    type: StrategyType;             // "analysis" | "execution" | "coordination" | "learning"
  };
  
  // Comunicación con el usuario
  user_facing: {
    summary: string;                 // Resumen en lenguaje natural
    visualization?: string;          // Diagramas opcionales (Mermaid/ASCII)
    key_points?: string[];          // Puntos importantes
    next_steps?: string[];          // Acciones sugeridas
  };
  
  // Instrucciones para Claude
  claude_instructions: {
    execution_type: ExecutionType;   // "immediate" | "user_confirmation" | "multi_step" | "delegated"
    actions: Action[];              // Lista ordenada de acciones
    context_requirements?: {         // Contexto necesario
      required_tools?: string[];     // Otras herramientas MCP necesarias
      required_info?: string[];      // Información a recopilar
    };
    decision_points?: DecisionPoint[]; // Puntos que requieren juicio de Claude
    fallback_strategy?: string;      // Estrategia de recuperación
  };
  
  // Datos específicos de la herramienta
  payload: {
    [key: string]: any;             // Estructura flexible por herramienta
    suggested_next_state?: {         // Estado sugerido para mantener entre llamadas
      workflow_progress?: any;       // Progreso del workflow actual
      accumulated_results?: any;     // Resultados acumulados
      next_step_context?: any;      // Contexto para el siguiente paso
    };
  };
  
  // Metadatos de ejecución
  metadata: {
    confidence_score: number;        // 0-1, confianza de la estrategia
    complexity_score: number;        // 1-10, complejidad de la tarea
    estimated_duration?: string;     // Duración legible
    performance_hints?: string[];    // Sugerencias de optimización
    learning_opportunities?: string[]; // Oportunidades de aprendizaje
  };
  
  // Manejo de errores
  error_handling?: {
    potential_errors: ErrorScenario[];
    recovery_strategies: RecoveryStrategy[];
  };
}
```

### Flujos de Ejecución

#### `execution_type` - Control de Ritmo y Autonomía

**`"immediate"`**: Luz verde para ejecución autónoma completa
- Claude ejecuta todas las `actions` de principio a fin
- No requiere consulta al usuario
- Ideal para análisis puros y operaciones determinísticas

**`"user_confirmation"`**: Luz amarilla con punto de control
- Ejecuta acciones iniciales (presentar información)
- Pausa y espera confirmación explícita del usuario
- Continúa con acciones restantes tras aprobación

**`"multi_step"`**: Modo estándar para workflows complejos
- Procesa `actions` secuencialmente
- Cada acción puede tener naturaleza diferente
- No requiere confirmación entre pasos individuales

**`"delegated"`**: Cambio de contexto a otro rol
- Claude adopta un rol específico (ej. 'think', 'analyst')
- Inicia nuevo hilo de pensamiento con prompt específico
- Sintetiza resultado de vuelta al workflow principal

#### `decision_points` - Objetos Activables
- **No son interrupciones flotantes**
- Se activan mediante acciones específicas: `{"type": "resolve_decision", "parameters": {"decision_id": "dp_123"}}`
- Proporcionan opciones y recomendaciones
- Claude decide autónomamente o delega al usuario según confianza

### Gestión de Estado Stateless
- **El servidor MCP es 100% sin estado**
- **Claude mantiene todo el contexto** entre llamadas
- `session_state` en respuestas es sugerencia de estructura de datos
- Claude debe pasar contexto relevante en llamadas subsecuentes

## Arquitectura Técnica Actualizada

### Alineación con el Ecosistema Claude

Nuestro MCP complementa, no reemplaza, las herramientas de configuración nativas. Se inserta en la jerarquía de configuración de la siguiente manera:

```
1. API System Prompt           → Rol general del agente
2. Global ~/.claude/CLAUDE.md  → Preferencias del desarrollador
3. Project .claude/CLAUDE.md   → Constitución y contexto estático del proyecto
4. Strategy Library MCP        → Lógica de workflow dinámica y cognición estratégica
5. Custom Slash Commands       → Atajos para invocar herramientas del MCP
6. In-Conversation Prompting   → Interacción en tiempo real
```

**Beneficios de esta Integración:**
- **Separación de responsabilidades**: CLAUDE.md para contexto estático, MCP para lógica dinámica
- **Consistencia**: Universal Response Schema garantiza respuestas predecibles
- **Escalabilidad**: Fácil adición de nuevos workflows sin sobrecargar CLAUDE.md
- **Fiabilidad**: Workflows complejos ejecutados en entorno Python robusto

### Estructura del Proyecto
```
strategy_library_mcp/
├── server.py                    # MCP server con JSON-RPC 2.0
├── schemas/
│   ├── universal_response.py    # StrategyResponse base schema
│   ├── architect_payloads.py    # Payloads específicos del architect
│   └── validation.py           # Validación y tipos
├── tools/
│   ├── architect/
│   │   ├── analyze_project.py
│   │   ├── decompose_phases.py
│   │   ├── task_graph.py
│   │   ├── mission_map.py
│   │   └── project_overview.py
│   └── base_tool.py           # Base class con universal response
├── utils/
│   ├── decision_engine.py     # Manejo de decision_points
│   ├── state_manager.py       # Utilidades para session_state
│   └── visualization.py       # Generación de Mermaid diagrams
├── claude_integration/
│   ├── commands.py            # Custom commands para Claude Code
│   ├── subagent_configs.py    # Configuraciones de subagents
│   └── CLAUDE.md             # Reglas de integración automática
├── templates/               # Templates reutilizables
└── tests/                  # Testing completo
```

### Herramienta Principal: Strategy-Architect (Motor de Estrategias)

**Decisión Arquitectónica Clave**: Implementar un endpoint único `strategy-architect` que encapsula el workflow completo de planificación, con lógica interna modular para máxima fiabilidad.

#### Endpoint Principal: `strategy-architect`
```python
@tool("strategy-architect")
def execute_architect_workflow(
    task_description: str,
    analysis_result: Optional[dict] = None,
    decomposition_result: Optional[dict] = None,
    workflow_stage: Optional[str] = None
) -> StrategyResponse[ArchitectPayload]:
```

**Funcionamiento del Motor de Estrategias:**

1. **Detección de Estado**: El motor analiza los inputs para determinar en qué etapa del workflow se encuentra
2. **Ejecución Determinista**: Ejecuta la secuencia estándar: Análisis → Descomposición → Grafo → Mapa
3. **Funciones Internas Modulares**: Cada paso se implementa en módulos separados pero se orquesta internamente
4. **Continuación de Workflow**: Puede continuar desde cualquier punto usando el estado previo

#### Arquitectura Interna del Motor
```
tools/architect/
├── __init__.py              # Endpoint principal strategy-architect
├── analyze_project.py       # Función: _analyze_project_idea()
├── decompose_phases.py      # Función: _decompose_to_phases()
├── task_graph.py           # Función: _generate_task_graph()
├── mission_map.py          # Función: _create_mission_map()
└── project_overview.py     # Función: _generate_project_overview()
```

#### Ventajas de esta Arquitectura

**✅ Fiabilidad Máxima**: Workflow determinista codificado en Python
**✅ API Externa Simple**: Un solo endpoint para todo el proceso de arquitectura
**✅ Implementación Modular**: Cada paso en su propio archivo para mantenibilidad
**✅ Stateless Real**: Claude mantiene el estado, el servidor es completamente sin estado
**✅ Continuación Inteligente**: Puede reanudar desde cualquier punto del workflow

#### Payload del Strategy-Architect
```typescript
interface ArchitectPayload {
  // Estado actual del workflow
  workflow_stage: "analysis" | "decomposition" | "task_graph" | "mission_map" | "complete";
  
  // Resultados acumulados
  analysis?: AnalysisResult;
  decomposition?: DecompositionResult;
  task_graph?: TaskGraphResult;
  mission_map?: MissionMapResult;
  
  // Estado sugerido para próxima llamada
  suggested_next_state?: {
    continue_workflow: boolean;
    next_inputs: dict;
    estimated_completion: string;
  };
  
  // Visualizaciones generadas
  diagrams?: {
    hierarchy_diagram?: string;  // Mermaid
    task_graph_diagram?: string; // Mermaid
    dependency_matrix?: string;  // ASCII table
  };
}

## Fases de Desarrollo Actualizadas

### Fase 1: Implementación del Universal Response Schema
- **Core Schema**: Implementar `StrategyResponse` con Pydantic genérics
- **Validation Layer**: Esquemas específicos para cada herramienta (`AnalysisPayload`, `TaskGraphPayload`, etc.)
- **Error Handling**: Sistema robusto de recovery strategies y fallback
- **Estado Stateless**: Diseño completamente sin estado en el servidor
- **Base Tool Class**: Clase base que garantiza el patrón universal

### Fase 2: Herramientas Core con Schema Universal
- **Implementación consistente**: Todas las herramientas siguen el mismo patrón
- **Payloads fuertemente tipados**: Validación Pydantic para cada tipo de payload
- **Decision Engine**: Sistema para manejar decision_points dinámicamente
- **Visualization Generator**: Utilidades para generar diagramas Mermaid
- **State Management**: Utilidades para sugerir session_state structures

### Fase 3: Optimizaciones para Claude Code
**Integración avanzada basada en task-agent-tools:**

- **CLAUDE.md Rules**: Reglas automáticas para invocación del MCP
  ```markdown
  # Strategy Library MCP Integration Rules
  
  ## Automatic MCP Invocation
  - When user mentions "project planning" → call analyze_project_idea
  - When user asks for "task breakdown" → call decompose_to_phases
  - Complex projects → spawn parallel subagents
  
  ## Parallel Execution Patterns
  - Analysis + Decomposition + Validation can run concurrently
  - Use subagents for independent research tasks
  ```

- **Parallel Subagents**: 
  - **Architect-Analyzer**: Especializado en análisis de requisitos
  - **Graph-Generator**: Creación y optimización de grafos de tareas
  - **Validator-Agent**: Validación y testing de estrategias
  - **Context-Manager**: Gestión de session_state entre llamadas

- **Custom Commands**: 
  - `/strategy-analyze "project description"` - Análisis rápido
  - `/strategy-decompose` - Descomposición guiada
  - `/strategy-execute` - Ejecución de plan completo
  - `/strategy-optimize` - Optimización de workflow existente

- **Context Optimization**: 
  - Session state management inteligente
  - Reutilización de análisis previos
  - Cache de decisiones comunes

### Fase 4: Advanced Features y Learning
- **Strategy-Learner Integration**: 
  - Acumulación de metadata de todas las ejecuciones
  - Pattern learning para mejorar confidence_scores
  - Optimización automática de workflows basada en historial

- **Workflow Templates**: 
  - Templates pre-configurados para casos comunes
  - Plantillas especializadas por tipo de proyecto
  - Configuraciones optimizadas para diferentes dominios

- **Performance Metrics**: 
  - Tracking de confidence scores y accuracy
  - Complexity tracking y optimización
  - Performance hints basados en execution patterns

- **Error Recovery**: 
  - Automated fallback strategies
  - Learning from failures para mejorar recovery
  - Graceful degradation cuando herramientas fallan

## Tecnologías Base
- **Python 3.8+**: Lenguaje principal
- **JSON-RPC 2.0**: Protocolo de comunicación
- **stdin/stdout**: Canal de comunicación
- **Variables de entorno**: Configuración
- **JSON Schema**: Validación de datos

## Casos de Uso con Motor de Estrategias

#### Workflow Completo (Caso Típico)
```
Usuario: "Analiza y planifica un sistema de e-commerce completo"

→ Claude: Llamada única a strategy-architect
   Input: { task_description: "sistema de e-commerce completo" }

→ MCP Motor de Estrategias ejecuta internamente:
   1. _analyze_project_idea() → análisis estructurado
   2. _decompose_to_phases() → fases del proyecto  
   3. _generate_task_graph() → grafo de dependencias
   4. _create_mission_map() → asignación de recursos

→ Respuesta StrategyResponse con:
   ├─ user_facing: "Plan completo generado con 4 fases, 23 tareas, estimación 8 semanas"
   ├─ claude_instructions: execution_type "user_confirmation" + actions
   ├─ payload: ArchitectPayload completo con todos los resultados
   └─ metadata: confidence_score 0.87, complexity_score 8
```

#### Continuación de Workflow (Caso Avanzado)
```
Usuario: "Modifica la fase de autenticación para usar OAuth2"

→ Claude: Llamada a strategy-architect con estado previo
   Input: { 
     task_description: "modificar autenticación a OAuth2",
     analysis_result: { ... },      // del workflow anterior
     decomposition_result: { ... },  // del workflow anterior
     workflow_stage: "task_graph"   // continuar desde aquí
   }

→ MCP Motor detecta continuación y ejecuta:
   1. Reutiliza análisis y descomposición existentes
   2. Regenera task_graph con modificaciones
   3. Actualiza mission_map según cambios

→ Respuesta optimizada solo con los cambios
```

#### Comandos Personalizados
```bash
# Comando simple
/strategy-architect "API REST para gestión de inventario"

# Comando con continuación
/strategy-continue "añadir sistema de notificaciones"

# Comando con validación
/strategy-validate "revisar estimaciones de tiempo"
```

#### Decision Points en Acción
```
Ejemplo de decision_point generado por el motor:

{
  "id": "dp_auth_method",
  "question": "¿Qué método de autenticación prefieres?",
  "options": [
    {"id": "jwt", "description": "JWT tokens (más simple)", "impact": "2 días menos" },
    { "id": "oauth2", "description": "OAuth2 (más seguro)", "impact": "3 días más" }
  ],
  "recommendation": "oauth2",
  "confidence": 0.75
}

Claude evalúa y decide automáticamente (alta confianza) o pregunta al usuario (baja confianza)
```

#### Integración CLAUDE.md Simplificada
```markdown
# Strategy Library MCP Integration

## Auto-trigger Rules
- Keywords: "planifica", "arquitectura", "diseña" → call strategy-architect
- Complex descriptions (>50 words) → use strategy-architect
- Follow-up questions → use suggested_next_state from previous response

## Execution Patterns
- Single call for complete workflows
- State management through payload.suggested_next_state
- Decision points resolved based on confidence scores
```

## Colaboración con Gemini
El desarrollo se realiza en colaboración con Gemini, quien proporciona análisis complementarios y validación de enfoques arquitectónicos.

## Decisiones Arquitectónicas Finales

### 1. Motor de Estrategias vs Herramientas Atómicas ✅
**Decisión**: Implementar Opción B - Motor de Estrategias encapsulado
**Razón**: Fiabilidad y consistencia en workflows deterministas de arquitectura
**Beneficio**: API simple, proceso robusto, experiencia de usuario superior

### 2. Gestión de Estado ✅
**Decisión**: `suggested_next_state` en `payload`, no en `claude_instructions`
**Razón**: Mantiene pureza conceptual del Universal Response Schema
**Beneficio**: Separación clara entre datos y acciones

### 3. Estructura del Proyecto ✅
**Decisión**: Directorio `claude_integration` en el mismo repositorio
**Razón**: Simplicidad para el MVP, acoplamiento controlado
**Beneficio**: Desarrollo y testing integrado

### 4. Paralelización ✅
**Decisión**: MVP con descripciones de tareas paralelas, implementación real en Fase 3
**Razón**: Complejidad gradual, funcionalidad desde el día 1
**Beneficio**: Diseño escalable sin requerir paralelismo inicial

## Próximos Pasos Confirmados
1. **Fase 1**: Implementar estructura base con Universal Response Schema
2. **Endpoint único**: `strategy-architect` con motor de estrategias interno
3. **Funciones modulares**: Cada paso del workflow en archivos separados
4. **Testing integral**: Validar tanto el motor como las funciones individuales

## Arquitectura de Comunicación

### Flujo Típico de Comunicación
```
1. Claude → MCP Tool Call
2. MCP → StrategyResponse (Universal Schema)
3. Claude → Parse response sections:
   ├─ user_facing → Present to user
   ├─ claude_instructions → Execute actions
   ├─ decision_points → Resolve decisions
   └─ payload → Use structured data
4. Claude → Maintain session_state for next calls
```

### Beneficios del Universal Response Schema
- **Predictibilidad**: Claude siempre sabe qué esperar
- **Consistencia**: Misma estructura para todas las herramientas
- **Escalabilidad**: Fácil integración de nuevas herramientas
- **Robustez**: Manejo de errores estructurado
- **Aprendizaje**: Metadata consistente para strategy-learner

## Directrices de Implementación

### Principios Rectores Fundamentales

#### 1. Dogmatismo con Universal Response Schema
- **Regla de Oro**: Validación estricta Pydantic en TODA salida del servidor
- **Sin excepciones**: Cada herramienta DEBE retornar StrategyResponse válido
- **Base de fiabilidad**: Esta consistencia es la columna vertebral del sistema

#### 2. Servidor como Ejecutor Fiable, no Pensador Creativo
- **Heurísticas basadas en reglas**: Usar patrones deterministas y predecibles
- **Rápido y determinista**: El servidor debe ser un motor confiable
- **No IA mágica interna**: La inteligencia reside en Claude, no en el servidor
- **MVP pragmático**: Funcionalidad sólida antes que sofisticación

#### 3. Estado en Claude, NO en Servidor
- **Servidor 100% stateless**: Nunca almacenar información entre llamadas
- **`suggested_next_state`**: Es una instrucción para Claude, no estado interno
- **Responsabilidad de Claude**: Mantener y pasar contexto cuando sea necesario
- **Pureza funcional**: Cada llamada es independiente y autocontenida

#### 4. Testing Concurrente con Desarrollo
- **Tests unitarios**: Para cada función implementada
- **Validación Pydantic**: Para todos los modelos de datos
- **Construcción incremental**: Sobre base sólida y validada
- **No dejar para el final**: Testing como parte integral del desarrollo

---
*Documento de trabajo - Versión 2.2*
*Creado: 2025-06-20*
*Actualizado: 2025-06-20 - Enriquecimiento con Ecosistema Claude y Directrices de Implementación*