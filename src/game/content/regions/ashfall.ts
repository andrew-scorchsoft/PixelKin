/**
 * Lane A (2026-10, docs/world/walkthrough/10-the-farlamp-isles.md Part II) — the
 * Ashfall Shelf, Kiln Gully, and the Cinderwind Scarp's rockfall.
 * This lane OWNS this file: new scripts + dialogue only, spread into the
 * registries via regions/index.ts (a ref here must be NEW, never an override).
 *
 * Flags this file owns:
 *   flag:scarp_rockfall_clear   the Galehigh haulers promise the Scarp cut (set by the
 *                               landing band on Galehigh's upper west road). Read through
 *                               the DERIVED flag:scarp_short_open (= this OR gleam:storm).
 *   flag:ashfall_camp_rested    the first night at the haulers' brazier (longer narration)
 *   flag:ashfall_picker_beaten / flag:ashfall_galewatch_beaten
 *   flag:picked_ashfall_nook / _ashfall_tin / _ashfall_lunchtin / _kiln_beacon / _kiln_chart
 *   flag:q_north_pane_hook      Oda Kilnwright tells you about the last pane (JOURNAL start)
 *   flag:q_north_pane           the pane taken from Kiln Gully's drying loft
 *   flag:q_north_pane_done      the pane set in the kite-stall lamp at Galehigh
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

const HOOK = 'flag:q_north_pane_hook';
const PANE = 'flag:q_north_pane';
const DONE = 'flag:q_north_pane_done';

export const ASHFALL_SCRIPTS: ScriptRegistry = {
  // The gallery mouth out of Cinderhead Deep, chained until Otho's Gleam (2026-10:
  // keeps the Stone Gleam on the thread — it used to be skippable).
  'script.scarp_climb_chained': [
    { op: 'narrate', text: 'A hauler\'s chain, and a slate: NOBODY CLIMBS TILL OTHO\'S TESTED THEM.' },
    { op: 'narrate', text: '[[Otho Grist]] keeps [[the headframe hall]], back up in the mine.' },
  ],
  // ---- Cinderwind Scarp: the rockfall (the return compressor) -----------------------
  'script.scarp_rockfall_blocked': [
    { op: 'emote', actor: 'rockfall_hauler', emote: 'alert' },
    { op: 'face', actor: 'rockfall_hauler', facing: 'left' },
    { op: 'say', speaker: 'HAULER', text: 'Whoa, love! Half the ridge came down on the old cut. You\'ll not reach Galehigh this way.' },
    { op: 'say', speaker: 'HAULER', text: 'Go [[up and round by the Ashfall]]: west to the crest-wood gap, then over the tips.' },
    { op: 'say', speaker: 'HAULER', text: 'Galehigh\'s lot have picks. Tell them Cinderhead\'s waiting on its cut?' },
    { op: 'move', actor: 'player', to: { tx: 19, ty: 4 } },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'face', actor: 'rockfall_hauler', facing: 'up' },
  ],
  'script.scarp_rockfall_hauler': [
    { op: 'say', speaker: 'HAULER', text: 'Thirty tons of ridge. Start at the bottom rock. It\'s always the bottom one.' },
    { op: 'say', speaker: 'HAULER', text: '[[Up and round by the Ashfall]], love: west to the crest-wood gap, over the tips.' },
  ],
  // Galehigh's upper west road, the first time you arrive by the Ashfall.
  'script.ashfall_rockfall_promise': [
    { op: 'narrate', text: 'Two Galehigh haulers shoulder picks by the old Scarp road. One eyes your ashy boots.' },
    { op: 'say', speaker: 'GALEHIGH HAULER', text: 'Came round by the Ashfall? Then you\'ve seen the Scarp cut. Cinderhead\'s shouted all week.' },
    { op: 'say', speaker: 'GALEHIGH HAULER', text: 'Leave it with us. By the time you head home, [[the short way down]] will be clear.' },
    { op: 'narrate', text: 'They tramp off toward the cut, arguing about which rock to start on.' },
  ],

  // ---- The Ashfall Shelf -------------------------------------------------------------
  'script.ashfall_brazier_rest': [
    { op: 'say', speaker: 'HAULER', text: 'Sit in, sit in. Haulers\' rule: nobody passes a lit brazier without warming their kin.', unless_flag: 'flag:ashfall_camp_rested' },
    { op: 'narrate', text: 'The night is wide and grey. The brazier ticks, and below, the mine still breathes.', unless_flag: 'flag:ashfall_camp_rested' },
    { op: 'setFlag', flag: 'flag:ashfall_camp_rested' },
    { op: 'heal' },
    { op: 'narrate', text: 'Your kin wake warm, smelling of coal-smoke. Galehigh is over the tips.' },
  ],
  'script.ashfall_vista': [
    { op: 'narrate', text: 'Across the gulf the whole Windward Stair climbs into the cold, cairn after cairn.' },
    { op: 'narrate', text: 'At your feet the wind pours up the gap: a draught a kite could lie on all the way across.' },
    { op: 'say', speaker: 'NOTCHED ON THE CAIRN', text: '"GALE-WATCH POST. Wind rising: kites out. Wind falling: kites home. Wind both: go and ask Mira."' },
  ],
  'script.oda_kilnwright': [
    // a precedence chain (latest stage first) so any flag mix plays exactly one stage
    { op: 'run', ref: 'script.oda_after', if_flag: DONE },
    { op: 'run', ref: 'script.oda_before_done', unless_flag: DONE },
  ],
  'script.oda_before_done': [
    { op: 'run', ref: 'script.oda_has_pane', if_flag: PANE },
    { op: 'run', ref: 'script.oda_open', unless_flag: PANE },
  ],
  'script.oda_open': [
    { op: 'run', ref: 'script.oda_remind', if_flag: HOOK },
    { op: 'run', ref: 'script.oda_hook', unless_flag: HOOK },
  ],
  'script.oda_hook': [
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'Mind the ash, dear. It gets in everything. Especially the tea.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'That stack was ours: lamp-glass for half the valleys. Then the dark came, and we let the fire go.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: '[[One pane is left]] in the gully. And [[Galehigh\'s kite-stall lamp]] stands blind.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'The stack breathes hot air. [[Ride its draught up]] and fetch the pane, would you?' },
    { op: 'setFlag', flag: HOOK },
  ],
  'script.oda_remind': [
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'The last pane\'s in [[the gully loft]]. Ride the stack\'s draught up, then take it to [[Galehigh\'s kite-stall lamp]].' },
  ],
  'script.oda_has_pane': [
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'Oh, look at it. Father said the last one out of a kiln is the warmest.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'And the stack\'s smoking! You woke the old girl. She was only sleeping.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'Don\'t give it to me, dear. [[Take it to Galehigh\'s kite-stall lamp]].' },
  ],
  'script.oda_after': [
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'A kite-hand came down to say the kite-stall lamp is lit. Amber. Like a sunset in a jar.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'I might go up and see it. Once the tea\'s brewed. Once the ash settles. Soon.' },
  ],
  'script.pickup_ashfall_nook': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Under old ash: a STARGLASS SHARD, still faintly warm. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_ashfall_nook' },
  ],
  'script.pickup_ashfall_lunchtin': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'A hauler\'s forgotten lunch-tin. Packed in ash at the bottom: a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_ashfall_lunchtin' },
  ],
  'script.pickup_ashfall_tin': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A tin marked "FOR THE NEXT ONE UP". Inside: a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_ashfall_tin' },
  ],
  'script.ashfall_picker': [
    { op: 'say', speaker: 'SILE', text: 'Up the slag cut on foot? Good. Let\'s see if your kin can carry their weight.' },
    { op: 'battle', trainer: 'ashfall_picker' },
    { op: 'say', speaker: 'SILE', text: 'Heavy hitters. Fine. [[Galehigh\'s east]], down past the gale-watch.' },
    { op: 'setFlag', flag: 'flag:ashfall_picker_beaten' },
  ],
  'script.ashfall_galewatch': [
    { op: 'say', speaker: 'PELL', text: 'Gale-watch! The wind wants a look at you before the top road. It says: a bout.' },
    { op: 'battle', trainer: 'ashfall_galewatch' },
    { op: 'say', speaker: 'PELL', text: 'The wind says go on. [[Galehigh\'s down and east]]. Hear pipes? You\'re close.' },
    { op: 'setFlag', flag: 'flag:ashfall_galewatch_beaten' },
  ],

  // ---- Kiln Gully ----------------------------------------------------------------------
  'script.kiln_last_pane': [
    { op: 'narrate', text: 'On the loft\'s drying rack, wrapped in stiff cloth: one pane of amber lamp-glass, undimmed.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'kiln_pane' },
    { op: 'narrate', text: 'You got THE LAST PANE!' },
    { op: 'setFlag', flag: PANE },
    // the "oh!" beat: lifting the last pane off the rack, the cold furnace wakes
    { op: 'shake', ms: 300, intensity: 0.004 },
    { op: 'cameraFocus', to: { tx: 10, ty: 3 }, ms: 700 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'flashColor', color: '#ff8a3a', ms: 500 },
    { op: 'narrate', text: 'Behind you, eleven winters of banked coal catch. Warm orange light runs across the hall.' },
    { op: 'narrate', text: 'It knew the last pane was going home.' },
    { op: 'cameraReset', ms: 600 },
    { op: 'narrate', text: '[[Galehigh\'s kite-stall lamp]] stands blind for want of glass. This would fit it.', unless_flag: HOOK },
    { op: 'narrate', text: 'Oda said [[the lamp by Galehigh\'s kite-stall]]. A short glide away now.', if_flag: HOOK },
  ],
  'script.pickup_kiln_beacon': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A lamp-wright\'s rusted strongbox. Inside, in straw: a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_kiln_beacon' },
  ],
  'script.pickup_kiln_chart': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'chart_shardstorm', count: 1 },
    { op: 'say', text: 'Pinned behind the glass crates: a STAR-CHART: SHARDSTORM!' },
    { op: 'setFlag', flag: 'flag:picked_kiln_chart' },
  ],
  'script.kiln_furnace_lore': [
    { op: 'narrate', text: 'The great furnace is cold, but deep inside a few coals still blink.' },
    { op: 'narrate', text: 'A brass plate: "KILNWRIGHT & DAUGHTERS. GLASS FOR EVERY VALLEY." Someone still polishes it.' },
  ],
  'script.galehigh_pane_lamp': [
    { op: 'run', ref: 'script.galehigh_pane_lamp_lit', if_flag: DONE },
    { op: 'run', ref: 'script.galehigh_pane_set', if_flag: PANE, unless_flag: DONE },
    { op: 'run', ref: 'script.galehigh_pane_blind', unless_flag: PANE },
  ],
  'script.galehigh_pane_blind': [
    { op: 'narrate', text: 'The lamp by the kite-stall stands blind, its pane cracked, its flame guttering.' },
    { op: 'say', speaker: 'KITE-MAKER', text: 'Storm took the glass. Nobody\'s drawn lamp-glass since the Kilnwrights\' fire went out.', unless_flag: HOOK },
    { op: 'narrate', text: 'Oda Kilnwright\'s last pane would fit it exactly.', if_flag: HOOK },
  ],
  'script.galehigh_pane_set': [
    { op: 'say', speaker: 'KITE-MAKER', text: 'Is that... Kilnwright glass? A new pane! Hold the lamp steady. Steadier. There!' },
    { op: 'takeItem', item: 'kiln_pane' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'setFlag', flag: DONE },
    { op: 'flashColor', color: '#ffb347', ms: 400 },
    { op: 'narrate', text: 'The flame steadies, and the kite-stall turns amber, like a sunset in a jar.' },
    { op: 'say', speaker: 'KITE-MAKER', text: 'Tell Oda it\'s lit! No, I\'ll send a kite-hand. Take this, from the festival purse.' },
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: 1200 },
    { op: 'narrate', text: 'You received 1,200 wicks!' },
  ],
  'script.galehigh_pane_lamp_lit': [
    { op: 'narrate', text: 'The kite-stall lamp burns amber behind the Kilnwrights\' last pane.' },
  ],
};

export const ASHFALL_DIALOGUE: DialogueRegistry = {
  'sign.cinderwind_ashfall': [
    { text: 'THE ASHFALL SHELF\nSOUTH: the Scarp and the mine. EAST: [[Galehigh\'s top road]].' },
    { text: 'Burnt into the board: "Mind where you dig. Mind more what you find."' },
  ],
  'sign.ashfall_century': [
    { text: 'A tipping-stone, notched once for every cart of slag tipped over the edge.' },
    { text: 'The last row stops halfway: "LAMPS OUT. CARTS STOPPED. THE GRASS CAN HAVE IT."' },
  ],
  'sign.ashfall_gate': [
    { text: 'GALEHIGH TERRACES, EAST.\nLeave the ash on THIS side of the gate.' },
  ],
  'sign.kiln_tally': [
    { text: 'A tally-board by the gully mouth, the last column half-finished: "PANES DRAWN, WINTER OF THE LONG DUSK: 1."' },
  ],
  'npc.kiln_rack_lore': [
    { text: 'Half-made lamp-globes on the rack, each scratched with the valley it was for.' },
  ],
  'npc.ashfall_windgap': [
    { text: 'The wind pours up toward the Windward Stair. Only [[a thermal-riding kin]] could cross.' },
  ],
  'npc.ashfall_kiln_draught': [
    { text: 'Hot air roars up the kiln stack to a gully mouth. [[A thermal-riding kin]] could ride it.' },
  ],
  'npc.windward_ashfall_gap': [
    { text: 'A wind steady enough to lie a kite on. Only [[a thermal-riding kin]] could cross.' },
  ],
  'npc.galehigh_rockfall_blocked': [
    { text: 'The old cut to the Scarp is choked with rock. Two haulers\' picks lean on it.' },
  ],
  'npc.ashfall_camp_hauler': [
    { speaker: 'HAULER', text: 'Our Oda says somebody must be here when the kiln wakes. Kilns don\'t wake. She pours tea.' },
  ],
  'npc.ashfall_picker_after': [
    { speaker: 'SILE', text: 'A century of slag underfoot, and the grass grows through it anyway. Stubborn. I like it.' },
  ],
  'npc.ashfall_galewatch_after': [
    { speaker: 'PELL', text: 'Somebody\'s lit the Windward climbers\' shelter again. Somebody always does.' },
  ],
};
