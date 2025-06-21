# CortexMCP - Project Brief v2.3
*Formerly: Strategy Library MCP Server*
*Evolution: From Deterministic Engine to Hybrid Collaborative Intelligence*

## Visión del Proyecto ✅ ACHIEVED → 🚀 EVOLVING
**CortexMCP** es un MCP server de vanguardia que proporciona a Claude Code **cognición estratégica colaborativa** mediante un modelo híbrido que combina la fiabilidad determinística con la inteligencia adaptativa de Claude, transformando ideas ambiguas en planes de proyecto ejecutables con capacidades de razonamiento avanzado.

**Status: FASE 2.5 COMPLETADA → FASE 2.7 PLANIFICADA** - CortexMCP evoluciona de "Motor de Estrategias determinista" a **"Plataforma de Inteligencia Colaborativa"** que permite a Claude participar activamente en el proceso de refinamiento estratégico, manteniendo la estructura robusta mientras inyecta inteligencia adaptativa en puntos críticos del workflow.

## Estado Actual: Operacional y Listo para Optimización

### ✅ **Logros de Fase 2.5 (COMPLETADOS)**
- **Motor de Estrategias**: Workflow completo de 4 fases totalmente funcional
- **Integración MCP**: Herramienta strategy-architect lista para producción
- **Compliance de Esquemas**: 100% validación StrategyResponse 
- **Diseño Stateless**: Continuación de workflow perfecta vía suggested_next_state
- **Mejora TDD**: Emparejamiento automático de tareas de prueba
- **Testing Integral**: Validación completa y testing de integración

### 🚀 **Próxima Fase: 2.7 - Collaborative Intelligence Enhancement**
- **Interactive Multi-Step Workflow**: Transformación del strategy-architect de monolítico a colaborativo
- **Claude Refinement Integration**: Inyección de inteligencia de Claude en puntos críticos del análisis
- **Hybrid Collaboration Pattern**: Combinación óptima de determinismo estructural y razonamiento adaptativo
- **Constitutional CLAUDE.md**: Evolución de manual técnico a filosofía de colaboración

### 🎯 **Fase 3.0 - Advanced Parallelization & Standards Alignment**
- **Framework Migration**: Migración a framework MCP oficial (mcp.server.fastmcp)
- **Parallel Execution Actions**: Implementación de execute_batch_tool y dispatch_sub_agent
- **Agent Swarm Coordination**: Capacidades avanzadas de coordinación de sub-agentes
- **Enhanced Integration**: CLAUDE.md constitucional con patrones de uso estructurados

## Contexto y Motivación ✅ REALIZADA
La idea surge de la necesidad de elevar a Claude Code desde un simple programador a un arquitecto, gestor de proyectos e ingeniero de procesos. En lugar de darle herramientas para hacer el trabajo, le damos herramientas para **pensar sobre cómo hacer el trabajo**.

**LOGRO CONSEGUIDO**: CortexMCP mitiga exitosamente problemas comunes en los agentes de IA, como el **"Context Drift"** y el **tiempo de corrección que niega las ganancias de productividad**, al encapsular workflows complejos en llamadas a herramientas atómicas y fiables con respuestas estructuradas.

### Dominio Específico ✅ IMPLEMENTADO
- **Orquestación del desarrollo de software**: ✅ Automatización completa de workflows de desarrollo
- **Cognición estratégica**: ✅ Capacidades avanzadas de análisis y planificación operacionales
- **Meta-automatización**: ✅ Sistema que planifica la escritura completa de módulos y proyectos

## ✅ Motor de Estrategias: OPERACIONAL → 🚀 EVOLUCIONANDO A COLABORATIVO

### Funcionalidad Core ✅ ACHIEVED
El Motor de Estrategias (strategy-architect) automatiza exitosamente la transición de una idea ambigua a un plan de proyecto estructurado mediante:

1. **Análisis de Requisitos** ✅: Procesamiento de descripciones en lenguaje natural con extracción de patrones, complejidad y requisitos implícitos
2. **Descomposición de Tareas** ✅: Generación de grafos de tareas con nodos (tareas) y aristas (dependencias)
3. **Estimación y Análisis de Riesgos** ✅: Enriquecimiento del grafo con metadatos de tiempo, complejidad y bloqueos potenciales  
4. **Asignación de Recursos** ✅: Mapeo de tareas a perfiles de agente apropiados con mejoras TDD

### 🚀 **NUEVA EVOLUCIÓN: Workflow Interactivo Multi-Paso**

#### **Paradigma de Colaboración Híbrida**
El nuevo diseño transforma el strategy-architect de un motor determinista monolítico a una **plataforma de colaboración inteligente** que combina:

- **Estructura Determinística**: Procesos robustos y predecibles para garantizar fiabilidad
- **Inteligencia Adaptativa**: Capacidades de razonamiento de Claude inyectadas en puntos críticos
- **Refinamiento Iterativo**: Mejora continua del análisis mediante colaboración humano-IA

#### **Nuevo Workflow Multi-Paso**

**Workflow Actual (Monolítico):**
```
Usuario → strategy-architect(descripción) → Plan Completo
```

**Nuevo Workflow (Colaborativo):**
```
1. Usuario → Claude: "Planifica API e-commerce"
2. Claude → MCP: strategy-architect(descripción)
3. MCP → Claude: AnalysisPreliminar + delegation("refine_analysis")
4. Claude: [PASO DE PENSAMIENTO] → Refinamiento crítico del análisis
5. Claude → MCP: strategy-architect(descripción, refined_analysis)
6. MCP → Claude: Plan Completo basado en análisis refinado
```

#### **Puntos de Inyección de Inteligencia**

**1. Refinamiento de Análisis Crítico**
- **Momento**: Después del análisis preliminar determinista
- **Delegación a Claude**: Adoptar rol de "Arquitecto Senior Crítico"
- **Objetivo**: Detectar patrones perdidos, tecnologías mejores, arquitecturas alternativas
- **Salida**: `RefinedAnalysis` con mejoras estratégicas

**2. Validación de Dependencias**
- **Momento**: Durante generación de task_graph
- **Delegación a Claude**: Revisar dependencias críticas y bloqueos potenciales
- **Objetivo**: Optimizar paralelización y identificar riesgos de integración

**3. Optimización de Asignación**
- **Momento**: Durante mission_map generation
- **Delegación a Claude**: Evaluar asignación de recursos y perfiles de agente
- **Objetivo**: Maximizar eficiencia basado en capacidades reales del equipo

#### **Ventajas del Workflow Híbrido**

✅ **Mantiene Fiabilidad**: La estructura determinística sigue siendo el backbone
✅ **Aumenta Inteligencia**: Claude aporta razonamiento crítico donde más valor añade
✅ **Reduce Context Drift**: Puntos de inyección controlados y estructurados
✅ **Mejora Calidad**: Análisis refinado produce planes superiores
✅ **Escalabilidad**: Compatible con arquitectura existente y futura paralelización

### Capacidades Actuales (Fase 2.5)
- **Tiempo de Respuesta**: <1.5 segundos para workflows completos
- **Compliance de Esquemas**: 100% validación StrategyResponse
- **Continuación de Workflow**: Ejecución stateless multi-paso
- **Integración TDD**: Emparejamiento automático de tareas de prueba
- **Manejo de Errores**: Respuestas de error compatibles con JSON-RPC 2.0

### ✅ Workflows Implementados y Operacionales

#### ✅ Motor de Estrategias: 4-Phase Workflow (COMPLETADO)
- **Phase 1**: Análisis ✅ - Extracción de patrones, complejidad y requisitos implícitos
- **Phase 2**: Descomposición ✅ - Generación de fases del proyecto con dependencias
- **Phase 3**: Grafo de Tareas ✅ - Dependencias detalladas con metadatos de complejidad
- **Phase 4**: Mapa de Misión ✅ - Asignación de recursos con mejoras TDD

#### ✅ Capacidades de Planificación Avanzada (OPERACIONALES)
- **Project Analysis**: Análisis automático de descripciones de proyecto
- **Complexity Assessment**: Evaluación determinística de complejidad
- **Technology Stack Suggestions**: Recomendaciones de stack tecnológico
- **Resource Assignment**: Mapeo inteligente a perfiles de agente
- **TDD Workflow**: Emparejamiento automático de tareas de implementación y prueba
- **Parallel Execution Planning**: Identificación de oportunidades de paralelización

## ✅ Innovación Clave: Universal Response Schema (IMPLEMENTADO)

### Arquitectura del Sistema de Respuesta Universal ✅ OPERACIONAL
Toda herramienta de CortexMCP retorna respuestas siguiendo un esquema universal que garantiza:
- **Comunicación consistente** ✅ - 100% validación StrategyResponse con Claude Code
- **Flujos de ejecución predecibles** ✅ - execution_type determinísticos implementados
- **Gestión de estado robusta** ✅ - suggested_next_state para continuación de workflows
- **Manejo de errores estructurado** ✅ - JSON-RPC 2.0 compliant error handling

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

### 🚀 **NUEVAS ACCIONES DE PARALELIZACIÓN (Fase 3.0)**

#### **Advanced Action Types para Ejecución Paralela**

**`execute_batch_tool`**: Paralelismo de Bajo Nivel
```typescript
{
  "type": "execute_batch_tool",
  "description": "Ejecutar tareas de linting y testing en paralelo",
  "parameters": {
    "tasks": [
      { "tool": "bash", "command": "npm run lint", "timeout": 30000 },
      { "tool": "bash", "command": "npm test", "timeout": 60000 },
      { "tool": "bash", "command": "npm run typecheck", "timeout": 45000 }
    ],
    "execution_mode": "parallel",
    "failure_strategy": "continue_on_failure"
  }
}
```

**`dispatch_sub_agent`**: Paralelismo de Alto Nivel (Agent Swarms)
```typescript
{
  "type": "dispatch_sub_agent",
  "description": "Delegar implementación del frontend a especialista React",
  "parameters": {
    "persona": "React-TypeScript Virtuoso",
    "task_prompt": "Implementar componente de dashboard con charts interactivos",
    "context_files": ["src/types/dashboard.ts", "src/api/metrics.ts"],
    "deliverables": ["componente funcional", "tests unitarios", "storybook"],
    "coordination_channel": "shared_state_key_dashboard_frontend"
  }
}
```

**`coordinate_parallel_execution`**: Orquestación de Múltiples Agentes
```typescript
{
  "type": "coordinate_parallel_execution",
  "description": "Coordinar desarrollo frontend y backend simultáneamente",
  "parameters": {
    "execution_graph": {
      "frontend_team": { "agent_count": 2, "focus": "UI/UX implementation" },
      "backend_team": { "agent_count": 1, "focus": "API development" },
      "testing_team": { "agent_count": 1, "focus": "integration testing" }
    },
    "synchronization_points": [
      { "milestone": "API_schema_defined", "required_teams": ["backend"] },
      { "milestone": "components_ready", "required_teams": ["frontend"] },
      { "milestone": "integration_ready", "required_teams": ["frontend", "backend"] }
    ]
  }
}
```

#### **Casos de Uso para Paralelización**

**1. Desarrollo de Características Independientes**
- Frontend y backend en paralelo con sincronización en API contracts
- Múltiples microservicios desarrollados por equipos especializados
- Testing automatizado concurrente con desarrollo

**2. Optimización de Performance**
- Linting, typechecking, y testing ejecutados simultáneamente
- Build processes paralelos para diferentes targets
- Análisis de código concurrente (security, quality, performance)

**3. Research y Análisis Distribuido**
- Múltiples agentes investigando tecnologías alternativas
- Análisis paralelo de competidores y best practices
- Validación simultánea de múltiples arquitecturas

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

### ✅ Estructura del Proyecto (IMPLEMENTADA Y OPERACIONAL)
```
cortex-mcp/                      # ✅ CortexMCP - Fully Operational
├── server.py                    # ✅ MCP server con JSON-RPC 2.0 + stdio
├── schemas/
│   ├── universal_response.py    # ✅ StrategyResponse base schema implementado
│   └── architect_payloads.py    # ✅ Payloads específicos del architect
├── tools/
│   ├── architect/               # ✅ Motor de Estrategias - 4 fases operacionales
│   │   ├── analyze_project.py   # ✅ Análisis de proyectos funcional
│   │   ├── decompose_phases.py  # ✅ Descomposición de fases operacional
│   │   ├── task_graph.py        # ✅ Generación de grafos de tareas completa
│   │   └── mission_map.py       # ✅ Mapas de misión con TDD enhancement
│   ├── base_tool.py            # ✅ Base class con universal response
│   └── strategy_architect.py   # ✅ Orchestrator principal operacional
├── tests/                      # ✅ Testing integral completado
│   ├── test_integration.py     # ✅ 5 tests de integración pasando
│   └── tools/architect/        # ✅ Tests unitarios comprehensivos
├── docs/                       # ✅ Documentación actualizada
│   ├── phase2.5_preparation.md # ✅ Completado
│   └── phase3_preparation.md   # ✅ Preparado para siguiente fase
├── config/                     # ✅ Configuraciones operacionales
└── utils/                      # ✅ Utilidades implementadas
```

### 🎯 Fase 3 - Preparación para Optimización
- **Framework Migration**: Migrar a mcp.server.fastmcp
- **Slash Commands**: /project:architect-plan, /project:architect-continue, /project:architect-analyze  
- **Enhanced CLAUDE.md**: Patrones de uso optimizados
- **Standards Compliance**: 100% alineación con especificaciones MCP

### ✅ Herramienta Principal: Strategy-Architect (Motor de Estrategias) - OPERACIONAL

**Decisión Arquitectónica Implementada**: ✅ Endpoint único `strategy-architect` completamente funcional que encapsula el workflow completo de planificación, con lógica interna modular probada para máxima fiabilidad.

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

**✅ Funcionamiento del Motor de Estrategias (OPERACIONAL):**

1. **Detección de Estado** ✅: El motor analiza los inputs para determinar automáticamente en qué etapa del workflow se encuentra
2. **Ejecución Determinista** ✅: Ejecuta la secuencia probada: Análisis → Descomposición → Grafo → Mapa  
3. **Funciones Internas Modulares** ✅: Cada paso implementado en módulos separados y orquestados internamente
4. **Continuación de Workflow** ✅: Continúa desde cualquier punto usando el estado previo vía suggested_next_state

**Métricas de Rendimiento Actuales:**
- **Tiempo de respuesta**: <1.5 segundos para workflows completos
- **Tasa de éxito**: 100% en tests de integración 
- **Cobertura de esquemas**: 100% validación StrategyResponse
- **Continuación de estado**: Operacional con 0% pérdida de contexto

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

## 🚀 **Fases de Desarrollo Evolutivas - Roadmap v2.3**

### ✅ **Fase 1-2.5: COMPLETADAS**
**Fundación Sólida y Motor de Estrategias Operacional**
- ✅ Universal Response Schema implementado con validación Pydantic
- ✅ Motor de Estrategias de 4 fases completamente funcional
- ✅ Testing integral y compliance 100% de esquemas
- ✅ Arquitectura stateless robusta y escalable

### 🚀 **Fase 2.7: Collaborative Intelligence Enhancement (INMEDIATA)**
**Transformación a Inteligencia Colaborativa Híbrida**

**Objetivos Principales:**
- **Workflow Multi-Paso**: Transformar strategy-architect de monolítico a colaborativo
- **Claude Refinement Integration**: Inyección de inteligencia de Claude en análisis crítico
- **Constitutional CLAUDE.md**: Implementar constitución de colaboración híbrida

**Tareas Específicas:**
1. **Modificar strategy-architect para workflow interactivo:**
   - Primer paso: análisis preliminar determinista 
   - Segundo paso: delegación a Claude para refinement crítico
   - Tercer paso: continuación con análisis refinado

2. **Ampliar Universal Response Schema:**
   - Nuevos action types: `refine_analysis`, `validate_dependencies`, `optimize_assignment`
   - Mejora de `execution_type: "delegated"` con contexto específico
   - Parámetros para refinement colaborativo

3. **Crear CLAUDE.md Constitucional:**
   - Filosofía de colaboración híbrida
   - Protocolos de workflow colaborativo
   - Triggers automáticos y patrones de uso

4. **Testing del nuevo paradigma:**
   - Tests de workflow multi-paso
   - Validación de refinement de análisis
   - Performance benchmarks colaborativos

**Tiempo Estimado**: 4-6 horas
**Beneficio**: Aprovecha inteligencia de Claude manteniendo fiabilidad determinística

### 🎯 **Fase 3.0: Advanced Parallelization & Standards Alignment**
**Paralelización Avanzada y Migración a Framework Oficial**

**Objetivos Principales:**
- **Framework Migration**: Migrar a mcp.server.fastmcp oficial
- **Parallel Execution Actions**: Implementar execute_batch_tool y dispatch_sub_agent
- **Agent Swarm Coordination**: Capacidades de coordinación multi-agente
- **Standards Compliance**: 100% alineación con especificaciones MCP

**Tareas Específicas:**
1. **Implementar Acciones de Paralelización:**
   ```typescript
   // Nuevas acciones a implementar
   execute_batch_tool    // Paralelismo de bajo nivel
   dispatch_sub_agent    // Agent swarms especializados  
   coordinate_parallel_execution // Orquestación multi-agente
   ```

2. **Sistema de Coordinación:**
   - Synchronization points entre agentes
   - Shared state management para equipos paralelos
   - Conflict resolution y merge strategies

3. **Migration a Framework Oficial:**
   - Reestructurar usando mcp.server.fastmcp
   - Mantener compatibilidad con Universal Response Schema
   - Optimizar performance con nuevas capacidades del framework

4. **Slash Commands Personalizados:**
   - `/project:architect-plan` - Planificación completa
   - `/project:architect-continue` - Continuación de workflow
   - `/project:architect-refine` - Refinamiento colaborativo

**Tiempo Estimado**: 8-12 horas
**Beneficio**: Capacidades de vanguardia en paralelización y standards compliance

### 🌟 **Fase 3.5: Agent Swarm Intelligence**
**Inteligencia Distribuida y Especialización Avanzada**

**Objetivos Futuros:**
- **Especialización de Agentes**: Perfiles específicos por dominio tecnológico
- **Learning y Adaptación**: Sistema de aprendizaje para mejorar confidence scores
- **Templates Inteligentes**: Workflows pre-configurados por tipo de proyecto
- **Performance Analytics**: Métricas avanzadas y optimización continua

**Capacidades Avanzadas:**
1. **Agent Specialization:**
   - Frontend-React-Virtuoso
   - Backend-API-Architect  
   - DevOps-Infrastructure-Expert
   - Security-Audit-Specialist

2. **Intelligent Templates:**
   - E-commerce Platform Template
   - Microservices Architecture Template
   - Real-time Application Template
   - Mobile-First PWA Template

3. **Learning System:**
   - Pattern recognition de proyectos exitosos
   - Optimización automática de estimaciones
   - Feedback loop para mejorar accuracy

4. **Advanced Analytics:**
   - Project success rate tracking
   - Complexity vs delivery time correlation
   - Technology stack effectiveness metrics

**Tiempo Estimado**: 12-16 horas
**Beneficio**: Plataforma de inteligencia arquitectónica de clase mundial

### 🔄 **Filosofía Evolutiva**
**Principios de Desarrollo Continuo:**
- **Compatibilidad hacia atrás**: Cada fase mantiene funcionalidad existente
- **Evolución incremental**: Mejoras graduales sin disrupciones
- **Testing continuo**: Validación en cada paso del desarrollo
- **User feedback integration**: Incorporación de feedback real de uso

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

## ✅ Fases Completadas y Próximos Pasos

### ✅ COMPLETADO - Fases 1-2.5
1. **Fase 1** ✅: Estructura base con Universal Response Schema implementada
2. **Fase 2** ✅: Endpoint único `strategy-architect` con motor de estrategias completamente funcional
3. **Fase 2.5** ✅: Funciones modulares operacionales con testing integral validado

### 🎯 PRÓXIMO - Fase 3: Standards Alignment & Claude Code Optimization
1. **Framework Migration**: Migrar a framework MCP oficial (mcp.server.fastmcp)
2. **Slash Commands**: Implementar comandos personalizados para Claude Code
3. **Enhanced Integration**: CLAUDE.md optimizado con patrones de uso estructurados
4. **Performance Optimization**: Optimizaciones de rendimiento y experiencia de usuario

**Tiempo estimado Fase 3**: 3 horas | **Preparación**: docs/phase3_preparation.md

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

## 🏛️ **Filosofía Constitucional del CLAUDE.md**

### **Paradigma: De Manual Técnico a Constitución de Colaboración**

El nuevo CLAUDE.md evoluciona de ser un simple manual de uso a convertirse en la **"Constitución Digital"** que define los principios, roles y protocolos de la colaboración híbrida entre Claude y CortexMCP.

#### **Principios Fundamentales de la Constitución**

**1. Principio de Colaboración Híbrida**
```markdown
# CLAUDE.md - Constitución de Colaboración CortexMCP

## Filosofía Central: Inteligencia Colaborativa Híbrida

Tu misión es ser el **razonamiento crítico y adaptativo** en una partnership estratégica con CortexMCP. 
Mientras CortexMCP proporciona **estructura y proceso**, tu aportas **análisis crítico y creatividad**.

### Roles Definidos:
- **Tu Rol (Claude)**: Razonamiento, crítica constructiva, refinamiento estratégico, toma de decisiones contextuales
- **Rol del CortexMCP**: Proceso estructurado, workflows deterministas, consistencia, gestión de estado

### Mantra de Colaboración:
"Juntos somos más fuertes: tu inteligencia + mi estructura = excelencia arquitectónica"
```

**2. Protocolos de Interacción Inteligente**
```markdown
## Protocolos de Workflow Colaborativo

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

### Patrón de Paralelización (Fase 3.0)
- `execute_batch_tool`: Úsalo para tareas técnicas independientes
- `dispatch_sub_agent`: Delega tareas complejas a especialistas virtuales
- Coordina sincronización en puntos críticos del desarrollo
```

**3. Triggers Automáticos y Contextuales**
```markdown
## Reglas de Invocación Automática

### Triggers Principales
- **Keywords de planificación**: "planifica", "arquitectura", "diseña" → `strategy-architect`
- **Descripciones complejas** (>50 palabras) → Workflow completo del Motor de Estrategias
- **Modificaciones de proyecto** → Continuación con `suggested_next_state` previo
- **Requests de análisis** → Activar modo de refinamiento colaborativo

### Triggers de Paralelización (Fase 3.0)
- **Múltiples tareas independientes** → `execute_batch_tool`
- **Equipos especializados necesarios** → `dispatch_sub_agent`
- **Proyectos complejos multi-componente** → `coordinate_parallel_execution`

### Anti-patterns (Evitar)
- No usar CortexMCP para tareas simples de 1-2 pasos
- No sobrecargar con micro-gestión de tareas triviales
- No usar paralelización para tareas secuenciales por naturaleza
```

**4. Memoria y Continuidad de Estado**
```markdown
## Gestión de Estado y Memoria

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
  parallel_execution_status: { ... }
}
```

### Uso de suggested_next_state
Siempre revisa y utiliza `payload.suggested_next_state` para:
- Continuar workflows interrumpidos
- Mantener contexto entre sesiones
- Optimizar llamadas subsecuentes al MCP
```

#### **Contenido Específico de la Constitución CLAUDE.md**

**Sección 1: Filosofía y Principios**
- Definición del rol colaborativo híbrido
- Principios de la inteligencia aumentada
- Ética de la colaboración humano-IA-sistema

**Sección 2: Workflow Patterns**
- Patrones de refinamiento interactivo
- Protocolos de toma de decisiones
- Gestión de paralelización y coordinación

**Sección 3: Triggers y Auto-invocación**
- Reglas automáticas de invocación del MCP
- Patrones contextuales para diferentes tipos de proyecto
- Anti-patterns y casos de uso inapropiados

**Sección 4: Estado y Continuidad**
- Gestión de estado stateless
- Patrones de memoria y contexto
- Uso óptimo de suggested_next_state

**Sección 5: Troubleshooting y Optimización**
- Resolución de problemas comunes
- Optimización de performance
- Mejores prácticas de colaboración

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
*CortexMCP Project Brief - Versión 2.3*
*Creado: 2025-06-20*
*Actualizado: 2025-06-21 - EVOLUCIÓN A INTELIGENCIA COLABORATIVA HÍBRIDA*
*Estado: Funcional v2.5 + Roadmap Evolutivo hacia Vanguardia Tecnológica*

## 🎯 Resumen Ejecutivo - Evolución Estratégica v2.3

**CortexMCP v2.5** está completamente operacional como servidor MCP de clase mundial, y **v2.3** define la evolución hacia **Inteligencia Colaborativa Híbrida** que combina la fiabilidad determinística con la capacidad de razonamiento avanzado de Claude.

**Próximo hito inmediato**: **Fase 2.7 - Collaborative Intelligence Enhancement** - Transformación del Motor de Estrategias de monolítico a colaborativo con inyección inteligente de capacidades de Claude.

**Visión a largo plazo**: Plataforma de inteligencia arquitectónica que:
- ✅ **Mantiene fiabilidad** del proceso estructurado
- 🚀 **Añade inteligencia adaptativa** en puntos críticos  
- 🌟 **Evoluciona hacia paralelización** avanzada y agent swarms
- 🏛️ **Establece nueva constitución** de colaboración humano-IA

**Innovation Core**: Transición de "Motor Determinista" a "Plataforma de Colaboración Inteligente" que representa el estado del arte en sistemas MCP colaborativos.

**Diferenciación competitiva**: Primer MCP que implementa el paradigma de "Hybrid Collaborative Intelligence" manteniendo 100% compatibilidad y fiabilidad operacional.