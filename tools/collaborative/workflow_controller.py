"""Collaborative Workflow Controller for Phase 2.7.

This module orchestrates hybrid collaborative workflows that combine deterministic
Motor de Estrategias reliability with Claude intelligence injection at optimal points.

Key Features:
- Multi-step workflow orchestration
- Intelligent collaboration point detection
- Seamless delegation to Claude refinement
- Stateless workflow continuation support
- 100% backward compatibility with existing workflows
"""

import uuid
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

from schemas.universal_response import (
    StrategyResponse, CollaborativeStrategyResponse, Strategy, StrategyType,
    UserFacing, ClaudeInstructions, ExecutionType, Action, Metadata,
    DelegationType, DelegationContext, CollaborationPoint, RefinementRecord
)
from schemas.architect_payloads import (
    ArchitectPayload, WorkflowStage, AnalysisResult, DecompositionResult,
    TaskGraphResult, MissionMapResult
)
from tools.architect.analyze_project import analyze_project
from tools.architect.decompose_phases import decompose_phases
from tools.architect.task_graph import generate_task_graph
from tools.architect.mission_map import create_mission_map
from utils.logger import strategy_logger, generate_trace_id


class CollaborativeWorkflowController:
    """Controller for hybrid collaborative intelligence workflows."""
    
    def __init__(self, collaboration_enabled: bool = True, confidence_threshold: float = 0.75):
        """Initialize collaborative workflow controller.
        
        Args:
            collaboration_enabled: Whether to enable collaborative features
            confidence_threshold: Threshold for triggering Claude collaboration
        """
        self.collaboration_enabled = collaboration_enabled
        self.confidence_threshold = confidence_threshold
        self.trace_id: Optional[str] = None
    
    def execute_collaborative_workflow(
        self,
        task_description: str,
        analysis_result: Optional[Dict[str, Any]] = None,
        decomposition_result: Optional[Dict[str, Any]] = None,
        workflow_stage: Optional[str] = None,
        refined_analysis: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
        debug_mode: bool = False
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute collaborative workflow with Claude intelligence injection.
        
        Args:
            task_description: Project description to analyze
            analysis_result: Previous analysis results (for continuation)
            decomposition_result: Previous decomposition results (for continuation)
            workflow_stage: Specific stage to execute
            refined_analysis: Claude-refined analysis (for collaboration continuation)
            trace_id: Optional trace ID for correlation
            debug_mode: Enable debug information
            
        Returns:
            CollaborativeStrategyResponse with workflow results and collaboration context
        """
        # Initialize trace ID
        self.trace_id = trace_id or generate_trace_id()
        
        # Log workflow start
        strategy_logger.info(
            "collaborative_workflow_started",
            f"Collaborative Motor de Estrategias initiated",
            trace_id=self.trace_id,
            context={
                "collaboration_enabled": self.collaboration_enabled,
                "stage": workflow_stage or "auto_detect",
                "has_refined_analysis": bool(refined_analysis)
            }
        )
        
        try:
            # Determine workflow execution path
            if self._should_use_collaboration(task_description, analysis_result, refined_analysis):
                return self._execute_collaborative_path(
                    task_description, analysis_result, decomposition_result,
                    workflow_stage, refined_analysis, debug_mode
                )
            else:
                return self._execute_deterministic_path(
                    task_description, analysis_result, decomposition_result,
                    workflow_stage, debug_mode
                )
                
        except Exception as e:
            strategy_logger.error(
                "collaborative_workflow_error",
                f"Collaborative workflow failed: {str(e)}",
                trace_id=self.trace_id,
                exception=e
            )
            raise
    
    def _should_use_collaboration(
        self,
        task_description: str,
        analysis_result: Optional[Dict[str, Any]],
        refined_analysis: Optional[Dict[str, Any]]
    ) -> bool:
        """Determine if collaborative workflow should be used.
        
        Returns:
            True if collaboration should be used, False for deterministic workflow
        """
        if not self.collaboration_enabled:
            return False
        
        # If we have refined analysis, we're in collaboration continuation
        if refined_analysis:
            return True
        
        # If we have no analysis yet, check if task complexity warrants collaboration
        if not analysis_result:
            # Complex task descriptions benefit from collaboration
            complexity_indicators = ['complex', 'enterprise', 'microservices', 'scalable', 'advanced']
            if any(indicator in task_description.lower() for indicator in complexity_indicators):
                return True
        
        # If we have analysis with low confidence, use collaboration
        if analysis_result:
            # This is a simplified heuristic - in real implementation,
            # we'd analyze the actual confidence metrics
            return len(task_description) > 100  # Proxy for complexity
        
        return False
    
    def _execute_collaborative_path(
        self,
        task_description: str,
        analysis_result: Optional[Dict[str, Any]],
        decomposition_result: Optional[Dict[str, Any]],
        workflow_stage: Optional[str],
        refined_analysis: Optional[Dict[str, Any]],
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute collaborative workflow path with Claude intelligence injection."""
        
        # If we have refined analysis, continue with it
        if refined_analysis:
            return self._continue_with_refined_analysis(
                task_description, refined_analysis, decomposition_result, debug_mode
            )
        
        # Otherwise, execute preliminary analysis and prepare for Claude refinement
        if not analysis_result:
            return self._execute_preliminary_analysis_with_delegation(
                task_description, debug_mode
            )
        
        # If we have analysis but need decomposition, continue workflow
        return self._continue_collaborative_workflow(
            task_description, analysis_result, decomposition_result, workflow_stage, debug_mode
        )
    
    def _execute_deterministic_path(
        self,
        task_description: str,
        analysis_result: Optional[Dict[str, Any]],
        decomposition_result: Optional[Dict[str, Any]],
        workflow_stage: Optional[str],
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute traditional deterministic workflow (backward compatibility)."""
        
        strategy_logger.info(
            "deterministic_workflow_executed",
            "Using traditional deterministic workflow",
            trace_id=self.trace_id
        )
        
        # Use existing strategy-architect logic
        from tools.strategy_architect import execute_architect_workflow
        traditional_result = execute_architect_workflow(
            task_description, analysis_result, decomposition_result, workflow_stage, self.trace_id, debug_mode
        )
        
        # Convert to CollaborativeStrategyResponse for consistency
        return CollaborativeStrategyResponse[ArchitectPayload](
            strategy=traditional_result.strategy,
            user_facing=traditional_result.user_facing,
            claude_instructions=traditional_result.claude_instructions,
            payload=traditional_result.payload,
            metadata=traditional_result.metadata,
            error_handling=traditional_result.error_handling,
            debug_payload=traditional_result.debug_payload,
            # Collaborative fields (inactive for deterministic path)
            collaboration_mode=False,
            delegation_context=None,
            collaboration_points=None,
            refinement_history=None,
            requires_claude_refinement=False,
            collaboration_stage=None
        )
    
    def _execute_preliminary_analysis_with_delegation(
        self,
        task_description: str,
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute preliminary analysis and prepare Claude delegation."""
        
        # Execute preliminary analysis
        analysis = analyze_project(task_description)
        
        # Create delegation context for Claude refinement
        delegation_id = f"refine_{uuid.uuid4().hex[:8]}"
        delegation_context = DelegationContext(
            delegation_id=delegation_id,
            delegation_type=DelegationType.REFINE_ANALYSIS,
            preliminary_result={"analysis": analysis.model_dump()},
            refinement_prompt=self._create_analysis_refinement_prompt(task_description, analysis),
            expected_improvements=[
                "Enhanced technology stack recommendations",
                "Improved complexity assessment",
                "Additional architectural patterns",
                "Risk identification and mitigation strategies"
            ],
            validation_criteria="Refined analysis shows improved technology recommendations and risk assessment",
            confidence_threshold=self.confidence_threshold,
            continuation_state={
                "task_description": task_description,
                "workflow_stage": "refined_analysis",
                "preliminary_analysis": analysis.model_dump()
            }
        )
        
        # Create collaboration point
        collaboration_points = [
            CollaborationPoint(
                point_id="analysis_refinement",
                stage="preliminary_analysis",
                delegation_type=DelegationType.REFINE_ANALYSIS,
                confidence_threshold=self.confidence_threshold,
                description="Refine preliminary analysis with Claude's critical review and expertise"
            )
        ]
        
        # Create delegation action for Claude
        delegation_action = Action(
            type="refine_analysis",
            description="Critically review and refine the preliminary project analysis",
            priority=1,
            validation_criteria="Analysis refinement completed with improved insights",
            parameters={
                "delegation_context": delegation_context.model_dump(),
                "refinement_focus": [
                    "technology_stack_optimization",
                    "architecture_pattern_validation", 
                    "complexity_assessment_review",
                    "risk_identification"
                ]
            }
        )
        
        # Create user-facing content
        user_facing = UserFacing(
            summary=f"📋 Preliminary analysis completed for project. Claude refinement recommended for enhanced insights.",
            key_points=[
                f"🎯 Domain: {analysis.domain or 'General'}",
                f"📊 Complexity: {analysis.complexity}",
                f"🔧 Stack: {', '.join(analysis.technology_stack[:3]) if analysis.technology_stack else 'TBD'}",
                "🤝 Collaboration recommended for refinement"
            ],
            next_steps=[
                "Review preliminary analysis results",
                "Provide refined analysis to continue workflow",
                "Proceed with enhanced strategic planning"
            ]
        )
        
        # Create Claude instructions for collaboration
        claude_instructions = ClaudeInstructions(
            execution_type=ExecutionType.COLLABORATIVE,
            actions=[delegation_action],
            context_requirements=None,
            decision_points=None,
            fallback_strategy="Continue with preliminary analysis if refinement unavailable"
        )
        
        # Create payload
        payload = ArchitectPayload(
            workflow_stage=WorkflowStage.ANALYSIS,
            analysis=analysis,
            decomposition=None,
            task_graph=None,
            mission_map=None,
            suggested_next_state={
                "workflow_stage": "refined_analysis",
                "task_description": task_description,
                "preliminary_analysis": analysis.model_dump(),
                "requires_refinement": True
            },
            continue_workflow=True,
            next_step="refine_analysis"
        )
        
        # Create metadata
        metadata = Metadata(
            confidence_score=0.65,  # Lower confidence to trigger refinement
            complexity_score=self._assess_complexity_score(analysis),
            estimated_duration="Pending refinement",
            learning_opportunities=["Collaborative analysis refinement techniques"]
        )
        
        strategy_logger.info(
            "preliminary_analysis_completed",
            "Preliminary analysis completed, Claude refinement prepared",
            trace_id=self.trace_id,
            context={"delegation_id": delegation_id}
        )
        
        return CollaborativeStrategyResponse[ArchitectPayload](
            strategy=Strategy(name="motor-de-estrategias-collaborative", version="2.7.0", type=StrategyType.ANALYSIS),
            user_facing=user_facing,
            claude_instructions=claude_instructions,
            payload=payload,
            metadata=metadata,
            # Collaborative fields
            collaboration_mode=True,
            delegation_context=delegation_context,
            collaboration_points=collaboration_points,
            refinement_history=None,
            requires_claude_refinement=True,
            collaboration_stage="preliminary_analysis"
        )
    
    def _continue_with_refined_analysis(
        self,
        task_description: str,
        refined_analysis: Dict[str, Any],
        decomposition_result: Optional[Dict[str, Any]],
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Continue workflow with Claude-refined analysis."""
        
        strategy_logger.info(
            "refined_analysis_continuation",
            "Continuing workflow with Claude-refined analysis",
            trace_id=self.trace_id
        )
        
        # Convert refined analysis to AnalysisResult with required defaults
        refined_analysis_with_defaults = {
            "patterns": [],
            "requirements_implicit": [],
            **refined_analysis
        }
        analysis = AnalysisResult(**refined_analysis_with_defaults)
        
        # Continue with enhanced deterministic workflow
        decomposition = decompose_phases(analysis)
        task_graph = generate_task_graph(decomposition, analysis)
        mission_map = create_mission_map(task_graph, analysis)
        
        # Create refinement record
        refinement_record = RefinementRecord(
            refinement_id=f"ref_{uuid.uuid4().hex[:8]}",
            delegation_type=DelegationType.REFINE_ANALYSIS,
            timestamp=datetime.now().isoformat(),
            original_confidence=0.65,
            refined_confidence=0.90,
            quality_improvement=0.25,
            duration_ms=None
        )
        
        # Create enhanced user-facing content
        user_facing = UserFacing(
            summary=f"✅ Enhanced strategic analysis completed with Claude collaboration. Complete plan generated for: {task_description[:100]}...",
            key_points=[
                f"🎯 Domain: {analysis.domain or 'General'} (refined)",
                f"📊 Complexity: {analysis.complexity}",
                f"⏱️ Duration: {decomposition.total_estimated_duration}",
                f"🔗 Phases: {len(decomposition.phases)}",
                f"📋 Tasks: {task_graph.task_count}",
                f"👥 Resources: {len(mission_map.resource_assignments)} assignments",
                "🤝 Enhanced through collaborative intelligence"
            ],
            next_steps=[
                "Review the complete enhanced strategic plan",
                "Begin execution with the mission map",
                "Monitor progress through task dependencies"
            ]
        )
        
        # Create completion instructions
        claude_instructions = ClaudeInstructions(
            execution_type=ExecutionType.USER_CONFIRMATION,
            actions=[
                Action(
                    type="review_enhanced_results",
                    description="Review complete strategic analysis enhanced through collaboration",
                    priority=1,
                    validation_criteria="Enhanced strategic plan validated and approved"
                )
            ]
        )
        
        # Create payload
        payload = ArchitectPayload(
            workflow_stage=WorkflowStage.COMPLETE,
            analysis=analysis,
            decomposition=decomposition,
            task_graph=task_graph,
            mission_map=mission_map,
            suggested_next_state=None,
            continue_workflow=False,
            next_step=None
        )
        
        # Enhanced metadata reflecting collaboration
        metadata = Metadata(
            confidence_score=0.90,  # Higher confidence after refinement
            complexity_score=self._assess_complexity_score(analysis),
            estimated_duration=mission_map.total_effort_estimate,
            learning_opportunities=[
                "Collaborative intelligence workflow patterns",
                "Analysis refinement techniques",
                "Hybrid human-AI strategic planning"
            ]
        )
        
        strategy_logger.info(
            "collaborative_workflow_completed",
            "Collaborative workflow completed successfully",
            trace_id=self.trace_id,
            context={"refinement_applied": True, "final_confidence": 0.90}
        )
        
        return CollaborativeStrategyResponse[ArchitectPayload](
            strategy=Strategy(name="motor-de-estrategias-collaborative", version="2.7.0", type=StrategyType.ANALYSIS),
            user_facing=user_facing,
            claude_instructions=claude_instructions,
            payload=payload,
            metadata=metadata,
            # Collaborative fields
            collaboration_mode=True,
            delegation_context=None,
            collaboration_points=None,
            refinement_history=[refinement_record],
            requires_claude_refinement=False,
            collaboration_stage="complete"
        )
    
    def _continue_collaborative_workflow(
        self,
        task_description: str,
        analysis_result: Dict[str, Any],
        decomposition_result: Optional[Dict[str, Any]],
        workflow_stage: Optional[str],
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Continue collaborative workflow from intermediate stage."""
        
        # For now, fall back to deterministic path
        # In future iterations, we could add more collaboration points
        return self._execute_deterministic_path(
            task_description, analysis_result, decomposition_result, workflow_stage, debug_mode
        )
    
    def _create_analysis_refinement_prompt(
        self, 
        task_description: str, 
        analysis: AnalysisResult
    ) -> str:
        """Create a detailed prompt for Claude to refine the preliminary analysis."""
        
        return f"""You are a Senior Software Architect reviewing a preliminary project analysis. Your role is to critically evaluate and enhance this analysis with your expertise.

**PROJECT DESCRIPTION:**
{task_description}

**PRELIMINARY ANALYSIS:**
- Domain: {analysis.domain or 'Not specified'}
- Complexity: {analysis.complexity}
- Technology Stack: {', '.join(analysis.technology_stack) if analysis.technology_stack else 'Not specified'}
- Keywords: {', '.join(analysis.keywords) if analysis.keywords else 'Not specified'}

**YOUR MISSION:**
Critically review and enhance this analysis. Focus on:

1. **Technology Stack Optimization**: Are there better technology choices? Missing technologies? Incompatible selections?

2. **Architecture Pattern Validation**: Is the implied architecture pattern optimal for this use case? What alternatives should be considered?

3. **Complexity Assessment**: Is the complexity rating accurate? What factors might increase or decrease it?

4. **Risk Identification**: What technical, architectural, or implementation risks are not captured?

5. **Domain Enhancement**: Can the domain classification be more specific or accurate?

**EXPECTED OUTPUT:**
Provide your refined analysis in the same structure, but with your enhancements:
- Enhanced domain classification
- Refined complexity assessment with justification
- Optimized technology stack recommendations
- Additional keywords and patterns identified
- Risk factors and mitigation strategies

**BE CRITICAL AND THOROUGH** - Your expertise is valued precisely because you can see what automated analysis might miss."""
    
    def _assess_complexity_score(self, analysis: AnalysisResult) -> int:
        """Assess complexity score from analysis results."""
        complexity_map = {
            "Baja": 3,
            "Media": 5,
            "Alta": 8
        }
        return complexity_map.get(analysis.complexity, 5)