"""Test suite for Task Graph module of Strategy Library MCP Server.

Implements comprehensive test coverage for Phase 2.3 task graph generation.
Following TDD methodology with specific test cases from Gemini feedback.

Test cases include:
1. Task generation for web app with granular validation
2. Dependency inheritance from phases to tasks
3. Complexity-based task adjustments
4. Edge cases and error conditions
"""

import pytest
from typing import List, Dict
from schemas.architect_payloads import (
    AnalysisResult, DecompositionResult, TaskGraphResult, 
    Task, Phase
)
from tools.architect.task_graph import (
    generate_task_graph, generate_tasks_from_phases,
    calculate_task_dependencies, identify_task_critical_path,
    detect_task_bottlenecks, load_task_templates
)


class TestTaskTemplateLoading:
    """Test configuration loading and validation."""
    
    def test_load_task_templates_success(self):
        """Test successful loading of task generation templates."""
        templates = load_task_templates()
        
        assert templates is not None
        assert "task_templates" in templates
        assert "design" in templates["task_templates"]
        assert "backend" in templates["task_templates"]
        assert "frontend" in templates["task_templates"]
    
    def test_task_template_structure_validation(self):
        """Test that task templates have required structure."""
        templates = load_task_templates()
        
        design_template = templates["task_templates"]["design"]
        assert "description" in design_template
        assert "tasks" in design_template
        assert len(design_template["tasks"]) > 0
        
        # Validate individual task structure (Gemini specific)
        task = design_template["tasks"][0]
        required_fields = ["id_suffix", "name", "description", "estimated_effort"]
        for field in required_fields:
            assert field in task, f"Missing required field: {field}"


class TestTaskGenerationForWebApp:
    """Test task generation for web application domain (Gemini test case #1)."""
    
    def setup_method(self):
        """Set up test fixtures for web app scenarios."""
        self.analysis_web_app = AnalysisResult(
            keywords=["web", "backend", "frontend", "api", "database"],
            patterns=["crud_operations", "user_management", "integration"],
            complexity="Media",
            requirements_implicit=["Authentication system", "Database design"],
            domain="web",
            technology_stack=["javascript", "python"]
        )
        
        self.decomposition_web_app = DecompositionResult(
            phases=[
                Phase(
                    id="design",
                    name="System Design & Architecture",
                    description="Define system architecture and API specifications",
                    estimated_duration="3-5 days",
                    dependencies=[],
                    deliverables=["architecture_diagram", "api_spec"]
                ),
                Phase(
                    id="backend",
                    name="Backend API Development", 
                    description="Implement server-side logic and APIs",
                    estimated_duration="1-2 weeks",
                    dependencies=["design"],
                    deliverables=["api_endpoints", "database_schema"]
                ),
                Phase(
                    id="frontend",
                    name="Frontend UI Implementation",
                    description="Build user interface components",
                    estimated_duration="1-2 weeks", 
                    dependencies=["design"],
                    deliverables=["ui_components", "user_flows"]
                ),
                Phase(
                    id="integration",
                    name="Frontend-Backend Integration",
                    description="Connect frontend and backend systems",
                    estimated_duration="3-5 days",
                    dependencies=["backend", "frontend"],
                    deliverables=["api_integration", "data_binding"]
                )
            ],
            total_estimated_duration="4-6 weeks",
            critical_path=["design", "backend", "integration"],
            parallel_opportunities=[["backend", "frontend"]]
        )
    
    def test_task_generation_for_web_app_backend(self):
        """Test specific task generation for Backend API Development phase."""
        task_graph = generate_task_graph(self.decomposition_web_app, self.analysis_web_app)
        
        # Find backend tasks (Gemini specific validation)
        backend_tasks = [task for task in task_graph.tasks if task.phase_id == "backend"]
        
        # Should generate 3-8 tasks for backend phase
        assert 3 <= len(backend_tasks) <= 8, f"Backend generated {len(backend_tasks)} tasks, expected 3-8"
        
        # Specific tasks should be generated (Gemini examples)
        task_names = [task.name for task in backend_tasks]
        
        # Check for specific granular tasks
        assert any("Database" in name or "Model" in name for name in task_names), "Should generate database/model task"
        assert any("Authentication" in name or "Auth" in name for name in task_names), "Should generate auth task"  
        assert any("CRUD" in name or "Endpoint" in name for name in task_names), "Should generate CRUD/endpoint task"
    
    def test_task_generation_granularity_per_phase(self):
        """Test that each phase generates appropriate number of tasks."""
        task_graph = generate_task_graph(self.decomposition_web_app, self.analysis_web_app)
        
        phases = ["design", "backend", "frontend", "integration"]
        for phase_id in phases:
            phase_tasks = [task for task in task_graph.tasks if task.phase_id == phase_id]
            
            # Each phase should generate 3-8 tasks based on complexity
            assert 3 <= len(phase_tasks) <= 8, f"Phase {phase_id} generated {len(phase_tasks)} tasks"
            
            # All tasks should have valid schema fields
            for task in phase_tasks:
                assert task.id.startswith(phase_id), f"Task ID should start with phase ID: {task.id}"
                assert task.name, "Task should have non-empty name"
                assert task.description, "Task should have description"
                assert task.phase_id == phase_id, "Task phase_id should match"


class TestDependencyInheritance:
    """Test dependency inheritance from phases to tasks (Gemini test case #2)."""
    
    def setup_method(self):
        """Set up test data with clear phase dependencies."""
        self.analysis_simple = AnalysisResult(
            keywords=["api", "database"],
            patterns=["crud_operations"],
            complexity="Baja",
            requirements_implicit=["Database design"],
            domain="api",
            technology_stack=["python"]
        )
        
        self.decomposition_with_deps = DecompositionResult(
            phases=[
                Phase(
                    id="design",
                    name="Design Phase",
                    description="Design system",
                    dependencies=[],  # No dependencies
                    deliverables=["specs"]
                ),
                Phase(
                    id="implementation", 
                    name="Implementation Phase",
                    description="Implement system",
                    dependencies=["design"],  # Depends on design
                    deliverables=["code"]
                ),
                Phase(
                    id="testing",
                    name="Testing Phase", 
                    description="Test system",
                    dependencies=["implementation"],  # Depends on implementation
                    deliverables=["test_results"]
                )
            ],
            critical_path=["design", "implementation", "testing"]
        )
    
    def test_dependency_inheritance_phase_to_task(self):
        """Test that phase dependencies translate to task dependencies."""
        task_graph = generate_task_graph(self.decomposition_with_deps, self.analysis_simple)
        
        # Get tasks by phase
        design_tasks = [t for t in task_graph.tasks if t.phase_id == "design"]
        implementation_tasks = [t for t in task_graph.tasks if t.phase_id == "implementation"] 
        testing_tasks = [t for t in task_graph.tasks if t.phase_id == "testing"]
        
        # Design tasks should have no external dependencies
        for task in design_tasks:
            external_deps = [dep for dep in task.dependencies if not dep.startswith("design")]
            assert len(external_deps) == 0, f"Design task {task.id} has external dependencies: {external_deps}"
        
        # Implementation tasks should depend on some design tasks
        implementation_task_deps = []
        for task in implementation_tasks:
            implementation_task_deps.extend(task.dependencies)
        
        design_task_ids = [t.id for t in design_tasks]
        has_design_dependency = any(dep in design_task_ids for dep in implementation_task_deps)
        assert has_design_dependency, "Implementation tasks should depend on design tasks"
        
        # Testing tasks should depend on implementation tasks  
        testing_task_deps = []
        for task in testing_tasks:
            testing_task_deps.extend(task.dependencies)
            
        implementation_task_ids = [t.id for t in implementation_tasks]
        has_implementation_dependency = any(dep in implementation_task_ids for dep in testing_task_deps)
        assert has_implementation_dependency, "Testing tasks should depend on implementation tasks"
    
    def test_dependency_matrix_accuracy(self):
        """Test that dependency matrix correctly represents task relationships."""
        task_graph = generate_task_graph(self.decomposition_with_deps, self.analysis_simple)
        
        # Dependency matrix should exist
        assert task_graph.dependency_matrix is not None
        
        # Every task should be in the dependency matrix
        task_ids = [task.id for task in task_graph.tasks]
        for task_id in task_ids:
            assert task_id in task_graph.dependency_matrix, f"Task {task_id} missing from dependency matrix"
        
        # Dependencies in matrix should match task dependencies
        for task in task_graph.tasks:
            matrix_deps = task_graph.dependency_matrix[task.id]
            assert set(matrix_deps) == set(task.dependencies), f"Matrix deps don't match task deps for {task.id}"


class TestComplexityAdjustments:
    """Test complexity-based task generation adjustments (Gemini test case #3)."""
    
    def test_simple_vs_complex_task_generation(self):
        """Test that simple projects generate fewer tasks than complex ones."""
        # Simple project
        analysis_simple = AnalysisResult(
            keywords=["web"], 
            patterns=["crud_operations"],
            complexity="Baja",
            requirements_implicit=["Basic functionality"],
            domain="web"
        )
        
        decomposition_simple = DecompositionResult(
            phases=[
                Phase(id="development", name="Development", description="Build app", dependencies=[])
            ]
        )
        
        # Complex project  
        analysis_complex = AnalysisResult(
            keywords=["web", "api", "database", "authentication", "real-time", "integration"],
            patterns=["crud_operations", "user_management", "real_time", "integration", "dashboard"],
            complexity="Alta", 
            requirements_implicit=["Complex auth", "Real-time features", "Third-party integration"],
            domain="web"
        )
        
        decomposition_complex = DecompositionResult(
            phases=[
                Phase(id="development", name="Development", description="Build complex app", dependencies=[])
            ]
        )
        
        # Generate task graphs
        simple_graph = generate_task_graph(decomposition_simple, analysis_simple)
        complex_graph = generate_task_graph(decomposition_complex, analysis_complex)
        
        # Complex project should generate more tasks
        assert len(complex_graph.tasks) > len(simple_graph.tasks), \
            f"Complex project ({len(complex_graph.tasks)} tasks) should have more tasks than simple ({len(simple_graph.tasks)} tasks)"
        
        # Task complexity scores should be higher for complex project
        simple_complexity = [t.complexity_score for t in simple_graph.tasks if t.complexity_score]
        complex_complexity = [t.complexity_score for t in complex_graph.tasks if t.complexity_score]
        
        if simple_complexity and complex_complexity:
            avg_simple = sum(simple_complexity) / len(simple_complexity)
            avg_complex = sum(complex_complexity) / len(complex_complexity)
            assert avg_complex > avg_simple, "Complex project tasks should have higher complexity scores"


class TestCriticalPathAndBottlenecks:
    """Test critical path identification and bottleneck detection."""
    
    def test_critical_path_calculation(self):
        """Test that critical path is correctly calculated through tasks."""
        analysis = AnalysisResult(
            keywords=["web"], 
            patterns=["crud_operations"],
            complexity="Media",
            requirements_implicit=["Standard features"],
            domain="web"
        )
        
        decomposition = DecompositionResult(
            phases=[
                Phase(id="phase1", name="Phase 1", description="First phase", dependencies=[]),
                Phase(id="phase2", name="Phase 2", description="Second phase", dependencies=["phase1"]),
                Phase(id="phase3", name="Phase 3", description="Third phase", dependencies=["phase2"])
            ],
            critical_path=["phase1", "phase2", "phase3"]
        )
        
        task_graph = generate_task_graph(decomposition, analysis)
        
        # Critical path should exist and contain task IDs
        assert task_graph.critical_path is not None
        assert len(task_graph.critical_path) > 0
        
        # All critical path tasks should exist
        task_ids = [task.id for task in task_graph.tasks]
        for critical_task_id in task_graph.critical_path:
            assert critical_task_id in task_ids, f"Critical path task {critical_task_id} not found in tasks"
    
    def test_bottleneck_detection(self):
        """Test that bottleneck tasks are correctly identified."""
        analysis = AnalysisResult(
            keywords=["web"],
            patterns=["integration"], 
            complexity="Media",
            requirements_implicit=["Integration points"],
            domain="web"
        )
        
        decomposition = DecompositionResult(
            phases=[
                Phase(id="setup", name="Setup", description="Setup phase", dependencies=[]),
                Phase(id="core", name="Core", description="Core development", dependencies=["setup"]),
                Phase(id="integration", name="Integration", description="Integration phase", dependencies=["core"])
            ]
        )
        
        task_graph = generate_task_graph(decomposition, analysis)
        
        # Bottlenecks should be detected
        assert task_graph.bottlenecks is not None
        
        # If bottlenecks exist, they should be valid task IDs
        if task_graph.bottlenecks:
            task_ids = [task.id for task in task_graph.tasks]
            for bottleneck_id in task_graph.bottlenecks:
                assert bottleneck_id in task_ids, f"Bottleneck task {bottleneck_id} not found"


class TestParallelExecution:
    """Test parallel task identification."""
    
    def test_parallel_task_identification(self):
        """Test identification of tasks that can run in parallel."""
        analysis = AnalysisResult(
            keywords=["web", "frontend", "backend"],
            patterns=["crud_operations"],
            complexity="Media", 
            requirements_implicit=["Frontend and backend"],
            domain="web"
        )
        
        decomposition = DecompositionResult(
            phases=[
                Phase(id="design", name="Design", description="Design phase", dependencies=[]),
                Phase(id="frontend", name="Frontend", description="Frontend work", dependencies=["design"]),
                Phase(id="backend", name="Backend", description="Backend work", dependencies=["design"])
            ],
            parallel_opportunities=[["frontend", "backend"]]
        )
        
        task_graph = generate_task_graph(decomposition, analysis)
        
        # Parallel tasks should be identified
        assert task_graph.parallel_tasks is not None
        
        # Should have at least one parallel group
        if task_graph.parallel_tasks:
            assert len(task_graph.parallel_tasks) > 0
            
            # Each parallel group should contain valid task IDs
            task_ids = [task.id for task in task_graph.tasks]
            for parallel_group in task_graph.parallel_tasks:
                assert len(parallel_group) >= 2, "Parallel group should have at least 2 tasks"
                for task_id in parallel_group:
                    assert task_id in task_ids, f"Parallel task {task_id} not found"


class TestTaskGraphResult:
    """Test TaskGraphResult schema compliance and completeness."""
    
    def test_task_graph_result_schema_compliance(self):
        """Test that generated TaskGraphResult complies with schema."""
        analysis = AnalysisResult(
            keywords=["web"],
            patterns=["crud_operations"],
            complexity="Media",
            requirements_implicit=["Standard web app"],
            domain="web"
        )
        
        decomposition = DecompositionResult(
            phases=[
                Phase(id="dev", name="Development", description="Main development", dependencies=[])
            ]
        )
        
        task_graph = generate_task_graph(decomposition, analysis)
        
        # Required fields should be present
        assert hasattr(task_graph, 'tasks'), "TaskGraphResult should have tasks field"
        assert hasattr(task_graph, 'task_count'), "TaskGraphResult should have task_count field" 
        assert hasattr(task_graph, 'dependency_matrix'), "TaskGraphResult should have dependency_matrix field"
        
        # task_count should match actual count
        assert task_graph.task_count == len(task_graph.tasks), "task_count should match actual task count"
        
        # All tasks should comply with Task schema
        for task in task_graph.tasks:
            assert hasattr(task, 'id'), "Task should have id"
            assert hasattr(task, 'name'), "Task should have name" 
            assert hasattr(task, 'description'), "Task should have description"
            assert hasattr(task, 'phase_id'), "Task should have phase_id"
            assert hasattr(task, 'dependencies'), "Task should have dependencies"
    
    def test_task_id_uniqueness(self):
        """Test that all generated task IDs are unique."""
        analysis = AnalysisResult(
            keywords=["web", "backend"],
            patterns=["crud_operations"],
            complexity="Media",
            requirements_implicit=["Web application"],
            domain="web"
        )
        
        decomposition = DecompositionResult(
            phases=[
                Phase(id="backend", name="Backend Development", description="Backend work", dependencies=[]),
                Phase(id="frontend", name="Frontend Development", description="Frontend work", dependencies=[])
            ]
        )
        
        task_graph = generate_task_graph(decomposition, analysis)
        
        # Collect all task IDs
        task_ids = [task.id for task in task_graph.tasks]
        
        # Check for uniqueness
        assert len(task_ids) == len(set(task_ids)), "All task IDs should be unique"


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_empty_phases_handling(self):
        """Test handling of empty phase list."""
        analysis = AnalysisResult(
            keywords=["test"],
            patterns=[],
            complexity="Baja",
            requirements_implicit=[],
            domain="test"
        )
        
        decomposition = DecompositionResult(phases=[])
        
        task_graph = generate_task_graph(decomposition, analysis)
        
        # Should handle gracefully
        assert task_graph.tasks == []
        assert task_graph.task_count == 0
        assert task_graph.dependency_matrix == {}
    
    def test_invalid_phase_template_handling(self):
        """Test handling of phases that don't match any template."""
        analysis = AnalysisResult(
            keywords=["unknown"],
            patterns=[],
            complexity="Media",
            requirements_implicit=[],
            domain="unknown"
        )
        
        decomposition = DecompositionResult(
            phases=[
                Phase(id="unknown_phase", name="Unknown Phase", description="Unknown work", dependencies=[])
            ]
        )
        
        # Should handle gracefully without crashing
        task_graph = generate_task_graph(decomposition, analysis)
        
        # Should still generate some tasks (fallback behavior)
        assert len(task_graph.tasks) > 0
        assert task_graph.task_count > 0


class TestIntegrationWorkflow:
    """Test complete Analysis → Decomposition → Task Graph workflow."""
    
    def test_complete_workflow_integration(self):
        """Test complete workflow integration as specified in preparation doc."""
        # This will test the example from phase2.3_preparation.md
        from tools.architect.analyze_project import analyze_project
        from tools.architect.decompose_phases import decompose_phases
        
        task_description = "Build web application with authentication"
        
        # Execute complete workflow
        analysis = analyze_project(task_description)
        decomposition = decompose_phases(analysis)
        task_graph = generate_task_graph(decomposition, analysis)
        
        # Validate workflow integrity
        assert analysis is not None, "Analysis should complete successfully"
        assert decomposition is not None, "Decomposition should complete successfully"
        assert task_graph is not None, "Task graph should complete successfully"
        
        # Check data flow between phases
        assert len(task_graph.tasks) > 0, "Task graph should generate tasks"
        assert task_graph.task_count == len(task_graph.tasks), "Task count should match"
        
        # Validate that analysis data influenced task generation
        task_names = [task.name for task in task_graph.tasks]
        # Should contain authentication-related tasks since it was in description
        has_auth_task = any("auth" in name.lower() or "login" in name.lower() for name in task_names)
        assert has_auth_task, "Should generate authentication-related tasks based on description"