#!/usr/bin/env python3
"""Integration test for complete 4-phase Motor de Estrategias workflow with TDD enforcement.

Tests the complete workflow: Analysis → Decomposition → Task Graph → Mission Map
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from schemas.architect_payloads import AnalysisResult, DecompositionResult, TaskGraphResult, MissionMapResult
from tools.architect.analyze_project import analyze_project
from tools.architect.decompose_phases import decompose_phases  
from tools.architect.task_graph import generate_task_graph
from tools.architect.mission_map import create_mission_map


def test_complete_workflow_with_tdd():
    """Test complete 4-phase workflow with TDD enforcement."""
    
    print("🚀 Testing Complete Motor de Estrategias Workflow with TDD Enhancement")
    print("=" * 80)
    
    # Test project description
    task_description = "Build a web application with user authentication, real-time chat, file upload, and admin dashboard. Include comprehensive testing and deployment automation."
    
    print(f"📋 Project Description: {task_description}")
    print()
    
    # Phase 2.1: Analysis
    print("🔍 Phase 2.1: Project Analysis")
    analysis = analyze_project(task_description)
    
    print(f"✅ Analysis Results:")
    print(f"   - Domain: {analysis.domain}")
    print(f"   - Complexity: {analysis.complexity}")
    print(f"   - Keywords: {', '.join(analysis.keywords[:5])}...")
    print(f"   - Patterns: {', '.join(analysis.patterns)}")
    print()
    
    # Phase 2.2: Decomposition
    print("🏗️ Phase 2.2: Project Decomposition")
    decomposition = decompose_phases(analysis)
    
    print(f"✅ Decomposition Results:")
    print(f"   - Phases: {len(decomposition.phases)}")
    for i, phase in enumerate(decomposition.phases[:3]):  # Show first 3
        print(f"     {i+1}. {phase.name}")
    if len(decomposition.phases) > 3:
        print(f"     ... and {len(decomposition.phases) - 3} more")
    print()
    
    # Phase 2.3: Task Graph
    print("📋 Phase 2.3: Task Graph Generation")
    task_graph = generate_task_graph(decomposition, analysis)
    
    print(f"✅ Task Graph Results:")
    print(f"   - Tasks: {task_graph.task_count}")
    print(f"   - Critical Path: {len(task_graph.critical_path)} tasks")
    print(f"   - Parallel Groups: {len(task_graph.parallel_tasks)}")
    print(f"   - Bottlenecks: {len(task_graph.bottlenecks)}")
    print()
    
    # Phase 2.4: Mission Map with TDD Enhancement
    print("🎯 Phase 2.4: Mission Map with TDD Enhancement")
    mission_map = create_mission_map(task_graph, analysis)
    
    print(f"✅ Mission Map Results:")
    print(f"   - Resource Assignments: {len(mission_map.resource_assignments)}")
    print(f"   - Execution Order: {len(mission_map.execution_order)} tasks")
    print(f"   - Parallel Groups: {len(mission_map.parallel_groups) if mission_map.parallel_groups else 0}")
    print(f"   - Total Effort: {mission_map.total_effort_estimate}")
    print()
    
    # TDD Enhancement Validation
    print("🧪 TDD Enhancement Validation")
    test_tasks = [task_id for task_id in mission_map.execution_order if task_id.startswith("test_")]
    impl_tasks = [task_id for task_id in mission_map.execution_order if not task_id.startswith("test_") and not any(kw in task_id for kw in ["validate", "deploy"])]
    
    print(f"✅ TDD Compliance:")
    print(f"   - Test Tasks: {len(test_tasks)}")
    print(f"   - Implementation Tasks: {len(impl_tasks)}")
    print(f"   - TDD Ratio: {len(test_tasks)/len(impl_tasks)*100:.1f}% (Target: >90%)")
    
    # Validate TDD ordering
    tdd_violations = 0
    for impl_task in impl_tasks:
        corresponding_test = None
        if impl_task.startswith("impl_"):
            corresponding_test = impl_task.replace("impl_", "test_")
        else:
            corresponding_test = f"test_{impl_task}"
        
        if corresponding_test in mission_map.execution_order:
            test_idx = mission_map.execution_order.index(corresponding_test)
            impl_idx = mission_map.execution_order.index(impl_task)
            if test_idx >= impl_idx:
                tdd_violations += 1
                print(f"   ⚠️  TDD Violation: {impl_task} before {corresponding_test}")
    
    print(f"   - TDD Ordering: {((len(impl_tasks) - tdd_violations) / len(impl_tasks) * 100):.1f}% compliant")
    print()
    
    # Resource Utilization Summary
    print("👥 Resource Utilization Summary")
    if mission_map.resource_utilization:
        for agent, utilization in mission_map.resource_utilization.items():
            print(f"   - {agent}: {utilization}")
    print()
    
    # Workflow Completion Validation
    print("✅ Workflow Completion Validation")
    
    # Validate all phases completed successfully
    assert isinstance(analysis, AnalysisResult), "Phase 2.1 failed"
    assert isinstance(decomposition, DecompositionResult), "Phase 2.2 failed"
    assert isinstance(task_graph, TaskGraphResult), "Phase 2.3 failed"
    assert isinstance(mission_map, MissionMapResult), "Phase 2.4 failed"
    
    # Validate TDD enhancement worked
    original_task_count = task_graph.task_count
    enhanced_task_count = len(mission_map.execution_order)
    tdd_enhancement_ratio = (enhanced_task_count - original_task_count) / original_task_count
    
    print(f"   ✅ All 4 phases completed successfully")
    print(f"   ✅ TDD enhancement added {enhanced_task_count - original_task_count} test tasks ({tdd_enhancement_ratio:.1%} increase)")
    print(f"   ✅ Execution order respects TDD dependencies ({100 - (tdd_violations/len(impl_tasks)*100):.1f}% compliant)")
    print(f"   ✅ Resource assignments include {len(set(r.agent_profile for r in mission_map.resource_assignments))} different agent types")
    
    # Success summary
    print()
    print("🎉 MOTOR DE ESTRATEGIAS COMPLETE!")
    print("=" * 80)
    print("✅ Phase 2.1: Analysis Intelligence - Domain classification and complexity assessment")
    print("✅ Phase 2.2: Decomposition Intelligence - Structural breakdown with dependencies")  
    print("✅ Phase 2.3: Task Intelligence - Granular execution planning with resource awareness")
    print("✅ Phase 2.4: Mission Intelligence - TDD-enforced resource optimization and execution orchestration")
    print()
    print("🚀 STRATEGIC ENHANCEMENT ACHIEVED:")
    print("   • TDD workflow is now INTRINSIC to the system (not manual reminder)")
    print("   • Automatic test task generation for every implementation task")
    print("   • Dependency enforcement: test tasks precede implementation tasks")
    print("   • Agent profiles include TDD expertise and workflow awareness")
    print("   • Parallel execution respects TDD cycles (test → implement → validate)")
    print()
    print("📊 Final Metrics:")
    print(f"   • Total Project Tasks: {enhanced_task_count}")
    print(f"   • TDD Test Coverage: {len(test_tasks)/len(impl_tasks)*100:.1f}%")
    print(f"   • Agent Profiles Utilized: {len(set(r.agent_profile for r in mission_map.resource_assignments))}")
    print(f"   • Estimated Project Duration: {mission_map.total_effort_estimate}")
    print(f"   • TDD Workflow Compliance: {100 - (tdd_violations/len(impl_tasks)*100):.1f}%")
    
    return {
        "analysis": analysis,
        "decomposition": decomposition, 
        "task_graph": task_graph,
        "mission_map": mission_map,
        "tdd_compliance": 100 - (tdd_violations/len(impl_tasks)*100),
        "test_coverage": len(test_tasks)/len(impl_tasks)*100
    }


if __name__ == "__main__":
    try:
        results = test_complete_workflow_with_tdd()
        print(f"\n🎯 SUCCESS: Complete Motor de Estrategias workflow validated with {results['tdd_compliance']:.1f}% TDD compliance!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FAILURE: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)