# Other AI Tools

Setup notes for AI/agent tools other than Claude Code itself, and any
shared integrations.

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

- [ ] List other tools in use (Cursor, Copilot, etc.) and link to their config
- [ ] Document shared MCP servers, if any
