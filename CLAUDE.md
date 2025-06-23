# CLAUDE.md - Development Guidelines for CortexMCP

## 🚨 Core Philosophy

**TEST-DRIVEN DEVELOPMENT IS NON-NEGOTIABLE.** Every single line of production code must be written in response to a failing test. No exceptions. This is not a suggestion or a preference - it is the fundamental practice that enables all other principles in this document.

We follow Test-Driven Development (TDD) with a strong emphasis on behavior-driven testing and the **4 Principios Rectores** of CortexMCP. All work must be done in small, incremental changes that maintain a working, tested state throughout development.

## ⚡ Quick Reference

### Key Principles
- **Write tests first (TDD)** - Red → Green → Refactor, always
- **Test behavior, not implementation** - Test through `validate_and_execute()` only
- **Follow the 4 Principios Rectores** without exception
- **No `Any` types** - Use proper Pydantic models and type hints
- **Immutable responses** - StrategyResponse objects are never modified
- **Small, async functions** - Every tool method must be async
- **Use real schemas in tests** - Import from `schemas/`, never redefine

### The 4 Principios Rectores (MANDATORY)
1. **Dogmatismo con Universal Response Schema** - ALL tools MUST return StrategyResponse
2. **Servidor como Ejecutor Fiable** - server.py ONLY delegates, ZERO business logic
3. **Estado en Claude, NO en Servidor** - MCP is stateless, Claude maintains context
4. **Testing Concurrente** - Test continuously during development, not after

### Preferred Stack
- **Language**: Python 3.10+ (with type hints everywhere)
- **Testing**: pytest + pytest-asyncio + pytest-cov
- **Server Framework**: FastMCP
- **Validation**: Pydantic v2 (strict mode)
- **Type Checking**: mypy (strict mode)
- **Async Operations**: aiofiles for all file I/O
- **Dependency Management**: Poetry (NEVER pip directly)

## 🧪 Testing Principles

### Behavior-Driven Testing

**NO "UNIT TESTS"** - this term is banned. Tests verify expected behavior from the consumer's perspective, treating each tool as a black box.

#### What This Means for CortexMCP:
```python
# ❌ WRONG - Testing implementation details
async def test_get_template_opens_file():
    with patch('aiofiles.open') as mock_open:
        # This tests HOW it works, not WHAT it does
        
# ✅ CORRECT - Testing behavior
async def test_get_planning_template_returns_phase_preparation_structure():
    tool = PlanningTemplateTool()
    result = await tool.validate_and_execute(template_name="phase_preparation")
    
    assert result["strategy"]["type"] == "planning"
    assert "phase_name" in json.loads(result["payload"]["template_content"])
```

### Testing Rules

1. **Test ONLY through public API** - For tools, this means `validate_and_execute()`
2. **Never test private methods** - If `_create_error_response()` needs testing, extract it
3. **Test files organize by behavior** - Not 1:1 with implementation files
4. **Test names describe behavior** - `test_retrospective_creation_generates_timestamped_file()`
5. **Coverage target: 90%+** - But ONLY behavior coverage, not line coverage

### Testing Tools Configuration

```python
# pytest.ini
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "--cov=. --cov-report=term-missing --asyncio-mode=auto"

# Use these decorators
@pytest.mark.asyncio  # For all async tests
@patch('aiofiles.open')  # For mocking file operations
```

## 🏗️ CortexMCP-Specific Guidelines

### 1. Tool Development Pattern

**EVERY tool MUST follow this pattern:**

```python
class YourTool(BaseTool[YourPayloadType]):
    """Tool description following Google docstring style."""
    
    def __init__(self):
        """Initialize with tool name and version."""
        super().__init__("your-tool", "1.0.0")
    
    def get_strategy_type(self) -> StrategyType:
        """Return the strategy type - MANDATORY."""
        return StrategyType.PLANNING  # or ANALYSIS, LEARNING, etc.
    
    async def execute(self, **kwargs) -> StrategyResponse[YourPayloadType]:
        """Execute tool logic - MUST be async, MUST return StrategyResponse."""
        try:
            # Your async logic here
            payload = YourPayloadType(...)
            return self.create_success_response(...)
        except Exception as e:
            # Error handling automatic via BaseTool
            raise
```

### 2. Server Delegation Pattern

**server.py MUST ONLY delegate:**

```python
# ✅ CORRECT - Pure delegation
@app.tool("tool-name")
async def tool_name(param: str) -> Dict:
    """Pure delegation to tool."""
    tool = YourTool()
    return await tool.validate_and_execute(param=param)

# ❌ WRONG - Business logic in server
@app.tool("tool-name")
async def tool_name(param: str) -> Dict:
    """NEVER do this."""
    if param == "something":  # NO! Logic belongs in tool
        return {"result": "processed"}
```

### 3. Async All The Way

**EVERY file operation MUST use aiofiles:**

```python
# ❌ WRONG
with open(file_path, 'r') as f:
    content = f.read()

# ✅ CORRECT
async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
    content = await f.read()
```

### 4. Response Schema Discipline

**NEVER return raw dicts or strings from tools:**

```python
# ❌ WRONG
async def execute(self, **kwargs):
    return {"status": "success"}  # NO!

# ✅ CORRECT
async def execute(self, **kwargs) -> StrategyResponse[PayloadType]:
    return self.create_success_response(
        summary="Operation completed",
        payload=PayloadType(...),
        # All other required fields
    )
```

## 📝 Code Style Requirements

### Type Hints Are MANDATORY

```python
# ❌ WRONG
def process_data(data):
    return data.upper()

# ✅ CORRECT
def process_data(data: str) -> str:
    return data.upper()
```

### Docstrings Follow Google Style

```python
async def execute(self, task_name: str, **kwargs) -> StrategyResponse[PayloadType]:
    """Execute retrospective creation.
    
    Args:
        task_name: Name of the completed task
        **kwargs: Additional parameters
        
    Returns:
        StrategyResponse[PayloadType]: Structured response
        
    Raises:
        ValueError: If task_name is invalid
    """
```

### Error Messages Are User-Facing

```python
# ❌ WRONG
raise ValueError("t_name param missing")  # Cryptic

# ✅ CORRECT
raise ValueError("task_name must be provided and at least 3 characters long")
```

## 🚀 Development Workflow

### The ONLY Acceptable Workflow:

1. **Write a failing test** that describes the behavior you want
2. **Run the test** and watch it fail (Red)
3. **Write minimal code** to make the test pass (Green)
4. **Refactor** if needed, keeping tests green
5. **Commit** with descriptive message referencing the behavior added

### Example TDD Session:

```bash
# 1. Write test first
cat > tests/test_new_feature.py << EOF
async def test_knowledge_synthesis_creates_summary_artifact():
    tool = KnowledgeSynthesisTool()
    result = await tool.validate_and_execute(
        sources=["retro1.md", "retro2.md"]
    )
    assert result["payload"]["summary_file"].endswith("_synthesis.md")
EOF

# 2. Run and see it fail
poetry run pytest tests/test_new_feature.py -v  # RED

# 3. Implement minimal code
# ... write KnowledgeSynthesisTool in tools/

# 4. Run until green
poetry run pytest tests/test_new_feature.py -v  # GREEN

# 5. Check coverage
poetry run pytest --cov=tools --cov-report=term-missing

# 6. Run all quality checks
poetry run black .
poetry run mypy .
poetry run flake8 .

# 7. Commit
git add -A
git commit -m "feat: Add knowledge synthesis tool for retrospective summaries"
```

## 🛡️ Quality Gates (ALL MUST PASS)

Before ANY commit:
```bash
# Format code
poetry run black .

# Type check
poetry run mypy . --strict

# Lint
poetry run flake8 .

# Test with coverage
poetry run pytest --cov=. --cov-report=term-missing --cov-fail-under=90

# All async syntax check
grep -r "def.*await" . --include="*.py"  # Should find nothing
```

## ⚠️ Common Violations & Corrections

### Violation 1: Implementing in server.py
```python
# ❌ VIOLATION
# server.py
async def process_retrospective(file: str):
    content = await read_file(file)  # NO! Business logic
    return analyze(content)

# ✅ CORRECTION
# server.py
async def process_retrospective(file: str):
    tool = KnowledgeIntegrationTool()
    return await tool.validate_and_execute(retrospective_file=file)
```

### Violation 2: Sync operations in async context
```python
# ❌ VIOLATION
async def save_artifact(content: str):
    with open("file.txt", "w") as f:  # NO! Blocks event loop
        f.write(content)

# ✅ CORRECTION  
async def save_artifact(content: str):
    async with aiofiles.open("file.txt", "w") as f:
        await f.write(content)
```

### Violation 3: Testing implementation
```python
# ❌ VIOLATION
def test_internal_template_parsing():
    assert tool._parse_template_json("{}")  # NO! Private method

# ✅ CORRECTION
async def test_invalid_json_template_returns_error_response():
    tool = PlanningTemplateTool()
    result = await tool.validate_and_execute(template_name="corrupted")
    assert result["payload"]["workflow_stage"] == "error"
```

## 🎯 The CortexMCP Testing Manifesto

**We test behaviors, not code.**  
**We test outcomes, not methods.**  
**We test contracts, not implementations.**  
**We test async, always async.**  
**We test first, code second.**

Every test you write should answer: **"What behavior am I guaranteeing to Claude?"**

If you cannot answer this question, delete the test.

---

*This document is LAW. Violations will be caught in code review. No exceptions.*  
*Last updated: 2025-06-23*  
*Validated against: CortexMCP v2.8.5 BaseTool Architecture*