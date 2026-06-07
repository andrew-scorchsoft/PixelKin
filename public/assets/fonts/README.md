# Fonts

In-game UI text uses one bundled pixel font, referenced everywhere through the
`PixelKin` family name (see `src/game/ui/theme.ts` and the `@font-face` rule in
`src/styles/global.css`). Keeping it to a single font is part of the game's
design language — one consistent voice across every screen.

## Press Start 2P (the `PixelKin` family)

- **Family name in code:** `PixelKin`
- **Source font:** Press Start 2P
- **Licence:** SIL Open Font License, Version 1.1 — see `OFL.txt` (shipped here).
- Designed on an 8px grid, so it renders crisp at 8px (body) and 16px (titles),
  matching our 240×160 internal resolution.

The TTF itself lives at `src/styles/fonts/PressStart2P-Regular.ttf` so Vite
bundles and fingerprints it (correct URLs in both dev and the static build). It's
referenced once, in the `@font-face` rule in `src/styles/global.css`; everything
else uses the `PixelKin` family name via `src/game/ui/theme.ts`. This file keeps
the licence alongside the served assets. Swapping the font is a one-line change to
the `@font-face` rule plus the TTF in `src/styles/fonts/`.
