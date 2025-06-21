"""Mission Map module for Strategy Library MCP Server.

Implements Phase 2.4 functionality with revolutionary TDD-enforced workflow architecture.
Converts task graphs into executable mission plans with intelligent resource assignment.

STRATEGIC ENHANCEMENT (Gemini's Insight):
- TDD workflow is now INTRINSIC to the system, not a manual reminder
- Automatic TDD task pairing: every implementation task gets a corresponding test task
- Dependency enforcement: test tasks are prerequisites for implementation tasks
- Agent profiles include TDD expertise and workflow awareness
- Resource planning respects TDD cycles (test → implement → validate)

Enhanced with insights from Phase 2.1, 2.2, and 2.3 meta-reflections:
- Configuration-driven architecture using JSON templates
- Enhanced function signature includes both TaskGraphResult and AnalysisResult
- Type safety with comprehensive MyPy compliance
- Error resilience with detailed diagnostics

Following Principios Rectores:
1. Dogmatismo con Universal Response Schema - strict MissionMapResult validation
2. Servidor como Ejecutor Fiable - deterministic resource assignment algorithms
3. Estado en Claude, NO en Servidor - pure functions, no state persistence
4. Testing Concurrente - comprehensive test coverage with TDD patterns
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple, Any
from schemas.architect_payloads import (
    AnalysisResult, TaskGraphResult, MissionMapResult, Task, ResourceAssignment
)


def load_agent_profiles() -> Dict[str, Any]:
    """Load agent profiles configuration from JSON file.
    
    Returns:
        Dict containing agent profiles with TDD expertise and capabilities
        
    Raises:
        FileNotFoundError: If configuration file not found
        json.JSONDecodeError: If configuration file malformed
    """
    config_path = Path(__file__).parent.parent.parent / "config" / "agent_profiles.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content: Dict[str, Any] = json.load(f)
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Agent profiles configuration not found at {config_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in agent profiles: {e.msg}", e.doc, e.pos)


def load_resource_assignment_rules() -> Dict[str, Any]:
    """Load resource assignment rules configuration from JSON file.
    
    Returns:
        Dict containing assignment priorities and optimization rules
        
    Raises:
        FileNotFoundError: If configuration file not found
        json.JSONDecodeError: If configuration file malformed
    """
    config_path = Path(__file__).parent.parent.parent / "config" / "resource_assignment_rules.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            content: Dict[str, Any] = json.load(f)
            return content
    except FileNotFoundError:
        raise FileNotFoundError(f"Resource assignment rules not found at {config_path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in resource assignment rules: {e.msg}", e.doc, e.pos)


def _normalize_agent_profile(profile: str) -> str:
    """Normalize agent profile names for consistency.
    
    Args:
        profile: Original agent profile name
        
    Returns:
        Normalized profile name (lowercase, underscores)
    """
    return profile.lower().replace(" ", "_").replace("-", "_")


def _generate_tdd_task_pairs(tasks: List[Task]) -> List[Task]:
    """Generate TDD task pairs - Gemini's strategic enhancement.
    
    For every implementation task without a corresponding test task,
    automatically generates a test task that must precede it.
    
    Args:
        tasks: Original list of tasks
        
    Returns:
        Expanded list of tasks with TDD test tasks added
    """
    enhanced_tasks = list(tasks)
    existing_test_tasks = {task.id for task in tasks if task.id.startswith("test_")}
    
    for task in tasks:
        # Skip if this is already a test task
        if task.id.startswith("test_"):
            continue
            
        # Skip if this is a validation/deployment task (not implementation)
        if any(keyword in task.name.lower() for keyword in ["validate", "deploy", "verify", "check"]):
            continue
            
        # Determine corresponding test task ID
        if task.id.startswith("impl_"):
            test_task_id = task.id.replace("impl_", "test_")
        else:
            test_task_id = f"test_{task.id}"
        
        # Skip if test task already exists
        if test_task_id in existing_test_tasks:
            continue
            
        # Generate test task
        test_task = Task(
            id=test_task_id,
            name=f"Write Unit Tests for {task.name}",
            description=f"Create comprehensive unit tests for {task.name}. These tests should fail initially (Red phase of TDD). Write tests that define the expected behavior and interface.",
            phase_id=task.phase_id,
            dependencies=[],  # Test tasks have no implementation dependencies
            estimated_effort=_estimate_test_effort(task.estimated_effort),
            complexity_score=max(1, (task.complexity_score or 3) - 1),  # Tests typically slightly less complex
            agent_profile=task.agent_profile,  # Same agent handles test and implementation
            artifacts_output=[f"test_{task.id}.py", f"test_cases_{task.id}.json"],
            validation_criteria=[
                "Tests fail initially (Red phase)",
                "Tests cover all expected functionality", 
                "Tests follow naming conventions",
                "Tests include edge cases"
            ],
            human_checkpoint=False
        )
        
        enhanced_tasks.append(test_task)
        existing_test_tasks.add(test_task_id)
    
    return enhanced_tasks


def _estimate_test_effort(implementation_effort: Optional[str]) -> str:
    """Estimate effort required for test task based on implementation effort.
    
    Args:
        implementation_effort: Effort estimate for implementation task
        
    Returns:
        Effort estimate for corresponding test task
    """
    if not implementation_effort:
        return "0.5 days"
    
    # Parse effort and calculate test effort (typically 30-50% of implementation)
    effort_lower = implementation_effort.lower()
    
    if "hour" in effort_lower:
        # Extract hours and calculate test hours
        try:
            hours = int(effort_lower.split()[0])
            test_hours = max(1, int(hours * 0.4))
            return f"{test_hours} hours"
        except (ValueError, IndexError):
            return "2 hours"
    
    elif "day" in effort_lower:
        # Extract days and calculate test days
        try:
            days = float(effort_lower.split()[0])
            test_days = max(0.25, days * 0.3)
            if test_days < 1:
                return f"{int(test_days * 8)} hours"
            else:
                return f"{test_days:.1f} days"
        except (ValueError, IndexError):
            return "0.5 days"
    
    else:
        return "0.5 days"


def _apply_tdd_dependencies(tasks: List[Task]) -> List[Task]:
    """Apply TDD dependency enforcement - test tasks must precede implementation.
    
    Args:
        tasks: List of tasks with test tasks included
        
    Returns:
        Updated tasks with TDD dependencies enforced
    """
    updated_tasks = []
    task_lookup = {task.id: task for task in tasks}
    
    for task in tasks:
        updated_dependencies = list(task.dependencies)
        
        # If this is an implementation task, ensure it depends on corresponding test task
        if not task.id.startswith("test_"):
            # Find corresponding test task
            test_task_id = None
            if task.id.startswith("impl_"):
                test_task_id = task.id.replace("impl_", "test_")
            else:
                test_task_id = f"test_{task.id}"
            
            # Add test dependency if test task exists
            if test_task_id in task_lookup and test_task_id not in updated_dependencies:
                updated_dependencies.append(test_task_id)
        
        # Create updated task
        updated_task = Task(
            id=task.id,
            name=task.name,
            description=task.description,
            phase_id=task.phase_id,
            dependencies=updated_dependencies,
            estimated_effort=task.estimated_effort,
            complexity_score=task.complexity_score,
            agent_profile=task.agent_profile,
            artifacts_output=task.artifacts_output,
            validation_criteria=task.validation_criteria,
            human_checkpoint=task.human_checkpoint
        )
        
        updated_tasks.append(updated_task)
    
    return updated_tasks


def assign_agent_profiles(tasks: List[Task], agent_config: Dict[str, Any]) -> List[ResourceAssignment]:
    """Assign optimal agent profiles to tasks with TDD workflow awareness.
    
    Args:
        tasks: List of tasks to assign agents to
        agent_config: Agent profiles configuration
        
    Returns:
        List of ResourceAssignment objects with intelligent agent assignment
    """
    assignments = []
    agent_profiles = agent_config.get("agent_profiles", {})
    
    # Track workload per agent for balancing
    agent_workload: Dict[str, List[str]] = {profile: [] for profile in agent_profiles.keys()}
    
    for task in tasks:
        # Determine best agent profile for this task
        assigned_profile = _determine_best_agent_profile(task, agent_profiles, agent_workload)
        
        # Calculate priority based on task characteristics
        priority = _calculate_task_priority(task)
        
        # Determine parallel group (tasks that can run concurrently)
        parallel_group = _determine_parallel_group(task, tasks)
        
        # Create resource assignment
        assignment = ResourceAssignment(
            task_id=task.id,
            agent_profile=assigned_profile,
            estimated_effort=task.estimated_effort or "1 day",
            priority=priority,
            parallel_group=parallel_group
        )
        
        assignments.append(assignment)
        
        # Update workload tracking
        if assigned_profile in agent_workload:
            agent_workload[assigned_profile].append(task.id)
    
    return assignments


def _determine_best_agent_profile(task: Task, agent_profiles: Dict[str, Any], current_workload: Dict[str, List[str]]) -> str:
    """Determine the best agent profile for a task using intelligent assignment algorithm.
    
    Args:
        task: Task to assign agent to
        agent_profiles: Available agent profiles
        current_workload: Current workload per agent
        
    Returns:
        Best agent profile name
    """
    if not agent_profiles:
        return "general_developer"
    
    # If task already has agent profile specified, validate and use it
    if task.agent_profile and _normalize_agent_profile(task.agent_profile) in agent_profiles:
        return _normalize_agent_profile(task.agent_profile)
    
    best_profile = None
    best_score = -1
    
    for profile_name, profile_config in agent_profiles.items():
        score = 0
        
        # Check specialization match
        specializations = profile_config.get("specializations", [])
        task_keywords = [task.name.lower(), task.description.lower(), task.phase_id.lower()]
        
        for specialization in specializations:
            if any(specialization in keywords for keywords in task_keywords):
                score += 10  # High weight for exact specialization match
        
        # Check complexity range compatibility
        complexity_range = profile_config.get("complexity_range", [1, 5])
        task_complexity = task.complexity_score or 3
        
        if complexity_range[0] <= task_complexity <= complexity_range[1]:
            score += 8  # Good compatibility with complexity
        elif task_complexity < complexity_range[0]:
            score += 4  # Overqualified but acceptable
        else:
            score -= 5  # Underqualified
        
        # Check TDD expertise for test tasks
        if task.id.startswith("test_") and profile_config.get("tdd_expertise", False):
            score += 9  # High weight for TDD expertise on test tasks
        
        # Workload balancing - prefer agents with lower current workload
        current_tasks = len(current_workload.get(profile_name, []))
        max_tasks = profile_config.get("max_concurrent_tasks", 3)
        
        if current_tasks < max_tasks:
            score += (max_tasks - current_tasks) * 2  # Prefer less loaded agents
        else:
            score -= 10  # Avoid overloaded agents
        
        # TDD workflow pairing - prefer same agent for test/implementation pairs
        if not task.id.startswith("test_"):
            corresponding_test = f"test_{task.id}" if not task.id.startswith("impl_") else task.id.replace("impl_", "test_")
            for other_task_id in current_workload.get(profile_name, []):
                if other_task_id == corresponding_test:
                    score += 15  # Strong preference for TDD workflow continuity
        
        if score > best_score:
            best_score = score
            best_profile = profile_name
    
    return best_profile or list(agent_profiles.keys())[0]


def _calculate_task_priority(task: Task) -> int:
    """Calculate task priority based on characteristics.
    
    Args:
        task: Task to calculate priority for
        
    Returns:
        Priority score (1-10, higher = more priority)
    """
    priority = 5  # Base priority
    
    # Test tasks get higher priority (TDD workflow)
    if task.id.startswith("test_"):
        priority += 2
    
    # Higher complexity tasks get higher priority
    if task.complexity_score:
        if task.complexity_score >= 4:
            priority += 2
        elif task.complexity_score >= 3:
            priority += 1
    
    # Human checkpoint tasks get higher priority
    if task.human_checkpoint:
        priority += 1
    
    # Critical path tasks (determined by dependencies) get higher priority
    if len(task.dependencies) == 0:  # Root tasks
        priority += 1
    
    return min(10, max(1, priority))


def _determine_parallel_group(task: Task, all_tasks: List[Task]) -> Optional[str]:
    """Determine parallel execution group for a task.
    
    Args:
        task: Task to group
        all_tasks: All tasks in the project
        
    Returns:
        Parallel group identifier or None
    """
    # Tasks with no dependencies can potentially run in parallel
    if not task.dependencies:
        return f"parallel_group_level_0"
    
    # Group by dependency depth level
    max_depth = 0
    task_lookup = {t.id: t for t in all_tasks}
    
    def calculate_depth(task_id: str, visited: Set[str]) -> int:
        if task_id in visited or task_id not in task_lookup:
            return 0
        visited.add(task_id)
        deps = task_lookup[task_id].dependencies
        if not deps:
            visited.remove(task_id)
            return 0
        max_dep_depth = max(calculate_depth(dep, visited) for dep in deps)
        visited.remove(task_id)
        return max_dep_depth + 1
    
    depth = calculate_depth(task.id, set())
    return f"parallel_group_level_{depth}"


def create_parallel_groups(tasks: List[Task], dependency_matrix: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """Create optimized parallel execution groups respecting TDD workflows.
    
    Args:
        tasks: List of all tasks
        dependency_matrix: Task dependency relationships
        
    Returns:
        Dictionary of parallel groups with task assignments
    """
    parallel_groups: Dict[str, List[str]] = {}
    
    # Calculate dependency depths for grouping
    task_depths = _calculate_task_depths(dependency_matrix)
    
    # Group tasks by dependency level
    depth_groups: Dict[int, List[str]] = {}
    for task_id, depth in task_depths.items():
        if depth not in depth_groups:
            depth_groups[depth] = []
        depth_groups[depth].append(task_id)
    
    # Create parallel groups while respecting TDD dependencies
    for depth_level, task_ids in depth_groups.items():
        if len(task_ids) <= 1:
            continue  # No parallel opportunities
        
        # Filter out tasks that have intra-level dependencies (TDD pairs)
        parallel_candidates = []
        for task_id in task_ids:
            dependencies = dependency_matrix.get(task_id, [])
            same_level_deps = [dep for dep in dependencies if task_depths.get(dep, -1) == depth_level]
            
            # Only include if no dependencies at same level (respects TDD test→impl ordering)
            if not same_level_deps:
                parallel_candidates.append(task_id)
        
        # Create parallel group if we have multiple candidates
        if len(parallel_candidates) > 1:
            # Further split by workload balancing and agent compatibility
            balanced_groups = _balance_parallel_workload(parallel_candidates, tasks)
            
            for i, group in enumerate(balanced_groups):
                group_id = f"level_{depth_level}_group_{i}"
                parallel_groups[group_id] = group
    
    return parallel_groups


def _calculate_task_depths(dependency_matrix: Dict[str, List[str]]) -> Dict[str, int]:
    """Calculate dependency depth for each task.
    
    Args:
        dependency_matrix: Task dependency mapping
        
    Returns:
        Dictionary mapping task_id -> depth in dependency graph
    """
    depths: Dict[str, int] = {}
    
    def calculate_depth(task_id: str, visited: Set[str]) -> int:
        if task_id in visited:
            return 0  # Cycle detection
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
    
    for task_id in dependency_matrix:
        if task_id not in depths:
            calculate_depth(task_id, set())
    
    return depths


def _balance_parallel_workload(task_ids: List[str], all_tasks: List[Task]) -> List[List[str]]:
    """Balance workload across parallel execution groups.
    
    Args:
        task_ids: Task IDs to balance
        all_tasks: All task objects for complexity lookup
        
    Returns:
        List of balanced parallel groups
    """
    if len(task_ids) <= 3:
        return [task_ids]  # Small groups don't need balancing
    
    # Sort tasks by complexity for better distribution
    task_lookup = {task.id: task for task in all_tasks}
    sorted_tasks = sorted(task_ids, key=lambda tid: task_lookup.get(tid, Task(
        id="", name="", description="", phase_id="", dependencies=[], 
        estimated_effort=None, complexity_score=None, agent_profile=None, 
        artifacts_output=[], validation_criteria=[], human_checkpoint=False
    )).complexity_score or 3, reverse=True)
    
    # Distribute into balanced groups (aim for groups of 2-4 tasks)
    target_group_size = 3
    groups = []
    
    for i in range(0, len(sorted_tasks), target_group_size):
        group = sorted_tasks[i:i + target_group_size]
        groups.append(group)
    
    return groups


def calculate_resource_utilization(assignments: List[ResourceAssignment], agent_config: Dict[str, Any]) -> Dict[str, str]:
    """Calculate resource utilization and optimization metrics.
    
    Args:
        assignments: Resource assignments for all tasks
        agent_config: Agent configuration with capacity limits
        
    Returns:
        Dictionary with utilization metrics per agent
    """
    utilization = {}
    agent_profiles = agent_config.get("agent_profiles", {})
    
    # Group assignments by agent profile
    agent_assignments: Dict[str, List[ResourceAssignment]] = {}
    for assignment in assignments:
        profile = assignment.agent_profile
        if profile not in agent_assignments:
            agent_assignments[profile] = []
        agent_assignments[profile].append(assignment)
    
    # Calculate utilization for each agent profile
    for profile, profile_assignments in agent_assignments.items():
        profile_config = agent_profiles.get(profile, {})
        max_concurrent = profile_config.get("max_concurrent_tasks", 3)
        
        # Calculate workload metrics
        total_tasks = len(profile_assignments)
        total_effort_days = _estimate_total_effort_days(profile_assignments)
        
        # Calculate parallel capacity utilization
        parallel_groups = {}
        for assignment in profile_assignments:
            if assignment.parallel_group:
                group = assignment.parallel_group
                if group not in parallel_groups:
                    parallel_groups[group] = 0
                parallel_groups[group] += 1
        
        max_parallel_load = max(parallel_groups.values()) if parallel_groups else 1
        utilization_percentage = min(100, (max_parallel_load / max_concurrent) * 100)
        
        efficiency_rating = _calculate_efficiency_rating(utilization_percentage, total_tasks)
        tdd_compliance = _calculate_tdd_compliance(profile_assignments)
        
        utilization[profile] = f"{utilization_percentage:.1f}% utilization ({total_tasks} tasks, {total_effort_days:.1f} days, {efficiency_rating}, TDD: {tdd_compliance:.0%})"
    
    return utilization


def _estimate_total_effort_days(assignments: List[ResourceAssignment]) -> float:
    """Estimate total effort in days for a set of assignments.
    
    Args:
        assignments: Resource assignments to calculate effort for
        
    Returns:
        Total effort in days
    """
    total_days = 0.0
    
    for assignment in assignments:
        effort = assignment.estimated_effort.lower()
        
        if "day" in effort:
            try:
                days = float(effort.split()[0])
                total_days += days
            except (ValueError, IndexError):
                total_days += 1.0
        elif "hour" in effort:
            try:
                hours = float(effort.split()[0])
                total_days += hours / 8.0  # 8 hours per day
            except (ValueError, IndexError):
                total_days += 0.125  # 1 hour default
        else:
            total_days += 1.0  # Default to 1 day
    
    return total_days


def _calculate_efficiency_rating(utilization_percentage: float, task_count: int) -> str:
    """Calculate efficiency rating based on utilization and task distribution.
    
    Args:
        utilization_percentage: Resource utilization percentage
        task_count: Number of tasks assigned
        
    Returns:
        Efficiency rating string
    """
    if utilization_percentage < 60:
        return "Under-utilized"
    elif utilization_percentage > 90:
        return "Over-utilized" 
    elif 70 <= utilization_percentage <= 85:
        return "Optimal"
    else:
        return "Good"


def _calculate_specialization_match(assignments: List[ResourceAssignment], profile_config: Dict[str, Any]) -> float:
    """Calculate how well assignments match agent specializations.
    
    Args:
        assignments: Assignments for an agent
        profile_config: Agent profile configuration
        
    Returns:
        Specialization match score (0.0 - 1.0)
    """
    if not assignments:
        return 0.0
    
    specializations = profile_config.get("specializations", [])
    if not specializations:
        return 0.5  # Neutral if no specializations defined
    
    # This would require task lookup - simplified for now
    return 0.8  # Assume good match for MVP


def _calculate_tdd_compliance(assignments: List[ResourceAssignment]) -> float:
    """Calculate TDD workflow compliance for agent assignments.
    
    Args:
        assignments: Assignments to analyze
        
    Returns:
        TDD compliance score (0.0 - 1.0)
    """
    if not assignments:
        return 0.0
    
    test_tasks = sum(1 for a in assignments if a.task_id.startswith("test_"))
    impl_tasks = sum(1 for a in assignments if not a.task_id.startswith("test_") and not any(keyword in a.task_id for keyword in ["validate", "deploy"]))
    
    if impl_tasks == 0:
        return 1.0 if test_tasks > 0 else 0.5
    
    # Ideal TDD ratio is close to 1:1 test:implementation
    tdd_ratio = test_tasks / impl_tasks if impl_tasks > 0 else 0
    compliance = min(1.0, tdd_ratio)
    
    return compliance


def _calculate_workload_balance(assignments: List[ResourceAssignment]) -> Dict[str, Dict[str, Any]]:
    """Calculate workload balance across all agent assignments.
    
    Args:
        assignments: All resource assignments
        
    Returns:
        Workload balance metrics per agent
    """
    agent_workloads: Dict[str, List[ResourceAssignment]] = {}
    
    for assignment in assignments:
        profile = assignment.agent_profile
        if profile not in agent_workloads:
            agent_workloads[profile] = []
        agent_workloads[profile].append(assignment)
    
    balance_metrics = {}
    for profile, profile_assignments in agent_workloads.items():
        total_effort_days = _estimate_total_effort_days(profile_assignments)
        task_count = len(profile_assignments)
        avg_priority = sum(a.priority for a in profile_assignments) / task_count if task_count > 0 else 0
        
        balance_metrics[profile] = {
            "total_effort_days": int(total_effort_days) if total_effort_days == int(total_effort_days) else total_effort_days,
            "task_count": task_count,
            "average_priority": avg_priority,
            "workload_score": total_effort_days * (avg_priority / 10)
        }
    
    return balance_metrics


def _detect_resource_conflicts(assignments: List[ResourceAssignment], agent_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Detect resource assignment conflicts and overallocation.
    
    Args:
        assignments: Resource assignments to analyze
        agent_config: Agent configuration with capacity limits
        
    Returns:
        List of detected conflicts
    """
    conflicts = []
    agent_profiles = agent_config.get("agent_profiles", {})
    
    # Group by parallel groups to detect conflicts
    parallel_assignments: Dict[str, List[ResourceAssignment]] = {}
    for assignment in assignments:
        if assignment.parallel_group:
            group = assignment.parallel_group
            if group not in parallel_assignments:
                parallel_assignments[group] = []
            parallel_assignments[group].append(assignment)
    
    # Check for overallocation in parallel groups
    for group_id, group_assignments in parallel_assignments.items():
        agent_loads: Dict[str, int] = {}
        for assignment in group_assignments:
            profile = assignment.agent_profile
            agent_loads[profile] = agent_loads.get(profile, 0) + 1
        
        for profile, load in agent_loads.items():
            max_concurrent = agent_profiles.get(profile, {}).get("max_concurrent_tasks", 3)
            if load > max_concurrent:
                conflicts.append({
                    "type": "overallocation",
                    "parallel_group": group_id,
                    "agent_profile": profile,
                    "assigned_tasks": load,
                    "max_capacity": max_concurrent,
                    "description": f"Agent {profile} assigned {load} tasks in parallel group {group_id}, exceeding capacity of {max_concurrent}"
                })
    
    return conflicts


def generate_execution_order(tasks: List[Task], dependency_matrix: Dict[str, List[str]]) -> List[str]:
    """Generate optimal execution order respecting TDD workflows and dependencies.
    
    Args:
        tasks: List of all tasks
        dependency_matrix: Task dependency relationships
        
    Returns:
        Ordered list of task IDs for execution
    """
    # Topological sort with TDD workflow optimization
    execution_order = []
    completed_tasks: Set[str] = set()
    remaining_tasks = {task.id for task in tasks}
    
    while remaining_tasks:
        # Find tasks with no pending dependencies
        ready_tasks = []
        for task_id in remaining_tasks:
            dependencies = dependency_matrix.get(task_id, [])
            if all(dep in completed_tasks for dep in dependencies):
                ready_tasks.append(task_id)
        
        if not ready_tasks:
            # Handle circular dependencies by picking highest priority task
            remaining_list = list(remaining_tasks)
            ready_tasks = [remaining_list[0]]
        
        # Prioritize TDD workflow: test tasks before implementation tasks
        tdd_prioritized = _prioritize_tdd_workflow(ready_tasks)
        
        # Add prioritized tasks to execution order
        for task_id in tdd_prioritized:
            execution_order.append(task_id)
            completed_tasks.add(task_id)
            remaining_tasks.remove(task_id)
    
    return execution_order


def _prioritize_tdd_workflow(ready_tasks: List[str]) -> List[str]:
    """Prioritize tasks within TDD workflow constraints.
    
    Args:
        ready_tasks: Tasks that are ready to execute
        
    Returns:
        Prioritized list following TDD workflow principles
    """
    # Separate test and implementation tasks
    test_tasks = [task_id for task_id in ready_tasks if task_id.startswith("test_")]
    impl_tasks = [task_id for task_id in ready_tasks if not task_id.startswith("test_")]
    
    prioritized = []
    
    # Process test tasks first (TDD Red phase)
    test_tasks.sort()  # Alphabetical order for consistency
    prioritized.extend(test_tasks)
    
    # Then implementation tasks (TDD Green phase)
    impl_tasks.sort()  # Alphabetical order for consistency
    prioritized.extend(impl_tasks)
    
    return prioritized


def create_mission_map(task_graph: TaskGraphResult, analysis: AnalysisResult) -> MissionMapResult:
    """Create comprehensive mission map with TDD-enforced workflow architecture.
    
    Main function implementing Phase 2.4 with Gemini's strategic enhancement.
    Transforms task graphs into executable mission plans with intelligent resource assignment.
    
    STRATEGIC ENHANCEMENT: TDD is now intrinsic to the workflow, not a manual reminder.
    
    Args:
        task_graph: Task graph from Phase 2.3 with comprehensive task specifications
        analysis: Analysis result from Phase 2.1 for domain and complexity information
        
    Returns:
        MissionMapResult with complete resource planning and TDD workflow enforcement
        
    Raises:
        ValueError: If task_graph or analysis are invalid
        FileNotFoundError: If configuration files are missing
    """
    if not task_graph:
        raise ValueError("TaskGraphResult is required for mission map creation")
    
    if not analysis:
        raise ValueError("AnalysisResult is required for intelligent resource assignment")
    
    # Handle empty task graph gracefully
    if not task_graph.tasks:
        return MissionMapResult(
            resource_assignments=[],
            execution_order=[],
            parallel_groups={},
            total_effort_estimate="0 days",
            resource_utilization={}
        )
    
    # Load configuration files
    agent_config = load_agent_profiles()
    rules_config = load_resource_assignment_rules()
    
    # STRATEGIC ENHANCEMENT: Apply TDD task pairing and dependency enforcement
    enhanced_tasks = _generate_tdd_task_pairs(task_graph.tasks)
    tdd_enforced_tasks = _apply_tdd_dependencies(enhanced_tasks)
    
    # Rebuild dependency matrix with TDD enhancements
    enhanced_dependency_matrix = {task.id: task.dependencies for task in tdd_enforced_tasks}
    
    # Assign agent profiles with TDD workflow awareness
    resource_assignments = assign_agent_profiles(tdd_enforced_tasks, agent_config)
    
    # Create parallel execution groups respecting TDD workflows
    parallel_groups = create_parallel_groups(tdd_enforced_tasks, enhanced_dependency_matrix)
    
    # Generate execution order with TDD workflow enforcement
    execution_order = generate_execution_order(tdd_enforced_tasks, enhanced_dependency_matrix)
    
    # Calculate resource utilization and optimization metrics
    resource_utilization = calculate_resource_utilization(resource_assignments, agent_config)
    
    # Calculate total effort estimate
    total_effort_estimate = _calculate_total_effort_estimate(resource_assignments)
    
    # Create and validate MissionMapResult
    mission_map = MissionMapResult(
        resource_assignments=resource_assignments,
        execution_order=execution_order,
        parallel_groups=parallel_groups,
        total_effort_estimate=total_effort_estimate,
        resource_utilization=resource_utilization
    )
    
    return mission_map


def _calculate_total_effort_estimate(assignments: List[ResourceAssignment]) -> str:
    """Calculate total effort estimate for the project.
    
    Args:
        assignments: All resource assignments
        
    Returns:
        Human-readable total effort estimate
    """
    total_days = _estimate_total_effort_days(assignments)
    
    if total_days < 1:
        hours = int(total_days * 8)
        return f"{hours} hours"
    elif total_days < 7:
        return f"{total_days:.1f} days"
    else:
        weeks = total_days / 5  # 5 working days per week
        if weeks < 4:
            return f"{weeks:.1f} weeks"
        else:
            months = weeks / 4
            return f"{months:.1f} months"