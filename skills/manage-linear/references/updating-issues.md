# Updating Linear Issues

Complete reference for updating issue properties using the Linear GraphQL API.

## Basic Update Structure

```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "<ISSUE_ID>" '<update-json>'
```

Issue ID can be UUID or identifier (e.g., "MAY-123")

## Update Fields Reference

All fields are optional - only include fields you want to change.

### Basic Properties

**Update title:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "title": "New title without emojis"
}'
```

**Update description:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "description": "Updated description in markdown format"
}'
```

**Update priority:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "priority": 1
}'
```

Priority values:
- 0 = No priority
- 1 = Urgent
- 2 = High
- 3 = Normal
- 4 = Low

**Update estimate:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "estimate": 5
}'
```

### Assignment

**Assign to user:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "assigneeId": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"
}'
```

**Unassign:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "assigneeId": null
}'
```

**Delegate to agent:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "delegateId": "AGENT_USER_ID"
}'
```

### Status/State

**Change workflow state:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "stateId": "STATE_ID"
}'
```

Get workflow states:
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-workflow-states "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"
```

Common state transitions:
- Triage → Backlog
- Backlog → In Progress
- In Progress → In Review
- In Review → Done
- Any → Canceled

### Project and Team

**Move to different project:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "projectId": "PROJECT_ID"
}'
```

**Remove from project:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "projectId": null
}'
```

**Move to different team:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "teamId": "TEAM_ID"
}'
```

**Note:** Moving teams may reset state, project, and other team-specific fields.

### Labels

**Replace all labels:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "labelIds": ["LABEL_ID_1", "LABEL_ID_2"]
}'
```

**Add labels (preserves existing):**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "addedLabelIds": ["NEW_LABEL_ID"]
}'
```

**Remove specific labels:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "removedLabelIds": ["LABEL_ID_TO_REMOVE"]
}'
```

**Clear all labels:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "labelIds": []
}'
```

Get available labels:
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-labels "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"
```

### Parent/Child Relationships

**Make issue a sub-issue:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "parentId": "PARENT_ISSUE_ID"
}'
```

**Remove parent (make top-level):**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "parentId": null
}'
```

### Cycle

**Add to cycle:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "cycleId": "CYCLE_ID"
}'
```

**Remove from cycle:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "cycleId": null
}'
```

Get team cycles:
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-cycles "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"
```

### Subscribers

**Set subscribers (replaces all):**
```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "subscriberIds": ["USER_ID_1", "USER_ID_2"]
}'
```

## Multiple Field Updates

Update multiple fields in single call:

```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "title": "Updated title",
  "description": "Updated description",
  "assigneeId": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b",
  "priority": 2,
  "stateId": "STATE_ID",
  "addedLabelIds": ["LABEL_ID"]
}'
```

## Common Update Patterns

### Move to In Progress

```bash
# 1. Get "In Progress" state ID
node ~/.claude/api-wrappers/linear-api.mjs get-workflow-states "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"

# 2. Update issue
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "stateId": "IN_PROGRESS_STATE_ID",
  "assigneeId": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"
}'
```

### Mark as Done

```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "stateId": "DONE_STATE_ID"
}'
```

### Escalate Priority

```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "priority": 1,
  "addedLabelIds": ["URGENT_LABEL_ID"]
}'
```

### Reassign Issue

```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "assigneeId": "NEW_ASSIGNEE_ID"
}'
```

### Move to Different Project

```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "projectId": "NEW_PROJECT_ID"
}'
```

### Add Bug Label

```bash
# 1. Get bug label ID
node ~/.claude/api-wrappers/linear-api.mjs get-labels "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"

# 2. Add label
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "addedLabelIds": ["BUG_LABEL_ID"]
}'
```

### Block Issue

```bash
node ~/.claude/api-wrappers/linear-api.mjs update-issue "MAY-123" '{
  "addedLabelIds": ["BLOCKED_LABEL_ID"],
  "description": "## Blocked\n\nReason: Waiting for API access\n\n[original description]"
}'
```

## Response Format

Update responses include the updated issue:

```json
{
  "success": true,
  "data": {
    "issueUpdate": {
      "success": true,
      "issue": {
        "id": "issue-uuid",
        "identifier": "MAY-123",
        "title": "Updated title",
        "url": "https://linear.app/...",
        "state": {
          "name": "In Progress"
        },
        "assignee": {
          "name": "Adam Harris",
          "email": "adam@example.com"
        }
      }
    }
  }
}
```

## Error Handling

Common errors:

**Issue not found:**
```json
{
  "success": false,
  "errors": [
    {"message": "Issue not found"}
  ]
}
```

**Invalid state for team:**
```json
{
  "success": false,
  "errors": [
    {"message": "State does not belong to issue's team"}
  ]
}
```

**Invalid field value:**
```json
{
  "success": false,
  "errors": [
    {"message": "Priority must be between 0 and 4"}
  ]
}
```

## Field Validation

Before updating, verify:

**State IDs** - Must belong to issue's team
**Project IDs** - Must belong to issue's team (or team must have access)
**Label IDs** - Should belong to issue's team (or be workspace labels)
**User IDs** - Must be active workspace members
**Priority** - Must be 0-4
**Estimate** - Must be positive integer or null

## Getting Reference IDs

**Get team's workflow states:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-workflow-states "TEAM_ID"
```

**Get team's labels:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-labels "TEAM_ID"
```

**Get team's projects:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-projects "TEAM_ID"
```

**Get workspace users:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-users
```

## Bulk Updates

To update multiple issues, call the API wrapper multiple times:

```bash
for issue_id in MAY-123 MAY-124 MAY-125; do
  node ~/.claude/api-wrappers/linear-api.mjs update-issue "$issue_id" '{
    "priority": 2
  }'
done
```

## Formatting Update Results

Parse and display update results:

```javascript
const result = JSON.parse(output);

if (!result.success) {
  console.log(`Error updating ${issueId}:`, result.error || result.errors);
  return;
}

const issue = result.data.issueUpdate.issue;
console.log(`Updated ${issue.identifier}:`);
console.log(`  Title: ${issue.title}`);
console.log(`  Status: ${issue.state.name}`);
console.log(`  Assignee: ${issue.assignee?.name || 'Unassigned'}`);
console.log(`  URL: ${issue.url}`);
```
