---
name: simplify-code
description: Code simplification, cleanup, and refactoring analysis. Use when finishing a feature, reviewing code quality, or when asked to simplify, clean up, refactor, or polish code. Supports analysis-only mode with severity ratings or action mode that makes changes directly.
---

# Code Simplification & Refactoring

Analyze and simplify code to produce clean, thoughtful, production-ready output.

## Modes

**Action mode (default)**: Analyze and fix issues directly
```
/simplify-code src/api/
```

**Analysis mode**: Report findings with severity, don't make changes
```
/simplify-code src/api/ --analyze
```

**Changed files**: Analyze files changed since branching from main
```
/simplify-code --changed
```

**Severity filter**: Only show/fix issues of certain severity
```
/simplify-code src/ --severity high
```

## Workflow

### 1. Identify Target Files

Parse the argument to determine what to analyze:

**File/directory path**: Read directly
```bash
/path/to/file.py
/path/to/feature/
```

**Git commit**: Extract changed files
```bash
git show --name-only <commit>
git diff <commit>^ <commit> --name-only
```

**--changed flag**: Files changed since main
```bash
git diff --name-only main...HEAD
```

**Description**: Search codebase for matching files

### 2. Analyze Each File

Read files and identify issues. See [references/patterns.md](references/patterns.md) for specific patterns.

**Categories and severity:**

| Category | HIGH | MEDIUM | LOW |
|----------|------|--------|-----|
| Dead code | Unused functions/classes | Unused imports/variables | Commented-out code |
| Complexity | >50 lines, >4 nesting, >6 params | 30-50 lines, 3-4 nesting | - |
| Duplication | Repeated logic blocks | Similar functions | - |
| Over-engineering | Unnecessary abstractions | Premature generalization | - |
| Naming | Misleading names | Inconsistent conventions | Single-letter vars |
| Structure | >500 line files | Mixed concerns | - |
| AI slop | Excessive error handling | Over-logging | Defensive copies |

### 3a. Analysis Mode (--analyze)

Present findings grouped by category:

```
## Refactoring Opportunities

### Dead Code (3 issues)
**[HIGH]** `src/api/routes.py:45` - Unused function `old_handler()`
  → Remove or determine if this should be called somewhere

**[MEDIUM]** `src/models/user.py:8` - Unused import `Optional`
  → Remove unused import

### Complexity (2 issues)
**[HIGH]** `src/services/processor.py:78-150` - Function `process_data()` is 72 lines
  → Extract helper functions for distinct operations

---
**Summary**: 5 issues (2 high, 2 medium, 1 low)
```

Then ask:
1. **Fix all issues** - Make the changes now
2. **Fix high-severity only** - Address critical issues, plan the rest
3. **Create plan file** - Write to `.planning/refactor-PLAN.md`
4. **Done** - Just wanted the analysis

### 3b. Action Mode (default)

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

**Action mode** - Report changes made:
```
Simplified 3 files:

src/auth/login.py
  - Removed unused import 'json'
  - Inlined single-use helper function
  - Simplified conditional chain

src/api/routes.py
  - Removed dead code block (unreachable after early return)
  - Combined duplicate validation logic
```

**Analysis mode** - Report findings with severity and offer next steps.

## Plan File Format

When creating a plan file (`.planning/refactor-YYYY-MM-DD-PLAN.md`):

```markdown
# Refactor Plan: [target]

Generated: [date]
Scope: [path or "changed files"]

## High Priority

- [ ] `file:line` - Description
  - How to fix

## Medium Priority

- [ ] `file:line` - Description
  - How to fix

## Low Priority

- [ ] `file:line` - Description
  - How to fix
```
