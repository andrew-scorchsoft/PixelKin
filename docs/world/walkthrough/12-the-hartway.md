# 12 — The Hartway (2026-11)

**Optional. Paul content: post-Chickenpig by construction, ships silently** (never in the
changelog, the guide or the website — `guide.mjs` FORBIDDEN carries the names). Level
band 17–22. Maps `hartway_foot`, `hartway_climb`. Content `content/regions/hartway.ts`.

## The true story under it

Paul used to go alpine hiking with **Greg**, who was experienced and completely
confident. Greg went first; Paul's job was to stop Greg doing stupid things.

- **The ridge.** Once, on a hard-snow ridge Paul would never have crossed alone, Greg's
  legs went shaky halfway and they both saw it was far more dangerous than they'd
  thought. At the far end they sat down and laughed, then walked up to the safe trail.
- **The herd.** From a ridge the animals had taken back, looking down on towns and
  valleys, they watched a mist roll in with a great herd of elk inside it. As the mist
  climbed the mountain there were shadows all around them: the herd using it as cover.

## How the game tells it

The **player takes Paul's end of the rope.** Greg has not climbed since Paul stopped
("nobody to tell me no"). The herd is the **Sunstags** (#121), the light of old summers
in their antlers: the Hartway is the *harts'* way up, and people only ever borrowed it.

### Side quest — "A Rope for Two" (`s8_a_rope_for_two`)

| Step | Where | Flag |
|---|---|---|
| Hollis the rope-warden: *nobody goes up alone*; only Greg knows the ridges | `hartway_foot` (the steps' `blocked_ref` runs the same hook) | `flag:q_hartway` |
| Paul at his lamp, menu option **Greg?** → **Paul's Rope-End** | `pearlmoor_breakwater` | `flag:greg_token` |
| (optional clue) Greg's slate at the Wayward Arms | `wayward_arms` | — |
| Greg on his stump; show him the knot | `pearlmoor_wanderwood_far` | `flag:greg_found` |
| Rope up at the foot → the steps open | `hartway_foot` | `flag:greg_roped` |
| The climb (below) | `hartway_climb` | `flag:hart_*` |
| Tell Paul (**The Hartway**) → 3 Lumen Drops; the Seat's stone stays on his lamp | `pearlmoor_breakwater` | `flag:q_hartway_done` |

Meeting Greg first also opens the quest (he points you at Paul). Paul's rope-end is the
only thing that moves him.

### The climb (south = lower)

| Tier | Beat |
|---|---|
| The Landing | **The Staircase**: Greg leads a one-wide rock rib through the gulf (`script.hart_staircase`). |
| The Shelf | He fixes **rope ladder 1** (`flag:hart_ladder_1`) so nobody has to do the rib again. Walkers' camp (rest). **"No, Greg" #1**: the chimney. |
| The High Shelf | **The Whiteback**, the story ridge: a captioned picture reel (stride → shaky legs → sitting down laughing). **#2**: rope in shorter. Then **rope ladder 2** (`flag:hart_ladder_2`). |
| The Seat | **#3**: the snow lip. Sit on the bench: the view, then the mist and the herd (`script.hart_mist_reel`). Greg gives the **Stone from the Seat**. |

- Three "No, Greg" choices set `flag:hart_sense_1..3`; all three derive
  `flag:hart_sense_all` (FlagStore `COUNT_AT_LEAST`) → Greg's 2 Beacon Charges and a line
  from Paul. Saying yes costs nothing: Greg is embarrassed, never hurt.
- After the herd, the Seat's high grass gains **Dawnfawn** (#120) (`*_herd` zones,
  `requires_flag: flag:hart_mist_seen`).
- The bench replays the view or the whole herd reel on later visits.

## Engine pieces this added (all data, reusable)

- **Flag-gated spans**: `SpanZone.requires_flag` / `hidden_when_flag` — a ladder that
  isn't there until its flag is. Pair it with a non-solid object carrying the same flag
  (`hartway_rope_ladder`). Mirrored in `worldmodel.py`; `check_traversal.mjs` walks it.
- **Captions on the `frames` op**: `captions` (per frame: a string, pages, or null) puts
  words on the stills and waits for Confirm; `frameSfx` fires a cue as a frame lands.
- **`hartway_set`**: the `gulf` family (the drop beside a ridge), drawn over `snow`.

## Validation hooks

- `hartway_foot` `to_climb` requires `flag:greg_roped`; `blocked_ref` `script.hartway_gate`.
- `hartway_climb` spans `rope_ladder_1/2` require `flag:hart_ladder_1/2`; both ridges are
  walkable without them (the audits prove the ridge road on its own).
- Bands: foot 17–19, climb 19–22 (`HARTWAY_ENCOUNTERS` in `build_species.py`; both maps
  in `CURATED_AREAS` and `progression.mjs` `TREND_SKIP_AREAS`).
- Geometry: the foot sits straight west of Wayward Rise at world (-27,-150); the climb
  is a mid-map portal (a mountain over other ground never places).
