"""Task Graph module for Strategy Library MCP Server.

Implements Phase 2.3 functionality to convert project phases into granular tasks
with comprehensive dependency management, critical path calculation, and parallel execution detection.

Enhanced with Gemini architect feedback:
- Function signature includes both DecompositionResult and AnalysisResult
- Configuration-driven task generation using task_generation_templates.json
- Granular task validation with specific test cases support

Following Principios Rectores:
1. Dogmatismo con Universal Response Schema - strict TaskGraphResult validation
2. Servidor como Ejecutor Fiable - deterministic task generation, no AI magic  
3. Estado en Claude, NO en Servidor - pure functions, no state
4. Testing Concurrente - comprehensive test coverage with TDD approach
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple, Any
from schemas.architect_payloads import (
    AnalysisResult, DecompositionResult, TaskGraphResult, Task, Phase
)


def load_task_templates() -> Dict[str, Any]:
    """Load task generation templates from configuration file.
    
    Returns:
        Dict containing task templates and configuration
        
    Raises:
        FileNotFoundError: If configuration file not found
        json.JSONDecodeError: If configuration file malformed
    """
    config_path = Path(__file__).parent.parent.parent / "config" / "task_generation_templates.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content: Dict[str, Any] = json.load(f)
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Task templates configuration not found at {config_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in task templates: {e.msg}", e.doc, e.pos)


def _normalize_phase_name_to_template(phase_name: str) -> str:
    """Normalize phase name to match template keys.
    
    Args:
        phase_name: Original phase name from decomposition
        
    Returns:
        Normalized template key name
    """
    phase_lower = phase_name.lower()
    
    # Direct mappings
    template_mappings = {
        "system design & architecture": "design",
        "system design and architecture": "design", 
        "design & architecture": "design",
        "design and architecture": "design",
        "architecture": "design",
        "design": "design",
        
        "backend api development": "backend",
        "backend development": "backend", 
        "api development": "backend",
        "server development": "backend",
        "backend": "backend",
        
        "frontend ui implementation": "frontend",
        "frontend implementation": "frontend",
        "ui development": "frontend", 
        "user interface": "frontend",
        "frontend": "frontend",
        
        "frontend-backend integration": "integration",
        "system integration": "integration",
        "api integration": "integration",
        "integration": "integration",
        
        "testing & validation": "testing",
        "testing and validation": "testing",
        "quality assurance": "testing",
        "testing": "testing",
        
        "deployment & infrastructure": "deployment",
        "deployment and infrastructure": "deployment",
        "infrastructure setup": "deployment",
        "deployment": "deployment"
    }
    
    # Check direct mapping first
    if phase_lower in template_mappings:
        return template_mappings[phase_lower]
    
    # Keyword-based fallback
    if any(keyword in phase_lower for keyword in ["design", "architect", "plan"]):
        return "design"
    elif any(keyword in phase_lower for keyword in ["backend", "api", "server", "database"]):
        return "backend"  
    elif any(keyword in phase_lower for keyword in ["frontend", "ui", "interface", "client"]):
        return "frontend"
    elif any(keyword in phase_lower for keyword in ["integration", "connect", "combine"]):
        return "integration"
    elif any(keyword in phase_lower for keyword in ["test", "qa", "validation", "verify"]):
        return "testing"
    elif any(keyword in phase_lower for keyword in ["deploy", "infrastructure", "production", "hosting"]):
        return "deployment"
    
    # Default fallback
    return "design"


def _apply_complexity_adjustments(tasks: List[Dict[str, Any]], complexity: str, templates_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Apply complexity-based adjustments to task list.
    
    Args:
        tasks: List of task templates
        complexity: Project complexity level ("Baja", "Media", "Alta") 
        templates_config: Configuration containing complexity adjustments
        
    Returns:
        Adjusted list of tasks
    """
    if "complexity_adjustments" not in templates_config:
        return tasks
    
    adjustments = templates_config["complexity_adjustments"].get(complexity, {})
    task_multiplier = adjustments.get("task_multiplier", 1.0)
    skip_optional = adjustments.get("skip_optional", False)
    
    # Apply task count multiplier
    if task_multiplier != 1.0:
        target_count = max(1, int(len(tasks) * task_multiplier))
        if target_count < len(tasks):
            # Remove lower priority tasks (later in list)
            tasks = tasks[:target_count]
        elif target_count > len(tasks) and task_multiplier > 1.0:
            # For complex projects, duplicate some tasks with variations
            additional_tasks = []
            for i in range(target_count - len(tasks)):
                if i < len(tasks):
                    base_task = tasks[i].copy()
                    base_task["id_suffix"] += f"_enhanced"
                    base_task["name"] += " (Enhanced)"
                    base_task["complexity_score"] = min(10, base_task.get("complexity_score", 3) + 1)
                    additional_tasks.append(base_task)
            tasks.extend(additional_tasks)
    
    return tasks


def _apply_domain_adjustments(phase_template_key: str, domain: Optional[str], templates_config: Dict[str, Any]) -> bool:
    """Check if phase should be included based on domain adjustments.
    
    Args:
        phase_template_key: Template key for the phase
        domain: Project domain classification
        templates_config: Configuration containing domain adjustments
        
    Returns:
        True if phase should be included, False otherwise
    """
    if not domain or "domain_adjustments" not in templates_config:
        return True
    
    domain_config = templates_config["domain_adjustments"].get(domain, {})
    priority_phases = domain_config.get("priority_phases", [])
    optional_phases = domain_config.get("optional_phases", [])
    
    # Always include priority phases
    if phase_template_key in priority_phases:
        return True
    
    # Include optional phases for medium/high complexity
    if phase_template_key in optional_phases:
        return True  # For now, include all optional phases
    
    # Include phases not specifically mentioned
    all_mentioned = priority_phases + optional_phases
    if phase_template_key not in all_mentioned:
        return True
    
    return True


def generate_tasks_from_phases(phases: List[Phase], analysis: AnalysisResult, templates_config: Dict[str, Any]) -> List[Task]:
    """Generate granular tasks from project phases using configuration templates.
    
    Args:
        phases: List of project phases from decomposition
        analysis: Analysis result for domain and complexity information
        templates_config: Loaded task generation templates
        
    Returns:
        List of Task objects with proper dependencies and metadata
    """
    all_tasks = []
    task_templates = templates_config.get("task_templates", {})
    
    for phase in phases:
        # Normalize phase name to template key
        template_key = _normalize_phase_name_to_template(phase.name)
        
        # Check domain adjustments
        if not _apply_domain_adjustments(template_key, analysis.domain, templates_config):
            continue
        
        # Get template for this phase type
        phase_template = task_templates.get(template_key, task_templates.get("design", {}))
        task_configs = phase_template.get("tasks", [])
        
        # Apply complexity adjustments
        task_configs = _apply_complexity_adjustments(task_configs, analysis.complexity, templates_config)
        
        # Generate tasks for this phase
        phase_tasks = []
        for i, task_config in enumerate(task_configs):
            task_id = f"{phase.id}{task_config['id_suffix']}"
            
            # Map internal dependencies to actual task IDs within this phase
            internal_deps = task_config.get("internal_dependencies", [])
            task_dependencies = [f"{phase.id}{dep}" for dep in internal_deps]
            
            # Create Task object
            task = Task(
                id=task_id,
                name=task_config["name"],
                description=task_config["description"],
                phase_id=phase.id,
                dependencies=task_dependencies,
                estimated_effort=task_config.get("estimated_effort"),
                complexity_score=task_config.get("complexity_score"),
                agent_profile=task_config.get("agent_profile"),
                artifacts_output=task_config.get("artifacts_output", []),
                validation_criteria=task_config.get("validation_criteria", []),
                human_checkpoint=task_config.get("human_checkpoint", False)
            )
            
            phase_tasks.append(task)
        
        all_tasks.extend(phase_tasks)
    
    return all_tasks


def _resolve_inter_phase_dependencies(tasks: List[Task], phases: List[Phase]) -> List[Task]:
    """Resolve dependencies between tasks from different phases.
    
    Args:
        tasks: List of tasks with intra-phase dependencies resolved
        phases: List of phases with their dependencies
        
    Returns:
        Updated list of tasks with inter-phase dependencies added
    """
    # Create phase dependency mapping
    phase_deps = {phase.id: phase.dependencies for phase in phases}
    
    # Group tasks by phase
    tasks_by_phase: Dict[str, List[Task]] = {}
    for task in tasks:
        if task.phase_id not in tasks_by_phase:
            tasks_by_phase[task.phase_id] = []
        tasks_by_phase[task.phase_id].append(task)
    
    # Add inter-phase dependencies
    updated_tasks = []
    for task in tasks:
        updated_dependencies = list(task.dependencies)  # Start with intra-phase deps
        
        # For each phase this task's phase depends on
        for dependent_phase_id in phase_deps.get(task.phase_id, []):
            if dependent_phase_id in tasks_by_phase:
                # Add dependency to the last task(s) of the dependent phase
                dependent_phase_tasks = tasks_by_phase[dependent_phase_id]
                if dependent_phase_tasks:
                    # Find tasks with no dependents within the dependent phase
                    dependent_task_ids = {t.id for t in dependent_phase_tasks}
                    final_tasks = []
                    for dep_task in dependent_phase_tasks:
                        is_final = True
                        for other_task in dependent_phase_tasks:
                            if dep_task.id in other_task.dependencies:
                                is_final = False
                                break
                        if is_final:
                            final_tasks.append(dep_task.id)
                    
                    # Add dependencies to final tasks of dependent phase
                    if final_tasks:
                        updated_dependencies.extend(final_tasks)
        
        # Create updated task
        updated_task = Task(
            id=task.id,
            name=task.name,
            description=task.description,
            phase_id=task.phase_id,
            dependencies=list(set(updated_dependencies)),  # Remove duplicates
            estimated_effort=task.estimated_effort,
            complexity_score=task.complexity_score,
            agent_profile=task.agent_profile,
            artifacts_output=task.artifacts_output,
            validation_criteria=task.validation_criteria,
            human_checkpoint=task.human_checkpoint
        )
        
        updated_tasks.append(updated_task)
    
    return updated_tasks


def calculate_task_dependencies(tasks: List[Task]) -> Dict[str, List[str]]:
    """Build comprehensive dependency matrix for all tasks.
    
    Args:
        tasks: List of all project tasks
        
    Returns:
        Dictionary mapping task_id -> list of task_ids it depends on
    """
    dependency_matrix = {}
    
    for task in tasks:
        dependency_matrix[task.id] = task.dependencies.copy()
    
    return dependency_matrix


def _calculate_task_depths(dependency_matrix: Dict[str, List[str]]) -> Dict[str, int]:
    """Calculate depth (longest path from root) for each task.
    
    Args:
        dependency_matrix: Task dependency mapping
        
    Returns:
        Dictionary mapping task_id -> depth in dependency graph
    """
    depths: Dict[str, int] = {}
    
    def calculate_depth(task_id: str, visited: Set[str]) -> int:
        if task_id in visited:
            return 0  # Cycle detection - return minimal depth
        if task_id in depths:
            return depths[task_id]
        
        visited.add(task_id)
        dependencies = dependency_matrix.get(task_id, [])
        
        if not dependencies:
            depths[task_id] = 0
        else:
            max_dep_depth = max(calculate_depth(dep_id, visited) for dep_id in dependencies)
            depths[task_id] = max_dep_depth + 1
        
        visited.remove(task_id)
        return depths[task_id]
    
    # Calculate depths for all tasks
    for task_id in dependency_matrix:
        if task_id not in depths:
            calculate_depth(task_id, set())
    
    return depths


def identify_task_critical_path(tasks: List[Task], dependency_matrix: Dict[str, List[str]]) -> List[str]:
    """Identify critical path through task-level dependencies.
    
    Uses depth-first approach to find longest path through task dependencies.
    Adapts Phase 2.2 algorithm patterns for task-level granularity.
    
    Args:
        tasks: List of all tasks
        dependency_matrix: Task dependency relationships
        
    Returns:
        List of task IDs representing the critical path
    """
    if not tasks:
        return []
    
    # Calculate task depths (longest path from any root)
    task_depths = _calculate_task_depths(dependency_matrix)
    
    # Find the task with maximum depth
    max_depth = max(task_depths.values()) if task_depths else 0
    end_tasks = [task_id for task_id, depth in task_depths.items() if depth == max_depth]
    
    if not end_tasks:
        return []
    
    # Trace back from the deepest task to build critical path
    critical_path: List[str] = []
    current_task: Optional[str] = end_tasks[0]  # Take first if multiple end tasks
    
    while current_task:
        critical_path.insert(0, current_task)  # Add to beginning
        
        # Find the dependency with maximum depth
        dependencies = dependency_matrix.get(current_task, [])
        if not dependencies:
            break
        
        # Choose dependency with highest depth
        max_dep_depth = -1
        next_task: Optional[str] = None
        for dep_task in dependencies:
            dep_depth = task_depths.get(dep_task, 0)
            if dep_depth > max_dep_depth:
                max_dep_depth = dep_depth
                next_task = dep_task
        
        current_task = next_task
    
    return critical_path


def detect_task_bottlenecks(tasks: List[Task], dependency_matrix: Dict[str, List[str]]) -> List[str]:
    """Identify potential bottleneck tasks based on dependency analysis.
    
    Bottlenecks are tasks that:
    1. Have multiple tasks depending on them (high fan-out)
    2. Are part of the critical path
    3. Have high complexity scores
    
    Args:
        tasks: List of all tasks
        dependency_matrix: Task dependency relationships
        
    Returns:
        List of task IDs that are potential bottlenecks
    """
    bottlenecks = []
    
    # Count how many tasks depend on each task (reverse dependencies)
    dependents_count = {}
    for task_id, dependencies in dependency_matrix.items():
        for dep_task in dependencies:
            if dep_task not in dependents_count:
                dependents_count[dep_task] = 0
            dependents_count[dep_task] += 1
    
    # Get critical path tasks
    critical_path = identify_task_critical_path(tasks, dependency_matrix)
    critical_path_set = set(critical_path)
    
    # Create task lookup for complexity scores
    task_lookup = {task.id: task for task in tasks}
    
    for task in tasks:
        bottleneck_score = 0
        
        # High fan-out (many tasks depend on this one)
        dependents = dependents_count.get(task.id, 0)
        if dependents >= 3:  # 3+ tasks depend on it
            bottleneck_score += 2
        elif dependents >= 2:
            bottleneck_score += 1
        
        # Critical path task
        if task.id in critical_path_set:
            bottleneck_score += 2
        
        # High complexity
        if task.complexity_score and task.complexity_score >= 4:
            bottleneck_score += 1
        
        # Consider bottleneck if score >= 3
        if bottleneck_score >= 3:
            bottlenecks.append(task.id)
    
    return bottlenecks


def _identify_parallel_task_groups(tasks: List[Task], dependency_matrix: Dict[str, List[str]]) -> List[List[str]]:
    """Identify groups of tasks that can run in parallel.
    
    Args:
        tasks: List of all tasks
        dependency_matrix: Task dependency relationships
        
    Returns:
        List of parallel groups, where each group is a list of task IDs
    """
    parallel_groups = []
    
    # Group tasks by their dependency depth level
    task_depths = _calculate_task_depths(dependency_matrix)
    depth_groups: Dict[int, List[str]] = {}
    
    for task_id, depth in task_depths.items():
        if depth not in depth_groups:
            depth_groups[depth] = []
        depth_groups[depth].append(task_id)
    
    # Each depth level with multiple tasks can potentially run in parallel
    for depth, task_ids in depth_groups.items():
        if len(task_ids) > 1:
            # Filter out tasks that have dependencies within the same depth level
            parallel_candidates = []
            for task_id in task_ids:
                dependencies = dependency_matrix.get(task_id, [])
                same_depth_deps = [dep for dep in dependencies if task_depths.get(dep, -1) == depth]
                
                # Only include if no dependencies at same depth level
                if not same_depth_deps:
                    parallel_candidates.append(task_id)
            
            # Add as parallel group if we have 2+ candidates
            if len(parallel_candidates) > 1:
                parallel_groups.append(parallel_candidates)
    
    return parallel_groups


def generate_task_graph(decomposition: DecompositionResult, analysis: AnalysisResult) -> TaskGraphResult:
    """Generate comprehensive task graph from project decomposition and analysis.
    
    Main function implementing enhanced signature from Gemini feedback.
    Orchestrates all task generation functionality following Phase 2.3 specifications.
    
    Args:
        decomposition: Project decomposition with phases and dependencies
        analysis: Project analysis with domain, complexity, and patterns
        
    Returns:
        TaskGraphResult with complete task specifications and metadata
        
    Raises:
        ValueError: If decomposition or analysis are invalid
        FileNotFoundError: If task templates configuration missing
    """
    if not decomposition or not decomposition.phases:
        # Handle empty phases gracefully
        return TaskGraphResult(
            tasks=[],
            task_count=0,
            dependency_matrix={},
            critical_path=[],
            parallel_tasks=[],
            bottlenecks=[]
        )
    
    if not analysis:
        raise ValueError("AnalysisResult is required for intelligent task generation")
    
    # Load task generation templates
    templates_config = load_task_templates()
    
    # Generate tasks from phases using templates
    tasks = generate_tasks_from_phases(decomposition.phases, analysis, templates_config)
    
    # Resolve inter-phase dependencies
    tasks = _resolve_inter_phase_dependencies(tasks, decomposition.phases)
    
    # Calculate comprehensive dependency matrix
    dependency_matrix = calculate_task_dependencies(tasks)
    
    # Identify critical path through tasks
    critical_path = identify_task_critical_path(tasks, dependency_matrix)
    
    # Detect potential bottlenecks
    bottlenecks = detect_task_bottlenecks(tasks, dependency_matrix)
    
    # Identify parallel execution opportunities
    parallel_tasks = _identify_parallel_task_groups(tasks, dependency_matrix)
    
    # Create and validate TaskGraphResult
    result = TaskGraphResult(
        tasks=tasks,
        task_count=len(tasks),
        dependency_matrix=dependency_matrix,
        critical_path=critical_path,
        parallel_tasks=parallel_tasks,
        bottlenecks=bottlenecks
    )
    
    return result