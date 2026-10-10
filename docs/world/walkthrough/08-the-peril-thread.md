# 08 — The Peril Thread: *what the Long Dusk costs*

> **Status: BUILT (R9, 2026-10).** A cross-region layer over the existing spine. It adds
> no Gleam, gate or progression flag. It makes the Dusk **visible and personal**: the
> player watches it get worse as they travel, and watches their own relit Gleams undo it.
> Read with the spine ([`README.md`](./README.md) §2 golden thread, §3 Arc B and Arc D)
> and the cinematic standard ([`../cinematics.md`](../cinematics.md)).

## 0. Why it exists

The playtest note was simple: *"We haven't shown any signs of the peril throughout the
land."* The spine had the beats (the `dusk_begins` omen, the drained Glowmoss site, Còr,
Coldfog, the Great Null), but between them the world was mostly cosy towns and challenges.
The Long Dusk was something you were told about, not something you saw cost anyone anything.

The thread answers that with three rules:

1. **Show a cost, then a face.** Every beat is a visible mark on the world (a crater, a
   doused brazier, a packed bundle, a notice) **and** a person living with it. The mark
   gets your attention; the person gives you a reason to care.
2. **It escalates in step with the journey.** The beats are staged on flags the journey
   already sets. Early on the Dusk is a rumour and one strange strike. By the North the
   falls come *nearer the mountain* and the Hollowing's notices are pinned in town squares.
   By the West, families have *chosen* the quiet. At the ring, the gone-quiet themselves
   come to look at the Spire. Arc B's monotonic rule holds: no beat shows the Dusk *weaker*
   than an earlier one, until the player turns it back.
3. **Your light heals it, visibly.** Each beat's lines change when the region's Gleam is
   relit, and several marks physically mend through same-footprint object swaps. The
   final bookend sends the post-game player home to see the first crater in flower. The
   point is that **progress matters to someone**, not only to the badge case.

**Tone (binding):** cosy-melancholy, "lanterns in the dark". No gore, no injury, nobody
dies on-screen, and no cartoon villainy. Grief is allowed (an old man's first tree; a
grandfather lost last winter to old age). The Hollowing stay *gentle and half-right*. Their
notice is kind, and the family who joined them are tired, not wicked. A little warmth
glints in most beats (Tamsin "isn't allowed to water them"). **Everything is optional
colour.** No beat gates a warp, blocks a lane or sets a progression flag.

## 1. The new canon fact: *fallen stars*

When a star gutters out, **sometimes its last cinder falls**. It lands cold and dark,
still hot enough on the way down to scorch whatever it strikes. Folk call it a
once-in-a-lifetime thing; the old ones know it isn't. **Every fall lands nearer the mountain.**
This makes the Long Dusk physical, and it is the dark mirror of the post-game
**Starfall** ([`06-postgame.md`](./06-postgame.md)). Those shards are the *woken* sky
settling and carry a warm gold core; a Dusk cinder is the same matter **gone out**: no
gold, only a cold blue-grey glow in its cracks. At `flag:dawn` every cinder **wakes** into
a star shard (`vigil_star_shard`), because it was never dead, only guttered. (LORE:
`fallen_stars`, unlocked by `flag:orchard_strike_seen`.)

## 2. The beats

| # | Region · map | Keyed on | The mark | The face (sample line) | Healing |
|---|---|---|---|---|---|
| **S1** | South · `duskapple_orchard` | first entry (`flag:orchard_strike_seen`); `flag:dusk_begins`; `gleam:ember`; `flag:dawn` | **The fallen star**: a scorched crater where the orchard's first tree stood, a cold cinder in its pit, two charred trees, singed grass. A once-only **first-sight cutscene** on the mouth band (letterbox, music out, camera on the crater, the gutter sting) | **Old Wendel** (`script.orchard_wendel`): *"The village says it's a once-in-a-lifetime thing. I've had a lifetime. It isn't."* **Tamsin**, his granddaughter (`script.orchard_tamsin`): *"It didn't make a sound. That's the bit I keep thinking about."* | `gleam:ember` → green **shoots** come up in the burn, and both voices turn hopeful. `flag:dawn` → the shoots **bloom**, the charred trees **leaf** again, the cinder **wakes** into a star shard |
| S2 | South · `tinderwick` *(placement deferred, §4)* | `flag:dusk_begins`; `gleam:ember`; `flag:dawn` | Lamps left burning in every window | **Neighbour** (`script.peril_tinderwick_neighbour`): *"We look like a festival that forgot to start."* | `gleam:ember`: *"I blew my window lamp out last night… and I slept."* |
| S3 | South · `pearlmoor_quay` *(placement deferred, §4)* | static | The **harbour notice**: the north-shore tide-lamps went dark and won't take a light | `sign.peril_pearlmoor_board`: *"The villagers are reported well. And very quiet."* | (the Tide Gleam beat in Pearlmoor carries the relief) |
| **E1** | East · `saltreach_fen_i` (landing) | `gleam:verdant`; `flag:dawn` | A fen family's **bundles**, packed to leave | **Fen mother** (`script.peril_fen_leaver`): *"Mother's lamp went out on the sill and wouldn't take a match. You don't stay, after a thing like that."* | `gleam:verdant` → the bundles are gone (*"We unpacked."*); dawn: *"Did you know the reeds are GOLD?"* |
| **N1** | North · `galehigh_terraces` (plaza) | `gleam:storm`; `flag:met_cor`; `flag:dawn` | The Hollowing's **notice**, pinned up again every night (`sign.peril_quiet_notice`: *"The dark does not take. It only keeps."*) | **Terrace weaver** (`script.peril_notice_reader`): *"The worst of it is how kind the hand is."* After `met_cor`: *"He doesn't have to take anything. People go to him."* | dawn: she takes the notice down and keeps it (*"It seemed rude to burn something that gentle."*) |
| **N2** | North · `hushfrost_pass_i` | `flag:orchard_strike_seen`; `gleam:frost`; `flag:dawn` | **The second fall**: a fresh crater in the snow beside the trail, its cinder still hissing | **Pass-walker** (`script.peril_hushfrost_counter`): *"This is the fourth I know of. Every one has come down nearer the mountain."* (She names the orchard if you saw it.) | `gleam:frost`: *"Just cold now. I'll take cold."* `flag:dawn` → the cinder **wakes**; folk warm their hands on it |
| **W1** | West · `sunvault_climb_i` | `gleam:solar`; `flag:dawn` | A family's own **brazier, doused on purpose**: they chose the Quiet | **Quiet father** (`script.peril_quiet_family`): *"It sounded like mercy. Some nights it still does."* | `gleam:solar` → the brazier is **lit** again (*"My youngest lit it while I slept."*); dawn: *"We're walking home tomorrow. In daylight."* |
| **W2** | West · `nightreach_observatory` | `flag:great_null_known`; `gleam:lunar`; `flag:dawn` | The **Ledger of Lights**: every star lost since the Dusk began, in one column that only grows | **Ledger-keeper** (`script.peril_ledger`): *"Two hundred and six. Somebody ought to remember them by name."* | `gleam:lunar` → *"Tonight I opened a second column. RELIT… eight lines, all yours."* |
| **C1** | Central · `penumbra_ring` | `flag:dawn` | People from the gone-quiet marsh villages, come to see whether the Spire is real | **Marsh-villager** (`script.peril_gone_quiet`): *"If you're going up there, we'll keep a lamp lit for you at the ring."* | dawn: *"We kept the lamp lit, and you came down in the morning."* |
| **P1** | Post-game · `dawnstead` | `flag:dawn` | The bookend | **Maudie** (`npc.peril_maudie_dawn`): *"His crater's gone and flowered… Worth the walk, if you've not been home."* | sends the player back to S1's payoff |

The thread is **weighted to the early game** (S1 is mandatory to *see*, because the satchel
errand runs through the orchard). It leans lighter as the spine's own peril set-pieces
take over (the drained Glowmoss site, Còr, Coldfog/Stillworks, the Great Null). It
deliberately skips places those set-pieces already own (Lowleaf's Còr letter, Cinderhead's
Lamp-down vigil, Coldfog's drained land).

## 3. Implementation (all data)

- **S1 (orchard)** is in its builder, [`tools/maps/build_duskapple_orchard.py`](../../../tools/maps/build_duskapple_orchard.py),
  which is the source of truth (re-run is deterministic). `apple_1` is removed. A
  `fallenstar_crater` decal (non-solid, inserted FIRST so the other objects draw over it) sits
  at (5,3). The `fallenstar_cinder_star` at (7,4) pairs with `vigil_star_shard`
  (`flag:dawn`). `apple_0/apple_2` swap between charred (`fallenstar_tree_charred`) and living
  versions on `flag:dawn`, as `burn_shoots`/`burn_bloom` do on `gleam:ember`/`flag:dawn`.
  Tamsin stands at (9,6). The first-sight band covers (20,8–9), the whole mouth.
- **The art** is four objects drawn in code ([`tools/maps/draw_fallenstar_objects.py`](../../../tools/maps/draw_fallenstar_objects.py)
  → `assets/tilesets/fallenstar/objects/` → `pack_objects.py`): `crater`, `crater_snow`,
  `cinder_star` and `tree_charred` (the served living tree's trunk under a drawn, burnt crown).
  The shared tile set stays frozen. Tile fills can't draw a strike (they square off into a
  patch that reads as a texture error), so the crater is one drawn decal.
- **E1–P1** are surgical adds to shipped maps via [`tools/maps/add_peril_thread.py`](../../../tools/maps/add_peril_thread.py),
  an idempotent, id-keyed upsert in the add_vigil_scars pattern. **Re-run it after rebuilding
  any of those maps.** Use `--check` to report drift without writing.
- **Words**: the `THE PERIL THREAD (R9)` blocks in `content/scripts.ts` and
  `content/dialogue.ts`, plus the LORE entry `fallen_stars` in `content/glossary.ts`. Each
  NPC is one placement running one script. Every stage is a single `say` guarded with
  `if_flag` and `unless_flag`, so exactly one stage plays (the `script.andrew_hint` pattern).
  To add a stage, splice a line with **both** guards set.
- **Swaps share footprint and solidity** (collision is flag-blind). The flowers and bundles
  are `solid:false`; the cinder/shard and dead/lit brazier pairs are both solid on the same
  rect; and the charred/living trees use the same walk-under crown.

## 4. Deferred South placements (Tinderwick / Pearlmoor are owned by other work)

The words exist; only the placements are outstanding:

| Map | id | at | sprite | ref | flags |
|---|---|---|---|---|---|
| `tinderwick` | `peril_neighbour` | a walkable tile beside the west hedge gap (the orchard mouth, near (1–3, 7–10)), facing the gap | `npc_old_woman` | `script.peril_tinderwick_neighbour` | none (the script stages itself) |
| `pearlmoor_quay` | `sign_peril_pearlmoor_board` | a harbour-side tile near the quay's lower landing, with a `sign` deco tile + `kind:'sign'` interact trigger | — | `sign.peril_pearlmoor_board` | none |

After placing them, re-run `audit_warps`/`audit_flow` on the map.

## 5. Validation hooks

- `tools/maps/add_peril_thread.py --check` reports *0 maps would change*.
- `audit_flow`, `audit_warps`, `validate_map` and `render_walkable --report-only` pass on all
  eight touched maps with no new warnings. The thread adds no orphans and no softlocks. In
  particular, the Sunvault brazier sits in the east pocket, because placing it by the gorge
  sealed a 5-tile orphan.
- `audit_region` and `audit_spatial` PASS (no warp or graph edits).
- No encounters and no money were added, so the balance gates are untouched.
