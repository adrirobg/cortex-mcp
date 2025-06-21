"""Decompose Phases Module - Phase 2.2 Implementation.

This module implements deterministic phase decomposition for project planning.
Takes AnalysisResult and generates structured project phases with dependencies,
critical path calculation, and parallel execution opportunities.

Follows the 4 Principios Rectores:
1. Dogmatismo con Universal Response Schema - Returns valid DecompositionResult
2. Servidor como Ejecutor Fiable - Deterministic heuristics, no AI magic
3. Estado en Claude, NO en Servidor - Pure functions, no internal state
4. Testing Concurrente - Comprehensive test coverage
"""

import json
import os
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from schemas.architect_payloads import AnalysisResult, DecompositionResult, Phase


def load_phase_templates() -> Dict[str, Any]:
    """Load phase templates from config/phase_templates.json.
    
    Returns:
        Dictionary containing template configurations for different project domains.
        
    Raises:
        FileNotFoundError: If templates file doesn't exist
        json.JSONDecodeError: If templates file contains invalid JSON
    """
    config_path = Path(__file__).parent.parent.parent / "config" / "phase_templates.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            templates: Dict[str, Any] = data.get("templates", {})
            return templates
    except FileNotFoundError:
        raise FileNotFoundError(f"Phase templates file not found at: {config_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in phase templates file: {e}", e.doc, e.pos)


def select_template_by_domain(domain: str) -> str:
    """Select appropriate template based on analysis domain.
    
    Args:
        domain: Project domain from AnalysisResult
        
    Returns:
        Template name to use for phase generation
    """
    # Load domain mapping from config
    config_path = Path(__file__).parent.parent.parent / "config" / "phase_templates.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            domain_mapping = data.get("domain_mapping", {})
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback to hardcoded mapping if config is unavailable
        domain_mapping = {
            "web": "web_app",
            "frontend": "web_app",
            "backend": "web_app", 
            "fullstack": "web_app",
            "api": "api_service",
            "microservice": "api_service",
            "rest": "api_service",
            "graphql": "api_service",
            "data": "data_pipeline",
            "analytics": "data_pipeline",
            "pipeline": "data_pipeline",
            "etl": "data_pipeline",
            "mobile": "mobile_app",
            "android": "mobile_app",
            "ios": "mobile_app",
            "app": "mobile_app"
        }
    
    # Normalize domain for case-insensitive matching
    domain_lower = domain.lower() if domain else ""
    
    # Return mapped template or default
    template_name: str = domain_mapping.get(domain_lower, "default")
    return template_name


def generate_phases_from_template(template_data: Dict[str, Any], complexity: str) -> List[Phase]:
    """Generate Phase objects from template data with complexity adjustments.
    
    Args:
        template_data: Template configuration data
        complexity: Project complexity level (baja, media, alta, muy_alta)
        
    Returns:
        List of Phase objects with adjusted durations
    """
    if "phases" not in template_data:
        return []
    
    # Load complexity adjustments
    config_path = Path(__file__).parent.parent.parent / "config" / "phase_templates.json"
    complexity_adjustments = {
        "baja": 0.7,
        "media": 1.0,
        "alta": 1.5,
        "muy_alta": 2.0
    }
    
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            complexity_adjustments = data.get("complexity_adjustments", complexity_adjustments)
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # Use default adjustments
    
    # Get complexity multiplier
    complexity_multiplier = complexity_adjustments.get(complexity.lower(), 1.0)
    
    phases = []
    for phase_data in template_data["phases"]:
        # Extract phase information
        phase_id = phase_data["id"]
        name = phase_data["name"]
        description = phase_data.get("description", "")
        dependencies = phase_data.get("dependencies", [])
        estimated_duration = phase_data.get("estimated_duration", "1 day")
        artifacts = phase_data.get("artifacts", [])
        
        # Apply complexity adjustment to duration
        adjusted_duration = _adjust_duration_by_complexity(estimated_duration, complexity_multiplier)
        
        # Create Phase object
        phase = Phase(
            id=phase_id,
            name=name,
            description=description,
            dependencies=dependencies,
            estimated_duration=adjusted_duration,
            deliverables=artifacts  # Use artifacts as deliverables
        )
        
        phases.append(phase)
    
    return phases


def calculate_phase_dependencies(phases: List[Phase]) -> Dict[str, List[str]]:
    """Calculate dependency mapping for phases.
    
    Args:
        phases: List of Phase objects
        
    Returns:
        Dictionary mapping phase IDs to their dependency lists
        
    Raises:
        ValueError: If invalid dependency references found
    """
    phase_ids = {phase.id for phase in phases}
    dependency_map = {}
    
    for phase in phases:
        # Validate that all dependencies exist
        invalid_deps = set(phase.dependencies) - phase_ids
        if invalid_deps:
            raise ValueError(f"Invalid dependency references in phase '{phase.id}': {invalid_deps}")
        
        dependency_map[phase.id] = phase.dependencies.copy()
    
    return dependency_map


def identify_critical_path(phases: List[Phase]) -> List[str]:
    """Identify critical path through project phases.
    
    Uses topological sorting and duration-based path analysis.
    
    Args:
        phases: List of Phase objects
        
    Returns:
        List of phase IDs representing the critical path
    """
    if not phases:
        return []
    
    # Build dependency map and duration map
    dependency_map = calculate_phase_dependencies(phases)
    duration_map = {phase.id: _parse_duration_to_days(phase.estimated_duration or "1 day") for phase in phases}
    
    # Find phases with no dependencies (entry points)
    entry_phases = [phase.id for phase in phases if not phase.dependencies]
    
    if not entry_phases:
        # Handle circular dependencies by returning first phase
        return [phases[0].id] if phases else []
    
    # Calculate longest path from each entry point
    longest_path = []
    max_duration = 0
    
    for entry_phase in entry_phases:
        path, total_duration = _calculate_longest_path(entry_phase, dependency_map, duration_map)
        if total_duration > max_duration:
            max_duration = total_duration
            longest_path = path
    
    return longest_path


def find_parallel_opportunities(phases: List[Phase]) -> List[List[str]]:
    """Find groups of phases that can be executed in parallel.
    
    Args:
        phases: List of Phase objects
        
    Returns:
        List of lists, each containing phase IDs that can run in parallel
    """
    if len(phases) < 2:
        return []
    
    dependency_map = calculate_phase_dependencies(phases)
    parallel_groups = []
    
    # Find phases that share the same dependencies
    dependency_groups: Dict[Tuple[str, ...], List[str]] = {}
    for phase in phases:
        dep_key = tuple(sorted(phase.dependencies))
        if dep_key not in dependency_groups:
            dependency_groups[dep_key] = []
        dependency_groups[dep_key].append(phase.id)
    
    # Groups with multiple phases can potentially run in parallel
    for dep_key, phase_ids in dependency_groups.items():
        if len(phase_ids) > 1:
            # Additional check: ensure phases don't depend on each other
            independent_phases = _filter_independent_phases(phase_ids, dependency_map)
            if len(independent_phases) > 1:
                parallel_groups.append(independent_phases)
    
    return parallel_groups


def estimate_total_duration(phases: List[Phase]) -> str:
    """Estimate total project duration considering dependencies and parallel execution.
    
    Args:
        phases: List of Phase objects
        
    Returns:
        String describing total estimated duration
    """
    if not phases:
        return "0 days"
    
    # Build dependency map and duration map
    dependency_map = calculate_phase_dependencies(phases)
    duration_map = {phase.id: _parse_duration_to_days(phase.estimated_duration or "1 day") for phase in phases}
    
    # Calculate critical path duration (accounts for dependencies)
    critical_path = identify_critical_path(phases)
    critical_duration = sum(duration_map.get(phase_id, 0) for phase_id in critical_path)
    
    # Format duration output
    if critical_duration == 0:
        return "0 days"
    elif critical_duration == 1:
        return "1 day"
    elif critical_duration < 7:
        return f"{critical_duration} days"
    elif critical_duration < 30:
        weeks = critical_duration / 7
        return f"{weeks:.1f} weeks"
    else:
        months = critical_duration / 30
        return f"{months:.1f} months"


def decompose_phases(analysis: AnalysisResult) -> DecompositionResult:
    """Main function to decompose project into structured phases.
    
    Args:
        analysis: Result from analyze_project (Phase 2.1)
        
    Returns:
        DecompositionResult with phases, dependencies, and execution plan
    """
    # Load templates and select appropriate one
    templates = load_phase_templates()
    template_name = select_template_by_domain(analysis.domain or "unknown")
    
    if template_name not in templates:
        template_name = "default"
    
    template_data = templates[template_name]
    
    # Generate phases from template
    phases = generate_phases_from_template(template_data, analysis.complexity)
    
    # Calculate project metrics
    total_duration = estimate_total_duration(phases)
    critical_path = identify_critical_path(phases)
    parallel_opportunities = find_parallel_opportunities(phases)
    
    # Create and return DecompositionResult
    return DecompositionResult(
        phases=phases,
        total_estimated_duration=total_duration,
        critical_path=critical_path,
        parallel_opportunities=parallel_opportunities
    )


# Helper functions for internal calculations

def _adjust_duration_by_complexity(duration: str, multiplier: float) -> str:
    """Adjust phase duration based on complexity multiplier."""
    days = _parse_duration_to_days(duration)
    adjusted_days = max(1, int(days * multiplier))
    
    if adjusted_days == 1:
        return "1 day"
    elif adjusted_days < 7:
        return f"{adjusted_days} days"
    elif adjusted_days < 30:
        weeks = adjusted_days / 7
        return f"{weeks:.1f} weeks"
    else:
        months = adjusted_days / 30
        return f"{months:.1f} months"


def _parse_duration_to_days(duration: str) -> int:
    """Parse duration string to days for calculations."""
    duration_lower = duration.lower()
    
    if "day" in duration_lower:
        # Extract number before "day"
        parts = duration_lower.split()
        for part in parts:
            if part.replace(".", "").replace("-", "").isdigit():
                return int(float(part.split("-")[0]))  # Take first number if range
    elif "week" in duration_lower:
        # Convert weeks to days
        parts = duration_lower.split()
        for part in parts:
            if part.replace(".", "").replace("-", "").isdigit():
                weeks = float(part.split("-")[0])
                return int(weeks * 7)
    elif "month" in duration_lower:
        # Convert months to days
        parts = duration_lower.split()
        for part in parts:
            if part.replace(".", "").replace("-", "").isdigit():
                months = float(part.split("-")[0])
                return int(months * 30)
    
    # Default fallback
    return 1


def _calculate_phase_complexity(phase_data: Dict[str, Any], project_complexity: str) -> int:
    """Calculate complexity score for individual phase."""
    base_complexity = {
        "baja": 3,
        "media": 5,
        "alta": 7,
        "muy_alta": 9
    }.get(project_complexity.lower(), 5)
    
    # Adjust based on phase characteristics
    if len(phase_data.get("dependencies", [])) > 2:
        base_complexity += 1
    
    if len(phase_data.get("artifacts", [])) > 3:
        base_complexity += 1
    
    return min(10, max(1, base_complexity))


def _suggest_agent_profile(phase_data: Dict[str, Any]) -> str:
    """Suggest appropriate agent profile for phase."""
    phase_name = phase_data.get("name", "").lower()
    phase_id = phase_data.get("id", "").lower()
    
    if "design" in phase_name or "architect" in phase_name:
        return "architect"
    elif "frontend" in phase_name or "ui" in phase_name:
        return "frontend_developer"
    elif "backend" in phase_name or "api" in phase_name:
        return "backend_developer"
    elif "data" in phase_name or "pipeline" in phase_name:
        return "data_engineer"
    elif "test" in phase_name or "qa" in phase_name:
        return "qa_engineer"
    elif "deploy" in phase_name or "devops" in phase_name:
        return "devops_engineer"
    elif "mobile" in phase_name or "app" in phase_name:
        return "mobile_developer"
    else:
        return "full_stack_developer"


def _generate_validation_criteria(phase_data: Dict[str, Any]) -> List[str]:
    """Generate validation criteria for phase completion."""
    criteria = []
    
    # Add artifact-based criteria
    artifacts = phase_data.get("artifacts", [])
    for artifact in artifacts:
        criteria.append(f"{artifact.replace('_', ' ').title()} completed and reviewed")
    
    # Add phase-specific criteria
    phase_name = phase_data.get("name", "").lower()
    if "design" in phase_name:
        criteria.append("Architecture approved by stakeholders")
    elif "test" in phase_name:
        criteria.append("All tests passing with >90% coverage")
    elif "deploy" in phase_name:
        criteria.append("Successful deployment to target environment")
    
    # Default criteria if none specific
    if not criteria:
        criteria.append("Phase deliverables completed and validated")
    
    return criteria


def _requires_human_checkpoint(phase_data: Dict[str, Any]) -> bool:
    """Determine if phase requires human review checkpoint."""
    phase_name = phase_data.get("name", "").lower()
    
    # Critical phases that typically require human oversight
    critical_keywords = ["design", "architect", "deploy", "release", "production"]
    
    return any(keyword in phase_name for keyword in critical_keywords)


def _calculate_longest_path(start_phase: str, dependency_map: Dict[str, List[str]], 
                          duration_map: Dict[str, int]) -> Tuple[List[str], int]:
    """Calculate longest path from start phase using DFS."""
    visited = set()
    
    def dfs(phase_id: str) -> Tuple[List[str], int]:
        if phase_id in visited:
            return [phase_id], duration_map.get(phase_id, 0)
        
        visited.add(phase_id)
        
        # Find all phases that depend on this one
        dependents = [pid for pid, deps in dependency_map.items() if phase_id in deps]
        
        if not dependents:
            # Leaf node
            return [phase_id], duration_map.get(phase_id, 0)
        
        # Find longest path among dependents
        longest_path = [phase_id]
        max_duration = duration_map.get(phase_id, 0)
        
        for dependent in dependents:
            path, duration = dfs(dependent)
            total_duration = duration_map.get(phase_id, 0) + duration
            if total_duration > max_duration:
                max_duration = total_duration
                longest_path = [phase_id] + path
        
        return longest_path, max_duration
    
    return dfs(start_phase)


def _filter_independent_phases(phase_ids: List[str], dependency_map: Dict[str, List[str]]) -> List[str]:
    """Filter phases that don't depend on each other."""
    independent = []
    
    for phase_id in phase_ids:
        # Check if this phase depends on any other phase in the group
        phase_deps = set(dependency_map.get(phase_id, []))
        other_phases = set(phase_ids) - {phase_id}
        
        if not phase_deps.intersection(other_phases):
            independent.append(phase_id)
    
    return independent