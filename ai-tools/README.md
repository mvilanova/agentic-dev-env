# AI Tools

Setup notes for the AI coding tools in use and their shared integrations.

## Agent harnesses

The agent harnesses in rotation — CLI/TUI programs that wrap an LLM with
a tool-use loop (read/write/edit files, run shell commands). None is the
centerpiece; they're interchangeable peers:

### ripgrep (shared prerequisite)

All three harnesses search files with `rg` when it's on PATH and fall
back to `find`/`grep` when it isn't. The fallback works but is slower
and less accurate (no `.gitignore` awareness), so install ripgrep before
the harnesses:

```sh
brew install ripgrep
```

Claude Code bundles its own `rg` and shims it into the shells it spawns,
so it works without this step — Codex CLI and Pi do not, and this
machine had no real `rg` binary until it was installed via brew.

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

### Shared PR completion instructions

Add the rule in [`PR-INSTRUCTIONS.md`](PR-INSTRUCTIONS.md) to both harnesses'
global instruction files: `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md`.
Preserve any existing instructions. This makes monitoring the latest commit's
CI checks and fixing failures caused by the change part of PR completion.
Start a new conversation after updating the files.

### Pi (Earendil Works)

Provider-agnostic — works with Anthropic, OpenAI, Gemini, and others. No
brew cask available; install via npm:

```sh
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

## Ponytail

[Ponytail](https://github.com/DietrichGebert/ponytail#install) — shared
coding guidance that favors existing code, standard libraries, and the
smallest working solution.

Install after the agent harnesses. Claude Code and Codex use Node.js
lifecycle hooks: `node` must be on the non-interactive shell's `PATH`.
If using nvm, complete [`../shell/README.md`](../shell/README.md#setup)
step 4 to install and select Node.js LTS, and pass both version checks
before running the plugin commands below. Installing nvm alone does not
install Node.js. Without Node, the skills still work but automatic
activation does not.

### Claude Code

Send these as **two separate prompts** inside Claude Code:

```text
/plugin marketplace add DietrichGebert/ponytail
```

```text
/plugin install ponytail@ponytail
```

The same commands work in the Claude Code desktop app's Code tab.

### Codex

Run in the terminal:

```sh
codex plugin marketplace add DietrichGebert/ponytail
codex plugin add ponytail@ponytail
```

Then run `codex`, open `/hooks`, review and trust Ponytail's two lifecycle
hooks, and start a new thread. Restart the Codex desktop app to pick up
the same installation.

### Pi

```sh
pi install git:github.com/DietrichGebert/ponytail
```

### Usage

The default mode is `full`. Use `/ponytail lite`, `/ponytail full`, or
`/ponytail ultra` to change intensity; say `stop ponytail` or `normal mode`
to turn it off for the conversation. See the
[upstream commands](https://github.com/DietrichGebert/ponytail#commands)
for review, audit, and other skills.

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

### Herdr workflows

#### Review before committing

For this workflow without permission prompts, start the primary agent inside
Herdr with the appropriate command:

```sh
codex --dangerously-bypass-approvals-and-sandbox
# Or:
claude --dangerously-skip-permissions
```

These flags disable permission safeguards for the entire primary and reviewer
sessions. The shortcut cannot change permissions in an already-running primary;
start a new session with the flag. The reviewer's "do not edit files" requirement
is an instruction, not an enforced restriction.

Ask the primary agent:

> Use Herdr to start a reviewer in a sibling pane without changing focus.
> If you are Codex, start Claude with Opus 5.5 at high effort
> (`--kind claude -- --model claude-opus-5-5 --effort high --dangerously-skip-permissions`); if you are Claude,
> start Codex with Sol 6.1 at high effort
> (`--kind codex -- -m gpt-6.1-sol -c model_reasoning_effort=high --dangerously-bypass-approvals-and-sandbox`).
> Review this task's diff for correctness, regressions, and missed callers.
> Do not edit files. Collect its findings, resolve confirmed issues, run the
> appropriate checks, and report the result.

To submit this request with `prefix+shift+r`, add the following to
`~/.config/herdr/config.toml`, then choose **reload config** in Herdr's
global menu. Focus the primary agent before pressing the shortcut.

```toml
[[keys.command]]
key = "prefix+shift+r"
type = "shell"
description = "ask agent to coordinate a review"
command = """
"$HERDR_BIN_PATH" agent prompt "$HERDR_ACTIVE_PANE_ID" \
"Use Herdr to start a reviewer in a sibling pane without changing focus. If you are Codex, start Claude with Opus 5.5 at high effort (--kind claude -- --model claude-opus-5-5 --effort high --dangerously-skip-permissions); if you are Claude, start Codex with Sol 6.1 at high effort (--kind codex -- -m gpt-6.1-sol -c model_reasoning_effort=high --dangerously-bypass-approvals-and-sandbox). Review this task's diff for correctness, regressions, and missed callers. Do not edit files. Collect its findings, resolve confirmed issues, run the appropriate checks, and report the result."
"""
```

The underlying sequence requires `jq` and the selected review CLI:

```sh
# Run from inside a Herdr pane.
test "${HERDR_ENV:-}" = 1 || exit 1

created=$(herdr pane split --current --direction right --cwd "$PWD" --no-focus) || exit
pane_id=$(printf '%s\n' "$created" | jq -er '.result.pane.pane_id') || exit

# Codex primary: start a Claude reviewer.
herdr agent start reviewer --kind claude --pane "$pane_id" -- --model claude-opus-5-5 --effort high --dangerously-skip-permissions || exit
# For a Claude primary, replace the preceding command with:
# herdr agent start reviewer --kind codex --pane "$pane_id" -- -m gpt-6.1-sol -c model_reasoning_effort=high --dangerously-bypass-approvals-and-sandbox || exit
herdr agent prompt reviewer \
  "Review the current diff for correctness and regressions. Trace affected callers. Do not edit files. Report actionable findings with file locations." \
  --wait --timeout 120000 || exit
herdr agent read reviewer --source recent-unwrapped --lines 160
```

This follows Herdr's [helper-agent recipe](https://herdr.dev/docs/agent-automation/#recipes).
In repeated automation, use unique names so an existing `reviewer` doesn't
collide. If the wait times out, inspect the reviewer before retrying; the
prompt may already have been delivered.

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

### herdr plugin: automatic review and feedback (current)

[herdr-hunk-diff](https://github.com/jhochenbaum/herdr-hunk-diff) opens a
Hunk review when an agent becomes idle, keeps it fresh with watch mode,
and submits inline comments back to that agent. Requires Herdr ≥ 0.8.0
and Node ≥ 22.12.

The upstream plugin defaults to a right-hand split. Our
[`hunk-horizontal.patch`](hunk-horizontal.patch) changes its shared opener
to split **down**, in the agent's existing tab, without stealing focus.
The patch includes a regression check. Use a linked local checkout so an
upstream reinstall does not overwrite it.

From this repository's root:

```sh
git clone https://github.com/jhochenbaum/herdr-hunk-diff.git ai-tools/.local/herdr-hunk-diff
git -C ai-tools/.local/herdr-hunk-diff checkout 47146a058858b4a7a116992aaae643436d80e7ab
git -C ai-tools/.local/herdr-hunk-diff apply "$PWD/ai-tools/hunk-horizontal.patch"
npm --prefix ai-tools/.local/herdr-hunk-diff ci --ignore-scripts
npm --prefix ai-tools/.local/herdr-hunk-diff run build
npm --prefix ai-tools/.local/herdr-hunk-diff prune --omit=dev --ignore-scripts
herdr plugin link "$PWD/ai-tools/.local/herdr-hunk-diff" --disabled
```

Create `config.toml` in the directory returned by
`herdr plugin config-dir jhochenbaum.hunkdiff`:

```toml
[review]
auto_open = true
on_states = ["idle"]
reuse_pane = true
default_target = "auto"
watch = true
placement = "split"

[roundtrip]
clear_after_send = true
```

Replace the existing review shortcut in `~/.config/herdr/config.toml`
and add the send shortcut:

```toml
[[keys.command]]
key = "prefix+shift+h"
type = "plugin_action"
command = "jhochenbaum.hunkdiff.review"

[[keys.command]]
key = "prefix+shift+s"
type = "plugin_action"
command = "jhochenbaum.hunkdiff.send-review"
```

Activate the workflow:

```sh
herdr plugin enable jhochenbaum.hunkdiff
herdr config check
herdr server reload-config
```

Review opens automatically below the agent when it finishes. Use
`prefix+shift+h` (`Ctrl+B`, then `Shift+H` with Herdr's default prefix) to
open or refresh it manually. In Hunk, press `c` on a diff line to write
a comment and `Ctrl+S` to save it. Press `prefix+shift+s` (`Ctrl+B`, then
`Shift+S`) to submit the saved comments as the agent's next prompt.
Successful delivery clears the submitted comments; a failed submission
keeps them for retry.

The plugin associates one agent and one review pane with each worktree.
If agents share a checkout, send from the intended agent's pane to choose
the recipient; separate worktrees keep reviews independent.

`ai-tools/.local/herdr-hunk-diff` is the active plugin installation, not a
temporary build directory. Herdr loads its compiled code and bundled Hunk
from there, so keep it while linked. The `.gitignore` entry excludes it
from version control. Development dependencies are pruned after building;
the compiled code and runtime dependencies remain.

To update, reinstall dependencies with `npm ci --ignore-scripts`, reapply
the patch to the updated checkout, rebuild, prune development dependencies,
and relink. Do not use `herdr plugin install` to update this linked copy.

The plugin pins Hunk 0.22.0. The standalone Homebrew installation is 0.23.0;
those builds cannot share the same running session daemon. Use the plugin's
bundled Hunk for this workflow until their versions are aligned.

The previous `hunk.diff`, `hunk.autodiff`, and `persiyanov.reviewr` plugins
have been uninstalled. Their installation instructions and shortcuts are
removed from this guide. Keep Herdr's agent integrations above: their idle
state reports trigger the current plugin's automatic opening.

## TODO

- [ ] Document Codex CLI / Pi config once customized (currently defaults)
- [ ] Document Cursor setup (present on this machine, not yet written up)
- [ ] Document shared MCP servers, if any
- [ ] Decide whether to actually configure hunk as git pager/difftool, or
      leave it available but unconfigured
