#!/bin/bash
input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd')
usage=$(echo "$input" | jq '.context_window.current_usage')

# Context percentage with color coding
if [ "$usage" != "null" ]; then
    current=$(echo "$usage" | jq '.input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens')
    size=$(echo "$input" | jq '.context_window.context_window_size')
    pct=$((current * 100 / size))
    if [ $pct -lt 40 ]; then
        context_pct="$pct%"
    elif [ $pct -le 80 ]; then
        context_pct=$(printf '\033[33m%d%%\033[0m' "$pct")
    else
        context_pct=$(printf '\033[31m%d%%\033[0m' "$pct")
    fi
else
    context_pct="0%"
fi

# Git branch
git_branch=""
git_diff=""
if git -C "$cwd" rev-parse --git-dir > /dev/null 2>&1; then
    branch=$(git -C "$cwd" --no-optional-locks rev-parse --abbrev-ref HEAD 2>/dev/null)
    [ -n "$branch" ] && git_branch="⎇ $branch"

    # Lines added/removed
    diff_stats=$(git -C "$cwd" --no-optional-locks diff --numstat 2>/dev/null | awk '{added+=$1; removed+=$2} END {print added" "removed}')
    added=$(echo "$diff_stats" | cut -d' ' -f1)
    removed=$(echo "$diff_stats" | cut -d' ' -f2)
    added=${added:-0}
    removed=${removed:-0}
    [ "$added" != "0" ] || [ "$removed" != "0" ] && git_diff="+$added/-$removed"
fi

# Build output
output="$(basename "$cwd") | ctx:$context_pct"
[ -n "$git_branch" ] && output+=" | $git_branch"
[ -n "$git_diff" ] && output+=" | $git_diff"
echo "$output"
