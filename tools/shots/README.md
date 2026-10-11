# tools/shots — headless screenshot harness

`shoot.mjs` boots the **real game** (Vite dev server + headless Chromium via the
`playwright` devDependency), writes a crafted current-schema save into slot 1,
drives the boot flow with the keyboard (Splash → Attract → Title → CONTINUE), waits
for the WorldScene to be idle, and screenshots the canvas.

```bash
node tools/shots/shoot.mjs --map tinderwick --x 5 --y 8 --out shots/tinderwick.png
node tools/shots/shoot.mjs --map pearlmoor_quay --x 13 --y 14 --facing up \
     --flags gleam:ember,has_beacon_wick --abilities tidecall --out pq.png
node tools/shots/shoot.mjs --map tinderwick --x 5 --y 8 --steps "right,right,down"
node tools/shots/shoot.mjs --map tinderwick --x 5 --y 8 --battle 2:6   # wild battle vs kin #2 lv 6
node tools/shots/shoot.mjs --map tinderwick --x 5 --y 8 --version-from 1.0  # "world has changed" notice
node tools/shots/shoot.mjs --scene title --out title.png
node tools/shots/shoot.mjs --batch shots.json   # one server + browser for every shot
```

`node tools/shots/shoot.mjs --help` lists every option. The most useful ones:

| Option | Meaning |
|---|---|
| `--flags a,b` | Flags held. Bare names get a `flag:` prefix; `gleam:*`, `chart:*` pass through. |
| `--abilities` | Lantern Gifts held (`tidecall,...`). |
| `--party` | `starter` (default: #1 lv `--level`, 5), `none`, or `ID[:LV],...`. |
| `--steps` | One tile per entry, walked after spawning; warps/triggers fire for real. |
| `--battle ID[:LV]` | Opens a normal wild battle on the map, shot at its command menu. |
| `--scale N` | Output is `240N × 160N` px (default 4). The viewport sets the render scale. |
| `--wait ms` | Extra settle time before the shot (700 default, 2500 for battles). |
| `--keep-hud` | Don't wait for the area-name banner / SAVED glyph to fade. |
| `--version-from v` | Save `last_version` (default = current `GAME_VERSION`, so no notice). |
| `--no-idle` / `--confirms N` | Shoot a scene that plays on load (a crown interlude) `--wait` ms after CONTINUE, then page it with N Confirm taps. Without `--no-idle` the four `interlude_*_seen` flags are seeded so crown-holding shots stay quiet. |
| `--greet ID` | Step beside that ambient kin (wherever it grazed), face it and Confirm — shoots its greeting mid-dialogue; `--confirms N` pages on (REGISTER note, its event). |
| `--no-defaults` | Skip the quiet flags (all `chart:*` so no reveal pops, tutorials seen, `has_starter`). |
| `--url` | Use an already-running dev server instead of starting one. |

**Batch file**: a JSON array of specs using the same keys as the CLI (without the
`--`, e.g. `{"map":"tinderwick","x":5,"y":8,"steps":"right,up","out":"a.png"}`, or
`{"scene":"title"}`). CLI options given alongside `--batch` act as defaults. A failing
shot saves `<out>.fail.png` (the whole page) and the run exits 1.

How it works: game state is read via the dev-only `window.__pixelkin` handle
(`src/main.ts`), and the save is built in-page from the game's own modules
(`makeStarterKin`, `CHARTS`, `SAVE_SCHEMA_VERSION`, `GAME_VERSION`), so it tracks schema
changes. Settings are forced to the `plain` shell, muted, instant text. Audio is also
muted at the browser level. Chromium comes from `PLAYWRIGHT_BROWSERS_PATH`
(`/opt/pw-browsers`). Never run `playwright install`. A shot takes about 6–9 s.
