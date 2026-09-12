# Terminal

Two terminal apps in rotation: iTerm2 and Ghostty.

## iTerm2

Profile exported via **Preferences → Profiles → Other Actions → Save
Profile as JSON**, checked in at [`iterm2-profile.json`](iterm2-profile.json)
(machine-specific fields like working directory stripped).

To import: **Preferences → Profiles → Other Actions → Import JSON Profiles**,
then select it as default if desired.

Notable settings:
- Font: `MesloLGS-NF-Regular 14` (Nerd Font — see [`../BOOTSTRAP.md`](../BOOTSTRAP.md))
- Unlimited scrollback, draw Powerline glyphs, mouse reporting on

## Ghostty

No custom config — running on Ghostty defaults
(`~/Library/Application Support/com.mitchellh.ghostty/config.ghostty` is
empty on this machine). Set the font manually in-app to a Nerd Font (e.g.
JetBrains Mono Nerd Font) to match Starship's prompt glyphs.

## TODO

- [ ] If Ghostty config is customized later, check in `config.ghostty`
