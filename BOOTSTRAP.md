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

## Next

Continue with [`shell/README.md`](shell/README.md) for the rest of the
shell setup (nvm, pnpm, aliases), then [`claude-code/`](claude-code/) and
[`ai-tools/`](ai-tools/).
