# 12 — The Hartway (2026-11)

**MAIN PATH** — the last pitch of the Windward pass: from the high crags
(`windward_stair_ii`) over the Hartshoulder to Pale Vault (`pale_vault_glacier`), on the map
`hartway_climb`, level band 35–36. Content `content/regions/hartway.ts`.

**Also Paul content, so it still ships silently:** never in the changelog; the guide describes
the required step without the hidden names (`guide.mjs` FORBIDDEN carries them).

## The true story under it

Paul used to go alpine hiking with **Greg**, who was experienced and completely confident.
Greg went first; Paul's job was to stop Greg doing stupid things.

- **The ridge.** Once, on a hard-snow ridge Paul would never have crossed alone, Greg's legs
  went shaky halfway and they both saw it was far more dangerous than they'd thought. At the
  far end they sat down and laughed, then walked up to the safe trail.
- **The herd.** From a ridge the animals had taken back, looking down on towns and valleys,
  they watched a mist roll in with a great herd of elk inside it. As the mist climbed the
  mountain there were shadows all around them: the herd using it as cover.

## How the game tells it

The **player takes Paul's end of the rope.** Greg has not climbed since his partner stopped
("nobody to tell me no"). The herd is the **Sunstags** (#121), the light of old summers in
their antlers: the Hartway is the *harts'* way up, and people only ever borrowed it. On the
main path Greg never names his partner; a player who knows Paul gets the rest.

### The required chain — "A Rope for Two" (`north_a_rope_for_two`)

| Step | Where | Flag |
|---|---|---|
| The low road north is drifted shut (`to_glacier` wants `flag:pass_open`) | `windward_stair_ii` | — |
| Hollis the rope-warden: *nobody goes up alone*; Greg is in Galehigh | `windward_stair_ii` (the steps' `blocked_ref` runs the same hook) | `flag:q_hartway` |
| Greg at the top of the town; promise to say "No, Greg" | `galehigh_terraces` (`greg_town`) | `flag:greg_found` |
| Rope up at the steps → they open | `windward_stair_ii` | `flag:greg_roped` |
| The climb (below) | `hartway_climb` | `flag:hart_*` |
| The safe trail down off the Seat | → `pale_vault_glacier` | `flag:pass_open` (derived) |

Greg is visible in Galehigh from the first visit ("just looking at the hill"), before the
player knows they will need him.

### The climb (south = lower)

| Tier | Beat |
|---|---|
| The Landing | **The Staircase**: Greg leads a one-wide rock rib through the gulf (`script.hart_staircase`). |
| The Shelf | He fixes **rope ladder 1** (`flag:hart_ladder_1`) so nobody has to do the rib again. Walkers' camp (rest). **"No, Greg" #1**: the chimney. |
| The High Shelf | **The Whiteback**, the story ridge: a captioned picture reel (stride → shaky legs → sitting down laughing). **#2**: rope in shorter. Then **rope ladder 2** (`flag:hart_ladder_2`). |
| The Seat | **#3**: the snow lip. Then you sit (the scene runs on from the lip beat, so it cannot be missed): the view, the mist and the herd (`script.hart_mist_reel`). Greg gives the **Stone from the Seat**. East end: the safe trail to Pale Vault. |

- Three "No, Greg" choices set `flag:hart_sense_1..3`; all three derive `flag:hart_sense_all`
  → Greg's 2 Beacon Charges. Saying yes costs nothing: Greg is embarrassed, never hurt.
- **Dawnfawn** (#120) graze the high grass above the Seat.
- The bench replays the view or the whole herd reel on later visits.

### Never locking a save out

`flag:pass_open` is a FlagStore `ANY_OF`: the Seat reached (`hart_b3_done` / `hart_mist_seen`),
or the player was already past the pass (`chart:pale-vault-glacier`, `gleam:frost` or later).
Those saves walk the low road as before; the Hartway stays there for them, and fetching Greg
from Galehigh still plays the whole story. Greg's stages and the story bands want
`flag:greg_roped`, so a mountain walked without him is simply quiet.

### Optional, for players who know Paul

- Paul's lamp menu gains **Greg?** once you have met Greg → **Paul's Rope-End**
  (`flag:greg_token`). Carry it to Greg and he knows the knot (`script.greg_knot`).
- After the herd, **The Hartway** on Paul's menu: he tells his own ridge and his own herd, keeps
  the stone, gives 3 Lumen Drops (`flag:q_hartway_done`).
- Seeds (words only): the Pearlmoor innkeep, the fisher after the Tide, Kathleen, Rose and the
  pinboard in Paul's house. None names the quest or says what happens on the mountain.

## Engine pieces this added (all data, reusable)

- **Flag-gated spans**: `SpanZone.requires_flag` / `hidden_when_flag` — a ladder that isn't
  there until its flag is. Pair it with a non-solid object carrying the same flag
  (`hartway_rope_ladder`). Mirrored in `worldmodel.py`; `check_traversal.mjs` walks it.
- **Captions on the `frames` op**: `captions` (per frame: a string, pages, or null) puts words
  on the stills and waits for Confirm; `frameSfx` fires a cue as a frame lands.
- **`hartway_set`**: the `gulf` family (the drop beside a ridge), drawn over `snow`.

## Validation hooks

- `windward_stair_ii`: `to_hartway` (17,5) requires `flag:greg_roped`, `blocked_ref`
  `script.hartway_gate`; `to_glacier(_e)` require `flag:pass_open`, `blocked_ref`
  `script.hartway_low_road`.
- `hartway_climb`: `to_crags` (14,48) and `to_vault` (27,2) are ungated; spans `rope_ladder_1/2`
  require `flag:hart_ladder_1/2`; both ridges are walkable without them.
- `pale_vault_glacier`: `to_hartway` (23,27) lands on the Seat's steps.
- Band 35–36 + day twins (`HARTWAY_ENCOUNTERS` in `build_species.py`; `CURATED_AREAS`).
- `audit_journey` replays the whole chain to reach the Frost Gleam; `audit_region` GRANTS:
  `greg_roped` on Stair II, `pass_open` on the climb.
- Geometry: every link is a mid-map portal (a mountain over other ground never places).
