/**
 * THE WILD WAYS (2026-10, docs/world/walkthrough/09-the-wild-ways.md) — the
 * Sunvault Climb rebuilt as a mountain face (S): four maps of ladders, ledges,
 * planks and the trestle over the gully. Climb I/II keep their old refs (in
 * scripts.ts / dialogue.ts); everything NEW on the face lives here.
 * This area's lane OWNS this file: new scripts + dialogue only, spread into the
 * registries via regions/index.ts (a ref here must be NEW, never an override).
 *
 * Flags this file owns:
 *   flag:sunvault_suncaller_beaten / _stargazer_beaten / _ledgewatcher_beaten  (sight trainers)
 *   flag:picked_sunvault_gully / _pitch / _ledge_tin / _brass                   (caches)
 *   flag:sunvault_shelter_seen                                                   (the shelter's tally line, once)
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

export const SUNVAULT_SCRIPTS: ScriptRegistry = {
  // ---- the Gilt Face (climb III) ----------------------------------------------
  'script.sunvault_keepers_shelter': [
    { op: 'narrate', text: 'The sun-keepers\' shelter: a stone lean-to pegged into the face, a bench, a tin of mirror-polish gone hard as amber.' },
    { op: 'action', actor: 'player', action: 'sit', holdMs: 1200 },
    { op: 'narrate', text: 'Every dawn they climbed this far to wipe the frost off the watchers\' mirrors, and rested here on the way down. Nobody has needed the bench for eleven winters. It holds you anyway.', unless_flag: 'flag:sunvault_shelter_seen' },
    { op: 'setFlag', flag: 'flag:sunvault_shelter_seen' },
    { op: 'heal', sleep: false },
    { op: 'narrate', text: 'Your kin curl in out of the wind. Rested. The top of the face is close now.' },
  ],
  'script.sunvault_spyglass': [
    { op: 'narrate', text: 'An old brass spyglass, bolted to the rock and aimed down the face. Through it: the shelves you climbed, the trestle like a stitch across the gully, and far below, the drowned gold of the Solarium.' },
    { op: 'narrate', text: 'Swing it up and there is only stone — and above the stone, stars. Not long now.' },
  ],
  'script.sunvault_suncaller': [
    { op: 'say', speaker: 'IMMA', text: 'A climber! The keepers used to call the sun up from this shelf, you know — one note, every dawn. I still practise. Tell me if it sounds like morning.' },
    { op: 'battle', trainer: 'sunvault_suncaller' },
    { op: 'say', speaker: 'IMMA', text: 'Not morning yet, then. But you made it sound closer. Ladder\'s to the west — keep three points on the rungs and your eyes off the drop.' },
    { op: 'setFlag', flag: 'flag:sunvault_suncaller_beaten' },
  ],
  'script.sunvault_stargazer': [
    { op: 'say', speaker: 'ORRIN', text: 'Shh — I\'m counting. Seven up there, and the eighth not yet... You\'ve the look of someone who\'s been relighting them. Prove it, and I\'ll lose count gladly.' },
    { op: 'battle', trainer: 'sunvault_stargazer' },
    { op: 'say', speaker: 'ORRIN', text: 'Proved. The gully behind me? Drop in if you like — you\'ll walk out under the old trestle, all the way to the lower shelf. Keepers used it as a quick way home.' },
    { op: 'setFlag', flag: 'flag:sunvault_stargazer_beaten' },
  ],
  'script.pickup_sunvault_gully': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'Wedged in the top of the slot, where the keepers dropped in: a waxed pouch, forgotten. Found a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_gully' },
  ],
  'script.pickup_sunvault_pitch': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A keeper\'s cubby cut into the face, halfway up nothing. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_pitch' },
  ],

  // ---- the Sun Ledges (climb IV) -----------------------------------------------
  'script.sunvault_ledgewatcher': [
    { op: 'say', speaker: 'PIM', text: 'Steady! One at a time on the planks — that\'s the rule, and I\'m the rule. You can cross when you\'ve crossed ME.' },
    { op: 'battle', trainer: 'sunvault_ledgewatcher' },
    { op: 'say', speaker: 'PIM', text: 'All right, all right. Mind the third board, it sings. Nightreach is two ledges up — you\'ll hear the dome before you see it.' },
    { op: 'setFlag', flag: 'flag:sunvault_ledgewatcher_beaten' },
  ],
  'script.sunvault_hill_spyglass': [
    { op: 'narrate', text: 'The watchers\' spyglass on the hill. North, the dome of Nightreach Observatory, its seven lamps a horseshoe of patient light. East, a grey smudge where the marshes lie, and above them a high white road along the col — the old rime-lamps, all of them dark.' },
    { op: 'narrate', text: 'Up here the sky is the densest you have ever seen it. Seven constellations hang lit. One space waits.' },
  ],
  'script.pickup_sunvault_ledge_tin': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 350 },
    { op: 'say', text: 'At the very end of the ledge, a watcher\'s tin pegged to the rock against the wind. Found 350 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_ledge_tin' },
  ],
  'script.pickup_sunvault_brass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 2 },
    { op: 'say', text: 'A coil of spare brass pegs and, under them, a climber\'s kit. Found 2 BRIGHT BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_brass' },
  ],
};

export const SUNVAULT_DIALOGUE: DialogueRegistry = {
  // ---- climb I / II (new signs on the rebuilt face) ---------------------------
  'npc.sunvault_wayfarer_face': [
    { speaker: 'RESTING WAYFARER', text: 'I\'ve walked every lit road in Vesperholm, and this is the first that goes straight UP. Ladders the whole way, and ledges, and planks over nothing. Rest a while. The eighth Lumenary has kept for years; it\'ll keep while your knees stop shaking.' },
  ],
  'sign.sunvault_face': [
    { text: 'THE SUNVAULT FACE. Ladders pegged by the sun-keepers. Climb facing the rungs; come down the same. The quick way home is the WEST NOTCH — one way only.' },
  ],
  'sign.sunvault_cleft': [
    { text: 'THE CLEFT. One plank, one climber. If it sways, that is the plank\'s business, not yours.' },
  ],
  // ---- climb III ------------------------------------------------------------
  'sign.sunvault_gilt_face': [
    { text: 'THE GILT FACE. Four pitches to the Sun Ledges, a shelter at the top. The keepers\' trestle crosses the gully on the second shelf — stay on the boards.' },
  ],
  'sign.sunvault_gully': [
    { text: 'THE GULLY. A drop in, a walk down, out under the trestle to the lower shelf. There is no climbing back up it. (The keepers called it "the quick way to breakfast.")' },
  ],
  'npc.sunvault_suncaller_after': [
    { speaker: 'IMMA', text: 'One note, every dawn. One day it will work again, and I intend to be in tune.' },
  ],
  'npc.sunvault_stargazer_after': [
    { speaker: 'ORRIN', text: 'Seven... and the space for an eighth. I keep counting it, in case I\'m wrong.' },
  ],
  // ---- climb IV --------------------------------------------------------------
  'sign.sunvault_sun_ledges': [
    { text: 'THE SUN LEDGES. Watchers\' pegs, keepers\' planks. The last of the climb — and the most exposed. NORTH: NIGHTREACH OBSERVATORY.' },
  ],
  'sign.sunvault_observatory_hill': [
    { text: 'OBSERVATORY HILL. NORTH — NIGHTREACH. The watchers keep seven lamps for seven stars. Walk toward the brightest sky in Vesperholm.' },
  ],
  'npc.sunvault_ledgewatcher_after': [
    { speaker: 'PIM', text: 'Third board sings. Told you.' },
  ],
  'npc.sunvault_hill_watcher': [
    { speaker: 'HILL WATCHER', text: 'The sun-keepers climbed to wipe the mirrors and we watchers climbed down to fetch the post — we met on these ledges every morning. Two orders, one job: keep the lights. Then the dark came and the job got lonelier.' },
    { speaker: 'HILL WATCHER', text: 'Look east, past the marsh. That line of dead lamps along the col is the Rimeway — the star-tenders\' high road to the Pale Vault. Barred, these days. From the marsh side, mind.' },
  ],
};
