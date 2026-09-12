# Other AI Tools

Setup notes for AI/agent tools other than Claude Code itself, and any
shared integrations.

## Agent harnesses

Alongside Claude Code, these are the other agent harnesses in
rotation — CLI/TUI programs that wrap an LLM with a tool-use loop
(read/write/edit files, run shell commands):

### Codex CLI (OpenAI)

```sh
brew install --cask codex
codex auth
```

### Pi (Earendil Works)

Provider-agnostic — works with Anthropic, OpenAI, Gemini, and others. No
brew cask available; install via npm:

```sh
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

## Herdr

https://herdr.dev/ — agent runtime / terminal-session manager.

```sh
brew install herdr
```

Installed after the terminal + shell setup, before diving into
per-harness config. Herdr installs its own integration hook into every
agent harness it finds — same pattern each time: a `SessionStart` hook
(`herdr-agent-state.sh`) that reports session state back to herdr over a
local socket (`HERDR_SOCKET_PATH`, `HERDR_PANE_ID`):

- Claude Code: `~/.claude/settings.json` → see
  [`../claude-code/README.md`](../claude-code/README.md#hooks)
- Codex CLI: `~/.codex/hooks.json`
- Cursor: `~/.cursor/hooks.json` (Cursor itself isn't otherwise documented
  here yet — see TODO)

None of the `herdr-agent-state.sh` scripts are vendored in this repo since
herdr overwrites them on reinstall/update.

## TODO

- [ ] Document Codex CLI / Pi config once customized (currently defaults)
- [ ] Document Cursor setup (present on this machine, not yet written up)
- [ ] Document shared MCP servers, if any
