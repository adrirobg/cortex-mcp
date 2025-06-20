# Implementation Plan - Strategy Library MCP Server

## Estado Actual del Proyecto ✅

### Documentos Finalizados
- **projectBrief.md v2.2**: Arquitectura completa y validada con Universal Response Schema
- **CLAUDE.md**: Configurado con Poetry, comandos de desarrollo y guías de integración
- **Directrices de implementación**: 4 principios rectores fundamentales establecidos

### Decisiones Arquitectónicas Confirmadas
1. **Motor de Estrategias**: Endpoint único `strategy-architect` con funciones internas modulares
2. **Universal Response Schema**: Estructura StrategyResponse con Pydantic genérics
3. **Stateless Design**: Claude mantiene contexto, servidor sin estado
4. **Poetry**: Gestión de dependencias y entorno virtual

## Plan de Implementación: Simulación del Strategy-Architect

### Concepto Meta: "Dogfooding Arquitectónico"
**Idea central**: Usar el propio workflow del strategy-architect para planificar e implementar la Fase 1, validando nuestro diseño en tiempo real.

### Simulación del Workflow Completo

#### Etapa 1: Analysis (analyze_project_idea)
**Input**: "Implementar Fase 1 del Strategy Library MCP Server"

**Análisis Estructurado**:
```json
{
  "keywords": ["MCP", "Pydantic", "JSON-RPC", "Universal Response", "Poetry"],
  "patterns": ["Servidor MCP", "Schema validation", "stdio transport"],
  "complexity": "Media",
  "requirements_implicit": [
    "Testing concurrente",
    "Validación estricta Pydantic", 
    "Modularidad interna",
    "Conformidad con estándar MCP"
  ]
}
```

#### Etapa 2: Decomposition (decompose_to_phases)
**Fases Lógicas Identificadas**:
1. **Setup del Proyecto**: 
   - Configuración Poetry (pyproject.toml)
   - Estructura de directorios según projectBrief
   - Dependencias base (Pydantic, pytest, mypy, black, flake8)

2. **Core Schemas**: 
   - Universal Response Schema (StrategyResponse)
   - Architect-specific payloads
   - Tipos y validaciones

3. **Servidor Base**: 
   - JSON-RPC 2.0 implementación
   - stdio transport
   - Manejo de errores básico

4. **Tool Base**: 
   - Clase base para herramientas
   - Garantía de Universal Response
   - Estructura modular

5. **Testing Framework**: 
   - Tests unitarios para esquemas
   - Tests de integración para servidor
   - Validación de respuestas

#### Etapa 3: Task Graph (generate_task_graph)
**Grafo de Dependencias**:
```
Setup del Proyecto
    ↓
Core Schemas → Tool Base → Servidor Base
    ↓            ↓           ↓
    → Testing Framework ← ←
```

**Dependencias Críticas**:
- Setup debe completarse antes que cualquier implementación
- Schemas son base para Tool Base y Servidor
- Testing es concurrente con toda implementación

#### Etapa 4: Mission Map (create_mission_map)
**Asignación y Estrategia**:
- **Implementación secuencial** con testing paralelo
- **Validación Pydantic** en cada componente
- **Principios stateless** mantenidos en toda la arquitectura
- **Checkpoints de validación** después de cada fase

### Respuesta StrategyResponse Simulada

```json
{
  "strategy": {
    "name": "implement-phase-1-strategy-library-mcp",
    "version": "1.0.0",
    "type": "execution"
  },
  "user_facing": {
    "summary": "Plan de implementación para Fase 1 del Strategy Library MCP Server generado con 5 fases principales, estimación 2-3 días de desarrollo",
    "key_points": [
      "Setup Poetry y estructura de directorios según projectBrief",
      "Implementar Universal Response Schema con validación Pydantic estricta",
      "Crear servidor MCP base con JSON-RPC 2.0 y stdio transport",
      "Desarrollar clase base para herramientas garantizando respuesta universal",
      "Testing concurrente con desarrollo para validación continua"
    ],
    "next_steps": [
      "Crear pyproject.toml con dependencias necesarias",
      "Implementar estructura de directorios",
      "Desarrollar schemas/universal_response.py",
      "Crear tests básicos de validación"
    ]
  },
  "claude_instructions": {
    "execution_type": "multi_step",
    "actions": [
      {
        "type": "create_project_structure",
        "description": "Setup Poetry, pyproject.toml y directorios",
        "priority": 1,
        "validation_criteria": "poetry install ejecuta sin errores"
      },
      {
        "type": "implement_schemas",
        "description": "Universal Response Schema con Pydantic",
        "priority": 2,
        "validation_criteria": "Tests de schema pasan validación"
      },
      {
        "type": "create_base_server", 
        "description": "Servidor JSON-RPC con stdio",
        "priority": 3,
        "validation_criteria": "Servidor responde a tools/list"
      },
      {
        "type": "implement_base_tool",
        "description": "Clase base garantizando Universal Response",
        "priority": 4,
        "validation_criteria": "Tool base retorna StrategyResponse válido"
      }
    ],
    "context_requirements": {
      "required_info": [
        "Estructura exacta de directorios del projectBrief",
        "Dependencias Poetry necesarias",
        "Especificación completa del Universal Response Schema"
      ]
    }
  },
  "payload": {
    "workflow_stage": "ready_for_execution",
    "implementation_order": [
      "setup_project",
      "core_schemas", 
      "base_server",
      "base_tool",
      "testing_integration"
    ],
    "suggested_next_state": {
      "continue_workflow": true,
      "next_step": "create_project_structure",
      "context_to_maintain": {
        "architecture_decisions": "Motor de Estrategias + Universal Response",
        "principles": ["Stateless", "Pydantic validation", "Concurrent testing"],
        "target_structure": "Ver projectBrief.md estructura de directorios"
      }
    }
  },
  "metadata": {
    "confidence_score": 0.92,
    "complexity_score": 6,
    "estimated_duration": "2-3 días",
    "performance_hints": [
      "Implementar testing desde el primer componente",
      "Validar cada schema con ejemplos reales",
      "Usar tipos estrictos en toda la implementación"
    ],
    "learning_opportunities": [
      "Validación del diseño Universal Response en práctica",
      "Efectividad del patrón Motor de Estrategias",
      "Robustez del servidor stateless"
    ]
  }
}
```

## Próximos Pasos Inmediatos

### Fase 1.1: Setup del Proyecto
1. **Crear pyproject.toml** con configuración Poetry
2. **Establecer estructura de directorios** según projectBrief
3. **Configurar dependencias** (Pydantic, pytest, mypy, black, flake8)
4. **Verificar** que `poetry install` ejecuta sin errores

### Fase 1.2: Core Schemas
1. **Implementar** `schemas/universal_response.py` con StrategyResponse
2. **Crear** `schemas/architect_payloads.py` con tipos específicos
3. **Desarrollar** tests unitarios para validación de esquemas
4. **Validar** que todos los tipos funcionan correctamente

### Fase 1.3: Servidor Base
1. **Implementar** `server.py` con JSON-RPC 2.0
2. **Configurar** stdio transport
3. **Añadir** manejo básico de errores
4. **Verificar** respuesta a `tools/list`

### Fase 1.4: Tool Base
1. **Crear** `tools/base_tool.py` con clase base
2. **Garantizar** retorno de StrategyResponse válido
3. **Implementar** estructura modular
4. **Testing** de integración básico

## Principios Rectores Durante Implementación

### 1. Dogmatismo con Universal Response Schema
- **Validación estricta Pydantic** en toda salida
- **Sin excepciones** en formato de respuesta
- **Testing** de schema en cada componente

### 2. Servidor como Ejecutor Fiable
- **Heurísticas deterministas** no IA mágica
- **Funcionalidad sólida** antes que sofisticación
- **MVP pragmático** enfocado en valor

### 3. Estado en Claude, NO en Servidor
- **Servidor 100% stateless** sin almacenamiento entre llamadas
- **Claude mantiene contexto** usando suggested_next_state
- **Pureza funcional** en cada llamada

### 4. Testing Concurrente
- **Test unitario** para cada función implementada
- **Validación continua** durante desarrollo
- **Base sólida** antes de avanzar

## Estado Post-Compact

Después del compact, Claude debería:
1. **Leer projectBrief.md v2.2** para contexto arquitectónico completo
2. **Revisar CLAUDE.md** para comandos Poetry y estructura
3. **Seguir este implementationPlan.md** para ejecución paso a paso
4. **Aplicar la simulación del strategy-architect** como metodología

---
*Plan de implementación preservado antes del compact*  
*Fecha: 2025-06-20*  
*Estado: Listo para ejecución de Fase 1*