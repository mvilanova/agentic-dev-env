# Claude Code

Global config lives at `~/.claude/settings.json`. This folder tracks a
redacted copy plus notes.

## Setup

1. Install Claude Code via the native installer, **not** the brew cask
   (see [`../../BOOTSTRAP.md`](../../BOOTSTRAP.md) step 7 for why — brew's
   `claude-code` cask lags behind):
   ```sh
   curl -fsSL https://claude.ai/install.sh | bash
   ```
2. Copy `settings.example.json` to `~/.claude/settings.json`, replacing
   placeholder paths (e.g. `<path-to-hooks>`) with real ones.
3. Restart Claude Code to pick up settings changes.

## Notable config

- **Models**: default model is Sonnet; `modelSettings` pins effort levels
  per model (`fable-5-1` medium, `opus-5` high).
- **Subagents**: `env.CLAUDE_CODE_SUBAGENT_MODEL=opus` forces subagents to
  use Opus regardless of the main model.
- **Hooks**: `hooks/` (see below) contains scripts referenced from
  `settings.json`.
- **UI**: `tui: fullscreen` uses the flicker-free renderer;
  `autoCompactWindow` is raised above default.
- **Status line**: `statusLine` runs `statusline.sh` (see below).

## Hooks

- `SessionStart` runs `herdr-agent-state.sh`, which is installed and managed
  by "herdr" (a terminal/agent-session manager) — not vendored here since
  herdr overwrites it on reinstall/update. Install herdr and its Claude Code
  integration to reproduce this hook.

## Status line

`statusline.sh` renders the bottom status line, Codex-style (one pastel
color per segment, dim `·` separators):

```
Fable 5.1 Medium · Fix drag preview (PR #3236) · tempo-ai · fix/event-drag-preview · Context 71% left · 5h 82% left · Weekly 64% left
```

- **Model + effort** from the JSON Claude Code pipes to the script.
- **Session title**: the `/rename` title if set, otherwise the auto-generated
  one, read from the transcript.
- **PR**: the open PR for the current branch via `gh pr list`, cached for
  5 minutes per branch under `~/.claude/statusline-pr-cache/` with a 3 s
  cap so a slow GitHub never stalls rendering. If the branch has no PR
  (e.g. the main checkout while work happens in worktrees), it falls back
  to the last PR URL of this repo mentioned in the transcript. The number
  is an OSC 8 hyperlink — Cmd+click opens it in terminals that support it.
- **Repo + branch**: worktrees resolve to the main repo's name.
- **Context / 5h / Weekly** remaining. The two usage segments only appear
  on Claude.ai subscriptions, after the first response.

Setup:

1. `cp statusline.sh ~/.claude/statusline.sh`
2. Keep the `statusLine` block from `settings.example.json` in
   `~/.claude/settings.json`.
3. `brew install jq` — required; the script prints a hint and exits
   without it. `gh` must be logged in for the PR segment (it is simply
   empty otherwise). `bc` ships with macOS and most Linux distros.
4. Restart Claude Code.

## TODO

- Document custom skills/commands if added
- Document MCP servers in use (e.g. Tempo)
