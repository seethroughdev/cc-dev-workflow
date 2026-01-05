# Reviewing Linear Tickets

Workflow for reviewing Linear tickets and creating 3-phase implementation plans.

## Overview

The ticket review process:
1. Fetch ticket details from Linear
2. Analyze codebase for relevant areas
3. Create strategic 3-phase implementation plan
4. Save plan to specs folder for reference

This replaces the `/ticket:review` slash command functionality.

## Workflow Steps

### Step 1: Extract Ticket ID

Accept various formats:
- Linear URL: `https://linear.app/albert-invent/issue/MAY-285/remove-legacy-maya-ui`
- Ticket identifier: `MAY-285`
- Just the number: `285` (assumes MAY team)

```javascript
function extractTicketId(input) {
  // From URL
  const urlMatch = input.match(/issue\/([A-Z]+-\d+)/);
  if (urlMatch) return urlMatch[1];

  // From identifier
  const idMatch = input.match(/^([A-Z]+-\d+)$/);
  if (idMatch) return idMatch[1];

  // Just number, assume MAY
  const numMatch = input.match(/^\d+$/);
  if (numMatch) return `MAY-${numMatch[0]}`;

  return input.trim();
}
```

### Step 2: Fetch Ticket Details

```bash
node ~/.claude/api-wrappers/linear-api.mjs get-issue "MAY-285"
```

Response includes:
- `title` - Issue title
- `description` - Full markdown description
- `url` - Linear URL
- `priority` - Priority level
- `state` - Current workflow state
- `assignee` - Assigned user
- `team` - Team information
- `project` - Project information
- `labels` - Applied labels
- `parent` - Parent issue (if sub-issue)
- `children` - Sub-issues

### Step 3: Analyze Codebase

Use the Task tool with `codebase-analyzer` subagent to identify relevant areas:

```
Use Task tool with prompt:
"Analyze the codebase for areas relevant to this Linear ticket:

Title: {title}
Description: {description}

Identify:
1. Relevant directories and files mentioned or implied
2. Existing patterns that relate to the requirements
3. Dependencies and integration points
4. Potential impact areas
5. Similar implementations to reference

Provide specific file paths and code patterns."
```

The codebase-analyzer will:
- Search for mentioned files, components, or modules
- Find related patterns and existing implementations
- Identify dependencies and integration points
- Note potential areas of impact

### Step 4: Create 3-Phase Implementation Plan

Based on ticket requirements and codebase analysis, create a strategic plan.

**Plan Structure:**

```markdown
# Ticket Review: {IDENTIFIER} - {Title}

**Ticket Link:** {url}

**Summary:** {Brief description of what needs to be done}

## Codebase Analysis

{Results from codebase-analyzer subagent}

Key files identified:
- path/to/file1.ext - Purpose
- path/to/file2.ext - Purpose
- ...

Existing patterns found:
- Pattern 1 description (file:line)
- Pattern 2 description (file:line)

## Implementation Plan

### Phase 1: Research & Understanding

High-level areas to investigate before starting:

- Area 1: What to understand and why
- Area 2: Dependencies to explore
- Area 3: Existing patterns to review

Questions to answer:
- Question 1
- Question 2

### Phase 2: Implementation Approach

General strategy and technical considerations:

- Approach 1: What needs to be done and general strategy
- Approach 2: Technical decisions to make
- Approach 3: Key areas where changes might be needed

Considerations:
- Consideration 1
- Consideration 2

### Phase 3: Validation & Completion

How to verify and integrate the changes:

- Validation 1: How to test the implementation
- Validation 2: Integration points to verify
- Validation 3: Rollout or deployment approach

Testing strategy:
- Test approach 1
- Test approach 2

## Questions & Considerations

{Any unclear requirements or decisions needed}

- Question or consideration 1
- Question or consideration 2
```

**Important Guidelines:**

- **High-level approaches**, not specific implementation tasks
- **Strategic thinking**, not detailed code changes
- **Questions and considerations**, not assumptions
- **File references** with line numbers where relevant
- **No code suggestions** in the plan (research and strategy only)

### Step 5: Present Plan and Ask for Feedback

Show the plan to the user:

```
Here's the implementation plan for {IDENTIFIER}:

[Display the formatted plan]

Would you like me to:
1. Adjust any phase or add more details
2. Save this to docs/specs/
3. Dive deeper into a specific phase
```

### Step 6: Save Plan (If Confirmed)

If user approves:

1. Check if `docs/specs/` exists in project
2. If not, ask: "The docs/specs/ folder doesn't exist. Create it and proceed, or skip saving?"
3. Generate filename: `YYYY-MM-DD-{slug-from-title}.md`
4. Save plan to file
5. Confirm: "Saved plan to docs/specs/{filename}"

```bash
# Generate filename
DATE=$(date +%Y-%m-%d)
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')
FILENAME="$DATE-$SLUG.md"

# Check if directory exists
if [ ! -d "docs/specs" ]; then
  # Ask user if should create
  read -p "Create docs/specs/? (y/n) " -n 1 -r
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p docs/specs
  else
    echo "Skipping save"
    exit 0
  fi
fi

# Save file
cat > "docs/specs/$FILENAME" << 'EOF'
[Plan content here]
EOF

echo "Saved to docs/specs/$FILENAME"
```

## Example: Complete Review Workflow

**User:** "Review MAY-285"

**Step 1: Extract ID**
```
Ticket ID: MAY-285
```

**Step 2: Fetch Details**
```bash
node ~/.claude/api-wrappers/linear-api.mjs get-issue "MAY-285"
```

Response:
```json
{
  "success": true,
  "data": {
    "issue": {
      "id": "...",
      "identifier": "MAY-285",
      "title": "Remove legacy Maya UI components",
      "description": "## Problem\n\nLegacy Maya UI components are causing maintenance overhead...",
      "url": "https://linear.app/albert-invent/issue/MAY-285",
      "priority": 3,
      "state": {"name": "Backlog", "type": "backlog"},
      "assignee": {"name": "Adam Harris"},
      "team": {"name": "Maya", "key": "MAY"},
      "project": {"name": "Albert UI"}
    }
  }
}
```

**Step 3: Analyze Codebase**
```
Using Task tool with codebase-analyzer:

"Analyze codebase for ticket MAY-285: Remove legacy Maya UI components.

The ticket describes removing old Maya UI components that are causing maintenance overhead.

Find:
1. Where Maya UI components are defined
2. Where they're imported and used
3. What depends on them
4. Modern replacements that exist"
```

Agent finds:
- `src/legacy/maya-ui/` directory with old components
- 15 files importing from `maya-ui`
- Modern equivalents in `src/components/`
- Build config references in webpack.config.js

**Step 4: Create Plan**
```markdown
# Ticket Review: MAY-285 - Remove legacy Maya UI components

**Ticket Link:** https://linear.app/albert-invent/issue/MAY-285

**Summary:** Remove legacy Maya UI components causing maintenance overhead and migrate to modern component library.

## Codebase Analysis

Legacy components located in:
- src/legacy/maya-ui/ - Old component library (500+ lines)

Components still using legacy imports:
- src/pages/inventory/InventoryGrid.jsx:12
- src/pages/tasks/TaskList.jsx:8
- src/components/forms/FormBuilder.jsx:15
(12 more files)

Modern replacements available:
- src/components/ui/ - New component library
- Already used in 40+ components

Build configuration:
- webpack.config.js:45 - Legacy path alias

## Implementation Plan

### Phase 1: Research & Understanding

- Inventory all legacy component usage across the codebase
- Map each legacy component to its modern equivalent
- Identify any components without direct replacements
- Review dependency graph to understand import chains
- Check if any external packages depend on legacy components

Questions to answer:
- Are there any components without modern equivalents?
- What's the migration path for components with behavioral differences?
- Are there any breaking changes in the modern components?

### Phase 2: Implementation Approach

- Create migration guide mapping old → new components
- Decide on migration strategy (big bang vs incremental)
- Update imports file by file to use modern components
- Address any API differences between old and new
- Remove legacy directory and build config references
- Update documentation to reference new components

Considerations:
- Consider feature flag if incremental migration preferred
- Test coverage for affected areas
- Communication plan for team about component changes

### Phase 3: Validation & Completion

- Verify all imports updated (no legacy references remain)
- Run full test suite to catch behavioral regressions
- Manual testing of affected pages and features
- Check bundle size impact (should decrease)
- Update team documentation and onboarding materials

Testing strategy:
- Automated: Component tests, integration tests
- Manual: User flows in affected areas
- Performance: Bundle size comparison

## Questions & Considerations

- Should this be done incrementally with feature flag, or all at once?
- Are there any known behavioral differences that need addressing?
- Timeline for this work - should it block other features?
```

**Step 5: Present and Get Feedback**
```
Here's the implementation plan for MAY-285: Remove legacy Maya UI components

[Display plan above]

Would you like me to:
1. Adjust any phase or add more details
2. Save this to docs/specs/
3. Dive deeper into a specific phase
```

**Step 6: Save (If User Confirms)**

User: "Yes, save it"

```bash
# Save to docs/specs/2025-11-20-remove-legacy-maya-ui-components.md
```

Response: "Saved plan to docs/specs/2025-11-20-remove-legacy-maya-ui-components.md"

## Tips for Effective Plans

**Good Phase 1 (Research):**
- Specific areas to investigate
- Questions that need answers
- Existing patterns to understand
- Not: "Look at the code"

**Good Phase 2 (Implementation):**
- High-level strategy
- Key decision points
- Areas requiring changes
- Not: Specific code changes or file edits

**Good Phase 3 (Validation):**
- How to verify it works
- Integration checkpoints
- Testing approach
- Not: Exact test cases

**Good Questions:**
- Genuine unknowns that need clarification
- Architectural decisions to make
- Timeline or priority considerations
- Not: Things answerable from ticket

## Integration with Other Workflows

After creating the plan:
- Reference plan when implementing: "See docs/specs/{filename}"
- Update plan during implementation if approach changes
- Link plan in PR description
- Archive plan after completion
