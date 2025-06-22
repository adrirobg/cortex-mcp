---
description: "Create session snapshot before /clear for context recovery"
allowed-tools: ["Write", "Read", "Bash"]
---

# Pre-Clear Session Snapshot

Create a session state snapshot to preserve context before using /clear command.

**Current Status**: $ARGUMENTS

## Actions to Execute:

1. **Create organized session snapshot**:
   - Create `.cortex/sessions/current_session.md` with complete context
   - Include current phase, blueprints, and recovery commands
   - Add timestamp and custom status message

2. **Update project references**:
   - Update `.cortex/config/project_profile.json` with current session info
   - Ensure all critical file paths are referenced

3. **Generate recovery commands**:
   - Provide exact Read commands for post-clear context recovery
   - Include direct continuation command for resuming work

**File Structure**:
```
.cortex/sessions/current_session.md  # Main session state
.cortex/config/project_profile.json  # Updated references
```

**Recovery Commands** (use after /clear):
```
Read .cortex/sessions/current_session.md
Read .cortex/config/project_profile.json
"Continue from where we left off using the session state"
```

Create this session snapshot now using the current project state and the provided status message.