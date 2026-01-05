# Linear API Operations Reference

Complete reference for all operations supported by the Linear API wrapper.

## API Wrapper Location

```
~/.claude/api-wrappers/linear-api.mjs
```

## Available Operations

### create-issue

Create a new Linear issue.

**Usage:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs create-issue '<IssueCreateInput-json>'
```

**Required Fields:**
- `teamId` (String) - Team ID

**Optional Fields:**
- `id` (String) - Custom UUID (auto-generated if not provided)
- `title` (String) - Issue title
- `description` (String) - Markdown description
- `assigneeId` (String) - User ID to assign
- `delegateId` (String) - Agent user ID to delegate
- `parentId` (String) - Parent issue ID (for sub-issues)
- `priority` (Int) - 0=None, 1=Urgent, 2=High, 3=Normal, 4=Low
- `estimate` (Int) - Complexity estimate
- `subscriberIds` (Array[String]) - User IDs to subscribe
- `labelIds` (Array[String]) - Label IDs to apply
- `stateId` (String) - Workflow state ID
- `projectId` (String) - Project ID
- `cycleId` (String) - Cycle ID
- `projectMilestoneId` (String) - Project milestone ID
- `sortOrder` (Float) - Custom sort order

**Example:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs create-issue '{
  "teamId": "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8",
  "title": "Add dark mode toggle",
  "description": "## Feature: Add dark mode toggle\n\nImplement dark mode...",
  "assigneeId": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b",
  "priority": 2,
  "projectId": "62417c2a-8fbb-4583-9867-f93828cb2ebc"
}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "issueCreate": {
      "success": true,
      "issue": {
        "id": "uuid",
        "identifier": "MAY-123",
        "title": "Add dark mode toggle",
        "url": "https://linear.app/albert-invent/issue/MAY-123",
        "state": {"name": "Triage"},
        "assignee": {"name": "Adam Harris", "email": "adam@example.com"},
        "team": {"name": "Maya", "key": "MAY"},
        "project": {"name": "Landing Grid with Custom Views"},
        "labels": {"nodes": []}
      }
    }
  }
}
```

### update-issue

Update an existing Linear issue.

**Usage:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "<issue-id>" '<IssueUpdateInput-json>'
```

**Issue ID:** UUID or identifier (e.g., "MAY-123")

**Available Fields:**
- `title` (String) - Issue title
- `description` (String) - Markdown description
- `assigneeId` (String) - User ID (null to unassign)
- `delegateId` (String) - Agent user ID
- `parentId` (String) - Parent issue ID (null to remove)
- `priority` (Int) - 0-4
- `estimate` (Int) - Complexity estimate
- `subscriberIds` (Array[String]) - Replaces all subscribers
- `labelIds` (Array[String]) - Replaces all labels
- `addedLabelIds` (Array[String]) - Adds labels (preserves existing)
- `removedLabelIds` (Array[String]) - Removes specific labels
- `teamId` (String) - Move to different team
- `cycleId` (String) - Cycle ID (null to remove)
- `projectId` (String) - Project ID (null to remove)
- `stateId` (String) - Workflow state ID

**Example:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "stateId": "state-uuid",
  "priority": 1,
  "addedLabelIds": ["label-uuid"]
}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "issueUpdate": {
      "success": true,
      "issue": {
        "id": "uuid",
        "identifier": "MAY-123",
        "title": "Add dark mode toggle",
        "url": "https://linear.app/...",
        "state": {"name": "In Progress"},
        "assignee": {"name": "Adam Harris", "email": "adam@example.com"}
      }
    }
  }
}
```

### get-issue

Get detailed information about a specific issue.

**Usage:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-issue "<issue-id>"
```

**Issue ID:** UUID or identifier (e.g., "MAY-123")

**Example:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-issue "MAY-123"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "issue": {
      "id": "uuid",
      "identifier": "MAY-123",
      "title": "Add dark mode toggle",
      "description": "## Feature...",
      "url": "https://linear.app/...",
      "priority": 2,
      "estimate": null,
      "createdAt": "2025-11-20T12:00:00.000Z",
      "updatedAt": "2025-11-20T14:00:00.000Z",
      "state": {
        "id": "state-uuid",
        "name": "In Progress",
        "type": "started"
      },
      "assignee": {
        "id": "user-uuid",
        "name": "Adam Harris",
        "email": "adam@example.com"
      },
      "team": {
        "id": "team-uuid",
        "name": "Maya",
        "key": "MAY"
      },
      "project": {
        "id": "project-uuid",
        "name": "Landing Grid with Custom Views"
      },
      "labels": {
        "nodes": [
          {"id": "label-uuid", "name": "feature"}
        ]
      },
      "parent": null,
      "children": {
        "nodes": []
      }
    }
  }
}
```

### query-issues

Query and filter issues.

**Usage:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '<IssueFilter-json>' [limit]
```

**Default limit:** 50

**Filter Examples:**

By assignee:
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "assignee": {"id": {"eq": "user-uuid"}}
}'
```

By state type:
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "state": {"type": {"eq": "started"}}
}'
```

Combined filters:
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "and": [
    {"assignee": {"id": {"eq": "user-uuid"}}},
    {"priority": {"in": [1, 2]}}
  ]
}'
```

**Response:**
```json
{
  "success": true,
  "data": {
    "issues": {
      "nodes": [
        {
          "id": "uuid",
          "identifier": "MAY-123",
          "title": "Issue title",
          "url": "https://linear.app/...",
          "priority": 2,
          "createdAt": "2025-11-20T12:00:00.000Z",
          "updatedAt": "2025-11-20T14:00:00.000Z",
          "state": {"name": "In Progress", "type": "started"},
          "assignee": {"name": "Adam Harris"},
          "team": {"name": "Maya", "key": "MAY"},
          "project": {"name": "Landing Grid with Custom Views"},
          "labels": {"nodes": [{"name": "feature"}]}
        }
      ],
      "pageInfo": {
        "hasNextPage": false,
        "endCursor": "cursor-string"
      }
    }
  }
}
```

### get-teams

List all teams in the workspace.

**Usage:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-teams
```

**Response:**
```json
{
  "success": true,
  "data": {
    "teams": {
      "nodes": [
        {
          "id": "team-uuid",
          "name": "Maya",
          "key": "MAY"
        }
      ]
    }
  }
}
```

### get-projects

List projects, optionally filtered by team.

**Usage:**
```bash
# All projects
node ~/.claude/api-wrappers/linear-api.mjs get-projects

# Projects for specific team
node ~/.claude/api-wrappers/linear-api.mjs get-projects "<team-id>"
```

**Example:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-projects "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "projects": {
      "nodes": [
        {
          "id": "project-uuid",
          "name": "Landing Grid with Custom Views",
          "state": "started",
          "team": {"name": "Maya"}
        }
      ]
    }
  }
}
```

### get-users

List all users in the workspace.

**Usage:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-users
```

**Response:**
```json
{
  "success": true,
  "data": {
    "users": {
      "nodes": [
        {
          "id": "user-uuid",
          "name": "Adam Harris",
          "email": "adam@example.com",
          "active": true
        }
      ]
    }
  }
}
```

### get-workflow-states

List workflow states for a team.

**Usage:**
```bash
# All workflow states
node ~/.claude/api-wrappers/linear-api.mjs get-workflow-states

# States for specific team
node ~/.claude/api-wrappers/linear-api.mjs get-workflow-states "<team-id>"
```

**Example:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-workflow-states "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "workflowStates": {
      "nodes": [
        {
          "id": "state-uuid",
          "name": "Triage",
          "type": "triage",
          "team": {"name": "Maya"}
        },
        {
          "id": "state-uuid-2",
          "name": "In Progress",
          "type": "started",
          "team": {"name": "Maya"}
        }
      ]
    }
  }
}
```

**State Types:**
- `triage` - Needs triage
- `backlog` - Backlog
- `unstarted` - To do
- `started` - In progress
- `completed` - Done
- `canceled` - Canceled

### get-labels

List issue labels, optionally filtered by team.

**Usage:**
```bash
# All labels
node ~/.claude/api-wrappers/linear-api.mjs get-labels

# Labels for specific team
node ~/.claude/api-wrappers/linear-api.mjs get-labels "<team-id>"
```

**Example:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-labels "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "issueLabels": {
      "nodes": [
        {
          "id": "label-uuid",
          "name": "feature",
          "color": "#4ea7fc",
          "team": {"name": "Maya"}
        },
        {
          "id": "label-uuid-2",
          "name": "bug",
          "color": "#eb5757",
          "team": {"name": "Maya"}
        }
      ]
    }
  }
}
```

## Error Handling

All operations return a consistent format:

**Success:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "error": "Error message"
}
```

**GraphQL Errors:**
```json
{
  "success": false,
  "errors": [
    {"message": "GraphQL error message"}
  ]
}
```

## Credentials

API wrapper expects credentials at:
```
~/.claude/credentials/linear.json
```

Format:
```json
{
  "apiKey": "lin_api_YOUR_KEY_HERE"
}
```

Get API key from: https://linear.app/settings/api

## Rate Limits

- API key authentication: 1,500 requests/hour per user
- Wrapper includes no rate limiting - be mindful of usage

## Response Parsing

Parse JSON responses:

```javascript
const result = JSON.parse(output);

if (!result.success) {
  console.error('Error:', result.error || result.errors);
  return;
}

// Access data
const data = result.data;
```

## Common Workflows

**Create ticket workflow:**
1. `get-teams` - Get team ID
2. `get-projects` - Get project ID (optional)
3. `get-users` - Get assignee ID (optional)
4. `get-workflow-states` - Get state ID (optional)
5. `create-issue` - Create with all IDs

**Update ticket workflow:**
1. `get-issue` - Verify current state
2. `get-workflow-states` - Get new state ID
3. `update-issue` - Update with new state

**Query and triage workflow:**
1. `query-issues` - Find issues needing triage
2. For each issue:
   - `get-issue` - Get full details
   - `update-issue` - Assign and set priority
