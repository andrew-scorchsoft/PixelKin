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
 *   flag:underways_watch_kept         the whole watch met (all three tried, Clemency told)
 * Reads flag:dawn (the post-dawn branches).
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

const DAWN = 'flag:dawn';
const OPEN = 'flag:q_underways';

export const UNDERWAYS_SCRIPTS: ScriptRegistry = {
  // ---- signposting: the way down, heard of before it's walked -------------------------
  // Andrew's P.S. (run from script.andrew_hint once the hub is open, before the Keystar).
  'script.underways_hint': [
    { op: 'say', speaker: 'ANDREW', text: 'One more thing, if you want a fire before the climb. The Hollowing keep a last watch under the Penumbra Ring. Down the old stair past the starlit dark, south-west corner. Nobody\'s turned away from it, they say.', unless_flag: 'flag:underways_watchfire_rested' },
    { op: 'setFlag', flag: OPEN },
  ],
  // The Ring's light-well (seen before reached): a grate in the south strip's floor.
  'script.underways_lightwell': [
    { op: 'narrate', text: 'An iron grate, set flush in the stone. You kneel and look down it.', unless_flag: 'flag:underways_lightwell_seen' },
    { op: 'narrate', text: 'Far, far down: a pale column of light standing in the dark, and beside it, small and orange, a fire someone is keeping. A voice comes up the shaft, laughing at something. Then a kettle.', unless_flag: DAWN },
    { op: 'narrate', text: 'Far down, the old shaft is full of morning, right to the floor. Someone down there is still keeping a fire, out of habit.', if_flag: DAWN },
    { op: 'setFlag', flag: 'flag:underways_lightwell_seen' },
    { op: 'setFlag', flag: OPEN },
  ],
  // The mouths' "not yet" (a gated warp's blocked_ref): it opens the journal entry.
  'script.underways_mouth_shut': [
    { op: 'narrate', text: 'Old steps go down into the dark under the Ring. A hooded lamp hangs at the top, turned low. Not yet: the watch keeps its stair for whoever has lit all eight.' },
    { op: 'setFlag', flag: OPEN },
  ],

  // ---- the Last Watch's fire (the REST POINT) -----------------------------------------
  'script.underways_watchfire_rest': [
    { op: 'say', speaker: 'CLEMENCY', text: 'Sit. Sit, sit. Nobody comes down this far without needing the fire, and nobody\'s turned away from it. That was always the rule.', unless_flag: 'flag:underways_watchfire_rested' },
    { op: 'narrate', text: 'The watch-fire burns low under an iron hood, enough light to see a face by and no more. Above, somewhere, the whole weight of the Ring. Above that, the Spire.', unless_flag: 'flag:underways_watchfire_rested' },
    { op: 'setFlag', flag: 'flag:underways_watchfire_rested' },
    { op: 'setFlag', flag: OPEN },
    { op: 'heal' },
    { op: 'narrate', text: 'Your kin wake warm. Old Clemency has put a blanket over them in the night, and folded it again before they stirred.' },
  ],

  // ---- the view up the Spire's shaft (seen, never climbed) ---------------------------
  'script.underways_shaft_view': [
    { op: 'narrate', text: 'The roots of the mountain open here on a round pit, worked and smooth, and you look up.', unless_flag: 'flag:underways_shaft_seen' },
    { op: 'narrate', text: 'Straight up. Up through the Ring\'s stone, up through the dark heart of the Spire, a shaft so tall its top is a single point of pale light. The Crown\'s light, falling all that way, and arriving here as a whisper.', unless_flag: 'flag:underways_shaft_seen' },
    { op: 'narrate', text: 'There is no way up it. There never was. It was dug so somebody could stand at the bottom and look.', unless_flag: 'flag:underways_shaft_seen' },
    { op: 'narrate', text: 'Off to one side, high in the rock, a little square of starlight: the grate in the Ring\'s floor, where you knelt and looked down.', if_flag: 'flag:underways_lightwell_seen', unless_flag: 'flag:underways_shaft_seen' },
    { op: 'setFlag', flag: 'flag:underways_shaft_seen' },
    { op: 'narrate', text: 'The pale point at the top of the shaft. The way up is out in the Ring, through the Spire\'s own door.', unless_flag: DAWN },
    { op: 'narrate', text: 'The shaft is full of morning now, a bright column right to the floor. Someone has set a cushion at the bottom of it.', if_flag: DAWN },
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
    { op: 'say', speaker: 'CLEMENCY', text: 'Odalie, Bran and Hesk, all three. You\'ve met the whole of the last watch now, dear. There aren\'t any more of us. There never were very many.' },
    { op: 'setFlag', flag: 'flag:underways_watch_kept' },
  ],
  'script.underways_clemency_dusk': [
    { op: 'face', actor: 'clemency', facing: 'down' },
    { op: 'say', speaker: 'CLEMENCY', text: 'So you\'re the one. They said you\'d come down here sooner or later. People always want to see the bottom of things before the top.', unless_flag: 'flag:underways_clemency_met' },
    { op: 'say', speaker: 'CLEMENCY', text: 'This is the last watch. Not a guard. We\'re not here to stop anybody. We\'re here so that when it\'s over, up there, somebody who loves him is close by.', unless_flag: 'flag:underways_clemency_met' },
    { op: 'say', speaker: 'CLEMENCY', text: 'I taught him his letters, you know. The Warden. Long before he was anybody\'s Warden. He was a careful boy. Too careful with his sorrows. He kept every one.', unless_flag: 'flag:underways_clemency_met' },
    { op: 'say', speaker: 'CLEMENCY', text: 'If you go round by the east cut and down the slump, there are warm stones in the far pocket. A light-kin comes to them, ember and light both, for the fire. I\'ve never seen one up top.', unless_flag: 'flag:underways_clemency_met' },
    { op: 'setFlag', flag: 'flag:underways_clemency_met' },
    { op: 'setFlag', flag: OPEN },
    { op: 'say', speaker: 'CLEMENCY', text: 'The fire\'s yours whenever you want it. Rest, and then go up and do what you have to. Be kind to him, if you can manage it.' },
  ],
  'script.underways_clemency_dawn': [
    { op: 'emote', actor: 'clemency', emote: 'heart' },
    { op: 'say', speaker: 'CLEMENCY', text: 'He came down, after. Sat right there by the fire and didn\'t say a word for an hour. Then he asked me if I still had the kettle.' },
    { op: 'say', speaker: 'CLEMENCY', text: 'I did. I always did. Sit down, dear. You\'ve earned a cup.' },
  ],

  // ---- the three watchers (the Hollowing's last watch) ---------------------------------
  'script.underways_watch_a': [
    { op: 'setFlag', flag: OPEN },
    { op: 'say', speaker: 'ODALIE', text: 'Down the old stair from the Ring. You walk like someone who\'s been walking a long time.' },
    { op: 'say', speaker: 'ODALIE', text: 'The watch is asked to try every traveller. Not to turn them back. To know them. Let me know you.' },
    { op: 'battle', trainer: 'underways_watch_a' },
    { op: 'say', speaker: 'ODALIE', text: 'There. Now I know you. The fire\'s down the ladder and through the cistern. Tell Clemency Odalie sent you, she\'ll put the kettle on.' },
    { op: 'setFlag', flag: 'flag:underways_watch_a_beaten' },
  ],
  'script.underways_watch_b': [
    { op: 'setFlag', flag: OPEN },
    { op: 'say', speaker: 'BRAN', text: 'Hold. The watch-fire\'s through here, and I\'m the one that keeps the way to it.' },
    { op: 'say', speaker: 'BRAN', text: 'Everyone who\'s sat by that fire has been tried first. Even the Warden was, once. He lost, too. He laughed about it.' },
    { op: 'battle', trainer: 'underways_watch_b' },
    { op: 'say', speaker: 'BRAN', text: 'Through you go. Mind the sleepers in the alcove. They don\'t like to be stepped over.' },
    { op: 'setFlag', flag: 'flag:underways_watch_b_beaten' },
  ],
  'script.underways_watch_c': [
    { op: 'setFlag', flag: OPEN },
    { op: 'say', speaker: 'HESK', text: 'The east stair, back up to the Ring. The last post of the last watch, and you\'re the last thing I\'ll ever stand it for, I think.' },
    { op: 'say', speaker: 'HESK', text: 'So let\'s make it a good one. Then I can tell them I saw the lamp-tender\'s apprentice fight, the night before.' },
    { op: 'battle', trainer: 'underways_watch_c' },
    { op: 'say', speaker: 'HESK', text: 'Good. That was good. Up the stair, then, and across the dark to the door. We\'ll be down here.' },
    { op: 'setFlag', flag: 'flag:underways_watch_c_beaten' },
  ],

  // ---- the caches ------------------------------------------------------------------------
  'script.pickup_underways_starglass': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Behind the glow-moss, in a niche cut for a lamp that was never set there: a sliver of starlight gone to glass. Found a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:picked_underways_starglass' },
  ],
  'script.pickup_underways_lumen': [
    { op: 'sfx', key: 'world-chest' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'giveItem', item: 'hearth_coal', count: 1 },
    { op: 'say', text: 'A watcher\'s tin, tied up with grey wool, a slate on the lid: FOR WHOEVER GOES UP. Found a LUMEN DROP and a HEARTH COAL!' },
    { op: 'setFlag', flag: 'flag:picked_underways_lumen' },
  ],
};

export const UNDERWAYS_DIALOGUE: DialogueRegistry = {
  'npc.underways_ring_lamp': [
    { text: 'A hooded lantern on a staff, its slit of light turned toward the dark by the threshold. Below it, chalked on the rock: an arrow, pointing down.' },
  ],
  'sign.underways_mouth': [
    { text: 'Scratched into the stair-post:\n"THE WATCH-ROAD. Go quiet. Go down. There is a fire at the bottom."' },
  ],
  'sign.underways_watch': [
    { text: 'THE LAST WATCH\n"We keep no gate. We keep a fire. Whoever comes down is welcome to it."' },
  ],
  'sign.underways_warmstones': [
    { text: 'Chalked on a flat stone, in a careful hand:\n"THE WARM STONES. Let the light-kin be. They only come for the fire."' },
  ],
  'npc.underways_watch_a_after': [
    { speaker: 'ODALIE', text: 'I trimmed the lamps along the Coldfog road, before. When they asked, I trimmed the last ones too. Same scissors. I still have them.' },
  ],
  'npc.underways_watch_b_after': [
    { speaker: 'BRAN', text: 'Funny thing, keeping watch under a tower you\'re hoping nobody climbs. Funnier still to find you\'re hoping someone does.' },
  ],
  'npc.underways_watch_c_after': [
    { speaker: 'HESK', text: 'If you see him up there, the Warden, tell him Hesk says the stair\'s swept. He\'ll know what it means.' },
  ],
};
