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
  // ---- Cinderwind Scarp: the rockfall (the return compressor) -----------------------
  'script.scarp_rockfall_blocked': [
    { op: 'emote', actor: 'rockfall_hauler', emote: 'alert' },
    { op: 'face', actor: 'rockfall_hauler', facing: 'left' },
    { op: 'say', speaker: 'HAULER', text: 'Whoa there, love! Mind your feet. Half the ridge came down across the old cut in the last blow. You\'ll not get to Galehigh this way.' },
    { op: 'say', speaker: 'HAULER', text: 'Up and round by the Ashfall, love. The crest wood parts back west, by the kite-runner. Over the tips and you come out on Galehigh\'s top road.' },
    { op: 'say', speaker: 'HAULER', text: 'The Galehigh lot have the picks for a job like this. Tell them Cinderhead\'s waiting on its cut, would you?' },
    { op: 'move', actor: 'player', to: { tx: 19, ty: 4 } },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'face', actor: 'rockfall_hauler', facing: 'up' },
  ],
  'script.scarp_rockfall_hauler': [
    { op: 'say', speaker: 'HAULER', text: 'Thirty tons of ridge if it\'s a pebble. I\'ve been sat here working out which rock to start on, and it\'s the one at the bottom. It\'s always the one at the bottom.' },
    { op: 'say', speaker: 'HAULER', text: 'Up and round by the Ashfall, love. Back west to the gap in the crest wood, then over the tips to Galehigh.' },
  ],
  // Galehigh's upper west road, the first time you arrive by the Ashfall.
  'script.ashfall_rockfall_promise': [
    { op: 'narrate', text: 'Two Galehigh haulers are shouldering picks at the head of the old Scarp road. One of them looks you up and down, and at the ash on your boots.' },
    { op: 'say', speaker: 'GALEHIGH HAULER', text: 'Came round by the Ashfall, did you? Then you\'ve seen what the fall did to the Scarp cut. Cinderhead\'s been shouting up about it all week.' },
    { op: 'say', speaker: 'GALEHIGH HAULER', text: 'Leave it with us. By the time you\'re heading home it\'ll be clear, and the short way down to the mine is yours again.' },
    { op: 'narrate', text: 'They tramp off toward the old cut, arguing cheerfully about which rock to start on.' },
  ],

  // ---- The Ashfall Shelf -------------------------------------------------------------
  'script.ashfall_brazier_rest': [
    { op: 'say', speaker: 'HAULER', text: 'Sit in, sit in. Haulers\' rule: nobody passes a lit brazier on the Ashfall without warming their kin at it.', unless_flag: 'flag:ashfall_camp_rested' },
    { op: 'narrate', text: 'Up here the night is wide and grey. The brazier ticks, the ash-grass hisses in the wind, and somewhere below the mine is still breathing.', unless_flag: 'flag:ashfall_camp_rested' },
    { op: 'setFlag', flag: 'flag:ashfall_camp_rested' },
    { op: 'heal' },
    { op: 'narrate', text: 'Your kin wake warm, with coal-smoke in their fur and feathers. Galehigh is just over the tips.' },
  ],
  'script.ashfall_vista': [
    { op: 'narrate', text: 'From the wind cairn the shelf drops away east, and across the gulf the whole of Windward Stair climbs into the cold: cairn after cairn, prayer-flags snapping, a climbers\' shelter halfway up with its lamp lit.' },
    { op: 'narrate', text: 'Right at your feet the wind pours up the gap, hard and steady, the kind of draught a kite could lie on all the way across.' },
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
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'Mind the ash, dear, it gets in everything. Even the tea. Especially the tea.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'See that old stack on the lip? That was ours. The Kilnwrights drew the lamp-glass for half the valleys up there in the gully. Every pane in Galehigh came through my father\'s hands.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'Then the dark came, the lamp-oil stopped coming up the haulers\' road, and we let the fire go. Eleven winters cold. I keep the camp so somebody\'s still here when it matters.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'There\'s one pane left up there, on the drying rack. The last we ever drew. And the lamp by the kite-stall in Galehigh has stood blind since the storm cracked its glass.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'The stack still breathes, you know. Hot air pours up it day and night. Mira\'s kite-folk can ride a draught like that. If you ever learn the trick of it, would you fetch that pane down for me?' },
    { op: 'setFlag', flag: HOOK },
  ],
  'script.oda_remind': [
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'The last pane is still up in the gully, on the drying rack in the loft. Ride the stack\'s draught up, if you can. Then take it to the blind lamp by Galehigh\'s kite-stall.' },
  ],
  'script.oda_has_pane': [
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'Oh. Oh, look at it. Father always said the last one out of a kiln is the warmest.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'And the stack is smoking again. I saw it from here. You woke the old girl up, didn\'t you? Oh, she was only sleeping.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'Don\'t give it to me, dear. I\'d only keep it in a drawer. Take it to the kite-stall lamp in Galehigh and let it do its job.' },
  ],
  'script.oda_after': [
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'A kite-hand came down the tips yesterday just to tell me the kite-stall lamp is lit. Amber, she said. Like a sunset caught in a jar.' },
    { op: 'say', speaker: 'ODA KILNWRIGHT', text: 'I might go up and see it. Once the tea\'s brewed. Once the ash settles. Soon.' },
  ],
  'script.pickup_ashfall_nook': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Something glints under a crust of old ash. You dig it out with your fingers: a STARGLASS SHARD, still faintly warm. Found it!' },
    { op: 'setFlag', flag: 'flag:picked_ashfall_nook' },
  ],
  'script.pickup_ashfall_lunchtin': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'Wedged between the slag and the rocks: a hauler\'s lunch-tin, long forgotten. The bread is past saving, but packed in ash at the bottom, still faintly warm, is a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_ashfall_lunchtin' },
  ],
  'script.pickup_ashfall_tin': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A hauler\'s tin wedged under the cart, "FOR THE NEXT ONE UP" scratched on the lid. Packed in straw inside: a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_ashfall_tin' },
  ],
  'script.ashfall_picker': [
    { op: 'say', speaker: 'SILE', text: 'Up the slag cut on your own two feet? Good. The tips are for folk who can carry their weight. Let\'s see if yours can carry theirs.' },
    { op: 'battle', trainer: 'ashfall_picker' },
    { op: 'say', speaker: 'SILE', text: 'Heavy hitters. Fine. Galehigh\'s east over the tips: drop down past the gale-watch and follow the road.' },
    { op: 'setFlag', flag: 'flag:ashfall_picker_beaten' },
  ],
  'script.ashfall_galewatch': [
    { op: 'say', speaker: 'PELL', text: 'Gale-watch! Nobody goes down to the top road till I\'ve seen what the wind thinks of them. And the wind thinks you need a bout.' },
    { op: 'battle', trainer: 'ashfall_galewatch' },
    { op: 'say', speaker: 'PELL', text: 'The wind says go on, then. Galehigh\'s straight down and east. If you hear pipes, you\'re close.' },
    { op: 'setFlag', flag: 'flag:ashfall_galewatch_beaten' },
  ],

  // ---- Kiln Gully ----------------------------------------------------------------------
  'script.kiln_last_pane': [
    { op: 'narrate', text: 'On the loft\'s drying rack, wrapped in a cloth gone stiff with ash, one pane of amber lamp-glass still stands in its carrying frame. The dark has not dulled it at all.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'kiln_pane' },
    { op: 'narrate', text: 'You got THE LAST PANE!' },
    { op: 'setFlag', flag: PANE },
    // the "oh!" beat: lifting the last pane off the rack, the cold furnace wakes
    { op: 'shake', ms: 300, intensity: 0.004 },
    { op: 'cameraFocus', to: { tx: 10, ty: 3 }, ms: 700 },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'flashColor', color: '#ff8a3a', ms: 500 },
    { op: 'narrate', text: 'Behind you, eleven winters of banked coal catch. One by one the furnace\'s glory-holes open orange, and warm light runs across the hall.' },
    { op: 'narrate', text: 'It knew the last pane was going home.' },
    { op: 'cameraReset', ms: 600 },
    { op: 'narrate', text: 'Galehigh\'s kite-stall lamp stands blind for want of glass. This would fit it.', unless_flag: HOOK },
    { op: 'narrate', text: 'Oda said the blind lamp by Galehigh\'s kite-stall. It\'s a short glide away now.', if_flag: HOOK },
  ],
  'script.pickup_kiln_beacon': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'A lamp-wright\'s strongbox in the corner, its lock rusted through. Inside, packed in straw: a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_kiln_beacon' },
  ],
  'script.pickup_kiln_chart': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'chart_shardstorm', count: 1 },
    { op: 'say', text: 'Pinned behind the store\'s glass crates, where the blowers could see it while they worked: a STAR-CHART: SHARDSTORM!' },
    { op: 'setFlag', flag: 'flag:picked_kiln_chart' },
  ],
  'script.kiln_furnace_lore': [
    { op: 'narrate', text: 'The great furnace is cold to the touch, but deep in its glory-holes a few coals still blink, banked eleven winters ago and never quite gone out.' },
    { op: 'narrate', text: 'A brass plate on its iron door: "KILNWRIGHT & DAUGHTERS. GLASS FOR THE LAMPS OF EVERY VALLEY THAT WILL HAVE IT." Someone has polished the plate since the fire went out.' },
  ],
  'script.galehigh_pane_lamp': [
    { op: 'run', ref: 'script.galehigh_pane_lamp_lit', if_flag: DONE },
    { op: 'run', ref: 'script.galehigh_pane_set', if_flag: PANE, unless_flag: DONE },
    { op: 'run', ref: 'script.galehigh_pane_blind', unless_flag: PANE },
  ],
  'script.galehigh_pane_blind': [
    { op: 'narrate', text: 'The lamp beside the kite-stall stands blind: its pane cracked right across, the flame inside guttering in the draught.' },
    { op: 'say', speaker: 'KITE-MAKER', text: 'Storm took the glass last spring. Nobody draws lamp-glass any more, not since the Kilnwrights let their fire go. So it gutters.', unless_flag: HOOK },
    { op: 'narrate', text: 'Oda Kilnwright\'s last pane would fit it exactly.', if_flag: HOOK },
  ],
  'script.galehigh_pane_set': [
    { op: 'say', speaker: 'KITE-MAKER', text: 'Is that... kiln glass? Kilnwright glass? I haven\'t seen a new pane since I was apprenticed. Hold the lamp steady. No, steadier. There!' },
    { op: 'takeItem', item: 'kiln_pane' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'setFlag', flag: DONE },
    { op: 'flashColor', color: '#ffb347', ms: 400 },
    { op: 'narrate', text: 'The flame steadies behind the new glass, and the whole kite-stall turns amber, like a sunset caught in a jar.' },
    { op: 'say', speaker: 'KITE-MAKER', text: 'Tell Oda it\'s lit. No, I\'ll tell her myself, I\'ll send a kite-hand down. And take this. The festival committee keeps a purse for exactly this sort of thing.' },
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: 1200 },
    { op: 'narrate', text: 'You received 1,200 wicks!' },
  ],
  'script.galehigh_pane_lamp_lit': [
    { op: 'narrate', text: 'The kite-stall lamp burns amber behind the Kilnwrights\' last pane. Even the kites hung beside it look warmer.' },
  ],
};

export const ASHFALL_DIALOGUE: DialogueRegistry = {
  'sign.cinderwind_ashfall': [
    { text: 'THE ASHFALL SHELF\nSOUTH: Cinderwind Scarp and the mine. EAST, over the tips: Galehigh\'s top road.' },
    { text: 'Burnt into the board underneath: "A hundred years of slag went over this edge. Mind where you dig. Mind more what you find."' },
  ],
  'sign.ashfall_century': [
    { text: 'A tipping-stone at the end of the old ore track, notched in hundreds of rows of five. A notch for every cart of slag that went over the edge.' },
    { text: 'The last row stops halfway. Under it, scratched deeper: "LAMPS OUT. CARTS STOPPED. THE GRASS CAN HAVE IT NOW."' },
  ],
  'sign.ashfall_gate': [
    { text: 'GALEHIGH TERRACES, EAST.\nThe kite-wrights ask that you leave the ash on THIS side of the gate.' },
  ],
  'sign.kiln_tally': [
    { text: 'A tally-board by the gully mouth, the last column half-finished: "PANES DRAWN, WINTER OF THE LONG DUSK: 1."' },
  ],
  'npc.kiln_rack_lore': [
    { text: 'Rows of half-made lamp-globes still hang on the rack, dusty with ash, waiting to be finished. Each one is scratched with the name of the valley it was for.' },
  ],
  'npc.ashfall_windgap': [
    { text: 'The wind pours up through the gap, hard and steady, and across the gulf Windward Stair climbs away. Only a kin that rides the thermals could cross from here.' },
  ],
  'npc.ashfall_kiln_draught': [
    { text: 'Hot air rolls out of the old kiln stack and roars straight up the cliff. Up there in the rock, a gully mouth is just visible. A kin that rides the thermals could ride this.' },
  ],
  'npc.windward_ashfall_gap': [
    { text: 'Below the west face, a grey shelf of old slag tips. The wind pours up between, steady enough to lie a kite on. Only a kin that rides the thermals could cross.' },
  ],
  'npc.galehigh_rockfall_blocked': [
    { text: 'The old cut down to Cinderwind Scarp is choked with fallen rock. Two haulers\' picks lean against it, waiting.' },
  ],
  'npc.ashfall_camp_hauler': [
    { speaker: 'HAULER', text: 'Our Oda won\'t leave the shelf. Says somebody has to be here when the kiln wakes up. Kilns don\'t wake up, I tell her. She just pours me more tea.' },
  ],
  'npc.ashfall_picker_after': [
    { speaker: 'SILE', text: 'A century of slag under your feet, and the grass grows up through it anyway. Grey, mind. Stubborn stuff. I like it.' },
  ],
  'npc.ashfall_galewatch_after': [
    { speaker: 'PELL', text: 'On a clear night you can see the Windward cairns from the lookout. Somebody\'s lit the climbers\' shelter again. Somebody always does.' },
  ],
};
