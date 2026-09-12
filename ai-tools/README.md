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

### Agent skill

https://herdr.dev/docs/agent-skill/ — a reusable skill (herdr-awareness:
querying/controlling other panes, session state, etc.) that any agent
supporting the skill system can load, on top of the `SessionStart`
integration above.

```sh
npx skills add herdrdev/herdr --skill herdr -g
```

- `-g` installs it globally (available to every project); drop it for a
  project-local install instead.
- Requires herdr already installed and the agent running inside a
  herdr-managed pane (`HERDR_ENV=1` set) to actually do anything at
  runtime.

Confirmed on this machine: the global install writes the actual skill
once to `~/.agents/skills/herdr` and symlinks it into each detected
harness's own skills dir — `~/.claude/skills/herdr`,
`~/.pi/agent/skills/herdr`, `~/.openclaw/skills/herdr`. It did **not**
symlink into `~/.codex/skills/`, even though Codex CLI is installed —
Codex's skill discovery apparently isn't picked up by this installer, so
Codex only has the `SessionStart` hook integration above, not the skill.

- Fallback if `npx skills` doesn't fit your setup: copy the skill file
  from the `herdrdev/herdr` GitHub repo directly into the agent's own
  instructions/skills mechanism.

## Hunk

https://www.hunk.dev/ — review-first terminal diff viewer for
agent-authored changesets. Works as a pager, difftool, or standalone
reviewer with Git, Jujutsu, and Sapling; renders agent-left annotations
(summary/rationale) inline above the hunk they refer to, and supports
custom TypeScript extensions.

```sh
brew install hunk
```

Other install methods (no brew, or want the latest before it's bottled):

```sh
curl -fsSL https://hunk.dev/install.sh | sh   # curl
npm i -g hunkdiff                              # npm
mise use -g hunk                               # mise
nix run github:modem-dev/hunk                  # Nix
```

Option, not yet decided: configure hunk as the git pager and difftool
(`git config --global core.pager hunk` / `git config --global diff.tool
hunk`), instead of just having it available to invoke manually.

## TODO

- [ ] Document Codex CLI / Pi config once customized (currently defaults)
- [ ] Document Cursor setup (present on this machine, not yet written up)
- [ ] Document shared MCP servers, if any
- [ ] Decide whether to actually configure hunk as git pager/difftool, or
      leave it available but unconfigured
