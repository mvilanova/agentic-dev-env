# Shell

Zsh, managed with [Oh My Zsh](https://ohmyz.sh/), plus
[Starship](https://starship.rs/) for the prompt.

## Setup

1. Install Oh My Zsh + plugins and Starship — see
   [`../BOOTSTRAP.md`](../BOOTSTRAP.md) steps 1 and 4.
2. Install [nvm](https://github.com/nvm-sh/nvm) and
   [pnpm](https://pnpm.io/) (standalone install).
3. Copy `.zshrc.example` to `~/.zshrc` and `.profile.example` to
   `~/.profile`, filling in any placeholders (e.g. `GH_TOKEN`).

## Notable config

- **`GH_TOKEN`**: prefer `gh auth login` over hardcoding a token in
  `.zshrc`. If you must hardcode one, use a fine-grained PAT with minimal
  scope, and never commit the real value.
- **`.profile` vs `.zshrc`**: `.profile` duplicates the pnpm/nvm PATH setup
  because this machine's pre-commit hooks run via `bash -lc`, which reads
  `.profile`, not `.zshrc`.
- **Auto Node version switching**: `.zshrc` hooks `chpwd` to run `nvm use`
  automatically when entering a directory with an `.nvmrc`.
- **Copilot review helpers**: `ghpr` (create PR + request Copilot review)
  and `ghcopilot` (request Copilot review on the current branch's PR).

## Security note

The real `.zshrc` on this machine previously had a live GitHub PAT
hardcoded (`export GH_TOKEN=...`), stripped out of `.zshrc.example` here.
If you haven't already, rotate that token in GitHub settings and switch to
`gh auth login` instead of hardcoding one.
