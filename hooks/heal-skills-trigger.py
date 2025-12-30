#!/usr/bin/env python3
"""
Stop hook for heal-skills self-learning system.

This hook analyzes the session transcript to determine if:
1. Any skills were activated during the session
2. There are potential learnings (errors, corrections, retries)

If both conditions are met, it blocks the stop and prompts Claude
to run the heal-skills skill for reflection.
"""

import json
import sys
import os
import re
from pathlib import Path


def parse_transcript(transcript_path: str) -> list[dict]:
    """Parse JSONL transcript file into list of events."""
    events = []
    try:
        with open(transcript_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except (FileNotFoundError, PermissionError):
        return []
    return events


def find_activated_skills(events: list[dict]) -> set[str]:
    """Find skills that were activated during the session."""
    skills = set()

    for event in events:
        # Check for Skill tool invocations
        if event.get("type") == "tool_use" and event.get("tool_name") == "Skill":
            tool_input = event.get("tool_input", {})
            if isinstance(tool_input, dict):
                skill_name = tool_input.get("skill", "")
                if skill_name:
                    skills.add(skill_name)

        # Check for SKILL.md file reads
        if event.get("type") == "tool_use" and event.get("tool_name") == "Read":
            tool_input = event.get("tool_input", {})
            if isinstance(tool_input, dict):
                file_path = tool_input.get("file_path", "")
                if "SKILL.md" in file_path:
                    # Extract skill name from path like skills/foo/SKILL.md
                    match = re.search(r'skills/([^/]+)/SKILL\.md', file_path)
                    if match:
                        skills.add(match.group(1))

    # Don't trigger self-reflection for heal-skills itself
    skills.discard("heal-skills")

    return skills


def detect_learnings(events: list[dict]) -> dict:
    """Detect potential learning opportunities in the session."""
    learnings = {
        "errors": [],
        "corrections": [],
        "retries": [],
        "has_learnings": False
    }

    # Track tool calls for retry detection
    tool_call_counts = {}

    # Correction indicators in user messages
    correction_patterns = [
        r'\bno[,.]?\s',
        r'\bactually\b',
        r'\bthat\'s wrong\b',
        r'\bthat\'s not right\b',
        r'\btry again\b',
        r'\bwrong\b',
        r'\bincorrect\b',
        r'\bnot what i\b',
        r'\bshould be\b',
        r'\binstead\b',
        r'\bfix\b',
    ]

    for event in events:
        # Check for errors in tool results
        if event.get("type") == "tool_result":
            content = str(event.get("content", ""))
            if any(err in content.lower() for err in ["error", "failed", "exception", "traceback"]):
                learnings["errors"].append(content[:200])

        # Check for user corrections
        if event.get("type") == "user":
            content = str(event.get("content", "")).lower()
            for pattern in correction_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    learnings["corrections"].append(content[:200])
                    break

        # Track potential retries (same tool called multiple times with different params)
        if event.get("type") == "tool_use":
            tool_name = event.get("tool_name", "")
            tool_input = str(event.get("tool_input", {}))
            key = f"{tool_name}"
            tool_call_counts[key] = tool_call_counts.get(key, 0) + 1

    # Flag high retry counts as potential learnings
    for tool, count in tool_call_counts.items():
        if count > 3:  # More than 3 calls to same tool type
            learnings["retries"].append(f"{tool}: {count} calls")

    # Determine if we have meaningful learnings
    learnings["has_learnings"] = bool(
        learnings["errors"] or
        learnings["corrections"] or
        learnings["retries"]
    )

    return learnings


def main():
    # Read input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # Allow stop on parse error

    # CRITICAL: Prevent infinite loops
    if input_data.get("stop_hook_active"):
        sys.exit(0)  # Allow stop

    transcript_path = input_data.get("transcript_path", "")
    if not transcript_path or not os.path.exists(transcript_path):
        sys.exit(0)  # Allow stop if no transcript

    # Parse transcript
    events = parse_transcript(transcript_path)
    if not events:
        sys.exit(0)  # Allow stop if empty

    # Find activated skills
    skills = find_activated_skills(events)
    if not skills:
        sys.exit(0)  # Allow stop if no skills used

    # Detect learnings
    learnings = detect_learnings(events)
    if not learnings["has_learnings"]:
        sys.exit(0)  # Allow stop if no learnings

    # We have skills AND learnings - suggest reflection
    skills_list = ", ".join(sorted(skills))

    learning_summary = []
    if learnings["errors"]:
        learning_summary.append(f"{len(learnings['errors'])} error(s)")
    if learnings["corrections"]:
        learning_summary.append(f"{len(learnings['corrections'])} correction(s)")
    if learnings["retries"]:
        learning_summary.append(f"{len(learnings['retries'])} retry pattern(s)")

    summary = ", ".join(learning_summary)

    output = {
        "decision": "block",
        "reason": f"""Skills used this session: {skills_list}
Potential learnings detected: {summary}

Consider running /heal-skills to capture these learnings and improve the skills for next time.

To skip, just say "skip" or "no thanks"."""
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
