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
    reward_flags: ['gleam:ember', 'crown_south'],
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
    reward_flags: ['gleam:tide', 'crown_south'],
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
};

export function getTrainer(id: string): TrainerDef | undefined {
  return TRAINERS[id];
}

/** Resolve a trainer dialogue ref to its pages (empty array if unknown/absent). */
export function getTrainerLines(ref: string | undefined): DialogueLine[] {
  if (!ref) return [];
  return TRAINER_DIALOGUE[ref] ?? [];
}
