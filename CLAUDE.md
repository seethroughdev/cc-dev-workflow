# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code plugin** (`aa` - alias for this workflow plugin) that provides development workflow automation tools. It extends Claude Code with slash commands, skills, and hooks for code quality tasks like auditing, refactoring analysis, smart commits, and beads issue tracking integration.

**Plugin ID**: `aa`
**Version**: See `.claude-plugin/plugin.json`

## Architecture

```
cc-dev-workflow/
├── .claude-plugin/
│   ├── plugin.json       # Plugin manifest (name, version, hooks, LSP servers)
│   └── marketplace.json  # Marketplace metadata
├── commands/             # Slash commands (invoked via /command-name)
│   ├── audit.md          # 5-parallel-agent code audit
│   ├── commit.md         # Smart commit with format/lint
│   ├── create-beads.md   # Create beads issues from plan files
│   ├── loop.md           # Iterative dev loop (wraps ralph-wiggum)
│   └── run-beads.md      # Execute beads issues with subagents
├── skills/               # Skills (auto-activated or manually invoked)
│   ├── heal-skills/      # Session transcript analysis for improvements
│   ├── pr/               # PR description generator from git changes
│   ├── simplify-code/    # Code cleanup, simplification, and refactoring analysis
│   └── testing/          # Minimal regression-focused testing philosophy
└── hooks/                # Event hooks (Python scripts)
    ├── heal-skills-trigger.py  # Stop: suggest /heal-skills if learnings detected
    ├── load-skills-context.py  # SessionStart: inject available skills manifest
    └── skill-activator.py      # UserPromptSubmit: match skills to user prompts
```

## Key Concepts

### Commands vs Skills
- **Commands** (`commands/*.md`): User-invoked via `/command-name`. Have YAML frontmatter with `description`, `argument-hint`, and optional `allowed-tools`.
- **Skills** (`skills/*/SKILL.md`): Domain knowledge that can be auto-activated by hooks or manually invoked. Have YAML frontmatter (`name`, `description`) and markdown body with workflow instructions.

### Hook System
Three Python hooks handle skill discovery, activation, and learning:
1. **SessionStart** (`load-skills-context.py`): Scans all skill directories and injects a manifest into context
2. **UserPromptSubmit** (`skill-activator.py`): Keyword-matches user prompts to suggest relevant skills
3. **Stop** (`heal-skills-trigger.py`): Detects if skills were used + errors/corrections occurred, suggests `/heal-skills`

Additional hooks for notifications (macOS only via `terminal-notifier`) on Stop and permission prompts.

### Skill Locations (priority order)
1. Global: `~/.claude/skills/`
2. Project: `${PROJECT}/.claude/skills/`
3. Plugin: `./skills/`

### Beads Integration
The plugin integrates with `beads` (bd) for issue tracking:
- `/create-beads <plan-path>`: Creates beads issues from a plan markdown file
- `/run-beads [plan-path | epic-id | --all]`: Executes ready issues via subagents

## Development Notes

### Version Bumping
Bump the version in `.claude-plugin/plugin.json` with every change pushed to the repository.

### Hook Paths
Always use `${CLAUDE_PLUGIN_ROOT}` for hook script paths in `plugin.json`. Relative paths resolve against the user's project directory, not the plugin directory.

```json
// WRONG - breaks when used from other projects
"command": "python3 hooks/skill-activator.py"

// CORRECT - resolves to plugin directory
"command": "python3 \"${CLAUDE_PLUGIN_ROOT}/hooks/skill-activator.py\""
```

### Testing Hooks
Hooks read JSON from stdin and output JSON to stdout. Test with:
```bash
echo '{"prompt": "refactor this code"}' | python hooks/skill-activator.py
```

### Plugin Configuration
The plugin provides LSP servers for Python (pyright) and TypeScript - these are configured in `.claude-plugin/plugin.json`.

### Notification Hooks
The plugin uses `terminal-notifier` for macOS notifications on Stop and permission prompts. Remove these from `plugin.json` if not on macOS.
