# Phase 2.7: Collaborative Intelligence Architecture Design
*Hybrid Collaborative Intelligence Enhancement*
*Date: 2025-06-21 | Based on CortexMCP Strategic Plan*

---

## 🎯 **Architecture Overview**

### **Current State (Monolithic)**
```
Usuario → Claude → strategy-architect(descripción) → Plan Completo
```

### **Target State (Collaborative)**
```
1. Usuario → Claude: "Planifica API e-commerce"
2. Claude → MCP: strategy-architect(descripción)
3. MCP → Claude: AnalysisPreliminar + delegation("refine_analysis")
4. Claude: [PASO DE PENSAMIENTO] → Refinamiento crítico del análisis
5. Claude → MCP: strategy-architect(descripción, refined_analysis)
6. MCP → Claude: Plan Completo basado en análisis refinado
```

---

## 🔧 **Core Components Design**

### **1. Collaborative Workflow Controller**

**Location**: `tools/collaborative/workflow_controller.py`

**Purpose**: Orchestrate multi-step collaborative workflows with Claude intelligence injection

**Key Functions**:
```python
def detect_collaboration_points(
    task_description: str,
    current_stage: WorkflowStage
) -> List[CollaborationPoint]:
    """Identify where Claude intelligence injection would add value"""

def should_delegate_to_claude(
    analysis_result: AnalysisResult,
    confidence_threshold: float = 0.75
) -> bool:
    """Determine if Claude refinement is needed"""

def prepare_delegation_context(
    preliminary_analysis: AnalysisResult,
    delegation_type: DelegationType
) -> DelegationContext:
    """Prepare context for Claude delegation"""
```

### **2. Enhanced Action Types**

**Location**: `schemas/collaborative_actions.py`

**New Action Types**:
```python
class CollaborativeActionType(str, Enum):
    REFINE_ANALYSIS = "refine_analysis"
    VALIDATE_DEPENDENCIES = "validate_dependencies" 
    OPTIMIZE_ASSIGNMENT = "optimize_assignment"
    CRITICAL_REVIEW = "critical_review"
    ARCHITECTURE_ALTERNATIVES = "architecture_alternatives"
```

**Action Schemas**:
```python
class RefineAnalysisAction(BaseModel):
    type: Literal["refine_analysis"]
    preliminary_analysis: AnalysisResult
    refinement_prompt: str
    expected_improvements: List[str]
    validation_criteria: str

class ValidateDependenciesAction(BaseModel):
    type: Literal["validate_dependencies"]
    task_graph: TaskGraphResult
    critical_paths: List[str]
    validation_prompt: str
```

### **3. Delegation Engine**

**Location**: `tools/collaborative/delegation_engine.py`

**Purpose**: Handle delegation to Claude with structured prompts and context management

**Key Components**:
```python
class DelegationEngine:
    def create_delegation_response(
        self,
        delegation_type: DelegationType,
        context: DelegationContext,
        preliminary_result: Any
    ) -> StrategyResponse:
        """Create response that delegates to Claude"""

    def process_delegation_result(
        self,
        delegation_result: Dict[str, Any],
        original_context: DelegationContext
    ) -> RefinedResult:
        """Process Claude's delegation response"""
```

### **4. Refined Result Integration**

**Location**: `tools/collaborative/result_integration.py`

**Purpose**: Merge Claude's refinements with deterministic analysis

**Integration Patterns**:
```python
def merge_refined_analysis(
    preliminary: AnalysisResult,
    claude_refinements: Dict[str, Any]
) -> AnalysisResult:
    """Merge Claude refinements with preliminary analysis"""

def validate_refinement_quality(
    original: Any,
    refined: Any
) -> RefinementQuality:
    """Validate that refinements improve quality"""
```

---

## 🔄 **Workflow State Machine**

### **Collaborative States**
```python
class CollaborativeWorkflowStage(str, Enum):
    PRELIMINARY_ANALYSIS = "preliminary_analysis"
    CLAUDE_REFINEMENT = "claude_refinement"
    REFINED_ANALYSIS = "refined_analysis"
    COLLABORATIVE_DECOMPOSITION = "collaborative_decomposition"
    TASK_GRAPH_OPTIMIZATION = "task_graph_optimization"
    MISSION_MAP_FINALIZATION = "mission_map_finalization"
    COMPLETE = "complete"
```

### **State Transitions**
```
preliminary_analysis → claude_refinement → refined_analysis
    ↓
collaborative_decomposition → task_graph_optimization → mission_map_finalization
    ↓
complete
```

### **Delegation Decision Points**
1. **After Preliminary Analysis**: 
   - Low confidence (< 0.75) → Delegate to Claude
   - High confidence (≥ 0.75) → Continue deterministically

2. **During Task Graph Generation**:
   - Complex dependencies detected → Validate with Claude
   - Simple dependencies → Continue deterministically

3. **During Mission Map Creation**:
   - Resource conflicts detected → Optimize with Claude
   - Clear assignments → Continue deterministically

---

## 📋 **Updated Universal Response Schema**

### **Enhanced Execution Types**
```python
class CollaborativeExecutionType(str, Enum):
    IMMEDIATE = "immediate"           # Current functionality
    USER_CONFIRMATION = "user_confirmation"  # Current functionality
    MULTI_STEP = "multi_step"         # Current functionality
    DELEGATED = "delegated"           # Enhanced for collaboration
    COLLABORATIVE = "collaborative"   # NEW: Multi-step with Claude interaction
```

### **Delegation Context Schema**
```python
class DelegationContext(BaseModel):
    delegation_id: str
    delegation_type: DelegationType
    preliminary_result: Dict[str, Any]
    refinement_prompt: str
    expected_output_schema: Dict[str, Any]
    continuation_state: Dict[str, Any]
    confidence_threshold: float = 0.75
```

### **Enhanced StrategyResponse**
```python
# Add to existing StrategyResponse
class StrategyResponse(BaseModel, Generic[PayloadType]):
    # ... existing fields ...
    
    # NEW: Collaboration support
    delegation_context: Optional[DelegationContext] = None
    collaboration_stage: Optional[CollaborativeWorkflowStage] = None
    refinement_history: Optional[List[RefinementRecord]] = None
```

---

## 🎛️ **Configuration & Control**

### **Collaboration Configuration**
```python
class CollaborationConfig(BaseModel):
    enable_collaboration: bool = True
    confidence_threshold: float = 0.75
    max_refinement_iterations: int = 2
    delegation_timeout_seconds: int = 30
    auto_accept_high_confidence: bool = True
    
    # Collaboration points configuration
    analysis_refinement_enabled: bool = True
    dependency_validation_enabled: bool = True
    resource_optimization_enabled: bool = True
```

### **Backward Compatibility**
```python
# Environment variable control
CORTEX_COLLABORATION_MODE = os.getenv("CORTEX_COLLABORATION_MODE", "auto")
# Values: "disabled", "auto", "always"

# Auto mode: Use collaboration only when confidence < threshold
# Always mode: Always use collaboration (for testing)
# Disabled mode: Use original monolithic workflow
```

---

## 🔧 **Implementation Strategy**

### **Phase 1: Core Infrastructure** 
1. Create collaborative workflow controller
2. Implement delegation engine
3. Add enhanced action types to schema
4. Update StrategyResponse for delegation support

### **Phase 2: Integration Points**
1. Modify strategy-architect to detect collaboration points
2. Implement refinement integration
3. Add state management for collaborative workflows
4. Create delegation response formatting

### **Phase 3: Testing & Validation**
1. Unit tests for each collaborative component
2. Integration tests for full collaborative workflow
3. Performance benchmarks (must maintain <1.5s for simple cases)
4. Backward compatibility validation

### **Phase 4: Documentation & Deployment**
1. Update CLAUDE.md with collaboration philosophy
2. Create usage examples and best practices
3. Performance optimization
4. Production deployment validation

---

## 📊 **Success Metrics**

### **Functional Requirements**
- [ ] Collaborative workflow executes successfully
- [ ] Claude refinements integrate seamlessly
- [ ] Backward compatibility maintained (100%)
- [ ] Performance preserved for simple cases (<1.5s)

### **Quality Requirements**
- [ ] Refined analysis shows measurable improvement
- [ ] Collaboration adds value without overhead
- [ ] Error handling robust across delegation points
- [ ] State management reliable for multi-step workflows

### **Experience Requirements**
- [ ] Natural collaboration flow for Claude
- [ ] Clear delegation prompts and context
- [ ] Intuitive refinement integration
- [ ] Predictable workflow behavior

---

## 🎯 **Key Design Principles**

1. **Hybrid Intelligence**: Combine deterministic reliability with adaptive intelligence
2. **Graceful Degradation**: Fall back to monolithic mode if collaboration fails
3. **Transparent Collaboration**: Clear visibility into collaboration points and outcomes
4. **Stateless Continuity**: Maintain stateless design while supporting multi-step workflows
5. **Performance Preservation**: No performance regression for simple use cases
6. **Backward Compatibility**: 100% compatibility with existing functionality

---

**This architecture design provides the foundation for implementing truly collaborative intelligence while maintaining the reliability and performance of the existing Motor de Estrategias.**

*Next: Implementation of core collaborative components*