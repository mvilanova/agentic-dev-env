# Git & GitHub CLI

## Setup

1. `gh auth login` (GitHub CLI authentication — no token files to manage).
2. Copy `.gitconfig.example` to `~/.gitconfig`, uncomment and fill in
   `[user] name` / `email`.
3. Copy `gitignore_global.example` to `~/.config/git/ignore` (git's global
   excludes file).
4. Copy `gh-config.yml.example` to `~/.config/gh/config.yml`.

## Notable config

- **Credential helper**: `.gitconfig` routes GitHub HTTPS auth through
  `gh auth git-credential` instead of a stored token — the path
  (`/opt/homebrew/bin/gh`) is Apple Silicon's default brew prefix; adjust
  to `which gh` on Intel Macs (`/usr/local/bin/gh`) or Linux.
- **Global gitignore**: excludes `**/.claude/settings.local.json`
  everywhere, so per-project local Claude Code overrides never get
  accidentally committed.
- **`gh` alias**: `co` → `pr checkout`.

## Note

The real `.gitconfig` on this machine has `user.name` / `user.email`
commented out — i.e. no git identity is set globally. Repos either set it
per-project or inherit `user.name`/`email` from elsewhere. Worth setting
explicitly if that's not intentional.
