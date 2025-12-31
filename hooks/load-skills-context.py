#!/usr/bin/env python3
"""
SessionStart hook that loads all available skills into context.

This runs once at session start and injects a manifest of all skills
so Claude always knows what skills are available.
"""

import json
import sys
import os
import re
from pathlib import Path


def find_plugin_root() -> Path:
    """Find the plugin root directory."""
    # Try environment variable first
    if os.environ.get("CLAUDE_PLUGIN_ROOT"):
        return Path(os.environ["CLAUDE_PLUGIN_ROOT"])

    # Fall back to script location
    script_dir = Path(__file__).parent
    return script_dir.parent


def parse_skill_frontmatter(content: str) -> dict:
    """Extract name and description from SKILL.md frontmatter."""
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        return {}

    frontmatter = frontmatter_match.group(1)
    result = {}

    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            result[key.strip()] = value.strip()

    return result


def load_all_skills(plugin_root: Path) -> list[dict]:
    """Load all skills from the skills directory."""
    skills = []
    skills_dir = plugin_root / "skills"

    if not skills_dir.exists():
        return skills

    for skill_dir in skills_dir.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        try:
            content = skill_file.read_text()
            frontmatter = parse_skill_frontmatter(content)

            # Extract keywords from description for matching
            description = frontmatter.get("description", "")
            name = frontmatter.get("name", skill_dir.name)

            skills.append({
                "name": name,
                "description": description,
                "path": str(skill_file.relative_to(plugin_root))
            })
        except Exception:
            continue

    return skills


def load_all_commands(plugin_root: Path) -> list[dict]:
    """Load all slash commands from the commands directory."""
    commands = []
    commands_dir = plugin_root / "commands"

    if not commands_dir.exists():
        return commands

    for cmd_file in commands_dir.glob("*.md"):
        try:
            content = cmd_file.read_text()
            frontmatter = parse_skill_frontmatter(content)

            name = frontmatter.get("name", cmd_file.stem)
            description = frontmatter.get("description", "")

            commands.append({
                "name": name,
                "description": description
            })
        except Exception:
            continue

    return commands


def main():
    # Read input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        input_data = {}

    plugin_root = find_plugin_root()

    # Load skills and commands
    skills = load_all_skills(plugin_root)
    commands = load_all_commands(plugin_root)

    if not skills and not commands:
        sys.exit(0)

    # Build context message
    context_parts = []

    if skills:
        context_parts.append("## Available Skills (auto-activate when relevant)\n")
        for skill in skills:
            context_parts.append(f"- **{skill['name']}**: {skill['description']}")
        context_parts.append("")

    if commands:
        context_parts.append("## Available Commands\n")
        for cmd in commands:
            context_parts.append(f"- `/{cmd['name']}`: {cmd['description']}")
        context_parts.append("")

    context_parts.append("When a user request matches a skill's purpose, proactively use that skill.")

    context = "\n".join(context_parts)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context
        }
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
