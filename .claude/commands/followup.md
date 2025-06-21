# Automated Follow-up Command

**Purpose**: Execute all automated follow-ups after completing meta-reflection analysis, ensuring no step is forgotten.

**Usage**: `/project:followup [phase-name]`

---

## 🔄 Automated Follow-up Checklist

**After completing ANY retrospective/meta-reflection analysis, Claude MUST execute these actions automatically:**

### **Action 1: Save Meta-Reflection Insights**
- Create `docs/meta-reflection_[phase-name].md` with complete analysis
- Include all 5 sections: Process Efficiency, Architecture, Bottlenecks, Improvements, Synthesis
- Add confidence score and validation methodology
- Include integration references

### **Action 2: Update Ideas Repository**  
- Add new improvement opportunities to `ideas/future_improvements.json`
- Assign unique IDs (imp_XXX format)
- Include priority scoring (effort, impact, score)
- Update metrics section (total count, categories, averages)
- Set source as "phase_X.X_meta_reflection"

### **Action 3: Strategy-Architect Planning**
- Identify highest-priority improvement (score ≥ 4.0) for circular workflow
- Provide strategic assessment of implementation readiness
- Consider integration potential with current phase
- Document strategic rationale for selection

### **Action 4: Prepare Next Phase Documentation**
- Create `docs/phase[X.X+1]_preparation.md` with optimized approach
- Incorporate all lessons learned from current and previous phases
- Apply process optimizations (TDD targets, configuration patterns, etc.)
- Include enhanced implementation strategy
- Set quantitative and qualitative success criteria

### **Action 5: Create TODO Items**
- Generate TODO list for all follow-up actions
- Mark items as completed as they are executed
- Include priorities and dependencies
- Ensure nothing is forgotten

---

## 📋 Implementation Template

```markdown
**Arguments**: $ARGUMENTS (phase name)

1. **Save insights** to `docs/meta-reflection_$ARGUMENTS.md`
2. **Update ideas** in `ideas/future_improvements.json` with new opportunities
3. **Consider strategy-architect** planning for highest-priority improvement
4. **Prepare next phase** documentation incorporating lessons learned
5. **Create TODOs** for tracking and validation

Execute all actions automatically in sequence, marking each as completed.
```

---

## 🎯 Quality Standards

**Each follow-up action must meet these standards:**

- **Completeness**: All required sections and fields populated
- **Accuracy**: Information reflects actual implementation results
- **Integration**: References to related files and previous phases
- **Actionability**: Clear next steps and implementation guidance
- **Consistency**: Maintains established formats and patterns

---

## 🚀 Usage Examples

```bash
# After completing Phase 2.3 retrospective
/project:followup phase2.3

# After completing Phase 2.4 retrospective  
/project:followup phase2.4

# After completing any feature retrospective
/project:followup feature-name
```

---

## ⚠️ Important Reminders

**FOR CLAUDE**: 
- **NEVER** skip automated follow-ups after retrospective
- **ALWAYS** execute all 5 actions in sequence
- **ALWAYS** create TODO items to track progress
- **ALWAYS** mark actions as completed when finished
- **REMEMBER** this is part of the circular improvement workflow

**The follow-up is NOT optional - it's a required part of every retrospective process.**

---

*Automated Follow-up Command*  
*Ensures Complete Circular Improvement Workflow*  
*No More Forgotten Follow-ups!*