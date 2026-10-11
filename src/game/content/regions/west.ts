/**
 * WEST world-craft content (docs/reviews/world-craft-panel.md §6): this region's
 * package OWNS this file — new optional scripts + dialogue only, spread into the
 * registries via regions/index.ts. Map placements that reference these refs ride
 * tools/maps/worldcraft/west.py (run through tools/maps/add_world_craft.py), the
 * West builders (Coldfog/Drownlight/Sunvault/Hushfrost R10 dressing) and
 * tools/maps/add_peril_thread.py (the Hushfrost pass-walker).
 *
 * Everything here is OPTIONAL colour: nothing gates a lane or a warp, and every
 * staged line uses the if_flag + unless_flag pair so exactly one plays.
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

export const WEST_SCRIPTS: ScriptRegistry = {
  // ===========================================================================
  // HUSHFROST PASS I — the frozen falls (the north nook's payoff)
  // ===========================================================================
  'script.hushfrost_falls': [
    { op: 'narrate', text: 'The waterfall froze where it fell and never finished falling. Behind the ice you can just see the water still moving — slow as a thought, still trying.' },
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'Somebody has scratched a tally into the ice at shoulder height. Eleven marks. One for every winter it has hung here.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'Water is running behind the ice now, loud and ordinary. The eleven tally-marks are softening at the edges.' },
  ],

  // ===========================================================================
  // W-4 — "THE PASS-WALKER'S MAP" (optional; the spiral of falls)
  // The pass-walker counts the falls she has seen. The player marks craters
  // (flag:fall_seen_<site>); each mark ticks a flag counter (passmap_1..4).
  // At three she spreads the map at Nightreach: the falls are a SPIRAL, and
  // the middle of it is the Spire. Other packages may add sites by setting
  // their own flag:fall_seen_<site> and running script.passmap_tick.
  // ===========================================================================
  // The counter: a flag cascade, highest first (each step guards on the one
  // below it, so a single run advances exactly one rung).
  'script.passmap_count': [
    { op: 'setFlag', if_flag: 'flag:passmap_3', flag: 'flag:passmap_4' },
    { op: 'setFlag', if_flag: 'flag:passmap_2', unless_flag: 'flag:passmap_3', flag: 'flag:passmap_3' },
    { op: 'setFlag', if_flag: 'flag:passmap_1', unless_flag: 'flag:passmap_2', flag: 'flag:passmap_2' },
    { op: 'setFlag', unless_flag: 'flag:passmap_1', flag: 'flag:passmap_1' },
  ],
  // A fall marked while the map is open counts at once; one seen before is
  // counted when she opens it (see script.passwalker).
  'script.passmap_tick': [
    { op: 'run', if_flag: 'flag:q_west_passmap', ref: 'script.passmap_count' },
  ],
  'script.fall_mark_sunvault': [
    { op: 'narrate', text: 'A cinder in a scorch on the terrace stone — cold, faintly blue in its cracks. It came down on what was once a garden of the sun.' },
    { op: 'narrate', if_flag: 'flag:q_west_passmap', unless_flag: 'flag:fall_seen_sunvault', text: 'You fix it the way the pass-walker showed you: where it lies, and which way the scorch was thrown. Toward the middle of the world.' },
    { op: 'run', unless_flag: 'flag:fall_seen_sunvault', ref: 'script.passmap_tick' },
    { op: 'setFlag', flag: 'flag:fall_seen_sunvault' },
  ],
  'script.fall_mark_coldfog': [
    { op: 'narrate', text: 'A fresh crater in the drained marsh. The cinder at its heart is the coldest thing you have ever stood beside, and the fog does not go near it.' },
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'This is the nearest fall to the mountain you have seen. The scorch points straight at it, like a finger.' },
    { op: 'narrate', if_flag: 'flag:q_west_passmap', unless_flag: 'flag:fall_seen_coldfog', text: 'You mark it for the pass-walker. Your hand is not quite steady doing it.' },
    { op: 'run', unless_flag: 'flag:fall_seen_coldfog', ref: 'script.passmap_tick' },
    { op: 'setFlag', flag: 'flag:fall_seen_coldfog' },
  ],
  // The pass-walker at her camp by the Hushfrost crater: her peril lines first
  // (staged in scripts.ts), then the map. She walks on ahead once it is open.
  'script.passwalker': [
    { op: 'run', ref: 'script.peril_hushfrost_counter' },
    { op: 'wait', unless_flag: 'flag:q_west_passmap', ms: 600 },
    { op: 'say', unless_flag: 'flag:q_west_passmap', speaker: 'PASS-WALKER', text: 'You look at the crater properly. Most folk glance and hurry. Here — you should see this.' },
    { op: 'narrate', unless_flag: 'flag:q_west_passmap', text: 'She unrolls an oilcloth map on her knee and pins its corners with stones. Iron tacks mark two places: the orchard, far to the south, and here.' },
    { op: 'say', unless_flag: 'flag:q_west_passmap', speaker: 'PASS-WALKER', text: "If you pass another fall — a scorch, a cinder, a dead patch where something came down — stand by it a while and remember where it lies. Then find me at Nightreach. The watchers keep a table wide enough to spread this out." },
    // open the map: this crater counts, the orchard counts if you saw it, and
    // any fall already seen elsewhere counts now (other regions' sites included)
    { op: 'run', unless_flag: 'flag:q_west_passmap', ref: 'script.passmap_open' },
    { op: 'move', unless_flag: 'flag:q_west_passmap_left', actor: 'peril_hushfrost_counter', to: { tx: 12, ty: 22 } },
    { op: 'setFlag', unless_flag: 'flag:q_west_passmap_left', flag: 'flag:q_west_passmap_left' },
  ],
  'script.passmap_open': [
    { op: 'setFlag', flag: 'flag:q_west_passmap' },
    { op: 'run', ref: 'script.passmap_count' },
    { op: 'run', if_flag: 'flag:orchard_strike_seen', ref: 'script.passmap_count' },
    { op: 'run', if_flag: 'flag:fall_seen_cinderhead', ref: 'script.passmap_count' },
    { op: 'run', if_flag: 'flag:fall_seen_galehigh', ref: 'script.passmap_count' },
    { op: 'run', if_flag: 'flag:fall_seen_sunvault', ref: 'script.passmap_count' },
    { op: 'run', if_flag: 'flag:fall_seen_coldfog', ref: 'script.passmap_count' },
  ],
  // At Nightreach (requires flag:q_west_passmap): not enough yet, the spiral,
  // or her quiet after-line.
  'script.passwalker_nightreach': [
    { op: 'say', unless_flag: 'flag:passmap_3', speaker: 'PASS-WALKER', text: 'Two tacks make a line, and a line is only a road. Bring me one more fall. The Sunvault terraces had a scorch, folk said. The Coldfog will have worse.' },
    { op: 'run', if_flag: 'flag:passmap_3', unless_flag: 'flag:q_west_passmap_done', ref: 'script.passmap_spiral' },
    { op: 'say', if_flag: 'flag:q_west_passmap_done', unless_flag: 'flag:dawn', speaker: 'PASS-WALKER', text: "I've stopped walking the pass. I sit up here and watch the middle of the map instead. Nothing's fallen tonight. I count that as news." },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'PASS-WALKER', text: 'The cinder in my pass woke, they tell me. Bright as a hearth in the snow. I took the map down. Kept the tacks, though.' },
  ],
  'script.passmap_spiral': [
    { op: 'letterbox', on: true, ms: 360 },
    { op: 'narrate', text: 'She spreads the oilcloth on the watchers\' table and you call out the falls. One by one she pushes in the iron tacks — the orchard in the far south, her pass in the west, the places you have stood since.' },
    { op: 'say', speaker: 'PASS-WALKER', text: 'Draw a line through them. Go on.' },
    { op: 'wait', ms: 900 },
    { op: 'silence', ms: 1200 },
    { op: 'say', speaker: 'PASS-WALKER', text: "...It's not a line. It's a spiral. And the middle of it is the Spire." },
    { op: 'tint', color: '#2a3550', alpha: 0.32, ms: 800 },
    { op: 'starfall', wait: true, from: 'right' },
    { op: 'narrate', text: 'Out past the dome, as if it had been listening, a cold streak crosses the sky and goes down behind the mountain. Neither of you says anything for a while.' },
    { op: 'tint', color: '#2a3550', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'PASS-WALKER', text: "They're going home. Every star that gutters falls a little nearer the one they were all lit from. Take this — it came down warm, long before the Dusk. I'd like one of them to be somewhere hopeful." },
    { op: 'sfx', key: 'world-gleam-a' },
    { op: 'giveItem', item: 'starglass_shard', count: 1 },
    { op: 'say', text: 'Received a STARGLASS SHARD!' },
    { op: 'setFlag', flag: 'flag:q_west_passmap_done' },
    { op: 'letterbox', on: false, ms: 360 },
  ],

  // ===========================================================================
  // W-2 — Còr in the West: the figure on the far gantry (before the band he
  // stands there, back turned; he does not answer).
  // ===========================================================================
  'script.stillworks_cor_silent': [
    { op: 'narrate', text: 'The cowled figure on the gantry does not turn. He is wiping a lantern-collar with a soft cloth, slowly, as if it might bruise.' },
  ],

  // ===========================================================================
  // COLDFOG MARCHES + DROWNLIGHT — desolation, authored. Zero humour; the
  // register is elegiac. Each read is one or two lines and then silence.
  // ===========================================================================
  'script.coldfog_set_table': [
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'A table laid for three under no roof at all. Three plates, three cups, a candle that was never lit. Nobody cleared it. Nobody came back to eat.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'Someone has cleared the table at last. One cup is missing — taken home, you would guess, by whoever came back for it.' },
  ],
  'script.coldfog_boat': [
    { op: 'narrate', text: 'A rowboat pulled up out of water that has stopped moving. The oar is still shipped, ready, and the fog has beaded on the seat where someone sat to think it over.' },
  ],
  'script.coldfog_boat_ii': [
    { op: 'narrate', text: 'Another boat on another bank. Not wrecked — put away, neat as shoes by a door, by people who did not expect to need it again.' },
  ],
  'script.drownlight_boat': [
    { op: 'narrate', text: "The keeper's boat, drawn up past the tide-line of a sea that has no tides any more. The rope is coiled. Whoever coiled it meant to come back." },
  ],
  // Doused lamp-posts take your flame for a breath, then gutter: Coldfog does
  // not put light out, it waits for light to stop (the canon, made felt).
  'script.coldfog_relight': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.16, ms: 400 },
    { op: 'narrate', text: 'The cold wick takes your flame. For one breath the post remembers what it was for — a small gold circle on the grey.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 1000 },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'Then the fog leans in, the way a tired hand closes a book, and the flame goes out. Coldfog does not take light. It waits for light to stop.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'It holds. In the thin daylight it is hardly needed, and it holds anyway.' },
  ],
  'script.coldfog_notice': [
    { op: 'narrate', text: "A neat hand on clean paper: 'NEIGHBOURS — You need not keep watch any longer. Let the lamps rest. Let your kin rest. Let yourselves rest. Nothing here will fade again; we have seen to it. — Your friends of the Quiet.'" },
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'It has been pinned square, and recently. The fog has not so much as curled the corners.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: "The paper has curled now. Under it, in pencil, someone has written: 'We kept watch anyway.'" },
  ],
  'script.coldfog_notice_works': [
    { op: 'narrate', text: "A card in a little glass case, beautifully lettered: 'THE HOLLOWFEN STILLWORKS. Tended. Visitors are welcome. Please close the door gently — the lanterns are resting.'" },
  ],
  // The hollow-eyed villager on the blight line (hidden at dawn: gone home).
  'script.coldfog_villager': [
    { op: 'say', unless_flag: 'gleam:lunar', speaker: 'VILLAGER', text: "We had a festival here once. Lanterns on the water. I think it was... no. It doesn't matter. Nothing has to matter now. That's the nice part." },
    { op: 'say', if_flag: 'gleam:lunar', speaker: 'VILLAGER', text: "Eight stars, they said at the camp. I counted. I counted twice. I don't... I don't know what to do with my hands." },
    { op: 'narrate', text: 'She smiles at you the way you might smile at a stranger\'s dog, and walks on along the grey.' },
  ],
  // A Hollowing acolyte at the works' door — gentle, half-right, never cruel.
  'script.coldfog_acolyte': [
    { op: 'say', speaker: 'HOLLOWING ACOLYTE', text: "Oh — you've a lit lamp. That's all right. I don't take them. I only help them rest when they're tired, and this road was so tired." },
    { op: 'say', unless_flag: 'gleam:lunar', speaker: 'HOLLOWING ACOLYTE', text: 'The works are just through there, if you want to see how quiet it can be. No one will stop you. We never stop anyone.' },
    { op: 'say', if_flag: 'gleam:lunar', speaker: 'HOLLOWING ACOLYTE', text: "The Crown is whole, they say. The Warden says it changes nothing. He said it very kindly. ...He hasn't slept since." },
  ],

  // ===========================================================================
  // SUNVAULT CLIMB — the fallen sun-dial
  // ===========================================================================
  'script.sunvault_sundial': [
    { op: 'narrate', text: 'A sun-dial, toppled, its gnomon snapped off clean. The hour-lines are cut deep and gilded, made for a sun that crossed this terrace every single day.' },
    { op: 'narrate', unless_flag: 'gleam:solar', text: 'The gilt holds no shadow. It has not told an hour in eleven years.' },
    { op: 'narrate', if_flag: 'gleam:solar', text: 'Under the Solar Gleam a thin gold shadow lies across it again. Not on any hour. Near enough.' },
  ],

  // ===========================================================================
  // W-1 WITNESS — Brisa, the morning after the Ember flickered (a staged
  // replacement for npc.brisa_after on the tinderwick_lumenary map; the
  // SOUTH map's placement swap is listed in the West package report).
  // ===========================================================================
  'script.brisa_after_staged': [
    { op: 'dialogue', unless_flag: 'flag:great_null_known', ref: 'npc.brisa_after' },
    { op: 'say', if_flag: 'flag:great_null_known', unless_flag: 'gleam:lunar', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'The beacon went out on its own last night, dear. Only for a breath. I relit it with my hands shaking — and I have lit that wick a thousand times.' },
    { op: 'dialogue', if_flag: 'gleam:lunar', ref: 'npc.brisa_after' },
  ],
};

export const WEST_DIALOGUE: DialogueRegistry = {};
