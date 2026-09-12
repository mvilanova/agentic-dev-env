# Other AI Tools

Setup notes for AI/agent tools other than Claude Code itself, and any
shared integrations.

## Agent harnesses

Alongside Claude Code, these are the other agent harnesses in
rotation — CLI/TUI programs that wrap an LLM with a tool-use loop
(read/write/edit files, run shell commands):

### Codex CLI (OpenAI)

```sh
npm install -g @openai/codex
codex auth
```

### Pi (Earendil Works)

Provider-agnostic — works with Anthropic, OpenAI, Gemini, and others.

```sh
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

## Herdr

https://herdr.dev/ — agent runtime / terminal-session manager. Installed
after the terminal + shell setup, before diving into Claude Code config.

Herdr installs its own Claude Code integration automatically: a
`SessionStart` hook (`herdr-agent-state.sh`) in `~/.claude/settings.json`
that reports session state back to herdr over a local socket
(`HERDR_SOCKET_PATH`, `HERDR_PANE_ID`). See
[`../claude-code/README.md`](../claude-code/README.md#hooks) — that hook
isn't vendored here since herdr overwrites it on reinstall/update.

## TODO

- [ ] Document Codex CLI / Pi config once customized (currently defaults)
- [ ] Document shared MCP servers, if any
