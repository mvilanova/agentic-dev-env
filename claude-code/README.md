# Claude Code

Global config lives at `~/.claude/settings.json`. This folder tracks a
redacted copy plus notes.

## Setup

1. Install Claude Code: https://claude.com/claude-code
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

## Hooks

- `SessionStart` runs `herdr-agent-state.sh`, which is installed and managed
  by "herdr" (a terminal/agent-session manager) — not vendored here since
  herdr overwrites it on reinstall/update. Install herdr and its Claude Code
  integration to reproduce this hook.

## TODO

- Document custom skills/commands if added
- Document MCP servers in use (e.g. Tempo)
