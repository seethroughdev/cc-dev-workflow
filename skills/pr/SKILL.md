---
name: pr
description: Generate or edit comprehensive PR descriptions from git changes. Use when creating pull requests, updating PR descriptions, or when asked to write a PR summary. Supports create mode (new PR) and edit mode (update existing). Optionally integrates with Linear tickets if detected in branch name.
---

# PR Description Generator

Generate comprehensive pull request descriptions from git changes.

## Modes

**Create mode** (default): Generate new PR description
```
/pr
```

**Edit mode**: Update existing PR description
```
/pr 123
/pr https://github.com/owner/repo/pull/456
```

## Workflow

### 1. Determine Mode

- If argument contains PR URL/number → **edit mode**: fetch current PR with `gh pr view`
- If no argument → **create mode**: analyze branch and changes

### 2. Gather Context

```bash
# Branch and commits
git branch --show-current
git log --oneline main..HEAD

# Changes (committed only, not uncommitted)
git diff main...HEAD
git diff --name-only main...HEAD
```

**Linear integration** (optional): If branch name contains ticket ID pattern (e.g., `maya-123`, `proj-456`):
- Extract ticket ID with regex: `([a-zA-Z]+-\d+)`
- Fetch details via Linear MCP if available
- Include ticket context in Problem/Summary sections

### 3. Generate Description

Read template from [references/template.md](references/template.md).

Fill each section:

| Section | Source |
|---------|--------|
| Summary | One-liner from commits + ticket title |
| Problem | Ticket description or inferred from changes |
| Solution | Root cause + fix approach from diff |
| Changes | Key modifications per file |
| Testing | Checklist from ticket acceptance criteria |
| Impact | Breaking changes, migrations needed |
| Review Notes | Architectural changes, risk areas |

**For edit mode**: Preserve existing good content, update only stale sections.

### 4. Review and Present

Before presenting:
- Remove redundant information between sections
- Keep language clear, direct, scannable
- No emojis, no em-dashes, avoid "enhance"
- Never mention Claude/AI in the description

Ask user to confirm before creating/updating PR.

### 5. Create or Update PR

**Create**: `gh pr create --title "..." --body "..."`
**Update**: `gh pr edit <number> --body "..."`

## Error Handling

- No git repo → inform and exit
- No Linear ticket in branch → proceed without ticket context
- Linear MCP unavailable → proceed without ticket context
