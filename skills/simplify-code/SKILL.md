---
name: simplify-code
description: Code simplification and cleanup after feature development. Use when finishing a feature, reviewing code quality, or when asked to simplify, clean up, or polish code. Accepts file paths, directory paths, git commits, or descriptions of where to find files. Removes redundancy, duplication, dead code, AI slop, and unnecessary complexity while ensuring code is clean, clear, and passes linting.
---

# Code Simplification

Analyze and simplify code to produce clean, thoughtful, production-ready output.

## Workflow

### 1. Identify Target Files

Parse the argument to determine what to analyze:

**File/directory path**: Read directly
```bash
# Single file
/path/to/file.py

# Directory (glob for code files)
/path/to/feature/
```

**Git commit**: Extract changed files
```bash
git show --name-only <commit>
git diff <commit>^ <commit> --name-only
```

**Description**: Search codebase for matching files
```bash
# "the auth module" → search for auth-related files
grep -r "auth" --include="*.py" -l
```

### 2. Analyze Each File

Read files and identify issues. See [references/patterns.md](references/patterns.md) for specific patterns.

**Priority order** (fix highest impact first):
1. Dead code (unused imports, functions, variables)
2. Duplication (repeated logic that should be extracted)
3. Over-engineering (abstractions without justification)
4. Verbose patterns (can be expressed more concisely)
5. Redundant comments (stating the obvious)
6. Inconsistent style (naming, formatting)

### 3. Apply Simplifications

Make changes using the Edit tool. For each change:
- Explain what's being simplified and why
- Show before/after when helpful
- Preserve behavior exactly (no functional changes)

### 4. Verify

After all changes:
```bash
make lint  # or project-specific lint command
```

Fix any lint errors introduced.

## Anti-Patterns to Remove

### AI Slop
- Excessive error handling for impossible cases
- Overly defensive programming
- Unnecessary abstractions "for flexibility"
- Feature flags for single-use code
- Backwards compatibility for code that was just written

### Over-Engineering
- Interfaces with single implementations
- Factory patterns for simple construction
- Strategy patterns for single strategies
- Dependency injection where simple imports work

### Redundant Comments
```python
# BAD: States the obvious
def get_user(id):
    # Get the user by ID
    return db.users.find(id)

# GOOD: Explains why, not what
def get_user(id):
    # Uses cached lookup for hot path
    return cache.get(f"user:{id}") or db.users.find(id)
```

### Verbose Patterns
```python
# BAD
if condition == True:
    return True
else:
    return False

# GOOD
return condition
```

## What to Preserve

- **Intentional complexity**: Sometimes verbose is clearer
- **Performance optimizations**: May look complex for good reason
- **Error handling at boundaries**: API/user input validation is necessary
- **Comments explaining "why"**: Non-obvious decisions
- **Type hints**: Keep them, they help

## Output

Report changes made:
```
Simplified 3 files:

src/auth/login.py
  - Removed unused import 'json'
  - Inlined single-use helper function
  - Simplified conditional chain

src/api/routes.py
  - Removed dead code block (unreachable after early return)
  - Combined duplicate validation logic

src/models/user.py
  - Removed redundant comments
```
