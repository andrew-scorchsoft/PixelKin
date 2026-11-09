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
    { op: 'narrate', text: 'The sun-keepers\' shelter: a stone lean-to, a bench, a tin of mirror-polish gone hard as amber.' },
    { op: 'action', actor: 'player', action: 'sit', holdMs: 1200 },
    { op: 'narrate', text: 'Every dawn they climbed here to wipe frost off the watchers\' mirrors. Nobody has needed the bench for eleven winters. It holds you anyway.', unless_flag: 'flag:sunvault_shelter_seen' },
    { op: 'setFlag', flag: 'flag:sunvault_shelter_seen' },
    { op: 'heal', sleep: false },
    { op: 'narrate', text: 'Your kin curl in out of the wind. Rested. The top of the face is close now.' },
  ],
  'script.sunvault_spyglass': [
    { op: 'narrate', text: 'A brass spyglass, aimed down the face: the shelves you climbed, the gully\'s trestle, and far below, the Solarium\'s drowned gold.' },
    { op: 'narrate', text: 'Swing it up and there is only stone — and above the stone, stars. Not long now.' },
  ],
  'script.sunvault_suncaller': [
    { op: 'say', speaker: 'IMMA', text: 'A climber! The keepers called the sun up from this shelf — one note, every dawn. I still practise. Tell me if it sounds like morning.' },
    { op: 'battle', trainer: 'sunvault_suncaller' },
    { op: 'say', speaker: 'IMMA', text: 'Not morning yet. But closer. [[Ladder\'s to the west]] — eyes off the drop.' },
    { op: 'setFlag', flag: 'flag:sunvault_suncaller_beaten' },
  ],
  'script.sunvault_stargazer': [
    { op: 'say', speaker: 'ORRIN', text: 'Shh — counting. Seven up there, the eighth not yet... You look like you\'ve been relighting them. Prove it, and I\'ll lose count gladly.' },
    { op: 'battle', trainer: 'sunvault_stargazer' },
    { op: 'say', speaker: 'ORRIN', text: 'Proved. [[The gully behind me]] comes out under the trestle. Quick way home.' },
    { op: 'setFlag', flag: 'flag:sunvault_stargazer_beaten' },
  ],
  'script.pickup_sunvault_gully': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'A forgotten waxed pouch at the top of the slot. Found a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_gully' },
  ],
  'script.pickup_sunvault_pitch': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A keeper\'s cubby, halfway up nothing. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_pitch' },
  ],

  // ---- the Sun Ledges (climb IV) -----------------------------------------------
  'script.sunvault_ledgewatcher': [
    { op: 'say', speaker: 'PIM', text: 'Steady! One at a time on the planks. That\'s the rule, and I\'m the rule.' },
    { op: 'battle', trainer: 'sunvault_ledgewatcher' },
    { op: 'say', speaker: 'PIM', text: 'All right. Mind the third board, it sings. [[Nightreach is two ledges up]] — you\'ll hear the dome before you see it.' },
    { op: 'setFlag', flag: 'flag:sunvault_ledgewatcher_beaten' },
  ],
  'script.sunvault_hill_spyglass': [
    { op: 'narrate', text: 'The watchers\' spyglass. North, Nightreach\'s dome, seven lamps in a patient horseshoe. East, along the col, a line of rime-lamps, all dark.' },
    { op: 'narrate', text: 'The sky up here is the densest you have ever seen it. Seven constellations lit. One space waits.' },
  ],
  'script.pickup_sunvault_ledge_tin': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 350 },
    { op: 'say', text: 'A watcher\'s tin, pegged against the wind. Found 350 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_ledge_tin' },
  ],
  'script.pickup_sunvault_brass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 2 },
    { op: 'say', text: 'Under a coil of brass pegs, a climber\'s kit. Found 2 BRIGHT BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_sunvault_brass' },
  ],
};

export const SUNVAULT_DIALOGUE: DialogueRegistry = {
  // ---- climb I / II (new signs on the rebuilt face) ---------------------------
  'npc.sunvault_wayfarer_face': [
    { speaker: 'RESTING WAYFARER', text: 'Every lit road in Vesperholm, and the first straight UP. Rest. The eighth Lumenary will keep while your knees stop shaking.' },
  ],
  'sign.sunvault_face': [
    { text: 'THE SUNVAULT FACE. Climb facing the rungs. Quick way home: [[the WEST NOTCH]], one way.' },
  ],
  'sign.sunvault_cleft': [
    { text: 'THE CLEFT. One plank, one climber. If it sways, that\'s its business.' },
  ],
  // ---- climb III ------------------------------------------------------------
  'sign.sunvault_gilt_face': [
    { text: 'THE GILT FACE. Four pitches to [[the Sun Ledges]]. Stay on the trestle\'s boards.' },
  ],
  'sign.sunvault_gully': [
    { text: 'THE GULLY. Drop in, walk out under the trestle to the lower shelf. No climbing back. (The keepers\' "quick way to breakfast.")' },
  ],
  'npc.sunvault_suncaller_after': [
    { speaker: 'IMMA', text: 'One note, every dawn. One day it will work again, and I intend to be in tune.' },
  ],
  'npc.sunvault_stargazer_after': [
    { speaker: 'ORRIN', text: 'Seven... and the space for an eighth. I keep counting it, in case I\'m wrong.' },
  ],
  // ---- climb IV --------------------------------------------------------------
  'sign.sunvault_sun_ledges': [
    { text: 'THE SUN LEDGES. The last, most exposed climb. NORTH: [[NIGHTREACH]].' },
  ],
  'sign.sunvault_observatory_hill': [
    { text: 'OBSERVATORY HILL. NORTH — [[NIGHTREACH]]. Walk toward the brightest sky.' },
  ],
  'npc.sunvault_ledgewatcher_after': [
    { speaker: 'PIM', text: 'Third board sings. Told you.' },
  ],
  'npc.sunvault_hill_watcher': [
    { speaker: 'HILL WATCHER', text: 'Keepers climbing up, watchers down: we met here every morning. Two orders, one job: keep the lights. Then the dark came, and it got lonelier.' },
    { speaker: 'HILL WATCHER', text: 'Those dead lamps along the col, east, are [[the Rimeway]] to Pale Vault. Barred these days — [[from the marsh side]].' },
  ],
};
