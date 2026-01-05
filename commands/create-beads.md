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

3. **Create beads issues from plan:**

   ```
   - Create epic for the overall plan:
     bd create "<extracted-epic-title>" -t epic -p <priority> -d "<description>" --json

   - Create task issues for each plan step/task:
     bd create "<task-title>" -t task -p <priority> --parent <epic-id> --json

   - Add dependencies between tasks if specified in plan:
     bd dep add <issue-id> --blocks <dependent-id>
   ```

4. **Add beads reference to plan file:**

   Append a reference section to $ARGUMENTS:
   ```markdown

   ## Beads Issues

   Epic: `<epic-id>`

   | Issue | Task |
   |-------|------|
   | `proj-abc` | Task 1 title |
   | `proj-def` | Task 2 title |
   ```

5. **Report:**
   - List created epic and task IDs
   - Suggest: "Run `/run-beads` to execute these issues"

</process>

<success_criteria>
- Beads issues created for all plan tasks
- Plan file has `## Beads Issues` section with issue IDs
- Epic and tasks properly linked with parent-child relationships
</success_criteria>
