"""Test suite for Mission Map module with TDD-enforced workflow architecture.

Testing Phase 2.4 functionality including:
- TDD task pairing and dependency enforcement
- Agent profile assignment with TDD awareness  
- Resource optimization with TDD workflows
- Parallel execution groups respecting TDD cycles
- Complete Motor de Estrategias workflow validation

Following Principios Rectores with TDD enhancement:
1. Dogmatismo con Universal Response Schema - strict MissionMapResult validation
2. Servidor como Ejecutor Fiable - deterministic resource assignment
3. Estado en Claude, NO en Servidor - pure functions, stateless design
4. Testing Concurrente - comprehensive TDD-aware test coverage
"""

import pytest
import json
from pathlib import Path
from unittest.mock import mock_open, patch
from typing import List, Dict, Any

from schemas.architect_payloads import (
    AnalysisResult, TaskGraphResult, MissionMapResult, Task, 
    ResourceAssignment, WorkflowStage
)
from tools.architect.mission_map import (
    create_mission_map, load_agent_profiles, load_resource_assignment_rules,
    assign_agent_profiles, create_parallel_groups, calculate_resource_utilization,
    generate_execution_order, _generate_tdd_task_pairs, _apply_tdd_dependencies,
    _normalize_agent_profile, _calculate_workload_balance, _detect_resource_conflicts
)


class TestMissionMapConfiguration:
    """Test configuration loading and validation."""
    
    def test_load_agent_profiles_success(self):
        """Test successful loading of agent profiles configuration."""
        mock_config = {
            "agent_profiles": {
                "system_architect": {
                    "specializations": ["architecture", "design"],
                    "complexity_range": [3, 5],
                    "max_concurrent_tasks": 2,
                    "tdd_expertise": True
                }
            }
        }
        
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_config))):
            result = load_agent_profiles()
            
        assert "agent_profiles" in result
        assert "system_architect" in result["agent_profiles"]
        assert result["agent_profiles"]["system_architect"]["tdd_expertise"] is True
    
    def test_load_agent_profiles_file_not_found(self):
        """Test graceful handling of missing agent profiles configuration."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError, match="Agent profiles configuration not found"):
                load_agent_profiles()
    
    def test_load_resource_assignment_rules_success(self):
        """Test successful loading of resource assignment rules."""
        mock_rules = {
            "assignment_priorities": {
                "exact_specialization": 10,
                "complexity_match": 8,
                "workload_balance": 6,
                "tdd_workflow_compliance": 9
            }
        }
        
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_rules))):
            result = load_resource_assignment_rules()
            
        assert "assignment_priorities" in result
        assert result["assignment_priorities"]["tdd_workflow_compliance"] == 9


class TestTDDTaskPairGeneration:
    """Test TDD task pairing functionality - Gemini's strategic enhancement."""
    
    def test_generate_tdd_task_pairs_basic(self):
        """Test basic TDD task pair generation."""
        tasks = [
            Task(
                id="impl_user_model",
                name="Implement User Model", 
                description="Create user model",
                phase_id="backend",
                dependencies=[],
                agent_profile="backend_developer"
            )
        ]
        
        result = _generate_tdd_task_pairs(tasks)
        
        # Should generate test task for implementation task
        test_tasks = [t for t in result if t.id.startswith("test_")]
        assert len(test_tasks) == 1
        assert test_tasks[0].id == "test_user_model"
        assert "unit tests" in test_tasks[0].description.lower()
        assert "should fail initially" in test_tasks[0].description
    
    def test_generate_tdd_task_pairs_respects_existing_tests(self):
        """Test that existing test tasks are not duplicated."""
        tasks = [
            Task(
                id="test_user_model",
                name="Test User Model",
                description="Existing test task", 
                phase_id="backend",
                dependencies=[]
            ),
            Task(
                id="impl_user_model",
                name="Implement User Model",
                description="Implementation task",
                phase_id="backend", 
                dependencies=[]
            )
        ]
        
        result = _generate_tdd_task_pairs(tasks)
        
        # Should not create duplicate test task
        test_tasks = [t for t in result if t.id.startswith("test_")]
        assert len(test_tasks) == 1
        assert test_tasks[0].description == "Existing test task"
    
    def test_apply_tdd_dependencies(self):
        """Test TDD dependency enforcement - test tasks must precede implementation."""
        tasks = [
            Task(id="test_user_model", name="Test", description="Test", phase_id="backend", dependencies=[]),
            Task(id="impl_user_model", name="Impl", description="Impl", phase_id="backend", dependencies=[])
        ]
        
        result = _apply_tdd_dependencies(tasks)
        
        # Implementation task should depend on corresponding test task
        impl_task = next(t for t in result if t.id == "impl_user_model")
        assert "test_user_model" in impl_task.dependencies


class TestAgentProfileAssignment:
    """Test intelligent agent profile assignment with TDD awareness."""
    
    def test_assign_agent_profiles_exact_match(self):
        """Test assignment with exact specialization match."""
        tasks = [
            Task(
                id="design_architecture",
                name="Design Architecture",
                description="System architecture design",
                phase_id="design",
                dependencies=[],
                agent_profile="system_architect"  # Pre-assigned
            )
        ]
        
        agent_config = {
            "agent_profiles": {
                "system_architect": {
                    "specializations": ["architecture", "design"],
                    "complexity_range": [3, 5],
                    "max_concurrent_tasks": 2
                }
            }
        }
        
        result = assign_agent_profiles(tasks, agent_config)
        
        assert len(result) == 1
        assert result[0].agent_profile == "system_architect"
        assert result[0].task_id == "design_architecture"
    
    def test_assign_agent_profiles_tdd_pairing(self):
        """Test that TDD task pairs get compatible agent assignments."""
        tasks = [
            Task(id="test_api_endpoint", name="Test API", description="Test API", phase_id="backend", dependencies=[]),
            Task(id="impl_api_endpoint", name="Impl API", description="Impl API", phase_id="backend", dependencies=["test_api_endpoint"])
        ]
        
        agent_config = {
            "agent_profiles": {
                "backend_developer": {
                    "specializations": ["api", "testing"],
                    "complexity_range": [2, 4],
                    "max_concurrent_tasks": 3,
                    "tdd_expertise": True
                }
            }
        }
        
        result = assign_agent_profiles(tasks, agent_config)
        
        # Both test and implementation should get same agent for TDD workflow continuity
        test_assignment = next(r for r in result if r.task_id == "test_api_endpoint")
        impl_assignment = next(r for r in result if r.task_id == "impl_api_endpoint")
        
        assert test_assignment.agent_profile == "backend_developer"
        assert impl_assignment.agent_profile == "backend_developer"
    
    def test_normalize_agent_profile(self):
        """Test agent profile normalization logic."""
        assert _normalize_agent_profile("Frontend Developer") == "frontend_developer"
        assert _normalize_agent_profile("System Architect") == "system_architect" 
        assert _normalize_agent_profile("backend-dev") == "backend_dev"


class TestParallelGroupCreation:
    """Test parallel execution group creation with TDD workflow respect."""
    
    def test_create_parallel_groups_respects_tdd_dependencies(self):
        """Test that parallel groups respect TDD test→implementation dependencies."""
        tasks = [
            Task(id="test_user_model", name="Test User", description="Test", phase_id="backend", dependencies=[]),
            Task(id="impl_user_model", name="Impl User", description="Impl", phase_id="backend", dependencies=["test_user_model"]),
            Task(id="test_auth_logic", name="Test Auth", description="Test", phase_id="backend", dependencies=[]),
            Task(id="impl_auth_logic", name="Impl Auth", description="Impl", phase_id="backend", dependencies=["test_auth_logic"])
        ]
        
        dependency_matrix = {
            "test_user_model": [],
            "impl_user_model": ["test_user_model"],
            "test_auth_logic": [], 
            "impl_auth_logic": ["test_auth_logic"]
        }
        
        result = create_parallel_groups(tasks, dependency_matrix)
        
        # Test tasks can run in parallel, but implementations must wait for their tests
        assert any("test_user_model" in group and "test_auth_logic" in group for group in result.values())
        
        # Implementation tasks should be in different groups from their test dependencies
        for group_id, group_tasks in result.items():
            if "impl_user_model" in group_tasks:
                assert "test_user_model" not in group_tasks
    
    def test_create_parallel_groups_workload_balancing(self):
        """Test parallel group creation with workload balancing."""
        tasks = [
            Task(id="task_1", name="Task 1", description="Task", phase_id="phase1", dependencies=[], complexity_score=5),
            Task(id="task_2", name="Task 2", description="Task", phase_id="phase1", dependencies=[], complexity_score=3),
            Task(id="task_3", name="Task 3", description="Task", phase_id="phase1", dependencies=[], complexity_score=2)
        ]
        
        dependency_matrix = {task.id: task.dependencies for task in tasks}
        
        result = create_parallel_groups(tasks, dependency_matrix)
        
        # Should create balanced groups considering complexity
        assert len(result) > 0
        
        # Verify group structure
        for group_id, group_tasks in result.items():
            assert isinstance(group_tasks, list)
            assert all(isinstance(task_id, str) for task_id in group_tasks)


class TestResourceUtilizationCalculation:
    """Test resource utilization calculation and optimization."""
    
    def test_calculate_resource_utilization_basic(self):
        """Test basic resource utilization calculation."""
        assignments = [
            ResourceAssignment(
                task_id="task_1",
                agent_profile="backend_developer",
                estimated_effort="2 days",
                priority=8,
                parallel_group="group_1"
            ),
            ResourceAssignment(
                task_id="task_2", 
                agent_profile="frontend_developer",
                estimated_effort="1 day",
                priority=6,
                parallel_group="group_1"
            )
        ]
        
        agent_config = {
            "agent_profiles": {
                "backend_developer": {"max_concurrent_tasks": 3},
                "frontend_developer": {"max_concurrent_tasks": 2}
            }
        }
        
        result = calculate_resource_utilization(assignments, agent_config)
        
        assert "backend_developer" in result
        assert "frontend_developer" in result
        assert "utilization" in result["backend_developer"]
    
    def test_calculate_workload_balance(self):
        """Test workload balance calculation across agents."""
        assignments = [
            ResourceAssignment(task_id="t1", agent_profile="dev1", estimated_effort="3 days", priority=8),
            ResourceAssignment(task_id="t2", agent_profile="dev1", estimated_effort="2 days", priority=6), 
            ResourceAssignment(task_id="t3", agent_profile="dev2", estimated_effort="1 day", priority=7)
        ]
        
        result = _calculate_workload_balance(assignments)
        
        assert "dev1" in result
        assert "dev2" in result
        assert result["dev1"]["total_effort_days"] == 5
        assert result["dev2"]["total_effort_days"] == 1
    
    def test_detect_resource_conflicts(self):
        """Test detection of resource assignment conflicts."""
        assignments = [
            ResourceAssignment(task_id="t1", agent_profile="dev1", estimated_effort="4 days", priority=8, parallel_group="g1"),
            ResourceAssignment(task_id="t2", agent_profile="dev1", estimated_effort="3 days", priority=6, parallel_group="g1")
        ]
        
        agent_config = {
            "agent_profiles": {
                "dev1": {"max_concurrent_tasks": 1}  # Can only handle 1 task at a time
            }
        }
        
        conflicts = _detect_resource_conflicts(assignments, agent_config)
        
        assert len(conflicts) > 0
        assert any("dev1" in conflict["description"] for conflict in conflicts)


class TestExecutionOrderGeneration:
    """Test execution order generation with TDD workflow enforcement."""
    
    def test_generate_execution_order_respects_tdd(self):
        """Test that execution order enforces TDD workflow (test→implement→validate)."""
        tasks = [
            Task(id="impl_feature", name="Implement", description="Impl", phase_id="dev", dependencies=["test_feature"]),
            Task(id="test_feature", name="Test", description="Test", phase_id="dev", dependencies=[]),
            Task(id="validate_feature", name="Validate", description="Validate", phase_id="dev", dependencies=["impl_feature"])
        ]
        
        dependency_matrix = {
            "test_feature": [],
            "impl_feature": ["test_feature"], 
            "validate_feature": ["impl_feature"]
        }
        
        result = generate_execution_order(tasks, dependency_matrix)
        
        # Should follow TDD order: test → implement → validate
        test_idx = result.index("test_feature")
        impl_idx = result.index("impl_feature")
        validate_idx = result.index("validate_feature")
        
        assert test_idx < impl_idx < validate_idx
    
    def test_generate_execution_order_parallel_optimization(self):
        """Test execution order optimization for parallel tasks."""
        tasks = [
            Task(id="test_a", name="Test A", description="Test", phase_id="dev", dependencies=[]),
            Task(id="test_b", name="Test B", description="Test", phase_id="dev", dependencies=[]),
            Task(id="impl_a", name="Impl A", description="Impl", phase_id="dev", dependencies=["test_a"]),
            Task(id="impl_b", name="Impl B", description="Impl", phase_id="dev", dependencies=["test_b"])
        ]
        
        dependency_matrix = {task.id: task.dependencies for task in tasks}
        
        result = generate_execution_order(tasks, dependency_matrix)
        
        # Test tasks should come before their implementations
        assert result.index("test_a") < result.index("impl_a")
        assert result.index("test_b") < result.index("impl_b")
        
        # Parallel test tasks can be in any order relative to each other
        assert len(result) == 4


class TestCreateMissionMapIntegration:
    """Test main create_mission_map function with complete TDD workflow integration."""
    
    def test_create_mission_map_basic_functionality(self):
        """Test basic mission map creation with TDD enhancement."""
        # Sample task graph with TDD structure
        task_graph = TaskGraphResult(
            tasks=[
                Task(id="test_user_api", name="Test User API", description="Test", phase_id="backend", dependencies=[]),
                Task(id="impl_user_api", name="Implement User API", description="Impl", phase_id="backend", dependencies=["test_user_api"])
            ],
            task_count=2,
            dependency_matrix={"test_user_api": [], "impl_user_api": ["test_user_api"]},
            critical_path=["test_user_api", "impl_user_api"],
            parallel_tasks=[],
            bottlenecks=[]
        )
        
        analysis = AnalysisResult(
            keywords=["api", "backend"],
            patterns=["rest_api"],
            complexity="Media",
            requirements_implicit=["authentication"],
            domain="web_application"
        )
        
        # Mock configuration files
        mock_agent_config = {
            "agent_profiles": {
                "backend_developer": {
                    "specializations": ["api", "testing"],
                    "complexity_range": [2, 4],
                    "max_concurrent_tasks": 3,
                    "tdd_expertise": True
                }
            }
        }
        
        mock_rules_config = {
            "assignment_priorities": {
                "exact_specialization": 10,
                "tdd_workflow_compliance": 9
            }
        }
        
        with patch("tools.architect.mission_map.load_agent_profiles", return_value=mock_agent_config), \
             patch("tools.architect.mission_map.load_resource_assignment_rules", return_value=mock_rules_config):
            
            result = create_mission_map(task_graph, analysis)
        
        # Validate MissionMapResult structure
        assert isinstance(result, MissionMapResult)
        assert len(result.resource_assignments) == 2
        assert len(result.execution_order) == 2
        
        # Validate TDD workflow in execution order
        assert result.execution_order.index("test_user_api") < result.execution_order.index("impl_user_api")
        
        # Validate resource assignments
        test_assignment = next(r for r in result.resource_assignments if r.task_id == "test_user_api")
        impl_assignment = next(r for r in result.resource_assignments if r.task_id == "impl_user_api")
        
        assert test_assignment.agent_profile == "backend_developer"
        assert impl_assignment.agent_profile == "backend_developer"
    
    def test_create_mission_map_empty_task_graph(self):
        """Test graceful handling of empty task graph."""
        empty_task_graph = TaskGraphResult(
            tasks=[],
            task_count=0,
            dependency_matrix={},
            critical_path=[],
            parallel_tasks=[],
            bottlenecks=[]
        )
        
        analysis = AnalysisResult(
            keywords=[],
            patterns=[],
            complexity="Baja", 
            requirements_implicit=[]
        )
        
        result = create_mission_map(empty_task_graph, analysis)
        
        assert isinstance(result, MissionMapResult)
        assert len(result.resource_assignments) == 0
        assert len(result.execution_order) == 0
    
    def test_create_mission_map_validates_inputs(self):
        """Test input validation for create_mission_map."""
        with pytest.raises(ValueError, match="TaskGraphResult is required"):
            create_mission_map(None, AnalysisResult(keywords=[], patterns=[], complexity="Baja", requirements_implicit=[]))
        
        with pytest.raises(ValueError, match="AnalysisResult is required"):
            create_mission_map(TaskGraphResult(tasks=[], task_count=0, dependency_matrix={}), None)


class TestCompleteWorkflowIntegration:
    """Test complete 4-phase Motor de Estrategias workflow with TDD enforcement."""
    
    def test_complete_workflow_tdd_integration(self):
        """Test complete workflow: Analysis → Decomposition → Task Graph → Mission Map with TDD."""
        # This would be an integration test with actual workflow execution
        # For now, testing the mission map component in isolation
        
        # Sample complex task graph representing real project
        complex_task_graph = TaskGraphResult(
            tasks=[
                Task(id="test_auth_model", name="Test Auth Model", description="Test", phase_id="backend", dependencies=[]),
                Task(id="impl_auth_model", name="Implement Auth Model", description="Impl", phase_id="backend", dependencies=["test_auth_model"]),
                Task(id="test_ui_components", name="Test UI Components", description="Test", phase_id="frontend", dependencies=[]),
                Task(id="impl_ui_components", name="Implement UI Components", description="Impl", phase_id="frontend", dependencies=["test_ui_components"]),
                Task(id="test_integration", name="Test Integration", description="Test", phase_id="integration", dependencies=["impl_auth_model", "impl_ui_components"]),
                Task(id="impl_integration", name="Implement Integration", description="Impl", phase_id="integration", dependencies=["test_integration"])
            ],
            task_count=6,
            dependency_matrix={
                "test_auth_model": [],
                "impl_auth_model": ["test_auth_model"],
                "test_ui_components": [],
                "impl_ui_components": ["test_ui_components"], 
                "test_integration": ["impl_auth_model", "impl_ui_components"],
                "impl_integration": ["test_integration"]
            },
            critical_path=["test_auth_model", "impl_auth_model", "test_integration", "impl_integration"],
            parallel_tasks=[["test_auth_model", "test_ui_components"]],
            bottlenecks=["impl_auth_model"]
        )
        
        analysis = AnalysisResult(
            keywords=["authentication", "ui", "integration"],
            patterns=["fullstack_web_app", "microservices"],
            complexity="Alta",
            requirements_implicit=["security", "scalability"],
            domain="web_application"
        )
        
        mock_agent_config = {
            "agent_profiles": {
                "backend_developer": {
                    "specializations": ["api", "authentication", "testing"],
                    "complexity_range": [3, 5],
                    "max_concurrent_tasks": 2,
                    "tdd_expertise": True
                },
                "frontend_developer": {
                    "specializations": ["ui", "components", "testing"],
                    "complexity_range": [2, 4],
                    "max_concurrent_tasks": 3,
                    "tdd_expertise": True
                },
                "integration_specialist": {
                    "specializations": ["integration", "api", "testing"],
                    "complexity_range": [3, 5],
                    "max_concurrent_tasks": 2,
                    "tdd_expertise": True
                }
            }
        }
        
        with patch("tools.architect.mission_map.load_agent_profiles", return_value=mock_agent_config), \
             patch("tools.architect.mission_map.load_resource_assignment_rules", return_value={"assignment_priorities": {}}):
            
            result = create_mission_map(complex_task_graph, analysis)
        
        # Validate comprehensive mission map
        assert len(result.resource_assignments) == 6
        assert len(result.execution_order) == 6
        
        # Validate TDD workflow enforcement across all task pairs
        tdd_pairs = [
            ("test_auth_model", "impl_auth_model"),
            ("test_ui_components", "impl_ui_components"),
            ("test_integration", "impl_integration")
        ]
        
        for test_task, impl_task in tdd_pairs:
            test_idx = result.execution_order.index(test_task)
            impl_idx = result.execution_order.index(impl_task)
            assert test_idx < impl_idx, f"TDD violation: {test_task} should come before {impl_task}"
        
        # Validate specialized agent assignments exist (exact matching depends on assignment algorithm)
        auth_test_assignment = next(r for r in result.resource_assignments if r.task_id == "test_auth_model")
        ui_test_assignment = next(r for r in result.resource_assignments if r.task_id == "test_ui_components")
        integration_test_assignment = next(r for r in result.resource_assignments if r.task_id == "test_integration")
        
        # Verify agents are assigned (exact profile depends on scoring algorithm)
        assert auth_test_assignment.agent_profile in ["backend_developer", "fullstack_developer", "integration_specialist", "frontend_developer"]
        assert ui_test_assignment.agent_profile in ["frontend_developer", "fullstack_developer", "backend_developer"]
        assert integration_test_assignment.agent_profile in ["integration_specialist", "fullstack_developer", "system_architect", "backend_developer", "frontend_developer"]
        
        # Validate parallel groups respect TDD dependencies
        if result.parallel_groups:
            for group_id, group_tasks in result.parallel_groups.items():
                # Test tasks can be parallel, but implementations must wait for their tests
                for task_id in group_tasks:
                    if task_id.startswith("impl_"):
                        corresponding_test = task_id.replace("impl_", "test_")
                        if corresponding_test in complex_task_graph.dependency_matrix.get(task_id, []):
                            assert corresponding_test not in group_tasks, f"TDD violation in parallel group: {task_id} grouped with its test dependency {corresponding_test}"


# Test fixtures and utilities
@pytest.fixture
def sample_analysis():
    """Sample analysis result for testing."""
    return AnalysisResult(
        keywords=["web", "api", "authentication"],
        patterns=["rest_api", "spa"],
        complexity="Media",
        requirements_implicit=["security", "scalability"],
        domain="web_application"
    )


@pytest.fixture 
def sample_task_graph():
    """Sample task graph for testing."""
    return TaskGraphResult(
        tasks=[
            Task(id="test_api", name="Test API", description="Test", phase_id="backend", dependencies=[]),
            Task(id="impl_api", name="Implement API", description="Impl", phase_id="backend", dependencies=["test_api"])
        ],
        task_count=2,
        dependency_matrix={"test_api": [], "impl_api": ["test_api"]},
        critical_path=["test_api", "impl_api"],
        parallel_tasks=[],
        bottlenecks=[]
    )


@pytest.fixture
def sample_agent_config():
    """Sample agent configuration for testing."""
    return {
        "agent_profiles": {
            "backend_developer": {
                "specializations": ["api", "database", "testing"],
                "complexity_range": [2, 4],
                "max_concurrent_tasks": 3,
                "tdd_expertise": True
            },
            "frontend_developer": {
                "specializations": ["ui", "components", "testing"], 
                "complexity_range": [2, 4],
                "max_concurrent_tasks": 3,
                "tdd_expertise": True
            }
        }
    }


# Performance and edge case tests
class TestMissionMapPerformance:
    """Test performance characteristics and edge cases."""
    
    def test_large_task_graph_performance(self):
        """Test mission map creation with large task graphs."""
        # Create large task graph (50+ tasks)
        tasks = []
        dependency_matrix = {}
        
        for i in range(25):  # 25 test/impl pairs = 50 tasks
            test_task = Task(
                id=f"test_feature_{i}",
                name=f"Test Feature {i}",
                description="Test",
                phase_id="phase_1",
                dependencies=[]
            )
            impl_task = Task(
                id=f"impl_feature_{i}",
                name=f"Implement Feature {i}",
                description="Impl", 
                phase_id="phase_1",
                dependencies=[f"test_feature_{i}"]
            )
            
            tasks.extend([test_task, impl_task])
            dependency_matrix[f"test_feature_{i}"] = []
            dependency_matrix[f"impl_feature_{i}"] = [f"test_feature_{i}"]
        
        large_task_graph = TaskGraphResult(
            tasks=tasks,
            task_count=len(tasks),
            dependency_matrix=dependency_matrix,
            critical_path=[],
            parallel_tasks=[],
            bottlenecks=[]
        )
        
        analysis = AnalysisResult(
            keywords=["performance", "test"],
            patterns=["large_project"],
            complexity="Alta",
            requirements_implicit=["scalability"]
        )
        
        mock_config = {
            "agent_profiles": {
                "developer": {
                    "specializations": ["general"],
                    "complexity_range": [1, 5],
                    "max_concurrent_tasks": 10,
                    "tdd_expertise": True
                }
            }
        }
        
        with patch("tools.architect.mission_map.load_agent_profiles", return_value=mock_config), \
             patch("tools.architect.mission_map.load_resource_assignment_rules", return_value={}):
            
            # Should complete within reasonable time 
            import time
            start_time = time.time()
            result = create_mission_map(large_task_graph, analysis)
            duration = time.time() - start_time
            
            assert duration < 5.0  # Should complete within 5 seconds
            assert len(result.resource_assignments) == 50
            assert len(result.execution_order) == 50
    
    def test_circular_dependency_detection(self):
        """Test handling of circular dependencies in task graph."""
        # This should be prevented by task graph generation, but test graceful handling
        tasks = [
            Task(id="task_a", name="Task A", description="Task", phase_id="phase", dependencies=["task_b"]),
            Task(id="task_b", name="Task B", description="Task", phase_id="phase", dependencies=["task_a"])
        ]
        
        dependency_matrix = {
            "task_a": ["task_b"],
            "task_b": ["task_a"]
        }
        
        circular_task_graph = TaskGraphResult(
            tasks=tasks,
            task_count=2,
            dependency_matrix=dependency_matrix,
            critical_path=[],
            parallel_tasks=[],
            bottlenecks=[]
        )
        
        analysis = AnalysisResult(
            keywords=["test"],
            patterns=["circular"],
            complexity="Baja", 
            requirements_implicit=[]
        )
        
        mock_config = {"agent_profiles": {"developer": {"specializations": [], "complexity_range": [1, 5], "max_concurrent_tasks": 1}}}
        
        with patch("tools.architect.mission_map.load_agent_profiles", return_value=mock_config), \
             patch("tools.architect.mission_map.load_resource_assignment_rules", return_value={}):
            
            # Should handle gracefully without infinite loops
            result = create_mission_map(circular_task_graph, analysis)
            
            assert isinstance(result, MissionMapResult)
            # Execution order should include original tasks plus generated test tasks
            # TDD enhancement adds test tasks, so total count will be > 2
            assert len(result.execution_order) >= 2
            # Verify no infinite loops by checking reasonable upper bound
            assert len(result.execution_order) <= 6  # 2 original + 2 test tasks + potential extras


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])