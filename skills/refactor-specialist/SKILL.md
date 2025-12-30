---
name: refactor-specialist
description: Analyzes code for refactoring opportunities including dead code, complexity, duplication, naming issues, and structural problems. Use after completing a feature or when cleaning up a codebase section.
---

<objective>
Find refactoring opportunities in code without security or correctness concerns. Focus on cleanup, polish, and maintainability improvements that make code easier to understand and modify.
</objective>

<quick_start>
Analyze a path:
```
/refactor src/api/
```

Analyze files changed since branching from main:
```
/refactor --changed
```

Filter by severity:
```
/refactor src/ --severity high
```
</quick_start>

<process>
<step_1>
**Parse arguments**

Determine target:
- If `--changed` flag: Get files changed since branching from main (`git diff --name-only main...HEAD`)
- Otherwise: Use provided path (file or directory)

Check for `--severity` filter (high, medium, low, or all). Default: all.
</step_1>

<step_2>
**Analyze each category**

For each file in scope, search for issues in these categories:

**Dead Code** (typically HIGH severity)
- Unused imports (imported but never referenced)
- Unused functions/methods (defined but never called)
- Unused variables (assigned but never read)
- Commented-out code blocks (>3 lines of commented code)
- Unreachable code (after return/raise/break)

**Complexity** (HIGH or MEDIUM)
- Long functions: >50 lines (HIGH), >30 lines (MEDIUM)
- Deep nesting: >4 levels (HIGH), >3 levels (MEDIUM)
- Too many parameters: >6 (HIGH), >4 (MEDIUM)
- Complex conditionals: >3 conditions in single if/elif
- God classes: >500 lines or >20 methods

**Duplication** (MEDIUM)
- Repeated code blocks (near-identical 5+ line blocks)
- Similar functions with minor variations
- Copy-paste patterns with only variable name changes

**Naming** (LOW or MEDIUM)
- Single-letter variables outside loop iterators (LOW)
- Unclear abbreviations without context (LOW)
- Inconsistent naming conventions in same file (MEDIUM)
- Misleading names (name suggests different behavior) (MEDIUM)

**Structure** (MEDIUM)
- Large files: >500 lines
- Circular import patterns
- Mixed concerns in single module
- Missing abstractions (repeated similar operations)
</step_2>

<step_3>
**Compile findings**

Group findings by category. For each finding include:
- Severity tag: `[HIGH]`, `[MEDIUM]`, or `[LOW]`
- Location: `file:line` or `file:start-end`
- Description: What the issue is and why it matters
- Brief suggestion: How to address it

Apply severity filter if specified.
</step_3>

<step_4>
**Present results**

Output findings in this format:

```
## Refactoring Opportunities

### Dead Code (X issues)
**[HIGH]** `src/api/routes.py:45` - Unused function `old_handler()`
  → Remove or determine if this should be called somewhere

**[MEDIUM]** `src/models/user.py:8` - Unused import `Optional`
  → Remove unused import

### Complexity (X issues)
**[HIGH]** `src/services/processor.py:78-150` - Function `process_data()` is 72 lines
  → Extract helper functions for distinct operations

[... more categories ...]

---
**Summary**: X issues (Y high, Z medium, W low)
```
</step_4>

<step_5>
**Ask for action**

After presenting findings, ask:

"What would you like to do?"
1. **Fix these issues** - I'll make the changes now
2. **Create a plan file** - I'll write a .planning/refactor-PLAN.md for later
3. **Fix high-severity only** - Address critical issues now, plan the rest
4. **Done for now** - Just wanted the analysis

Wait for user response before proceeding.
</step_5>

<step_6>
**Execute chosen action**

Based on user choice:

**Fix issues**: Work through findings systematically, starting with high severity. Mark each as complete.

**Create plan file**: Write findings to `.planning/refactor-YYYY-MM-DD-PLAN.md` with checkboxes for each item.

**Fix high only**: Address high-severity items, write medium/low to plan file.

**Done**: End the skill.
</step_6>
</process>

<analysis_techniques>
**Finding dead code**:
- Use Grep to find function/class definitions
- Use Grep to search for usages
- Compare definitions vs usages

**Finding complexity**:
- Use Read to examine function length
- Count indentation levels for nesting depth
- Count parameters in function signatures

**Finding duplication**:
- Look for similar patterns across files
- Identify repeated exception handling, validation, or data transformation blocks

**Finding naming issues**:
- Scan for single-letter variables (except `i`, `j`, `k`, `x`, `y`, `n` in appropriate contexts)
- Look for inconsistent casing (mixing snake_case and camelCase)

**Finding structural issues**:
- Check file line counts
- Look for import patterns that suggest circular dependencies
- Identify modules doing too many unrelated things
</analysis_techniques>

<severity_guidelines>
<high>
Issues that significantly impact maintainability or indicate bugs:
- Dead code (confusion about what's used)
- Functions >50 lines
- Nesting >4 levels
- >6 function parameters
</high>

<medium>
Issues worth addressing but not urgent:
- Moderate complexity (30-50 line functions, 3-4 nesting levels)
- Code duplication
- Large files (>500 lines)
- Inconsistent naming
</medium>

<low>
Minor polish items:
- Single-letter variables
- Minor naming improvements
- Style consistency
</low>
</severity_guidelines>

<plan_file_template>
When creating a plan file, use this structure:

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
</plan_file_template>

<success_criteria>
Analysis is complete when:
- All files in scope have been examined
- Findings are grouped by category with severity
- User has been presented with action options
- Chosen action has been executed (fixes made OR plan file created)
</success_criteria>
