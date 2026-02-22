---
description: Execute ready beads issues with subagents
argument-hint: [plan-path | epic-id | --all]
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, Task, AgentOutputTool, AskUserQuestion, Skill
context: fork
---

Execute beads issues using subagent delegation.

<objective>
Find ready issues (no blockers) and execute them using dedicated subagents. Execute sequentially by default, or in parallel when explicitly told the dependency graph allows concurrent execution.

- If a plan file path is provided: extract epic ID from the `## Beads Issues` section
- If an epic ID is provided: execute only tasks under that epic
- If `--all` is provided: execute all ready issues
- If no argument: show ready issues and ask which to execute
</objective>

<context>
Ready issues: !`bd ready --json`
Blocked issues: !`bd blocked --json`
All open issues: !`bd list --status open --json`
</context>

<process>

1. **Determine scope:**

   - If `$ARGUMENTS` is a file path (contains `/` or ends in `.md`):
     1. Read the plan file
     2. Find the `## Beads Issues` section
     3. Extract the epic ID from `Epic: \`<epic-id>\``
     4. Use that epic ID to scope execution
   - If `$ARGUMENTS` is an epic ID: get child tasks of that epic
   - If `$ARGUMENTS` is `--all`: get all ready issues
   - If no argument: list ready issues and ask user which to run

2. **Validate issues are ready:**
   - Use `bd ready --json` to get issues with no open blockers
   - Use `bd blocked --json` to identify and report blocked issues
   - Skip issues with `deferred` status or children of deferred parents
   - If no ready issues: report and exit

3. **Optionally preview dependency graph:**
   ```bash
   bd graph <epic-id>
   ```

4. **Execute issues:**

   **Default behavior (sequential):** Process ready issues one at a time.

   **Parallel execution (when explicitly allowed):** If the dependency graph analysis indicates specific issues can be run concurrently, you MAY launch multiple subagents in parallel by including multiple Task tool calls in a single message. Only do this when:
   - You are explicitly told the issues can run in parallel
   - The dependency graph confirms no blocking relationships between them
   - The issues don't modify the same files

   For each ready issue:

   ```
   1. Claim the issue atomically:
      bd update <issue-id> --claim --json
      # --claim sets assignee + status in one step, preventing race conditions

   2. Get full issue context:
      bd show <issue-id> --json
      # Returns: title, description, design, acceptance, notes, labels, priority, parent

   3. Check if in a worktree: `[ -f .git ]`

   4. Spawn a subagent (Task tool, subagent_type="general-purpose"):

      "Execute beads issue <issue-id>: <issue-title>

      Description: <description from bd show>
      Acceptance criteria: <acceptance from bd show>
      Design notes: <design from bd show>
      Additional notes: <notes from bd show>
      Labels: <labels from bd show>
      Priority: <priority> (P0=critical, P1=high, P2=medium, P3=low, P4=backlog)
      Parent epic: <parent title if applicable>

      [If in worktree, add:]
      Git context: You are in a git worktree. Beads state is shared across
      worktrees via Dolt. Do not switch branches or modify other worktrees.

      Instructions:
      1. Read CLAUDE.md for project conventions (test commands, lint commands, etc.)
      2. Implement the fix/feature as described
      3. Run relevant tests per project conventions
      4. Ensure code passes linting per project conventions

      DO NOT close the issue or create commits.

      Report: files modified, test results, any blockers"

   5. For sequential: Wait for subagent (TaskOutput), then proceed to next
      For parallel: Launch all eligible subagents together, then collect results

   6. On success:
      bd close <issue-id> --reason "<summary>" --force --json
      # --force bypasses gate checks (gh:pr, gh:run, timer, bead)
      # Gates are for human workflows; subagent execution closes directly

   7. On failure: leave as in_progress, record error

   8. Re-check ready issues: `bd ready --json`
      # Closing an issue may unblock dependent tasks
   9. Update remaining work list with newly unblocked issues
   10. Proceed to next ready issue (or next batch if parallel)
   ```

   **Execution mode rules:**
   - **Sequential (default):** Only ONE subagent running at a time. Wait for completion before starting next.
   - **Parallel (when told):** Launch multiple Task tool calls in a SINGLE message when explicitly informed by dependency analysis that issues are independent.

5. **Finalize:**
   - Run full test suite per project conventions
   - Run linting per project conventions
   - Report summary: succeeded, failed, still blocked

6. **Offer next steps:**
   - If all succeeded: "Ready to commit? Run `/commit`"
   - If failures: show failed issues, ask to retry or skip

</process>

<success_criteria>
- All targeted issues executed and closed
- Code tested and linted
- Clear report of outcomes
</success_criteria>

<error_handling>
If a subagent fails:
1. Leave issue as in_progress
2. Report which issues succeeded vs failed
3. Ask user: retry, skip, or abort remaining

If unexpected errors occur:
- Run `bd doctor` to check for database issues
- Use `bd stale --days 1` to find abandoned in_progress issues
- Use `bd reopen <id> --reason "Retrying"` for failed-then-fixed scenarios
</error_handling>

<worktree_handling>
When working in a git worktree (detected by `.git` being a file, not a directory):

1. **Beads storage is shared**: The `.beads/` directory lives in the main worktree. All worktrees share the same Dolt database. This is intentional.

2. **Use `--claim` to prevent double-claiming**: The atomic claim prevents race conditions when multiple worktrees work concurrently.

3. **Subagent instructions for worktrees:**
   When spawning subagents in a worktree context, include:
   - "You are in a git worktree, not the main repo"
   - "Beads state is shared via Dolt — do not switch branches or modify other worktrees"
</worktree_handling>
