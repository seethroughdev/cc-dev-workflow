---
name: manage-linear
description: Complete Linear issue management system for creating, updating, querying, and reviewing tickets. Use when working with Linear tickets, creating feature/bug/task tickets, searching issues, updating issue properties, or creating implementation plans. Replaces Linear MCP for self-contained Linear operations.
---

<objective>
Provide comprehensive Linear issue management without requiring MCP tools in every context. Create well-formatted tickets using templates, query and filter issues, update properties, and generate implementation plans. All API calls go through secure wrapper to protect credentials.
</objective>

<quick_start>
<create_ticket>
**Create a feature ticket:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs create-issue '{
  "teamId": "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8",
  "title": "Add dark mode toggle",
  "description": "## Feature: Add dark mode toggle\n\n### User Story\nAs a user, I want to toggle dark mode so that I can reduce eye strain.\n\n### Acceptance Criteria\n- [ ] Toggle switch in settings\n- [ ] Persists across sessions",
  "projectId": "62417c2a-8fbb-4583-9867-f93828cb2ebc",
  "assigneeId": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b",
  "priority": 2
}'
```

**Query your assigned issues:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "assignee": {"id": {"eq": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"}}
}'
```

**Update issue status:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "ISSUE_ID" '{
  "stateId": "STATE_ID"
}'
```
</create_ticket>
</quick_start>

<context>
<credentials_setup>
Before using this skill, ensure Linear API credentials are configured:

1. Create credentials file: `~/.claude/credentials/linear.json`
2. Add your API key:
```json
{
  "apiKey": "lin_api_YOUR_KEY_HERE"
}
```
3. Get API key from: https://linear.app/settings/api

The secure wrapper (`~/.claude/api-wrappers/linear-api.mjs`) handles all API calls and prevents credentials from appearing in chat.
</credentials_setup>

<team_defaults>
**Default Team**: Maya (`ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8`)
**Default Project**: Landing Grid with Custom Views (`62417c2a-8fbb-4583-9867-f93828cb2ebc`)
**Default Assignee**: Adam Harris (`022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b`)

**Team Members:**
- Adam Harris: `022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b`
- Amitesh: `aaeed863-c28b-419f-be99-7b9b4a0c3919`
- Shiun: `b28908a5-73d4-48ca-a54a-252469a380a4`
- Ityam: `da1240fb-1b21-41d2-aad9-4679005b9fa8`
- Vikash: `c1b4fd1a-a192-46ab-a87e-272b01a57b2b`
- Lenore: `c10605d0-9d98-4c38-8913-7353a93cfbcd`

**Maya Team Projects:**
- Landing Grid with Custom Views: `62417c2a-8fbb-4583-9867-f93828cb2ebc` (Default)
- ACL missing records across modules: `466be8e7-72fa-40bc-8b2e-81793c8cfd7d`
- Admin Pages - GA Launch: `02a8b098-4f65-4525-9fb8-53c2b08f2e7a`
- Landing Grids in Breakthrough: `0c4e0291-1355-4dab-b5c7-4845b56e7c49`
- Inventory Spec Search: `2d32273d-cc67-43cb-8df1-9983acf81e25`
- Formula Search: `f60115ea-dfa3-4d7e-bea1-0c201d26ab84`
- Column Grouping: `5eea649c-31ef-4696-815b-8c3e90691cf3`
- Property Data Search: `fae910e2-fc17-43e8-83ea-2f6cb54917b7`
- Admin Settings - Soft Launch: `35babf52-dac8-4631-97a3-1091dfac8036`
- Angular Migration - Version 20: `f4c995f9-e91a-4aae-85cc-908eb49d1671`
- React Migration - Version 19: `99dc3c4a-f092-4165-8166-203c2ad8a961`
- Lit POC: `7ec66509-df11-42a5-9b3c-3139d2474af5`
- Albert UI: `49435cd7-48df-4070-b2c3-f543e2e2f7b9`
</team_defaults>

<writing_style>
**CRITICAL Style Rules:**
- NO emojis in ticket titles or descriptions
- NO em-dashes (—) - use regular dashes (-) or commas instead
- AVOID "enhance" - use improve, add, fix, update, implement
- Use clear, direct language without embellishment
- Keep content scannable and concise
</writing_style>
</context>

<workflow>
<operation name="create_ticket">
**Creating Linear Tickets**

1. **Determine ticket type** (feature, bug, or task)
2. **Gather information** using appropriate template
3. **Must get "Problem to solve"** - Never create tickets with only implementation details
4. **Format description** using template from `~/.claude/templates/ticket-{type}.md`
5. **Preview** complete ticket description for user approval
6. **Create** via secure API wrapper with all required fields
7. **Return** ticket URL and identifier

**Required fields for creation:**
- `teamId` (default: Maya)
- `title` (cleaned up, no emojis)
- `description` (markdown formatted from template)
- `projectId` (default: Landing Grid with Custom Views)
- `assigneeId` (default: Adam Harris)
- `priority` (0=None, 1=Urgent, 2=High, 3=Normal, 4=Low)

**Template locations:**
- Feature: `/Users/adamw/.claude/templates/ticket-feature.md`
- Bug: `/Users/adamw/.claude/templates/ticket-bug.md`
- Task: `/Users/adamw/.claude/templates/ticket-task.md`

See [references/creating-tickets.md](references/creating-tickets.md) for detailed workflow and examples.
</operation>

<operation name="query_issues">
**Querying and Searching Issues**

Use filters to find specific issues:

```bash
# My assigned issues
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "assignee": {"id": {"eq": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"}}
}'

# Issues in a specific project
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "project": {"id": {"eq": "PROJECT_ID"}}
}'

# Issues with specific status
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "state": {"name": {"eq": "In Progress"}}
}'

# Combined filters (AND logic)
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "and": [
    {"assignee": {"id": {"eq": "USER_ID"}}},
    {"state": {"type": {"eq": "started"}}}
  ]
}'
```

See [references/querying-issues.md](references/querying-issues.md) for filter reference and query patterns.
</operation>

<operation name="update_issues">
**Updating Issue Properties**

```bash
# Update status
node ~/.claude/api-wrappers/linear-api.mjs update-issue "ISSUE_ID" '{
  "stateId": "STATE_ID"
}'

# Update assignee and priority
node ~/.claude/api-wrappers/linear-api.mjs update-issue "ISSUE_ID" '{
  "assigneeId": "USER_ID",
  "priority": 2
}'

# Update description
node ~/.claude/api-wrappers/linear-api.mjs update-issue "ISSUE_ID" '{
  "description": "Updated description in markdown"
}'

# Add labels (preserves existing)
node ~/.claude/api-wrappers/linear-api.mjs update-issue "ISSUE_ID" '{
  "addedLabelIds": ["LABEL_ID_1", "LABEL_ID_2"]
}'
```

See [references/updating-issues.md](references/updating-issues.md) for complete update patterns.
</operation>

<operation name="review_ticket">
**Review Ticket and Create Implementation Plan**

1. **Extract ticket ID** from URL or use directly (e.g., MAY-123)
2. **Fetch ticket details** via `get-issue` operation
3. **Analyze codebase** for relevant areas using Task tool with codebase-analyzer
4. **Create 3-phase plan**:
   - Phase 1: Research & Understanding
   - Phase 2: Implementation Approach
   - Phase 3: Validation & Completion
5. **Ask for feedback** and offer to save to `docs/specs/`
6. **Save plan** if confirmed: `docs/specs/YYYY-MM-DD-{summary}.md`

This workflow matches the `/ticket:review` slash command pattern.

See [references/reviewing-tickets.md](references/reviewing-tickets.md) for detailed workflow.
</operation>
</workflow>

<common_patterns>
<get_reference_data>
**Get teams, projects, users, states, labels:**

```bash
# List all teams
node ~/.claude/api-wrappers/linear-api.mjs get-teams

# List projects for Maya team
node ~/.claude/api-wrappers/linear-api.mjs get-projects "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"

# List all users
node ~/.claude/api-wrappers/linear-api.mjs get-users

# List workflow states for Maya team
node ~/.claude/api-wrappers/linear-api.mjs get-workflow-states "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"

# List labels for Maya team
node ~/.claude/api-wrappers/linear-api.mjs get-labels "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"
```
</get_reference_data>

<extract_ticket_id>
**Extract ticket ID from various formats:**

```javascript
// From URL: https://linear.app/albert-invent/issue/MAY-285/remove-legacy-maya-ui
const ticketId = url.match(/issue\/([A-Z]+-\d+)/)[1]; // "MAY-285"

// From text: "See MAY-123 for details"
const ticketId = text.match(/([A-Z]+-\d+)/)[1]; // "MAY-123"

// Direct: "MAY-123"
const ticketId = input.trim(); // "MAY-123"
```
</extract_ticket_id>

<parse_api_response>
**Handle API responses:**

```javascript
const result = JSON.parse(output);

if (!result.success) {
  // Handle error
  console.error(result.error || result.errors);
  return;
}

// Access data
const issue = result.data.issueCreate.issue;
const url = issue.url;
const identifier = issue.identifier;
```
</parse_api_response>
</common_patterns>

<examples>
<example name="create_feature_ticket">
**User:** "Create a feature ticket for implementing social login"

**Process:**
1. Ask about the feature: "What social providers? What's the benefit to users?"
2. User responds: "Google and GitHub, faster onboarding without password"
3. Read template: `/Users/adamw/.claude/templates/ticket-feature.md`
4. Generate description using template structure
5. Preview: Show complete markdown description
6. User approves
7. Create via API:
```bash
node ~/.claude/api-wrappers/linear-api.mjs create-issue '{
  "teamId": "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8",
  "title": "Implement social login with Google and GitHub",
  "description": "## Feature: Implement Social Login\n\n### User Story\nAs a new user, I want to sign in with my existing Google or GitHub account so that I can access the platform without creating a new password.\n\n### Description\nEnable users to authenticate using their existing social media accounts (Google, GitHub) for faster onboarding...",
  "projectId": "62417c2a-8fbb-4583-9867-f93828cb2ebc",
  "assigneeId": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b",
  "priority": 2
}'
```
8. Return: "Created MAY-456: https://linear.app/albert-invent/issue/MAY-456"
</example>

<example name="query_my_issues">
**User:** "Show me my current issues in progress"

**Process:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "and": [
    {"assignee": {"id": {"eq": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"}}},
    {"state": {"type": {"eq": "started"}}}
  ]
}'
```

Format output as readable list with identifiers and titles.
</example>

<example name="review_ticket_and_plan">
**User:** "/ticket:review MAY-285" or "Review https://linear.app/albert-invent/issue/MAY-285"

**Process:**
1. Extract ID: "MAY-285"
2. Fetch details:
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-issue "MAY-285"
```
3. Use Task tool with codebase-analyzer for relevant code
4. Create 3-phase implementation plan
5. Ask: "Should I save this to docs/specs/?"
6. If yes, save to `docs/specs/2025-11-20-remove-legacy-maya-ui.md`
</example>
</examples>

<anti_patterns>
<what_to_avoid>
- **Don't create tickets from brainstorming** unless explicitly requested
- **Don't skip the preview step** - always show user the description first
- **Don't use MCP Linear tools** - use the secure API wrapper instead
- **Don't include emojis** in any ticket content
- **Don't use em-dashes** - use regular dashes or commas
- **Don't create tickets without problem statement** - must understand "why"
- **Don't hardcode credentials** - always use the secure wrapper
- **Don't expose API keys** in chat or tool calls
</what_to_avoid>
</anti_patterns>

<security_checklist>
- ✓ API key stored in `~/.claude/credentials/linear.json` (never in skill files)
- ✓ All API calls go through `~/.claude/api-wrappers/linear-api.mjs`
- ✓ Credentials never appear in Bash commands or chat output
- ✓ API wrapper handles authentication headers internally
- ✓ JSON responses parsed and sanitized before display
</security_checklist>

<validation>
<verify_ticket_created>
After creating a ticket:
1. Check `success: true` in API response
2. Extract `issue.identifier` (e.g., "MAY-456")
3. Extract `issue.url` for user
4. Verify all required fields populated (assignee, project, team)
5. Return formatted result with URL
</verify_ticket_created>

<verify_query_results>
After querying issues:
1. Check `success: true` in API response
2. Verify `data.issues.nodes` exists
3. Format results as readable list
4. Include pagination info if `hasNextPage: true`
</verify_query_results>
</validation>

<success_criteria>
You're successfully using this skill when:
- Tickets are created with proper templates and all required fields
- API wrapper is used for all Linear operations (no MCP tools)
- Credentials never appear in chat or command output
- Ticket descriptions follow templates and style guidelines (no emojis, no em-dashes)
- Query results are filtered correctly and formatted clearly
- Implementation plans follow 3-phase structure from ticket review workflow
- Users receive ticket URLs and identifiers after creation
</success_criteria>

<reference_guides>
For detailed information, see reference files:

- [references/creating-tickets.md](references/creating-tickets.md) - Complete ticket creation workflow with templates
- [references/querying-issues.md](references/querying-issues.md) - Filter syntax and query patterns
- [references/updating-issues.md](references/updating-issues.md) - All update operations and field reference
- [references/reviewing-tickets.md](references/reviewing-tickets.md) - Implementation plan generation workflow
- [references/api-operations.md](references/api-operations.md) - Complete API wrapper reference
</reference_guides>
