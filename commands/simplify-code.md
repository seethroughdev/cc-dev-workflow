---
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion, Task, Skill
description: Simplify and clean up code - remove redundancy, dead code, AI slop, and unnecessary complexity
argument-hint: <path|commit|description>
---

# Code Simplification

Activate the `simplify-code` skill to analyze and simplify code.

## Target

$ARGUMENTS

## Instructions

1. Parse the target above to identify files:
   - **Path**: Read the file or glob directory for code files
   - **Git commit**: Run `git show --name-only <commit>` to get changed files
   - **Description**: Search the codebase to find matching files

2. Read the patterns reference file at `skills/simplify-code/references/patterns.md` for specific patterns to identify

3. For each file, analyze and fix (in priority order):
   - Dead code (unused imports, functions, variables, unreachable code)
   - Duplication (extract repeated logic)
   - Over-engineering (remove unnecessary abstractions)
   - Verbose patterns (simplify conditionals, string building)
   - Redundant comments (remove obvious ones, keep "why" explanations)
   - AI slop (excessive error handling, defensive programming, over-logging)

4. After changes, run linting:
   ```bash
   make lint
   ```

5. Report all changes made with a summary per file
