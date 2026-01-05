---
description: Format, lint, and create logical commits from staged files
argument-hint: [optional: push, rebase, merge, or other git operations]
allowed-tools: Bash(git:*), Bash(npm:*), Bash(npx:*), Bash(make:*), Bash(ruff:*), Bash(uv:*), Read, Glob, AskUserQuestion, Task, Skill
---

<objective>
Create well-structured git commits from staged files by running format/lint tools, grouping related changes into logical commits, and writing clear commit messages.

Never reference Claude, AI, or any co-author attribution. No emojis. Never use the word "enhance". Keep messages concise, present tense, and specific to the actual changes.
</objective>

<context>
Staged files: !`git diff --cached --name-only`
Unstaged changes: !`git diff --name-only`
Current branch: !`git branch --show-current`
Recent commits for style reference: !`git log --oneline -10`
</context>

<conflict_detection>
CRITICAL: Before running any format/lint commands, check for files that appear in BOTH staged and unstaged lists above.

If any file has both staged AND unstaged changes:
1. STOP immediately
2. Use AskUserQuestion to ask the user:
   - "File X has both staged and unstaged changes. Running format/lint may cause conflicts."
   - Options: "Stash unstaged changes first", "Stage all changes for this file", "Skip formatting this file", "Abort and let me handle it"
3. Only proceed after user confirms approach for each conflicting file
</conflict_detection>

<process>
1. **Detect conflicts**: Compare staged vs unstaged file lists. If overlap exists, ask user before proceeding (see conflict_detection above).

2. **Identify project tools**: Check for Makefile, package.json, pyproject.toml, or similar to find format/lint commands:
   - Python: `make format`, `ruff format`, `ruff check --fix`
   - JavaScript/TypeScript: `npm run format`, `npm run lint:fix`
   - Use whatever the project has configured

3. **Run format and lint on staged files only**:
   - For each staged file, run appropriate format/lint tools
   - Re-stage any files modified by formatting: `git add <file>`

4. **Analyze changes for logical grouping**:
   - Review the staged diff content
   - Group files by logical unit of work (feature, bugfix, refactor, config change, etc.)
   - Each group becomes one commit

5. **Create commits for each group**:
   - Unstage files not in current group: `git restore --staged <files>`
   - Write commit message following conventions:
     - Format: `type(scope): description`
     - Types: feat, fix, refactor, test, docs, chore, style, perf
     - Present tense, lowercase, no period
     - Be specific to what actually changed, not generic
   - Commit the group
   - Repeat for remaining groups

6. **Pre-push skill healing** (only if $ARGUMENTS contains "push"):
   Before pushing, analyze if any skills could benefit from learnings in this session:

   a. **Scan available skills**: Check these locations for SKILL.md files:
      - `~/.claude/skills/*/SKILL.md` (global)
      - `.claude/skills/*/SKILL.md` (project)
      - Plugin skills directories

   b. **Match skills to changes**: Review the committed changes and session context. Identify skills that:
      - Were activated during this session
      - Relate to the type of work done (testing, refactoring, commits, etc.)
      - Could benefit from learnings based on any corrections, retries, or insights

   c. **Ask user**: If relevant skills are found, use AskUserQuestion:
      - "Would you like to run heal-skills before pushing?"
      - Show which skills were detected as relevant
      - Options: "Yes, heal all relevant skills", "Yes, let me choose which", "No, just push"

   d. **Execute healing**: If user approves:
      - For a single skill: invoke `/heal-skills --skill <skill-name>`
      - For multiple skills: spawn parallel Task subagents, one per skill:
        ```
        Task(subagent_type="general-purpose", prompt="Run /heal-skills --skill <skill-name>")
        ```
      - Wait for all healing tasks to complete before pushing

7. **Handle additional operations**: If $ARGUMENTS provided (push, rebase, merge, etc.), execute after all commits complete and any skill healing is done.
</process>

<commit_message_rules>
- Format: `type(scope): specific description`
- Present tense: "add", "fix", "remove", "update", "refactor"
- No period at end
- Under 72 characters
- Be specific: "fix null check in user validation" not "fix bug"
- NO emojis
- NO "enhance" - use "improve", "optimize", "extend", "refine" instead
- NO AI/Claude attribution or Co-Authored-By lines
- NO generic messages like "update files" or "make changes"
</commit_message_rules>

<success_criteria>
- All staged files formatted and linted
- Changes grouped into logical, atomic commits
- Each commit message is specific, present tense, follows type(scope): format
- No conflicts created between staged/unstaged changes
- Pre-push skill healing offered if pushing (user can decline)
- Additional git operations ($ARGUMENTS) completed if specified
- Zero AI attribution in any commit
</success_criteria>
