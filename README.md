# Agentic Dev Environment

Documentation and config for how I set up my machine for agentic software
engineering — shell, terminal, Claude Code, and other AI tools.

Goal: if I get a new machine, this repo is enough to rebuild the setup.

## Contents

- [`BOOTSTRAP.md`](BOOTSTRAP.md) — first steps on a new machine, in order
  (Homebrew, Oh My Zsh, Vim, Nerd Fonts, Starship, terminal, herdr, agent
  harnesses)
- [`claude-code/`](claude-code/) — Claude Code settings, hooks, and skills
- [`shell/`](shell/) — shell (zsh/bash) config and aliases
- [`vim/`](vim/) — Vim config and plugins
- [`git/`](git/) — git and GitHub CLI config
- [`terminal/`](terminal/) — terminal emulator setup
- [`ai-tools/`](ai-tools/) — other AI coding tools and how they're configured

## Conventions

- Real config files that may contain machine-specific paths or secrets are
  kept as `*.example.*` templates here, with notes on what to fill in.
- Each subfolder has its own `README.md` explaining what's there and setup
  steps.
