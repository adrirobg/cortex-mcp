---
description: "Recover context after /clear command using session snapshots"
allowed-tools: ["Read"]
---

# Post-Clear Context Recovery

Restore complete project context automatically using preserved session state.

## Automatic Recovery Sequence:

1. **Read current session snapshot**:
   ```
   Read .cortex/sessions/current_session.md
   ```

2. **Load project profile** (contains all file references):
   ```
   Read .cortex/config/project_profile.json
   ```

3. **Follow session snapshot guidance**: 
   The `current_session.md` contains all necessary file paths and recovery commands. Extract and execute the file reads specified in the "ARCHIVOS CRÍTICOS PARA CONTINUIDAD" section.

4. **Execute continuation command**:
   Use the "COMANDO DIRECTO DE CONTINUACIÓN" provided in the session snapshot.

## What This Recovers:

- **Complete Context**: All preserved state from session snapshot
- **File References**: Dynamic paths from project profile and session
- **Work Queue**: Exact next steps from session guidance
- **Knowledge State**: Recent retrospectives and improvements
- **Phase Status**: Current and next phase information

## How It Works:

This command is designed to work with the output of `/project:save-session`. The session snapshot contains all the specific file paths and recovery instructions needed. Just read the two core files above, then follow the guidance within them.

**No hardcoded file paths** - everything is dynamically referenced through the session management system.