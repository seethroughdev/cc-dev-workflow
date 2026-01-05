# Querying Linear Issues

Complete reference for searching and filtering Linear issues using the GraphQL API.

## Basic Query Structure

```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '<filter-json>' [limit]
```

Default limit: 50 issues

## Filter Syntax

Filters use nested JSON objects with comparison operators and logical combinators.

### Comparison Operators

- `eq` - Equals
- `neq` - Not equals
- `in` - In array
- `nin` - Not in array
- `contains` - Contains substring (case-insensitive)
- `notContains` - Does not contain substring
- `null` - Is null (boolean)

### Date Comparators

- `eq` - Equal to date
- `neq` - Not equal to date
- `gt` - Greater than
- `gte` - Greater than or equal
- `lt` - Less than
- `lte` - Less than or equal

### Logical Combinators

- `and` - All conditions must be true
- `or` - Any condition must be true

## Common Filter Patterns

### By Assignee

**My assigned issues:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "assignee": {"id": {"eq": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"}}
}'
```

**Unassigned issues:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "assignee": {"null": true}
}'
```

**Assigned to specific person:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "assignee": {"id": {"eq": "USER_ID"}}
}'
```

### By Status/State

**Issues in specific state:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "state": {"name": {"eq": "In Progress"}}
}'
```

**Issues by state type:**
```bash
# All started issues (in progress, in review, etc.)
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "state": {"type": {"eq": "started"}}
}'

# All completed issues
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "state": {"type": {"eq": "completed"}}
}'

# All backlog issues
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "state": {"type": {"eq": "backlog"}}
}'
```

**State types:**
- `triage` - Needs triage
- `backlog` - In backlog
- `unstarted` - Not started
- `started` - In progress
- `completed` - Done
- `canceled` - Canceled

### By Project

**Issues in specific project:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "project": {"id": {"eq": "62417c2a-8fbb-4583-9867-f93828cb2ebc"}}
}'
```

**Issues without project:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "project": {"null": true}
}'
```

### By Team

**Issues for Maya team:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "team": {"id": {"eq": "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"}}
}'
```

### By Label

**Issues with specific label:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "labels": {"some": {"id": {"eq": "LABEL_ID"}}}
}'
```

**Issues with any of multiple labels:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "labels": {"some": {"id": {"in": ["LABEL_ID_1", "LABEL_ID_2"]}}}
}'
```

### By Priority

**High priority issues:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "priority": {"eq": 2}
}'
```

**Urgent or high priority:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "priority": {"in": [1, 2]}
}'
```

Priority values:
- 0 = No priority
- 1 = Urgent
- 2 = High
- 3 = Normal
- 4 = Low

### By Date

**Issues created in last 7 days:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "createdAt": {"gte": "'$(date -u -v-7d +%Y-%m-%dT%H:%M:%S.000Z)'"}
}'
```

**Issues updated today:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "updatedAt": {"gte": "'$(date -u +%Y-%m-%dT00:00:00.000Z)'"}
}'
```

### By Title/Description

**Search title:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "title": {"contains": "login"}
}'
```

**Search description:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "description": {"contains": "authentication"}
}'
```

### By Parent/Child

**Sub-issues of specific parent:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "parent": {"id": {"eq": "PARENT_ISSUE_ID"}}
}'
```

**Issues with sub-issues:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "hasSubIssues": true
}'
```

## Combining Filters

### AND Logic (all conditions must match)

**My in-progress issues:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "and": [
    {"assignee": {"id": {"eq": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"}}},
    {"state": {"type": {"eq": "started"}}}
  ]
}'
```

**High priority bugs in specific project:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "and": [
    {"priority": {"eq": 2}},
    {"labels": {"some": {"name": {"eq": "bug"}}}},
    {"project": {"id": {"eq": "PROJECT_ID"}}}
  ]
}'
```

### OR Logic (any condition must match)

**Issues assigned to me or unassigned:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "or": [
    {"assignee": {"id": {"eq": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"}}},
    {"assignee": {"null": true}}
  ]
}'
```

### Complex Nested Filters

**My issues that are either urgent OR (high priority AND in progress):**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "and": [
    {"assignee": {"id": {"eq": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"}}},
    {"or": [
      {"priority": {"eq": 1}},
      {"and": [
        {"priority": {"eq": 2}},
        {"state": {"type": {"eq": "started"}}}
      ]}
    ]}
  ]
}'
```

## Response Format

Query responses include:

```json
{
  "success": true,
  "data": {
    "issues": {
      "nodes": [
        {
          "id": "issue-uuid",
          "identifier": "MAY-123",
          "title": "Issue title",
          "url": "https://linear.app/...",
          "priority": 2,
          "createdAt": "2025-11-20T12:00:00.000Z",
          "updatedAt": "2025-11-20T14:00:00.000Z",
          "state": {
            "name": "In Progress",
            "type": "started"
          },
          "assignee": {
            "name": "Adam Harris"
          },
          "team": {
            "name": "Maya",
            "key": "MAY"
          },
          "project": {
            "name": "Landing Grid with Custom Views"
          },
          "labels": {
            "nodes": [
              {"name": "feature"}
            ]
          }
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

## Pagination

Default limit: 50 issues

**Get more results:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{...}' 100
```

For cursor-based pagination (not yet implemented in wrapper):
- Check `pageInfo.hasNextPage`
- Use `pageInfo.endCursor` for next page

## Common Use Cases

### Sprint Planning

**All backlog issues for Maya team:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "and": [
    {"team": {"id": {"eq": "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"}}},
    {"state": {"type": {"eq": "backlog"}}}
  ]
}' 100
```

### Daily Standup

**My issues in progress or review:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "and": [
    {"assignee": {"id": {"eq": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b"}}},
    {"state": {"type": {"in": ["started"]}}}
  ]
}'
```

### Bug Triage

**All untriaged bugs:**
```bash
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "and": [
    {"labels": {"some": {"name": {"eq": "bug"}}}},
    {"state": {"type": {"eq": "triage"}}}
  ]
}'
```

### Project Status

**All issues in specific project, grouped by status:**
```bash
# Get all issues
node ~/.claude/api-wrappers/linear-api.mjs query-issues '{
  "project": {"id": {"eq": "PROJECT_ID"}}
}' 200

# Then group by state.type in processing
```

## Formatting Results for Display

Parse and format query results for readability:

```javascript
const result = JSON.parse(output);

if (!result.success) {
  console.log("Error:", result.error);
  return;
}

const issues = result.data.issues.nodes;

if (issues.length === 0) {
  console.log("No issues found");
  return;
}

console.log(`Found ${issues.length} issue(s):\n`);

issues.forEach(issue => {
  console.log(`${issue.identifier}: ${issue.title}`);
  console.log(`  Status: ${issue.state.name}`);
  console.log(`  Assignee: ${issue.assignee?.name || 'Unassigned'}`);
  console.log(`  Priority: ${getPriorityName(issue.priority)}`);
  console.log(`  URL: ${issue.url}\n`);
});

if (result.data.issues.pageInfo.hasNextPage) {
  console.log("(More results available)");
}
```
