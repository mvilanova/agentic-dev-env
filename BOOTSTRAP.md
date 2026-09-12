# Bootstrap: New Machine Setup

Order of operations when setting up a new machine, before getting into
tool-specific config (Claude Code, other AI tools, etc.).

Preference: install via **Homebrew** wherever a formula/cask exists. Fall
back to the tool's own installer (curl script, npm) only when it has no
brew option.

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
agent harnesses below — it installs its own integration hooks into each
one. See [`ai-tools/README.md`](ai-tools/README.md#herdr).

## 7. Agent harnesses (CLI/TUI coding agents)

Claude Code, Codex CLI, and Pi — each is a CLI/TUI program that wraps an
LLM with a tool-use loop (read/write/edit files, run shell commands) so it
can act on a codebase directly.

```sh
# Claude Code (Anthropic) — brew cask
brew install --cask claude-code

# Codex CLI (OpenAI) — brew cask
brew install --cask codex

# Pi (provider-agnostic, Earendil Works) — no brew cask, use npm
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

> Note: Anthropic's own docs point to a native curl installer
> (`curl -fsSL https://claude.ai/install.sh | bash`) as the primary
> supported method, which auto-updates itself independently of brew. On
> this machine that installer ran *in addition to* the brew cask, leaving
> two copies (`~/.local/bin/claude`, ahead on PATH, vs. the brew-installed
> one) — worth reconciling to just the brew cask for a single, predictable
> update path.

See [`claude-code/`](claude-code/) for Claude Code config, and
[`ai-tools/README.md`](ai-tools/README.md) for Codex CLI and Pi.

## Next

Continue with [`shell/README.md`](shell/README.md) for the rest of the
shell setup (nvm, pnpm, aliases), then [`claude-code/`](claude-code/) and
[`ai-tools/`](ai-tools/).
