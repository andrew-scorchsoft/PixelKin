# PixelKin — W7 Expert Panel: The West Region

> A convened, independent review of PixelKin's newly built **West quadrant** —
> the sunset quadrant, the threshold of the endgame (commits `08af46d..fbc8c5f`):
> Hushfrost Pass I→II + Aurora Hollow, Sunken Solarium (+ Lumenary), Sunvault
> Climb I→II + Helia Vault, Nightreach Observatory (+ Lumenary/inn/home), the
> Coldfog Marches I→II detour (+ Drownlight Beacon + Hollowfen Stillworks), the
> W5 content layer, the W6 encounter mirror, the crossroads spoke + R5 delivery.
> Judged against the binding acceptance specs: `walkthrough/04-west.md` (every
> hook + staging + §10 voice), the spine README §0/§5 (Gleam shapes 7 & 8 + the
> standing kit), `level-design.md` §2a/§2b/§3a/§11, `interiors.md`,
> `cinematics.md`, `story-bible.md` §7, `10-economy.md` §4, the humour style
> sheet. The North panel's findings discipline is the floor.

## The panel

| Panelist | Discipline | Watches for |
|----------|------------|-------------|
| **Devs "Dee" Okonkwo** | Level & world design | the four-register contrast arc, ring-circuit flow, choke integrity |
| **Tomás Reic** | Narrative & quest design | the seven-lamp escalation, B4 dread, Còr-tone firewall, humour calibration |
| **Mara Holloway** | Systems & balance | the +4 warden delta, the band ladder, encounter tables, economy |
| **Ivo Castellan** | Producer / first-time player | the endgame threshold, "can the player actually finish," vision-alignment |

## How it was run

Evidence was *gathered, not assumed*: all 16 West maps + the crossroads
re-rendered and eyeballed against §11/§3a; `audit_region` / `audit_flow` (all 16)
/ `audit_warps` run and read critically; `progression.mjs` + `validate.mjs` run
for the balance verdict; **three quest chains traced flag-by-flag setter-to-consumer
across map JSON + TS** (the Lit Stage, the full Vigil of the Seven, the X1
caretaker incl. the postgame dawn-swap); the fog-road sequence-break claim verified
in geometry + flag logic; the entire West scripts/dialogue block read as prose; and
an **exhaustive grep of the whole repo** for the crown/hub flag setters.

---

## Part 1 — The audit (what's working, keep it)

1. **The four visual registers land, and the contrast arc reads as a whole.**
   Hushfrost is a frozen blue-grey ache (ice crystals, snowpatch grass, lonely
   lamp-posts); the Solarium is flooded gold (a domed sun-temple, the three Lit-Stage
   braziers, Tidecall flood-pools, bone columns, sun-flowers — real warmth after the
   cold); Coldfog is genuinely *drained* (desaturated grey-green murk, snuffed
   null-lanterns, lightless pools, one creeping edge of gold the fog hasn't taken
   yet); Nightreach is bone-and-deepblue star-temple (brass-telescope dome, the seven
   watch-lamp posts of the Astral Walk, star-chart signboards, the densest starfield
   in the game). Frozen → gold → grey → star-blue. **Dee:** "This is the strongest
   register-to-register journey in the game. Coldfog as the deliberate held-dark
   counter-image is the masterstroke — it makes the rim's warmth *mean* something."

2. **The west ring-circuit is real and `audit_region` PASSES.** "region 'west':
   8 nodes, circuit closes through the outer ring via hushfrost_pass_i,
   hushfrost_pass_ii, nightreach_observatory, sunken_solarium, sunvault_climb_i,
   sunvault_climb_ii." All 16 `audit_flow` runs PASS (0 failures, 0 design warnings);
   `audit_warps` PASS with only the *pre-existing South-town* border warnings (no West
   map flagged). Reachability, chokes, free-pass, dead-ends, screens — all clean.

3. **The band ladder 40→52 is continuous and the +4 warden delta is the right rung.**
   `progression.mjs` PASSES. Lucan ace 46 vs predicted checkpoint L42 (rusher L43 /
   mainline L42 / explorer L46) = **+4**; Nessa ace 52 vs L48 (L47–L52) = **+4**. The
   North panel established the escalating delta as a *feature* (Brisa −1 … Mira/Ysolde
   +2 … Lucan/Nessa +4). The brief's worry that the precedent might break is unfounded:
   +4 is the correct top rung — the two hardest, most haunted wardens in the game.
   **Mara:** "The delta escalates smoothly all the way to the climax. Don't touch it.
   Lucan 46 met at ~44–45, Nessa 52 met at ~50–51 — both winnable, both a wall."

4. **The Lit Stage chain (Chain A) is airtight and tighter than spec.** Traced
   flag-by-flag: `lucan_quest`→`q_west_stage` reveals mote-1; mote-1→reveals brazier-1
   (sets `q_west_brazier_1`)→reveals mote-2; …→brazier-3→`q_west_stage_lit`→reveals the
   Lucan bond-test (req `q_west_stage_lit`, `blocked_ref: npc.lucan_not_ready`). The
   brazier *ordering* is enforced through the **mote-pickup gating** (mote-2 requires
   `q_west_brazier_1`), which is even stricter than the spec's "brazier requires
   previous brazier." No sequence break possible. The Lucan trainer carries
   `reward_flags:['gleam:solar']` + `reward_abilities:['sunsketch']`. Clean.

5. **The full Vigil of the Seven (Chain B) is the best-wired ceremony in the game,
   and the fog-road sequence-break CANNOT corrupt it.** The chain:
   `pickup_striker`(`req:None`, on sunvault_climb_ii) → `picked_striker` →
   `west_lamp_1`(req `picked_striker`) → lamp_2(req lamp_1) → … → `fenn_counsel`(lamp_5,
   C4) → `wren_nightreach`(lamp_6, A5) → `great_null_named`(lamp_7, B4) sets
   `q_west_lamp_7 + q_west_vigil_kept + great_null_known + q_west_vigil`. Each lamp hard-
   requires the previous with a `blocked_ref` in voice; Nessa's bond-test
   (`lumenary_nightreach`) hard-requires `q_west_vigil_kept` (`blocked_ref:
   npc.nessa_not_ready`). **The W4 "harmless deviation" claim VERIFIES:** a player
   arriving via the Coldfog back-door cannot reach Nessa's battle without
   `q_west_vigil_kept`, which back-chains all the way to `picked_striker` — and the
   striker sits behind the Sunsketch gate on sunvault_climb_ii. `q_west_vigil` (set by
   Nessa's hook) is purely cosmetic (hides the hook NPC); the lamps key on
   `picked_striker`, not it — so even skipping the hook is harmless. The C4/A5/B4
   embedments, the `if_flag:flag:q_north_ribbon_placed` (Wren's N3 ribbon callback) and
   the `if_flag:flag:seen_stillworks` (Nessa's "you've walked the Hollowfen" reinforce)
   are per-step guards that degrade silently. **Tomás:** "Seven lamps, seven regions
   remembered, and the staging *is* the climax run-up. Nothing in the game is wired
   this carefully."

6. **The X1 caretaker chain (Chain C) AND its postgame dawn-swap are integrity-clean.**
   `caretaker_quest`→`q_west_caretaker` reveals the aurora-oil cache (req
   `q_west_caretaker`, in the Emberward-gated Aurora Hollow)→`picked_aurora_oil`→
   `caretaker_done`(req `picked_aurora_oil`)→`q_west_caretaker_done` + Bright Lamp. The
   **dawn-swap pair** is correct: object `hushfrost_numbed_kin_awake`(req `flag:dawn`)
   ↔ `hushfrost_numbed_kin`(hidden `flag:dawn`) at the **same footprint (17,22), same
   (non-)solidity** — exactly the "swap pair MUST share footprint+solidity" rule; the
   examine-line trigger pair mirrors it. The kin *sleeps easier in the light* now and
   *wakes only at dawn* — the B-arc weight is kept, as the spec demands.

7. **The Coldfog Còr-tone discipline is clinically clean — zero humour, the hooks'
   lines verbatim.** The whole Coldfog block carries a source comment "ZERO humour in
   this whole block; the register is elegiac, merciful-and-wrong." The husk-keeper line
   is verbatim from the hooks ("Every lamp in here is sleeping, not dead. That's the
   horror of it — and the mercy he believes in."); the marsh-hermit verbatim ("They
   didn't burn it. They didn't break it. They just... turned the light down… Kindest
   thing, they said. Kindest thing."). The Stillworks B4 set-piece is `silence`-heavy,
   ends on "the gauge… rests at zero… because zero, here, is the finished number," and
   even the cache pickups carry the grief ("whoever they were for is long past needing
   them," "left ready for a morning that never came," "took them — gently"). The
   Hollowing's own signs are *courteously* awful ("The Wardens of the Quiet ask that you
   not wake them"). **Tomás:** "The firewall is total. Grief at industrial scale, never
   a cackle. This is how you write a sympathetic apocalypse."

8. **The seven lamp remembrances escalate and each region's voice rings true.** Ember =
   Tinderwick's hearths ("the colour of home"); Tide = Pearlmoor's bell ("tides go out
   so they can come back. You have been coming back ever since"); Verdant = Lowleaf's
   moss ("be like the moss"); Stone = Cinderhead's vigil ("anyone can LIGHT a lamp;
   carrying one is the trick of the whole thing"); Frost = Pale Vault's ice (Fenn's C4);
   Storm = Galehigh's kites (Wren's A5); Solar = the Solarium's stage (Nessa's B4). They
   *build*: "Four of seven. Past the halfway… you had not realised, until now, that you
   were checking each one." The B4 naming is grave, with the cold tint on "aimed at the
   Keystar" landing exactly as cinematics.md asks. **The best-written sequence in the
   game to date — a half-step above North's Còr/Fenn/Wren cluster.**

9. **The two Lumenary interiors are DISTINCT — West avoided North's MIN-1.** Lucan's
   hall reads theatrical/warm (red banners, hung triple-lantern focal, a costume rack,
   stage crates); Nessa's reads astronomer (blue banners, a brass telescope on a plinth
   as the focal piece, a blue-flame star-brazier). Both use the correct cool-stone
   register and the proper `aisle_runner`. Per-warden identity, exactly to interiors.md.

10. **The Helia Vault is a real Sunsketch puzzle micro-dungeon, not a locked room.**
    The render shows sequential-bloom ledges joined by sun-vine bridges + ladders, a
    sun-mirror dish redirect, terminating in the gold reliquary (a STAR-CHART: SUNBURST
    NOVA). `audit_flow`: 7 triggers all reachable. The spec's "promote it from a plain
    locked room to a puzzle" was honoured.

11. **Encounter tables respect §3a r12 and the X3 leg-3 is truly optional.** Solarium
    garden bands 0.11, mandatory crossing lanes **0.05** (half-rate), Tidecall water
    halls 0.07. The tables carry a proper weight ladder (16→14→…→3) — the brief's "flat
    no-common" worry doesn't hold; there *is* a clear common (kin 114 @ w16, kin 105 @
    w18 on crossings). X3 `chart_done` keys on `q_west_chart_2` (legs 1+2) only — the
    Coldfog survey-cairn leg (chart_3) stays optional, as BUILT. `validate.mjs`: 0/0 on
    162 species; W6 sync added the West maps to `CURATED_AREAS` honestly.

12. **The Last-Warm-Day pivot is the tonal turn the region needs.** "Daylight saved
    all season, spent all at once, on purpose, together… Nobody asks if you have earned
    it. That is the whole custom: warmth, spent freely, knowing it fades." It quietly
    rebukes the Hollowing *before* you see the Stillworks — the Arc-D cold→warm pivot,
    fire-warm swell after the coldest regions. Sanctioned humour is present and well-homed
    (the Hushfrost sign "The Pass Committee thanks you for not testing this" — bathos in
    officialdom, one wry note per region).

---

## Part 2 — Findings ledger

### BLOCKER

- **BLK-1 — The Crown never closes and the hub never opens: `flag:crown_west`,
  `flag:crown_north`, `flag:crown_east`, and `flag:hub_unlocked` are NEVER SET anywhere
  in the repo. The game cannot be completed.**
  *Evidence:* an exhaustive grep across `src/`, `tools/`, and all map JSON for any
  *assignment* of these four flags (`setFlag`, `reward_flags`, `: true`) returns **only
  `crown_south`** (hand-set on both South wardens: `trainers.ts:25,252`). `crown_east`,
  `crown_north`, `crown_west`, `hub_unlocked` have **zero setters**. Every region's
  source comments promise the opposite — "the ENGINE derives flag:crown_east"
  (`trainers.ts:288`), "with Storm already held the ENGINE closes flag:crown_north"
  (`trainers.ts:518`), "the ENGINE derives crown_west + hub_unlocked (last quadrant)"
  (`scripts.ts:2332`, `trainers.ts:722`) — **but that derivation code does not exist.**
  `applyBattleResult` (`WorldScene.ts:729`) only applies `result.set_flags` (the literal
  `reward_flags`) and `grant_abilities`; `FlagStore.setMany` does no derivation; there is
  no boot-time reconcile, no gleam→crown pass, nothing. Nessa grants only
  `['gleam:lunar']`; Lucan only `['gleam:solar']`; Otho only `['gleam:stone']`; Ysolde
  only `['gleam:frost']`.
  *Consumers left stranded:* `vesper_crossroads → penumbra_ring` is
  `requires_flag:flag:hub_unlocked` (`graph.ts:250`); the `umbral_spire` node is
  `unlocked_by_flag:flag:hub_unlocked` (`graph.ts:144`); the four hub spokes are gated on
  `opens_flag: crown_east/north/west` (`graph.ts:258–260`). With no setter, **beating
  Nessa lights `gleam:lunar` but the Penumbra Ring, the Umbral Spire, and the four-way hub
  all stay permanently sealed** — the West's own §0 trap 3 ("`crown_west` and
  `hub_unlocked` BOTH fire at Nightreach") fails, and the hand-off to Central is a dead
  wall. typecheck is clean, so nothing flags it at build.
  *Why West owns it:* this is a cross-region engine gap (North/East shipped with their
  crowns equally orphaned — the prior panels missed it because nothing downstream of
  `crown_north`/`crown_east` was reachable yet to expose it). **West is the milestone that
  surfaces it:** W5's commit literally claims "WEST COMPLETE, all eight Gleams earnable"
  → the Crown completing and `hub_unlocked` firing is the *entire point* of the eighth
  Gleam, and Central C1 (Penumbra Ring/Starwell) now sits behind the dead gate. This must
  be fixed before West can be called complete.
  *Fix (small, one place):* add a derived-flag pass that runs whenever a gleam flag is
  set — the natural home is right after `this.flags.setMany(result.set_flags)` in
  `applyBattleResult` (mirrored on any other gleam-setting path / on save-load for
  robustness). For each quadrant, if both its gleams are held, set the crown; if all four
  crowns are held, set `hub_unlocked`. Map: South = ember+tide, East = verdant+stone,
  North = storm+frost, West = solar+lunar. Then **remove the redundant hand-set
  `crown_south`** from the two South wardens so the single derivation owns all four (or
  leave it — idempotent — but document that South is the legacy double-set). Re-run the
  four balance gates + a manual Nessa-win check that `penumbra_ring` opens. *(Note: this
  is logic, not a type/lint error, which is exactly why CI is green and the bug is
  invisible to the gates — see MIN-1 for the test that would have caught it.)*

### MAJOR
*(none)*

### MINOR

- **MIN-1 — No test/gate asserts the crown-derivation invariant, so BLK-1 ships green.**
  *Evidence:* CI runs typecheck + the four balance gates; none model flag derivation, so
  a completed-but-unwinnable game passes every check. *Fix:* add a tiny progression
  assertion (in `progression.mjs` or a new `validate_flags.mjs`) that simulates "hold all
  eight gleams → expect `hub_unlocked` derivable," and one per quadrant. Cheap insurance
  against the exact class of bug BLK-1 is, and it would have caught North's and East's
  latent versions too. Wire it into `.github/workflows/checks.yml`.

- **MIN-2 — Hushfrost Pass I is a 60-step leg and Sunvault Climb II is 62 — the region's
  two longest, both unbroken by a heal.** *Evidence:* `audit_region` travel:
  `hushfrost_pass_i ≈60`, `sunvault_climb_ii ≈62`, `sunken_solarium ≈55`,
  `hushfrost_pass_ii ≈51`. The Solarium green-room rest sits *after* Hushfrost (≈111 steps
  of route before the first West heal); the Climb's down-ledges cut II to 31 the fast way
  (good) but the *first up-traverse* is long. `level-design.md` §2b wants heal spacing
  ≈2 legs. The audit PASSES (the band is gentle and the ledges fold II), so this is
  pacing, not a bug. *Fix:* none required; if a future pass wants headroom, seed a
  one-line crag-NPC or a cache rest-beat near the Hushfrost I midpoint and the Sunvault II
  pre-Helia ledge. Lower priority than North's 93-step Windward I (which this is already
  better than).

- **MIN-3 — A stray placeholder-look glyph in the Sunken Solarium render.** *Evidence:*
  `/tmp/w7/sunken_solarium.png` bottom-right carries a small yellow square with a face —
  an `item_cache` placeholder sprite that didn't resolve to its art in the render. Likely
  a missing/served-name mismatch on one cache object; harmless in-engine (the script
  fires) but it reads as "unfinished" on the map. *Fix:* confirm the cache's `sprite`
  key maps to a packed object; if it's the generic item_cache placeholder, that's
  consistent with other regions (cosmetic only) — verify it's intended, else point it at
  the proper served sprite.

### POLISH

- **POL-1 — The two Lumenary halls still share the same furniture *shell* (bookcase +
  apothecary shelf + two benches + round table), differing only in focal piece + banners.**
  *Evidence:* `/tmp/w7/sunken_solarium_lumenary.png` vs `/tmp/w7/nightreach_lumenary.png`.
  This is a *far* milder version of North's MIN-1 — the focal pieces (hung lanterns vs
  brass telescope) and banner colours genuinely differentiate them, so it's identity-
  present, not copy-paste. *Fix (optional):* one more per-warden prop swap each (a
  star-globe for Nessa, a prop-trunk for Lucan) would push them from "distinct" to
  "unmistakable." Not required.

- **POL-2 — The seven Astral-Walk watch-lamps render identically lit in the static
  capture.** *Evidence:* `/tmp/w7/nightreach_observatory.png` shows all seven posts the
  same. The lit/unlit state is runtime flag-driven (`q_west_lamp_*`), so this is a render
  artefact, not a build issue — but worth a note that the *unlit* art variant exists and
  swaps correctly (the chain proves it does). No action.

### PRAISE
*(carried in Part 1; the standouts: the four-register contrast arc, the un-breakable
Vigil chain with the verified fog-road safety, the seven-lamp remembrance escalation, the
total Coldfog Còr-tone firewall, and the two genuinely distinct Lumenary halls.)*

---

## Part 3 — The three weakest things (mandatory)

1. **The Crown/hub flags are never set (BLK-1).** Not a polish item — the single fact
   that takes the region from "ship-ready" to "rework the one-line derivation first." The
   eighth Gleam is *supposed* to complete the Crown and open the endgame, and right now it
   does neither, because the "engine derives it" code that four regions' comments promise
   was never written. Everything else in the West is excellent; this is the one wall.

2. **The missing derivation has no test, so it shipped invisibly through green CI
   (MIN-2/MIN-1).** The deeper weakness behind BLK-1: the gates model *balance* but not
   *progression reachability*, so a literally-uncompletable game passes every check. The
   roster's selling point is that it's empirically validated; the *journey* deserves the
   same one-line invariant.

3. **The two longest legs (Hushfrost I ≈60, Sunvault II ≈62) run without a heal beat
   (MIN-2).** The one place the moment-to-moment risks "long" — the first West route and
   the pre-Helia climb. The art and encounter variety carry it (and the audit passes), but
   it's the softest pacing in an otherwise tight region; a single mid-leg rest-beat each
   would close the gap to the §2b ideal.

---

## Part 4 — Verdict & consistency check

**Verdict: FIX-THEN-SHIP.** One BLOCKER (BLK-1, the crown/hub derivation), and it is a
*small, localized* fix — a single derived-flag pass in `applyBattleResult` plus removing
or documenting the legacy `crown_south` double-set, guarded by a one-line progression test
(MIN-1). Everything else in the West is the best work in the game: the chains are
airtight, the fog-road safety verifies, the four registers are the strongest contrast arc
to date, the seven-lamp sequence out-writes North's character peak, and the Còr-tone
firewall is total. **The region is content-complete and creatively ship-ready; it is
mechanically blocked on a one-place engine gap that the West milestone is the first to
expose.** Fix BLK-1, add the test, and this ships at the top of the regional bar.

**What West did better than South/East/North:**
- **The contrast arc.** Four distinct registers in one quadrant, with Coldfog as a
  deliberate held-dark counter-image — a level of thematic art-direction the earlier
  regions (single-register each) never attempted.
- **The capstone chain craft.** The Vigil of the Seven is wired tighter than North's
  Lamp-Line, *and* the sequence-break vector (the fog back-door) was anticipated and
  proven harmless in the flag logic — not just asserted.
- **The narrative peak.** The seven-lamp remembrances are a half-step above North's
  Còr/Fenn/Wren cluster: the game remembering *itself*, region by region, is a payoff only
  the last quadrant could earn, and it's executed with restraint.
- **Lumenary identity.** West shipped two *distinct* halls; North shipped two near-
  identical ones (North's MIN-1). Lesson learned and applied.

**What South/East/North did better:**
- **Shippability out of the box.** South/East/North each shipped SHIP-READY with no
  blocker; West is the first region gated on an engine fix — albeit an inherited,
  region-agnostic one that the prior panels should arguably have caught (their crowns were
  equally unset, just not yet downstream of anything reachable).
- **Heal-leg spacing.** South's legs sat nearest the §2b ideal; West's two longest legs
  (MIN-2) run a touch long, though still shorter than North's 93-step Windward I.

*All panelist names are original personas standing in for handheld-RPG disciplines, per
VISION.md — described by craft and era, never by any existing studio or person.*
