#!/usr/bin/env python3
"""Extractor de plan para Fase 2.7 usando CortexMCP Strategy-Architect."""

from tools.strategy_architect import execute_architect_workflow
import json

def main():
    # Descripción detallada de la Fase 2.7
    task_description = """
    Implementar Fase 2.7: Collaborative Intelligence Enhancement

    OBJETIVO PRINCIPAL:
    Transformar el strategy-architect actual de un motor determinista monolítico a una plataforma de colaboración inteligente híbrida que permita a Claude participar activamente en el refinamiento estratégico en puntos críticos del análisis, manteniendo la fiabilidad determinística del proceso estructurado.

    CAPACIDADES A IMPLEMENTAR:
    1. Workflow interactivo multi-paso con puntos de inyección de inteligencia Claude
    2. Delegation pattern para refinamiento colaborativo del análisis preliminar  
    3. Nuevos action types: refine_analysis, validate_dependencies, optimize_assignment
    4. Actualización del Universal Response Schema para workflow colaborativo
    5. CLAUDE.md constitucional con filosofía de colaboración híbrida
    6. Compatibilidad 100% hacia atrás con funcionalidad actual

    CONTEXTO TÉCNICO:
    - Motor de Estrategias completamente funcional (4 fases operacionales)
    - Universal Response Schema implementado y validado 
    - Arquitectura stateless robusta establecida
    - Testing integral completado (100% compliance)

    PATRÓN OBJETIVO:
    Usuario → Claude → MCP(análisis preliminar) → Claude(refinement crítico) → MCP(workflow completo con análisis refinado)

    RESTRICCIONES:
    - Mantener compatibilidad total con API actual
    - Preservar performance (<1.5s response time)
    - Zero breaking changes en módulos existentes
    - Testing integral requerido para cada componente
    """
    
    print("🚀 EJECUTANDO MOTOR DE ESTRATEGIAS PARA PLANIFICAR FASE 2.7")
    print("=" * 70)
    
    # Ejecutar análisis estratégico completo
    result = execute_architect_workflow(task_description.strip())
    
    print("\n📋 PLAN ESTRATÉGICO GENERADO:")
    print("=" * 50)
    
    # Mostrar análisis
    if result.payload.analysis:
        analysis = result.payload.analysis
        print(f"\n🎯 ANÁLISIS DEL PROYECTO:")
        print(f"• Dominio: {analysis.domain or 'Software Architecture Evolution'}")
        print(f"• Complejidad: {analysis.complexity}")
        print(f"• Patrón arquitectónico: {analysis.architectural_pattern}")
        if analysis.technology_stack:
            print(f"• Stack tecnológico: {', '.join(analysis.technology_stack)}")
        if analysis.keywords:
            print(f"• Keywords clave: {', '.join(analysis.keywords[:5])}")
    
    # Mostrar descomposición en fases
    if result.payload.decomposition:
        decomp = result.payload.decomposition
        print(f"\n📊 PLAN DE EJECUCIÓN ({decomp.total_estimated_duration}):")
        for i, phase in enumerate(decomp.phases, 1):
            print(f"\n{i}. {phase.name} ({phase.estimated_duration})")
            print(f"   📝 {phase.description}")
            if phase.deliverables:
                print(f"   📦 Entregables:")
                for deliverable in phase.deliverables[:3]:
                    print(f"      - {deliverable}")
            if phase.dependencies:
                print(f"   🔗 Dependencias: {', '.join(phase.dependencies)}")
    
    # Mostrar tareas críticas
    if result.payload.task_graph:
        task_graph = result.payload.task_graph
        print(f"\n🎯 TAREAS CRÍTICAS (Total: {task_graph.task_count}):")
        for task in task_graph.tasks[:8]:  # Top 8 tareas
            priority_emoji = "🔴" if hasattr(task, 'priority') and task.priority == "Alta" else "🟡"
            print(f"   {priority_emoji} {task.name} ({task.estimated_duration})")
            if hasattr(task, 'description'):
                print(f"      → {task.description[:80]}...")
    
    # Mostrar asignaciones de recursos
    if result.payload.mission_map:
        mission = result.payload.mission_map
        print(f"\n👥 ASIGNACIÓN DE RECURSOS:")
        print(f"• Estimación total: {mission.total_effort_estimate}")
        
        # Agrupar por perfil de agente
        agent_tasks = {}
        for assignment in mission.resource_assignments:
            profile = assignment.agent_profile
            if profile not in agent_tasks:
                agent_tasks[profile] = []
            agent_tasks[profile].append(assignment)
        
        for profile, assignments in agent_tasks.items():
            print(f"\n   👤 {profile} ({len(assignments)} tareas):")
            for assignment in assignments[:3]:  # Top 3 por agente
                print(f"      • {assignment.task_id}")
                if hasattr(assignment, 'estimated_effort'):
                    print(f"        Esfuerzo: {assignment.estimated_effort}")
    
    # Mostrar metadatos
    print(f"\n📊 MÉTRICAS DEL PLAN:")
    print(f"• Confianza del análisis: {result.metadata.confidence_score:.1%}")
    print(f"• Complejidad evaluada: {result.metadata.complexity_score}/10")
    print(f"• Duración estimada: {result.metadata.estimated_duration}")
    
    if result.metadata.learning_opportunities:
        print(f"\n🎓 OPORTUNIDADES DE APRENDIZAJE:")
        for opportunity in result.metadata.learning_opportunities[:3]:
            print(f"   • {opportunity}")
    
    # Guardar plan completo en JSON
    plan_file = "phase27_strategic_plan.json"
    with open(plan_file, 'w', encoding='utf-8') as f:
        json.dump(result.model_dump(), f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Plan completo guardado en: {plan_file}")
    print("\n✅ ANÁLISIS ESTRATÉGICO COMPLETADO")
    print("=" * 70)

if __name__ == "__main__":
    main()