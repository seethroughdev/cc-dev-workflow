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

2. **Extract epic from plan file:**

   Parse the plan to identify the epic:
   - **Title**: Use the H1 heading (`# ...`) or the first H2 if no H1 exists
   - **Description**: Use any intro paragraph or objectives section
   - **Priority**: Default to P2 unless plan indicates urgency

   Example plan structures to handle:
   ```markdown
   # Implement Search Feature        ← Epic title

   ## Objective                      ← Epic description
   Add semantic search capability...

   ## Tasks                          ← Individual tasks
   1. Add search endpoint
   2. Create search UI
   ```

3. **Extract structured fields per task:**

   For each task, parse the plan for these distinct sections:
   - **Title**: The task heading or numbered item
   - **Description**: Main body/context for the task
   - **Acceptance criteria**: Extract from "acceptance criteria", "done when", "requirements", or checklist items
   - **Design/implementation notes**: Extract from "design", "implementation", "approach", or "technical notes" sections
   - **Notes**: Any additional context that doesn't fit above
   - **Labels**: Infer from task context (e.g., `frontend`, `backend`, `api`, `database`, `testing`, `docs`)

4. **Create beads issues from plan:**

   For descriptions and design notes, use `--body-file` to avoid shell escaping issues:

   ```
   - Create epic for the overall plan:
     # Write description to temp file to avoid shell escaping issues
     echo "<description>" > /tmp/bd-desc-epic.md
     bd create "<extracted-epic-title>" -t epic -p <priority> --body-file=/tmp/bd-desc-epic.md --json

   - Create task issues for each plan step/task:
     # Write structured content to temp files
     echo "<description>" > /tmp/bd-desc-<n>.md
     bd create "<task-title>" -t task -p <priority> --parent <epic-id> \
       --body-file=/tmp/bd-desc-<n>.md \
       --acceptance "<acceptance criteria>" \
       --design "<design/implementation notes>" \
       --notes "<additional notes>" \
       --labels "<label1>,<label2>" \
       --json

   - Add dependencies between tasks if specified in plan:
     bd dep add <issue-id> --blocks <dependent-id>

   - For tasks discovered during planning (e.g., prerequisite work identified):
     bd dep add <issue-id> --deps discovered-from:<parent-id>
   ```

   Clean up temp files after creation:
   ```bash
   rm -f /tmp/bd-desc-*.md
   ```

   > **Alternative**: If the plan follows a beads-compatible markdown format, `bd create -f plan.md --json` can create multiple issues at once. Use our custom parsing for arbitrary plan formats.

5. **Sync beads state:**
   ```bash
   bd sync
   ```

6. **Add beads reference to plan file:**

   Append a reference section to $ARGUMENTS:
   ```markdown

   ## Beads Issues

   Epic: `<epic-id>`

   | Issue | Task | Labels |
   |-------|------|--------|
   | `proj-abc` | Task 1 title | frontend |
   | `proj-def` | Task 2 title | backend, api |
   ```

7. **Report:**
   - List created epic and task IDs
   - Suggest: "Run `/run-beads` to execute these issues"

</process>

<success_criteria>
- Beads issues created for all plan tasks
- Plan file has `## Beads Issues` section with issue IDs
- Epic and tasks properly linked with parent-child relationships
- Structured fields (acceptance, design, notes) populated where available
- Labels applied for categorization
- Beads state synced after creation
</success_criteria>
