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
per-harness config. After `brew install herdr`, run its integration
installer for each harness in use:

```sh
herdr integration install claude
herdr integration install codex
herdr integration install pi
```

Each reports session state back to herdr over a local socket
(`HERDR_SOCKET_PATH`, `HERDR_PANE_ID`), but the mechanism differs slightly
per harness:

- **Claude Code**: installs a `SessionStart` hook script to
  `~/.claude/hooks/herdr-agent-state.sh` and wires it into
  `~/.claude/settings.json` → see
  [`../claude-code/README.md`](../claude-code/README.md#hooks)
- **Codex CLI**: installs `~/.codex/herdr-agent-state.sh` and wires it via
  `~/.codex/hooks.json`, also touching `~/.codex/config.toml`
- **Pi**: installs a TypeScript extension to
  `~/.pi/agent/extensions/herdr-agent-state.ts` (not a hooks.json — Pi's
  extension mechanism is different from the other two)
- **Cursor**: `~/.cursor/hooks.json` (Cursor itself isn't otherwise
  documented here yet — see TODO)

None of the installed integration files are vendored in this repo since
`herdr integration install` overwrites them on reinstall/update.

## TODO

- [ ] Document Codex CLI / Pi config once customized (currently defaults)
- [ ] Document Cursor setup (present on this machine, not yet written up)
- [ ] Document shared MCP servers, if any
