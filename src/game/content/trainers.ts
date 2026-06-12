/**
 * Trainer registry — authored opponents (rivals, Lampwardens). Adding a trainer
 * is a data edit here, never engine code. Each entry maps to a `BattleRequest`
 * of kind 'trainer' by id (see BattleScene). Intro/defeat lines are supplied as
 * dialogue here so a trainer fight is self-contained (the BattleScene reads
 * `getTrainer(id)` and `getTrainerLines(ref)` rather than the world DialogueRegistry).
 *
 * First Lumenary: Brisa Tallow, the Lampwarden of Tinderwick (Ember). Beating
 * her relights the first constellation — the player earns the Ember Gleam and the
 * 'crown_south' progression flag.
 */
import type { DialogueLine, TrainerDef, TrainerRegistry } from './types';

export const TRAINERS: TrainerRegistry = {
  lampwarden_tinderwick: {
    id: 'lampwarden_tinderwick',
    name: 'BRISA TALLOW',
    title: 'Lampwarden',
    party: [
      { species_id: 10, level: 7 }, // Tallowpup — Ember
      { species_id: 18, level: 10 }, // Hearthkit — Ember (ace ~10 per walkthrough/01-south)
    ],
    intro_ref: 'trainer.lampwarden_tinderwick.intro',
    defeat_ref: 'trainer.lampwarden_tinderwick.defeat',
    reward_flags: ['gleam:ember'], // crown_south now DERIVES in FlagStore — never hand-set
    payout: 600, // Lampwarden 60 × ace 10
    music: 'battle-emberfall',
    ai: 'smart', // Lampwardens play the matchup, not just the biggest number
  },

  // The Beacon ascent (Tinderwick): Brisa's wick-tenders hold the stair floors —
  // SIGHT trainers pitched between the coast road (~6) and Brisa's ace 10, so the
  // climb itself is the on-ramp to the bond-test.
  beacon_keeper_a: {
    id: 'beacon_keeper_a',
    name: 'TANSY',
    title: 'Wick-tender',
    party: [
      { species_id: 16, level: 7 }, // Wickmoth — Ember
    ],
    payout: 140, // keeper 20 × ace 7
    music: 'battle-emberfall',
  },
  beacon_keeper_b: {
    id: 'beacon_keeper_b',
    name: 'COLE',
    title: 'Wick-tender',
    party: [
      { species_id: 10, level: 7 }, // Tallowpup — Ember
      { species_id: 16, level: 8 }, // Wickmoth — Ember
    ],
    payout: 160, // keeper 20 × ace 8
    music: 'battle-emberfall',
  },

  // A2 — Wren's first FRIENDLY battle on Dimglass Coast I (walkthrough/01-south §2):
  // teaches trainer battles in a low-stakes, cosy frame, pitched ~2 levels under the
  // player (~7 at the second grass beat). No reward flags — the route trigger tracks it.
  wren_dimglass: {
    id: 'wren_dimglass',
    name: 'WREN',
    title: 'Wayfarer',
    party: [
      { species_id: 8, level: 5 }, // Glimflit — Light
      { species_id: 26, level: 6 }, // Brinelet — Tide
    ],
    intro_ref: 'trainer.wren_dimglass.intro',
    defeat_ref: 'trainer.wren_dimglass.defeat',
    payout: 144, // rival 24 × ace 6
    music: 'battle-emberfall',
  },

  // Dimglass Coast II route trainers — the XP bridge between the Ember Gleam (~10)
  // and Pearlmoor (rec. 12): two travelling Wayfarers on the tidal flats.
  flats_wayfarer_a: {
    id: 'flats_wayfarer_a',
    name: 'MORROW',
    title: 'Wayfarer',
    party: [
      { species_id: 26, level: 9 }, // Brinelet — Tide
      { species_id: 31, level: 9 }, // Lumpin — Tide/Light
    ],
    intro_ref: 'trainer.flats_wayfarer_a.intro',
    defeat_ref: 'trainer.flats_wayfarer_a.defeat',
    payout: 144, // route 16 × ace 9
    music: 'battle-emberfall',
  },
  flats_wayfarer_b: {
    id: 'flats_wayfarer_b',
    name: 'ELSPETH',
    title: 'Lamp-courier',
    party: [
      { species_id: 27, level: 10 }, // Brineroll — Tide
      { species_id: 31, level: 11 }, // Lumpin — Tide/Light
    ],
    intro_ref: 'trainer.flats_wayfarer_b.intro',
    defeat_ref: 'trainer.flats_wayfarer_b.defeat',
    payout: 176, // route 16 × ace 11
    music: 'battle-emberfall',
  },

  // Glowmoss Deep (East) — the first cave dungeon's SIGHT keepers (dungeon
  // keeper class, 10-economy §4), pitched to the walkthrough's ~20 rec. band:
  // the on-ramp between Sable Quill's ace 22 and the Cinderhead galleries.
  glowmoss_keeper_a: {
    id: 'glowmoss_keeper_a',
    name: 'DELL',
    title: 'Moss-tender',
    party: [
      { species_id: 56, level: 19 }, // Sporeling — Verdant
      { species_id: 57, level: 20 }, // Sporemid — Verdant (ace)
    ],
    payout: 400, // keeper 20 × ace 20
    music: 'battle-emberfall',
  },
  glowmoss_keeper_b: {
    id: 'glowmoss_keeper_b',
    name: 'MIRREL',
    title: 'Deepwood Warden',
    party: [
      { species_id: 65, level: 20 }, // Glowsip — Verdant/Light
      { species_id: 67, level: 21 }, // Fennlight — Verdant/Light (ace)
    ],
    payout: 420, // keeper 20 × ace 21
    music: 'battle-emberfall',
  },

  // Saltreach Fen I route trainers — the 16→18 on-ramp between Pearlmoor and
  // the Lowleaf cluster (route class, 10-economy §4).
  fen_wader_a: {
    id: 'fen_wader_a',
    name: 'MARIGOLD',
    title: 'Fen-wader',
    party: [
      { species_id: 59, level: 16 }, // Dewling — Verdant/Tide
      { species_id: 27, level: 17 }, // Brineroll — Tide (ace)
    ],
    payout: 272, // route 16 × ace 17
    music: 'battle-emberfall',
  },
  fen_courier_b: {
    id: 'fen_courier_b',
    name: 'OSPREY',
    title: 'Plank-courier',
    party: [
      { species_id: 31, level: 17 }, // Lumpin — Tide/Light
      { species_id: 60, level: 18 }, // Poolfrond — Verdant/Tide (ace)
    ],
    payout: 288, // route 16 × ace 18
    music: 'battle-emberfall',
  },

  // Saltreach Fen II — the deep channels' one route trainer: the reed-line
  // lamplighter who keeps the lantern-reeds (the 17→18 top of the fen ramp).
  reed_lamplighter: {
    id: 'reed_lamplighter',
    name: 'TARN',
    title: 'Reed-lamplighter',
    party: [
      { species_id: 31, level: 17 }, // Lumpin — Tide/Light
      { species_id: 59, level: 18 }, // Dewling — Verdant/Tide (ace)
    ],
    payout: 288, // route 16 × ace 18
    music: 'battle-emberfall',
  },

  // Lowleaf Hollow — the forest-fringe lane's two bloom-warden SIGHT trainers
  // (keeper class, 10-economy §4): the 19–21 on-ramp to Sable's ace 22, posted
  // on the fen-wood lane so the Tended Bed errand walks through them.
  bloom_warden_a: {
    id: 'bloom_warden_a',
    name: 'IVY',
    title: 'Bloom-warden',
    party: [
      { species_id: 56, level: 19 }, // Sporeling — Verdant
      { species_id: 65, level: 20 }, // Glowsip — Verdant/Light (ace)
    ],
    payout: 400, // keeper 20 × ace 20
    music: 'battle-emberfall',
  },
  bloom_warden_b: {
    id: 'bloom_warden_b',
    name: 'FERN',
    title: 'Bloom-warden',
    party: [
      { species_id: 38, level: 20 }, // Mossglow — Light/Verdant
      { species_id: 67, level: 21 }, // Fennlight — Verdant/Light (ace)
    ],
    payout: 420, // keeper 20 × ace 21
    music: 'battle-emberfall',
  },

  // E2 "Spores for the Stall" — the cross Sporeling squatting on the third
  // spore cache in Glowmoss Deep. A wild heart in a trainer's frame (the
  // scripted-battle pattern); it pays no wicks — it is not a person.
  spore_squatter: {
    id: 'spore_squatter',
    name: 'CROSS SPORELING',
    party: [
      { species_id: 56, level: 21 }, // Sporeling — Verdant, cross as a wet cat
    ],
    music: 'battle-emberfall',
  },

  // Pearlmoor breakwater — the Causeway Bell loop's two net-hand SIGHT trainers
  // (route class, 10-economy §4): the 12→14 on-ramp between arrival (~12) and
  // Reyl's ace 16, posted so the causeway crossing is mandatory.
  net_hand_a: {
    id: 'net_hand_a',
    name: 'MAREN',
    title: 'Net-hand',
    party: [
      { species_id: 26, level: 12 }, // Brinelet — Tide
      { species_id: 31, level: 12 }, // Lumpin — Tide/Light (ace)
    ],
    intro_ref: 'trainer.net_hand_a.intro',
    defeat_ref: 'trainer.net_hand_a.defeat',
    payout: 192, // route 16 × ace 12
    music: 'battle-emberfall',
  },
  net_hand_b: {
    id: 'net_hand_b',
    name: 'COB',
    title: 'Net-hand',
    party: [
      { species_id: 31, level: 13 }, // Lumpin — Tide/Light
      { species_id: 27, level: 14 }, // Brineroll — Tide (ace)
    ],
    intro_ref: 'trainer.net_hand_b.intro',
    defeat_ref: 'trainer.net_hand_b.defeat',
    payout: 224, // route 16 × ace 14
    music: 'battle-emberfall',
  },

  // Second Lumenary: Reyl Wash, the Lampwarden of Pearlmoor Quay (Tide) — an old
  // ferryman. Beating him relights the Tide constellation: the player earns the Tide
  // Gleam AND the Tidecall Lantern Gift (granted via reward_abilities). 'crown_south'
  // is set once both Ember + Tide are held, so it's listed here too (the FlagStore
  // ignores a re-set, and a player can reach Pearlmoor before clearing Tinderwick).
  lampwarden_pearlmoor: {
    id: 'lampwarden_pearlmoor',
    name: 'REYL WASH',
    title: 'Lampwarden',
    party: [
      { species_id: 26, level: 12 }, // Brinelet — Tide
      { species_id: 31, level: 13 }, // Lumpin — Tide/Light
      { species_id: 27, level: 14 }, // Brineroll — Tide
      { species_id: 24, level: 16 }, // Shimmral — Tide/Light (ace)
    ],
    intro_ref: 'trainer.lampwarden_pearlmoor.intro',
    defeat_ref: 'trainer.lampwarden_pearlmoor.defeat',
    reward_flags: ['gleam:tide'], // crown_south now DERIVES in FlagStore — never hand-set
    reward_abilities: ['tidecall'],
    payout: 960, // Lampwarden 60 × ace 16
    music: 'battle-emberfall',
    ai: 'smart', // Lampwardens play the matchup, not just the biggest number
  },

  // Third Lumenary: Sable Quill, the Lampwarden of Lowleaf Hollow (Verdant) —
  // a shy botanist whose glowmoss vouches where she won't speak. Beating her
  // relights the Verdant constellation AND grants Glimmerstep. NOTE: she does
  // NOT carry 'crown_east' — the quadrant crown rides the warden reward_flags
  // pattern (South's worked example), and East is strictly linear, so the
  // crown lands on Otho Grist (the SECOND East Gleam) when Cinderhead builds.
  lampwarden_lowleaf: {
    id: 'lampwarden_lowleaf',
    name: 'SABLE QUILL',
    title: 'Lampwarden',
    party: [
      { species_id: 56, level: 18 }, // Sporeling — Verdant
      { species_id: 59, level: 19 }, // Dewling — Verdant/Tide
      { species_id: 65, level: 20 }, // Glowsip — Verdant/Light
      { species_id: 66, level: 22 }, // Lumournis — Verdant/Light (ace)
    ],
    intro_ref: 'trainer.lampwarden_lowleaf.intro',
    defeat_ref: 'trainer.lampwarden_lowleaf.defeat',
    reward_flags: ['gleam:verdant'],
    reward_abilities: ['glimmerstep'],
    payout: 1320, // Lampwarden 60 × ace 22
    music: 'battle-emberfall',
    ai: 'smart', // Lampwardens play the matchup, not just the biggest number
  },

  // Fourth Lumenary: Otho Grist, Lampwarden of Cinderhead Mine (Stone) — the
  // curve's one deliberate WALL (§4: rec ~26 after the Descent Vigil vs ace 28).
  // A bulk team (roof, not rush): high def/hp Stone that punishes a glass cannon.
  // His win relights the Stone constellation AND, as East's SECOND Gleam, the
  // engine derives flag:crown_east (the warden reward_flags pattern, South's
  // worked example — Stone grants NO Lantern Gift, so no reward_abilities).
  lampwarden_cinderhead: {
    id: 'lampwarden_cinderhead',
    name: 'OTHO GRIST',
    title: 'Lampwarden',
    party: [
      { species_id: 48, level: 25 }, // Rubbol — Stone
      { species_id: 46, level: 26 }, // Voltcrag — Stone/Storm
      { species_id: 69, level: 27 }, // Riddlestone — Stone
      { species_id: 55, level: 28 }, // Ferrolith — Stone (ace, the wall)
    ],
    intro_ref: 'trainer.lampwarden_cinderhead.intro',
    defeat_ref: 'trainer.lampwarden_cinderhead.defeat',
    reward_flags: ['gleam:stone'],
    payout: 1680, // Lampwarden 60 × ace 28
    music: 'battle-emberfall',
    ai: 'smart',
  },

  // The two vigil-miner SIGHT trainers in Cinderhead Deep (keeper class) — they
  // hold the Descent Vigil's chamber leg, the §4 gap-closer made mandatory.
  gallery_miner_a: {
    id: 'gallery_miner_a',
    name: 'DRUSE',
    title: 'Vigil Miner',
    party: [
      { species_id: 47, level: 24 }, // Pebbit — Stone
      { species_id: 49, level: 25 }, // Gravelo — Stone (ace)
    ],
    intro_ref: 'trainer.gallery_miner_a.intro',
    defeat_ref: 'trainer.gallery_miner_a.defeat',
    payout: 500, // keeper 20 × ace 25
    music: 'battle-emberfall',
  },
  gallery_miner_b: {
    id: 'gallery_miner_b',
    name: 'HOBB',
    title: 'Vigil Miner',
    party: [
      { species_id: 45, level: 25 }, // Sparkrat — Stone/Storm
      { species_id: 48, level: 26 }, // Rubbol — Stone (ace)
    ],
    intro_ref: 'trainer.gallery_miner_b.intro',
    defeat_ref: 'trainer.gallery_miner_b.defeat',
    payout: 520, // keeper 20 × ace 26
    music: 'battle-emberfall',
  },

  // ===========================================================================
  // THE NORTH (walkthrough/03-north) — Galehigh's terraces and skyloft, the
  // Windward Stair, Pale Vault's undercroft, the A4 rival battle, and the two
  // cold-leg Lampwardens. Bands per the spine §4: Galehigh 28–31, Windward
  // 34–36, undercroft 37–39; aces Mira ~34, Ysolde ~40, Wren A4 at/above the
  // player (~41 — the ONE rival fight that breaks "Wren ~2 under you").
  // ===========================================================================

  // Galehigh's terrace lane — two route sight trainers (28–30).
  galehigh_kitehand: {
    id: 'galehigh_kitehand',
    name: 'PERRIN',
    title: 'Kite-hand',
    party: [
      { species_id: 88, level: 28 }, // Sparrowcaw — Storm
      { species_id: 97, level: 29 }, // Thrumvane — Storm (ace)
    ],
    intro_ref: 'trainer.galehigh_kitehand.intro',
    defeat_ref: 'trainer.galehigh_kitehand.defeat',
    payout: 464, // route 16 × ace 29
    music: 'battle-emberfall',
  },
  galehigh_terracer: {
    id: 'galehigh_terracer',
    name: 'SORREL',
    title: 'Terrace-farmer',
    party: [
      { species_id: 91, level: 29 }, // Cirruff — Storm/Light
      { species_id: 45, level: 30 }, // Sparkrat — Stone/Storm (ace)
    ],
    intro_ref: 'trainer.galehigh_terracer.intro',
    defeat_ref: 'trainer.galehigh_terracer.defeat',
    payout: 480, // route 16 × ace 30
    music: 'battle-emberfall',
  },

  // The skyloft's two wind-ward SIGHT keepers (the Kite-Rising loop's posts,
  // keeper class, 29–31 — the on-ramp to Mira's 34).
  skyloft_ward_a: {
    id: 'skyloft_ward_a',
    name: 'TAMSIN',
    title: 'Wind-ward',
    party: [
      { species_id: 97, level: 29 }, // Thrumvane — Storm
      { species_id: 98, level: 30 }, // Thrumble — Storm (ace)
    ],
    intro_ref: 'trainer.skyloft_ward_a.intro',
    defeat_ref: 'trainer.skyloft_ward_a.defeat',
    payout: 600, // keeper 20 × ace 30
    music: 'battle-emberfall',
  },
  skyloft_ward_b: {
    id: 'skyloft_ward_b',
    name: 'BRAN',
    title: 'Wind-ward',
    party: [
      { species_id: 91, level: 30 }, // Cirruff — Storm/Light
      { species_id: 89, level: 31 }, // Flintbeak — Storm (ace)
    ],
    intro_ref: 'trainer.skyloft_ward_b.intro',
    defeat_ref: 'trainer.skyloft_ward_b.defeat',
    payout: 620, // keeper 20 × ace 31
    music: 'battle-emberfall',
  },

  // Fifth Lumenary: Mira Vael, Lampwarden of Galehigh Terraces (Storm) — the
  // breathless kite-flier; a fast, adrenaline-keyed team met at ~30–31. Win
  // relights the Storm constellation AND grants the Updraft Kite (the warden
  // reward pattern). crown_north waits on Ysolde — never hand-set here.
  mira_vael: {
    id: 'mira_vael',
    name: 'MIRA VAEL',
    title: 'Lampwarden',
    party: [
      { species_id: 98, level: 30 }, // Thrumble — Storm
      { species_id: 95, level: 31 }, // Glacewing — Storm/Frost
      { species_id: 89, level: 32 }, // Flintbeak — Storm
      { species_id: 90, level: 34 }, // Strikeaven — Storm (ace, THE storm-bird)
    ],
    intro_ref: 'trainer.mira_vael.intro',
    defeat_ref: 'trainer.mira_vael.defeat',
    reward_flags: ['gleam:storm'],
    reward_abilities: ['updraft_kite'],
    payout: 2040, // Lampwarden 60 × ace 34
    music: 'battle-nightfall',
    ai: 'smart',
  },

  // The Windward Stair's three route sight trainers (34–36).
  windward_craghand: {
    id: 'windward_craghand',
    name: 'EDDA',
    title: 'Crag-hand',
    party: [
      { species_id: 45, level: 34 }, // Sparkrat — Stone/Storm
      { species_id: 89, level: 35 }, // Flintbeak — Storm (ace)
    ],
    intro_ref: 'trainer.windward_craghand.intro',
    defeat_ref: 'trainer.windward_craghand.defeat',
    payout: 560, // route 16 × ace 35
    music: 'battle-emberfall',
  },
  windward_galewatch: {
    id: 'windward_galewatch',
    name: 'ROWAN',
    title: 'Gale-watch',
    party: [
      { species_id: 98, level: 34 }, // Thrumble — Storm
      { species_id: 95, level: 35 }, // Glacewing — Storm/Frost (ace)
    ],
    intro_ref: 'trainer.windward_galewatch.intro',
    defeat_ref: 'trainer.windward_galewatch.defeat',
    payout: 560, // route 16 × ace 35
    music: 'battle-emberfall',
  },
  windward_cragwatch: {
    id: 'windward_cragwatch',
    name: 'MERLE',
    title: 'Crag-watch',
    party: [
      { species_id: 89, level: 35 }, // Flintbeak — Storm
      { species_id: 94, level: 36 }, // Hailwhirr — Storm/Frost (ace)
    ],
    intro_ref: 'trainer.windward_cragwatch.intro',
    defeat_ref: 'trainer.windward_cragwatch.defeat',
    payout: 576, // route 16 × ace 36
    music: 'battle-emberfall',
  },

  // A4 — Wren's wobble at the undercroft door: the HARD rival battle, at/above
  // the player's level by design (the one beat that breaks "Wren ~2 under you"
  // — do not "correct" it). Kindled line + a North catch; no reward flags
  // beyond the route trigger's bookkeeping (the script sets the battled flag).
  wren_pale_vault: {
    id: 'wren_pale_vault',
    name: 'WREN',
    title: 'Wayfarer',
    party: [
      { species_id: 9, level: 39 }, // Glimscout — Light (Glimflit, kindled)
      { species_id: 95, level: 39 }, // Glacewing — Storm/Frost (a North catch)
      { species_id: 28, level: 41 }, // Brinewrath — Tide (Brinelet's apex, the ace)
    ],
    intro_ref: 'trainer.wren_pale_vault.intro',
    defeat_ref: 'trainer.wren_pale_vault.defeat',
    payout: 984, // rival 24 × ace 41
    music: 'battle-veil',
    ai: 'smart',
  },

  // The undercroft's two frost-ward SIGHT keepers (the Lamp-Line's posts,
  // keeper class, 37–39 — the on-ramp to Ysolde's 40).
  undercroft_ward_a: {
    id: 'undercroft_ward_a',
    name: 'SELA',
    title: 'Frost-ward',
    party: [
      { species_id: 72, level: 37 }, // Glaceling — Frost
      { species_id: 84, level: 38 }, // Hushbore — Frost (ace)
    ],
    intro_ref: 'trainer.undercroft_ward_a.intro',
    defeat_ref: 'trainer.undercroft_ward_a.defeat',
    payout: 760, // keeper 20 × ace 38
    music: 'battle-emberfall',
  },
  undercroft_ward_b: {
    id: 'undercroft_ward_b',
    name: 'ORRIN',
    title: 'Frost-ward',
    party: [
      { species_id: 81, level: 38 }, // Blizzrhare — Frost
      { species_id: 84, level: 39 }, // Hushbore — Frost (ace)
    ],
    intro_ref: 'trainer.undercroft_ward_b.intro',
    defeat_ref: 'trainer.undercroft_ward_b.defeat',
    payout: 780, // keeper 20 × ace 39
    music: 'battle-emberfall',
  },

  // Sixth Lumenary: Ysolde Frost, Lampwarden of Pale Vault Glacier (Frost) —
  // the serene glaciologist; a patient chill-keyed team met at ~38–39. Win
  // relights the Frost constellation AND grants Emberward; with gleam:storm
  // already held the ENGINE derives flag:crown_north (never hand-set).
  ysolde_frost: {
    id: 'ysolde_frost',
    name: 'YSOLDE FROST',
    title: 'Lampwarden',
    party: [
      { species_id: 72, level: 36 }, // Glaceling — Frost
      { species_id: 81, level: 37 }, // Blizzrhare — Frost
      { species_id: 84, level: 38 }, // Hushbore — Frost
      { species_id: 95, level: 38 }, // Glacewing — Storm/Frost
      { species_id: 87, level: 40 }, // Prismantus — Light/Frost (ace — the light that holds)
    ],
    intro_ref: 'trainer.ysolde_frost.intro',
    defeat_ref: 'trainer.ysolde_frost.defeat',
    reward_flags: ['gleam:frost'],
    reward_abilities: ['emberward'],
    payout: 2400, // Lampwarden 60 × ace 40
    music: 'battle-nightfall',
    ai: 'smart',
  },

  // ===========================================================================
  // THE WEST (walkthrough/04-west) — Hushfrost Pass, the Sunken Solarium's Lit
  // Stage, the Sunvault Climb, and Nightreach's Vigil of the Seven. Bands per
  // the spine §4: Hushfrost 40–42, Solarium 42–46 (Lucan ace 46), Sunvault
  // 46–48, Nightreach 48–52 (Nessa ace 52). Coldfog keeps NO trainers by
  // design — nobody posts a road through a drained land.
  // ===========================================================================

  // Hushfrost Pass — three route sight trainers on the cold leg (40–42).
  hushfrost_lampman: {
    id: 'hushfrost_lampman',
    name: 'DUNSTAN',
    title: 'Coldfog Lampman',
    party: [
      { species_id: 84, level: 41 }, // Hushbore — Frost
      { species_id: 78, level: 41 }, // Crystarn — Frost (ace)
    ],
    intro_ref: 'trainer.hushfrost_lampman.intro',
    defeat_ref: 'trainer.hushfrost_lampman.defeat',
    payout: 656, // route 16 × ace 41
    music: 'battle-emberfall',
  },
  hushfrost_survivor: {
    id: 'hushfrost_survivor',
    name: 'HESPER',
    title: 'Pass Survivor',
    party: [
      { species_id: 82, level: 42 }, // Vortexlope — Frost/Storm (ace)
    ],
    intro_ref: 'trainer.hushfrost_survivor.intro',
    defeat_ref: 'trainer.hushfrost_survivor.defeat',
    payout: 672, // route 16 × ace 42
    music: 'battle-emberfall',
  },
  hushfrost_thawtender: {
    id: 'hushfrost_thawtender',
    name: 'TILDA',
    title: 'Thaw-tender',
    party: [
      { species_id: 75, level: 42 }, // Geodrake — Frost/Stone
      { species_id: 87, level: 42 }, // Prismantus — Light/Frost (ace)
    ],
    intro_ref: 'trainer.hushfrost_thawtender.intro',
    defeat_ref: 'trainer.hushfrost_thawtender.defeat',
    payout: 672, // route 16 × ace 42
    music: 'battle-emberfall',
  },

  // The Solarium's two troupe-player SIGHT trainers working the flooded lanes
  // (route class — festival players, not dungeon posts; 43–45).
  troupe_player_a: {
    id: 'troupe_player_a',
    name: 'CALLA',
    title: 'Troupe Player',
    party: [
      { species_id: 114, level: 43 }, // Sunsprout — Verdant/Solar
      { species_id: 117, level: 44 }, // Helibud — Solar (ace)
    ],
    intro_ref: 'trainer.troupe_player_a.intro',
    defeat_ref: 'trainer.troupe_player_a.defeat',
    payout: 704, // route 16 × ace 44
    music: 'battle-emberfall',
  },
  troupe_player_b: {
    id: 'troupe_player_b',
    name: 'ORSINO',
    title: 'Troupe Player',
    party: [
      { species_id: 115, level: 44 }, // Solvyne — Verdant/Solar
      { species_id: 120, level: 45 }, // Dawnfawn — Solar/Verdant (ace)
    ],
    intro_ref: 'trainer.troupe_player_b.intro',
    defeat_ref: 'trainer.troupe_player_b.defeat',
    payout: 720, // route 16 × ace 45
    music: 'battle-emberfall',
  },

  // Seventh Lumenary: Lucan Pyre, Lampwarden of the Sunken Solarium (Solar) —
  // the Last-Warm-Day's theatrical ringleader; warm, grandiose, deeply kind.
  // Fought ON the relit Heliarium stage (the bond-test trigger requires
  // flag:q_west_stage_lit). Win relights the Solar constellation AND grants
  // Sunsketch. crown_west waits on Nessa — never hand-set here.
  lucan_pyre: {
    id: 'lucan_pyre',
    name: 'LUCAN PYRE',
    title: 'Lampwarden',
    party: [
      { species_id: 117, level: 42 }, // Helibud — Solar
      { species_id: 115, level: 43 }, // Solvyne — Verdant/Solar
      { species_id: 104, level: 44 }, // Goldmane — Solar/Stone
      { species_id: 121, level: 44 }, // Sunstag — Solar/Verdant
      { species_id: 123, level: 46 }, // Solreach — Solar (ace — the stage lead)
    ],
    intro_ref: 'trainer.lucan_pyre.intro',
    defeat_ref: 'trainer.lucan_pyre.defeat',
    reward_flags: ['gleam:solar'],
    reward_abilities: ['sunsketch'],
    payout: 2760, // Lampwarden 60 × ace 46
    music: 'battle-nightfall',
    ai: 'smart',
  },

  // The Sunvault Climb's two route sight trainers (46–48).
  sunvault_terracer: {
    id: 'sunvault_terracer',
    name: 'BEL',
    title: 'Terrace-tender',
    party: [
      { species_id: 115, level: 46 }, // Solvyne — Verdant/Solar
      { species_id: 121, level: 47 }, // Sunstag — Solar/Verdant (ace)
    ],
    intro_ref: 'trainer.sunvault_terracer.intro',
    defeat_ref: 'trainer.sunvault_terracer.defeat',
    payout: 752, // route 16 × ace 47
    music: 'battle-emberfall',
  },
  sunvault_skywatcher: {
    id: 'sunvault_skywatcher',
    name: 'TAM',
    title: 'Sky-watcher',
    party: [
      { species_id: 126, level: 47 }, // Lunveil — Light/Lunar
      { species_id: 118, level: 48 }, // Helicore — Solar (ace)
    ],
    intro_ref: 'trainer.sunvault_skywatcher.intro',
    defeat_ref: 'trainer.sunvault_skywatcher.defeat',
    payout: 768, // route 16 × ace 48
    music: 'battle-emberfall',
  },

  // Nightreach's two junior-watcher SIGHT keepers on the Astral Walk
  // (keeper class, 49–51 — the on-ramp to Nessa's 52).
  junior_watcher_a: {
    id: 'junior_watcher_a',
    name: 'LIRA',
    title: 'Junior Watcher',
    party: [
      { species_id: 106, level: 49 }, // Drowshorn — Lunar
      { species_id: 127, level: 50 }, // Lunvane — Light/Lunar (ace)
    ],
    intro_ref: 'trainer.junior_watcher_a.intro',
    defeat_ref: 'trainer.junior_watcher_a.defeat',
    payout: 1000, // keeper 20 × ace 50
    music: 'battle-emberfall',
  },
  junior_watcher_b: {
    id: 'junior_watcher_b',
    name: 'OS',
    title: 'Junior Watcher',
    party: [
      { species_id: 112, level: 50 }, // Nightwraith — Lunar
      { species_id: 125, level: 51 }, // Crystalune — Lunar/Frost (ace)
    ],
    intro_ref: 'trainer.junior_watcher_b.intro',
    defeat_ref: 'trainer.junior_watcher_b.defeat',
    payout: 1020, // keeper 20 × ace 51
    music: 'battle-emberfall',
  },

  // A5 — Wren returns RESOLVED at lamp 6 of the Astral Walk: the warm mirror
  // of A4. Easy again, ~2 under the player by design (the A2 register back,
  // tempered) — one friendly bout for the road's sake before the last lamp.
  wren_nightreach: {
    id: 'wren_nightreach',
    name: 'WREN',
    title: 'Wayfarer',
    party: [
      { species_id: 9, level: 49 }, // Glimscout — Light
      { species_id: 96, level: 49 }, // Frigalance — Storm/Frost (the North catch, kindled)
      { species_id: 28, level: 50 }, // Brinewrath — Tide (the ace, as ever)
    ],
    intro_ref: 'trainer.wren_nightreach.intro',
    defeat_ref: 'trainer.wren_nightreach.defeat',
    payout: 1200, // rival 24 × ace 50
    music: 'battle-veil',
    ai: 'smart',
  },

  // A6 — Wren at peace in Dawnstead (walkthrough 06-postgame): the OPTIONAL,
  // re-runnable post-game rematch, offered never forced ("loser buys the
  // lanterns"). Friendly capstone at the lv55-65 rematch band — his arc team
  // grown, plus the sun-bright Wickmoth he caught in the verge this morning.
  // No reward flags, no progression gate; script.wren_rematch re-runs forever.
  wren_rematch: {
    id: 'wren_rematch',
    name: 'WREN',
    title: 'Wayfarer',
    party: [
      { species_id: 9, level: 58 }, // Glimscout — Light (his first, kept out of love)
      { species_id: 16, level: 59 }, // Wickmoth — Ember (the day-form catch, sun-bright)
      { species_id: 96, level: 60 }, // Frigalance — Storm/Frost (the North line, kindled)
      { species_id: 28, level: 62 }, // Brinewrath — Tide (the ace, as ever)
    ],
    intro_ref: 'trainer.wren_rematch.intro',
    defeat_ref: 'trainer.wren_rematch.defeat',
    payout: 1488, // rival 24 × ace 62
    music: 'battle-veil',
    ai: 'smart',
  },

  // Eighth Lumenary: Nessa Cole, Lampwarden of Nightreach Observatory (Lunar)
  // — the quiet insomniac astronomer, the most powerful and most haunted
  // Warden. A contemplative dreamlight team built around doze pressure (lull
  // + patient walls); met at ~50–51 after the Vigil of the Seven. Win relights
  // the Lunar constellation AND grants Starreach; with gleam:solar already
  // held the ENGINE derives flag:crown_west AND flag:hub_unlocked (the last
  // quadrant) — never hand-set.
  nessa_cole: {
    id: 'nessa_cole',
    name: 'NESSA COLE',
    title: 'Lampwarden',
    party: [
      { species_id: 106, level: 48 }, // Drowshorn — Lunar
      { species_id: 112, level: 49 }, // Nightwraith — Lunar
      { species_id: 125, level: 50 }, // Crystalune — Lunar/Frost
      { species_id: 127, level: 50 }, // Lunvane — Light/Lunar
      { species_id: 107, level: 52 }, // Lunarbel — Lunar/Light (ace — the dreamlight bell)
    ],
    intro_ref: 'trainer.nessa_cole.intro',
    defeat_ref: 'trainer.nessa_cole.defeat',
    reward_flags: ['gleam:lunar'],
    reward_abilities: ['starreach'],
    payout: 3120, // Lampwarden 60 × ace 52
    music: 'battle-nightfall',
    ai: 'smart',
  },

  // --- The Umbral Spire (05-central-endgame) — the endgame difficulty ramp. ---
  // The Hollowing's acolytes tend the null-works with drained Dark kin: each is
  // a PERSON doing a careful, terrible kindness (story-bible §7), keeper class,
  // 'smart' AI (the spine's "hardest sustained run"). Their asks/defeats live in
  // their scripts (the sight-keeper pattern); no in-battle dialogue needed.
  hollowing_acolyte_a: {
    id: 'hollowing_acolyte_a',
    name: 'MERRIN',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 136, level: 52 }, // Mothdim — Dark
      { species_id: 137, level: 53 }, // Nullmoth — Dark (ace)
    ],
    payout: 1060, // keeper 20 × ace 53
    music: 'battle-nightfall',
    ai: 'smart',
  },
  hollowing_acolyte_b: {
    id: 'hollowing_acolyte_b',
    name: 'TACE',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 134, level: 52 }, // Wispwane — Dark/Light
      { species_id: 133, level: 52 }, // Flutterwane — Dark/Light
      { species_id: 137, level: 53 }, // Nullmoth — Dark (ace)
    ],
    payout: 1060, // keeper 20 × ace 53
    music: 'battle-nightfall',
    ai: 'smart',
  },
  hollowing_acolyte_c: {
    id: 'hollowing_acolyte_c',
    name: 'IVORWEN',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 141, level: 53 }, // Cindersob — Dark/Ember
      { species_id: 142, level: 54 }, // Embergone — Dark/Ember (ace)
    ],
    payout: 1080, // keeper 20 × ace 54
    music: 'battle-nightfall',
    ai: 'smart',
  },
  hollowing_acolyte_d: {
    id: 'hollowing_acolyte_d',
    name: 'HARL',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 143, level: 54 }, // Whorlix — Storm/Dark
      { species_id: 138, level: 55 }, // Voidmantle — Dark (ace)
    ],
    payout: 1100, // keeper 20 × ace 55
    music: 'battle-nightfall',
    ai: 'smart',
  },
  hollowing_acolyte_e: {
    id: 'hollowing_acolyte_e',
    name: 'SEFA',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 135, level: 54 }, // Liminalux — Dark/Light
      { species_id: 139, level: 55 }, // Wispwane Null — Dark/Light (ace)
    ],
    payout: 1100, // keeper 20 × ace 55
    music: 'battle-nightfall',
    ai: 'smart',
  },

  // THE FINAL BATTLE — Warden Còr at the Great Null (ace ~56). Dark/Lunar
  // pressure with Omenire's lull (doze) as the signature threat; Nullmajor —
  // his alone, never catchable — closes on the Hollowing Hymn. Winning does
  // not defeat him: it earns the right to ANSWER him (the resolution rides
  // script.warden_cor_final; reward flags stay on the trigger's sets_flags).
  warden_cor: {
    id: 'warden_cor',
    name: 'WARDEN CÒR',
    title: 'Keeper of the Hollowing',
    party: [
      { species_id: 113, level: 53 }, // Omenire — Lunar/Dark (lull: the doze threat)
      { species_id: 85, level: 54 }, // Stillwarden — Frost/Dark
      { species_id: 135, level: 54 }, // Liminalux — Dark/Light
      { species_id: 138, level: 55 }, // Voidmantle — Dark
      { species_id: 142, level: 55 }, // Embergone — Dark/Ember
      { species_id: 150, level: 56 }, // Nullmajor — Dark (the ace; the Hollowing Hymn)
    ],
    intro_ref: 'trainer.warden_cor.intro',
    defeat_ref: 'trainer.warden_cor.defeat',
    payout: 6720, // Còr 120 × ace 56
    music: 'battle-boss-eclipse',
    ai: 'smart',
  },

  // ===========================================================================
  // THE STARFALL VIGILS (06-postgame · R3) — the endgame challenge chain. The
  // Vigilants are the generation of keepers who tended the lamps BEFORE the Long
  // Dusk, out of retirement to stand vigil over the fallen star-shards. Each is
  // the game's first FULL-SIX, smart-AI trial — the new `vigilant` payout class
  // (80w × ace; the ladder route 16 → keeper 20 → rival 24 → warden 60 →
  // vigilant 80 → cor 120). Their aces double as their site's bed catch (the
  // trial proves you can face what you came to catch). Parties/levels/payouts
  // are VERBATIM from the 06-postgame "chain master list" trainer table.
  // Vigilants on `battle-nightfall`; Fenn on the Spire boss cue (`battle-boss-eclipse`,
  // the Còr final's bed) — the only boss cue shipped — sincere throughout.
  // ===========================================================================
  vigilant_esra: {
    id: 'vigilant_esra',
    name: 'WICK-MOTHER ESRA',
    title: 'Vigilant',
    party: [
      { species_id: 7, level: 58 }, // Wicklord — Ember
      { species_id: 12, level: 58 }, // Chandrek — Ember
      { species_id: 19, level: 59 }, // Warmantis — Ember
      { species_id: 43, level: 59 }, // Pyrolith — Ember/Stone
      { species_id: 17, level: 59 }, // Scorchwing — Ember
      { species_id: 33, level: 60 }, // Embralux — Ember/Light (ace)
    ],
    intro_ref: 'trainer.vigilant_esra.intro',
    defeat_ref: 'trainer.vigilant_esra.defeat',
    payout: 4800, // vigilant 80 × ace 60
    music: 'battle-nightfall',
    ai: 'smart',
  },
  vigilant_bramm: {
    id: 'vigilant_bramm',
    name: 'OLD FOREMAN BRAMM',
    title: 'Vigilant',
    party: [
      { species_id: 40, level: 60 }, // Lumenmoss — Verdant/Light
      { species_id: 64, level: 60 }, // Rootwarden — Verdant
      { species_id: 58, level: 61 }, // Mycelarch — Verdant
      { species_id: 52, level: 61 }, // Lithonyx — Stone
      { species_id: 55, level: 61 }, // Ferrolith — Stone
      { species_id: 70, level: 62 }, // Mycovast — Verdant/Stone (ace)
    ],
    intro_ref: 'trainer.vigilant_bramm.intro',
    defeat_ref: 'trainer.vigilant_bramm.defeat',
    payout: 4960, // vigilant 80 × ace 62
    music: 'battle-nightfall',
    ai: 'smart',
  },
  vigilant_ondra: {
    id: 'vigilant_ondra',
    name: 'ONDRA VAEL',
    title: 'Vigilant',
    party: [
      { species_id: 102, level: 62 }, // Tempestail — Storm
      { species_id: 79, level: 62 }, // Glacitern — Frost
      { species_id: 96, level: 63 }, // Frigalance — Storm/Frost
      { species_id: 93, level: 63 }, // Cumulance — Storm
      { species_id: 82, level: 63 }, // Vortexlope — Frost/Storm
      { species_id: 144, level: 64 }, // Nullhusk — Storm/Dark (ace)
    ],
    intro_ref: 'trainer.vigilant_ondra.intro',
    defeat_ref: 'trainer.vigilant_ondra.defeat',
    payout: 5120, // vigilant 80 × ace 64
    music: 'battle-nightfall',
    ai: 'smart',
  },
  vigilant_solenne: {
    id: 'vigilant_solenne',
    name: 'DAME SOLENNE',
    title: 'Vigilant',
    party: [
      { species_id: 121, level: 64 }, // Sunstag — Solar/Verdant
      { species_id: 110, level: 64 }, // Lunaquell — Lunar
      { species_id: 123, level: 65 }, // Solreach — Solar
      { species_id: 127, level: 65 }, // Lunvane — Light/Lunar
      { species_id: 128, level: 65 }, // Solarmourn — Solar
      { species_id: 119, level: 66 }, // Helithorn — Solar (ace)
    ],
    intro_ref: 'trainer.vigilant_solenne.intro',
    defeat_ref: 'trainer.vigilant_solenne.defeat',
    payout: 5280, // vigilant 80 × ace 66
    music: 'battle-nightfall',
    ai: 'smart',
  },
  vigilant_mer: {
    id: 'vigilant_mer',
    name: 'WARDEN MER',
    title: 'Vigilant',
    party: [
      { species_id: 135, level: 66 }, // Liminalux — Dark/Light
      { species_id: 138, level: 66 }, // Voidmantle — Dark
      { species_id: 85, level: 67 }, // Stillwarden — Frost/Dark
      { species_id: 140, level: 67 }, // Wisprestored — Light
      { species_id: 145, level: 67 }, // Cindervast — Dark
      { species_id: 146, level: 68 }, // Bogvast — Dark (ace)
    ],
    intro_ref: 'trainer.vigilant_mer.intro',
    defeat_ref: 'trainer.vigilant_mer.defeat',
    payout: 5440, // vigilant 80 × ace 68
    music: 'battle-nightfall',
    ai: 'smart',
  },

  // The summit Round — the three Vigilants who "climbed ahead" (Ondra → Solenne
  // → Mer), back-to-back inside `script.starfall_round`, a band higher than their
  // home sites (67–69). Each pays the flat post-crown re-runnable rate (5,520 =
  // vigilant 80 × ace 69) — optional income outside the solvency legs.
  vigilant_ondra_summit: {
    id: 'vigilant_ondra_summit',
    name: 'ONDRA VAEL',
    title: 'Vigilant',
    party: [
      { species_id: 102, level: 67 }, // Tempestail — Storm
      { species_id: 79, level: 67 }, // Glacitern — Frost
      { species_id: 96, level: 68 }, // Frigalance — Storm/Frost
      { species_id: 93, level: 68 }, // Cumulance — Storm
      { species_id: 82, level: 68 }, // Vortexlope — Frost/Storm
      { species_id: 144, level: 69 }, // Nullhusk — Storm/Dark (ace)
    ],
    intro_ref: 'trainer.vigilant_ondra_summit.intro',
    defeat_ref: 'trainer.vigilant_ondra_summit.defeat',
    payout: 5520, // vigilant 80 × ace 69
    music: 'battle-nightfall',
    ai: 'smart',
  },
  vigilant_solenne_summit: {
    id: 'vigilant_solenne_summit',
    name: 'DAME SOLENNE',
    title: 'Vigilant',
    party: [
      { species_id: 121, level: 67 }, // Sunstag — Solar/Verdant
      { species_id: 110, level: 67 }, // Lunaquell — Lunar
      { species_id: 123, level: 68 }, // Solreach — Solar
      { species_id: 127, level: 68 }, // Lunvane — Light/Lunar
      { species_id: 128, level: 68 }, // Solarmourn — Solar
      { species_id: 119, level: 69 }, // Helithorn — Solar (ace)
    ],
    intro_ref: 'trainer.vigilant_solenne_summit.intro',
    defeat_ref: 'trainer.vigilant_solenne_summit.defeat',
    payout: 5520, // vigilant 80 × ace 69
    music: 'battle-nightfall',
    ai: 'smart',
  },
  vigilant_mer_summit: {
    id: 'vigilant_mer_summit',
    name: 'WARDEN MER',
    title: 'Vigilant',
    party: [
      { species_id: 135, level: 68 }, // Liminalux — Dark/Light
      { species_id: 138, level: 68 }, // Voidmantle — Dark
      { species_id: 85, level: 68 }, // Stillwarden — Frost/Dark
      { species_id: 140, level: 69 }, // Wisprestored — Light
      { species_id: 145, level: 69 }, // Cindervast — Dark
      { species_id: 146, level: 69 }, // Bogvast — Dark (ace)
    ],
    intro_ref: 'trainer.vigilant_mer_summit.intro',
    defeat_ref: 'trainer.vigilant_mer_summit.defeat',
    payout: 5520, // vigilant 80 × ace 69
    music: 'battle-nightfall',
    ai: 'smart',
  },

  // THE LAST LESSON — Star-tender Fenn at full strength, the hardest fight in the
  // game. His six, read in order, are the game's arc: the small light first
  // (Glimscout), then the moons (Lunarbel, Crystalune), the light that holds
  // (Prismantus), the sun's spiral (Helixia), and the one he named as a hope:
  // Dawnwatcher, ace 70. `cor` class, 120 × 70 = 8,400w. Sincere throughout.
  startender_fenn: {
    id: 'startender_fenn',
    name: 'STAR-TENDER FENN',
    title: 'Star-tender',
    party: [
      { species_id: 9, level: 68 }, // Glimscout — Light (the small light first)
      { species_id: 107, level: 68 }, // Lunarbel — Lunar/Light
      { species_id: 125, level: 68 }, // Crystalune — Lunar/Frost
      { species_id: 87, level: 69 }, // Prismantus — Light/Frost (the light that holds)
      { species_id: 131, level: 69 }, // Helixia — Solar (the sun's spiral)
      { species_id: 129, level: 70 }, // Dawnwatcher — Lunar/Light (the one he named, ace)
    ],
    intro_ref: 'trainer.startender_fenn.intro',
    defeat_ref: 'trainer.startender_fenn.defeat',
    payout: 8400, // cor 120 × ace 70
    music: 'battle-boss-eclipse',
    ai: 'smart',
  },
};

/** Intro/defeat dialogue for trainers, kept beside the roster they belong to. */
export const TRAINER_DIALOGUE: Record<string, DialogueLine[]> = {
  'trainer.lampwarden_tinderwick.intro': [
    { speaker: 'BRISA TALLOW', text: 'So the lamp-tender sends an apprentice. Good. The dark needs fewer cowards.' },
    { speaker: 'BRISA TALLOW', text: 'Show me your spark, Wayfarer. If it holds, the Ember Gleam is yours.' },
  ],
  'trainer.lampwarden_tinderwick.defeat': [
    { speaker: 'BRISA TALLOW', text: 'Hah! A warm flame indeed. The southern crown remembers your light.' },
    { speaker: 'BRISA TALLOW', text: 'Take the Ember Gleam. One constellation relit — only seven dusks to go.' },
  ],
  'trainer.wren_dimglass.intro': [
    { speaker: 'WREN', text: "No Lamps, no stakes — just us and our partners. Show me what your bond's worth." },
    {
      speaker: 'WREN',
      text: "And a kindness, since we're friends: ember chars the green, green drinks the tide, tide drowns the ember — round and round. Match your move to that, not your mood.",
    },
  ],
  'trainer.wren_dimglass.defeat': [
    { speaker: 'WREN', text: "Ha! Knew you'd be good. Race you to Pearlmoor — keep to the lamps, Wayfarer." },
  ],
  'trainer.flats_wayfarer_a.intro': [
    { speaker: 'MORROW', text: 'Hold there, friend. Two lamps on a dark flat had better test their wicks — that is the custom.' },
  ],
  'trainer.flats_wayfarer_a.defeat': [
    { speaker: 'MORROW', text: 'A steady flame, yours. Pearlmoor sits past the buoys — the old ferryman keeps the second Gleam.' },
  ],
  'trainer.flats_wayfarer_b.intro': [
    { speaker: 'ELSPETH', text: 'Courier post! Letters for Pearlmoor — and a standing wager for any Wayfarer who dares the flats.' },
  ],
  'trainer.flats_wayfarer_b.defeat': [
    { speaker: 'ELSPETH', text: 'The wager is yours. Mind the tide pools, and tell Reyl his letters are late because of you.' },
  ],
  'trainer.net_hand_a.intro': [
    { speaker: 'MAREN', text: 'Nobody walks the moor-boards but bell-business and net-hands — and you don\'t smell of either yet.' },
    { speaker: 'MAREN', text: 'Rope or no rope, the causeway tests every lamp it carries. Out here that\'s the LAW.' },
  ],
  'trainer.net_hand_a.defeat': [
    { speaker: 'MAREN', text: 'Steady on wet stone — that\'s rarer than you\'d think. Go on, then. Mind Cob by the far lantern; he\'s been spoiling for a bout all season.' },
  ],
  'trainer.net_hand_b.intro': [
    { speaker: 'COB', text: 'Past Maren with your boots still dry! Then you\'re the one carrying the old rope home.' },
    { speaker: 'COB', text: 'One more net between you and the bell, Wayfarer. Mine\'s the heavier.' },
  ],
  'trainer.net_hand_b.defeat': [
    { speaker: 'COB', text: 'Hah! Well hauled. The shrine\'s at the causeway\'s end — ring it LOUD, so the whole quay hears it come back.' },
  ],
  'trainer.lampwarden_pearlmoor.intro': [
    { speaker: 'REYL WASH', text: 'Apprentice, is it. I have ferried a hundred Wayfarers across this harbour. Few read the water right.' },
    { speaker: 'REYL WASH', text: 'Tides go out so they can come back, see. Show me your bond holds against mine — then I will teach you to ask the sea to part.' },
  ],
  'trainer.lampwarden_pearlmoor.defeat': [
    { speaker: 'REYL WASH', text: 'Well rowed, Wayfarer. The Tide constellation answers you — see it shiver awake over the masts.' },
    { speaker: 'REYL WASH', text: 'The Tide Gleam is yours, and with it the Tidecall. Step to the shallows now; the moon-water will part where it would not before.' },
  ],
  'trainer.lampwarden_lowleaf.intro': [
    { speaker: 'SABLE QUILL', text: 'I\'m better at this part than the talking part. My moss thinks so too.' },
    { speaker: 'SABLE QUILL', text: 'Everything green in this hall keeps a little light it was never asked to keep. Show me your kin do the same.' },
  ],
  'trainer.lampwarden_lowleaf.defeat': [
    { speaker: 'SABLE QUILL', text: '...Oh. Oh, that was LOVELY. Don\'t tell anyone I said that out loud.' },
    { speaker: 'SABLE QUILL', text: 'The Verdant Gleam is yours — the moss vouched for you, and the moss has never once been wrong about a person.' },
  ],
  'trainer.lampwarden_cinderhead.intro': [
    { speaker: 'OTHO GRIST', text: 'No rush in my kin and no rush in me. We are the mountain, Wayfarer. We OUTLAST.' },
    { speaker: 'OTHO GRIST', text: 'Show me a light that does not gutter when the rock leans in. That is all a Gleam ever was.' },
  ],
  'trainer.lampwarden_cinderhead.defeat': [
    { speaker: 'OTHO GRIST', text: 'Hah. You did not out-hit them. You out-LASTED them. ...That, I respect. That is the deep way.' },
    { speaker: 'OTHO GRIST', text: 'A steady light. The Stone remembers it. Come — let the vigil see what you carried up.' },
  ],
  'trainer.gallery_miner_a.intro': [
    { speaker: 'DRUSE', text: 'Wick against wick, Wayfarer. Crew rule. You do not pass the gallery till you have weighed it.' },
  ],
  'trainer.gallery_miner_a.defeat': [
    { speaker: 'DRUSE', text: 'Steady enough. The lamp is two chambers on — and Hobb is between you and it.' },
  ],
  'trainer.gallery_miner_b.intro': [
    { speaker: 'HOBB', text: 'Last lamp before the vigil-lamp, and it is mine to keep. Come on, then.' },
  ],
  'trainer.gallery_miner_b.defeat': [
    { speaker: 'HOBB', text: 'Well held. Lift the vigil-lamp gentle, now — it has waited a long dark for a steady hand.' },
  ],

  // --- The North. Defeat lines are the sanctioned humour home in Galehigh /
  // Windward (good-loser energy, never mockery); the Pale Vault cluster stays
  // sincere throughout, and Wren's A4 lines stay unresolved by design.
  'trainer.galehigh_kitehand.intro': [
    { speaker: 'PERRIN', text: 'The wind\'s representative requests a bout! It would ask itself, but it\'s busy with the kites.' },
  ],
  'trainer.galehigh_kitehand.defeat': [
    { speaker: 'PERRIN', text: 'Down I come. The wind keeps no favourites — it just enjoys the view.' },
  ],
  'trainer.galehigh_terracer.intro': [
    { speaker: 'SORREL', text: 'Thirty years I\'ve farmed sideways on this cliff. A bout holds no fears for me whatsoever.' },
  ],
  'trainer.galehigh_terracer.defeat': [
    { speaker: 'SORREL', text: 'Well grown, that bond of yours. Better soil than mine, clearly. It would have to be.' },
  ],
  'trainer.skyloft_ward_a.intro': [
    { speaker: 'TAMSIN', text: 'The ledge admits no flame the wind hasn\'t weighed — and up here, the wind weighs HONESTLY.' },
  ],
  'trainer.skyloft_ward_a.defeat': [
    { speaker: 'TAMSIN', text: 'Well flown! And I\'d trained that gust personally. It clearly liked you better.' },
  ],
  'trainer.skyloft_ward_b.intro': [
    { speaker: 'BRAN', text: 'Last ward before the launch ledge. Let\'s hear the wind say yes to you.' },
  ],
  'trainer.skyloft_ward_b.defeat': [
    { speaker: 'BRAN', text: 'It said yes. The ledge is yours to stand, Wayfarer.' },
  ],
  'trainer.mira_vael.intro': [
    { speaker: 'MIRA VAEL', text: 'Five hundred feet of open air under the ledge and a storm overhead that LIKES you. There is no better arena in Vesperholm — let\'s give the wind a show!' },
    { speaker: 'MIRA VAEL', text: 'My kin ride the gusts the way your kite did. Match them in the air, Wayfarer — the Storm Gleam watches!' },
  ],
  'trainer.mira_vael.defeat': [
    { speaker: 'MIRA VAEL', text: 'HA! Did you feel the wind change sides halfway through? It does that for the ones it means to keep.' },
    { speaker: 'MIRA VAEL', text: 'The Storm Gleam is yours, Wayfarer — and the wind with it. Come to the ledge; the sky wants relighting.' },
  ],
  'trainer.windward_craghand.intro': [
    { speaker: 'EDDA', text: 'Stair custom at every bend — the climb tests your legs, the crag-hands test the rest.' },
  ],
  'trainer.windward_craghand.defeat': [
    { speaker: 'EDDA', text: 'Four hundred and twelve steps a day, and the lesson walks UP to me. Well fought.' },
  ],
  'trainer.windward_galewatch.intro': [
    { speaker: 'ROWAN', text: 'The gale-watch greets every flame that climbs this far. The greeting is a bout. It keeps us both warm.' },
  ],
  'trainer.windward_galewatch.defeat': [
    { speaker: 'ROWAN', text: 'Warm enough! The high blue suits you better than it suits most.' },
  ],
  'trainer.windward_cragwatch.intro': [
    { speaker: 'MERLE', text: 'The glacier ahead doesn\'t practise mercy, Wayfarer. Consider this your last rehearsal.' },
  ],
  'trainer.windward_cragwatch.defeat': [
    { speaker: 'MERLE', text: 'Rehearsal passed. The cold will find you ready, and it will be very disappointed about it.' },
  ],
  'trainer.wren_pale_vault.intro': [
    { speaker: 'WREN', text: 'No friendly rules this time. Everything you have — make me FEEL it.' },
  ],
  'trainer.wren_pale_vault.defeat': [
    { speaker: 'WREN', text: '...Yeah. Okay. ...Yeah.' },
  ],
  'trainer.undercroft_ward_a.intro': [
    { speaker: 'SELA', text: 'The vault admits no flame the wards haven\'t weighed. The brackets deserve that much care.' },
  ],
  'trainer.undercroft_ward_a.defeat': [
    { speaker: 'SELA', text: 'Weighed, and worthy of the line. Walk on, lamplighter.' },
  ],
  'trainer.undercroft_ward_b.intro': [
    { speaker: 'ORRIN', text: 'I send Ysolde nothing the cold could blow out on the way. Show me yours holds.' },
  ],
  'trainer.undercroft_ward_b.defeat': [
    { speaker: 'ORRIN', text: 'It holds. Finish the line — the vault has waited years to be bright.' },
  ],
  'trainer.ysolde_frost.intro': [
    { speaker: 'YSOLDE FROST', text: 'Cold does not hate the flame, wanderer. It only waits to see if the flame means it.' },
    { speaker: 'YSOLDE FROST', text: 'Seven brackets say yours does. Now warm your kin — and let me see the light hold.' },
  ],
  'trainer.ysolde_frost.defeat': [
    { speaker: 'YSOLDE FROST', text: '...It held. Through everything my vault could ask of it, it held.' },
    { speaker: 'YSOLDE FROST', text: 'The Frost Gleam is yours, wanderer — and the northern crown closes with it. Stand still a moment. This is worth standing still for.' },
  ],

  // --- The West. Hushfrost runs sincere (the caretaker owns the register);
  // the Solarium/Sunvault defeat lines carry the sanctioned good-loser warmth;
  // Nightreach stays reverent; Coldfog has no trainers at all, by design.
  'trainer.hushfrost_lampman.intro': [
    { speaker: 'DUNSTAN', text: 'Hold there, Wayfarer. My lamp is losing to that fog an inch a season — so before you pass, show me a flame the cold has not argued down.' },
  ],
  'trainer.hushfrost_lampman.defeat': [
    { speaker: 'DUNSTAN', text: 'There it is. That is the burn I have been rationing all winter. Go on — and warm the throat for the rest of us.' },
  ],
  'trainer.hushfrost_survivor.intro': [
    { speaker: 'HESPER', text: 'I walked out of the deep fog once, on one lamp and no luck to spare. Every flame that passes me gets tested now. I owe the road that much.' },
  ],
  'trainer.hushfrost_survivor.defeat': [
    { speaker: 'HESPER', text: 'Steady right through. ...Good. If the fog takes anyone else this year, it will not be for want of my checking.' },
  ],
  'trainer.hushfrost_thawtender.intro': [
    { speaker: 'TILDA', text: 'Mind the lane — I have just swept the rime off it. Terrace rule from back home: a clear road is paid for with a bout.' },
  ],
  'trainer.hushfrost_thawtender.defeat': [
    { speaker: 'TILDA', text: 'Well fought! And see — the gold on the fog ahead is real. Stored daylight, a whole gardenful. First warm thing I have said all week that the weather agreed with.' },
  ],
  'trainer.troupe_player_a.intro': [
    { speaker: 'CALLA', text: 'A walker in the wings! House rule, friend: nobody crosses the flooded lanes during rehearsal without giving the understudies a scene.' },
  ],
  'trainer.troupe_player_a.defeat': [
    { speaker: 'CALLA', text: 'Upstaged in my own water. Forty years of stagecraft and the audience walks in off a glacier with better timing.' },
  ],
  'trainer.troupe_player_b.intro': [
    { speaker: 'ORSINO', text: 'Stop! That is — forgive me, the boards say STOP, in the play. One bout, traveller, for the company. The drowned halls make a tremendous house.' },
  ],
  'trainer.troupe_player_b.defeat': [
    { speaker: 'ORSINO', text: 'Bravo. No, truly — I have died on stage a hundred times and that was the most convincing of them.' },
  ],
  'trainer.lucan_pyre.intro': [
    { speaker: 'LUCAN PYRE', text: 'PLACES! The stage is lit, the house is full, and the last warm day has found its closing scene. You fetched our daylight up spark by spark, apprentice — now act the part it paid for.' },
    { speaker: 'LUCAN PYRE', text: 'Show me a bond that remembers the sun! Not the heat, mind — anyone can burn. The PROMISE of it. The coming back.' },
  ],
  'trainer.lucan_pyre.defeat': [
    { speaker: 'LUCAN PYRE', text: '...Hold. Hold the lights just there. Do you hear the house? That is not applause for ME, and I have never been gladder to be upstaged.' },
    { speaker: 'LUCAN PYRE', text: 'The Solar Gleam is yours, Wayfarer. The sun only went to sleep — and tonight, between us, I think we woke the understudy.' },
  ],
  'trainer.sunvault_terracer.intro': [
    { speaker: 'BEL', text: 'Mind the beds! These terraces fed a garden by sunlight once — now they make do with mine. Every lamp that climbs through gets weighed against the gold. Custom.' },
  ],
  'trainer.sunvault_terracer.defeat': [
    { speaker: 'BEL', text: 'Weighed, and the garden approves. The overgrowth leaned toward you the whole bout — it has never once done that for me, and I prune it.' },
  ],
  'trainer.sunvault_skywatcher.intro': [
    { speaker: 'TAM', text: 'You are walking into the brightest sky in Vesperholm, friend. The watchers send nothing up the rim they have not tested — consider me the test.' },
  ],
  'trainer.sunvault_skywatcher.defeat': [
    { speaker: 'TAM', text: 'Passed, and then some. Go on up — and when the dome takes your breath, that is not the climb. That is the sky.' },
  ],
  'trainer.junior_watcher_a.intro': [
    { speaker: 'LIRA', text: 'Hold the walk, please. Seven lamps, seven stars, and a junior watcher to keep the order of it — nobody crosses my stretch unweighed. Even the senior watchers. ESPECIALLY the senior watchers.' },
  ],
  'trainer.junior_watcher_a.defeat': [
    { speaker: 'LIRA', text: 'Weighed and recorded. ...In my own ledger, which nobody reads. The walk is yours, Wayfarer — keep the order.' },
  ],
  'trainer.junior_watcher_b.intro': [
    { speaker: 'OS', text: 'A lamp on the high terrace. Good — the vigil likes a tested flame. I keep the last stretch before the seventh lamp; show me yours keeps too.' },
  ],
  'trainer.junior_watcher_b.defeat': [
    { speaker: 'OS', text: 'It keeps. Walk on — and walk soft. Nessa has been at the eyepiece three nights straight, waiting on whatever it is you are carrying.' },
  ],
  'trainer.wren_nightreach.intro': [
    { speaker: 'WREN', text: "Friendly rules. Like the coast. I want to remember what it's FOR before we light the last one." },
  ],
  'trainer.wren_nightreach.defeat': [
    { speaker: 'WREN', text: 'Ha — there it is. THAT\'s the thing the quiet doesn\'t have. Come on.' },
  ],
  'trainer.wren_rematch.intro': [
    { speaker: 'WREN', text: 'Friendly rules. Morning rules. Best light we\'ve ever had for it.' },
  ],
  'trainer.wren_rematch.defeat': [
    { speaker: 'WREN', text: 'Still you. Good. Some things should survive a sunrise.' },
  ],
  'trainer.nessa_cole.intro': [
    { speaker: 'NESSA COLE', text: 'Seven watch-fires, lit in the order they came home. I watched every one from this eyepiece. You walk the way a careful light burns.' },
    { speaker: 'NESSA COLE', text: 'One star left, and it is mine to vouch for. My kin keep the dream-hours with me — the soft dark, the kind that lets you sleep. Stay awake through it, Wayfarer... and the eighth will answer you.' },
  ],
  'trainer.nessa_cole.defeat': [
    { speaker: 'NESSA COLE', text: '...Awake at the end of it. All my long watches, and I have never been so glad to lose an argument with the dark.' },
    { speaker: 'NESSA COLE', text: 'Stand by the lamp, Wayfarer. The eighth star has been waiting longest of all — and I would like to watch it remember.' },
  ],

  // --- The summit. Còr's case lives in script.warden_cor_final (portraits, the
  // full cadence); these are only the battle's own frame — courteous to the last.
  'trainer.warden_cor.intro': [
    { speaker: 'WARDEN CÒR', text: 'Very well. Let the lamps make the argument, then — yours as they are, mine as I have made them.' },
    { speaker: 'WARDEN CÒR', text: 'I will be gentle. I am always gentle. That was never the part anyone disagreed with.' },
  ],
  'trainer.warden_cor.defeat': [
    { speaker: 'WARDEN CÒR', text: '...Still lit. Every one of them, still lit.' },
  ],

  // --- The Starfall Vigils (06-postgame). The spec-verbatim keeper lines live
  // in the script.vigil_* cutscenes; these refs are ONLY the battle's own short
  // frame (the warden_cor convention — postgame-panel MAJ-1: identical strings
  // here displayed every line twice). Glint stays with Esra/Bramm/Ondra/Solenne;
  // Mer and the summit are SINCERE throughout.
  'trainer.vigilant_esra.intro': [
    { speaker: 'WICK-MOTHER ESRA', text: 'Show me a steady flame, dear.' },
  ],
  'trainer.vigilant_esra.defeat': [
    { speaker: 'WICK-MOTHER ESRA', text: 'Bright. Properly bright.' },
  ],
  'trainer.vigilant_bramm.intro': [
    { speaker: 'OLD FOREMAN BRAMM', text: 'The deep way, then. Walk it.' },
  ],
  'trainer.vigilant_bramm.defeat': [
    { speaker: 'OLD FOREMAN BRAMM', text: 'Hah! Up you come.' },
  ],
  'trainer.vigilant_ondra.intro': [
    { speaker: 'ONDRA VAEL', text: 'Stand into the wind!' },
  ],
  'trainer.vigilant_ondra.defeat': [
    { speaker: 'ONDRA VAEL', text: 'HA! Well flown!' },
  ],
  'trainer.vigilant_solenne.intro': [
    { speaker: 'DAME SOLENNE', text: 'Full light, my dear. Begin.' },
  ],
  'trainer.vigilant_solenne.defeat': [
    { speaker: 'DAME SOLENNE', text: 'And... bow.' },
  ],
  'trainer.vigilant_mer.intro': [
    { speaker: 'WARDEN MER', text: 'Steady, now. Show me steady.' },
  ],
  'trainer.vigilant_mer.defeat': [
    { speaker: 'WARDEN MER', text: 'Handed on, then. Gladly.' },
  ],

  // The summit Round — the three who climbed ahead.
  'trainer.vigilant_ondra_summit.intro': [
    { speaker: 'ONDRA VAEL', text: 'Mine\'s the front of the queue — warm up on me.' },
  ],
  'trainer.vigilant_ondra_summit.defeat': [
    { speaker: 'ONDRA VAEL', text: 'Same as the aerie. Sharper. Go on — Solenne\'s next, and she rehearsed.' },
  ],
  'trainer.vigilant_solenne_summit.intro': [
    { speaker: 'DAME SOLENNE', text: 'Encore of the encore. The summit makes a tremendous house — and the lighting, my dear, is finally perfect.' },
  ],
  'trainer.vigilant_solenne_summit.defeat': [
    { speaker: 'DAME SOLENNE', text: 'Bravo, again. Mer keeps the last gate before the old man. Go gently — she always means it.' },
  ],
  'trainer.vigilant_mer_summit.intro': [
    { speaker: 'WARDEN MER', text: 'One more steadiness, before he asks you for all of it. I hand the light on gladly now. Show me once more why.' },
  ],
  'trainer.vigilant_mer_summit.defeat': [
    { speaker: 'WARDEN MER', text: 'It holds, to the last gate. He\'s waiting at the lantern. ...Be everything you\'ve become.' },
  ],

  // The Last Lesson — sincere throughout (the humour stopped at the marshes).
  // The full speech lives in script.starfall_round; this is the battle's frame.
  'trainer.startender_fenn.intro': [
    { speaker: 'STAR-TENDER FENN', text: 'The last lesson, apprentice. Begin.' },
  ],
  'trainer.startender_fenn.defeat': [
    { speaker: 'STAR-TENDER FENN', text: 'Kept. Every lamp of it, kept.' },
  ],
};

export function getTrainer(id: string): TrainerDef | undefined {
  return TRAINERS[id];
}

/** Resolve a trainer dialogue ref to its pages (empty array if unknown/absent). */
export function getTrainerLines(ref: string | undefined): DialogueLine[] {
  if (!ref) return [];
  return TRAINER_DIALOGUE[ref] ?? [];
}
