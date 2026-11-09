/**
 * Lane N3 (2026-10, docs/world/walkthrough/11-the-hollowing-country.md Part D) —
 * THE PENUMBRA UNDERWAYS: two portal floors under the Penumbra Ring, the genre's last
 * road. The Hollowing's LAST WATCH keeps its fire down here under the Spire's roots:
 * not to stop you, but to be there when it ends, whichever way it ends. Optional;
 * never connected to the Spire. Builder: tools/maps/build_penumbra_underways.py
 * (+ the two mouths and the light-well in build_penumbra_ring.py).
 *
 * This lane OWNS this file: new scripts + dialogue only (spread via regions/index.ts).
 * Senna is never named here; Còr's past stays dosed (story-bible §11-§12).
 *
 * The watch-fire's keeper is OLD CLEMENCY (renamed from "Old Maudry" in review fix FD,
 * 2026-10-14: the Drownlight's Shutterkeeper is Maudry Kell, who met Còr as a stranger;
 * Clemency is the one who taught him his letters).
 *
 * Flags this file owns:
 *   flag:underways_watch_a_beaten / _b_beaten / _c_beaten   the last watch's three watchers
 *   flag:picked_underways_starglass / flag:picked_underways_lumen
 *   flag:underways_watchfire_rested   the first night at the watch-fire (longer narration)
 *   flag:underways_shaft_seen         the first look up the Spire's shaft
 *   flag:underways_clemency_met       Old Clemency's first meeting
 *   flag:q_underways                  "The Last Watch" opens (journal): heard of / seen
 *   flag:underways_lightwell_seen     the first look down the Ring's light-well
 *   flag:underways_watch_kept         the whole watch met (all three tried, Clemency told).
 *                                     FD2: it CHANGES THE WORLD — Odalie, Bran and Hesk leave
 *                                     their posts (the `_after` NPCs hide) and gather at
 *                                     Clemency's fire (`<tid>_fire` twins, script.*_fire)
 * Reads flag:dawn (the post-dawn branches).
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

const DAWN = 'flag:dawn';
const OPEN = 'flag:q_underways';

export const UNDERWAYS_SCRIPTS: ScriptRegistry = {
  // ---- signposting: the way down, heard of before it's walked -------------------------
  // Andrew's P.S. (run from script.andrew_hint once the hub is open, before the Keystar).
  'script.underways_hint': [
    { op: 'say', speaker: 'ANDREW', text: 'Fancy a fire before the climb? The Hollowing keep a last watch [[under the Penumbra Ring]]: down [[the old stair, south-west corner]]. Nobody\'s turned away.', unless_flag: 'flag:underways_watchfire_rested' },
    { op: 'setFlag', flag: OPEN },
  ],
  // The Ring's light-well (seen before reached): a grate in the south strip's floor.
  'script.underways_lightwell': [
    { op: 'narrate', text: 'An iron grate, set flush in the stone. You kneel and look down it.', unless_flag: 'flag:underways_lightwell_seen' },
    { op: 'narrate', text: 'Far down: a pale column of light in the dark, and beside it, small and orange, a fire someone is keeping. A laugh comes up the shaft. Then a kettle.', unless_flag: DAWN },
    { op: 'narrate', text: 'Far down, the shaft is full of morning. Someone is still keeping a fire, out of habit.', if_flag: DAWN },
    { op: 'setFlag', flag: 'flag:underways_lightwell_seen' },
    { op: 'setFlag', flag: OPEN },
  ],
  // The mouths' "not yet" (a gated warp's blocked_ref): it opens the journal entry.
  'script.underways_mouth_shut': [
    { op: 'narrate', text: 'Old steps go down under the Ring, a hooded lamp turned low at the top. Not yet: the watch keeps its stair for whoever has [[lit all eight]].' },
    { op: 'setFlag', flag: OPEN },
  ],

  // ---- the Last Watch's fire (the REST POINT) -----------------------------------------
  'script.underways_watchfire_rest': [
    { op: 'say', speaker: 'CLEMENCY', text: 'Sit, sit. Nobody comes down this far without needing the fire, and nobody\'s turned away. That was always the rule.', unless_flag: 'flag:underways_watchfire_rested' },
    { op: 'narrate', text: 'The watch-fire burns low under an iron hood, enough to see a face by. Above, the whole weight of the Ring. Above that, the Spire.', unless_flag: 'flag:underways_watchfire_rested' },
    { op: 'setFlag', flag: 'flag:underways_watchfire_rested' },
    { op: 'setFlag', flag: OPEN },
    { op: 'heal' },
    { op: 'narrate', text: 'Your kin wake warm. Clemency put a blanket over them in the night, and folded it before they stirred.' },
  ],

  // ---- the view up the Spire's shaft (seen, never climbed) ---------------------------
  'script.underways_shaft_view': [
    { op: 'narrate', text: 'The mountain\'s roots open on a round pit, worked smooth. You look up.', unless_flag: 'flag:underways_shaft_seen' },
    { op: 'narrate', text: 'Straight up, through the Ring\'s stone and the dark heart of the Spire, a shaft so tall its top is one pale point. The Crown\'s light, arriving here as a whisper.', unless_flag: 'flag:underways_shaft_seen' },
    { op: 'narrate', text: 'There is no way up it. It was dug so somebody could stand at the bottom and look.', unless_flag: 'flag:underways_shaft_seen' },
    { op: 'narrate', text: 'High in the rock, a little square of starlight: the grate in the Ring\'s floor, where you knelt and looked down.', if_flag: 'flag:underways_lightwell_seen', unless_flag: 'flag:underways_shaft_seen' },
    { op: 'setFlag', flag: 'flag:underways_shaft_seen' },
    { op: 'narrate', text: 'The pale point at the top. [[The way up is through the Spire\'s door]], out in the Ring.', unless_flag: DAWN },
    { op: 'narrate', text: 'The shaft is full of morning now. Someone has set a cushion at the bottom.', if_flag: DAWN },
  ],

  // ---- Old Clemency, who keeps the watch-fire -----------------------------------------
  'script.underways_clemency': [
    { op: 'run', ref: 'script.underways_clemency_dawn', if_flag: DAWN },
    { op: 'run', ref: 'script.underways_clemency_dusk', unless_flag: DAWN },
    // the whole watch met: Odalie, Bran and Hesk have each tried you (a nested chain,
    // one flag per guard) — the journal's "The Last Watch" is kept
    { op: 'run', ref: 'script.underways_clemency_kept_a', if_flag: 'flag:underways_watch_a_beaten', unless_flag: 'flag:underways_watch_kept' },
  ],
  'script.underways_clemency_kept_a': [
    { op: 'run', ref: 'script.underways_clemency_kept_b', if_flag: 'flag:underways_watch_b_beaten' },
  ],
  'script.underways_clemency_kept_b': [
    { op: 'run', ref: 'script.underways_clemency_kept', if_flag: 'flag:underways_watch_c_beaten' },
  ],
  'script.underways_clemency_kept': [
    { op: 'emote', actor: 'clemency', emote: 'heart' },
    { op: 'say', speaker: 'CLEMENCY', text: 'Odalie, Bran and Hesk, all three. That\'s the whole last watch, dear. There never were very many of us.' },
    { op: 'say', speaker: 'CLEMENCY', text: 'Take this. The watch drew it the first winter: the dark as we meant it, not a void but a held breath. Nobody here has the heart to use it now.' },
    { op: 'giveItem', item: 'chart_voidburst', count: 1 },
    { op: 'say', speaker: 'CLEMENCY', text: 'And no sense the three of them standing in the cold for nobody. I\'ll call them in.' },
    { op: 'sfx', key: 'world-moorbell-a' },
    { op: 'narrate', text: 'She rings the little watch-bell, twice, soft. Up the galleries, someone laughs. Then footsteps, coming in.' },
    { op: 'setFlag', flag: 'flag:underways_watch_kept' },
  ],
  // ---- FD2: the watch, kept — the three watchers at Clemency's fire ---------------------
  'script.underways_watch_a_fire': [
    { op: 'say', speaker: 'ODALIE', text: 'Two rings. Eleven winters it meant "keep watch". Tonight it meant "come in". I didn\'t know what to do with my hands.', unless_flag: DAWN },
    { op: 'say', speaker: 'ODALIE', text: 'I took my scissors up the Coldfog road this morning. Not to trim anything. Just to stand under the lamps while they burned.', if_flag: DAWN },
  ],
  'script.underways_watch_b_fire': [
    { op: 'say', speaker: 'BRAN', text: 'No gap to hold now. I sat in that choke so long it\'s worn to my shape. Empty now. Strange thing to be proud of.', unless_flag: DAWN },
    { op: 'say', speaker: 'BRAN', text: 'Eleven winters of cards with one eye on the dark. This morning I dealt to the Warden himself. He still can\'t bluff. Pull up a stone.', if_flag: DAWN },
  ],
  'script.underways_watch_c_fire': [
    { op: 'say', speaker: 'HESK', text: 'I walked off the last post of the last watch. Felt like stepping off a cliff. Turns out it\'s just floor, and a fire at the end.', unless_flag: DAWN },
    { op: 'say', speaker: 'HESK', text: 'I swept the east stair once more, for habit, then stood up top in the morning till my eyes ran. Don\'t tell Clemency. She\'ll say she knew.', if_flag: DAWN },
  ],
  'script.underways_clemency_dusk': [
    { op: 'face', actor: 'clemency', facing: 'down' },
    { op: 'say', speaker: 'CLEMENCY', text: 'So you\'re the one. People always want to see the bottom of things before the top.', unless_flag: 'flag:underways_clemency_met' },
    { op: 'say', speaker: 'CLEMENCY', text: 'This is the last watch. Not a guard; we stop nobody. We\'re here so that when it\'s over, up there, somebody who loves him is close by.', unless_flag: 'flag:underways_clemency_met' },
    { op: 'say', speaker: 'CLEMENCY', text: 'I taught the Warden his letters, long before he was anybody\'s Warden. A careful boy. Too careful with his sorrows. He kept every one.', unless_flag: 'flag:underways_clemency_met' },
    { op: 'say', speaker: 'CLEMENCY', text: 'Warm stones lie [[by the east cut, down the slump]]. A light-kin comes to them, ember and light both. Now and then a jester-kin, bright one side, dark the other, comes to do its turn and bow.', unless_flag: 'flag:underways_clemency_met' },
    { op: 'setFlag', flag: 'flag:underways_clemency_met' },
    { op: 'setFlag', flag: OPEN },
    { op: 'say', speaker: 'CLEMENCY', text: 'The fire\'s yours whenever you want it. Rest, then go up and do what you must. Be kind to him, if you can.' },
  ],
  'script.underways_clemency_dawn': [
    { op: 'emote', actor: 'clemency', emote: 'heart' },
    { op: 'say', speaker: 'CLEMENCY', text: 'He came down, after. Sat by the fire an hour without a word. Then he asked if I still had the kettle.' },
    { op: 'say', speaker: 'CLEMENCY', text: 'I did. I always did. Sit down, dear. You\'ve earned a cup.' },
  ],

  // ---- the three watchers (the Hollowing's last watch) ---------------------------------
  'script.underways_watch_a': [
    { op: 'setFlag', flag: OPEN },
    { op: 'say', speaker: 'ODALIE', text: 'You walk like someone who\'s been walking a long time.' },
    { op: 'say', speaker: 'ODALIE', text: 'The watch tries every traveller. Not to turn them back. To know them. Let me know you.' },
    { op: 'battle', trainer: 'underways_watch_a' },
    { op: 'say', speaker: 'ODALIE', text: 'Now I know you. [[The fire\'s down the ladder]], through the cistern. Tell Clemency Odalie sent you.' },
    { op: 'setFlag', flag: 'flag:underways_watch_a_beaten' },
  ],
  'script.underways_watch_b': [
    { op: 'setFlag', flag: OPEN },
    { op: 'say', speaker: 'BRAN', text: 'Hold. The watch-fire\'s through here, and I keep the way to it.' },
    { op: 'say', speaker: 'BRAN', text: 'Everyone who sits by that fire is tried first. Even the Warden was, once. He lost, and laughed about it.' },
    { op: 'battle', trainer: 'underways_watch_b' },
    { op: 'say', speaker: 'BRAN', text: 'Through you go. Mind the sleepers in the alcove.' },
    { op: 'setFlag', flag: 'flag:underways_watch_b_beaten' },
  ],
  'script.underways_watch_c': [
    { op: 'setFlag', flag: OPEN },
    { op: 'say', speaker: 'HESK', text: 'The east stair, up to the Ring. The last post of the last watch, and you\'re the last I\'ll stand it for, I think.' },
    { op: 'say', speaker: 'HESK', text: 'So let\'s make it a good one. I\'ll tell them I saw the lamp-tender\'s apprentice fight, the night before.' },
    { op: 'battle', trainer: 'underways_watch_c' },
    { op: 'say', speaker: 'HESK', text: 'Good. [[Up the stair]], then, and across the dark [[to the door]]. We\'ll be down here.' },
    { op: 'setFlag', flag: 'flag:underways_watch_c_beaten' },
  ],

  // ---- the caches ------------------------------------------------------------------------
  'script.pickup_underways_starglass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Behind the glow-moss, in an empty lamp-niche: a sliver of starlight gone to glass. Found a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_underways_starglass' },
  ],
  'script.pickup_underways_lumen': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'A watcher\'s tin tied with grey wool: FOR WHOEVER GOES UP. Found a LUMEN DROP and a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_underways_lumen' },
  ],
};

export const UNDERWAYS_DIALOGUE: DialogueRegistry = {
  'npc.underways_ring_lamp': [
    { text: 'A hooded lantern on a staff, its slit of light toward the threshold. Chalked below: an arrow, pointing down.' },
  ],
  'sign.underways_mouth': [
    { text: 'Scratched into the stair-post:\n"THE WATCH-ROAD. Go quiet. Go down. There is a fire at the bottom."' },
  ],
  'sign.underways_watch': [
    { text: 'THE LAST WATCH\n"We keep no gate. We keep a fire. Whoever comes down is welcome to it."' },
  ],
  'sign.underways_warmstones': [
    { text: 'Chalked on a flat stone:\n"THE WARM STONES. Let the light-kin be. They only come for the fire.\nIf the jester comes, CLAP. It waits for it."' },
  ],
  'npc.underways_watch_a_after': [
    { speaker: 'ODALIE', text: 'I trimmed the Coldfog road\'s lamps, before. When they asked, I trimmed the last ones out. Same scissors. I still have them.' },
  ],
  'npc.underways_watch_b_after': [
    { speaker: 'BRAN', text: 'Funny, keeping watch under a tower you hope nobody climbs. Funnier to find you hope someone does.' },
  ],
  'npc.underways_watch_c_after': [
    { speaker: 'HESK', text: 'If you see the Warden up there, tell him Hesk says the stair\'s swept. He\'ll know.' },
  ],
};
