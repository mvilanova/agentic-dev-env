# Vim

Stock Vim (installed via brew, not the macOS system `/usr/bin/vim`) with
[vim-plug](https://github.com/junegunn/vim-plug) for plugin management.

## Setup

1. Install Vim: `brew install vim`
2. Install vim-plug:
   ```sh
   curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
     https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
   ```
3. Copy `.vimrc.example` to `~/.vimrc`.
4. Open vim and run `:PlugInstall` to install plugins.

## Notable config

- Based on the stock example `.vimrc` (backups, undofile, hlsearch,
  matchit) with [vim-lsp](https://github.com/prabirshrestha/vim-lsp)
  added as the only plugin.
- **Python LSP**: if `ruff` is installed (`pip install ruff` or
  `brew install ruff`), vim-lsp registers it as the Python language
  server, and `.py` files are auto-formatted on save via
  `LspDocumentFormatSync`.

## Note on PATH

`brew install vim` installs to `/opt/homebrew/bin/vim`, but macOS ships a
system vim at `/usr/bin/vim` which may resolve first depending on PATH
order. Check with `which -a vim`.
