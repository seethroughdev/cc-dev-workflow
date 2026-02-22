---
description: Create beads issues from a plan file (does not execute)
argument-hint: <plan-path>
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, AskUserQuestion, Task, Skill
---

Create beads issues from the plan at $ARGUMENTS.

<objective>
Read the plan file, extract an epic and tasks, create beads issues, and add a reference section to the plan for correlation.

This command only creates issues - use `/run-beads` to execute them.
</objective>

<context>
Plan file: @$ARGUMENTS
Existing issues: !`bd list --status open --json`
</context>

<process>

1. **Verify plan exists:**
   - Read $ARGUMENTS
   - If plan doesn't exist: error and exit
   - Check if plan already has a `## Beads Issues` section (skip creation if so)

2. **Try built-in markdown import first:**

   If the plan follows a beads-compatible markdown format (H1 as epic, H2s as tasks, optional YAML frontmatter), use the built-in parser:

   ```bash
   bd create -f "$ARGUMENTS" --json
   ```

   **Compatible format example:**
   ```markdown
   ---
   priority: 1
   type: feature
   ---

   # Epic Title

   Epic description...

   **Dependencies:**
   - blocks: bd-xyz

   ## Task 1 Title

   Task 1 description...

   ## Task 2 Title

   - [ ] Subtask A
   - [x] Subtask B (already done)
   ```

   The built-in parser handles:
   - YAML frontmatter (priority, type, assignee)
   - H1 → epic, H2 → child tasks
   - Checklist items (`- [ ]`) → sub-issues
   - Dependency references (`blocks: bd-xyz`)

   If `bd create -f` succeeds, skip to step 5 (add reference section).

3. **Fall back to manual parsing for non-standard plans:**

   If the plan doesn't fit the standard format (numbered lists, custom sections, etc.), parse manually.

   **Extract epic:**
   - **Title**: Use the H1 heading or first H2 if no H1
   - **Description**: Intro paragraph or objectives section
   - **Priority**: P0 (critical) through P4 (backlog). Default P2 unless plan indicates urgency.

   **Extract tasks with structured fields:**
   - **Title**: Task heading or numbered item
   - **Description**: Main body/context
   - **Type**: `task` (default), `chore` (maintenance), `decision` (architectural choices), `bug` (fixes)
   - **Acceptance criteria**: From "acceptance criteria", "done when", "requirements", or checklist items
   - **Design/implementation notes**: From "design", "implementation", "approach", or "technical notes" sections
   - **Notes**: Additional context
   - **Labels**: Infer from context (e.g., `frontend`, `backend`, `api`, `database`, `testing`, `docs`)

4. **Create beads issues:**

   Use `--body-file` for descriptions to avoid shell escaping issues:

   ```bash
   # Create epic
   echo "<description>" > /tmp/bd-desc-epic.md
   bd create "<epic-title>" -t epic -p <priority> --body-file=/tmp/bd-desc-epic.md --json

   # Create child tasks
   echo "<description>" > /tmp/bd-desc-<n>.md
   bd create "<task-title>" -t <type> -p <priority> --parent <epic-id> \
     --body-file=/tmp/bd-desc-<n>.md \
     --acceptance "<acceptance criteria>" \
     --design "<design/implementation notes>" \
     --notes "<additional notes>" \
     --labels "<label1>,<label2>" \
     --json

   # Add dependencies (child depends on parent):
   #   bd dep add <child-id> <parent-id>
   # means "child depends on parent" (child cannot start until parent is done)
   bd dep add <dependent-task-id> <prerequisite-task-id>

   # For discovered work:
   bd dep add <new-id> <source-id> --type discovered-from

   # Link to external trackers if referenced in plan:
   bd update <id> --external-ref "gh-123"
   ```

   Parse the `--json` output from each `bd create` to extract the created issue ID reliably.

   Clean up temp files after creation:
   ```bash
   rm -f /tmp/bd-desc-*.md
   ```

5. **Add beads reference to plan file:**

   Append a reference section to $ARGUMENTS:
   ```markdown

   ## Beads Issues

   Epic: `<epic-id>`

   | Issue | Task | Type | Labels |
   |-------|------|------|--------|
   | `proj-abc` | Task 1 title | task | frontend |
   | `proj-def` | Task 2 title | chore | backend, api |
   ```

6. **Report:**
   - List created epic and task IDs
   - Show dependency graph: `bd graph <epic-id>`
   - Suggest: "Run `/run-beads` to execute these issues"

</process>

<success_criteria>
- Beads issues created for all plan tasks
- Plan file has `## Beads Issues` section with issue IDs
- Epic and tasks properly linked with parent-child relationships
- Dependencies correctly oriented (child depends on parent)
- Structured fields (acceptance, design, notes) populated where available
- Labels applied for categorization
- JSON output parsed for reliable issue ID extraction
</success_criteria>
