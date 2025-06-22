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
    ArchitectPayload, WorkflowStage, StageCompletionStatus, AnalysisResult, DecompositionResult,
    TaskGraphResult, MissionMapResult
)
from tools.architect.analyze_project import analyze_project
from tools.architect.domain_heuristics import analyze_domain_indicators, DomainAnalysisResult
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
        """Execute collaborative workflow with Claude intelligence injection and stage-based execution.
        
        Args:
            task_description: Project description to analyze
            analysis_result: Previous analysis results (for continuation)
            decomposition_result: Previous decomposition results (for continuation)
            workflow_stage: Specific stage to execute ("analysis", "decomposition", "task_graph", "mission_map", or None for complete)
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
                "stage": workflow_stage or "complete_workflow",
                "has_refined_analysis": bool(refined_analysis)
            }
        )
        
        try:
            # Stage-based execution logic (Phase 2.8.1)
            if workflow_stage:
                return self._execute_stage_based_workflow(
                    task_description, analysis_result, decomposition_result,
                    workflow_stage, refined_analysis, debug_mode
                )
            
            # Backward compatibility: execute complete workflow when stage is None
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
        
        # Use collaborative workflow (eliminating traditional fallback)
        # Note: This fallback path is being eliminated in Phase 2.8.4-Prep consolidation
        # All workflows now use collaborative intelligence
        from tools.architect_unified import execute_architect_workflow
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
        # Handle case where refined_analysis might be a string instead of dict
        if isinstance(refined_analysis, str):
            # If it's a string, create a minimal dict structure
            refined_analysis = {
                "refined_insights": refined_analysis,
                "keywords": [],
                "patterns": [],
                "complexity": "medium",
                "requirements_implicit": []
            }
        
        refined_analysis_with_defaults = {
            "keywords": [],
            "patterns": [],
            "complexity": "medium",
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
    
    def _execute_stage_based_workflow(
        self,
        task_description: str,
        analysis_result: Optional[Dict[str, Any]],
        decomposition_result: Optional[Dict[str, Any]],
        workflow_stage: str,
        refined_analysis: Optional[Dict[str, Any]],
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute specific workflow stage based on workflow_stage parameter.
        
        Args:
            task_description: Project description to analyze
            analysis_result: Previous analysis results (for continuation)
            decomposition_result: Previous decomposition results (for continuation)
            workflow_stage: Specific stage to execute
            refined_analysis: Claude-refined analysis (for collaboration continuation)
            debug_mode: Enable debug information
            
        Returns:
            CollaborativeStrategyResponse with stage-specific results and next-stage guidance
        """
        strategy_logger.info(
            "stage_based_execution",
            f"Executing stage-based workflow: {workflow_stage}",
            trace_id=self.trace_id,
            context={"stage": workflow_stage}
        )
        
        # Validate stage parameter
        valid_stages = ["analysis", "decomposition", "task_graph", "mission_map", "complete", "clarification_needed"]
        if workflow_stage not in valid_stages:
            raise ValueError(f"Invalid workflow_stage: {workflow_stage}. Must be one of: {', '.join(valid_stages)}")
        
        # Execute specific stage
        if workflow_stage == "analysis":
            return self._execute_analysis_stage(task_description, debug_mode)
        elif workflow_stage == "decomposition":
            return self._execute_decomposition_stage(analysis_result, refined_analysis, debug_mode)
        elif workflow_stage == "task_graph":
            return self._execute_task_graph_stage(analysis_result, decomposition_result, refined_analysis, debug_mode)
        elif workflow_stage == "mission_map":
            return self._execute_mission_map_stage(analysis_result, decomposition_result, refined_analysis, debug_mode)
        elif workflow_stage == "complete":
            # Execute complete workflow as before
            return self._execute_complete_workflow(task_description, analysis_result, decomposition_result, refined_analysis, debug_mode)
        elif workflow_stage == "clarification_needed":
            return self._execute_clarification_stage(task_description, debug_mode)
        else:
            raise ValueError(f"Unhandled workflow stage: {workflow_stage}")
    
    def _execute_analysis_stage(
        self,
        task_description: str,
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute analysis stage with enhanced domain intelligence."""
        strategy_logger.info(
            "analysis_stage_execution",
            "Executing analysis stage with domain intelligence",
            trace_id=self.trace_id
        )
        
        # Execute domain analysis with multi-dimensional heuristics
        domain_analysis = analyze_domain_indicators(task_description)
        
        # Execute traditional project analysis
        analysis = analyze_project(task_description)
        
        # Enhance analysis with domain intelligence
        analysis.domain_analysis_context = domain_analysis.analysis_context
        analysis.domain_confidence_scores = domain_analysis.confidence_scores
        analysis.recommended_domain = domain_analysis.recommended_domain
        
        # Override domain if confidence is high enough
        if domain_analysis.max_confidence > 0.7:
            analysis.domain = domain_analysis.recommended_domain
            analysis.domain_decision_rationale = f"High confidence ({domain_analysis.max_confidence:.2f}) domain classification"
        else:
            analysis.domain_decision_rationale = f"Low confidence ({domain_analysis.max_confidence:.2f}) - may need clarification"
        
        # Check if collaborative domain selection is needed
        if domain_analysis.requires_collaboration:
            return self._execute_analysis_with_domain_collaboration(
                task_description, analysis, domain_analysis, debug_mode
            )
        
        # Create user-facing content
        user_facing = UserFacing(
            summary=f"📋 Analysis stage completed for: {task_description[:50]}...",
            key_points=[
                f"🎯 Domain: {analysis.domain or 'General'}",
                f"📊 Complexity: {analysis.complexity}",
                f"🔧 Stack: {', '.join(analysis.technology_stack[:3]) if analysis.technology_stack else 'TBD'}",
                "⏭️ Ready for decomposition stage"
            ],
            next_steps=[
                "Review analysis results",
                "Continue with decomposition stage",
                "Provide analysis_result to next stage"
            ]
        )
        
        # Create Claude instructions for next stage
        claude_instructions = ClaudeInstructions(
            execution_type=ExecutionType.IMMEDIATE,
            actions=[
                Action(
                    type="continue_workflow",
                    description="Continue with decomposition stage using analysis results",
                    priority=1,
                    validation_criteria="Analysis results validated and ready for decomposition"
                )
            ]
        )
        
        # Create payload with next-stage guidance
        payload = ArchitectPayload(
            workflow_stage=WorkflowStage.ANALYSIS,
            analysis=analysis,
            decomposition=None,
            task_graph=None,
            mission_map=None,
            suggested_next_state={
                "workflow_stage": "decomposition",
                "analysis_result": analysis.model_dump(),
                "task_description": task_description,
                "continue_workflow": True,
                "next_stage": "decomposition",
                "required_inputs": {
                    "analysis_result": "Results from analysis stage"
                },
                "estimated_duration": "Pending decomposition stage"
            },
            continue_workflow=True,
            next_step="decomposition",
            # Phase 2.8.1: Stage-specific fields
            current_stage="analysis",
            stage_completion_status=StageCompletionStatus.COMPLETED,
            next_stage_requirements=["analysis_result"]
        )
        
        # Create metadata
        metadata = Metadata(
            confidence_score=0.8,
            complexity_score=self._assess_complexity_score(analysis),
            estimated_duration="Analysis complete - proceed to decomposition",
            learning_opportunities=["Stage-based workflow execution"]
        )
        
        return CollaborativeStrategyResponse[ArchitectPayload](
            strategy=Strategy(name="motor-de-estrategias-staged", version="2.8.0", type=StrategyType.ANALYSIS),
            user_facing=user_facing,
            claude_instructions=claude_instructions,
            payload=payload,
            metadata=metadata,
            collaboration_mode=False,
            delegation_context=None,
            collaboration_points=None,
            refinement_history=None,
            requires_claude_refinement=False,
            collaboration_stage="analysis"
        )
    
    def _execute_analysis_with_domain_collaboration(
        self,
        task_description: str,
        analysis: AnalysisResult,
        domain_analysis: DomainAnalysisResult,
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute analysis stage with domain collaboration decision_point."""
        
        # Create decision point for domain selection
        decision_point = {
            "id": "domain_selection",
            "question": "Based on heuristic analysis, which domain best describes this project?",
            "options": [
                {
                    "id": option.domain_id,
                    "description": f"{option.domain_name} (confidence: {option.confidence_score:.1%})",
                    "impact": f"Supporting evidence: {', '.join(option.supporting_evidence[:2])}",
                    "concerns": option.potential_concerns[:1] if option.potential_concerns else []
                }
                for option in domain_analysis.domain_options[:4]  # Top 4 options
            ],
            "recommendation": domain_analysis.recommended_domain,
            "confidence": domain_analysis.max_confidence,
            "context": {
                "complexity_assessment": domain_analysis.analysis_context.complexity_assessment,
                "key_technologies": domain_analysis.analysis_context.technology_indicators[:3],
                "detected_patterns": list(domain_analysis.analysis_context.detected_keywords.keys())[:3]
            }
        }
        
        # Create delegation action for domain decision
        domain_decision_action = Action(
            type="evaluate_domain_options",
            description="Evaluate domain classification options and make informed decision",
            priority=1,
            validation_criteria="Domain selected and rationale provided",
            parameters={
                "decision_point": decision_point,
                "domain_analysis_context": domain_analysis.analysis_context.model_dump(),
                "decision_guidance": "Select the domain that best matches the project based on your understanding of the requirements and context"
            }
        )
        
        # Create user-facing content highlighting domain uncertainty
        user_facing = UserFacing(
            summary=f"📋 Analysis completed with domain uncertainty. Claude evaluation needed for optimal classification.",
            key_points=[
                f"🎯 Top Domain: {domain_analysis.recommended_domain} ({domain_analysis.max_confidence:.1%} confidence)",
                f"📊 Complexity: {analysis.complexity}",
                f"🔧 Technologies: {', '.join(domain_analysis.analysis_context.technology_indicators[:3])}",
                f"🤔 Confidence below threshold - collaboration recommended"
            ],
            next_steps=[
                "Review domain classification options",
                "Select the most appropriate domain based on project context",
                "Continue with enhanced analysis using selected domain"
            ]
        )
        
        # Create Claude instructions for domain collaboration
        claude_instructions = ClaudeInstructions(
            execution_type=ExecutionType.MULTI_STEP,
            actions=[domain_decision_action],
            decision_points=[decision_point],
            fallback_strategy="Use recommended domain if unable to make decision"
        )
        
        # Create payload with domain collaboration context
        payload = ArchitectPayload(
            workflow_stage=WorkflowStage.ANALYSIS,
            analysis=analysis,
            decomposition=None,
            task_graph=None,
            mission_map=None,
            suggested_next_state={
                "workflow_stage": "analysis_domain_refinement",
                "analysis_result": analysis.model_dump(),
                "domain_analysis_context": domain_analysis.analysis_context.model_dump(),
                "domain_options": [opt.model_dump() for opt in domain_analysis.domain_options],
                "requires_domain_decision": True,
                "task_description": task_description
            },
            continue_workflow=True,
            next_step="domain_decision",
            current_stage="analysis_domain_collaboration",
            stage_completion_status=StageCompletionStatus.PARTIAL,
            next_stage_requirements=["domain_decision"]
        )
        
        # Create metadata reflecting collaboration need
        metadata = Metadata(
            confidence_score=domain_analysis.max_confidence,
            complexity_score=self._assess_complexity_score(analysis),
            estimated_duration="Pending domain decision",
            learning_opportunities=["Collaborative domain classification", "Multi-dimensional heuristic analysis"]
        )
        
        strategy_logger.info(
            "domain_collaboration_initiated",
            f"Domain collaboration triggered - confidence {domain_analysis.max_confidence:.2f} below threshold",
            trace_id=self.trace_id,
            context={"domain_options": len(domain_analysis.domain_options)}
        )
        
        return CollaborativeStrategyResponse[ArchitectPayload](
            strategy=Strategy(name="motor-de-estrategias-domain-intelligence", version="2.8.2", type=StrategyType.ANALYSIS),
            user_facing=user_facing,
            claude_instructions=claude_instructions,
            payload=payload,
            metadata=metadata,
            collaboration_mode=True,
            delegation_context=None,
            collaboration_points=[
                CollaborationPoint(
                    point_id="domain_classification",
                    stage="analysis",
                    delegation_type=DelegationType.EVALUATE_OPTIONS,
                    confidence_threshold=0.7,
                    description="Evaluate domain classification options with full project context"
                )
            ],
            refinement_history=None,
            requires_claude_refinement=True,
            collaboration_stage="domain_selection"
        )
    
    def _execute_clarification_stage(
        self,
        task_description: str,
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute clarification stage for ambiguous project descriptions.
        
        Phase 2.8.3: Collaboration Point MVP Implementation
        This stage is triggered when domain confidence is below threshold and 
        the system needs user clarification to provide optimal strategic planning.
        
        Args:
            task_description: Project description requiring clarification
            debug_mode: Enable debug information
            
        Returns:
            CollaborativeStrategyResponse with clarification request and domain options
        """
        strategy_logger.info(
            "clarification_stage_execution",
            "Executing clarification stage for ambiguous project description",
            trace_id=self.trace_id
        )
        
        # Execute domain analysis using existing Phase 2.8.2 heuristics
        domain_analysis = analyze_domain_indicators(task_description)
        
        # Execute basic project analysis for context
        analysis = analyze_project(task_description)
        
        # Enhance analysis with domain intelligence context
        analysis.domain_analysis_context = domain_analysis.analysis_context
        analysis.domain_confidence_scores = domain_analysis.confidence_scores
        analysis.recommended_domain = domain_analysis.recommended_domain
        analysis.domain_decision_rationale = f"Clarification needed - confidence {domain_analysis.max_confidence:.2f} below threshold"
        
        # Create clarification decision point using proper DecisionPoint schema
        from schemas.universal_response import DecisionPoint
        
        clarification_decision_point = DecisionPoint(
            id="clarification_request",
            question=f"I need clarification to provide optimal strategic planning for your project. Based on analysis, I detected multiple possible interpretations:",
            options=[
                {
                    "id": option.domain_id,
                    "description": f"{option.domain_name}",
                    "impact": f"Confidence: {option.confidence_score:.1%} - {', '.join(option.supporting_evidence[:2]) if option.supporting_evidence else 'General software approach'}",
                    "concerns": option.potential_concerns[:1] if option.potential_concerns else []
                }
                for option in domain_analysis.domain_options[:4]  # Top 4 options for clarity
            ],
            recommendation=domain_analysis.recommended_domain,
            confidence=domain_analysis.max_confidence
        )
        
        # Create clarification action for Claude
        clarification_action = Action(
            type="request_clarification",
            description="Request user clarification to improve strategic planning accuracy",
            priority=1,
            validation_criteria="User provides clarification that enables confident domain classification",
            parameters={
                "decision_point": clarification_decision_point.model_dump(),
                "clarification_guidance": "Ask the user specific questions to clarify the project type and requirements",
                "next_workflow_stage": "analysis",
                "ambiguity_sources": [
                    f"Domain confidence below threshold ({domain_analysis.max_confidence:.1%} < 70%)",
                    f"Multiple possible domains detected: {len(domain_analysis.domain_options)}",
                    f"Technology indicators: {', '.join(domain_analysis.analysis_context.technology_indicators[:3]) if domain_analysis.analysis_context.technology_indicators else 'unclear'}"
                ],
                "suggested_clarifications": [
                    "What type of application are you building?",
                    "What programming language or technology stack do you prefer?",
                    "Is this for web, mobile, command-line, or another platform?",
                    "What is the main purpose or goal of this project?"
                ]
            }
        )
        
        # Create user-facing content for clarification request
        user_facing = UserFacing(
            summary=f"🤔 Need clarification to provide optimal strategic planning",
            key_points=[
                f"📊 Analysis confidence: {domain_analysis.max_confidence:.1%} (below 70% threshold)",
                f"🎯 Top possibilities: {', '.join([opt.domain_name for opt in domain_analysis.domain_options[:3]])}",
                f"🔧 Detected technologies: {', '.join(domain_analysis.analysis_context.technology_indicators[:3]) if domain_analysis.analysis_context.technology_indicators else 'unclear'}",
                "❓ Clarification will improve planning accuracy and relevance"
            ],
            next_steps=[
                "Review the detected domain options below",
                "Answer clarification questions to narrow down project type", 
                "Provide additional context about your specific requirements",
                "Continue with enhanced analysis after clarification"
            ]
        )
        
        # Create Claude instructions for clarification workflow
        claude_instructions = ClaudeInstructions(
            execution_type=ExecutionType.USER_CONFIRMATION,
            actions=[clarification_action],
            decision_points=[clarification_decision_point],
            fallback_strategy="Use highest confidence domain if clarification cannot be obtained"
        )
        
        # Create payload with clarification context
        payload = ArchitectPayload(
            workflow_stage=WorkflowStage.CLARIFICATION_NEEDED,
            analysis=analysis,
            decomposition=None,
            task_graph=None,
            mission_map=None,
            suggested_next_state={
                "workflow_stage": "analysis",
                "task_description": task_description,
                "domain_analysis_context": domain_analysis.analysis_context.model_dump(),
                "domain_options": [opt.model_dump() for opt in domain_analysis.domain_options],
                "requires_clarification": True,
                "clarification_completed": False
            },
            continue_workflow=False,  # Workflow pauses for user clarification
            next_step="user_clarification",
            current_stage="clarification_needed",
            stage_completion_status=StageCompletionStatus.PARTIAL,
            next_stage_requirements=["user_clarification", "domain_selection"]
        )
        
        # Create metadata reflecting clarification need
        metadata = Metadata(
            confidence_score=domain_analysis.max_confidence,
            complexity_score=self._assess_complexity_score(analysis),
            estimated_duration="Pending user clarification",
            learning_opportunities=["Collaborative clarification workflow", "Confidence-driven collaboration triggers"]
        )
        
        strategy_logger.info(
            "clarification_request_generated",
            f"Clarification request generated for low confidence task - {domain_analysis.max_confidence:.2f} confidence",
            trace_id=self.trace_id,
            context={
                "domain_options_count": len(domain_analysis.domain_options),
                "confidence_threshold": 0.7,
                "requires_collaboration": domain_analysis.requires_collaboration
            }
        )
        
        return CollaborativeStrategyResponse[ArchitectPayload](
            strategy=Strategy(name="motor-de-estrategias-clarification", version="2.8.3", type=StrategyType.ANALYSIS),
            user_facing=user_facing,
            claude_instructions=claude_instructions,
            payload=payload,
            metadata=metadata,
            collaboration_mode=True,
            delegation_context=None,
            collaboration_points=[
                CollaborationPoint(
                    point_id="project_clarification",
                    stage="clarification_needed",
                    delegation_type=DelegationType.EVALUATE_OPTIONS,
                    confidence_threshold=0.7,
                    description="Request user clarification for ambiguous project descriptions"
                )
            ],
            refinement_history=None,
            requires_claude_refinement=False,  # This IS the clarification stage
            collaboration_stage="clarification_request"
        )
    
    def _execute_decomposition_stage(
        self,
        analysis_result: Optional[Dict[str, Any]],
        refined_analysis: Optional[Dict[str, Any]],
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute decomposition stage only."""
        strategy_logger.info(
            "decomposition_stage_execution",
            "Executing decomposition stage",
            trace_id=self.trace_id
        )
        
        # Validate required inputs
        if not analysis_result and not refined_analysis:
            raise ValueError("analysis_result is required for decomposition stage")
        
        # Use refined analysis if available, otherwise use analysis_result
        analysis_data = refined_analysis if refined_analysis else analysis_result
        analysis = AnalysisResult(**analysis_data)
        
        # Execute decomposition
        decomposition = decompose_phases(analysis)
        
        # Create user-facing content
        user_facing = UserFacing(
            summary=f"🏗️ Decomposition stage completed. Project broken into {len(decomposition.phases)} phases.",
            key_points=[
                f"🔗 Phases: {len(decomposition.phases)}",
                f"⏱️ Duration: {decomposition.total_estimated_duration}",
                f"📈 Critical Path: {len(decomposition.critical_path)} phases",
                "⏭️ Ready for task graph generation"
            ],
            next_steps=[
                "Review phase breakdown",
                "Continue with task graph stage",
                "Provide decomposition_result to next stage"
            ]
        )
        
        # Create Claude instructions for next stage
        claude_instructions = ClaudeInstructions(
            execution_type=ExecutionType.IMMEDIATE,
            actions=[
                Action(
                    type="continue_workflow",
                    description="Continue with task graph stage using decomposition results",
                    priority=1,
                    validation_criteria="Decomposition results validated and ready for task graph"
                )
            ]
        )
        
        # Create payload with next-stage guidance
        payload = ArchitectPayload(
            workflow_stage=WorkflowStage.DECOMPOSITION,
            analysis=analysis,
            decomposition=decomposition,
            task_graph=None,
            mission_map=None,
            suggested_next_state={
                "workflow_stage": "task_graph",
                "analysis_result": analysis.model_dump(),
                "decomposition_result": decomposition.model_dump(),
                "continue_workflow": True,
                "next_stage": "task_graph",
                "required_inputs": {
                    "analysis_result": "Results from analysis stage",
                    "decomposition_result": "Results from decomposition stage"
                },
                "estimated_duration": decomposition.total_estimated_duration
            },
            continue_workflow=True,
            next_step="task_graph",
            # Phase 2.8.1: Stage-specific fields
            current_stage="decomposition",
            stage_completion_status=StageCompletionStatus.COMPLETED,
            next_stage_requirements=["analysis_result", "decomposition_result"]
        )
        
        # Create metadata
        metadata = Metadata(
            confidence_score=0.85,
            complexity_score=self._assess_complexity_score(analysis),
            estimated_duration=decomposition.total_estimated_duration,
            learning_opportunities=["Phase decomposition techniques"]
        )
        
        return CollaborativeStrategyResponse[ArchitectPayload](
            strategy=Strategy(name="motor-de-estrategias-staged", version="2.8.0", type=StrategyType.ANALYSIS),
            user_facing=user_facing,
            claude_instructions=claude_instructions,
            payload=payload,
            metadata=metadata,
            collaboration_mode=False,
            delegation_context=None,
            collaboration_points=None,
            refinement_history=None,
            requires_claude_refinement=False,
            collaboration_stage="decomposition"
        )
    
    def _execute_task_graph_stage(
        self,
        analysis_result: Optional[Dict[str, Any]],
        decomposition_result: Optional[Dict[str, Any]],
        refined_analysis: Optional[Dict[str, Any]],
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute task graph stage only."""
        strategy_logger.info(
            "task_graph_stage_execution",
            "Executing task graph stage",
            trace_id=self.trace_id
        )
        
        # Validate required inputs
        if not decomposition_result:
            raise ValueError("decomposition_result is required for task_graph stage")
        if not analysis_result and not refined_analysis:
            raise ValueError("analysis_result is required for task_graph stage")
        
        # Use refined analysis if available, otherwise use analysis_result
        analysis_data = refined_analysis if refined_analysis else analysis_result
        analysis = AnalysisResult(**analysis_data)
        decomposition = DecompositionResult(**decomposition_result)
        
        # Execute task graph generation
        task_graph = generate_task_graph(decomposition, analysis)
        
        # Create user-facing content
        user_facing = UserFacing(
            summary=f"📊 Task graph stage completed. Generated {task_graph.task_count} interconnected tasks.",
            key_points=[
                f"📋 Tasks: {task_graph.task_count}",
                f"🔗 Dependencies: {len([t for t in task_graph.tasks if t.dependencies])} tasks have dependencies",
                f"🚧 Bottlenecks: {len(task_graph.bottlenecks)} identified",
                "⏭️ Ready for mission map generation"
            ],
            next_steps=[
                "Review task graph and dependencies",
                "Continue with mission map stage",
                "Validate task complexity estimates"
            ]
        )
        
        # Create Claude instructions for next stage
        claude_instructions = ClaudeInstructions(
            execution_type=ExecutionType.IMMEDIATE,
            actions=[
                Action(
                    type="continue_workflow",
                    description="Continue with mission map stage using task graph results",
                    priority=1,
                    validation_criteria="Task graph validated and ready for mission map"
                )
            ]
        )
        
        # Create payload with next-stage guidance
        payload = ArchitectPayload(
            workflow_stage=WorkflowStage.TASK_GRAPH,
            analysis=analysis,
            decomposition=decomposition,
            task_graph=task_graph,
            mission_map=None,
            suggested_next_state={
                "workflow_stage": "mission_map",
                "analysis_result": analysis.model_dump(),
                "decomposition_result": decomposition.model_dump(),
                "task_graph_result": task_graph.model_dump(),
                "continue_workflow": True,
                "next_stage": "mission_map",
                "required_inputs": {
                    "analysis_result": "Results from analysis stage",
                    "decomposition_result": "Results from decomposition stage",
                    "task_graph_result": "Results from task graph stage"
                },
                "estimated_duration": "Pending mission map creation"
            },
            continue_workflow=True,
            next_step="mission_map",
            # Phase 2.8.1: Stage-specific fields
            current_stage="task_graph",
            stage_completion_status=StageCompletionStatus.COMPLETED,
            next_stage_requirements=["analysis_result", "decomposition_result", "task_graph_result"]
        )
        
        # Create metadata
        metadata = Metadata(
            confidence_score=0.85,
            complexity_score=self._assess_complexity_score(analysis),
            estimated_duration="Task graph complete - proceed to mission map",
            learning_opportunities=["Task dependency analysis", "Critical path optimization"]
        )
        
        return CollaborativeStrategyResponse[ArchitectPayload](
            strategy=Strategy(name="motor-de-estrategias-staged", version="2.8.0", type=StrategyType.ANALYSIS),
            user_facing=user_facing,
            claude_instructions=claude_instructions,
            payload=payload,
            metadata=metadata,
            collaboration_mode=False,
            delegation_context=None,
            collaboration_points=None,
            refinement_history=None,
            requires_claude_refinement=False,
            collaboration_stage="task_graph"
        )
    
    def _execute_mission_map_stage(
        self,
        analysis_result: Optional[Dict[str, Any]],
        decomposition_result: Optional[Dict[str, Any]],
        refined_analysis: Optional[Dict[str, Any]],
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute mission map stage only."""
        strategy_logger.info(
            "mission_map_stage_execution",
            "Executing mission map stage",
            trace_id=self.trace_id
        )
        
        # Validate required inputs
        if not decomposition_result:
            raise ValueError("decomposition_result is required for mission_map stage")
        if not analysis_result and not refined_analysis:
            raise ValueError("analysis_result is required for mission_map stage")
        
        # Use refined analysis if available, otherwise use analysis_result
        analysis_data = refined_analysis if refined_analysis else analysis_result
        analysis = AnalysisResult(**analysis_data)
        decomposition = DecompositionResult(**decomposition_result)
        
        # Generate task graph if not provided (mission map depends on it)
        task_graph = generate_task_graph(decomposition, analysis)
        
        # Execute mission map creation
        mission_map = create_mission_map(task_graph, analysis)
        
        # Create user-facing content
        user_facing = UserFacing(
            summary=f"🎯 Mission map stage completed. Strategic plan finalized with {len(mission_map.resource_assignments)} resource assignments.",
            key_points=[
                f"👥 Resources: {len(mission_map.resource_assignments)} assignments",
                f"⏱️ Total Effort: {mission_map.total_effort_estimate}",
                f"🔄 Execution Order: {len(mission_map.execution_order)} steps",
                "✅ Stage-based workflow complete"
            ],
            next_steps=[
                "Review complete mission map",
                "Begin execution following the mission plan",
                "Monitor resource utilization and progress"
            ]
        )
        
        # Create completion instructions
        claude_instructions = ClaudeInstructions(
            execution_type=ExecutionType.USER_CONFIRMATION,
            actions=[
                Action(
                    type="review_mission_map",
                    description="Review complete mission map and execution plan",
                    priority=1,
                    validation_criteria="Mission map validated and approved for execution"
                )
            ]
        )
        
        # Create final payload
        payload = ArchitectPayload(
            workflow_stage=WorkflowStage.MISSION_MAP,
            analysis=analysis,
            decomposition=decomposition,
            task_graph=task_graph,
            mission_map=mission_map,
            suggested_next_state=None,  # Workflow complete
            continue_workflow=False,
            next_step=None,
            # Phase 2.8.1: Stage-specific fields
            current_stage="mission_map",
            stage_completion_status=StageCompletionStatus.COMPLETED,
            next_stage_requirements=None  # No next stage - workflow complete
        )
        
        # Create metadata
        metadata = Metadata(
            confidence_score=0.9,
            complexity_score=self._assess_complexity_score(analysis),
            estimated_duration=mission_map.total_effort_estimate,
            learning_opportunities=["Resource allocation optimization", "Stage-based strategic planning"]
        )
        
        return CollaborativeStrategyResponse[ArchitectPayload](
            strategy=Strategy(name="motor-de-estrategias-staged", version="2.8.0", type=StrategyType.ANALYSIS),
            user_facing=user_facing,
            claude_instructions=claude_instructions,
            payload=payload,
            metadata=metadata,
            collaboration_mode=False,
            delegation_context=None,
            collaboration_points=None,
            refinement_history=None,
            requires_claude_refinement=False,
            collaboration_stage="mission_map"
        )
    
    def _execute_complete_workflow(
        self,
        task_description: str,
        analysis_result: Optional[Dict[str, Any]],
        decomposition_result: Optional[Dict[str, Any]],
        refined_analysis: Optional[Dict[str, Any]],
        debug_mode: bool
    ) -> CollaborativeStrategyResponse[ArchitectPayload]:
        """Execute complete workflow when stage='complete' is specified."""
        # Fall back to existing collaborative or deterministic path
        if self._should_use_collaboration(task_description, analysis_result, refined_analysis):
            return self._execute_collaborative_path(
                task_description, analysis_result, decomposition_result,
                None, refined_analysis, debug_mode
            )
        else:
            return self._execute_deterministic_path(
                task_description, analysis_result, decomposition_result,
                None, debug_mode
            )