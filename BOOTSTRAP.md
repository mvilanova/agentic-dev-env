# Bootstrap: New Machine Setup

Order of operations when setting up a new machine, before getting into
tool-specific config (Claude Code, other AI tools, etc.).

## 1. Oh My Zsh

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

> Note: `shell/.zshrc.example` in this repo also adds
> `zsh-syntax-highlighting` (`brew install zsh-syntax-highlighting`,
> sourced manually — it's not an Oh My Zsh bundled plugin).

## 2. Nerd Fonts

https://www.nerdfonts.com/

```sh
brew install --cask font-meslo-lgs-nerd-font
brew install --cask font-jetbrains-mono-nerd-font
```

Set your terminal's font to one of these afterward (see
[`terminal/README.md`](terminal/README.md)) — required for Starship's
prompt glyphs to render correctly.

## 3. Starship

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

## 4. Terminal

Set up iTerm2 and/or Ghostty — see [`terminal/README.md`](terminal/README.md).

## 5. Herdr (agent runtime)

https://herdr.dev/

Installed after the terminal + shell basics are in place, before
Claude Code config. See [`ai-tools/README.md`](ai-tools/README.md#herdr).

## 6. Agent harnesses (CLI/TUI coding agents)

Claude Code, Codex CLI, and Pi — each is a CLI/TUI program that wraps an
LLM with a tool-use loop (read/write/edit files, run shell commands) so it
can act on a codebase directly.

```sh
# Claude Code (Anthropic)
npm install -g @anthropic-ai/claude-code

# Codex CLI (OpenAI)
npm install -g @openai/codex

# Pi (provider-agnostic, Earendil Works)
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
```

See [`claude-code/`](claude-code/) for Claude Code config, and
[`ai-tools/README.md`](ai-tools/README.md) for Codex CLI and Pi.

## Next

Continue with [`shell/README.md`](shell/README.md) for the rest of the
shell setup (nvm, pnpm, aliases), then [`claude-code/`](claude-code/) and
[`ai-tools/`](ai-tools/).
