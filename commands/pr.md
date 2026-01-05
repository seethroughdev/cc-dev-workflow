---
description: Generate or edit comprehensive PR descriptions with Linear ticket integration
tools: [Bash, Read, mcp__linear__get_issue]
---

# Generate or Edit PR Description

Generate a comprehensive pull request description using the template at `/Users/adamw/.claude/templates/pr-new.md`, with automatic Linear ticket integration.

## Arguments:
- `$ARGUMENTS` - Optional PR URL or number for editing existing PRs
  - Examples: `123`, `#456`, `https://github.com/owner/repo/pull/789`
  - If empty, creates new PR description

## Detection and mode selection:

- If `$ARGUMENTS` contains a PR URL or number, switch to **edit mode**
- If `$ARGUMENTS` is empty, use **create mode** for new PR descriptions

## Steps to follow:

1. **Determine mode and get context:**

   **For edit mode (when `$ARGUMENTS` contains PR URL/number):**
   - Parse `$ARGUMENTS` to extract PR number from URL or direct number
   - Use `gh pr view $ARGUMENTS` to get current PR description and details
   - Extract existing content to understand current state

   **For create mode (when `$ARGUMENTS` is empty):**
   - Get the current git branch name using `git branch --show-current`
   - If the branch name contains a Linear ticket ID (format: maya-123, maya-1234, etc.), extract it
   - Use `mcp__linear__get_issue` with the extracted ticket ID to fetch Linear ticket details
   - If ticket found, incorporate its title, description, and details into the PR description

2. **Read the PR template:**

   - Read the template at `/Users/adamw/.claude/templates/pr-new.md`
   - Understand all sections and requirements

3. **Analyze git changes:**

   **For both modes:**
   - Run `git log --oneline main..HEAD` to see commits since branching from main
   - Run `git diff main...HEAD` to see committed changes only (not uncommitted files)
   - Run `git diff --name-only main...HEAD` to get list of changed files

4. **Generate or update PR description:**

   **For create mode:**
   - Use the PR template structure from step 2
   - If Linear ticket found, incorporate its title, description, and acceptance criteria into relevant sections
   - Fill in Summary based on git changes and ticket context
   - Populate Problem section with ticket details or inferred issues from code changes
   - Describe Solution approach based on code changes
   - List specific Changes by file with key modifications
   - Create Testing checklist (use ticket acceptance criteria if available)
   - Assess Impact (breaking changes, migration needs, etc.)
   - Add Review Notes highlighting key areas

   **For edit mode:**
   - Preserve existing good content from current PR description
   - Update sections that need improvement based on latest git changes
   - Maintain the overall structure and any custom sections already added
   - Only modify sections that clearly need updates

5. **Review and simplify:**

   - Remove any redundant information between sections
   - Eliminate unnecessary details that don't add value
   - Ensure each section serves a distinct purpose
   - Keep language clear, direct, and scannable
   - Remove filler words and verbose explanations

6. **Format and present:**
   - Present the complete PR description using the template format
   - Include Linear ticket link if found using the URL from the Linear MCP response
   - Ensure all placeholders are replaced with actual content
   - Follow the writing style guidelines (no emojis, no em-dashes, avoid "enhance")
   - IMPORTANT: Never mention Claude, AI assistance, or automated generation anywhere in the PR description

7. **Confirm with user:**
   - **For create mode:** Ask if ready to create the PR
   - **For edit mode:** Ask if ready to update the existing PR description
   - Example: "I've prepared the PR description above. Are you ready to create/update the PR, or would you like me to make any changes first?"
   - Wait for confirmation before proceeding with any PR creation/update actions

## Linear ticket integration:

- Extract ticket ID from branch name using regex pattern
- Fetch ticket details using `mcp__linear__get_issue`
- Use the URL field from the Linear MCP response for the ticket link
- Include ticket link in final PR description if found

## Error handling:

- If no git repository, inform user and exit
- If no Linear ticket found in branch name, proceed with standard PR generation
- If Linear API fails, proceed without ticket integration but note the attempt
