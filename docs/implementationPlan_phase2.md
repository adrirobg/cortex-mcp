# Implementation Plan Phase 2 - Strategy Library MCP Server

## Estado Actual del Proyecto ✅

### Fase 1 Completada con Éxito
- **Universal Response Schema**: Implementado y validado con Pydantic v2
- **Servidor MCP Base**: JSON-RPC 2.0 funcionando con stdio transport
- **Base Tool Class**: Garantizando StrategyResponse en todas las herramientas
- **Testing Framework**: 32+ tests pasando con cobertura completa
- **Validación Completa**: Todos los Principios Rectores implementados y validados

### Arquitectura Consolidada
1. **Stateless Design**: Servidor sin estado, Claude mantiene contexto
2. **Universal Response Schema**: Formato StrategyResponse sin excepciones
3. **Motor de Estrategias**: Patrón validado con mock, listo para implementación real
4. **Poetry**: Entorno de desarrollo estable y reproducible

### Mock Actual a Reemplazar
- **server.py**: `_mock_strategy_architect_response()` funciona pero es estático
- **tools/architect/**: Estructura creada pero solo con `__init__.py`
- **Schemas**: `ArchitectPayload` completo con todos los modelos necesarios

## Plan de Implementación: Simulación del Strategy-Architect

### Concepto Meta: "Dogfooding Arquitectónico - Fase 2"
**Idea central**: Usar el propio workflow del strategy-architect para planificar la implementación del Motor de Estrategias real, replicando el éxito de la Fase 1.

### Simulación del Workflow Completo

#### Etapa 1: Analysis (analyze_project_idea)
**Input**: "Implementar Fase 2: Motor de Estrategias real que reemplace mock actual"

**Análisis Estructurado**:
```json
{
  "keywords": ["strategy-architect", "analyze_project", "decompose_phases", "task_graph", "mission_map", "heuristics"],
  "patterns": ["Modular functions", "Deterministic logic", "Pydantic models", "Internal workflow"],
  "complexity": "Media-Alta",
  "requirements_implicit": [
    "Mantener 100% compatibilidad con ArchitectPayload",
    "Lógica determinística sin IA",
    "Integración seamless con server.py existente",
    "Testing concurrente obligatorio",
    "Preservar todos los Principios Rectores"
  ],
  "domain": "MCP Server Internal Logic",
  "technology_stack": ["Python", "Pydantic", "typing", "deterministic algorithms"]
}
```

#### Etapa 2: Decomposition (decompose_to_phases)
**Fases Lógicas Identificadas**:

1. **Analyze Project Module**: 
   - Función `analyze_project(task_description: str) -> AnalysisResult`
   - Heurísticas de keywords (web, api, data, mobile, etc.)
   - Detección de patrones comunes
   - Estimación de complejidad basada en longitud y keywords

2. **Decompose Phases Module**: 
   - Función `decompose_phases(analysis: AnalysisResult) -> DecompositionResult`
   - Patrones predefinidos de fases (setup, core, integration, testing, deployment)
   - Generación de dependencies entre fases
   - Estimación de duración por fase

3. **Task Graph Module**: 
   - Función `generate_task_graph(decomposition: DecompositionResult) -> TaskGraphResult`
   - Conversión de fases a tareas granulares
   - Cálculo de dependency matrix
   - Identificación de critical path y bottlenecks

4. **Mission Map Module**: 
   - Función `create_mission_map(task_graph: TaskGraphResult) -> MissionMapResult`
   - Asignación de agent profiles a tareas
   - Optimización de parallel execution groups
   - Resource utilization planning

5. **Strategy Architect Coordinator**: 
   - Función principal `execute_architect_workflow()`
   - Integración de todos los módulos
   - Manejo de estado del workflow
   - Generación del StrategyResponse final

#### Etapa 3: Task Graph (generate_task_graph)
**Grafo de Dependencias**:
```
analyze_project.py → decompose_phases.py → task_graph.py → mission_map.py
       ↓                    ↓                  ↓              ↓
   test_analyze_project → test_decompose → test_task_graph → test_mission_map
       ↓                    ↓                  ↓              ↓
                    strategy_architect.py (Coordinator)
                              ↓
                    test_strategy_architect.py
                              ↓
                    Integration with server.py
```

**Dependencias Críticas**:
- analyze_project es base para decompose_phases
- decompose_phases es base para task_graph
- task_graph es base para mission_map
- strategy_architect coordina todos los módulos
- Testing es paralelo y obligatorio para cada módulo

#### Etapa 4: Mission Map (create_mission_map)
**Asignación y Estrategia**:
- **Implementación secuencial** de módulos con testing paralelo
- **Heurísticas determinísticas** en cada función (sin IA)
- **Compatibilidad total** con ArchitectPayload existente
- **Integración gradual** reemplazando mock progresivamente

### Respuesta StrategyResponse Simulada

```json
{
  "strategy": {
    "name": "implement-phase-2-strategy-architect-engine",
    "version": "2.0.0",
    "type": "execution"
  },
  "user_facing": {
    "summary": "Plan de implementación para Fase 2: Motor de Estrategias real con 5 módulos internos, manteniendo compatibilidad total con arquitectura existente, estimación 3-4 días",
    "key_points": [
      "Implementar analyze_project.py con heurísticas de keywords y patrones",
      "Crear decompose_phases.py con templates de fases predefinidas",
      "Desarrollar task_graph.py con algoritmos de dependencias",
      "Construir mission_map.py con asignación de recursos",
      "Integrar todo en strategy_architect.py como coordinador principal"
    ],
    "next_steps": [
      "Crear analyze_project.py y test correspondiente",
      "Implementar lógica determinística de keywords",
      "Validar que retorna AnalysisResult válido",
      "Proceder secuencialmente con cada módulo"
    ],
    "visualization": "```mermaid\nsequenceDiagram\n    participant C as Claude\n    participant S as Server\n    participant A as AnalyzeProject\n    participant D as DecomposePhases\n    participant T as TaskGraph\n    participant M as MissionMap\n    \n    C->>S: strategy-architect call\n    S->>A: analyze_project(description)\n    A-->>S: AnalysisResult\n    S->>D: decompose_phases(analysis)\n    D-->>S: DecompositionResult\n    S->>T: generate_task_graph(decomposition)\n    T-->>S: TaskGraphResult\n    S->>M: create_mission_map(task_graph)\n    M-->>S: MissionMapResult\n    S-->>C: Complete StrategyResponse\n```"
  },
  "claude_instructions": {
    "execution_type": "multi_step",
    "actions": [
      {
        "type": "implement_analyze_project",
        "description": "Crear analyze_project.py con heurísticas determinísticas",
        "priority": 1,
        "validation_criteria": "Función retorna AnalysisResult válido con keywords y patrones detectados",
        "parameters": {
          "file_path": "tools/architect/analyze_project.py",
          "test_path": "tests/tools/architect/test_analyze_project.py",
          "return_type": "AnalysisResult"
        }
      },
      {
        "type": "implement_decompose_phases",
        "description": "Crear decompose_phases.py con templates de fases",
        "priority": 2,
        "validation_criteria": "Función retorna DecompositionResult con fases y dependencias",
        "parameters": {
          "file_path": "tools/architect/decompose_phases.py",
          "test_path": "tests/tools/architect/test_decompose_phases.py",
          "return_type": "DecompositionResult"
        }
      },
      {
        "type": "implement_task_graph",
        "description": "Crear task_graph.py con algoritmos de dependencias",
        "priority": 3,
        "validation_criteria": "Función retorna TaskGraphResult con dependency matrix",
        "parameters": {
          "file_path": "tools/architect/task_graph.py", 
          "test_path": "tests/tools/architect/test_task_graph.py",
          "return_type": "TaskGraphResult"
        }
      },
      {
        "type": "implement_mission_map",
        "description": "Crear mission_map.py con asignación de recursos",
        "priority": 4,
        "validation_criteria": "Función retorna MissionMapResult con resource assignments",
        "parameters": {
          "file_path": "tools/architect/mission_map.py",
          "test_path": "tests/tools/architect/test_mission_map.py", 
          "return_type": "MissionMapResult"
        }
      },
      {
        "type": "implement_strategy_architect",
        "description": "Crear coordinador principal strategy_architect.py",
        "priority": 5,
        "validation_criteria": "Función principal retorna StrategyResponse completo integrando todos los módulos",
        "parameters": {
          "file_path": "tools/architect/strategy_architect.py",
          "test_path": "tests/tools/architect/test_strategy_architect.py",
          "return_type": "StrategyResponse[ArchitectPayload]"
        }
      }
    ],
    "context_requirements": {
      "required_info": [
        "ArchitectPayload schema completo para compatibilidad",
        "Modelos Pydantic: AnalysisResult, DecompositionResult, TaskGraphResult, MissionMapResult",
        "Principios: Lógica determinística, no IA, testing concurrente"
      ]
    },
    "decision_points": [
      {
        "decision": "Estrategia de keywords para analyze_project",
        "options": ["Predefined dictionary", "Pattern matching", "Combined approach"],
        "recommendation": "Combined approach",
        "confidence": 0.8
      },
      {
        "decision": "Templates de fases para decompose_phases", 
        "options": ["Fixed templates", "Dynamic generation", "Hybrid approach"],
        "recommendation": "Hybrid approach",
        "confidence": 0.85
      }
    ]
  },
  "payload": {
    "workflow_stage": "ready_for_execution",
    "implementation_order": [
      "analyze_project_module",
      "decompose_phases_module", 
      "task_graph_module",
      "mission_map_module",
      "strategy_architect_coordinator",
      "server_integration"
    ],
    "suggested_next_state": {
      "continue_workflow": true,
      "next_step": "implement_analyze_project",
      "context_to_maintain": {
        "phase_1_success": "Universal Response Schema y servidor base funcionando",
        "compatibility_requirement": "100% compatible con ArchitectPayload existente",
        "principles": ["Deterministic logic", "Pydantic validation", "Concurrent testing", "Stateless design"],
        "target_replacement": "server.py _mock_strategy_architect_response function"
      },
      "modules_to_create": [
        "tools/architect/analyze_project.py",
        "tools/architect/decompose_phases.py", 
        "tools/architect/task_graph.py",
        "tools/architect/mission_map.py",
        "tools/architect/strategy_architect.py"
      ],
      "tests_to_create": [
        "tests/tools/architect/test_analyze_project.py",
        "tests/tools/architect/test_decompose_phases.py",
        "tests/tools/architect/test_task_graph.py", 
        "tests/tools/architect/test_mission_map.py",
        "tests/tools/architect/test_strategy_architect.py"
      ]
    }
  },
  "metadata": {
    "confidence_score": 0.94,
    "complexity_score": 7,
    "estimated_duration": "3-4 días",
    "performance_hints": [
      "Implementar y testear cada módulo individualmente antes de integrar",
      "Usar heurísticas simples y determinísticas para máxima confiabilidad",
      "Validar cada función con múltiples casos de prueba",
      "Mantener compatibilidad estricta con schemas existentes"
    ],
    "learning_opportunities": [
      "Implementación de heurísticas determinísticas en analyze_project",
      "Algoritmos de generación de dependency graphs en task_graph",
      "Patrones de coordinación de módulos en strategy_architect",
      "Integración seamless con arquitectura existente"
    ]
  }
}
```

## Próximos Pasos Inmediatos

### Fase 2.1: Analyze Project Module
1. **Crear** `tools/architect/analyze_project.py` con función principal
2. **Implementar** heurísticas de keywords (web, api, data, mobile, etc.)
3. **Detectar** patrones comunes en descripciones de proyectos
4. **Crear** `tests/tools/architect/test_analyze_project.py` con casos de prueba
5. **Validar** que retorna `AnalysisResult` válido

### Fase 2.2: Decompose Phases Module  
1. **Crear** `tools/architect/decompose_phases.py` con templates
2. **Implementar** patrones de fases predefinidas (setup, core, integration, etc.)
3. **Generar** dependencias entre fases automáticamente
4. **Crear** test correspondiente con validación de `DecompositionResult`
5. **Verificar** que fases generadas son lógicas y coherentes

### Fase 2.3: Task Graph Module
1. **Crear** `tools/architect/task_graph.py` con algoritmos de dependencias
2. **Implementar** conversión de fases a tareas granulares
3. **Calcular** dependency matrix y critical path
4. **Identificar** bottlenecks y parallel opportunities
5. **Validar** que `TaskGraphResult` es completo y correcto

### Fase 2.4: Mission Map Module
1. **Crear** `tools/architect/mission_map.py` con asignación de recursos
2. **Implementar** mapping de agent profiles a tareas
3. **Optimizar** parallel execution groups
4. **Calcular** resource utilization estimates
5. **Validar** que `MissionMapResult` es actionable

### Fase 2.5: Strategy Architect Coordinator
1. **Crear** `tools/architect/strategy_architect.py` como coordinador principal
2. **Integrar** todos los módulos en workflow secuencial
3. **Manejar** estado del workflow y error handling
4. **Generar** `StrategyResponse[ArchitectPayload]` completo
5. **Reemplazar** mock en `server.py` con implementación real

## Principios Rectores Durante Implementación

### 1. Dogmatismo con Universal Response Schema
- **Compatibilidad total** con `ArchitectPayload` existente
- **Validación Pydantic estricta** en cada función
- **StrategyResponse format** exacto sin excepciones
- **Testing** de schema compliance en cada módulo

### 2. Servidor como Ejecutor Fiable
- **Heurísticas determinísticas** en lugar de lógica mágica
- **Algoritmos predecibles** que den resultados consistentes
- **Error handling robusto** con fallbacks claros
- **Funcionalidad sólida** antes que sofisticación artificial

### 3. Estado en Claude, NO en Servidor
- **Funciones puras** sin estado interno
- **Todas las funciones** reciben contexto como parámetros
- **suggested_next_state** para continuidad de workflow
- **Zero persistence** en el servidor entre llamadas

### 4. Testing Concurrente
- **Test unitario** para cada función implementada
- **Casos de prueba múltiples** para cada heurística
- **Validación de edge cases** y error conditions
- **Integration tests** para el workflow completo

## Detalles Técnicos Específicos

### Heurísticas para analyze_project
```python
# Keywords mapping
DOMAIN_KEYWORDS = {
    'web': ['web', 'website', 'frontend', 'backend', 'html', 'css', 'javascript'],
    'api': ['api', 'rest', 'graphql', 'endpoint', 'service', 'microservice'],
    'data': ['data', 'database', 'analytics', 'pipeline', 'etl', 'warehouse'],
    'mobile': ['mobile', 'app', 'android', 'ios', 'react-native', 'flutter'],
    'ai': ['ai', 'ml', 'machine learning', 'neural', 'model', 'prediction']
}

# Complexity heuristics
def calculate_complexity(description: str, keywords: List[str]) -> str:
    if len(description) < 50: return "Baja"
    if len(keywords) > 10: return "Alta"
    return "Media"
```

### Templates para decompose_phases
```python
# Phase templates by domain
PHASE_TEMPLATES = {
    'web': ['setup', 'frontend', 'backend', 'integration', 'testing', 'deployment'],
    'api': ['design', 'implementation', 'documentation', 'testing', 'deployment'],
    'data': ['collection', 'processing', 'storage', 'analysis', 'visualization'],
    'default': ['planning', 'implementation', 'testing', 'deployment']
}
```

### Criterios de Validación por Módulo

#### analyze_project.py
- ✅ Función `analyze_project(task_description: str) -> AnalysisResult`
- ✅ Keywords extraídos de DOMAIN_KEYWORDS predefinidos
- ✅ Patterns detectados usando regex o string matching
- ✅ Complexity calculado con heurísticas determinísticas
- ✅ AnalysisResult válido con todos los campos requeridos

#### decompose_phases.py  
- ✅ Función `decompose_phases(analysis: AnalysisResult) -> DecompositionResult`
- ✅ Fases generadas de templates basados en domain
- ✅ Dependencies calculadas lógicamente entre fases
- ✅ Estimated_duration basado en complexity
- ✅ DecompositionResult válido con critical_path

#### task_graph.py
- ✅ Función `generate_task_graph(decomposition: DecompositionResult) -> TaskGraphResult`
- ✅ Tasks generadas granularmente de cada fase
- ✅ Dependency_matrix calculada correctamente
- ✅ Critical_path identificado usando algoritmos de grafos
- ✅ TaskGraphResult válido con parallel_tasks y bottlenecks

#### mission_map.py
- ✅ Función `create_mission_map(task_graph: TaskGraphResult) -> MissionMapResult`
- ✅ Agent_profiles asignados por tipo de tarea
- ✅ Resource_assignments optimizados para parallel execution
- ✅ Execution_order calculado respetando dependencies
- ✅ MissionMapResult válido con resource_utilization

#### strategy_architect.py
- ✅ Función `execute_architect_workflow(**kwargs) -> StrategyResponse[ArchitectPayload]`
- ✅ Integra todos los módulos secuencialmente
- ✅ Maneja workflow_stage apropiadamente
- ✅ Genera StrategyResponse completo con todos los payloads
- ✅ Compatible 100% con server.py existente

## Estado Post-Implementación

Después de completar la Fase 2, el sistema tendrá:
1. **Motor de Estrategias real** funcionando con lógica determinística
2. **Mock completamente reemplazado** por implementación robusta
3. **5 módulos internos** completamente testeados
4. **Workflow completo** de analysis → decomposition → task_graph → mission_map
5. **Compatibilidad total** con la arquitectura existente de Fase 1

---
*Implementation Plan Phase 2 - Strategy Architect Engine*  
*Fecha: 2025-06-20*  
*Estado: Listo para ejecución secuencial*  
*Basado en: Éxito de Fase 1 y metodología dogfooding validada*