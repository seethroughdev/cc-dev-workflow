---
allowed-tools: Read, Glob, AskUserQuestion, Task, Skill
description: Start an iterative development loop with auto-populated prompt (wraps ralph-wiggum)
argument-hint: <task-description> [--max N]
---

# Iterative Development Loop

You MUST invoke the `ralph-wiggum:ralph-loop` skill with the following configuration.

## User's Task

$ARGUMENTS

## Action Required

**Immediately** use the Skill tool with:
- `skill`: `ralph-wiggum:ralph-loop`
- `args`: The formatted prompt below with options

## Formatted Prompt

Construct the ralph-loop invocation with this prompt (replace `{{TASK}}` with the user's task from above):

```
"You are in an iterative development loop.

## Your Task
{{TASK}}

## Each Iteration
1. Check git status and existing files for previous work
2. Identify what's incomplete vs requirements
3. Make ONE focused improvement
4. Verify with tests/lint/build as appropriate
5. Assess: Are ALL requirements fully met?

## Completion
When EVERYTHING is done and verified:
<promise>LOOP_COMPLETE</promise>

## If Stuck (after 3+ attempts on same issue)
Document the blocker, list what you tried, then:
<promise>LOOP_COMPLETE</promise>" --completion-promise "LOOP_COMPLETE" --max-iterations {{MAX}}
```

## Defaults

- **max-iterations**: 5 (override with `--max N` in user arguments)

## Argument Parsing

1. Extract the task description (everything except flags)
2. If `--max N` appears, use N for max-iterations; otherwise use 5
3. Pass everything to ralph-wiggum:ralph-loop

## Examples

| User runs | max-iterations |
|-----------|----------------|
| `/loop Fix the login bug` | 5 |
| `/loop Add tests --max 10` | 10 |
| `/loop Refactor auth module --max 3` | 3 |
