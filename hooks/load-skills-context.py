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
from typing import Optional, List, Tuple, Dict


def find_plugin_root() -> Path:
    """Find the plugin root directory."""
    # Try environment variable first
    if os.environ.get("CLAUDE_PLUGIN_ROOT"):
        return Path(os.environ["CLAUDE_PLUGIN_ROOT"])

    # Fall back to script location
    script_dir = Path(__file__).parent
    return script_dir.parent


def get_all_skill_directories(plugin_root: Path, project_dir: Optional[str]) -> List[Tuple[Path, str]]:
    """Get all directories that may contain skills.

    Returns list of (path, source_label) tuples.
    """
    dirs = []

    # 1. Global user skills: ~/.claude/skills
    global_skills = Path.home() / ".claude" / "skills"
    if global_skills.exists():
        dirs.append((global_skills, "global"))

    # 2. Project-specific skills: ${PROJECT_PATH}/.claude/skills
    if project_dir:
        project_skills = Path(project_dir) / ".claude" / "skills"
        if project_skills.exists():
            dirs.append((project_skills, "project"))

    # 3. Plugin's own skills
    plugin_skills = plugin_root / "skills"
    if plugin_skills.exists():
        dirs.append((plugin_skills, "plugin"))

    return dirs


def get_all_command_directories(plugin_root: Path, project_dir: Optional[str]) -> List[Tuple[Path, str]]:
    """Get all directories that may contain commands.

    Returns list of (path, source_label) tuples.
    """
    dirs = []

    # 1. Global user commands: ~/.claude/commands
    global_cmds = Path.home() / ".claude" / "commands"
    if global_cmds.exists():
        dirs.append((global_cmds, "global"))

    # 2. Project-specific commands: ${PROJECT_PATH}/.claude/commands
    if project_dir:
        project_cmds = Path(project_dir) / ".claude" / "commands"
        if project_cmds.exists():
            dirs.append((project_cmds, "project"))

    # 3. Plugin's own commands
    plugin_cmds = plugin_root / "commands"
    if plugin_cmds.exists():
        dirs.append((plugin_cmds, "plugin"))

    return dirs


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


def load_all_skills(plugin_root: Path, project_dir: Optional[str]) -> List[Dict]:
    """Load all skills from all skill directories."""
    skills = []
    seen_names = set()

    for skills_dir, source in get_all_skill_directories(plugin_root, project_dir):
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

                # Skip duplicates (first one wins - global > project > plugin)
                if name in seen_names:
                    continue
                seen_names.add(name)

                skills.append({
                    "name": name,
                    "description": description,
                    "source": source,
                    "path": str(skill_file)
                })
            except Exception:
                continue

    return skills


def load_all_commands(plugin_root: Path, project_dir: Optional[str]) -> List[Dict]:
    """Load all slash commands from all command directories."""
    commands = []
    seen_names = set()

    for commands_dir, source in get_all_command_directories(plugin_root, project_dir):
        for cmd_file in commands_dir.glob("*.md"):
            try:
                content = cmd_file.read_text()
                frontmatter = parse_skill_frontmatter(content)

                name = frontmatter.get("name", cmd_file.stem)
                description = frontmatter.get("description", "")

                # Skip duplicates
                if name in seen_names:
                    continue
                seen_names.add(name)

                commands.append({
                    "name": name,
                    "description": description,
                    "source": source
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
    project_dir = input_data.get("cwd")

    # Load skills and commands from all locations
    skills = load_all_skills(plugin_root, project_dir)
    commands = load_all_commands(plugin_root, project_dir)

    if not skills and not commands:
        sys.exit(0)

    # Build context message
    context_parts = []

    if skills:
        context_parts.append("## Available Skills (auto-activate when relevant)\n")
        for skill in skills:
            source_tag = f" [{skill['source']}]" if skill.get('source') else ""
            context_parts.append(f"- **{skill['name']}**{source_tag}: {skill['description']}")
        context_parts.append("")

    if commands:
        context_parts.append("## Available Commands\n")
        for cmd in commands:
            source_tag = f" [{cmd['source']}]" if cmd.get('source') else ""
            context_parts.append(f"- `/{cmd['name']}`{source_tag}: {cmd['description']}")
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
