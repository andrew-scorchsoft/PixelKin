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
 *   flag:picked_mournfields_shelf / _plot   the shrine shelf's cache, the west plot's
 *   flag:mournfields_shrine_read       first read of the field shrine (longer narration)
 *   flag:mournfields_tender_met        the field-tender's first meeting (longer lines)
 * Reads flag:dawn (the post-dawn branches: the sleepers wake, the lanterns unhood).
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

const DAWN = 'flag:dawn';

export const MOURNFIELDS_SCRIPTS: ScriptRegistry = {
  // ---- the field shrine (seen from below, reached from the upper terrace) ----------
  'script.mournfields_shrine': [
    { op: 'narrate', text: 'A wayside shrine, the kind every farm in the valleys keeps at the top field. Five candles stand on a brass board, each one put out and its wick trimmed.', unless_flag: 'flag:mournfields_shrine_read' },
    { op: 'narrate', text: 'Under each candle, a name is scratched into the board. Not people. Fields. NETHERLEA. LONG ACRE. THE BROOK PIECE. MILLER\'S. THE TOP FIELD.', unless_flag: 'flag:mournfields_shrine_read' },
    { op: 'narrate', text: 'Someone has written underneath, very neatly: "We put them to sleep one at a time, so nobody would wake to find the rest gone."', unless_flag: 'flag:mournfields_shrine_read' },
    { op: 'setFlag', flag: 'flag:mournfields_shrine_read' },
    { op: 'narrate', text: 'Five trimmed candles. Folded blankets left at the step, ready for whoever is cold.', unless_flag: DAWN },
    { op: 'narrate', text: 'One of the five candles is burning again: THE TOP FIELD. Nobody has written anything new on the board. Nobody needed to.', if_flag: DAWN },
  ],
  'script.pickup_mournfields_shelf': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 2 },
    { op: 'say', text: 'Tucked behind the shrine, out of the wind: a lamp-tender\'s tin, never opened. Inside, packed in wool, 2 BEACON CHARGES!' },
    { op: 'setFlag', flag: 'flag:picked_mournfields_shelf' },
  ],

  'script.pickup_mournfields_plot': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'In the corner of the west plot, under a fold of old sacking: a farmer\'s ember-pot, still faintly warm. Found a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_mournfields_plot' },
  ],

  // ---- the field-tender (the sleepers' field) -----------------------------------------
  'script.mournfields_tender': [
    { op: 'run', ref: 'script.mournfields_tender_dawn', if_flag: DAWN },
    { op: 'run', ref: 'script.mournfields_tender_dusk', unless_flag: DAWN },
  ],
  'script.mournfields_tender_dusk': [
    { op: 'face', actor: 'field_tender', facing: 'up' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Shh. Mind your step, dear. They\'ve only just gone off.', unless_flag: 'flag:mournfields_tender_met' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'I tuck them in every evening. Nobody makes me. It\'s just that they always kick the blankets off on the cold side, and I can\'t bear to see it.', unless_flag: 'flag:mournfields_tender_met' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'This was my field. The light went out of the sky and the barley wouldn\'t ripen, and the kin kept waking up hungry in the dark. Every night, hungry and frightened.', unless_flag: 'flag:mournfields_tender_met' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'So when the Wardens said they could let them sleep, I said yes. I\'d say yes again. You\'d say yes too, if you\'d heard them.', unless_flag: 'flag:mournfields_tender_met' },
    { op: 'setFlag', flag: 'flag:mournfields_tender_met' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'You\'re the one lighting the sky back up, aren\'t you. I can see it on you. Well. Go gently past my sleepers, that\'s all I ask.' },
  ],
  'script.mournfields_tender_dawn': [
    { op: 'emote', actor: 'field_tender', emote: 'music' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Look at them. Up before me, the lazy things. They\'ve been at the stooks all morning.' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'I kept the blankets. I fold them every evening anyway. Habit. Or maybe in case.' },
    { op: 'say', speaker: 'FIELD-TENDER', text: 'Thank you. I don\'t know how else to say it, so I\'ll just say it the once and then go back to work.' },
  ],

  // ---- the walker at the Coldfog gate (the wayfinding voice) -----------------------
  'script.mournfields_walker': [
    { op: 'say', speaker: 'STILLWATER TRADER', text: 'West, that gap? Coldfog Marches. North, up the bank, Stillwater. South, down the col, the Rimeway.' },
    { op: 'say', speaker: 'STILLWATER TRADER', text: 'The bank\'s the thing. You can hop down off it anywhere, but you can\'t climb it. To go up to Stillwater you walk east to the one stair by the shrine, then back along the top.' },
    { op: 'say', speaker: 'STILLWATER TRADER', text: 'It\'s not a wrong turn, love. It\'s just the long way round, and the long way round is how fields are.', unless_flag: DAWN },
    { op: 'say', speaker: 'STILLWATER TRADER', text: 'I\'m carrying candles down to Coldfog now. Can you believe it? Candles. Somebody ordered a hundred.', if_flag: DAWN },
  ],

  // ---- the two acolytes ------------------------------------------------------------
  'script.mournfields_ines': [
    { op: 'say', speaker: 'INES', text: 'Up the stair from the sleepers\' field? Quietly, then. We\'ve only just got the little ones off.' },
    { op: 'say', speaker: 'INES', text: 'I\'ll not stop you. But I\'ll see what kind of kin walks with the one who\'s waking the sky. Softly, mind.' },
    { op: 'battle', trainer: 'mournfields_ines' },
    { op: 'say', speaker: 'INES', text: 'They\'re gentle with you. Yours, I mean. That\'s good. I was worried they wouldn\'t be.' },
    { op: 'setFlag', flag: 'flag:mournfields_ines_beaten' },
  ],
  'script.mournfields_corran': [
    { op: 'say', speaker: 'CORRAN', text: 'The Rimeway road. Nobody comes up it but us, carrying blankets. You\'re not carrying blankets.' },
    { op: 'say', speaker: 'CORRAN', text: 'I\'m meant to ask travellers to turn their lamps down through the fields. I\'m going to ask you, and you\'re going to say no. So let\'s have it out.' },
    { op: 'battle', trainer: 'mournfields_corran' },
    { op: 'say', speaker: 'CORRAN', text: 'Keep it lit, then. I won\'t pretend I didn\'t look at it. Go on, the col\'s yours.' },
    { op: 'setFlag', flag: 'flag:mournfields_corran_beaten' },
  ],
};

export const MOURNFIELDS_DIALOGUE: DialogueRegistry = {
  'sign.mourning_fields': [
    { text: 'THE MOURNING FIELDS\nWEST: Coldfog Marches. NORTH, up the bank: Stillwater. SOUTH: the Rimeway col.' },
    { text: 'The old name, MOORLEA FIELDS, has been painted over in grey. Neatly.' },
  ],
  'sign.mournfields_col': [
    { text: 'THE COL ROAD\nDown to the Rimeway and the high road home. The Rime Gate is lifted from the marsh side.' },
  ],
  'sign.mournfields_notice': [
    { text: 'A notice in the Hollowing\'s careful hand:\n"THESE KIN ARE SLEEPING. Please do not wake them. Please do not lift the blankets."' },
    { text: 'Underneath, in a child\'s writing: "the grey one with ears likes his ears scratched but he is asleep now"' },
  ],
  'npc.mournfields_ines_after': [
    { speaker: 'INES', text: 'When it\'s all done, whichever way it goes, someone will still have to tuck them in. I\'ll do it. I\'d like to.' },
  ],
  'npc.mournfields_corran_after': [
    { speaker: 'CORRAN', text: 'I carry the blankets up from the col every week. Coldfog makes the warmest wool there is. Isn\'t that a strange thing.' },
  ],
};
