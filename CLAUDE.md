# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Claude Code plugin** (`aa`) that provides development workflow automation through slash commands. It integrates with the `beads` issue tracker and extends Claude Code with commands for code auditing, issue creation, and automated issue execution.

**Plugin ID**: `aa`
**Version**: See `.claude-plugin/plugin.json`
**Repository**: https://github.com/seethroughdev/cc-dev-workflow

## Architecture

```
cc-dev-workflow/
├── .claude-plugin/
│   ├── plugin.json       # Plugin manifest (version, hooks, notifications)
│   └── marketplace.json  # Marketplace metadata
├── commands/             # Slash commands (invoked via /command-name)
│   ├── audit.md          # /audit - 5-parallel-agent code audit
│   ├── create-beads.md   # /create-beads - Create beads issues from plan files
│   └── run-beads.md      # /run-beads - Execute beads issues with subagents
├── hooks/                # Reserved for future event hooks (currently empty)
├── skills/               # Reserved for future skill modules (currently empty)
└── statusline/           # Status bar integration (if applicable)
```

## Core Commands

### `/audit [plan-path or description]`
Comprehensive code audit using 5 parallel sub-agents:
1. **Plan Compliance** - Does code match the plan?
2. **Security** - OWASP vulnerabilities, injection risks, auth issues
3. **Code Quality** - DRY, KISS, YAGNI, naming, complexity
4. **Architecture** - Coupling, responsibilities, tech debt
5. **Completeness** - Error handling, edge cases, test coverage

Returns findings grouped by severity with actionable remediation suggestions.

### `/create-beads <plan-path>`
Convert a markdown plan file into beads issues:
- Reads `## Beads Issues` section from plan
- Creates issue hierarchy (epics, tasks)
- Sets acceptance criteria, labels, and priorities

### `/run-beads [plan-path | epic-id | --all]`
Execute ready beads issues using subagent delegation:
- Automatically claims issues (atomic operation prevents races)
- Spawns dedicated subagent per issue
- Runs sequentially by default (or parallel if dependency graph allows)
- Closes issues on successful completion
- Runs project's test suite and linting per conventions

## Beads Integration

The plugin uses `beads` (bd) CLI for issue management:
- **Minimum version**: v0.55.x (or later)
- **Key commands used**:
  - `bd ready --json` - Get issues with no blockers
  - `bd list --json` - List all issues
  - `bd show <id> --json` - Get issue details
  - `bd update <id> --claim --json` - Atomically claim issue
  - `bd close <id> --reason "..." --force --json` - Close after completion

## Development & Maintenance

### Version Management
**CRITICAL**: Bump version in **both** files together:
- `.claude-plugin/plugin.json` (main version)
- `.claude-plugin/marketplace.json` (marketplace sync)

These must stay in sync or the marketplace will have stale metadata. Always bump both on every release pushed to the repository.

### Command Format
Each command file (`commands/*.md`) requires:
```yaml
---
description: Short description of what the command does
argument-hint: [expected arguments]
allowed-tools: Tool1, Tool2, ...
context: fork
---
```

The `context: fork` means each command runs in isolation from other sessions.

### Testing Commands
Commands can be tested manually in Claude Code using `/command-name`:
1. Use a scratch project (not production code)
2. Test the command's full workflow
3. Verify output format matches expectations
4. Test with both valid and edge-case inputs

### Notification Hooks
The plugin uses `terminal-notifier` for macOS notifications on Stop and permission prompts. For non-macOS systems, remove the notification hooks from `plugin.json`.

## Recent Changes

**Version 1.5.0 (2024-02-14)**: Deprecated skills and hooks
- Removed auto-activation hooks (`skill-activator.py`, `load-skills-context.py`)
- Removed healing hook (`heal-skills-trigger.py`)
- Removed deprecated skills (heal-skills, pr, simplify-code, testing)
- Plugin now focuses on core commands: audit, create-beads, run-beads
- Simplified plugin.json for easier maintenance

**Rationale**: The hook-based skill activation added complexity without proportional benefit. Modern Claude Code provides better features through direct command invocation and team-based workflows.

## Git Workflow

This plugin is published to the Claude Code marketplace. All changes should:
1. Follow conventional commit format (feat:, fix:, chore:, etc.)
2. Bump version in both `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`
3. Push directly to main (no feature branches required)
4. Plugin users will see updates automatically on next Claude Code session
