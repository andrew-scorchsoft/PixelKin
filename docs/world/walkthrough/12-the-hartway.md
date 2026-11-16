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
| The low road north is BURIED (sealed under a drift, both ends); the road goes east round the Shoulder | `windward_stair_ii` (the east annex) | — |
| Hollis the rope-warden on the Landing: *nobody goes up alone*; Greg is in Galehigh | `hartway_climb` (stepping up to the Staircase alone runs the same hook) | `flag:q_hartway` |
| Greg at the top of the town; promise to say "No, Greg" | `galehigh_terraces` (`greg_town`) | `flag:greg_found` |
| Rope up on the Landing → the Staircase beat arms | `hartway_climb` | `flag:greg_roped` |
| The climb (below) | `hartway_climb` | `flag:hart_*` |
| The trail west off the Seat | → `pale_vault_glacier` (edge link) | `flag:pass_open` (derived) |

**The Hartway slots INTO the pass (v1.51).** No closed road, no steps into a side zone: Stair II
gained a ten-column east annex (the Shoulder) so the climb sits edge-to-edge between the two
maps — in by its west edge at the foot (rows 45-46), out by its west edge at the Seat (rows 9-10).

**The ridges cannot be walked.** The Staircase and the Whiteback are solid `gulf` cells wearing a
pinned `crest_*` tile: a two-pixel line of snow on a fin of rock. The `edge` cutscene op carries
Greg and then the player across (hauled steps, the sprite teetering), so the mountain itself is
the gate: without Greg you stop at the first ridge. Ladders are climbed with a real climb
animation (back to the camera, hand over hand, never at a run) everywhere a ladder span exists.

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
Those saves find both rope ladders already fixed (`flag:hart_rope_1/2`, ANY_OF: Greg's own
`hart_ladder_n` or the same later milestones), so the pass is walkable end to end; fetching Greg
from Galehigh still plays the whole story (he "tries the old pegs" instead of fixing new ones). Greg's stages and the story bands want
`flag:greg_roped`, so a mountain walked without him is simply quiet.

### Optional, for players who know Paul

- Paul's lamp menu gains **Greg?** once you have met Greg → **Paul's Rope-End**
  (`flag:greg_token`). Carry it to Greg and he knows the knot (`script.greg_knot`).
- After the herd, **The Hartway** on Paul's menu: he tells his own ridge and his own herd, keeps
  the stone, gives 3 Lumen Drops (`flag:q_hartway_done`).
- Seeds (words only): the Pearlmoor innkeep, the fisher after the Tide, Kathleen, Rose and the
  pinboard in Paul's house. None names the quest or says what happens on the mountain.

### Staging rules this map learned (two sub-agent reviews, 2026-11)

- A fix-it beat that happens off-screen didn't happen: `cameraFocus` on rope ladder 2 as Greg
  drops it, and walk the player to the bench before "you sit".
- The player follows Greg out onto the Whiteback before the reel starts, so the showpiece ridge
  is walked, not only watched.
- The exit off the Seat is the trail west along its back (signed); the Lumen Drop cache costs a
  detour into the high grass.
- Stepping up to the Staircase ropes you in on the spot once Greg has agreed, and he leads
  straight off (gate-keepers come to you).
- Iron pegs are signed at both ladder sites before the ladders exist: a seeded lock, not a
  false lead.

## Engine pieces this added (all data, reusable)

- **Flag-gated spans**: `SpanZone.requires_flag` / `hidden_when_flag` — a ladder that isn't
  there until its flag is. Pair it with a non-solid object carrying the same flag
  (`hartway_rope_ladder`). Mirrored in `worldmodel.py`; `check_traversal.mjs` walks it.
- **Captions on the `frames` op**: `captions` (per frame: a string, pages, or null) puts words
  on the stills and waits for Confirm; `frameSfx` fires a cue as a frame lands.
- **`hartway_set`**: the `gulf` family (the drop beside a ridge), drawn over `snow`, plus the
  ten pinned `crest_*` tiles (a ridge nobody can walk).
- **The `edge` op**: `{op:'edge', actor, path, speed?, sidle?, teeter?}` walks an actor along a
  line that collides (hauled steps via `Actor.HAUL`, a lean each step, optional stop-and-wobble).
- **Ladder climbing**: `Player.execute` climbs any `kind:'ladder'` span (slower, hauled, back to
  the camera, mirrored each rung).

## Validation hooks

- `windward_stair_ii` (W=38): `to_hartway(_s)` on the east edge (37,16)/(37,17), ungated; the
  old `to_glacier` warps are gone (the north gap is sealed, a drift + `sign.hartway_low_road`).
- `hartway_climb`: `to_crags(_s)` (0,45)/(0,46) and `to_vault(_s)` (0,9)/(0,10), ungated; spans
  `rope_ladder_1/2` require `flag:hart_rope_1/2`; both ridges are SOLID (pinned crest tiles).
- `pale_vault_glacier`: `to_hartway(_s)` on the east edge (31,10)/(31,11); the south gap is sealed.
- Band 35–36 + day twins (`HARTWAY_ENCOUNTERS` in `build_species.py`; `CURATED_AREAS`).
- `audit_journey` replays the whole chain to reach the Frost Gleam; `audit_region` GRANTS:
  `greg_roped`, `hart_rope_1/2` and `pass_open` on the climb.
- Geometry: both links are EDGE links, so the map places (`world_geometry.py --check`).
