# Retro Map & Route Design — Research Report (2026-06)

> **What this is.** A research digest of how the cartridge-era masters actually built
> their maps, routes, dungeons, towns and world graphs — the GBC/GBA
> creature-collecting classics, the SNES top-down action-adventure, and SNES-era
> Final Fantasy — followed by a design-panel synthesis of what PixelKin adopts.
> Evidence includes **primary sources** (the community disassemblies of the Gen 1/3
> creature-collectors: real map dimensions, encounter rates, trainer sight data) and
> the standard analyses (the Light World grid studies, the Boss Keys dungeon-graph
> series, the FF6 *Reverse Design*).
>
> **Brand-name rule:** competitor names appear in THIS document only, as research
> citations. Everything that graduates into the binding rulebook
> ([`level-design.md`](./level-design.md)) is stated **by structure, never by brand**
> — and nothing here licenses copying a layout, name, or asset. See `VISION.md`.

---

## Part I — Findings

### 1. The screen is the design unit (and always was)

- **Gen 1 viewport = 10×9 walkable tiles; every Kanto map is an exact multiple of
  the screen** (Pallet 20×18 = 2×2 screens; Viridian 40×36 = 4×4; Route 3 = 7×2).
  **Gen 3 viewport = 15×10; every Hoenn map quantizes to 20-tile chunks.** The
  designers composed in screen units: a "place" is 1–2 screenfuls, a route is a
  ribbon of 4–7. (pret/pokered map constants; pret/pokeemerald layouts.json)
- A choke + its guarding trainer + the escape ledge always fit **one viewport**
  (max trainer sight 5 < half-screen 7): every threat is readable before it fires.
- Landmarks enter the viewport **at least one screen before they're reachable** —
  the goal telegraphs itself.
- The Hoenn region was literally **rotated 90° to suit the GBA's 3:2 screen** —
  the hardware viewport shaped the macro-geography, not just the rooms.
- ALttP builds its Light World as an **8×8 grid of 32×32-tile chunks**, hand-grouped
  into ~8–11 themed regions whose cores are ~2×2 chunks each; at 16×16 granularity
  **only 6 of 256 sub-chunks are unreachable**. Near-total navigability is what makes
  a map feel rich rather than corridor-like. (Overworld Overload, icewatergames)

### 2. Route grammar: the S-bend, the choke, the one-way valve

- **Routes are narrow, folded corridors.** Hoenn horizontal routes are 20 tiles
  tall (exactly 2 screens); the *walkable* lane inside is roughly one screen wide,
  snaking within tree/cliff borders that eat 4–8 tiles per side.
- **The S-bend multiplies perceived length.** The genre's first route performs
  **5 S-bends through 5 grass patches** — "it allows the Route to feel longer
  without physically making it longer." The most space-efficient first route in
  the era runs 3 S-bends, 2 mandatory grass patches, and only **12 tiles of tall
  grass on the forced path**. The era's weakest first route is the one with 1.5
  bends and mostly-mandatory grass. (Fantendo first-routes analysis)
- **Route anatomy alternates bulge → choke → bulge.** Open bulges hold the optional
  grass fields; 1–3-tile chokes hold the *mandatory* content (grass crossing,
  trainer, story trigger) because the player cannot route around a choke.
- **Ledges are one-way valves, one per S-bend.** Outbound you fight through grass;
  homebound you hop the ledges and skip nearly all of it. Variants: a loop inverted
  to compress the *outbound* leg; paired one-way lanes (an east-only upper passage
  + a west-only return); ledges as a temporary point-of-no-return that soft-locks
  backtracking until a traversal power arrives.
- **Trainer sight is short and legible: 2–3 tiles typical, 1–5 max** (primary data
  from the Gen 3 map JSON), facing fixed. Mandatory fight = sight spans the full
  choke (the famous 5-trainer one-lane bridge gauntlet); dodgeable fight = short
  line across a wide lane — slipping past is a reward for reading the map. Routes
  carry ~3–6 corridor trainers; the optional detours carry more.
- **Dead ends always pay** — an item ball, a TM, a rare patch, or an NPC gift.
  A dead end with nothing is a design fault in this genre.

### 3. Encounter pacing: the dial is rate × coverage

Primary numbers (per-step chance on encounter tiles, /256):

| Context | Rate | Coverage |
|---------|-----:|----------|
| First-route grass (Gen 1) | 25 (~10%/step) | five small dodgeable patches |
| Standard route grass (Gen 3) | 20 | flanking fields, lane clear |
| Long route / sparse desert | 15 / 10 | larger bands |
| Forest interior (floor is mostly grass) | **8** | wall-to-wall |
| Caves (every tile rolls) | **10** | wall-to-wall |
| Surf water (every tile rolls) | **4** | wall-to-wall |
| Safari/reserve zones | 25–30 | opt-in attraction |

- **Where encounter tiles are mandatory or wall-to-wall, the rate is halved or
  worse; where the terrain is optional and small, the rate runs high.** Pacing is
  rate × coverage, never rate alone.
- A mandatory crossing of ~6 tiles at ~10%/step yields **0–1 encounters** — one
  heartbeat encounter, not a wall.
- Encounter fatigue was a known failure (the era's caves are remembered as bat
  gauntlets); the shipped mitigations: the low cave rate, a purchasable repel
  item, and a heal at the dungeon mouth.
- By mid-game, **grass should be mostly optional** — forced grass is an opening-
  hour teaching tool, then it becomes opt-in levelling.

### 4. The region is the level: topology, gating, heal spacing

- **Topology: a main loop with stub spurs** — not a pure line, not a hub-web. The
  Gen 1 badge path is a circuit that ends by **arriving back at the starting town
  from a new direction** (by sea) — the era's strongest "the world is whole" beat.
  Each region keeps ONE earned four-way hub you pass near early and enter late.
- **Field-move gating is lock-and-key at world scale, and every key re-opens
  EARLIER maps**: the cut-tree shortcuts on already-visited routes, the surf
  shorelines you walked past in act 1, the boulder rooms inside old caves. The
  first region's gate objects are deliberately seeded on the very first routes so
  the player learns "powers re-value old ground" in hour one.
- **Return-trip compressors escalate in scale**: ledge hop (within a route) →
  cut-tree shortcut (within an act) → a two-screen tunnel reconnecting a mid-game
  route to an hour-one route → surf loops → flight. Each new power collapses an
  old walk *just as it would become tedious*.
- **One-way macro routes give journeys a direction flavour** (the downhill cycling
  road: a joyride southbound, a grind northbound).
- **Level-curve continuity is enforced by wild data, not signs**: adjacent maps
  overlap by 1–2 levels and step up ~2–4 per map; dungeons sit ~2 levels above
  the route that feeds them.
- **Heal spacing:** every town heals, and where the gap is too long the games drop
  a **free-standing roadside heal at the dungeon mouth**. Working rule: never more
  than ~2 routes + 1 dungeon from a heal; one immediately before every multi-floor
  cave.
- **ALttP's connective tissue**: themed region cores are joined by deliberate
  "pathway" zones with their own consistent look — the connectors are designed,
  not leftover. Gate with terrain that reads as world (ridges, trees, riverbanks);
  mix **hard gates** (binary item locks) with **soft gates** (crossable but
  inefficient) so cleverness has room. After the intro, **~60% of the map is
  visitable** — open most of the world early, lock a few corners hard.
- **FF's two-scale lesson**: the world map compresses travel so position stays a
  story indicator; vehicles are gating tiers (foot → ship → canoe → airship), and
  each tier **re-values terrain the player already saw** (rivers were scenery,
  then the canoe makes them roads). The map opens in acts; the strongest version
  makes the map itself a story beat (the mid-game world reshuffle).
- **Iteration evidence:** the Gen 3 developers *straightened* an early tunnel "to
  better serve the events that take place there" — story beats won over maze
  complexity; and a fixed, authored world beat the creator's original wish for
  randomly generated ones.

### 5. Dungeon grammar: graphs, floors, freedom that can't go wrong

- **Notate dungeons as lock-and-key graphs** (the Boss Keys vocabulary): rooms
  from entrance to boss; small keys above their locks; the dungeon item above the
  obstacles it answers. **Graph shape is the diagnostic — tall-and-narrow =
  linear; wide = real choice.** Sprawl is not nonlinearity: the mission graph
  reveals how little choice a sprawling floor plan may actually contain.
- **The big-key economy**: one prize that pays three ways (the big doors, the boss
  door, AND the chest holding the dungeon's traversal item). Small keys are local
  currency; the big key is the structural pivot.
- **Freedom without bad decisions**: optional offshoots are short and return the
  player to the main path; the best dungeons **loop back over their own rooms**
  with new knowledge rather than adding corridors; hidden shortcuts let players
  feel clever; rooms **teach, then test** (same enemy, harder configuration —
  ramp by layout, not by stat).
- **Multi-floor legibility**: explicit ladders/stairs; bridges that pass visibly
  *over* lower paths so one screen states the 3D relationship; drop-holes that
  land in a known room double as shortcuts and as spatial teaching. Keep vertical
  depth limited and legible.
- **Floor rhythm from the creature-collectors** (primary dimensions): big maze
  floor → small connector/decoy floor → big maze floor, ending in a designer
  set-piece; decoy ladders lead to single-room item pockets; a tower is just a
  cave with tiny floors (six 13×13 floors + a big summit). One landmark dungeon
  per region is *not* a maze at all — it confounds with sheer size or darkness
  instead.
- **Darkness is a comfort gate, not a wall** — the dark dungeon is trivial with
  the light-key and disorienting without it, but gropeable.
- **The wrong branch has treasure** (the FF convention): at any fork the dead-end
  branch carries a chest, so wrong turns always pay — and a visible chest *labels*
  a branch as the optional one. Risk-priced treasure (a great chest behind an
  over-band monster) is a legitimate spice.
- **The dungeon, not the battle, is the difficulty unit** (FF6 *Reverse Design*,
  the "Long Game"): encounter survivability is held nearly flat; difficulty is
  cumulative attrition of resources across the run, and **safe-room spacing is
  the pacing dial** — rest points sit before the hard room, mid-way through long
  runs, and before the boss. Critical path requires zero gated powers on first
  traversal; gated branches inside the dungeon pay the return visit.

### 6. Towns: the kit, the tiers, the mouth

- **Three size tiers, screen-quantized** (primary data): hamlet 20×18/20×20
  (2×2 screens, 2–4 houses + one plot building, often *no* shop/heal), standard
  town 40×36-ish (heal + shop + arena + 3–5 houses, one holding a utility NPC),
  metropolis (department store, attraction, condo blocks) — **one per region**.
- **The heal sits at the town mouth** — "weary trainers coming back from an
  adventure need a place to rest" on the arrival path, not buried. The SNES-JRPG
  phrasing: enter town, press up, walk into the inn.
- **Shops read at a glance** (the visible counter), clustered near the entrance.
- **Towns are never mazes** — crossing entrance→exit must be free of house-maze
  friction; the town is the safe zone.
- **No superfluous interiors**: every enterable building serves a purpose;
  unenterable facades are legitimate set-dressing; when unsure, smaller —
  **3–4 purposeful interiors** is a healthy fully-explorable footprint.
- **NPC irony** (FF6 *Reverse Design*): hints are delivered in-fiction as
  character speech, never as system text; tuck one reward-NPC away to pay nosing
  around; cut any NPC with nothing to add.
- **One town per region breaks the kit** for memorability (the raft town, the
  treehouse town, the hot-spring town) — and the break is structural, not just
  palette.
- **Map-building order from the era's practitioners**: terrain masses first
  (trees/mountains define the shape), then buildings, then paths — the same
  presence-grid-first order our mapkit already uses.

### 7. Visual language

- **One tile, one meaning**: cliff *face* = wall, plateau *top* = walkable, stairs
  are the only vertical verb; water/pits read by palette + border alone.
- **Biome colour-coding is a navigation instrument** — regions are identifiable
  at a glance from dominant palette currents.
- **Gating must be drawn**: the blocker is a visible object (the sleeping beast,
  the thirsty guards), "specified on your game map or at least implied" — players
  keep a mental tally of every visible blocker they pass.
- **Secrets telegraph**: the cracked wall, the odd tree, suspicious symmetry —
  a tease the player can't decode is noise. Almost every obstacle has multiple
  solutions; no single consumable is ever the only way in.
- **Composition disguises direction as freedom**: ridges, treelines and water do
  the railroading so the UI never has to.
- **The mirror-world trick**: reusing macro-geography with transformed landmarks
  + changed traversal buys second-act content from first-act maps — *if* the
  transformation changes traversal, not just palette. (PixelKin's relit-vs-drained
  area states are this lever.)

---

## Part II — Panel synthesis: what PixelKin adopts

The standing panel (three cartridge-era handheld RPG designers + the systems/UX
designer, per `level-design.md` §1) reviewed Part I against our built South region
and the binding rules. Verdicts:

**Already aligned (keep, no change):**
- Screen-unit composition (§0), diegetic gating (Fork B), tease-don't-block
  (Fork D), the structural principles (§3a), the composition standard (§11), the
  cliff top/face grammar, the SNES interior enclosure spec, hard-edged encounter
  tufts, NPC-delivered hints (our scripts already speak in-fiction).

**Adopted — new or sharpened rules (now binding; see level-design.md changelog):**
1. **Rate × coverage is the encounter dial** (sharpens Fork E): wall-to-wall
   terrains (cave floors, glowmoss, surf water) run at *half or less* the rate of
   small optional patches. Our flat 0.10–0.14 cave band was too hot next to the
   era's 10/256 ≈ 4%; caves and water get explicit lower bands.
2. **The S-bend rule** (new in §3a): fold the critical path 3–5 times per route
   map; straight-line distance is never the walked distance. Mandatory grass on
   the forced path stays small (≈6–12 tiles) — one heartbeat encounter per
   crossing.
3. **Level-band continuity is data** (new §2b): adjacent maps overlap 1–2 levels,
   step 2–4, dungeons +2 over their feeder route — now measured by
   `audit_region.py`.
4. **Heal-anchor spacing** (new §2b): never more than ~2 route legs + 1 dungeon
   from a rest-heal; a roadside rest belongs at every multi-floor dungeon mouth.
5. **Return compressors escalate in scale** (sharpens §3a rule 1): ledge → act
   shortcut → cross-region re-link → (late) the Lanternway as our flight-tier.
   Every Gift must re-open something on an *earlier* map, seeded before the Gift
   is earned.
6. **Dungeon graphs before dungeon tiles** (new in §2a): sketch the lock-and-key
   graph (keys above locks, target slightly-wide shape, one loop over the
   entrance) before carving floors; teach-then-test room ramps; the wrong branch
   has treasure; darkness is a comfort gate.
7. **Town mouth rule** (sharpens Fork C/§11 rule 5): the rest-heal building faces
   the main arrival entrance; shops cluster visibly near it; crossing the town is
   friction-free.
8. **Connector vocabulary** (new §2b): the transition zones between areas are
   designed pieces with their own consistent look — border-to-border terrain
   continuity at every warp seam.
9. **Open early, lock corners** (new §2b): after the opening, most of the region
   should be *visitable*; the locks worth keeping are few, visible, and named.
10. **One kit-breaker per region** (new §11 note): one town/area per region
    breaks the standard kit structurally — and only one.

**Considered and rejected:**
- *Forced movement corridors* (the downhill road): charming but needs a new
  engine verb; shelved until a region genuinely wants it.
- *A separate compressed world-map scale* (the FF lesson): our region graph +
  Lanternway hub already does the act-gating job at one scale; a second scale
  would fight the handheld idiom we sell.
- *Random encounter-free travel tier*: our Lamplight axis and charges cover the
  "friction-free when earned" need diegetically.

---

## Part III — What changed in the repo (2026-06)

- **`docs/world/level-design.md`**: added **§2b — The region is the level** (the
  scene-scale rules: topology, band continuity, heal spacing, connector seams,
  act gating); extended **§3a** with rules 11–14 (S-bend folding, rate×coverage,
  sight-legibility, dungeon-graph-first); updated Fork E's rate table; updated
  the §8 checklist; replaced the stale §9 scaffold with the built skill + audit
  stack.
- **`tools/maps/audit_flow.py`** (new): the executable §3a pass — reachability,
  choke-trigger integrity, free-pass detection, loop/return asymmetry, dead-end
  payoff, per-screen interest. Wired into `mk.finalize()`.
- **`tools/maps/audit_region.py`** (new): the scene auditor — graph.ts⇄JSON sync,
  Gift unlock waves, level-band cliffs, region topology, route leg lengths.
- **`tools/maps/worldmodel.py`** (new): the shared movement/portal/sight model
  (engine-faithful: ledges as directed hops, ability gates, object footprints,
  NPC bodies) + the graph.ts parser.
- **`tools/maps/mapkit.py`**: multi-tileset support — `register_tileset()` /
  `gid(name, set=…)` / `gid_at()` / `next_first_gid()` so areas can stack accent
  kits above the shared set.
- **`tools/maps/patterns.py`**: new stamps — `gift_tease` (the gated, signed,
  breadcrumbed promise), `cave_ladder` (floor-link halves, landing-on-mirror),
  `mandatory_band` (full-corridor crossing with the lane paused).
- **Four real bugs found by the new audits and fixed** (builders + rebuilt maps):
  Tinderwick's waxcake cache sealed in an unreachable pocket; a sign tile sealing
  Pearlmoor's entire west Lanternway spoke; the Tideglass cavern door with no
  standable approach tile; the `dusk_begins` and `glowmoss_drained` story beats
  walk-aroundable (now full-cut trigger bands with flag pairs).

## Sources

**Creature-collector side** (primary + analyses)
- pret/pokered — map constants & wild tables: <https://github.com/pret/pokered>
- pret/pokeemerald — layouts, map JSON (trainer sight), wild encounters: <https://github.com/pret/pokeemerald>
- "A short analysis of the first Routes (Gen I–IV)": <https://fantendo.fandom.com/wiki/User_blog:Shadow_Inferno/A_short_analysis_of_the_first_Routes_in_Pokemon_Games_(Gen_I-IV)>
- Satoshi Tajiri, TIME Asia interview (1999): <http://edition.cnn.com/ASIANOW/time/magazine/99/1122/pokemon6.fullinterview1.html>
- Tajiri 1997 interview (trans.): <https://lavacutcontent.com/satoshi-tajiri-1997-interview/>
- TCRF — Ruby/Sapphire early maps: <https://tcrf.net/Development:Pok%C3%A9mon_Ruby_and_Sapphire/Early_Maps>
- TheGamer route/region analyses (Rock Tunnel, Cycling Road, best routes, map ranking)
- PokéCommunity Daily mapping tutorials; Essentials Docs "Guide: Game design"
- Bulbapedia: Route 1 / Route 9 / Cycling Road / Diglett's Cave / Hoenn

**SNES action-adventure + JRPG side**
- "Overworld Overload" Pts 1–3 (Game Developer): the Light World grid analysis
- icewatergames — ALttP level-design analysis
- Mark Brown / GMTK "Boss Keys" (+ BorisTheBrave, "Lock and Key Dungeons": <https://www.boristhebrave.com/2021/02/27/lock-and-key-dungeons/>)
- Mike Stout, "Learning From The Masters" (Game Developer)
- Zelda Dungeon "Bridging the Gap"; Zelda Wiki (Dark World, Magic Mirror)
- *Reverse Design: Final Fantasy 6* (thegamedesignforum.com) — the "Long Game"
- zharth, "World Map and Game Flow in FF1"; FF Wiki (world map, save points)
- Goomba Stomp FF4 retrospective; rpgmaker.net town-design thread

*(Full URL list in the research agents' transcripts; caveats: a few sources were
excerpt-only due to fetch blocks; Gen 1 rate semantics are standard disassembly
knowledge.)*
