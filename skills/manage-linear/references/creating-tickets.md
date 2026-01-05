# Creating Linear Tickets

Complete workflow for creating feature, bug, and task tickets with proper templates and formatting.

## Ticket Creation Workflow

### Step 1: Determine Ticket Type

Ask the user which type (if not specified):
- **Feature**: New functionality or capability
- **Bug**: Something broken that needs fixing
- **Task**: Technical work, refactoring, or maintenance

### Step 2: Gather Required Information

**CRITICAL**: Must get "Problem to solve" - never create tickets with only implementation details.

If user only provides implementation: "To write a good ticket, please explain the problem you're trying to solve from a user perspective."

**For Features:**
- User story (who, what, why)
- Description of what needs to be built
- Why it's valuable
- Acceptance criteria (specific, testable)
- Any design links or resources

**For Bugs:**
- Bug description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Impact and severity
- Error messages or screenshots

**For Tasks:**
- Problem being addressed
- Proposed solution
- Context and dependencies
- Acceptance criteria
- Related resources

### Step 3: Read Template

Read the appropriate template file:
- Feature: `/Users/adamw/.claude/templates/ticket-feature.md`
- Bug: `/Users/adamw/.claude/templates/ticket-bug.md`
- Task: `/Users/adamw/.claude/templates/ticket-task.md`

### Step 4: Format Description

Use template structure to format the description in markdown.

**Style Requirements:**
- NO emojis anywhere
- NO em-dashes (—) - use regular dashes (-) or commas
- AVOID "enhance" - use improve, add, fix, update, implement
- Clear, scannable content
- Acceptance criteria as checkbox list: `- [ ] Criterion`

### Step 5: Preview for Approval

Show user the complete ticket description:

```
Here's the ticket description I've prepared:

---
## Feature: [Title]

### User Story
As a [user], I want [goal] so that [benefit].

### Description
[Clear description]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
---

Does this look good, or would you like to make any edits?
```

### Step 6: Create Ticket via API

Once approved, create using secure API wrapper:

```bash
node ~/.claude/api-wrappers/linear-api.mjs create-issue '{
  "teamId": "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8",
  "title": "Clean ticket title without emojis",
  "description": "Complete markdown description from template",
  "projectId": "62417c2a-8fbb-4583-9867-f93828cb2ebc",
  "assigneeId": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b",
  "priority": 2,
  "stateId": "TRIAGE_STATE_ID",
  "labelIds": ["LABEL_ID_1", "LABEL_ID_2"]
}'
```

**Required Fields:**
- `teamId` - Default: Maya (`ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8`)
- `title` - Cleaned up, no emojis
- `description` - Markdown formatted from template
- `projectId` - Default: Landing Grid with Custom Views
- `assigneeId` - Default: Adam Harris

**Optional but Recommended:**
- `priority` - 0=None, 1=Urgent, 2=High, 3=Normal, 4=Low
  - Features: 2 (High) by default
  - Bugs: Based on severity
  - Tasks: 3 (Normal) by default
- `stateId` - Workflow state (usually "Triage")
- `labelIds` - Apply relevant labels

### Step 7: Return Result

Parse response and return formatted result:

```javascript
const result = JSON.parse(output);

if (!result.success) {
  return `Error creating ticket: ${result.error || result.errors}`;
}

const issue = result.data.issueCreate.issue;
return `Created ${issue.identifier}: ${issue.url}`;
```

## Default Priority Guidelines

- **Features**: Priority 2 (High) - new functionality is important
- **Bugs**:
  - Critical (P1): Production down, security issue
  - High (P2): Major functionality broken, many users affected
  - Normal (P3): Minor issues, workarounds available
  - Low (P4): Cosmetic, nice-to-have fixes
- **Tasks**: Priority 3 (Normal) - technical work, refactoring

## Adding Links to Tickets

External resources should use the `links` array (not just markdown links):

```json
{
  "links": [
    {
      "url": "https://figma.com/file/abc123",
      "title": "Design Mockups"
    },
    {
      "url": "https://github.com/org/repo/pull/456",
      "title": "Related PR"
    }
  ]
}
```

## Label Assignment

Common label patterns:
- Type labels: `feature`, `bug`, `task`
- Status labels: `needs-review`, `needs-triage`, `blocked`
- Area labels: `frontend`, `backend`, `infrastructure`

Get label IDs:
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-labels "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8"
```

## Complete Example

**User Request:** "Create a bug ticket for login button not working on mobile"

**Process:**

1. Ask clarifying questions:
   - "What happens when you tap the login button?"
   - "Which mobile OS and browser?"
   - "Does it work on desktop?"

2. User provides:
   - Button doesn't respond on iOS Safari
   - Works fine on desktop
   - No error messages

3. Read bug template

4. Format description:
```markdown
## Bug Description
The login button on the mobile app does not respond to touch events on iOS devices.

## Steps to Reproduce
1. Open app on iPhone 12 or newer
2. Navigate to login page
3. Enter valid credentials
4. Tap the "Login" button

## Expected Behavior
Button should respond to tap and initiate authentication.

## Actual Behavior
Button does not respond to touch events. No visual feedback, no authentication attempt.

## Environment
- Browser: Safari Mobile
- OS: iOS 16.4+
- App Version: v2.1.3

## Impact
- Severity: High
- Users Affected: All iOS mobile users (~40% of user base)
```

5. Preview for user approval

6. Create:
```bash
node ~/.claude/api-wrappers/linear-api.mjs create-issue '{
  "teamId": "ec32d1a7-ef2a-4ddf-b3a3-900dfc229fa8",
  "title": "Login button not responding on iOS Safari",
  "description": "[formatted markdown above]",
  "projectId": "62417c2a-8fbb-4583-9867-f93828cb2ebc",
  "assigneeId": "022c9ced-1c33-4c6e-bc5b-8e2ee4bcd87b",
  "priority": 2
}'
```

7. Return: "Created MAY-789: https://linear.app/albert-invent/issue/MAY-789"
