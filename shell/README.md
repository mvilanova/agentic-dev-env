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
4. Install direnv and copy `direnv.toml` to
   `~/.config/direnv/direnv.toml` — see
   [`../BOOTSTRAP.md`](../BOOTSTRAP.md) step 10.

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
- **Auto Python venv activation**: handled by direnv, not a custom `chpwd`
  hook — see below.

## direnv (Python venvs)

[direnv](https://direnv.net/) activates a project's venv whenever you `cd`
anywhere inside it (including subdirectories) and deactivates it when you
leave. Preferred over a hand-rolled `chpwd` hook because it handles
subdirectories and unloading correctly, and only runs `.envrc` files you've
explicitly approved.

### Per-project setup

At the project root:

```sh
echo 'source .venv/bin/activate' > .envrc   # adjust path, e.g. backend/.venv
direnv allow
```

`direnv allow` must be re-run whenever `.envrc` changes — that's the
safety check that stops a freshly cloned repo from running code on `cd`.

### Notes

- **Don't use `layout python`**: direnv's built-in creates a *separate*
  venv under `.direnv/`. Use `source .../activate` to reuse the project's
  existing `.venv`.
- **Prompt**: direnv only exports env vars, so the venv's `(venv)` `PS1`
  prefix doesn't appear. Starship's `python` module reads `VIRTUAL_ENV`
  directly, so the prompt still shows the active venv.
- **Quiet logging** ([`direnv.toml`](direnv.toml)): silences the
  `direnv: loading ...` and `direnv: export +VIRTUAL_ENV ...` lines on
  every `cd`; errors (e.g. a blocked `.envrc`) still show. Run
  `direnv status` to see what's loaded. Gotchas found on direnv 2.37.1:
  - `log_format = "-"` (documented as "disable logging") prints garbled
    `%!!(MISSING)...` output instead.
  - `export DIRENV_LOG_FORMAT=""` only silences `direnv exec`, not the
    shell hook.
  - `log_filter` is an *allow*-list (only matching lines are shown), so
    `"^$"` hides everything except errors.

## Security note

The real `.zshrc` on this machine previously had a live GitHub PAT
hardcoded (`export GH_TOKEN=...`), stripped out of `.zshrc.example` here.
If you haven't already, rotate that token in GitHub settings and switch to
`gh auth login` instead of hardcoding one.
