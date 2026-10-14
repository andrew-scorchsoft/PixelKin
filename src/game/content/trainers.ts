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
import { SPAR_TRAINERS } from './sparring';

export const TRAINERS: TrainerRegistry = {
  lampwarden_tinderwick: {
    id: 'lampwarden_tinderwick',
    name: 'BRISA TALLOW',
    title: 'Lampwarden',
    party: [
      { species_id: 10, level: 6 }, // Tallowpup — Ember (eased 2026-10 from 7)
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
      { species_id: 16, level: 6 }, // Wickmoth — Ember
    ],
    payout: 120, // keeper 20 × ace 6
    music: 'battle-emberfall',
  },
  beacon_keeper_b: {
    id: 'beacon_keeper_b',
    name: 'COLE',
    title: 'Wick-tender',
    party: [
      { species_id: 10, level: 6 }, // Tallowpup — Ember
      { species_id: 16, level: 7 }, // Wickmoth — Ember
    ],
    payout: 140, // keeper 20 × ace 7
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
      { species_id: 31, level: 10 }, // Lumpin — Tide/Light (eased 11→10, 2026-10)
    ],
    intro_ref: 'trainer.flats_wayfarer_b.intro',
    defeat_ref: 'trainer.flats_wayfarer_b.defeat',
    payout: 160, // route 16 × ace 10
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
    solo_line: 'A very cross Sporeling puffs itself up and blocks the way!',
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

  // R9 "The Old Light": Punchwheel's two keepers (talk-to, by the up-stairs;
  // both required). They read cards the machine wrote. No Tide kin — Reyl's
  // hall keeps that surprise. Pitched between the flats (~11) and Reyl's 16.
  oldlight_heckler: {
    id: 'oldlight_heckler',
    name: 'THE HECKLER',
    title: 'Jest-keeper',
    party: [
      { species_id: 167, level: 11 }, // JesterHalf — Light/Dark
      { species_id: 8, level: 12 }, // Glimflit — Light (ace)
    ],
    intro_ref: 'trainer.oldlight_heckler.intro', // the battle-screen opener (trainer-intro beat)
    defeat_ref: 'trainer.oldlight_heckler.defeat',
    payout: 240, // keeper 20 × ace 12
    music: 'battle-emberfall',
  },
  oldlight_ringmaster: {
    id: 'oldlight_ringmaster',
    name: 'THE RINGMASTER',
    title: 'Jest-keeper',
    party: [
      { species_id: 167, level: 12 }, // JesterHalf — Light/Dark
      { species_id: 69, level: 13 }, // Riddlestone — Stone (ace)
    ],
    intro_ref: 'trainer.oldlight_ringmaster.intro', // the battle-screen opener (trainer-intro beat)
    defeat_ref: 'trainer.oldlight_ringmaster.defeat',
    payout: 260, // keeper 20 × ace 13
    music: 'battle-emberfall',
  },
  // R11: the top floor's BOSS — the TOLL before the card, not the climax. Mr.
  // Punchwheel's headline act (the house's own three clowns) stands in the only gap
  // to the drum, guarding Tam's card. Ace 15, one under Reyl (16) — the climb's capstone, the last
  // stepping-stone before the Lumenary. Rest first in the green-room chair.
  oldlight_headliners: {
    id: 'oldlight_headliners',
    name: 'MR. PUNCHWHEEL',
    title: 'Jest-engine', // presents his headline act: the house's three clowns
    party: [
      { species_id: 169, level: 14 }, // The Smiler — Light
      { species_id: 171, level: 14 }, // McClownface — Tide/Light
      { species_id: 167, level: 15 }, // JesterHalf — Light/Dark (ace)
    ],
    intro_ref: 'trainer.oldlight_headliners.intro',
    defeat_ref: 'trainer.oldlight_headliners.defeat',
    payout: 300, // keeper 20 × ace 15
    music: 'battle-jesthouse-boss',
    ai: 'smart', // a boss: plays the matchup
  },
  // R10: the jest-house REGULARS — optional sight trainers waiting in each
  // floor's alcove (F1-F5), rising 10 -> 14 so the climb is the grind bed before
  // Reyl (16) and the fen. Balanced, never hard: two-to-three kin; the house's own clowns (JesterHalf, The Smiler, McClownface) turn up in the bills.
  oldlight_usher: {
    id: 'oldlight_usher',
    name: 'THE USHER',
    title: 'Jest-house regular',
    party: [
      { species_id: 169, level: 10 }, // The Smiler — Light
      { species_id: 16, level: 11 }, // Wickmoth — Ember (ace)
    ],
    intro_ref: 'trainer.oldlight_usher.intro', // the battle-screen opener (trainer-intro beat)
    defeat_ref: 'trainer.oldlight_usher.defeat',
    payout: 176, // route 16 × ace 11
  },
  oldlight_juggler: {
    id: 'oldlight_juggler',
    name: 'THE JUGGLER',
    title: 'Jest-house regular',
    party: [
      { species_id: 167, level: 11 }, // JesterHalf — Light/Dark
      { species_id: 47, level: 11 }, // Pebbit — Stone
      { species_id: 8, level: 12 }, // Glimflit — Light (ace)
    ],
    intro_ref: 'trainer.oldlight_juggler.intro', // the battle-screen opener (trainer-intro beat)
    defeat_ref: 'trainer.oldlight_juggler.defeat',
    payout: 192, // route 16 × ace 12
  },
  oldlight_pie_thrower: {
    id: 'oldlight_pie_thrower',
    name: 'THE PIE-THROWER',
    title: 'Jest-house regular',
    party: [
      { species_id: 26, level: 12 }, // Brinelet — Tide
      { species_id: 171, level: 12 }, // McClownface — Tide/Light (ace)
    ],
    intro_ref: 'trainer.oldlight_pie_thrower.intro', // the battle-screen opener (trainer-intro beat)
    defeat_ref: 'trainer.oldlight_pie_thrower.defeat',
    payout: 192, // route 16 × ace 12
  },
  oldlight_mirror: {
    id: 'oldlight_mirror',
    name: 'THE MIRROR',
    title: 'Jest-house regular',
    party: [
      { species_id: 69, level: 12 }, // Riddlestone — Stone
      { species_id: 69, level: 13 }, // Riddlestone — Stone (ace) — of course
    ],
    intro_ref: 'trainer.oldlight_mirror.intro', // the battle-screen opener (trainer-intro beat)
    defeat_ref: 'trainer.oldlight_mirror.defeat',
    payout: 208, // route 16 × ace 13
  },
  oldlight_critic: {
    id: 'oldlight_critic',
    name: 'THE CRITIC',
    title: 'Jest-house regular',
    party: [
      { species_id: 111, level: 13 }, // Spirlet — Lunar
      { species_id: 105, level: 13 }, // Snoozlet — Lunar
      { species_id: 69, level: 14 }, // Riddlestone — Stone (ace)
    ],
    intro_ref: 'trainer.oldlight_critic.intro', // the battle-screen opener (trainer-intro beat)
    defeat_ref: 'trainer.oldlight_critic.defeat',
    payout: 224, // route 16 × ace 14
  },

  // S4 "The Booji-Wooji Man" — Paul, the Lifting House's mystery, fought at the
  // breakwater's end (script.booji_paul; OPTIONAL side-quest bout, route class).
  // The Chickenpig (#163) wades in on Paul's side as his SECOND — the only place
  // you see it in battle before the epilogue catch. (Rematches drop it: it's not
  // his, just odd company; breakwater_paul_rematch fields his real stones.)
  breakwater_paul: {
    id: 'breakwater_paul',
    name: 'PAUL',
    title: 'The Booji-Wooji Man',
    party: [
      { species_id: 53, level: 13 }, // Oreling — Stone
      { species_id: 163, level: 15 }, // Chickenpig — Solar (the dark lamp's odd company, scrapping on Paul's side)
    ],
    intro_ref: 'trainer.breakwater_paul.intro',
    defeat_ref: 'trainer.breakwater_paul.defeat',
    payout: 240, // route 16 × ace 15
    music: 'battle-emberfall',
  },

  // Paul's REMATCH — re-runnable, offered never forced (the wren_rematch pattern):
  // once you've met him, talking to Paul at the dark lamp re-runs this friendly
  // bout. While the Chickenpig is still HIS odd company (you haven't caught it),
  // it scraps alongside him here too, with the question-stone restored for a
  // meatier rematch. Not in the economy budget (BUILT_PAYOUTS), like wren_rematch.
  breakwater_paul_rematch: {
    id: 'breakwater_paul_rematch',
    name: 'PAUL',
    title: 'The Booji-Wooji Man',
    party: [
      { species_id: 53, level: 13 }, // Oreling — Stone
      { species_id: 69, level: 15 }, // Riddlestone — Stone (a stone that asks questions)
      { species_id: 163, level: 15 }, // Chickenpig — Solar (the dark lamp's company, still scrapping for Paul)
    ],
    intro_ref: 'trainer.breakwater_paul_rematch.intro',
    defeat_ref: 'trainer.breakwater_paul_rematch.defeat',
    payout: 240, // repeatable; like wren_rematch, off the budget
    music: 'battle-emberfall',
  },

  // Paul's rematch AFTER you've caught the Chickenpig — it walks with you now, so
  // it's gone from his line; he fields his genuine stones. (Same off-budget rule.)
  breakwater_paul_rematch_post: {
    id: 'breakwater_paul_rematch_post',
    name: 'PAUL',
    title: 'The Booji-Wooji Man',
    party: [
      { species_id: 53, level: 13 }, // Oreling — Stone
      { species_id: 69, level: 15 }, // Riddlestone — Stone (ace; a stone that asks questions)
    ],
    intro_ref: 'trainer.breakwater_paul_rematch.intro',
    defeat_ref: 'trainer.breakwater_paul_rematch.defeat',
    payout: 240, // repeatable; off the budget
    music: 'battle-emberfall',
  },

  // Route trainers on the new Pearlmoor <-> Crossroads route (Wrackline Path /
  // Lanternfall Road) — sight beats in the corridor chokes, route class.
  wrackline_drifter: {
    id: 'wrackline_drifter',
    name: 'DRIFTER OSK',
    title: 'Wayfarer',
    party: [
      { species_id: 26, level: 17 }, // Brinelet — Tide
      { species_id: 31, level: 18 }, // Lumpin — Tide/Light (ace)
    ],
    intro_ref: 'trainer.wrackline_drifter.intro',
    defeat_ref: 'trainer.wrackline_drifter.defeat',
    payout: 288, // route 16 × ace 18
    music: 'battle-emberfall',
  },
  lanternfall_warden: {
    id: 'lanternfall_warden',
    name: 'LAMP-KEEPER NELL',
    title: 'Lampwright',
    party: [
      { species_id: 31, level: 19 }, // Lumpin — Tide/Light
      { species_id: 53, level: 20 }, // Oreling — Stone (ace)
    ],
    intro_ref: 'trainer.lanternfall_warden.intro',
    defeat_ref: 'trainer.lanternfall_warden.defeat',
    payout: 320, // route 16 × ace 20
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

  // --- Cinderwind Scarp (2026-10 geometry fix) — the climb from Cinderhead
  // Deep to Galehigh: two route trainers on the turns (route 16 × ace).
  scarp_hauler: {
    id: 'scarp_hauler',
    name: 'HOBB-REE',
    title: 'Ore-hauler',
    party: [
      { species_id: 53, level: 28 }, // Oreling — Stone
      { species_id: 48, level: 30 }, // Rubbol — Stone (ace)
    ],
    payout: 480, // route 16 × ace 30
  },
  scarp_kiterunner: {
    id: 'scarp_kiterunner',
    name: 'RUE',
    title: 'Kite-runner',
    party: [
      { species_id: 100, level: 29 }, // Squallox — Storm
      { species_id: 91, level: 29 }, // Cirruff — Storm/Light
      { species_id: 101, level: 31 }, // Galefox — Storm (ace)
    ],
    payout: 496, // route 16 × ace 31
  },

  // --- The Umbral Approach (2026-10 geometry fix) — the mountain road up from
  // the Crossroads. Three Hollowing acolytes keep its turns: keeper class like
  // their Spire siblings, but plain AI (the climb warms you up; the Spire is
  // where the hardest sustained run lives).
  approach_acolyte_a: {
    id: 'approach_acolyte_a',
    name: 'ORLA',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 136, level: 50 }, // Mothdim — Dark
      { species_id: 112, level: 51 }, // Nightwraith — Lunar (ace)
    ],
    payout: 1020, // keeper 20 × ace 51
    music: 'battle-nightfall',
  },
  approach_acolyte_b: {
    id: 'approach_acolyte_b',
    name: 'BRENN',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 141, level: 51 }, // Cindersob — Dark/Ember
      { species_id: 143, level: 52 }, // Whorlix — Storm/Dark (ace)
    ],
    payout: 1040, // keeper 20 × ace 52
    music: 'battle-nightfall',
  },
  approach_acolyte_c: {
    id: 'approach_acolyte_c',
    name: 'WYNNE',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 133, level: 52 }, // Flutterwane — Dark/Light
      { species_id: 134, level: 52 }, // Wispwane — Dark/Light
      { species_id: 113, level: 53 }, // Omenire — Lunar/Dark (ace)
    ],
    payout: 1060, // keeper 20 × ace 53
    music: 'battle-nightfall',
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

  // GEORGINA, the Cat-keeper — the optional East side-quest boss (gloamwood_dell,
  // post-Verdant). A bubbly sunshine-goth who battles with cats and one dragon-cat;
  // pitched a touch above Sable's Lowleaf band (ace 27). Her ace Gloampurr is the
  // kitten she then gifts the player. No reward flags — her script handles the gift
  // and quest closure; payout at the rival rate for a named optional bout.
  trainer_georgina: {
    id: 'trainer_georgina',
    name: 'GEORGINA',
    title: 'the Cat-keeper',
    sprite: 'georgina',
    party: [
      { species_id: 18, level: 24 }, // Hearthkit — Ember (a hearth-cat)
      { species_id: 19, level: 25 }, // Warmantis — Ember/Light (the grown fire-cat)
      { species_id: 164, level: 27 }, // Gloampurr — Lunar/Solar dragon-cat (ace)
    ],
    intro_ref: 'trainer.georgina.intro',
    defeat_ref: 'trainer.georgina.defeat',
    payout: 648, // rival 24 × ace 27
    music: 'battle-emberfall',
    ai: 'smart',
  },
  // ---- THE WILD WAYS (09-the-wild-ways.md) — one block per area lane ----------
  // the Wick-Run (A)
  runner_vess: {
    id: 'runner_vess',
    name: 'VESS',
    title: 'Runner',
    party: [
      { species_id: 11, level: 47 }, // Tallowcrest — Ember
      { species_id: 118, level: 48 }, // Helicore — Solar (ace)
    ],
    payout: 768, // route 16 × ace 48
  },
  runner_dace: {
    id: 'runner_dace',
    name: 'DACE',
    title: 'Runner',
    party: [
      { species_id: 6, level: 47 }, // Wickmere — Light/Ember
      { species_id: 115, level: 48 }, // Solvyne — Solar/Verdant
      { species_id: 19, level: 49 }, // Warmantis — Ember/Light (ace)
    ],
    payout: 784, // route 16 × ace 49
  },
  runner_tamsin: {
    id: 'runner_tamsin',
    name: 'TAMSIN',
    title: 'Runner',
    party: [
      { species_id: 11, level: 47 }, // Tallowcrest — Ember
      { species_id: 116, level: 48 }, // Auravane — Verdant/Solar (ace)
    ],
    payout: 768, // route 16 × ace 48
  },
  runner_ossie: {
    id: 'runner_ossie',
    name: 'OSSIE',
    title: 'Runner',
    party: [
      { species_id: 6, level: 47 }, // Wickmere — Light/Ember
      { species_id: 121, level: 48 }, // Sunstag — Solar/Verdant (ace)
    ],
    payout: 768, // route 16 × ace 48
  },
  runner_pip: {
    id: 'runner_pip',
    name: 'PIP',
    title: 'Runner',
    party: [
      { species_id: 115, level: 48 }, // Solvyne — Solar/Verdant
      { species_id: 19, level: 49 }, // Warmantis — Ember/Light (ace)
    ],
    payout: 784, // route 16 × ace 49
  },
  runner_rook: {
    id: 'runner_rook',
    name: 'ROOK',
    title: 'Runners\' Captain',
    party: [
      { species_id: 11, level: 48 }, // Tallowcrest — Ember
      { species_id: 121, level: 49 }, // Sunstag — Solar/Verdant
      { species_id: 12, level: 49 }, // Chandrek — Ember/Light
      { species_id: 7, level: 50 }, // Wicklord — Light/Ember (ace)
    ],
    payout: 800, // route 16 × ace 50
  },
  // the Mirelights (B)
  mire_eelcatcher: {
    id: 'mire_eelcatcher',
    name: 'MOSS',
    title: 'Eel-catcher',
    party: [
      { species_id: 28, level: 39 }, // Brinewrath — Tide
      { species_id: 61, level: 40 }, // Tidalarch — Verdant/Tide (ace)
    ],
    payout: 640, // route 16 × ace 40
  },
  mire_lampdiver: {
    id: 'mire_lampdiver',
    name: 'ODO',
    title: 'Lamp-diver',
    party: [
      { species_id: 32, level: 40 }, // Lumplass — Tide/Light
      { species_id: 68, level: 41 }, // Fernlance — Verdant/Light
      { species_id: 22, level: 42 }, // Tidwraith — Tide/Light (ace)
    ],
    payout: 672, // route 16 × ace 42
  },
  mire_acolyte: {
    id: 'mire_acolyte',
    name: 'BROTHER IVES',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 22, level: 41 }, // Tidwraith — Tide/Light
      { species_id: 32, level: 43 }, // Lumplass — Tide/Light (ace)
    ],
    payout: 688, // route 16 × ace 43
  },
  // the Rimeway (C): two rime-walkers (North era, 40-42) + the fog-walker (West era, 46-48)
  rimeway_walker_ivo: {
    id: 'rimeway_walker_ivo',
    name: 'IVO',
    title: 'Rime-walker',
    party: [
      { species_id: 75, level: 40 }, // Geodrake — Frost/Stone
      { species_id: 81, level: 41 }, // Blizzrhare — Frost (ace)
    ],
    payout: 656, // route 16 × ace 41
    music: 'battle-emberfall',
  },
  rimeway_walker_sef: {
    id: 'rimeway_walker_sef',
    name: 'SEF',
    title: 'Rime-walker',
    party: [
      { species_id: 74, level: 41 }, // Geolace — Frost/Stone
      { species_id: 78, level: 41 }, // Crystarn — Frost
      { species_id: 76, level: 42 }, // Vaultclaw — Frost/Stone (ace)
    ],
    payout: 672, // route 16 × ace 42
    music: 'battle-emberfall',
  },
  rimeway_fogwalker: {
    id: 'rimeway_fogwalker',
    name: 'DUNNE',
    title: 'Fog-walker',
    party: [
      { species_id: 134, level: 47 }, // Wispwane
      { species_id: 79, level: 47 }, // Glacitern — Frost/Storm
      { species_id: 85, level: 48 }, // Stillwarden — Frost/Dark (ace)
    ],
    payout: 768, // route 16 × ace 48
    music: 'battle-emberfall',
  },
  // the Old Seams (D): the old hands Otho let down to see the seam their grandparents sealed
  seams_miner_kester: {
    id: 'seams_miner_kester',
    name: 'KESTER',
    title: 'Seam-miner',
    party: [
      { species_id: 49, level: 29 }, // Gravelo — Stone
      { species_id: 54, level: 30 }, // Orebound — Stone (ace)
    ],
    payout: 480, // route 16 × ace 30
  },
  seams_miner_wenna: {
    id: 'seams_miner_wenna',
    name: 'WENNA',
    title: 'Seam-miner',
    party: [
      { species_id: 43, level: 30 }, // Pyrolith — Ember/Stone
      { species_id: 69, level: 31 }, // Riddlestone — Stone (ace)
    ],
    payout: 496, // route 16 × ace 31
  },
  seams_miner_tam: {
    id: 'seams_miner_tam',
    name: 'TAM',
    title: 'Seam-miner',
    party: [
      { species_id: 45, level: 30 }, // Sparkrat — Stone/Storm
      { species_id: 54, level: 31 }, // Orebound — Stone (ace)
    ],
    payout: 496, // route 16 × ace 31
  },
  seams_miner_penhal: {
    id: 'seams_miner_penhal',
    name: 'PENHAL',
    title: 'Seam-miner',
    party: [
      { species_id: 42, level: 31 }, // Coalump — Ember
      { species_id: 52, level: 32 }, // Lithonyx — Stone
      { species_id: 43, level: 33 }, // Pyrolith — Ember/Stone (ace)
    ],
    payout: 528, // route 16 × ace 33
  },
  seams_miner_jory: {
    id: 'seams_miner_jory',
    name: 'JORY',
    title: 'Seam-miner',
    party: [
      { species_id: 54, level: 32 }, // Orebound — Stone
      { species_id: 55, level: 33 }, // Ferrolith — Stone (ace)
    ],
    payout: 528, // route 16 × ace 33
  },
  // Sunvault Climb rebuild (S): the Gilt Face + the Sun Ledges (48-49)
  sunvault_suncaller: {
    id: 'sunvault_suncaller',
    name: 'IMMA',
    title: 'Sun-keeper',
    party: [
      { species_id: 122, level: 48 }, // Solray — Solar
      { species_id: 118, level: 48 }, // Helicore — Solar
      { species_id: 123, level: 49 }, // Solreach — Solar (ace)
    ],
    payout: 784, // route 16 × ace 49
    music: 'battle-emberfall',
  },

  // ---- Lane A — the Ashfall Shelf (walkthrough/10 Part II): two route trainers on
  // the shelf's chokes (route 16 × ace, 10-economy §4).
  ashfall_picker: {
    id: 'ashfall_picker',
    name: 'SILE',
    title: 'Ore-hauler',
    party: [
      { species_id: 45, level: 30 }, // Sparkrat — Stone/Storm
      { species_id: 49, level: 32 }, // Gravelo — Stone (ace)
    ],
    payout: 512, // route 16 × ace 32
  },
  ashfall_galewatch: {
    id: 'ashfall_galewatch',
    name: 'PELL',
    title: 'Gale-watch',
    party: [
      { species_id: 89, level: 31 }, // Flintbeak — Storm
      { species_id: 46, level: 33 }, // Voltcrag — Stone/Storm (ace)
    ],
    payout: 528, // route 16 × ace 33
  },
  sunvault_stargazer: {
    id: 'sunvault_stargazer',
    name: 'ORRIN',
    title: 'Star-watcher',
    party: [
      { species_id: 126, level: 48 }, // Lunveil — Light/Lunar
      { species_id: 106, level: 48 }, // Drowshorn — Lunar
      { species_id: 127, level: 49 }, // Lunvane — Light/Lunar (ace)
    ],
    payout: 784, // route 16 × ace 49
    music: 'battle-emberfall',
  },
  sunvault_ledgewatcher: {
    id: 'sunvault_ledgewatcher',
    name: 'PIM',
    title: 'Star-watcher',
    party: [
      { species_id: 124, level: 48 }, // Petalune — Lunar/Frost
      { species_id: 104, level: 49 }, // Goldmane — Solar/Stone (ace)
    ],
    payout: 784, // route 16 × ace 49
    music: 'battle-emberfall',
  },

  // ---- THE FARLAMP ISLES (walkthrough/10 Part I) — Lane C1: the two boat-trainers
  // on the sea + Bram Fathom, the isles' keeper (post-isles-dawn super-trainer) ----
  sound_oarsman: {
    id: 'sound_oarsman',
    name: 'CALDER',
    title: 'Oarsman',
    party: [
      { species_id: 173, level: 64 }, // Fathomere — Tide/Light
      { species_id: 28, level: 65 }, // Brinewrath — Tide (ace)
    ],
    payout: 1040, // route 16 × ace 65
  },
  shelf_kelper: {
    id: 'shelf_kelper',
    name: 'ROWAN',
    title: 'Kelp-farmer',
    party: [
      { species_id: 175, level: 64 }, // Beaconclaw — Stone/Light
      { species_id: 61, level: 65 }, // Tidalarch — Verdant/Tide
      { species_id: 32, level: 66 }, // Lumplass — Tide/Light (ace)
    ],
    payout: 1056, // route 16 × ace 66
  },
  // pass 2: a boat-trainer on each of the two emptiest waters
  shelf_salvager: {
    id: 'shelf_salvager',
    name: 'DUNSTAN',
    title: 'Salvager',
    party: [
      { species_id: 175, level: 65 }, // Beaconclaw — Stone/Light
      { species_id: 30, level: 66 }, // Glostrael — Tide/Light
      { species_id: 28, level: 67 }, // Brinewrath — Tide (ace)
    ],
    payout: 1072, // route 16 × ace 67
  },
  fog_pilot: {
    id: 'fog_pilot',
    name: 'WILLA',
    title: 'Fog-pilot',
    party: [
      { species_id: 176, level: 66 }, // Fogwisp
      { species_id: 85, level: 67 }, // Stillwarden — Frost/Dark
      { species_id: 173, level: 68 }, // Fathomere — Tide/Light (ace)
    ],
    payout: 1088, // route 16 × ace 68
  },
  bram_fathom: {
    id: 'bram_fathom',
    name: 'BRAM FATHOM',
    title: 'Isle Keeper',
    party: [
      { species_id: 28, level: 68 }, // Brinewrath — Tide
      { species_id: 85, level: 68 }, // Stillwarden — Frost/Dark
      { species_id: 61, level: 69 }, // Tidalarch — Verdant/Tide
      { species_id: 30, level: 69 }, // Glostrael — Tide/Light
      { species_id: 173, level: 69 }, // Fathomere — Tide/Light
      { species_id: 175, level: 70 }, // Beaconclaw — Stone/Light (ace)
    ],
    intro_ref: 'trainer.bram_fathom.intro',
    defeat_ref: 'trainer.bram_fathom.defeat',
    payout: 5600, // vigilant 80 × ace 70
    music: 'battle-nightfall',
    ai: 'smart',
  },
  // the rematch: re-runnable forever (optional income outside the solvency legs)
  bram_fathom_rematch: {
    id: 'bram_fathom_rematch',
    name: 'BRAM FATHOM',
    title: 'Isle Keeper',
    party: [
      { species_id: 28, level: 70 },
      { species_id: 85, level: 70 },
      { species_id: 61, level: 71 },
      { species_id: 30, level: 71 },
      { species_id: 173, level: 71 },
      { species_id: 175, level: 72 }, // Beaconclaw (ace)
    ],
    intro_ref: 'trainer.bram_fathom_rematch.intro',
    defeat_ref: 'trainer.bram_fathom_rematch.defeat',
    payout: 5760, // vigilant 80 × ace 72
    music: 'battle-nightfall',
    ai: 'smart',
  },
  // ---- Lane E (walkthrough/10 Part III): Lowtinder & Tinderwick Bay ------------------
  // Optional mid-game beds (Tidecall, 17-23) + Gran Tallow's post-game reef bout.
  // Payouts = class rate x ace (10-economy §4), mirrored in progression.mjs BUILT_PAYOUTS.
  bay_diver: {
    id: 'bay_diver',
    name: 'SKERRY',
    title: 'Lamp-diver',
    party: [
      { species_id: 27, level: 17 }, // Brineroll — Tide
      { species_id: 24, level: 18 }, // Shimmral — Tide/Light
      { species_id: 31, level: 19 }, // Lumpin — Tide/Light (ace)
    ],
    payout: 304, // route 16 × ace 19
    music: 'battle-emberfall',
  },
  bay_nethand: {
    id: 'bay_nethand',
    name: 'CORRA',
    title: 'Net-hand',
    party: [
      { species_id: 21, level: 18 }, // Tidmaren — Tide/Light
      { species_id: 27, level: 19 }, // Brineroll — Tide
      { species_id: 24, level: 20 }, // Shimmral — Tide/Light (ace)
    ],
    payout: 320, // route 16 × ace 20
    music: 'battle-emberfall',
  },
  lt_mudlark: {
    id: 'lt_mudlark',
    name: 'PIP',
    title: 'Eel-catcher',
    party: [
      { species_id: 14, level: 19 }, // Embrift — Ember
      { species_id: 27, level: 19 }, // Brineroll — Tide
      { species_id: 11, level: 20 }, // Tallowcrest — Ember (ace)
    ],
    payout: 320, // route 16 × ace 20
    music: 'battle-emberfall',
  },
  lt_lampwright: {
    id: 'lt_lampwright',
    name: 'HOLLIS',
    title: 'Lampwright',
    party: [
      { species_id: 16, level: 18 }, // Wickmoth — Ember
      { species_id: 6, level: 20 }, // Wickmere — Light/Ember
      { species_id: 14, level: 21 }, // Embrift — Ember (ace)
    ],
    payout: 420, // keeper 20 × ace 21
    music: 'battle-emberfall',
  },
  lt_cellar_keeper: {
    id: 'lt_cellar_keeper',
    name: 'OLD WICKMAN',
    title: 'Wick-tender',
    party: [
      { species_id: 11, level: 20 }, // Tallowcrest — Ember
      { species_id: 42, level: 21 }, // Coalump — Ember
      { species_id: 6, level: 22 }, // Wickmere — Light/Ember (ace)
    ],
    payout: 440, // keeper 20 × ace 22
    music: 'battle-emberfall',
  },
  // Gran Tallow (post-game, rematchable): Lowtinder's last Lampwarden, on her reef by
  // the old Tinder Light. Ember lamps + forty years of sea; warden-class pay.
  lowtinder_ottery: {
    id: 'lowtinder_ottery',
    name: 'GRAN TALLOW',
    title: 'Lampwarden',
    party: [
      { species_id: 12, level: 63 }, // Chandrek — Ember/Light
      { species_id: 17, level: 64 }, // Scorchwing — Ember
      { species_id: 25, level: 64 }, // Prismare — Tide/Light
      { species_id: 7, level: 64 }, // Wicklord — Light/Ember
      { species_id: 33, level: 65 }, // Embralux — Ember/Light
      { species_id: 34, level: 66 }, // Tideveil — Tide/Light (ace: forty years under the sea)
    ],
    intro_ref: 'trainer.lowtinder_ottery.intro',
    defeat_ref: 'trainer.lowtinder_ottery.defeat',
    payout: 3960, // warden 60 × ace 66
    music: 'battle-emberfall',
    ai: 'smart',
  },
  // ---- Lane C2 (10-the-farlamp-isles.md Part I): the Undertide's divers + the
  // Farlamp's second keeper (post-game, 61-66; route 16 / keeper 20 × ace).
  undertide_diver_ness: {
    id: 'undertide_diver_ness',
    name: 'NESS',
    title: 'Lamp-diver',
    party: [
      { species_id: 172, level: 60 }, // Fathomote — Tide/Light
      { species_id: 29, level: 61 }, // Glostern — Tide/Light
      { species_id: 173, level: 62 }, // Fathomere — Tide/Light (ace)
    ],
    payout: 992, // route 16 × ace 62
  },
  undertide_diver_corin: {
    id: 'undertide_diver_corin',
    name: 'CORIN',
    title: 'Lamp-diver',
    party: [
      { species_id: 174, level: 61 }, // Hermiwick — Stone/Tide
      { species_id: 28, level: 62 }, // Brinewrath — Tide
      { species_id: 61, level: 63 }, // Tidalarch — Verdant/Tide (ace)
    ],
    payout: 1008, // route 16 × ace 63
  },
  undertide_nethand_bryn: {
    id: 'undertide_nethand_bryn',
    name: 'BRYN',
    title: 'Net-hand',
    party: [
      { species_id: 85, level: 62 }, // Stillwarden — Frost/Dark
      { species_id: 176, level: 63 }, // Fogwisp — Frost/Dark
      { species_id: 175, level: 64 }, // Beaconclaw — Stone/Light (ace)
    ],
    payout: 1024, // route 16 × ace 64
  },
  undertide_keeper_isolde: {
    id: 'undertide_keeper_isolde',
    name: 'ISOLDE',
    title: 'Wick-tender',
    party: [
      { species_id: 30, level: 63 }, // Glostrael — Tide/Light
      { species_id: 25, level: 64 }, // Prismare — Tide/Light
      { species_id: 176, level: 64 }, // Fogwisp — Frost/Dark
      { species_id: 175, level: 65 }, // Beaconclaw — Stone/Light (ace)
    ],
    payout: 1300, // keeper 20 × ace 65
  },
  undertide_diver_marlo: {
    id: 'undertide_diver_marlo',
    name: 'MARLO',
    title: 'Lamp-diver',
    party: [
      { species_id: 138, level: 64 }, // Voidmantle — Dark
      { species_id: 173, level: 65 }, // Fathomere — Tide/Light
      { species_id: 55, level: 66 }, // Ferrolith — Stone (ace)
    ],
    payout: 1056, // route 16 × ace 66
  },
  // After the isles' dawn: Ondine's re-runnable bout at the Drowned Stair's head
  // (optional income, outside the one-time journey budget).
  undertide_rematch_ondine: {
    id: 'undertide_rematch_ondine',
    name: 'ONDINE',
    title: 'Lamp-diver',
    party: [
      { species_id: 30, level: 66 }, // Glostrael — Tide/Light
      { species_id: 175, level: 66 }, // Beaconclaw — Stone/Light
      { species_id: 176, level: 67 }, // Fogwisp — Frost/Dark
      { species_id: 173, level: 67 }, // Fathomere — Tide/Light (ace)
    ],
    payout: 1072, // route 16 × ace 67
  },
  // ---- Lane N3 (walkthrough/11 Parts C + D): the Mourning Fields' two acolytes (keeper
  // rate, like every northern acolyte) and the Penumbra Underways' last watch (keeper class, the Umbral Approach's).
  mournfields_ines: {
    id: 'mournfields_ines',
    name: 'INES',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 113, level: 48 }, // Omenire — Lunar/Dark
      { species_id: 180, level: 49 }, // Lullwing — Dark/Lunar (the grey dream-moth)
      { species_id: 85, level: 50 }, // Stillwarden — Frost/Dark (ace)
    ],
    payout: 1000, // keeper 20 × ace 50 (every northern acolyte pays keeper rate)
  },
  mournfields_corran: {
    id: 'mournfields_corran',
    name: 'CORRAN',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 125, level: 49 }, // Crystalune — Lunar/Frost
      { species_id: 142, level: 50 }, // Embergone — Dark/Ember
      { species_id: 138, level: 51 }, // Voidmantle — Dark (ace)
    ],
    payout: 1020, // keeper 20 × ace 51
  },
  underways_watch_a: {
    id: 'underways_watch_a',
    name: 'ODALIE',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 143, level: 52 }, // Whorlix — Storm/Dark
      { species_id: 135, level: 53 }, // Liminalux — Dark/Light
      { species_id: 138, level: 54 }, // Voidmantle — Dark (ace)
    ],
    payout: 1080, // keeper 20 × ace 54
  },
  underways_watch_b: {
    id: 'underways_watch_b',
    name: 'BRAN',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 113, level: 53 }, // Omenire — Lunar/Dark
      { species_id: 127, level: 53 }, // Lunvane — Light/Lunar
      { species_id: 85, level: 54 }, // Stillwarden — Frost/Dark
      { species_id: 142, level: 55 }, // Embergone — Dark/Ember (ace)
    ],
    payout: 1100, // keeper 20 × ace 55
  },
  underways_watch_c: {
    id: 'underways_watch_c',
    name: 'HESK',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 135, level: 54 }, // Liminalux — Dark/Light
      { species_id: 15, level: 55 }, // Pyriven — Ember/Dark
      { species_id: 138, level: 56 }, // Voidmantle — Dark (ace)
    ],
    payout: 1120, // keeper 20 × ace 56
  },
  // ---- Lane N1 (walkthrough/11 Parts A + E): the Hollowing's Country. Keeper class
  // like their Approach/Spire siblings, plain AI (they'd rather talk). Coldfog 46-50,
  // Stillwater 48-52. The Hollowing family #178-#180 is Lane N4's (ids fixed by the
  // build contract).
  coldfog_acolyte_north: {
    id: 'coldfog_acolyte_north',
    name: 'BRIN',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 136, level: 47 }, // Mothdim — Dark
      { species_id: 141, level: 48 }, // Cindersob — Dark/Ember (ace)
    ],
    payout: 960, // keeper 20 × ace 48
    music: 'battle-nightfall',
  },
  coldfog_acolyte_east: {
    id: 'coldfog_acolyte_east',
    name: 'FENWICK',
    title: 'Hollowing Elder',
    party: [
      { species_id: 133, level: 48 }, // Flutterwane — Dark/Light
      { species_id: 180, level: 48 }, // the dream-moth — Dark/Lunar
      { species_id: 137, level: 49 }, // Nullmoth — Dark (ace)
    ],
    payout: 980, // keeper 20 × ace 49
    music: 'battle-nightfall',
  },
  coldfog_acolyte_deep: {
    id: 'coldfog_acolyte_deep',
    name: 'ODRAN',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 139, level: 49 }, // WispwaneNull — Dark/Light
      { species_id: 142, level: 50 }, // Embergone — Dark/Ember (ace)
    ],
    payout: 1000, // keeper 20 × ace 50
    music: 'battle-nightfall',
  },
  coldfog_acolyte_west: {
    id: 'coldfog_acolyte_west',
    name: 'MARROW',
    title: 'Hollowing Elder',
    party: [
      { species_id: 179, level: 49 }, // the lantern-keeper — Dark/Light
      { species_id: 137, level: 49 }, // Nullmoth — Dark
      { species_id: 138, level: 50 }, // Voidmantle — Dark (ace)
    ],
    payout: 1000, // keeper 20 × ace 50
    music: 'battle-nightfall',
  },
  still_acolyte_hale: {
    id: 'still_acolyte_hale',
    name: 'HALE',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 180, level: 49 }, // the dream-moth — Dark/Lunar
      { species_id: 136, level: 49 }, // Mothdim — Dark
      { species_id: 113, level: 50 }, // Omenire — Lunar/Dark (ace)
    ],
    payout: 1000, // keeper 20 × ace 50
    music: 'battle-nightfall',
  },
  still_acolyte_vesna: {
    id: 'still_acolyte_vesna',
    name: 'VESNA',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 112, level: 50 }, // Nightwraith — Lunar
      { species_id: 179, level: 50 }, // the lantern-keeper — Dark/Light
      { species_id: 135, level: 51 }, // Liminalux — Dark/Light (ace)
    ],
    payout: 1020, // keeper 20 × ace 51
    music: 'battle-nightfall',
  },
  still_lamplighter_grisel: {
    id: 'still_lamplighter_grisel',
    name: 'GRISEL',
    title: 'Hollowing Lamplighter',
    party: [
      { species_id: 141, level: 50 }, // Cindersob — Dark/Ember
      { species_id: 179, level: 51 }, // the lantern-keeper — Dark/Light
      { species_id: 142, level: 51 }, // Embergone — Dark/Ember
      { species_id: 138, level: 52 }, // Voidmantle — Dark (ace)
    ],
    payout: 1040, // keeper 20 × ace 52
    music: 'battle-nightfall',
  },
  // ---- Lane N2 (walkthrough/11 Part B): THE DROWNLIGHT — three acolytes who
  // sit with the shutters (keeper class, sight trainers) and the SHUTTERKEEPER
  // (warden class, 'smart'; a one-time optional bout, ace = #179 the shuttered
  // lantern-keeper — lane N4's kin). Lines in content/regions/drownlight.ts.
  drownlight_acolyte_odell: {
    id: 'drownlight_acolyte_odell',
    name: 'ODELL',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 137, level: 50 }, // Nullmoth — Dark
      { species_id: 85, level: 51 }, // Stillwarden — Frost/Dark (ace)
    ],
    payout: 1020, // keeper 20 × ace 51
    music: 'battle-nightfall',
  },
  drownlight_acolyte_prue: {
    id: 'drownlight_acolyte_prue',
    name: 'PRUE',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 134, level: 51 }, // Wispwane — Dark/Light
      { species_id: 178, level: 51 }, // the snuffer-cap (#178, lane N4) — Dark/Ember
      { species_id: 87, level: 52 }, // Prismantus — Light/Frost (ace)
    ],
    payout: 1040, // keeper 20 × ace 52
    music: 'battle-nightfall',
  },
  drownlight_acolyte_hask: {
    id: 'drownlight_acolyte_hask',
    name: 'HASK',
    title: 'Hollowing Acolyte',
    party: [
      { species_id: 136, level: 52 }, // Mothdim — Dark
      { species_id: 141, level: 52 }, // Cindersob — Dark/Ember
      { species_id: 138, level: 53 }, // Voidmantle — Dark (ace)
    ],
    payout: 1060, // keeper 20 × ace 53
    music: 'battle-nightfall',
  },
  drownlight_shutterkeeper: {
    id: 'drownlight_shutterkeeper',
    name: 'MAUDRY KELL',
    title: 'Shutterkeeper',
    party: [
      { species_id: 85, level: 52 }, // Stillwarden — Frost/Dark
      { species_id: 135, level: 53 }, // Liminalux — Dark/Light
      { species_id: 113, level: 53 }, // Omenire — Lunar/Dark
      { species_id: 179, level: 54 }, // the shuttered lantern-keeper (#179, lane N4) — Dark/Light (ace)
    ],
    intro_ref: 'trainer.drownlight_shutterkeeper.intro',
    defeat_ref: 'trainer.drownlight_shutterkeeper.defeat',
    payout: 3240, // warden 60 × ace 54
    music: 'battle-nightfall',
    ai: 'smart',
  },
  // The Lumenary sparring partners (2026-10 economy review): content/sparring.ts.
  ...SPAR_TRAINERS,
};

/** Intro/defeat dialogue for trainers, kept beside the roster they belong to. */
export const TRAINER_DIALOGUE: Record<string, DialogueLine[]> = {
  // THE FARLAMP ISLES (Lane C1): Bram Fathom, the isles' keeper
  'trainer.bram_fathom.intro': [{ speaker: 'BRAM', text: 'By the lit lamp, then. Show me what the mainland\'s made of.' }],
  'trainer.bram_fathom.defeat': [{ speaker: 'BRAM', text: 'Well rowed. Well fought. The isles are yours to come and go.' }],
  'trainer.bram_fathom_rematch.intro': [{ speaker: 'BRAM', text: 'I\'ve been practising. On the gulls, mostly.' }],
  'trainer.bram_fathom_rematch.defeat': [{ speaker: 'BRAM', text: 'Again! You\'ll make an old keeper humble yet.' }],
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
  'trainer.breakwater_paul.intro': [
    { speaker: 'PAUL', text: 'On purpose. Remember that part.' },
  ],
  'trainer.breakwater_paul.defeat': [
    { speaker: 'PAUL', text: '...Set down soft as a loaf. Sid will be unbearable.' },
  ],
  'trainer.breakwater_paul_rematch.intro': [
    { speaker: 'PAUL', text: 'Back for another? Good. A man my age needs reminding he can still lose interestingly.' },
  ],
  'trainer.breakwater_paul_rematch.defeat': [
    { speaker: 'PAUL', text: 'Ha. Still here, still on purpose. Come find me again — the dark lamp keeps regular hours.' },
  ],
  'trainer.wrackline_drifter.intro': [
    { speaker: 'DRIFTER OSK', text: 'Down the wrackline, are you? Long way round to the crossroads. Tide-things in this grass have teeth — let me see if YOU do.' },
  ],
  'trainer.wrackline_drifter.defeat': [
    { speaker: 'DRIFTER OSK', text: 'Hah — teeth and then some. The cave mouth\'s on past the bend. Mind the dark; the sea talks to itself in there.' },
  ],
  'trainer.lanternfall_warden.intro': [
    { speaker: 'LAMP-KEEPER NELL', text: 'I keep the lamps down to the hub. You\'ll not pass an unlit stretch on my watch — nor an untested Wayfarer. Up they go.' },
  ],
  'trainer.lanternfall_warden.defeat': [
    { speaker: 'LAMP-KEEPER NELL', text: 'Brightly done. The crossroads is just below, where all the lit roads meet. Tell the Waykeeper Nell\'s lamps are trimmed.' },
  ],
  // R9 — the Old Light's keepers (final lines: F2.HECKLER.DEFEAT / F4.RING.DEFEAT).
  'trainer.oldlight_heckler.defeat': [
    { speaker: 'HECKLER', text: "(flips to the last card) 'YOU WIN. THE HECKLER SITS DOWN QUIETLY.'" },
    { speaker: 'HECKLER', text: '...He even wrote me losing. (sits down, loudly) Here. Your wicks. He wrote those too.' },
  ],
  'trainer.oldlight_headliners.intro': [
    { speaker: 'PUNCHWHEEL', text: 'Three clowns, one tune, NO refunds. Take it away, my darlings!' },
  ],
  'trainer.oldlight_headliners.defeat': [
    { speaker: 'PUNCHWHEEL', text: '(clockwork applause, slightly sarcastic) A tough crowd. The toughest. They will be talking about this in the lift for weeks.' },
  ],
  'trainer.oldlight_ringmaster.defeat': [
    { speaker: 'RINGMASTER', text: "HELLO! Welcome, welcome! Pull up a stool by the fire, you're going to LOVE it here!" },
    { speaker: 'RINGMASTER', text: "...Ahem. Your riddle. The machine wrote it. He's never been surer of anything. Bad sign." },
  ],
  'trainer.lampwarden_pearlmoor.intro': [
    { speaker: 'REYL WASH', text: 'Apprentice, is it. I have ferried a hundred Wayfarers across this harbour. Few read the water right.' },
    { speaker: 'REYL WASH', text: 'Tides go out so they can come back, see. Show me your bond holds against mine — then I will teach you to ask the sea to part.' },
  ],
  'trainer.lampwarden_pearlmoor.defeat': [
    { speaker: 'REYL WASH', text: 'Well rowed, Wayfarer. The Tide constellation answers you — see it shiver awake over the masts.' },
    { speaker: 'REYL WASH', text: 'The Tide Gleam is yours, and with it the Tidecall. Step to the shallows now; the moon-water will part where it would not before.' },
  ],
  'trainer.georgina.intro': [
    { speaker: 'GEORGINA', portrait: 'georgina', expr: 'delighted', text: "Oh, you brought my Pim home — and you've kin of your OWN, look at them! Right. There's only one proper way to say thank you to a fellow keeper." },
    { speaker: 'GEORGINA', portrait: 'georgina', expr: 'sunny', text: "A friendly bout! No stakes, all cuddles after. My babies have been moping in the dark all week and a good fuss is EXACTLY what they need. Mittens — wakey-wakey, sweetheart!" },
  ],
  'trainer.georgina.defeat': [
    { speaker: 'GEORGINA', portrait: 'georgina', expr: 'delighted', text: "EEE! Did you SEE them?! Lost AND adorable — best of both, that's my motto. You're a natural, you know. Come inside, I've got something for you." },
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
    { speaker: 'OTHO GRIST', portrait: 'otho', expr: 'neutral', text: 'No rush in my kin and no rush in me. We are the mountain, Wayfarer. We OUTLAST.' },
    { speaker: 'OTHO GRIST', portrait: 'otho', expr: 'grave', text: 'Show me a light that does not gutter when the rock leans in. That is all a Gleam ever was.' },
  ],
  'trainer.lampwarden_cinderhead.defeat': [
    { speaker: 'OTHO GRIST', portrait: 'otho', expr: 'proud', text: 'Hah. You did not out-hit them. You out-LASTED them. ...That, I respect. That is the deep way.' },
    { speaker: 'OTHO GRIST', portrait: 'otho', expr: 'warm', text: 'A steady light. The Stone remembers it. Come — let the vigil see what you carried up.' },
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
  // ---- Lane E (walkthrough/10 Part III): Gran Tallow on her reef ----
  'trainer.lowtinder_ottery.intro': [
    { speaker: 'GRAN TALLOW', text: 'Lampwarden of the low town, forty years on shift. Show me the light that woke the whole sky, duckling.' },
  ],
  'trainer.lowtinder_ottery.defeat': [
    { speaker: 'GRAN TALLOW', text: 'Outshone! By a Wayfarer in a borrowed boat. Oh, I haven\'t had this much fun since the water came up.' },
  ],
  // ---- Lane N2 (walkthrough/11 Part B): the Shutterkeeper ----
  'trainer.drownlight_shutterkeeper.intro': [
    { speaker: 'MAUDRY KELL', text: 'Thirty-one winters I kept this light. Let\'s see what yours is made of.' },
  ],
  'trainer.drownlight_shutterkeeper.defeat': [
    { speaker: 'MAUDRY KELL', text: 'Steady. Steady all the way down. ...My girl rowed like that.' },
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
