#!/usr/bin/env python3
"""
UserPromptSubmit hook that detects relevant skills and reminds Claude to use them.

This hook:
1. Scans all available skills
2. Extracts keywords from skill names and descriptions
3. Matches against the user's prompt
4. Injects a reminder about matching skills
"""

import json
import sys
import os
import re
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Set


def find_plugin_root() -> Path:
    """Find the plugin root directory."""
    if os.environ.get("CLAUDE_PLUGIN_ROOT"):
        return Path(os.environ["CLAUDE_PLUGIN_ROOT"])
    script_dir = Path(__file__).parent
    return script_dir.parent


def get_all_skill_directories(plugin_root: Path, project_dir: Optional[str]) -> List[Tuple[Path, str]]:
    """Get all directories that may contain skills."""
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
    """Get all directories that may contain commands."""
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


def extract_keywords(text: str) -> Set[str]:
    """Extract meaningful keywords from text."""
    # Lowercase and split on non-alphanumeric
    words = re.findall(r'[a-z]+', text.lower())

    # Filter out common stop words
    stop_words = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
        'ought', 'used', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by',
        'from', 'as', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'between', 'under', 'again', 'further', 'then', 'once', 'here',
        'there', 'when', 'where', 'why', 'how', 'all', 'each', 'few', 'more',
        'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
        'same', 'so', 'than', 'too', 'very', 'just', 'and', 'but', 'if', 'or',
        'because', 'until', 'while', 'this', 'that', 'these', 'those', 'what',
        'which', 'who', 'whom', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours',
        'you', 'your', 'yours', 'he', 'him', 'his', 'she', 'her', 'hers', 'it',
        'its', 'they', 'them', 'their', 'use', 'using', 'file', 'files', 'code',
        'please', 'want', 'help', 'make', 'like', 'get', 'also'
    }

    return {w for w in words if w not in stop_words and len(w) > 2}


def load_skills_with_keywords(plugin_root: Path, project_dir: Optional[str]) -> List[Dict]:
    """Load all skills with their keywords for matching."""
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

                name = frontmatter.get("name", skill_dir.name)
                description = frontmatter.get("description", "")

                # Skip duplicates
                if name in seen_names:
                    continue
                seen_names.add(name)

                # Build keyword set from name and description
                keywords = extract_keywords(name.replace("-", " "))
                keywords.update(extract_keywords(description))

                # Add some explicit trigger words based on common skill types
                name_lower = name.lower()
                if "refactor" in name_lower:
                    keywords.update(["refactor", "refactoring", "cleanup", "clean", "improve", "optimize"])
                if "audit" in name_lower:
                    keywords.update(["audit", "review", "check", "analyze", "analysis", "security"])
                if "commit" in name_lower:
                    keywords.update(["commit", "commits", "git", "message"])
                if "heal" in name_lower or "learn" in name_lower:
                    keywords.update(["learn", "learning", "improve", "heal", "fix", "update", "skill"])
                if "test" in name_lower:
                    keywords.update(["test", "testing", "tests", "spec", "specs", "unit", "integration"])

                skills.append({
                    "name": name,
                    "description": description,
                    "keywords": keywords,
                    "source": source
                })
            except Exception:
                continue

    return skills


def load_commands_with_keywords(plugin_root: Path, project_dir: Optional[str]) -> List[Dict]:
    """Load all commands with their keywords for matching."""
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

                keywords = extract_keywords(name.replace("-", " "))
                keywords.update(extract_keywords(description))

                commands.append({
                    "name": name,
                    "description": description,
                    "keywords": keywords,
                    "source": source
                })
            except Exception:
                continue

    return commands


def match_skills(prompt: str, skills: List[Dict], threshold: int = 1) -> List[Dict]:
    """Find skills that match the user prompt."""
    prompt_keywords = extract_keywords(prompt)
    matches = []

    for skill in skills:
        # Count keyword overlaps
        overlap = prompt_keywords & skill["keywords"]

        # Give extra weight if skill name keywords match (strong signal)
        name_keywords = extract_keywords(skill["name"].replace("-", " "))
        name_overlap = prompt_keywords & name_keywords
        score = len(overlap) + len(name_overlap)  # name matches count double

        if score >= threshold:
            matches.append({
                "name": skill["name"],
                "description": skill["description"],
                "matched_keywords": list(overlap | name_overlap),
                "score": score
            })

    # Sort by score descending
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:3]  # Return top 3 matches


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    prompt = input_data.get("prompt", "")
    if not prompt or len(prompt) < 10:
        sys.exit(0)

    plugin_root = find_plugin_root()
    project_dir = input_data.get("cwd")

    # Load skills and commands from all locations
    skills = load_skills_with_keywords(plugin_root, project_dir)
    commands = load_commands_with_keywords(plugin_root, project_dir)

    # Find matches
    skill_matches = match_skills(prompt, skills)
    command_matches = match_skills(prompt, commands, threshold=1)

    if not skill_matches and not command_matches:
        sys.exit(0)

    # Build reminder context
    context_parts = ["[Skill Activator] Relevant skills detected for this request:"]

    if skill_matches:
        for match in skill_matches:
            context_parts.append(
                f"- **{match['name']}**: {match['description']} "
                f"(matched: {', '.join(match['matched_keywords'][:5])})"
            )

    if command_matches:
        context_parts.append("\nRelevant commands:")
        for match in command_matches:
            context_parts.append(f"- `/{match['name']}`: {match['description']}")

    context_parts.append("\nConsider using these skills/commands if appropriate for this task.")

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": "\n".join(context_parts)
        }
    }

    print(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
