"""Tests for decompose_phases module.

Comprehensive test coverage for Phase 2.2 implementation following Testing Concurrente principle.
Validates template loading, phase generation, dependency calculation, and DecompositionResult schema compliance.
"""

import pytest
import json
from unittest.mock import patch, mock_open
from tools.architect.decompose_phases import (
    decompose_phases,
    load_phase_templates,
    select_template_by_domain,
    generate_phases_from_template,
    calculate_phase_dependencies,
    estimate_total_duration,
    identify_critical_path,
    find_parallel_opportunities
)
from schemas.architect_payloads import AnalysisResult, DecompositionResult, Phase


class TestLoadPhaseTemplates:
    """Test phase template loading functionality."""
    
    def test_load_valid_templates(self):
        """Test loading valid phase templates from JSON."""
        # TODO: Implement template loading from config/phase_templates.json
        templates = load_phase_templates()
        
        assert isinstance(templates, dict)
        assert "web_app" in templates
        assert "api_service" in templates
        assert "data_pipeline" in templates
        assert "mobile_app" in templates
        assert "default" in templates
    
    def test_template_structure_validation(self):
        """Test that loaded templates have correct structure."""
        templates = load_phase_templates()
        
        # Validate web_app template structure
        web_template = templates["web_app"]
        assert "description" in web_template
        assert "phases" in web_template
        assert "estimated_base_duration" in web_template
        
        # Validate phase structure
        phases = web_template["phases"]
        assert len(phases) > 0
        
        for phase in phases:
            assert "id" in phase
            assert "name" in phase
            assert "dependencies" in phase
            assert isinstance(phase["dependencies"], list)
    
    def test_load_templates_file_not_found(self):
        """Test handling when templates file doesn't exist."""
        with patch("builtins.open", side_effect=FileNotFoundError):
            with pytest.raises(FileNotFoundError):
                load_phase_templates()
    
    def test_load_invalid_json(self):
        """Test handling of invalid JSON in templates file."""
        with patch("builtins.open", mock_open(read_data="invalid json")):
            with pytest.raises(json.JSONDecodeError):
                load_phase_templates()


class TestSelectTemplateByDomain:
    """Test domain-to-template selection logic."""
    
    def test_select_web_template(self):
        """Test selection of web_app template for web domain."""
        template_name = select_template_by_domain("web")
        assert template_name == "web_app"
    
    def test_select_api_template(self):
        """Test selection of api_service template for api domain."""
        template_name = select_template_by_domain("api")
        assert template_name == "api_service"
    
    def test_select_data_template(self):
        """Test selection of data_pipeline template for data domain."""
        template_name = select_template_by_domain("data")
        assert template_name == "data_pipeline"
    
    def test_select_mobile_template(self):
        """Test selection of mobile_app template for mobile domain."""
        template_name = select_template_by_domain("mobile")
        assert template_name == "mobile_app"
    
    def test_select_default_template(self):
        """Test fallback to default template for unknown domain."""
        template_name = select_template_by_domain("unknown_domain")
        assert template_name == "default"
    
    def test_select_template_case_insensitive(self):
        """Test template selection is case insensitive."""
        template_name = select_template_by_domain("WEB")
        assert template_name == "web_app"


class TestGeneratePhasesFromTemplate:
    """Test phase generation from templates."""
    
    def test_generate_web_phases(self):
        """Test generation of phases for web application."""
        # TODO: Mock template data
        template_data = {
            "phases": [
                {"id": "design", "name": "System Design", "dependencies": []},
                {"id": "backend", "name": "Backend Development", "dependencies": ["design"]},
                {"id": "frontend", "name": "Frontend Development", "dependencies": ["design"]}
            ]
        }
        
        phases = generate_phases_from_template(template_data, "media")
        
        assert len(phases) == 3
        assert all(isinstance(phase, Phase) for phase in phases)
        assert phases[0].id == "design"
        assert phases[1].id == "backend"
        assert phases[2].id == "frontend"
    
    def test_generate_phases_with_complexity_adjustment(self):
        """Test that phase durations are adjusted based on complexity."""
        template_data = {
            "phases": [
                {"id": "implementation", "name": "Implementation", "dependencies": [], "estimated_duration": "1 week"}
            ]
        }
        
        # Test with different complexity levels
        phases_low = generate_phases_from_template(template_data, "baja")
        phases_high = generate_phases_from_template(template_data, "alta")
        
        # TODO: Verify duration adjustments based on complexity
        assert len(phases_low) == 1
        assert len(phases_high) == 1
    
    def test_generate_phases_empty_template(self):
        """Test handling of empty template."""
        template_data = {"phases": []}
        
        phases = generate_phases_from_template(template_data, "media")
        assert len(phases) == 0


class TestCalculatePhaseDependencies:
    """Test phase dependency calculation."""
    
    def test_calculate_simple_dependencies(self):
        """Test calculation of simple linear dependencies."""
        phases = [
            Phase(id="a", name="Phase A", description="First phase", dependencies=[]),
            Phase(id="b", name="Phase B", description="Second phase", dependencies=["a"]),
            Phase(id="c", name="Phase C", description="Third phase", dependencies=["b"])
        ]
        
        dependency_map = calculate_phase_dependencies(phases)
        
        assert dependency_map["a"] == []
        assert dependency_map["b"] == ["a"]
        assert dependency_map["c"] == ["b"]
    
    def test_calculate_complex_dependencies(self):
        """Test calculation of complex dependencies with multiple parents."""
        phases = [
            Phase(id="a", name="Phase A", description="First phase", dependencies=[]),
            Phase(id="b", name="Phase B", description="Second phase", dependencies=[]),
            Phase(id="c", name="Phase C", description="Third phase", dependencies=["a", "b"]),
            Phase(id="d", name="Phase D", description="Fourth phase", dependencies=["c"])
        ]
        
        dependency_map = calculate_phase_dependencies(phases)
        
        assert dependency_map["a"] == []
        assert dependency_map["b"] == []
        assert set(dependency_map["c"]) == {"a", "b"}
        assert dependency_map["d"] == ["c"]
    
    def test_calculate_dependencies_invalid_reference(self):
        """Test handling of invalid dependency references."""
        phases = [
            Phase(id="a", name="Phase A", description="First phase", dependencies=["nonexistent"])
        ]
        
        # TODO: Decide if this should raise error or ignore invalid references
        with pytest.raises(ValueError):
            calculate_phase_dependencies(phases)


class TestIdentifyCriticalPath:
    """Test critical path identification."""
    
    def test_identify_linear_critical_path(self):
        """Test identification of critical path in linear dependency chain."""
        phases = [
            Phase(id="a", name="Phase A", description="First phase", dependencies=[], estimated_duration="1 day"),
            Phase(id="b", name="Phase B", description="Second phase", dependencies=["a"], estimated_duration="2 days"),
            Phase(id="c", name="Phase C", description="Third phase", dependencies=["b"], estimated_duration="1 day")
        ]
        
        critical_path = identify_critical_path(phases)
        assert critical_path == ["a", "b", "c"]
    
    def test_identify_complex_critical_path(self):
        """Test identification of critical path with parallel branches."""
        phases = [
            Phase(id="a", name="Phase A", description="First phase", dependencies=[], estimated_duration="1 day"),
            Phase(id="b", name="Phase B", description="Second phase", dependencies=["a"], estimated_duration="3 days"),
            Phase(id="c", name="Phase C", description="Third phase", dependencies=["a"], estimated_duration="1 day"),
            Phase(id="d", name="Phase D", description="Fourth phase", dependencies=["b", "c"], estimated_duration="1 day")
        ]
        
        critical_path = identify_critical_path(phases)
        # Critical path should go through the longer branch (a -> b -> d)
        assert "a" in critical_path
        assert "b" in critical_path
        assert "d" in critical_path
    
    def test_identify_critical_path_no_phases(self):
        """Test critical path identification with no phases."""
        critical_path = identify_critical_path([])
        assert critical_path == []


class TestFindParallelOpportunities:
    """Test parallel execution opportunities identification."""
    
    def test_find_simple_parallel_opportunities(self):
        """Test finding simple parallel execution opportunities."""
        phases = [
            Phase(id="a", name="Phase A", description="First phase", dependencies=[]),
            Phase(id="b", name="Phase B", description="Second phase", dependencies=["a"]),
            Phase(id="c", name="Phase C", description="Third phase", dependencies=["a"]),
            Phase(id="d", name="Phase D", description="Fourth phase", dependencies=["b", "c"])
        ]
        
        parallel_opportunities = find_parallel_opportunities(phases)
        
        # b and c can run in parallel after a
        assert ["b", "c"] in parallel_opportunities or ["c", "b"] in parallel_opportunities
    
    def test_find_no_parallel_opportunities(self):
        """Test case with no parallel execution opportunities."""
        phases = [
            Phase(id="a", name="Phase A", description="First phase", dependencies=[]),
            Phase(id="b", name="Phase B", description="Second phase", dependencies=["a"]),
            Phase(id="c", name="Phase C", description="Third phase", dependencies=["b"])
        ]
        
        parallel_opportunities = find_parallel_opportunities(phases)
        assert len(parallel_opportunities) == 0
    
    def test_find_multiple_parallel_groups(self):
        """Test finding multiple groups of parallel phases."""
        phases = [
            Phase(id="a", name="Phase A", description="First phase", dependencies=[]),
            Phase(id="b", name="Phase B", description="Second phase", dependencies=[]),
            Phase(id="c", name="Phase C", description="Third phase", dependencies=["a"]),
            Phase(id="d", name="Phase D", description="Fourth phase", dependencies=["b"]),
            Phase(id="e", name="Phase E", description="Fifth phase", dependencies=["c", "d"])
        ]
        
        parallel_opportunities = find_parallel_opportunities(phases)
        
        # Should find both (a,b) and (c,d) as parallel groups
        assert len(parallel_opportunities) >= 1


class TestEstimateTotalDuration:
    """Test total project duration estimation."""
    
    def test_estimate_linear_duration(self):
        """Test duration estimation for linear phase sequence."""
        phases = [
            Phase(id="a", name="Phase A", description="First phase", dependencies=[], estimated_duration="2 days"),
            Phase(id="b", name="Phase B", description="Second phase", dependencies=["a"], estimated_duration="3 days"),
            Phase(id="c", name="Phase C", description="Third phase", dependencies=["b"], estimated_duration="1 day")
        ]
        
        total_duration = estimate_total_duration(phases)
        assert "6 days" in total_duration or "6" in total_duration
    
    def test_estimate_parallel_duration(self):
        """Test duration estimation with parallel phases."""
        phases = [
            Phase(id="a", name="Phase A", description="First phase", dependencies=[], estimated_duration="1 day"),
            Phase(id="b", name="Phase B", description="Second phase", dependencies=["a"], estimated_duration="3 days"),
            Phase(id="c", name="Phase C", description="Third phase", dependencies=["a"], estimated_duration="2 days"),
            Phase(id="d", name="Phase D", description="Fourth phase", dependencies=["b", "c"], estimated_duration="1 day")
        ]
        
        total_duration = estimate_total_duration(phases)
        # Should be 1 + max(3,2) + 1 = 5 days
        assert "5 days" in total_duration or "5" in total_duration
    
    def test_estimate_duration_no_phases(self):
        """Test duration estimation with no phases."""
        total_duration = estimate_total_duration([])
        assert total_duration == "0 days"


class TestDecomposePhases:
    """Test main decompose_phases function."""
    
    def test_decompose_web_project(self):
        """Test decomposition of web project."""
        analysis_result = AnalysisResult(
            keywords=["web", "frontend", "backend"],
            patterns=["web_application"],
            complexity="media",
            domain="web",
            technology_stack=["javascript", "python"],
            requirements_implicit=["responsive_design", "api_integration"]
        )
        
        result = decompose_phases(analysis_result)
        
        # Validate DecompositionResult structure
        assert isinstance(result, DecompositionResult)
        assert len(result.phases) > 0
        assert result.total_estimated_duration is not None
        assert result.critical_path is not None
        assert isinstance(result.critical_path, list)
    
    def test_decompose_api_project(self):
        """Test decomposition of API project."""
        analysis_result = AnalysisResult(
            keywords=["api", "rest", "microservice"],
            patterns=["api_service"],
            complexity="baja",
            domain="api",
            technology_stack=["python", "fastapi"],
            requirements_implicit=["documentation", "testing"]
        )
        
        result = decompose_phases(analysis_result)
        
        assert isinstance(result, DecompositionResult)
        assert len(result.phases) > 0
        # API projects should have phases like design, implementation, documentation
        phase_names = [phase.name for phase in result.phases]
        assert any("design" in name.lower() for name in phase_names)
    
    def test_decompose_data_project(self):
        """Test decomposition of data pipeline project."""
        analysis_result = AnalysisResult(
            keywords=["data", "pipeline", "etl"],
            patterns=["data_processing"],
            complexity="alta",
            domain="data",
            technology_stack=["python", "pandas"],
            requirements_implicit=["data_validation", "monitoring"]
        )
        
        result = decompose_phases(analysis_result)
        
        assert isinstance(result, DecompositionResult)
        assert len(result.phases) > 0
        # Data projects should have phases like sourcing, processing, storage
        phase_names = [phase.name for phase in result.phases]
        assert any("data" in name.lower() for name in phase_names)
    
    def test_decompose_mobile_project(self):
        """Test decomposition of mobile app project."""
        analysis_result = AnalysisResult(
            keywords=["mobile", "app", "ios", "android"],
            patterns=["mobile_application"],
            complexity="alta",
            domain="mobile",
            technology_stack=["react-native"],
            requirements_implicit=["app_store_compliance", "device_testing"]
        )
        
        result = decompose_phases(analysis_result)
        
        assert isinstance(result, DecompositionResult)
        assert len(result.phases) > 0
        # Mobile projects should have UI design, development, testing phases
        phase_names = [phase.name for phase in result.phases]
        assert any("ui" in name.lower() or "design" in name.lower() for name in phase_names)
    
    def test_decompose_unknown_domain(self):
        """Test decomposition with unknown domain falls back to default."""
        analysis_result = AnalysisResult(
            keywords=["custom", "unknown"],
            patterns=["unknown_pattern"],
            complexity="media",
            domain="unknown",
            technology_stack=["custom_tech"],
            requirements_implicit=[]
        )
        
        result = decompose_phases(analysis_result)
        
        assert isinstance(result, DecompositionResult)
        assert len(result.phases) > 0
        # Should use default template with generic phases
        phase_names = [phase.name for phase in result.phases]
        assert any("planning" in name.lower() or "implementation" in name.lower() for name in phase_names)
    
    def test_decompose_result_schema_compliance(self):
        """Test that decompose_phases returns valid DecompositionResult."""
        analysis_result = AnalysisResult(
            keywords=["web"],
            patterns=["web_app"],
            complexity="media",
            domain="web",
            technology_stack=["javascript"],
            requirements_implicit=[]
        )
        
        result = decompose_phases(analysis_result)
        
        # Validate all required fields are present
        assert hasattr(result, 'phases')
        assert hasattr(result, 'total_estimated_duration')
        assert hasattr(result, 'critical_path')
        assert hasattr(result, 'parallel_opportunities')
        
        # Validate types
        assert isinstance(result.phases, list)
        assert all(isinstance(phase, Phase) for phase in result.phases)
        if result.critical_path:
            assert isinstance(result.critical_path, list)
        if result.parallel_opportunities:
            assert isinstance(result.parallel_opportunities, list)


class TestIntegrationWithAnalyzeProject:
    """Test integration between decompose_phases and analyze_project."""
    
    def test_integration_web_workflow(self):
        """Test complete workflow from analysis to decomposition for web project."""
        # This test requires analyze_project from Phase 2.1
        from tools.architect.analyze_project import analyze_project
        
        description = "Create a modern web application with React frontend and Node.js backend"
        
        # Phase 2.1: Analysis
        analysis = analyze_project(description)
        
        # Phase 2.2: Decomposition
        decomposition = decompose_phases(analysis)
        
        # Validate workflow integration
        assert isinstance(analysis, AnalysisResult)
        assert isinstance(decomposition, DecompositionResult)
        assert len(decomposition.phases) > 0
        assert decomposition.total_estimated_duration is not None
    
    def test_integration_api_workflow(self):
        """Test complete workflow from analysis to decomposition for API project."""
        from tools.architect.analyze_project import analyze_project
        
        description = "Build a RESTful API service with authentication and database integration"
        
        # Phase 2.1: Analysis
        analysis = analyze_project(description)
        
        # Phase 2.2: Decomposition 
        decomposition = decompose_phases(analysis)
        
        # Validate workflow integration
        assert isinstance(analysis, AnalysisResult)
        assert isinstance(decomposition, DecompositionResult)
        assert analysis.domain in ["api", "web"]  # Could be classified as either
        assert len(decomposition.phases) > 0
    
    def test_integration_data_workflow(self):
        """Test complete workflow from analysis to decomposition for data project."""
        from tools.architect.analyze_project import analyze_project
        
        description = "Develop a data analytics pipeline with ETL processes and PostgreSQL storage"
        
        # Phase 2.1: Analysis
        analysis = analyze_project(description)
        
        # Phase 2.2: Decomposition
        decomposition = decompose_phases(analysis)
        
        # Validate workflow integration
        assert isinstance(analysis, AnalysisResult)
        assert isinstance(decomposition, DecompositionResult)
        assert analysis.domain == "data"
        assert len(decomposition.phases) > 0


class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_analysis_result(self):
        """Test handling of minimal AnalysisResult."""
        analysis_result = AnalysisResult(
            keywords=[],
            patterns=[],
            complexity="media",
            domain="unknown",
            technology_stack=[],
            requirements_implicit=[]
        )
        
        result = decompose_phases(analysis_result)
        
        # Should still return valid result using default template
        assert isinstance(result, DecompositionResult)
        assert len(result.phases) > 0
    
    def test_invalid_complexity_value(self):
        """Test handling of invalid complexity values."""
        analysis_result = AnalysisResult(
            keywords=["web"],
            patterns=["web_app"],
            complexity="invalid_complexity",
            domain="web",
            technology_stack=["javascript"],
            requirements_implicit=[]
        )
        
        # Should handle gracefully, possibly defaulting to "media"
        result = decompose_phases(analysis_result)
        assert isinstance(result, DecompositionResult)
    
    def test_very_long_phase_list(self):
        """Test handling of templates with many phases."""
        # TODO: Create or mock a template with many phases
        # This tests performance and memory handling
        pass
    
    def test_circular_dependencies(self):
        """Test detection and handling of circular dependencies in templates."""
        # TODO: Test what happens if template configuration has circular deps
        # Should either detect and raise error or resolve gracefully
        pass


# Test fixtures and utilities
@pytest.fixture
def sample_web_analysis():
    """Fixture providing sample web project analysis."""
    return AnalysisResult(
        keywords=["web", "frontend", "backend", "react", "node"],
        patterns=["web_application", "spa"],
        complexity="media",
        domain="web",
        technology_stack=["javascript", "react", "nodejs"],
        requirements_implicit=["responsive_design", "api_integration", "testing"]
    )


@pytest.fixture
def sample_api_analysis():
    """Fixture providing sample API project analysis."""
    return AnalysisResult(
        keywords=["api", "rest", "microservice", "database"],
        patterns=["api_service", "microservice"],
        complexity="baja",
        domain="api",
        technology_stack=["python", "fastapi", "postgresql"],
        requirements_implicit=["documentation", "authentication", "testing"]
    )


@pytest.fixture
def sample_data_analysis():
    """Fixture providing sample data project analysis."""
    return AnalysisResult(
        keywords=["data", "pipeline", "etl", "analytics"],
        patterns=["data_processing", "batch_processing"],
        complexity="alta",
        domain="data",
        technology_stack=["python", "pandas", "postgresql"],
        requirements_implicit=["data_validation", "monitoring", "scalability"]
    )