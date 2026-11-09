/**
 * Lane N3 (2026-10, docs/world/walkthrough/11-the-hollowing-country.md Part C) —
 * THE MOURNING FIELDS: Stillwater's fallow farmland, quieted by the Hollowing. The
 * field-kin sleep where they lay, tucked under grey coldfog blankets; the scarecrows are
 * lamp-posts with their lanterns hooded. The dread register of the Marches, but tender:
 * grief dressed as mercy, never menace. Builder: tools/maps/build_mourning_fields.py.
 *
 * This lane OWNS this file: new scripts + dialogue only (spread via regions/index.ts).
 *
 * Flags this file owns:
 *   flag:mournfields_ines_beaten / flag:mournfields_corran_beaten  the two acolytes
 *   flag:picked_mournfields_shelf / _plot / _terrace / _brook   the shrine shelf's cache (a
 *                                      Lumen Drop), the west plot's (Lullwool Charms), the east
 *                                      terrace's (the Harvest Knot, a toggle key item that hushes
 *                                      wild kin ×0.25), the Brook Piece's (a Hearth Coal) — never sold
 *   flag:harvest_knot_hung             the Harvest Knot's toggle (ITEMS → use; items.ts)
 *   flag:mournfields_knot_noted        the field-tender has seen the knot on your lamp (once)
 *   flag:mournfields_brook_met         first look at the Brook Piece's sleeper (longer lines)
 *   flag:mournfields_tender_gift       the field-tender's dawn gift (Lullwool Charms), once
 *   flag:mournfields_shrine_read       first read of the field shrine (longer narration)
 *   flag:mournfields_tender_met        the field-tender's first meeting (longer lines)
 * Reads flag:dawn (the post-dawn branches: the sleepers wake, the lanterns unhood).
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

const DAWN = 'flag:dawn';

export const MOURNFIELDS_SCRIPTS: ScriptRegistry = {
  // ---- the field shrine (seen from below, reached from the upper terrace) ----------
  'script.mournfields_shrine': [
    { op: 'narrate', text: 'A wayside shrine, the kind every valley farm keeps at the top field. Five candles on a brass board, each put out, its wick trimmed.', unless_flag: 'flag:mournfields_shrine_read' },
    { op: 'narrate', text: 'Under each candle, a name. Not people. Fields. NETHERLEA. LONG ACRE. THE BROOK PIECE. MILLER\'S. THE TOP FIELD.', unless_flag: 'flag:mournfields_shrine_read' },
    { op: 'narrate', text: 'Underneath, very neatly: "We put them to sleep one at a time, so nobody would wake to find the rest gone."', unless_flag: 'flag:mournfields_shrine_read' },
    { op: 'setFlag', flag: 'flag:mournfields_shrine_read' },
    { op: 'narrate', text: 'Five trimmed candles. Folded blankets at the step, for whoever is cold.', unless_flag: DAWN },
    // the second dawn change (2026-10-14 second pass): all five burn, the names read out
    { op: 'sfx', key: 'world-heal', if_flag: DAWN },
    { op: 'narrate', text: 'All five candles burn again. NETHERLEA. LONG ACRE. THE BROOK PIECE. MILLER\'S. THE TOP FIELD. Warm wax runs over the names.', if_flag: DAWN },
    { op: 'narrate', text: 'Under the neat line, in a rounder hand, one word: "Morning."', if_flag: DAWN },
  ],
  // The Fields' finds are the Fields' own (2026-10-14 review: no shop-stock here).
  'script.pickup_mournfields_shelf': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'Behind the shrine, on the harvest-sweets shelf: a honey-bead in a twist of straw. Found a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:picked_mournfields_shelf' },
  ],

  'script.pickup_mournfields_plot': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lullwool_charm', count: 2 },
    { op: 'say', text: 'Under sacking in the west plot: two charge cells wound in grey wool, the way you\'d wrap something you didn\'t want to wake. Found 2 LULLWOOL CHARMS!' },
    { op: 'say', text: 'They burn [[threefold at a dozing kin]], plain at a waking one.' },
    { op: 'setFlag', flag: 'flag:picked_mournfields_plot' },
  ],

  'script.pickup_mournfields_terrace': [
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'harvest_knot', count: 1 },
    { op: 'say', text: 'On the top field\'s last post: the year\'s last sheaf, plaited into a knot with ribbon. Found the HARVEST KNOT!' },
    { op: 'say', text: '[[Tie it to your lamp from ITEMS]] and wild kin take you for the harvest coming home, and let you by.' },
    { op: 'setFlag', flag: 'flag:picked_mournfields_terrace' },
  ],

  // ---- THE BROOK PIECE (the fifth field: the bramble nook under the col pine) -------
  'script.pickup_mournfields_brook': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'In a tin under the hedge, packed in ash: a live coal, "for if he wakes cold". Found a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_mournfields_brook' },
  ],
  'script.mournfields_brook_sleeper': [
    { op: 'run', ref: 'script.mournfields_brook_sleeper_dawn', if_flag: DAWN },
    { op: 'run', ref: 'script.mournfields_brook_sleeper_dusk', unless_flag: DAWN },
  ],
  'script.mournfields_brook_sleeper_dusk': [
    { op: 'narrate', text: 'An old grey Hushvole, asleep alone in the smallest field under the best blanket. The hem is stitched: TUSSOCK.', unless_flag: 'flag:mournfields_brook_met' },
    { op: 'narrate', text: 'The others are tucked in where the road can see them. This one, where nobody would ever step on him.', unless_flag: 'flag:mournfields_brook_met' },
    { op: 'setFlag', flag: 'flag:mournfields_brook_met' },
    { op: 'narrate', text: 'He breathes slow. One ear twitches at your lamp, then settles.' },
  ],
  'script.mournfields_brook_sleeper_dawn': [
    { op: 'sfx', key: 'world-heal' },
    { op: 'narrate', text: 'TUSSOCK is up, nose deep in the stubble. His blanket is folded beside him, very badly, as only a Hushvole would.' },
    { op: 'narrate', text: 'He looks at you, then at the gap under the pine: does she know he\'s awake?' },
  ],

  // ---- the field-tender (the sleepers' field) -----------------------------------------
  'script.mournfields_tender': [
    { op: 'run', ref: 'script.mournfields_tender_dawn', if_flag: DAWN },
    { op: 'run', ref: 'script.mournfields_tender_dusk', unless_flag: DAWN },
  ],
  'script.mournfields_tender_dusk': [
    { op: 'face', actor: 'field_tender', facing: 'up' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Shh. Mind your step, dear. They\'ve only just gone off.', unless_flag: 'flag:mournfields_tender_met' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'I tuck them in every evening. Nobody makes me. They kick the blankets off on the cold side, and I can\'t bear it.', unless_flag: 'flag:mournfields_tender_met' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'This was my field. The light went and the barley wouldn\'t ripen, and the kin kept waking hungry in the dark. Every night, hungry and frightened.', unless_flag: 'flag:mournfields_tender_met' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'When the Wardens said they could let them sleep, I said yes. I\'d say it again. So would you, if you\'d heard them.', unless_flag: 'flag:mournfields_tender_met' },
    { op: 'setFlag', flag: 'flag:mournfields_tender_met' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'You\'re the one lighting the sky back up. I can see it on you. Go gently past my sleepers, that\'s all I ask.' },
    { op: 'run', ref: 'script.mournfields_tender_knot', if_flag: 'flag:picked_mournfields_terrace', unless_flag: 'flag:mournfields_knot_noted' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Don\'t wake my Tussock in the Brook Piece. He was the first I tucked in, and the hardest.', if_flag: 'flag:mournfields_brook_met' },
  ],
  // once: she sees the top field's knot on your lamp, and says keep it
  'script.mournfields_tender_knot': [
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Is that the top field\'s knot? Well. Somebody ought to have it.' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Keep it on your lamp. The wild ones will think you\'re the harvest coming home. They always let us by.' },
    { op: 'setFlag', flag: 'flag:mournfields_knot_noted' },
  ],
  'script.mournfields_tender_dawn': [
    { op: 'emote', actor: 'field_tender', emote: 'music' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Look at them, up before me! At the stooks all morning.' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'I still fold the blankets every evening. Habit. Or in case.' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Somebody\'s lit all five candles at the shrine. I read the names out at first light, like the old harvest-home. Silly. I cried at the Brook Piece.' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'The green moth\'s still in the Brook Piece\'s long grass. Leaf wings, glows like a lamp through a hedge. It sat up with my Tussock every night he slept, and never went to any other field.', if_flag: 'flag:mournfields_brook_met' },
    { op: 'run', ref: 'script.mournfields_tender_knot', if_flag: 'flag:picked_mournfields_terrace', unless_flag: 'flag:mournfields_knot_noted' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Thank you. I\'ll say it the once and then go back to work.', unless_flag: 'flag:mournfields_tender_gift' },
    { op: 'run', ref: 'script.mournfields_tender_gift', unless_flag: 'flag:mournfields_tender_gift' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Go on. They\'ve a whole day to make up for, and so have you.' },
  ],
  // the dawn gift, once: the wool charms she wound for the sleepers' lamps
  'script.mournfields_tender_gift': [
    { op: 'say', speaker: 'FIELD-TENDER', text: 'I wound these for the sleepers\' lamps, the nights they wouldn\'t settle. I won\'t need them now.' },
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lullwool_charm', count: 3 },
    { op: 'say', text: 'Got 3 LULLWOOL CHARMS! They burn [[threefold at a dozing kin]].' },
    { op: 'setFlag', flag: 'flag:mournfields_tender_gift' },
  ],

  // ---- the wool-gatherer at the Coldfog gate (the wayfinding voice) ----------------
  // (was "Stillwater trader" — a trader with nothing to sell; the 2026-10-14 review)
  'script.mournfields_walker': [
    { op: 'say', speaker: 'WOOL-GATHERER', text: 'Mind the fences, love. The fog leaves its wool on the wire overnight, and somebody has to pick it off. That\'s me.', unless_flag: DAWN },
    { op: 'say', speaker: 'WOOL-GATHERER', text: '[[West]]: Coldfog Marches. [[North, up the bank]]: Stillwater. South, down the col: the Rimeway.' },
    { op: 'say', speaker: 'WOOL-GATHERER', text: 'You can hop down the bank anywhere, but not climb it. For Stillwater, take [[the one stair by the shrine]], east, where a lamp\'s left a slit open. Then back along the top.' },
    { op: 'say', speaker: 'WOOL-GATHERER', text: 'Not a wrong turn. Just the long way round, which is how fields are.', unless_flag: DAWN },
    { op: 'say', speaker: 'WOOL-GATHERER', text: 'Every blanket here came off these fences, a skein a night. I don\'t know what it\'s for any more. I just know how to do it.', unless_flag: DAWN },
    { op: 'say', speaker: 'WOOL-GATHERER', text: 'No fog on the wire this morning, first time in eleven winters. I came out with my basket anyway and stood here laughing.', if_flag: DAWN },
    { op: 'say', speaker: 'WOOL-GATHERER', text: 'I\'m carrying candles down to Coldfog now. Somebody ordered a hundred!', if_flag: DAWN },
  ],

  // ---- the two acolytes ------------------------------------------------------------
  'script.mournfields_ines': [
    { op: 'say', speaker: 'INES', text: 'Quietly, now. We\'ve only just got the little ones off.' },
    { op: 'say', speaker: 'INES', text: 'I\'ll not stop you. But I\'ll see what kin walk with the one waking the sky. Softly, mind.' },
    { op: 'battle', trainer: 'mournfields_ines' },
    { op: 'say', speaker: 'INES', text: 'Yours are gentle with you. Good. I worried they wouldn\'t be.' },
    { op: 'setFlag', flag: 'flag:mournfields_ines_beaten' },
  ],
  'script.mournfields_corran': [
    { op: 'say', speaker: 'CORRAN', text: 'Nobody comes up the Rimeway road but us, carrying blankets. You\'re not carrying blankets.' },
    { op: 'say', speaker: 'CORRAN', text: 'I\'m to ask you to turn your lamp down through the fields. You\'ll say no. So let\'s have it out.' },
    { op: 'battle', trainer: 'mournfields_corran' },
    { op: 'say', speaker: 'CORRAN', text: 'Keep it lit, then. I won\'t pretend I didn\'t look. Go on, the col\'s yours.' },
    { op: 'setFlag', flag: 'flag:mournfields_corran_beaten' },
  ],
};

export const MOURNFIELDS_DIALOGUE: DialogueRegistry = {
  'sign.mourning_fields': [
    { text: 'THE MOURNING FIELDS\nWEST: Coldfog Marches. NORTH, up the bank: Stillwater. SOUTH: the Rimeway col.' },
    { text: 'The old name, MOORLEA FIELDS, has been painted over in grey. Neatly.' },
  ],
  'sign.mournfields_col': [
    { text: 'THE COL ROAD\nDown to [[the Rimeway]] and the high road home. The Rime Gate lifts from the marsh side.' },
  ],
  'sign.mournfields_brook': [
    { text: 'A scrubbed marker stone:\nTHE BROOK PIECE.\nThe brook went under in the second winter.' },
    { text: 'Scratched below, small: "T. sleeps here. Mind the hedge, it\'s for the wind, not for you."' },
    { text: 'Under that, older: "Let the long grass be. The big green moth with leaf wings sits up with him some nights. It never goes to any other field. Let it."' },
  ],
  'sign.mournfields_notice': [
    { text: 'In the Hollowing\'s careful hand:\n"THESE KIN ARE SLEEPING. Please do not wake them or lift the blankets."' },
    { text: 'Underneath, in a child\'s writing: "the grey one with ears likes his ears scratched but he is asleep now"' },
  ],
  'npc.mournfields_ines_after': [
    { speaker: 'INES', text: 'Whichever way it goes, someone will still have to tuck them in. I\'d like it to be me.' },
  ],
  'npc.mournfields_corran_after': [
    { speaker: 'CORRAN', text: 'I carry blankets up from the col every week. Coldfog makes the warmest wool there is. Strange, isn\'t it.' },
  ],
};
