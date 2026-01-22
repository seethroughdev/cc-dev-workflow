---
name: commit
description: Format, lint, and create logical commits from staged files. Use when asked to commit changes, or after completing a feature.
---

# Smart Commit

Create well-structured git commits by running format/lint, grouping related changes, and writing clear commit messages.

## Usage

```
/commit              # Commit staged changes
/commit push         # Commit and push
/commit --all        # Stage all and commit
```

## Workflow

### 1. Gather Context

Run these commands to understand the current state:

```bash
git diff --cached --name-only          # Staged files
git diff --name-only                   # Unstaged files
git branch --show-current              # Current branch
git log --oneline -5                   # Recent commits for style
```

### 2. Check for Conflicts

**Critical**: Compare staged vs unstaged file lists. If any file appears in both:

1. Stop and ask the user:
   - "File X has both staged and unstaged changes. Running format/lint may cause conflicts."
   - Options: "Stash unstaged first", "Stage all changes for this file", "Skip formatting", "Abort"

2. Only proceed after user confirms approach for each conflicting file.

### 3. Format and Lint

Identify project tools (check for Makefile, package.json, pyproject.toml):

| Project Type | Format Command | Lint Command |
|--------------|----------------|--------------|
| Python | `make format` or `ruff format <files>` | `ruff check --fix <files>` |
| JS/TS | `npm run format` or `npx prettier --write <files>` | `npm run lint:fix` |
| Go | `go fmt <files>` | `golangci-lint run --fix` |

Run format/lint on staged files only, then re-stage any modified files:
```bash
git add <formatted-files>
```

### 4. Group Changes Logically

Review the staged diff and group files by logical unit:
- Feature additions
- Bug fixes
- Refactors
- Config/dependency changes
- Tests
- Docs

Each group becomes one commit.

### 5. Create Commits

For each logical group:

1. Unstage files not in current group:
   ```bash
   git restore --staged <other-files>
   ```

2. Write commit message following conventions:
   - Format: `type(scope): description`
   - Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`, `perf`
   - Present tense, lowercase, no period
   - Be specific to what actually changed

3. Commit:
   ```bash
   git commit -m "type(scope): specific description"
   ```

4. Re-stage remaining files and repeat.

### 6. Post-Commit Operations

If arguments include `push`:
```bash
git push
```

If arguments include `--all`:
- Stage all changes first: `git add -A`
- Then proceed with format/lint/commit flow

## Commit Message Rules

**Do:**
- Present tense: "add", "fix", "remove", "update"
- Be specific: `fix null check in user validation`
- Under 72 characters
- Use conventional commit types

**Don't:**
- No emojis
- No "enhance" (use "improve", "extend", "refine")
- No AI attribution or Co-Authored-By
- No generic messages like "update files"
- No period at end

## Examples

```
feat(auth): add password reset flow
fix(api): handle null response from payment service
refactor(utils): extract date formatting helpers
test(user): add coverage for edge cases in validation
chore(deps): update react to 18.2
docs(readme): add deployment instructions
```

## Single File Quick Path

If only one file is staged and it's a simple change:
- Skip grouping analysis
- Format/lint the file
- Commit with appropriate message
- Done
