#!/bin/bash
# Claude Code status line: model [effort] · title (PR #n, an OSC 8 link) · repo · branch · Context n% left · weekly n% left
command -v jq >/dev/null || { echo "statusline: jq not installed (brew install jq)"; exit 0; }
input=$(cat)
j() { printf '%s' "$input" | jq -r "$1 // empty"; }

model=$(j .model.display_name)
effort=$(j .effort.level)
cwd=$(j .workspace.current_dir); [ -z "$cwd" ] && cwd=$(j .cwd)
ctx=$(j .context_window.remaining_percentage)
week_used=$(j .rate_limits.seven_day.used_percentage)
five_used=$(j .rate_limits.five_hour.used_percentage)
tp=$(j .transcript_path); title=$(j .session_name)
if [ -z "$title" ] && [ -f "$tp" ]; then
  # /rename title wins over the auto-generated one; last record is current.
  title=$(grep -F "\"type\":\"custom-title\"" "$tp" | tail -1 | jq -r ".customTitle // empty" 2>/dev/null)
  [ -z "$title" ] && title=$(grep -F "\"type\":\"ai-title\"" "$tp" | tail -1 | jq -r ".aiTitle // empty" 2>/dev/null)
fi
# Free text from the transcript: drop control characters so no stray escape sequence reaches the terminal.
title=$(printf '%s' "$title" | tr -d '\000-\037\177')

branch=""; repo=""; pr=""; pr_url=""
if [ -n "$cwd" ] && common=$(git -C "$cwd" --no-optional-locks rev-parse --path-format=absolute --git-common-dir 2>/dev/null); then
  branch=$(git -C "$cwd" --no-optional-locks branch --show-current 2>/dev/null)
  # Worktrees share the main repo's common dir, so this yields "tempo-ai" in any of them.
  if [ "$(basename "$common")" = ".git" ]; then repo=$(basename "$(dirname "$common")"); else repo=$(basename "$common" .git); fi

  if [ -n "$branch" ]; then
    cache_dir=$HOME/.claude/statusline-pr-cache
    cache="$cache_dir/$(printf '%s' "$common:$branch" | tr -c 'A-Za-z0-9' '_')"
    mkdir -p "$cache_dir"
    mtime=$(stat -f %m "$cache" 2>/dev/null || stat -c %Y "$cache" 2>/dev/null || echo 0)
    if [ $(( $(date +%s) - mtime )) -gt 300 ]; then
      # Open PRs only; 3s hard cap. Result (even empty) is cached so a failure doesn't retry every render.
      tmp=$(mktemp)
      ( cd "$cwd" && exec gh pr list --head "$branch" --state open --json url -q '.[0].url // empty' ) >"$tmp" 2>/dev/null &
      gpid=$!
      ( sleep 3; kill "$gpid" 2>/dev/null ) >/dev/null 2>&1 &
      wpid=$!
      wait "$gpid" 2>/dev/null
      kill "$wpid" 2>/dev/null; wait "$wpid" 2>/dev/null
      mv "$tmp" "$cache"
    fi
    pr_url=$(tr -d '[:space:]' <"$cache" 2>/dev/null)
  fi
  # No PR on this branch (e.g. the main checkout while the work lives in worktrees):
  # fall back to the last PR of this repo that the session created or opened.
  if [ -z "$pr_url" ] && [ -f "$tp" ] && slug=$(git -C "$cwd" --no-optional-locks remote get-url origin 2>/dev/null | sed -E 's#.*github\.com[:/]##; s#\.git$##'); then
    pr_url=$(grep -oE "https://github\.com/$slug/pull/[0-9]+" "$tp" 2>/dev/null | tail -1)
  fi
  pr=${pr_url##*/}
fi

# Codex-style: each segment one fixed pastel color (24-bit RGB "r;g;b"), dim separators.
c() { printf '\033[38;2;%sm%s\033[0m' "$1" "$2"; }
TITLE='137;221;255'; MODEL='236;196;141'; PR='199;146;234'; REPO='195;232;141'
BRANCH='130;170;255'; CTX='247;140;108'; FIVE='255;203;107'; WEEK='240;113;160'; SEP='110;118;135'

out=()
[ -n "$model" ] && out+=("$(c "$MODEL" "$model${effort:+ $(printf "%s" "${effort:0:1}" | tr a-z A-Z)${effort:1}}")")
# The PR number is an OSC 8 hyperlink (Cmd+click); terminals without support show plain text.
link() { printf '\033]8;;%s\a%s\033]8;;\a' "$1" "$2"; }
t="$title"; [ -n "$pr" ] && t="${t:+$t }($(link "$pr_url" "PR #$pr"))"
[ -n "$t" ] && out+=("$(c "$TITLE" "$t")")
[ -n "$repo" ] && out+=("$(c "$REPO" "$repo")")
[ -n "$branch" ] && out+=("$(c "$BRANCH" "$branch")")
[ -n "$ctx" ] && out+=("$(c "$CTX" "$(printf 'Context %.0f%% left' "$ctx")")")
[ -n "$five_used" ] && out+=("$(c "$FIVE" "$(printf '5h %.0f%% left' "$(echo "100 - $five_used" | bc)")")")
[ -n "$week_used" ] && out+=("$(c "$WEEK" "$(printf 'Weekly %.0f%% left' "$(echo "100 - $week_used" | bc)")")")

sep=""; line=""
for s in "${out[@]}"; do line+="$sep$s"; sep=" $(c "$SEP" '·') "; done
printf '%s\n' "$line"
