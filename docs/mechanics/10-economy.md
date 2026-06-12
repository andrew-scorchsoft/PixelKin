# PixelKin — Economy, Shops & Progression Budget

> The design for **wicks** (money), **shops**, **Star-charts** (taught moves),
> battle **XP/payout** tuning, and the **per-region battle & earnings budget**
> that keeps the locked level curve (walkthrough spine §4) reachable,
> challenging, and solvent. The executable twin of this doc is
> **`tools/balance/progression.mjs`** — a journey-long model of XP and wicks
> for three player profiles. **Any change to a number in this doc, in
> `src/game/content/economy.ts`/`items.ts`/`trainers.ts`, or to a region's
> battle roster must re-run that model and pass.**
>
> Status: the core systems here are **BUILT** (money, payouts, shop UI,
> Star-charts, catch XP, the faint tithe — schema v2); §10 lists what's
> designed-but-pending. The per-region budgets for East/North/West/Central are
> **design contracts** for those regions' authors.

## 1. The currency: wicks

**Wicks** — waxed, brass-capped lamp-wicks, bundled and traded. In a land
where night doesn't lift, everyone always needs one more; they're small,
stable in value, and burn the same in every valley. Tinderwick minted the
custom (and took its name from it). Diegetic, humble, and ours.

- Code: `SaveGame.money` (save schema v2), helpers in `content/economy.ts`.
- Display: `1,240w` (`formatWicks`) — shown in the ITEMS header and the shop
  counter; never a `$`/coin glyph.
- Voice: "wicks" lower-case in dialogue ("that'll be forty wicks, dear").
- A new Wayfarer starts with **250w** (`STARTING_WICKS`) — enough for two
  balms, not enough to skip the verge.

## 2. Where wicks come from

| Source | Amount | Notes |
|---|---|---|
| **Trainer payouts** | class rate × ace level (§4) | the backbone; wild battles pay **nothing** |
| **Named side quests** | per-region purse (§5 budget) | each region's 3+ quests; scaled to local prices |
| **Valuables** | Wax Cake 250w · Moth-amber 600w · Embergloss 600w · Starglass Shard 1,500w · Murk Pearl 1,500w | found in caches/Lamplight nooks, sold at any counter (Embergloss/Murk Pearl are Coldfog's drained-fen finds) |
| **Loose finds** | small `giveMoney` drops | a purse in a cache, festival thanks |
| **Selling items** | half price (`SELL_RATE 0.5`) | keepers buy anything priced; never key items |

And where they go (sinks): balms, lamps, **Star-charts** (the aspirational
sink), and the **faint tithe** — on a blackout the kind light keeps **10%** of
your wicks (`FAINT_TITHE_RATE`; narrated as thanks left at the hearth — losing
costs, gently). Inn/home rests stay **free** (canon hospitality); pressure
lives in consumables and charts, not in healing.

## 3. The price list (authoritative)

Prices live on `ItemDef.price` (`content/items.ts`); one price everywhere.

| Item | Effect | Price | First sold |
|---|---|---:|---|
| Tallow Balm | heal 20 | 120w | Tinderwick |
| Warm Balm | heal 60 | 500w | Pearlmoor |
| Bright Balm | full heal | 1,200w | Galehigh, once `gleam:storm` is held (Pale Vault keeps no counter) |
| Glow Charge | one throw, catch ×1.5 | 200w | Tinderwick |
| Beacon Charge | one throw, catch ×2.5 | 600w | everywhere, once `gleam:ember` is held (flag-gated stock) |
| Star-charts | teach a move | 800–4,000w by tier (§6) | everywhere |

**Catching reframed (2026-06):** the vesperlamp is a **key item** — one device,
plain throws free — and the purchasable line is **charges** (one boosted throw
each; `04-capture.md`). The old Vesperlamp/Bright/Radiant Lamp consumable rung
is retired; saves migrate (v3) old lamps into charges.

Quest charms (Tide Charm, Drift Charm, Wrecklight Charm, the Marsh Lamp —
E1's ×2.0 deep-growth conditional — the Aurora Charm and Sun Charm — N2's and
X2's ×2.5 conditionals on Frost-met / Solar-met kin — the caretaker's **Bright
Lamp** (X1, item id `caretaker_lamp`, an unconditional ×2.5), the Starlamp, and
the festival Glow Salve) have **no price** — unbuyable, unsellable, earned only. Now that status conditions run (Part B, BUILT), add
next: **Soothing Tea** (cure any status, ~200w) and **Rekindle Drop** (wake a
fainted kin at half health, ~900w) — add to this table + items.ts together.

## 4. Trainer payouts

`TrainerDef.payout`, authored to the formula **payout = class rate × ace
level** (the model's drift check recomputes built trainers):

| Class | Rate | Who |
|---|---:|---|
| route | 16w | wayfarers, couriers, shepherds on the lanes |
| keeper | 20w | wick-tenders, miners, acolytes — dungeon/loop posts |
| rival | 24w | Wren |
| warden | 60w | the eight Lampwardens |
| cor | 120w | Warden Còr |

So Brisa pays 600w, Reyl 960w, Lucan Pyre 2,760w and Nessa Cole 3,120w —
and a beaten region roughly funds its own shop tier plus one chart — the
model verifies exactly that.

## 5. Shops — how they look and work

**The counter (built — `ui/ShopMenu.ts`).** Talking to a keeper runs their
script: flavour line(s), then `{ op: 'shop', shop: '<id>' }` opens the
counter. Root menu **BUY / SELL / LEAVE**; BUY and SELL are full-screen
list + detail panes (the StarterSelect pattern): item rows with price and
held-count right-aligned, the selected item's description below, and the
wallet always in the header. **One Confirm trades one item** (tap-tap-tap to
stock up; the wallet counts along); unaffordable rows dim; B backs out.
Selling pays half price; valuables their `sell` value; key items never list.

**The data (built).** `ShopDef { id, name, stock: string[] }` in
`content/shops.ts`; prices come from the ItemDefs. The one-time **kit keeper**
pattern stays: kit script → flag → the *trading* keeper swaps in
(`script.shop_tinderwick`, `script.shop_pearlmoor` are the worked examples).
A new shop = a ShopDef + a keeper script + the NPC pair on the map.

**Per-region stocking plan (design contract).** Each Lumenary town's shop
carries: its tier of balm + charges (see §3 "first sold"), **the previous tier
too** (a struggling player can stock up cheap), and **2–4 Star-charts** —
the region's element pair + one Plain utility. Planned counters:

| Shop | New stock beyond the previous tier |
|---|---|
| Tinderwick General *(built)* | Tallow Balm, Glow Charge (+ Beacon Charge once `gleam:ember`), charts: Cinder Spit, Mist Spray |
| Pearlmoor Chandlery *(built)* | Warm Balm, Glow + Beacon Charges, charts: Wave Crash, Hearth Pulse, Gust Up, Focus Mind |
| Lowleaf provisioner *(built)* | charts: Spore Puff, Root Strike, Lifedrain |
| Cinderhead pit-stores *(built)* | charts: Focus Mind, Gust Up (no Stone chart minted yet) |
| Galehigh kite-stall *(built)* | Bright Balm (once `gleam:storm`), charts: Thunder Kick, Volt Arc, Gale Slam, Swift Step — **the whole cold leg's counter: Pale Vault deliberately keeps no shop** (resupply rides the Windward drop-shortcut); the find-first Tempest nuke chart is Thunderroost's prize |
| ~~Pale Vault warm-house~~ | — (no counter; see Galehigh row) |
| ~~Solarium dig-counter~~ | — **dropped (2026-06, built):** the Solarium is a ruin — the festival trades in bread and stories; the Lumenary green room is the rest point, no counter (the Pale Vault precedent) |
| ~~Nightreach last-counter~~ | — **dropped (2026-06, built):** the star-temple keeps a vigil, not a till; **the West ships no counter** — the Galehigh kite-stall (one hub-spoke away) remains the late counter, and the West's aspirational chart (Sunburst Nova, 4,000w tier) is the Helia Vault's find-first prize. The planned West charts may land on a Central/postgame counter instead |

## 6. Star-charts — the taught-move system

**Lore.** A **Star-chart** is a pressed chart of one small constellation
figure. A kin that studies it by lamplight learns to draw that figure in
battle. One study burns the chart's glow out — **single-use**, repurchasable
where sold. Sold by chandlers and chartwrights; the rarest are found, not
sold (a star-tender's hand-pressed originals). Never "TM/HM": traversal is
**Lantern Gifts** (player abilities, unrelated); moves are **charts**.

**Mechanics (built).** `ItemDef { category: 'chart', teach_move }`; used from
the ITEMS menu → pick a kin → learn. Compatibility (`KinInstance.canStudy`):
the kin **shares the move's type**, the move is **Plain**, or the move is
already in its species learnset (levelup/kindling/tutor). Already-known
refuses; a full moveset runs the shared **`ui/MoveLearnPrompt`** (the same
set-one-aside flow battle level-ups use — battle-runtime-plan Part A, shipped).
Giving up at the prompt leaves the chart **unspent**.

**The pool & pricing tiers.** Charts draw from the 125-move pool (wave 2 —
both channels now run full ladders per type); signature moves are **never**
printed as charts (they belong to one line):

| Tier | Power band | Price | Where |
|---|---|---:|---|
| early | Quick/Light (40–60) | 800–900w | South |
| mid | Standard (75–80), key status | 1,200–1,400w | South–East |
| late | Heavy (90–95), strong utility | 2,200–2,400w | North–West |
| end | Nuke (110+) | 4,000w | Nightreach/post-Crown **found or one-stock** |

Nuke charts (Tempest, Sunburst Nova, Eclipse Wave, Maelstrom…) are
**find-first**: landmark/Lamplight rewards, with at most one late counter
stocking one. Heavy/Nuke charts are why late optional content pays.

**Wave 2 — DONE (2026-06).** The pool grew 94 → **125** through the pipeline
(`gen_moves.py`): a light-physical (58) and heavy-special (92) per type
(symmetric, so the chart's empirical balance held — fair-roster spread
47.8–53.2% after, vs the same-tier roster signal unchanged from baseline),
plus **11 apex signature moves** owned by the Constellation Wardens +
Keylumen/Nullmajor/Dawnbrael (`build_species.py SIGNATURE_MOVES`, learned
L44–52; excluded from the generic sim pools so they shape only their owners).
Learnsets were rebuilt band-aware (richer mid-game kits, no more nuke-at-31).
Still deferred: a second status move per type — wait for the status engine
(Part B), since the simulator can't cost status yet.

## 7. XP & the level dynamic (tuned by the model)

Engine formulas (`KinInstance.ts`, `BattleScene.ts`):

- exp to reach level L = **L³**; stats re-derive from level (no EV/IV).
- yield per defeated kin = **bst × level / 20** — *retuned from the
  first-slice /60, which left the curve unreachable (−18 levels by the
  climax on any sane battle count)*.
- **Trainer battles pay ×1.5 XP** (the genre's raised-kin bonus).
- **A catch pays the same XP as a knock-out** — collecting is the game's
  heart and must keep you *on* the curve, not punish you off it.
- XP goes to the **active battler only**. The model's `leadShare` schedule
  encodes the consequence: south/east players raise fresh catches (lead gets
  ~45–55% of XP), north onward the core team is set (70–100%). If we ever add
  an XP-share, re-tune the divisor down.

**Model results (2026-06, all checks passing):**

| Checkpoint | rec | ace | rusher | mainline | explorer |
|---|--:|--:|--:|--:|--:|
| Ember Gleam (Brisa) | 10 | 10 | L11 | L11 | L13 |
| Tide Gleam (Reyl) | 12 | 16 | L16 | L16 | L18 |
| Verdant Gleam (Sable) | 18 | 22 | L22 | L21 | L24 |
| Stone Gleam (Otho) — *the wall* | 26* | 28 | L28 | L27 | L31 |
| Storm Gleam (Mira) | 28 | 34 | L32 | L32 | L35 |
| Frost Gleam (Ysolde) | 36 | 40 | L38 | L37 | L41 |
| Solar Gleam (Lucan) | 42 | 46 | L43 | L42 | L46 |
| Lunar Gleam (Nessa) | 48 | 52 | L48 | L48 | L52 |
| Warden Còr (climax) | 54 | 56 | L52 | L53 | L57 |

\* post-Descent-Vigil expectation; §4 entry rec is 22 (the wall by design).

**The difficulty shape this buys** — early Gleams land at/above ace (gentle
on-ramp); from Mira onward the mainline player fights wardens **2–4 levels
under the ace** (the "you have to work for it" middle); the climax lands 3
under Còr with the explorer barely above him. Stretch beats stay stretch
(Otho, Wren A4 at/above player, the Spire); breathing room stays (arrival
towns, festivals, post-Gleam backtracks).

## 8. The per-region battle & earnings budget (binding)

The JOURNEY table in `progression.mjs` is the contract; summarised:

| Region | Trainer battles (class mix) | Wild fights (mainline) | Quest wicks | Valuables |
|---|---|--:|--:|---|
| South *(built + breakwater pair)* | 9 — 4 route, 3 keeper, 1 rival, 2 warden | ~29 | 750w | Wax Cake |
| East *(fen + Lowleaf built)* | 12 — 3 route, 7 keeper, 2 warden | ~36 | 1,550w | Moth-amber ×2 |
| North | 13 — 6 route, 4 keeper, 1 rival (A4), 2 warden | ~21 | 1,600w + finds | Moth-amber ×2 |
| West *(built)* | 12 — 7 route, 2 keeper, 1 rival (A5), 2 warden | ~21 | 1,100w + finds | Starglass ×4 + Moth-amber ×3 (Coldfog's Embergloss/Murk Pearl ride the optional detour) |
| Central *(built)* | 6 — 5 keeper (acolytes), Còr | ~10 (set-piece catches + spoke top-ups; no wild zones past the hub) | 0w quests + 1,400w finds (the quest pay is item-shaped: Radiant Lamp ×3.5, Way-lamp, the Lampling) | Starglass ×2 + Moth-amber |

Rules for region authors:

1. **Every route segment ships 2–3 sight trainers; every earned loop 2; every
   dungeon floor-run 2–3.** Trainers are the curve's spine *and* the wallet's
   income — a quiet route under-levels AND impoverishes.
2. **Trainer levels track the §4 band top**, kin count grows 1–2 (routes) →
   2 (dungeons) → 4–5 (wardens); wardens' aces are fixed by the spine.
3. **Each region's income ≈ its core kit + one chart + ~20% buffer.** The
   model enforces solvency; if a region adds spending, add quest wicks or a
   valuable, not a payout-rate change.
4. **1–2 mandatory grass crossings per route** (existing level-design rule)
   supply the wild-fight floor the rusher column relies on.

## 9. Tuning rules — when the game changes (binding)

- **Add/move/resize an area, add trainers, change bands** → update the
  JOURNEY leg in `progression.mjs`, re-run. Under-curve? Add trainers or
  raise a band *within* §4 (never re-pin a warden's ace casually). Over-curve?
  Trim optional grass XP (encounter rate), not trainer beats.
- **Change a price/payout/start purse** → mirror in `economy.ts`/`items.ts` ↔
  `PRICES`/`PAYOUT_RATE`/`BUILT_PAYOUTS` in the model, re-run.
- **Change the XP formula** → tune in the model first, then mirror into
  `BattleScene.expYield` (the engine comment points back here).
- **Make the game bigger** (a new optional region, post-game): post-Crown
  content keys off the *Dawnstead 55–65* band; charts tier "end" and Starglass
  valuables are the levers — payout classes don't grow past `cor`.
- **Invariants the model fails on:** mainline within −1/+4 of every rec;
  rusher ≥ rec−3; explorer ≤ ace+4; every wallet ≥ 0 on the planned kit;
  built payouts on formula; chart tiers ascend; chart moves exist.

## 10. Implementation status

**Built (this change):** `SaveGame.money` + v1→v2 migration · payouts +
"earned N wicks" in BattleScene · faint tithe in blackout · ShopMenu +
`shop`/`giveMoney` ops · Tinderwick + Pearlmoor live counters · 6 chart items
+ ItemsMenu study flow + `KinInstance.canStudy/learnMove/replaceMove` ·
catch XP + trainer ×1.5 + /20 yield · wallet in ITEMS header · glossary
entries (Wicks, Star-chart) · `tools/balance/progression.mjs`.

**Built (wave 2 follow-up, 2026-06):** the 125-move pool + apex signatures
(§6) · the move-learn prompt (`ui/MoveLearnPrompt`, shared by level-ups and
charts — Part A shipped).

**Designed, pending:** status cures + Rekindle Drop (needs battle-runtime
Part B) · buy-quantity picker (nice-to-have; single-tap works) · a **Loretender**
NPC (recall a forgotten learnset move for wicks — the late-game wick sink,
suggest the Hearthkeeper's counterpart at the Crossroads) · a second status
move per type (after Part B) · East→Central shop data (per §5 table, as each
region is built).
