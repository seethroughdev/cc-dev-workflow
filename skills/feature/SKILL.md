---
allowed-tools: Read, Grep, Glob, Task, AskUserQuestion, Write, Edit
description: |
  Structured feature planning workflow with intake, interview, and detailed plan output.
  Use when: user wants to plan a feature, design a feature, spec out functionality,
  think through requirements, or says "let's plan", "help me design", "I want to build".
  NOT for implementation - this is planning only.
argument-hint: <brief feature description>
---

# Feature Planning Mode

Feature: **$ARGUMENTS**

## Phase 1: Intake

Collect everything the user knows before asking questions.

**Critical behavior:**
- Respond ONLY with "Got it. What else?" after each input
- NO questions, suggestions, or commentary during intake
- Continue until user signals done ("done", "that's it", "finished", etc.)

Silently categorize into: Requirements, Constraints, Context, Edge Cases, Open Questions.

## Phase 2: Skill Activation

Identify and activate relevant skills based on intake (api, cli, ios, search, testing, deployment, frontend-design, etc.). Note which are relevant and why.

## Phase 3: Adaptive Interview

Use AskUserQuestion to fill gaps NOT covered during intake. Skip anything already answered.

**Topics (if unknown):**
1. Success Criteria - How do we know it's working?
2. User Personas - Who uses this? Different user types?
3. Constraints - Tech limitations? Dependencies?
4. Risks - What could go wrong?
5. MVP vs Full Vision - Minimum viable vs dream version?
6. Priority - Relative to other work?

**Style:**
- 1-3 questions at a time
- Mark recommended option in choices
- Stop when you have enough for a solid plan

## Phase 4: Plan Output

Read [references/plan-template.md](references/plan-template.md) and write the plan document.

Save to `.planning/NNN-feature-name-PLAN.md` (check existing files for next number).

---

**Begin:** Acknowledge the feature, then say:

"Ready for intake. Tell me everything you know about this feature. I'll respond with 'Got it. What else?' until you're done."
