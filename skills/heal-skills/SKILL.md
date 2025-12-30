---
name: heal-skills
description: Self-learning system that analyzes session transcripts to identify activated skills and propose improvements based on mistakes or learnings. Automatically triggered via Stop hook or manually invoked.
---

<objective>
Analyze the current session to identify skills that were activated, detect mistakes or learnings, and propose updates to those skills. This creates a continuous improvement loop where skills evolve based on real usage.
</objective>

<quick_start>
Manually trigger reflection:
```
/heal-skills
```

With specific focus:
```
/heal-skills --skill refactor-specialist
```

Review without making changes:
```
/heal-skills --dry-run
```
</quick_start>

<process>
<step_1>
**Locate and parse transcript**

The transcript path is available from:
- Hook input: `transcript_path` in stdin JSON
- Manual: `~/.claude/projects/[project-hash]/[session-id]/transcript.jsonl`

Read the transcript file. Each line is a JSON object representing a conversation turn.

Look for skill activations by searching for patterns:
- `"tool_name": "Skill"` tool calls
- Skill file reads: `skills/*/SKILL.md`
- References to skill names in assistant responses
</step_1>

<step_2>
**Identify activated skills**

From the transcript, extract:
1. Which skills were explicitly invoked (via Skill tool)
2. Which skill files were read (via Read tool on SKILL.md files)
3. Skill names mentioned in context

Create a list of activated skills with their file paths:
```
Activated Skills:
- refactor-specialist: skills/refactor-specialist/SKILL.md
- heal-skills: skills/heal-skills/SKILL.md
```

If no skills were activated, report this and exit gracefully.
</step_2>

<step_3>
**Analyze session for learnings**

Review the transcript for learning opportunities:

**Mistakes to capture:**
- Tool calls that failed and required retry
- Incorrect assumptions that were corrected
- User corrections or clarifications
- Approaches that didn't work and were abandoned

**Improvements to capture:**
- Better patterns discovered during execution
- Edge cases encountered that weren't covered
- Missing steps that had to be added
- Clarifications that would help future runs

**Success patterns to reinforce:**
- Approaches that worked well
- Efficient sequences of operations
- User praise or confirmation of good output

For each learning, note:
- What happened (the context)
- What was learned (the insight)
- Which skill it applies to
- Suggested update (specific text change)
</step_3>

<step_4>
**Read current skill content**

For each activated skill with proposed learnings:
1. Read the full SKILL.md file
2. Identify the section where the learning applies:
   - `<process>` for workflow improvements
   - `<analysis_techniques>` or similar for method improvements
   - `<edge_cases>` or `<gotchas>` for warnings (create if needed)
   - `<examples>` for new examples
</step_4>

<step_5>
**Present findings and proposals**

Format the analysis:

```markdown
## Session Learning Analysis

### Skills Activated
- [skill-name]: [brief description of usage]

### Learnings Identified

#### 1. [Learning Title]
**Context**: What happened in the session
**Insight**: What we learned
**Applies to**: [skill-name]
**Proposed change**:
Location: `<section_name>` in SKILL.md
```diff
- Old text (if replacing)
+ New text to add
```

#### 2. [Next Learning]
...

### Summary
- X skills were activated
- Y learnings identified
- Z proposed updates
```
</step_5>

<step_6>
**Get user approval**

Present options:

"How would you like to proceed?"
1. **Apply all changes** - Update all skills with proposed learnings
2. **Review individually** - Go through each change one by one
3. **Save for later** - Write proposals to `.planning/skill-learnings-[date].md`
4. **Skip** - Don't apply any changes this time

Wait for user response before proceeding.
</step_6>

<step_7>
**Apply approved changes**

Based on user choice:

**Apply all**: Make each edit to the skill files, adding new sections if needed.

**Review individually**: For each proposal, show the diff and ask approve/skip/modify.

**Save for later**: Create a markdown file with all proposals for future review.

After applying changes, summarize what was updated:
```
Updated skills:
- refactor-specialist: Added edge case for monorepos
- audit: Clarified severity criteria
```
</step_7>
</process>

<transcript_parsing>
**Transcript format** (JSONL - one JSON object per line):

```json
{"type": "user", "content": "user message..."}
{"type": "assistant", "content": "assistant response..."}
{"type": "tool_use", "tool_name": "Read", "tool_input": {...}}
{"type": "tool_result", "tool_use_id": "...", "content": "..."}
```

**Finding skill activations**:
```python
# Pseudocode for transcript analysis
for line in transcript:
    obj = json.loads(line)
    if obj.get("tool_name") == "Skill":
        skill_name = obj["tool_input"]["skill"]
        activated_skills.add(skill_name)
    if obj.get("tool_name") == "Read":
        path = obj["tool_input"]["file_path"]
        if "SKILL.md" in path:
            activated_skills.add(extract_skill_name(path))
```

**Finding errors/corrections**:
- Look for tool_result with error indicators
- Look for user messages containing corrections ("no", "actually", "that's wrong", "try again")
- Look for repeated similar tool calls (indicates retry)
</transcript_parsing>

<learning_categories>
<mistakes>
Signs of mistakes in transcript:
- `"error"` or `"failed"` in tool results
- User messages with correction language
- Assistant messages with "I apologize" or "let me try again"
- Same tool called multiple times with different parameters
</mistakes>

<improvements>
Signs of improvement opportunities:
- Long sequences that could be shortened
- Missing validation that caused issues
- Assumptions stated that turned out wrong
- User providing context that should be in the skill
</improvements>

<successes>
Signs of success to reinforce:
- User confirmation ("perfect", "thanks", "that worked")
- Clean execution without retries
- Efficient tool sequences
</successes>
</learning_categories>

<update_guidelines>
When proposing skill updates:

**DO:**
- Be specific about what text to add/change
- Preserve existing structure and style
- Add to appropriate sections (don't create redundant sections)
- Include context for why the change helps

**DON'T:**
- Propose changes unrelated to session learnings
- Remove existing content without strong justification
- Add overly verbose explanations
- Duplicate information already in the skill
</update_guidelines>

<edge_cases>
**No skills activated**: Report "No skills were activated in this session" and exit.

**No learnings found**: Report "Session completed successfully with no notable learnings" and exit.

**Skill file not found**: Skip that skill with a warning, continue with others.

**Transcript not accessible**: Ask user to provide the transcript path manually.

**Conflicting learnings**: Present both and ask user to choose which applies.
</edge_cases>

<automatic_trigger>
When triggered by Stop hook:
1. Check `stop_hook_active` - if true, exit immediately (prevent loops)
2. Parse transcript for skill activations
3. Only proceed if skills were found AND learnings detected
4. Present findings with option to skip (respect user's time)

The hook should be non-intrusive - only interrupt when there's something meaningful to learn.
</automatic_trigger>

<success_criteria>
The skill completes successfully when:
- Transcript has been analyzed for skill activations
- Learnings have been identified (or confirmed none exist)
- User has been presented with findings
- Approved changes have been applied (or saved/skipped per user choice)
- Summary of actions has been provided
</success_criteria>
