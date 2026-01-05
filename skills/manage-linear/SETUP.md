# Linear Skill Setup Guide

Complete setup instructions for the `manage-linear` skill.

## Prerequisites

- Node.js installed (for running the API wrapper)
- Linear workspace access
- Linear API key

## Setup Steps

### 1. Create Credentials File

Create the credentials file:

```bash
mkdir -p ~/.claude/credentials
touch ~/.claude/credentials/linear.json
chmod 600 ~/.claude/credentials/linear.json
```

### 2. Get Your Linear API Key

1. Go to https://linear.app/settings/api
2. Click "Create key"
3. Name it "Claude Code" or similar
4. Copy the generated key (starts with `lin_api_`)

### 3. Add API Key to Credentials File

Edit `~/.claude/credentials/linear.json`:

```json
{
  "apiKey": "lin_api_YOUR_KEY_HERE"
}
```

Replace `lin_api_YOUR_KEY_HERE` with your actual API key.

### 4. Copy Template Files (If Not Already Present)

The skill expects ticket templates at:

```
~/.claude/templates/ticket-feature.md
~/.claude/templates/ticket-bug.md
~/.claude/templates/ticket-task.md
```

If you have project-specific templates (like in `docs/templates/`), you can:
- Copy them to `~/.claude/templates/`
- Or update the skill to reference your project templates

### 5. Verify API Wrapper is Executable

```bash
chmod +x ~/.claude/api-wrappers/linear-api.mjs
```

### 6. Test the Setup

Test that the API wrapper can connect:

```bash
node ~/.claude/api-wrappers/linear-api.mjs get-teams
```

Expected output:
```json
{
  "success": true,
  "data": {
    "teams": {
      "nodes": [
        {
          "id": "...",
          "name": "Maya",
          "key": "MAY"
        }
      ]
    }
  }
}
```

If you see an error about credentials:
- Check that `~/.claude/credentials/linear.json` exists
- Verify the API key is correct
- Ensure the file is valid JSON

## File Structure

After setup, you should have:

```
~/.claude/
├── credentials/
│   └── linear.json                    # Your API key (never commit!)
├── api-wrappers/
│   └── linear-api.mjs                 # Secure API wrapper
├── skills/
│   └── manage-linear/
│       ├── SKILL.md                   # Main skill file
│       ├── SETUP.md                   # This file
│       └── references/
│           ├── creating-tickets.md    # Ticket creation workflow
│           ├── querying-issues.md     # Query filters reference
│           ├── updating-issues.md     # Update operations reference
│           ├── reviewing-tickets.md   # Ticket review workflow
│           └── api-operations.md      # Complete API reference
├── commands/
│   └── linear.md                      # Slash command wrapper
└── templates/
    ├── ticket-feature.md              # Feature ticket template
    ├── ticket-bug.md                  # Bug ticket template
    └── ticket-task.md                 # Task ticket template
```

## Security Notes

**IMPORTANT:**

1. **Never commit credentials** - The `linear.json` file contains your API key
2. **Never share your API key** - It provides full access to your Linear workspace
3. **Rotate keys regularly** - Generate new keys periodically for security
4. **Use file permissions** - Keep credentials file readable only by you (`chmod 600`)

The API wrapper is designed to prevent credentials from appearing in:
- Chat output
- Tool call parameters
- Error messages

All API calls are made server-side through the wrapper.

## Troubleshooting

### Error: "Failed to load credentials"

**Cause:** Credentials file doesn't exist or is invalid JSON

**Solution:**
```bash
# Check if file exists
ls -la ~/.claude/credentials/linear.json

# Check file contents (make sure it's valid JSON)
cat ~/.claude/credentials/linear.json

# Fix JSON formatting if needed
echo '{"apiKey": "lin_api_YOUR_KEY"}' > ~/.claude/credentials/linear.json
```

### Error: "Linear API key not found"

**Cause:** Credentials file exists but doesn't have `apiKey` field

**Solution:**
```bash
# Ensure the file has the correct structure
cat > ~/.claude/credentials/linear.json << 'EOF'
{
  "apiKey": "lin_api_YOUR_ACTUAL_KEY_HERE"
}
EOF
```

### Error: 401 Unauthorized

**Cause:** Invalid or expired API key

**Solution:**
1. Go to https://linear.app/settings/api
2. Revoke the old key
3. Create a new key
4. Update `~/.claude/credentials/linear.json` with new key

### Error: "command not found: node"

**Cause:** Node.js not installed

**Solution:**
```bash
# Install Node.js
# macOS:
brew install node

# Or download from: https://nodejs.org/
```

### Rate Limit Errors

**Cause:** Exceeded API rate limit (1,500 requests/hour)

**Solution:**
- Wait for rate limit to reset (at top of next hour)
- Batch operations when possible
- Cache reference data (teams, projects, users) to reduce queries

## Usage Examples

### Create a Feature Ticket

```
User: /linear create a feature ticket for dark mode toggle
```

The skill will:
1. Ask clarifying questions
2. Read the feature template
3. Generate formatted description
4. Preview for approval
5. Create via API wrapper
6. Return ticket URL

### Query Your Issues

```
User: /linear show my issues in progress
```

The skill will:
1. Query issues with your assignee ID and "started" state
2. Format results as readable list
3. Include ticket URLs

### Update Issue Status

```
User: /linear move MAY-123 to in progress
```

The skill will:
1. Get workflow states for the team
2. Find "In Progress" state ID
3. Update issue via API wrapper
4. Confirm update

### Review a Ticket

```
User: /linear review MAY-285
```

The skill will:
1. Fetch ticket details
2. Analyze codebase for relevant areas
3. Create 3-phase implementation plan
4. Ask if you want to save to docs/specs/

## Next Steps

After setup:

1. **Try creating a test ticket** to verify everything works
2. **Review the reference files** in `references/` for detailed documentation
3. **Customize templates** if you want different ticket formats
4. **Set up your team defaults** in the skill (already configured for Maya team)

## Support

If you encounter issues not covered here:

1. Check the reference files in `~/.claude/skills/manage-linear/references/`
2. Verify credentials file format and permissions
3. Test API wrapper directly to isolate issues
4. Check Linear API status: https://status.linear.app/
