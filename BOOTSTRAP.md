# Bootstrap: New Machine Setup

Order of operations when setting up a new machine, before getting into
tool-specific config (Claude Code, other AI tools, etc.).

Preference: install via **Homebrew** wherever a formula/cask exists. Fall
back to the tool's own installer (curl script, npm) when it has no brew
option, or (Claude Code specifically — see step 7) when brew's version
lags too far behind.

## 0. Homebrew

https://brew.sh/

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## 1. Oh My Zsh

No brew formula for Oh My Zsh itself — use the official installer:

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Enable plugins in `~/.zshrc`:

```sh
plugins=(git autojump brew colored-man-pages history macos pip python)
```

Install `autojump` itself via brew (the plugin just wraps it):

```sh
brew install autojump
```

Also install `zsh-syntax-highlighting` (not an Oh My Zsh bundled plugin —
sourced manually at the end of `.zshrc`, see `shell/.zshrc.example`):

```sh
brew install zsh-syntax-highlighting
```

## 2. Vim

```sh
brew install vim
```

See [`vim/README.md`](vim/README.md) for vim-plug setup and config.

## 3. Nerd Fonts

https://www.nerdfonts.com/

```sh
brew install --cask font-meslo-lgs-nerd-font
brew install --cask font-jetbrains-mono-nerd-font
```

Set your terminal's font to one of these afterward (see
[`terminal/README.md`](terminal/README.md)) — required for Starship's
prompt glyphs to render correctly.

## 4. Starship

https://starship.rs/guide/

```sh
brew install starship
starship preset gruvbox-rainbow -o ~/.config/starship.toml
```

Then add to `~/.zshrc` (already in `shell/.zshrc.example`):

```sh
eval "$(starship init zsh)"
```

The generated config is checked in at
[`shell/starship.toml`](shell/starship.toml) — copy it to
`~/.config/starship.toml` instead of regenerating the preset, unless you
want to start from a different Starship preset.

## 5. Terminal

```sh
brew install --cask iterm2
brew install --cask ghostty
```

Then see [`terminal/README.md`](terminal/README.md) for profile import
(iTerm2) and font setup (both).

> Note: on this machine iTerm2 was installed outside brew (manual
> download) — reinstall via the cask above for a brew-managed setup.

## 6. Herdr (agent runtime)

https://herdr.dev/

```sh
brew install herdr
```

Installed after the terminal + shell basics are in place, before the
agent harnesses below. After installing the harnesses in step 7, run
herdr's integration installer for each one:

```sh
herdr integration install claude
herdr integration install codex
herdr integration install pi
```

See [`ai-tools/README.md`](ai-tools/README.md#herdr) for what each one
sets up. Optionally, also add herdr's
[agent skill](ai-tools/README.md#agent-skill) for reusable
herdr-awareness inside the agent itself:

```sh
npx skills add herdrdev/herdr --skill herdr -g
```

## 7. Agent harnesses (CLI/TUI coding agents)

Claude Code, Codex CLI, and Pi — each is a CLI/TUI program that wraps an
LLM with a tool-use loop (read/write/edit files, run shell commands) so it
can act on a codebase directly.

```sh
# Claude Code (Anthropic) — native installer, NOT the brew cask (see note)
curl -fsSL https://claude.ai/install.sh | bash

# Codex CLI (OpenAI) — brew cask
brew install --cask codex

# Pi (provider-agnostic, Earendil Works) — no brew cask, use npm
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

> Note: Claude Code is the one exception to "prefer brew" in this repo.
> Homebrew's `claude-code` cask lags noticeably behind Anthropic's native
> installer (checked 2026-09-12: brew had 2.1.236 vs. native's 2.1.269,
> even right after `brew update`), and the native installer auto-updates
> itself in the background — which is what Anthropic's own docs recommend
> as primary. This machine previously had both installed at once (brew
> cask + native, native winning on PATH); the brew cask was removed to
> avoid the duplicate.

See [`ai-tools/README.md`](ai-tools/README.md#agent-harnesses) for all
three, and [`ai-tools/claude-code/`](ai-tools/claude-code/) for Claude
Code's settings file specifically.

## 8. Hunk (diff review)

https://www.hunk.dev/ — review-first terminal diff viewer for
agent-authored changesets.

```sh
brew install hunk
```

See [`ai-tools/README.md`](ai-tools/README.md#hunk) for other install
methods and usage notes.

## Next

Continue with [`shell/README.md`](shell/README.md) for the rest of the
shell setup (nvm, pnpm, aliases), then [`ai-tools/`](ai-tools/).
