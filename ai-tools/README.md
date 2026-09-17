# AI Tools

Setup notes for the AI coding tools in use and their shared integrations.

## Agent harnesses

The agent harnesses in rotation — CLI/TUI programs that wrap an LLM with
a tool-use loop (read/write/edit files, run shell commands). None is the
centerpiece; they're interchangeable peers:

### Claude Code (Anthropic)

Native installer, not the brew cask (see
[`../BOOTSTRAP.md`](../BOOTSTRAP.md) step 7 for why):

```sh
curl -fsSL https://claude.ai/install.sh | bash
```

Settings file and notes: [`claude-code/`](claude-code/).

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
  [`claude-code/README.md`](claude-code/README.md#hooks)
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

### reviewr plugin

https://github.com/persiyanov/herdr-reviewr — a code-review pane beside
the agent: read its diff (uncommitted / branch / last turn / commits),
comment on lines, and send the comments back to the agent's input. Never
edits the worktree. Requires herdr ≥ 0.7.5.

```sh
herdr plugin install persiyanov/herdr-reviewr
```

To update, reinstall (config is keyed by plugin id and survives):

```sh
herdr plugin uninstall persiyanov.reviewr && herdr plugin install persiyanov/herdr-reviewr
```

It auto-opens when herdr creates a workspace for a git worktree. To
toggle it with `cmd+r`, add this to `~/.config/herdr/config.toml` (then
`herdr server reload-config` if herdr is already running):

```toml
[[keys.command]]
key = "cmd+r"
type = "plugin_action"
command = "persiyanov.reviewr.toggle"
```

Or without a keybinding:
`herdr plugin action invoke toggle --plugin persiyanov.reviewr`.

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

### herdr plugin

https://github.com/edmundmiller/herdr-plugin-hunk — opens a hunk diff in
a herdr split pane or tab, so a diff can be pulled up next to the agent
without leaving herdr. Needs herdr ≥ 0.7.0, `python3`, and `hunk` on
`PATH`.

```sh
herdr plugin install edmundmiller/herdr-plugin-hunk
```

Actions are `hunk.diff.<scope>-<split|tab>`, with `<scope>` one of
`worktree`, `staged`, `branch`. Keybinding in
`~/.config/herdr/config.toml` (then `herdr server reload-config` if herdr
is already running):

```toml
[[keys.command]]
key = "prefix+shift+h"
type = "plugin_action"
command = "hunk.diff.worktree-split"
```

`HUNK_THEME` (e.g. `catppuccin-mocha`) overrides the theme the plugin
passes to hunk.

Overlaps with herdr's [reviewr plugin](#reviewr-plugin) — reviewr is a
persistent review pane with line comments that go back to the agent,
this is a quick one-off diff view.

## TODO

- [ ] Document Codex CLI / Pi config once customized (currently defaults)
- [ ] Document Cursor setup (present on this machine, not yet written up)
- [ ] Document shared MCP servers, if any
- [ ] Decide whether to actually configure hunk as git pager/difftool, or
      leave it available but unconfigured
