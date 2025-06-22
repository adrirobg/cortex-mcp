# CLAUDE.md - CortexMCP External Cognitive Brain

**IMPORTANT: This configuration defines immutable operational rules for CortexMCP collaboration.**

---

## 🧠 Core Mission Statement

YOU MUST operate as Claude's **External Cognitive Brain** - amplifying strategic thinking through structured templates while preserving complete creative control.

**FUNDAMENTAL PRINCIPLE**: 
- **CortexMCP** = Provides structure, templates, persistence  
- **Claude** = Provides analysis, creativity, decisions
- **Never reverse these roles**

---

## 🔧 Current System Status

### Available Tools (Phase 2.8.5 MVP)
```bash
# ONLY these tools are operational:
get-planning-template    # Retrieves cognitive scaffolding
save-planning-artifact   # Persists structured results
```

**IMPORTANT**: Always use current Planning Toolkit tools, never reference old strategy-architect system.

---

## 🎯 Automatic Invocation Rules

### PRIMARY TRIGGERS (Use CortexMCP when user says):
- **"Plan"** / **"Planifica"** → `get-planning-template("phase_preparation")`
- **"Organize"** / **"Structure"** → `get-planning-template("phase_preparation")`  
- **"Design strategy"** → `get-planning-template("phase_preparation")`
- **Complex project descriptions (>50 words)** → Use Planning Toolkit workflow

### ANTI-PATTERNS (DO NOT use CortexMCP for):
- Simple 1-2 step tasks
- Code fixes or debugging  
- General conversation
- File reading or editing

---

## 📋 Planning Toolkit Workflow (EXACT STEPS)

### Step 1: Template Retrieval
```python
# When planning is needed:
get_planning_template("phase_preparation")
```

### Step 2: Cognitive Work (YOUR ROLE)
1. **Analyze** user requirements deeply
2. **Fill template** with strategic insights  
3. **Make decisions** on architecture, approach, timeline
4. **Structure thinking** using template as scaffolding

### Step 3: Artifact Persistence  
```python
# Save completed analysis:
save_planning_artifact("project_name_plan.json", filled_content)
save_planning_artifact("project_name_plan.md", readable_version)  # Optional
```

**IMPORTANT**: Always save artifacts - this creates external memory between sessions.

---

## 🏗️ Development Environment

### Environment Setup
```bash
# Project uses Poetry (NOT pip)
poetry install
poetry shell

# Run MCP server  
poetry run python server.py

# Verify functionality
poetry run python -c "from tools.planning_toolkit import get_planning_template; print('✅ Planning Toolkit operational')"
```

### Testing Commands
```bash
# CRITICAL: Run these before committing
poetry run pytest tests/                    # All tests
poetry run mypy .                          # Type checking  
poetry run black .                         # Code formatting
poetry run flake8 .                        # Style checking
```

**YOU MUST run tests and linting before any commits.**

---

## 📁 Project Structure (CURRENT)

```
server.py                           # MCP interface (only delegation)
├── get-planning-template           # → tools/planning_toolkit.py
└── save-planning-artifact          # → tools/planning_toolkit.py

tools/
├── planning_toolkit.py            # Core implementation  
├── knowledge_management.py        # Retrospective tools
└── base_tool.py                   # Base classes

.cortex/
├── templates/                      # Cognitive scaffolding
│   ├── phase_preparation.json     # Machine-readable structure
│   └── phase_preparation.md       # Human-readable guide  
└── artifacts/planning/             # Generated external memory
```

**IMPORTANT**: Templates are in `.cortex/templates/`, artifacts save to `.cortex/planning/`

---

## 🎨 Code Style & Quality Standards

### Python Code Standards
- **Type hints**: Required for all functions
- **Docstrings**: Google style for all modules/functions  
- **Error handling**: Comprehensive try/catch with logging
- **Imports**: Organized (stdlib, third-party, local)

### Architecture Principles  
1. **Servidor como Ejecutor Fiable**: server.py only delegates
2. **Zero Cognition in Tools**: Pure deterministic functions
3. **Stateless Design**: No data persistence between calls
4. **Template-Driven**: Structure guides, doesn't constrain

### Example Pattern (Follow This):
```python
# server.py - Pure delegation
@app.tool("tool-name")  
def tool_name(param: str) -> str:
    try:
        from tools.module import function
        return function(param)
    except Exception as e:
        logger.error(f"Delegation failed: {e}")
        raise ValueError(f"Tool execution failed: {e}")

# tools/module.py - Zero cognition implementation
def function(param: str) -> str:
    """Pure deterministic operation - no cognitive processing."""
    # Simple file operations, data processing, etc.
    return json.dumps({"status": "success", "result": result})
```

---

## 🧠 Cognitive Collaboration Patterns

### Template-Guided Cognition Process
1. **Receive template** → Structured JSON with empty fields
2. **Apply expertise** → Fill with strategic analysis and decisions  
3. **Maintain creativity** → Template guides, never constrains
4. **Generate insights** → Add value through cognitive work
5. **Create artifacts** → Persistent external memory

### Decision-Making Authority
- **YOU decide**: Architecture, technology choices, timelines
- **YOU analyze**: Requirements, risks, alternatives  
- **YOU structure**: Implementation approaches and phases
- **CortexMCP provides**: Templates, storage, organization

**IMPORTANT**: Never delegate cognitive decisions to CortexMCP tools.

---

## 📊 Success Metrics & Validation

### Per-Session Goals
- ✅ **Template Usage**: Use Planning Toolkit for complex tasks
- ✅ **Artifact Generation**: Create reusable planning documents  
- ✅ **Quality Consistency**: Apply systematic strategic thinking
- ✅ **Time Efficiency**: Reduce planning overhead through structure

### Workflow Validation
```bash
# Test complete workflow
1. Request: get-planning-template("phase_preparation")
2. Verify: Template retrieval successful  
3. Process: Fill template with analysis
4. Save: save-planning-artifact("test_plan.json", content)
5. Confirm: Artifact saved to .cortex/planning/
```

**IMPORTANT**: If workflow fails, debug using error messages and logs.

---

## 🚨 Critical Constraints & Boundaries

### File Access Rules
- **READ**: Any file in project repository
- **WRITE**: Only through save-planning-artifact tool  
- **MODIFY**: Use Edit/MultiEdit tools for code changes
- **CREATE**: New files via Write tool when necessary

### Security & Privacy
- **NO**: API keys, passwords, secrets in any artifacts
- **NO**: Personal information in planning documents
- **YES**: Technical specifications, architecture decisions  
- **YES**: Public information, open-source references

### Anti-Over-Engineering Guards
- **Keep tools simple**: Single responsibility functions
- **Avoid complexity**: No unnecessary abstractions  
- **Prove value first**: MVP before feature expansion
- **Measure impact**: Quantify improvements

---

## 🔄 Continuous Improvement Protocol

### Learning from Sessions  
1. **Note what works**: Effective planning patterns
2. **Identify gaps**: Missing template fields or guidance
3. **Suggest improvements**: Template or tool enhancements
4. **Document insights**: Use save-planning-artifact for meta-learning

### Error Recovery
```bash
# If tools fail:
1. Check server status: poetry run python server.py
2. Verify imports: from tools.planning_toolkit import *
3. Test manually: python -c "from tools.planning_toolkit import get_planning_template; print(get_planning_template('phase_preparation'))"
4. Report specific error message
```

---

## ⚡ Quick Reference Commands

### Most Used Operations
```bash
# Start server
poetry run python server.py

# Run tests  
poetry run pytest tests/

# Format code
poetry run black . && poetry run flake8 .

# Type check
poetry run mypy .
```

### Emergency Debugging
```bash
# Server logs
STRATEGY_LOG_LEVEL=debug poetry run python server.py

# Test specific component
poetry run pytest tests/test_planning_toolkit.py -v

# Manual tool test
poetry run python -c "from tools.planning_toolkit import get_planning_template; print(get_planning_template('phase_preparation'))"
```

---

## 🎯 Next Phase Roadmap

### Phase 2.8.6: Workflow Library Expansion
- **Add**: Code Review, Architecture Decision, Testing Strategy workflows
- **Pattern**: Follow existing Planning Toolkit blueprint  
- **Timeline**: 2-3 weeks

### Phase 2.9: Meta-Workflow Intelligence  
- **Add**: Template validation, workflow analytics
- **Innovation**: Meta-Workflow Generator (workflow to create workflows)
- **Timeline**: 1 month

**IMPORTANT**: Always follow Workflow Integration Blueprint for new additions.

---

*Updated: 2025-06-22*  
*Status: Planning Toolkit MVP ✅ OPERATIONAL*  
*Architecture: External Cognitive Brain - Proven & Validated*