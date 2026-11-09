/**
 * THE WILD WAYS (2026-10, docs/world/walkthrough/09-the-wild-ways.md) — the Rimeway (C): the star-tenders' high road and the Rime Gate.
 * This area's lane OWNS this file: new scripts + dialogue only, spread into the
 * registries via regions/index.ts (a ref here must be NEW, never an override).
 *
 * Flags this file owns:
 *   flag:rimeway_ice_core     the clear-ice core cut from the Fold's frozen falls (Isel's errand)
 *   flag:has_frostglass_lens  Isel cut the Frostglass Lens (the KEY to the Mirelights' ferry — Lane B reads it)
 *   flag:rime_gate_open       the Rime Gate's bar is lifted (from the Descent, the marsh side);
 *                             the Rimeway is a road both ways and the rime-lamps wake
 *   flag:rimeway_walker_ivo_beaten / _sef_beaten / flag:rimeway_fogwalker_beaten
 *   flag:picked_rimeway_pool / _tin / _cairn / _oil / _fen
 *   flag:rimeway_refuge_seen
 *   flag:q_rimeway_lens / flag:q_rimeway_gate   JOURNAL starts (Isel's ask / Hale's tale of the gate)
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

const CORE = 'flag:rimeway_ice_core';
const LENS = 'flag:has_frostglass_lens';
const OPEN = 'flag:rime_gate_open';

export const RIMEWAY_SCRIPTS: ScriptRegistry = {
  // ---- Pale Vault: Isel the lens-grinder -------------------------------------
  'script.isel_lens': [
    { op: 'run', ref: 'script.isel_cut', if_flag: CORE },
    { op: 'run', ref: 'script.isel_ask', unless_flag: CORE },
  ],
  'script.isel_ask': [
    { op: 'say', speaker: 'ISEL', text: 'Lenses, wayfarer, ground from glacier ice. The old watchers swore by Pale Vault glass. Now it\'s mostly spectacles. Dull work.' },
    { op: 'say', speaker: 'ISEL', text: 'What I\'d LIKE to cut is a true-eye: a lens that shows a false light for what it is. For that I need clear ice — and [[the frozen falls up the Rimeway]] hold the clearest in the North.' },
    { op: 'say', speaker: 'ISEL', text: 'A fen ferryman wrote for one years back — said the lights on his mere had started lying. [[Bring me a core from the falls]] and I\'ll finally answer him.' },
    { op: 'setFlag', flag: 'flag:q_rimeway_lens' },
  ],
  'script.isel_cut': [
    { op: 'say', speaker: 'ISEL', text: 'Is that — oh, that\'s TRUE ice. Not a bubble in it. Sit down, this won\'t take long. ...Well. It will. Sit anyway.' },
    { op: 'narrate', text: 'Isel works the core on her wheel a long while, frost-dust glittering, then holds it up to the dark. Through it, the town\'s lamps look exactly like lamps.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'frostglass_lens' },
    { op: 'narrate', text: 'You got the FROSTGLASS LENS! A false light looks false through it.' },
    { op: 'say', speaker: 'ISEL', text: 'There. A true-eye. Take it to [[Old Ansel, the Saltreach ferryman]]. Tell him Pale Vault answers its letters. Eventually.' },
    { op: 'setFlag', flag: LENS },
  ],

  // ---- the Ascent ---------------------------------------------------------------
  'script.rimeway_walker_ivo': [
    { op: 'say', speaker: 'IVO', text: 'Mind the Glare below — [[read the stones before you step]], or you\'ll slide till spring. We test every climber. It\'s the only company we get.' },
    { op: 'battle', trainer: 'rimeway_walker_ivo' },
    { op: 'say', speaker: 'IVO', text: 'You climb like a tender. They came up every night with oil for the rime-lamps. Not since the dark.' },
    { op: 'setFlag', flag: 'flag:rimeway_walker_ivo_beaten' },
  ],
  'script.pickup_rimeway_pool': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'Frozen into the islet: a tender\'s spare charge. You chip it free. Found a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_rimeway_pool' },
  ],
  'script.pickup_rimeway_tin': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: 'An oil-tender\'s pay-tin under the cairn-stones, wax-sealed. Found 300 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_rimeway_tin' },
  ],

  // ---- the Fold -----------------------------------------------------------------
  'script.rimeway_ice_core': [
    { op: 'narrate', if_flag: CORE, text: 'The frozen falls, cut where you took the core. The hole is already glazing over.' },
    { op: 'narrate', unless_flag: CORE, text: 'THE FROZEN FALLS. A waterfall stopped mid-pour. At its heart, behind the white, ice so clear it hardly looks there.' },
    { op: 'sfx', key: 'world-pickup', unless_flag: CORE },
    { op: 'narrate', unless_flag: CORE, text: 'You work a CLEAR-ICE CORE free and wrap it in your coat. [[Isel in Pale Vault]] will want this.' },
    { op: 'setFlag', flag: CORE, unless_flag: CORE },
  ],
  'script.rimeway_refuge': [
    { op: 'narrate', unless_flag: 'flag:rimeway_refuge_seen', text: 'THE TENDERS\' REFUGE. Bunks for four, one jar of oil left, and a chalk rota on the wall — stopping eleven winters ago.' },
    { op: 'setFlag', flag: 'flag:rimeway_refuge_seen' },
    { op: 'heal', sleep: false },
    { op: 'narrate', text: 'The stove still draws. You and your kin warm through. Rested.' },
  ],
  'script.tender_hale': [
    { op: 'say', speaker: 'HALE', text: 'A visitor! Up the Rimeway! Sit, sit. I\'m Hale — last of the rime-tenders. I keep one lamp lit. Can\'t carry oil for the rest alone.' },
    { op: 'say', speaker: 'HALE', unless_flag: OPEN, text: 'The road ran north through the gate to the marshes and Nightreach. The Wardens of the Quiet [[barred it from the marsh side]] — to keep the fog in, they said. To keep us out, I think.' },
    { op: 'setFlag', flag: 'flag:q_rimeway_gate' },
    { op: 'say', speaker: 'HALE', unless_flag: OPEN, text: '[[Come up from the marsh]] and you could lift that bar in a breath. From here? Stare through the grille all you like.' },
    { op: 'say', speaker: 'HALE', if_flag: OPEN, text: 'You lifted it! The bar rang off the col like a bell, and the lamps are back down the whole road. Oil-runs again. My knees are furious. I\'ve never been happier.' },
    { op: 'say', speaker: 'HALE', unless_flag: CORE, text: 'If you pass the falls — [[Isel in Pale Vault]] is always after clear ice. Never could get up here herself.' },
  ],
  'script.rimeway_walker_sef': [
    { op: 'say', speaker: 'SEF', text: 'You came over the Glare? On purpose? Then meet a Vaultclaw — they live nowhere else in the world. Mine first.' },
    { op: 'battle', trainer: 'rimeway_walker_sef' },
    { op: 'say', speaker: 'SEF', text: 'The wild ones den up here. Go gently — they\'ve had the Fold to themselves a long while.' },
    { op: 'setFlag', flag: 'flag:rimeway_walker_sef_beaten' },
  ],
  'script.pickup_rimeway_cairn': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'In the tenders\' cairn, an offering nobody came back for. Found a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:picked_rimeway_cairn' },
  ],

  // ---- the Descent (the marsh end) ------------------------------------------------
  'script.rime_gate_lift': [
    { op: 'letterbox', on: true },
    { op: 'narrate', text: 'THE RIME GATE — and this side, the bar: black iron in its brackets, wired with grey cord. A Hollowing knot. Neat. Patient.' },
    { op: 'narrate', text: 'The cord gives. You shoulder the beam and it lifts — heavier than it looks, then all at once light.' },
    { op: 'sfx', key: 'world-door' },
    { op: 'shake', ms: 500, intensity: 0.004 },
    { op: 'setFlag', flag: OPEN },
    { op: 'narrate', text: 'The gate swings. Cold, clean air pours down from the Fold — and one by one, all along the high road, the rime-lamps catch and burn.' },
    { op: 'letterbox', on: false },
  ],
  'script.rime_acolyte': [
    { op: 'say', speaker: 'ACOLYTE', unless_flag: OPEN, text: 'You\'re going to lift it. I can see it in how you stand. ...I won\'t stop you. I\'m not here to stop anyone. I\'m here because someone should be.' },
    { op: 'say', speaker: 'ACOLYTE', unless_flag: OPEN, text: 'We barred it so the fog would stay down here, quiet, and nothing would come down to wake the marsh. It seemed kind. Most of what we did seemed kind.' },
    { op: 'say', speaker: 'ACOLYTE', if_flag: OPEN, text: 'So that\'s the sound the lamps make, coming back. I\'d forgotten. ...Go on. The road\'s yours. I\'ll stay and watch a while.' },
  ],
  'script.rimeway_fogwalker': [
    { op: 'say', speaker: 'DUNNE', text: 'Fog in the marsh, ice on the ridge, and a stranger strolling between. Show me what keeps you warm.' },
    { op: 'battle', trainer: 'rimeway_fogwalker' },
    { op: 'say', speaker: 'DUNNE', text: 'Warm enough. [[The gate\'s at the ridge\'s end]]. The Wardens\' acolyte will be there — don\'t be hard on her. She\'s the only one who still comes up.' },
    { op: 'setFlag', flag: 'flag:rimeway_fogwalker_beaten' },
  ],
  'script.pickup_rimeway_oil': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'bright_balm', count: 2 },
    { op: 'say', text: 'A tender\'s oil-satchel, dropped the night the gate was barred. Found 2 BRIGHT BALMS!' },
    { op: 'setFlag', flag: 'flag:picked_rimeway_oil' },
  ],
  'script.pickup_rimeway_fen': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 400 },
    { op: 'say', text: 'Half-sunk in the drained fen, a lamp-tithe box, coins still in it. Found 400 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_rimeway_fen' },
  ],
};

export const RIMEWAY_DIALOGUE: DialogueRegistry = {
  'npc.isel_after': [
    { speaker: 'ISEL', text: 'Through a true-eye a false light just looks... tired. A lamp with nobody behind it. Take care with what you see.' },
  ],
  'sign.pale_vault_rimeway': [
    { text: 'NORTH — [[THE RIMEWAY]]. The tenders\' high road to the Fold and the Rime Gate. Ice, ladders, the Glare. Read the stones.' },
  ],
  'sign.rimeway_foot': [
    { text: 'THE RIMEWAY. Rime-lamps every hundred paces. (Newer paint:) NO OIL SINCE THE DARK. CLIMB WITH YOUR OWN LIGHT.' },
    { text: '(Chalked under it:) THE VAULT\'S WARDEN WALKS IT FIRST. SO SHOULD YOU.' },
  ],
  'sign.rimeway_glare': [
    { text: 'THE GLARE. Wind-polished: [[you slide till something stops you]], so pick what. Ladder [[far north-west]].' },
  ],
  'npc.rimeway_walker_ivo_after': [
    { speaker: 'IVO', text: 'Read the stones. They never move. That\'s the whole trick of the Glare.' },
  ],
  'npc.rime_gate_barred': [
    { text: 'THE RIME GATE. Through the grille, a ridge road falls north into fog. The bar is [[on the far side]], wired shut. From here it won\'t move.' },
  ],
  'sign.rimeway_falls': [
    { text: 'THE FROZEN FALLS. Do not cross the plunge pool unless you mean to. (Scratched:) THE CLEAREST ICE IN THE NORTH IS BEHIND THE WHITE.' },
  ],
  'sign.rimeway_fold': [
    { text: 'THE FOLD. The top of the Rimeway. Refuge north-east. The Rime Gate beyond — closed, by order of the Wardens of the Quiet.' },
  ],
  'npc.rimeway_walker_sef_after': [
    { speaker: 'SEF', text: 'Vaultclaws, Hale\'s lamp and me. That\'s the Fold\'s whole population.' },
  ],
  'npc.rime_gate_wrongside': [
    { text: 'The Rime Gate. The bar is down, wired with grey cord. Step up to it and you could lift it.' },
  ],
  'sign.rimeway_marsh_end': [
    { text: 'THE RIMEWAY — MARSH END. To the Fold and Pale Vault. (A newer board, nailed over:) ROAD CLOSED. BY ORDER OF THE WARDENS OF THE QUIET.' },
  ],
  'sign.rimeway_hollowing_notice': [
    { text: 'NOTICE. This gate is barred so that the marsh may rest. Please do not lift it. Please do not be unkind to the one who keeps it. — The Wardens of the Quiet' },
  ],
  'npc.rimeway_fogwalker_after': [
    { speaker: 'DUNNE', text: 'Ridge road home\'s quicker than the marsh, once that gate\'s up. Wish I\'d had the nerve years ago.' },
  ],
};
