---
description: Enterprise-grade code audit with 5 parallel sub-agents covering plan compliance, security, code quality, architecture, and completeness
argument-hint: [plan-path or description of what to audit]
allowed-tools: Read, Glob, Grep, AskUserQuestion, Task, Skill
context: fork
---

<objective>
Execute a comprehensive code audit using 5 parallel sub-agents, compile findings into an actionable report, and optionally create a remediation plan.

**Input**: $ARGUMENTS (path to a plan file, or description of what to audit)

**Constraints**:
- NEVER implement code - audit and plan only
- NO fluff, NO compliments - only findings and actionable items
- "No issues found" is a valid outcome - don't manufacture findings
- All exploration happens in sub-agents to preserve context
- Plans saved alongside original plan with `-AUDIT` suffix
</objective>

<context>
Git status: !`git status --short`
Recent commits: !`git log --oneline -5`
Changed files: !`git diff --name-only HEAD~5 2>/dev/null || git diff --name-only`
</context>

<process>

## Phase 1: Determine Audit Scope

If $ARGUMENTS contains a file path, read it to understand the plan.
If $ARGUMENTS is a description, use it to identify relevant code.
If $ARGUMENTS is empty, use the git context above to identify recent changes.

Use AskUserQuestion to clarify scope if ambiguous:
- Which files/features to audit?
- Is there a specific plan this code should follow?
- Any known concerns to focus on?

## Phase 2: Launch 5 Parallel Sub-Agents

Launch ALL 5 agents in a SINGLE message using multiple Task tool calls. Each agent must:
- Focus ONLY on its assigned dimension
- Return specific findings with file paths and line numbers (if any)
- Provide severity (critical/high/medium/low) for each finding
- Suggest specific fixes (not implement them)
- Report "No issues found" if the code is genuinely sound - don't invent problems

### Agent 1: Plan Compliance
```
subagent_type: Explore
prompt: |
  AUDIT: Plan Compliance

  Plan/Spec: [include plan content or reference]
  Code to audit: [file paths]

  Check:
  1. Does implementation match the plan exactly?
  2. Are there missing features from the plan?
  3. Is there scope creep (code not in plan)?
  4. Are acceptance criteria met?

  Output format:
  ## Plan Compliance Findings

  ### Deviations
  - [file:line] Description (severity)

  ### Missing from Plan
  - Feature: [description]

  ### Scope Creep
  - [file:line] Code not in plan: [description]

  ### Verdict: PASS | FAIL | PARTIAL
```

### Agent 2: Security
```
subagent_type: Explore
prompt: |
  AUDIT: Security

  Code to audit: [file paths]

  Check for:
  1. OWASP Top 10 vulnerabilities
  2. Injection risks (SQL, command, XSS)
  3. Authentication/authorization issues
  4. Secrets or credentials in code
  5. Insecure dependencies
  6. Input validation gaps

  Output format:
  ## Security Findings

  ### Critical
  - [file:line] [vulnerability type] - Description
    Fix: [specific remediation]

  ### High/Medium/Low
  - [same format]

  ### Verdict: SECURE | VULNERABLE | NEEDS REVIEW
```

### Agent 3: Code Quality
```
subagent_type: Explore
prompt: |
  AUDIT: Code Quality

  Code to audit: [file paths]

  Check for:
  1. DRY violations (duplicated code)
  2. KISS violations (overcomplicated solutions)
  3. YAGNI violations (unused/speculative code)
  4. Poor naming (unclear variables, functions)
  5. Long functions (>50 lines)
  6. Deep nesting (>3 levels)
  7. Magic numbers/strings

  Output format:
  ## Code Quality Findings

  ### Complexity Issues
  - [file:line] Issue - Suggested simplification

  ### Duplication
  - [file:line] duplicates [file:line] - Extract to: [suggestion]

  ### Naming Issues
  - [file:line] `old_name` -> `suggested_name`

  ### Verdict: CLEAN | NEEDS REFACTOR | MESSY
```

### Agent 4: Architecture
```
subagent_type: Explore
prompt: |
  AUDIT: Architecture

  Code to audit: [file paths]

  Check for:
  1. Tight coupling between modules
  2. Circular dependencies
  3. Violation of single responsibility
  4. Missing abstractions
  5. Leaky abstractions
  6. Hard-coded dependencies (should be injected)
  7. Future extensibility blockers

  Output format:
  ## Architecture Findings

  ### Coupling Issues
  - [file] tightly coupled to [file] via [mechanism]
    Decouple by: [suggestion]

  ### Responsibility Violations
  - [file/class] does too much: [list responsibilities]
    Split into: [suggestions]

  ### Tech Debt Traps
  - [file:line] Will cause problems when: [scenario]

  ### Verdict: SOLID | NEEDS WORK | FRAGILE
```

### Agent 5: Completeness
```
subagent_type: Explore
prompt: |
  AUDIT: Completeness

  Code to audit: [file paths]

  Check for:
  1. Missing error handling
  2. Uncovered edge cases
  3. Missing input validation
  4. Incomplete test coverage
  5. Missing documentation for public APIs
  6. TODO/FIXME comments left behind
  7. Unhandled promise rejections / exceptions

  Output format:
  ## Completeness Findings

  ### Missing Error Handling
  - [file:line] [operation] can fail but isn't handled
    Add: [specific error handling]

  ### Edge Cases
  - [file:line] Doesn't handle: [edge case]

  ### Test Gaps
  - [file:function] Missing tests for: [scenarios]

  ### Verdict: COMPLETE | GAPS | INCOMPLETE
```

## Phase 3: Compile Report

After all agents return, compile findings into a single report:

```
# Audit Report: [scope description]
Date: [timestamp]
Files Audited: [count]

## Executive Summary
- Plan Compliance: [verdict]
- Security: [verdict]
- Code Quality: [verdict]
- Architecture: [verdict]
- Completeness: [verdict]

## Critical Issues (address immediately)
[List all critical/high severity findings]

## Medium Priority
[List medium findings]

## Low Priority / Suggestions
[List low findings]

## Metrics
- Total findings: X
- Critical: X | High: X | Medium: X | Low: X
```

## Phase 4: Offer Remediation Plan

Use AskUserQuestion:
- "Do you want me to create a remediation plan for these findings?"
- Options: All findings | Critical only | Specific categories | No plan needed

If yes, create the remediation plan:

**Naming convention**:
- If auditing a plan file: Replace `-PLAN.md` with `-AUDIT.md`
  - Example: `.planning/007-query-feature-PLAN.md` → `.planning/007-query-feature-AUDIT.md`
- If no plan file: `.planning/[scope-description]-AUDIT.md`
  - Example: `.planning/query-routes-AUDIT.md`

**Plan contents**:
- Group fixes by file to minimize context switches
- Prioritize by severity
- Include specific code changes needed (but DO NOT implement)
- Estimate complexity (simple/moderate/complex) for each fix

NEVER implement any code. Your job ends at the plan.
</process>

<success_criteria>
- All 5 sub-agents launched in parallel (single message)
- Each agent returns specific findings with file:line references (or confirms no issues)
- Report compiled with clear severity classifications
- Actionable items are specific enough to implement
- No implementation - audit and planning only
- No fluff or compliments - only genuine findings or "no issues"
</success_criteria>

<output>
**Report**: Displayed in conversation (not saved unless requested)
**Plan**: `.planning/[original-plan-name]-AUDIT.md` (only if approved)
</output>

<verification>
Before completing:
- Did all 5 agents return results?
- Are findings specific (file:line, not vague)?
- Is severity assigned to each finding?
- Are suggested fixes actionable?
- Was the user asked before creating any plan?
- Was NO code implemented?
</verification>
