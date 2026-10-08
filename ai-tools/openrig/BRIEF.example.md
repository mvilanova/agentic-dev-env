# Goal
Add dark mode to the Tempo web app in `frontend/`.

# Constraints
- Tailwind 4: use a `dark` custom variant driven by a `data-theme`
  attribute, not only `prefers-color-scheme`.
- Default to the system preference; persist a manual override in
  `localStorage`.
- The toggle lives in the existing settings UI.
- No new dependencies.
- Follow `AGENTS.md`. Run `pnpm lint` and `pnpm test` before handing off.

# Acceptance
- Every screen reachable from the main nav is readable in both themes.
- Calendar cards, auth screens and the home agenda (known hard-coded
  colors) use theme tokens.
- Screenshots of light and dark for home, calendar and settings are
  attached to the PR.
- Open one PR against `feat/dark-mode`. Do not merge.
