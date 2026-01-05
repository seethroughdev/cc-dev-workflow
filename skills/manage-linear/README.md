# manage-linear Skill

Complete Linear issue management for Claude Code without MCP dependency.

## Overview

The `manage-linear` skill provides comprehensive Linear operations:
- Create tickets (feature/bug/task) with templates
- Query and filter issues
- Update issue properties
- Review tickets and generate implementation plans

All operations use a secure API wrapper that prevents credentials from appearing in chat.

## Quick Start

### 1. Setup (One-Time)

See [SETUP.md](SETUP.md) for complete setup instructions.

**Quick setup:**
```bash
# Create credentials file
mkdir -p ~/.claude/credentials
cat > ~/.claude/credentials/linear.json << 'EOF'
{
  "apiKey": "lin_api_YOUR_KEY_HERE"
}
EOF
chmod 600 ~/.claude/credentials/linear.json

# Get API key from: https://linear.app/settings/api
```

### 2. Usage

**Via slash command:**
```
/linear create a feature ticket for social login
/linear show my issues in progress
/linear move MAY-123 to done
/linear review MAY-285
```

**Direct invocation:**
```
Use the manage-linear skill to create a bug ticket for login issues
```

## Features

### Ticket Creation

Creates well-formatted tickets using templates:

- **Feature tickets** - User stories with acceptance criteria
- **Bug tickets** - Reproduction steps, environment, impact
- **Task tickets** - Problem, solution, acceptance criteria

**Workflow:**
1. Asks clarifying questions
2. Reads appropriate template
3. Generates formatted description
4. Previews for approval
5. Creates via API
6. Returns ticket URL

**Style enforcement:**
- NO emojis in titles or descriptions
- NO em-dashes (—) - uses regular dashes (-)
- AVOIDS "enhance" - uses improve, add, fix, update
- Always gets "Problem to solve" before creating

### Issue Querying

Filter and search issues using GraphQL filters:

```
Show my issues in progress
Find all high priority bugs
List issues in the Albert UI project
Show unassigned issues in Maya team
```

Supports complex filters:
- By assignee, status, priority, project, team
- By labels, dates, parent/child relationships
- Logical operators (AND, OR)

See [references/querying-issues.md](references/querying-issues.md) for complete filter reference.

### Issue Updates

Update any issue property:

```
Move MAY-123 to in progress
Assign MAY-123 to me
Set priority to urgent for MAY-123
Add bug label to MAY-123
```

Supports:
- Status/state changes
- Assignment and priority
- Labels (add, remove, replace)
- Project and team changes
- Parent/child relationships

See [references/updating-issues.md](references/updating-issues.md) for all update operations.

### Ticket Review

Generate strategic implementation plans:

```
Review MAY-285
```

**Creates 3-phase plan:**
1. **Research & Understanding** - Areas to investigate
2. **Implementation Approach** - Strategy and decisions
3. **Validation & Completion** - Testing and integration

Optionally saves to `docs/specs/YYYY-MM-DD-{title}.md`

See [references/reviewing-tickets.md](references/reviewing-tickets.md) for workflow details.

## Architecture

### Components

```
~/.claude/
├── credentials/
│   └── linear.json              # API key (secure, never exposed)
├── api-wrappers/
│   └── linear-api.mjs           # Secure GraphQL wrapper
├── skills/
│   └── manage-linear/
│       ├── SKILL.md             # Main skill logic
│       ├── README.md            # This file
│       ├── SETUP.md             # Setup instructions
│       └── references/          # Detailed documentation
│           ├── creating-tickets.md
│           ├── querying-issues.md
│           ├── updating-issues.md
│           ├── reviewing-tickets.md
│           └── api-operations.md
└── commands/
    └── linear.md                # Slash command wrapper
```

### Security Model

**Credentials never appear in:**
- Chat output
- Tool call parameters
- Error messages
- Bash command history

**How it works:**
1. API key stored in `~/.claude/credentials/linear.json`
2. All operations call the wrapper: `linear-api.mjs`
3. Wrapper loads credentials internally
4. Wrapper makes authenticated GraphQL requests
5. Only results returned to chat

### API Wrapper Operations

```bash
# Create issue
node ~/.claude/api-wrappers/linear-api.mjs create-issue '{...}'

# Update issue
node ~/.claude/api-wrappers/linear-api.mjs update-issue "ID" '{...}'

# Get issue
node ~/.claude/api-wrappers/linear-api.mjs get-issue "ID"

# Query issues
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{...}'

# Get reference data
node ~/.claude/api-wrappers/linear-api.mjs get-teams
node ~/.claude/api-wrappers/linear-api.mjs get-projects "TEAM_ID"
node ~/.claude/api-wrappers/linear-api.mjs get-users
node ~/.claude/api-wrappers/linear-api.mjs get-workflow-states "TEAM_ID"
node ~/.claude/api-wrappers/linear-api.mjs get-labels "TEAM_ID"
```

See [references/api-operations.md](references/api-operations.md) for complete API reference.

## Configuration

### Team Defaults

Pre-configured in SKILL.md for Maya team:

```
Default Team: Maya (ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8)
Default Project: Landing Grid with Custom Views
Default Assignee: Adam Harris
```

**Team members and projects** are documented in SKILL.md for quick reference.

### Templates

Ticket templates expected at:
```
~/.claude/templates/ticket-feature.md
~/.claude/templates/ticket-bug.md
~/.claude/templates/ticket-task.md
```

You can:
- Use global templates in `~/.claude/templates/`
- Reference project templates in `docs/templates/`
- Customize template locations in SKILL.md

## Usage Examples

### Example 1: Create Feature Ticket

```
User: /linear create a feature for implementing OAuth login

Skill: What OAuth providers should be supported?

User: Google and GitHub

Skill: What's the benefit to users?

User: Faster onboarding without password management

Skill: Here's the ticket description I've prepared:

---
## Feature: Implement OAuth Login

### User Story
As a new user, I want to sign in with my Google or GitHub account
so that I can access the platform without creating a password.

### Description
Enable users to authenticate using OAuth providers (Google, GitHub)
for faster onboarding and improved user experience.

### Acceptance Criteria
- [ ] User can sign in using Google account
- [ ] User can sign in using GitHub account
- [ ] New user account created on first social login
- [ ] Existing user account can link social accounts
- [ ] OAuth errors display user-friendly messages
---

Does this look good?

User: Yes, create it

Skill: Created MAY-456: https://linear.app/albert-invent/issue/MAY-456
```

### Example 2: Query Issues

```
User: /linear show my high priority issues that are in progress

Skill: [Queries with filter]:
{
  "and": [
    {"assignee": {"id": {"eq": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"}}},
    {"priority": {"eq": 2}},
    {"state": {"type": {"eq": "started"}}}
  ]
}

Found 3 issue(s):

MAY-123: Add OAuth login support
  Status: In Progress
  Assignee: Adam Harris
  Priority: High
  URL: https://linear.app/...

MAY-124: Fix mobile navigation bug
  Status: In Progress
  Assignee: Adam Harris
  Priority: High
  URL: https://linear.app/...

MAY-125: Implement dark mode toggle
  Status: In Review
  Assignee: Adam Harris
  Priority: High
  URL: https://linear.app/...
```

### Example 3: Review Ticket

```
User: /linear review MAY-285

Skill: [Fetches ticket details]
[Analyzes codebase using Task tool]

# Ticket Review: MAY-285 - Remove legacy Maya UI components

**Ticket Link:** https://linear.app/albert-invent/issue/MAY-285

**Summary:** Remove legacy Maya UI components causing maintenance
overhead and migrate to modern component library.

## Codebase Analysis

Legacy components located in:
- src/legacy/maya-ui/ - Old component library

12 files still using legacy imports...

[Full 3-phase plan]

Would you like me to:
1. Adjust any phase or add more details
2. Save this to docs/specs/
3. Dive deeper into a specific phase

User: Save it

Skill: Saved plan to docs/specs/2025-11-20-remove-legacy-maya-ui.md
```

## Replacing Linear MCP

This skill is designed to **replace** the Linear MCP tool dependency.

**Before (with MCP):**
```
Every context needs Linear MCP configured
Credentials exposed in tool calls
Must invoke MCP tools directly
Limited to MCP's available operations
```

**After (with this skill):**
```
Skill available in all contexts automatically
Credentials secured in wrapper
Natural language interface
Extended operations (templates, reviews, plans)
```

**Migration:**
1. Set up credentials (one time)
2. Use `/linear` or invoke skill directly
3. Disable Linear MCP in contexts where not needed

## Development

### Adding New Operations

To add a new operation to the API wrapper:

1. Add function to `~/.claude/api-wrappers/linear-api.mjs`
2. Add case to main() switch statement
3. Document in `references/api-operations.md`
4. Add examples to SKILL.md if needed

### Customizing Templates

To use custom ticket templates:

1. Create/modify templates in `~/.claude/templates/`
2. Or update SKILL.md to reference your project templates
3. Follow existing template structure
4. Ensure templates use markdown format

### Extending the Skill

The skill uses progressive disclosure:
- Core workflow in SKILL.md (under 500 lines)
- Detailed docs in references/ files
- Can add new reference files as needed

## Troubleshooting

### Common Issues

**Credentials not found:**
- Check `~/.claude/credentials/linear.json` exists
- Verify JSON is valid
- Ensure file permissions: `chmod 600`

**API errors:**
- Verify API key is correct
- Check Linear API status: https://status.linear.app/
- Ensure you haven't hit rate limits (1,500/hour)

**Ticket creation fails:**
- Verify team ID is correct
- Check project ID exists for team
- Ensure assignee ID is valid user

See [SETUP.md](SETUP.md) for detailed troubleshooting.

## Reference Documentation

- [SETUP.md](SETUP.md) - Complete setup instructions
- [references/creating-tickets.md](references/creating-tickets.md) - Ticket creation workflow
- [references/querying-issues.md](references/querying-issues.md) - Query filters and patterns
- [references/updating-issues.md](references/updating-issues.md) - Update operations
- [references/reviewing-tickets.md](references/reviewing-tickets.md) - Ticket review workflow
- [references/api-operations.md](references/api-operations.md) - Complete API reference

## License

This skill is part of your personal Claude Code configuration.
