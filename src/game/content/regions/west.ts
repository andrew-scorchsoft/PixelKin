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

// ---------------------------------------------------------------------------
// AFTER-GLEAM (2026-10): the Sunken Solarium and Nightreach answer their Gleams.
// Placements ride tools/maps/worldcraft/west.py (`after` twins, `talk`
// re-points); the pre-Gleam branch of a staged script is the original ref.
// ---------------------------------------------------------------------------
const SOLAR = 'gleam:solar';
const LUNAR = 'gleam:lunar';

const WEST_AFTER_SCRIPTS: ScriptRegistry = {
  'script.solarium_witness_staged': [
    { op: 'dialogue', ref: 'npc.solarium_witness', unless_flag: SOLAR },
    { op: 'dialogue', ref: 'npc.solarium_witness_lit', if_flag: SOLAR },
  ],
  'script.solarium_rest_lit': [
    { op: 'say', speaker: 'MATRON', text: "In off the water, pilgrim. The players are weeping happily. Sit, warm up." },
    { op: 'heal' },
    { op: 'say', speaker: 'MATRON', text: "There. Forty years, and nobody mourns the Last-Warm-Day tonight." },
  ],
  // The vigil warden's last stage already hangs on the Star-vigil having played.
  'script.star_vigil_warden_staged': [
    { op: 'dialogue', ref: 'npc.star_vigil_warden_after', unless_flag: LUNAR },
    { op: 'dialogue', ref: 'npc.star_vigil_warden_lit', if_flag: LUNAR },
  ],
  'script.nightreach_inn_rest_lit': [
    { op: 'say', speaker: 'INNKEEP', text: "Nobody's sleeping tonight! Eight stars. Even my day-sleepers are out." },
    { op: 'heal' },
    { op: 'say', speaker: 'INNKEEP', text: "Rested. Whatever waits on that mountain, the whole town watches with you." },
  ],
};

const WEST_AFTER_DIALOGUE: DialogueRegistry = {
  // --- the Sunken Solarium (gleam:solar) --------------------------------------
  'npc.solarium_festival_goer_lit': [
    { speaker: 'FESTIVAL-GOER', text: "\"Spend warm days until one sticks,\" I said. This one stuck. Now what?" },
  ],
  'npc.solarium_bread_lit': [
    { speaker: 'BREAD-SHARER', text: "Warm bread, no charge! My oven's stored daylight flared. Gold crust!" },
    { speaker: 'BREAD-SHARER', text: "Eat it slowly. That's the new custom. I've just made it up." },
  ],
  'npc.solarium_kid_lit': [
    { speaker: 'FESTIVAL KID', text: "The gold in the water went BRIGHTER! My sleeve's ruined. Don't care." },
  ],
  'npc.solarium_prompter_lit': [
    { speaker: 'PROMPTER', text: "Forty years I prompted from dark wings. Tonight they were LIT. Joy!" },
  ],
  'npc.solarium_hall_keeper_lit': [
    { speaker: 'SUN-LEDGER KEEPER', text: "Tonight's ledger: \"and the sun's own star stood over the stage.\" I left the page's rest blank. It isn't finished with us." },
  ],
  'npc.solarium_witness_lit': [
    { speaker: 'OLD STAGEHAND', text: "I rigged that stage as a boy. Tomorrow I rig it for a lit house." },
  ],
  // --- Nightreach Observatory (gleam:lunar) -----------------------------------
  'npc.nightreach_watcher_steps_a_lit': [
    { speaker: 'OLD WATCHER', text: "Eight lamps lit, and I'm still holding mine. Nobody said when to put them down." },
  ],
  'npc.nightreach_watcher_steps_b_lit': [
    { speaker: 'WATCH KID', text: "I RAN the bell route! Rang the last one lying down. Best part, they say." },
  ],
  'npc.star_vigil_warden_lit': [
    { speaker: 'VIGIL WARDEN', text: "When the last star came home, the whole town stood up to do nothing at all." },
    { speaker: 'VIGIL WARDEN', text: "Go when you're ready. We'll keep watching. That is what watching IS." },
  ],
  'npc.nightreach_home_elder_lit': [
    { speaker: 'LENS-GRINDER', text: "The dome's lens held all eight! Same work, child. It always was." },
  ],
  'npc.nightreach_home_kid_lit': [
    { speaker: 'WATCHER KID', text: "I inked the eighth star in! Then I drew the mountain, with a lamp on top." },
  ],
  'npc.nightreach_inn_guest_lit': [
    { speaker: 'TIRED GUEST', text: "I booked the week off and the sky finished itself while I was ASLEEP." },
  ],
  'npc.nightreach_inn_watcher_lit': [
    { speaker: 'OFF-SHIFT WATCHER', text: "Dawn-watch was the rota's sad joke. Now everyone's fighting for it." },
  ],
  'npc.nightreach_hall_keeper_lit': [
    { speaker: 'NIGHT-CLERK', text: "My just-in-case page got used: \"The eighth came home.\" I've ruled another." },
  ],
};

export const WEST_SCRIPTS: ScriptRegistry = {
  ...WEST_AFTER_SCRIPTS,
  // ===========================================================================
  // HUSHFROST PASS I — the frozen falls (the north nook's payoff)
  // ===========================================================================
  'script.hushfrost_falls': [
    { op: 'narrate', text: 'The waterfall froze mid-fall. Behind the ice the water still moves, still trying.' },
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'A tally scratched in the ice. Eleven marks: one for every winter.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'Water runs behind the ice now, loud and ordinary. The tally is softening.' },
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
    { op: 'narrate', text: 'A cinder in a scorch on the terrace stone, faintly blue in its cracks.' },
    { op: 'narrate', if_flag: 'flag:q_west_passmap', unless_flag: 'flag:fall_seen_sunvault', text: 'You mark it as the pass-walker showed you: where it lies, and which way the scorch points. Toward the middle of the world.' },
    { op: 'run', unless_flag: 'flag:fall_seen_sunvault', ref: 'script.passmap_tick' },
    { op: 'setFlag', flag: 'flag:fall_seen_sunvault' },
  ],
  'script.fall_mark_coldfog': [
    { op: 'narrate', text: 'A fresh crater in the drained marsh. Its cinder is so cold the fog keeps away.' },
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'The nearest fall to the mountain yet. The scorch points at it like a finger.' },
    { op: 'narrate', if_flag: 'flag:q_west_passmap', unless_flag: 'flag:fall_seen_coldfog', text: 'You mark it for the pass-walker. Your hand is not quite steady doing it.' },
    { op: 'run', unless_flag: 'flag:fall_seen_coldfog', ref: 'script.passmap_tick' },
    { op: 'setFlag', flag: 'flag:fall_seen_coldfog' },
  ],
  // The pass-walker at her camp by the Hushfrost crater: her peril lines first
  // (staged in scripts.ts), then the map. She walks on ahead once it is open.
  'script.passwalker': [
    { op: 'run', ref: 'script.peril_hushfrost_counter' },
    // The map is a Long-Dusk errand: after dawn she has taken it down.
    { op: 'run', unless_flag: 'flag:dawn', ref: 'script.passwalker_offer' },
  ],
  'script.passwalker_offer': [
    { op: 'wait', unless_flag: 'flag:q_west_passmap', ms: 600 },
    { op: 'say', unless_flag: 'flag:q_west_passmap', speaker: 'PASS-WALKER', text: 'You look at the crater properly. Most folk hurry by. Here, see this.' },
    { op: 'narrate', unless_flag: 'flag:q_west_passmap', text: 'She unrolls an oilcloth map, pinned with stones. Iron tacks mark two places: the orchard, far south, and here.' },
    { op: 'say', unless_flag: 'flag:q_west_passmap', speaker: 'PASS-WALKER', text: "If you pass another fall, [[stand by it a while]] and remember where it lies. Then [[find me at Nightreach]]." },
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
    { op: 'run', unless_flag: 'flag:dawn', ref: 'script.passwalker_ask' },
    { op: 'run', if_flag: 'flag:passmap_3', unless_flag: 'flag:q_west_passmap_done', ref: 'script.passmap_spiral' },
    { op: 'say', if_flag: 'flag:q_west_passmap_done', unless_flag: 'flag:dawn', speaker: 'PASS-WALKER', text: "I watch the middle of the map now. Nothing's fallen tonight. That's news." },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'PASS-WALKER', text: 'The cinder in my pass woke, they say. I took the map down. Kept the tacks.' },
  ],
  // Not enough falls yet — only asked before dawn (after it, the map is down).
  'script.passwalker_ask': [
    { op: 'say', unless_flag: 'flag:passmap_3', speaker: 'PASS-WALKER', text: 'Two tacks make a line, and a line is only a road. [[Bring me one more fall]]: try [[Sunvault or the Coldfog]].' },
  ],
  'script.passmap_spiral': [
    { op: 'letterbox', on: true, ms: 360 },
    { op: 'narrate', text: 'She spreads the oilcloth on the watchers\' table. You call out the falls, and one by one she pushes in the iron tacks.' },
    { op: 'say', speaker: 'PASS-WALKER', text: 'Draw a line through them. Go on.' },
    { op: 'wait', ms: 900 },
    { op: 'silence', ms: 1200 },
    { op: 'say', speaker: 'PASS-WALKER', text: "...It's not a line. It's a spiral. And the middle of it is the Spire." },
    { op: 'tint', color: '#2a3550', alpha: 0.32, ms: 800 },
    { op: 'starfall', wait: true, from: 'right' },
    { op: 'narrate', text: 'Out past the dome a cold streak falls behind the mountain. Neither of you speaks.' },
    { op: 'tint', color: '#2a3550', alpha: 0, ms: 900 },
    { op: 'say', speaker: 'PASS-WALKER', text: "They're going home. Every guttering star falls nearer the one they were lit from. Take this. It fell warm, before the Dusk. Let one be somewhere hopeful." },
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
    { op: 'narrate', text: 'The cowled figure on the gantry does not turn. He wipes a lantern-collar, gently.' },
  ],

  // ===========================================================================
  // COLDFOG MARCHES + DROWNLIGHT — desolation, authored. Zero humour; the
  // register is elegiac. Each read is one or two lines and then silence.
  // ===========================================================================
  'script.coldfog_set_table': [
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'A table laid for three under no roof. A candle never lit. Nobody came back to eat.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'The table is cleared at last. One cup is missing, taken home.' },
  ],
  'script.coldfog_boat': [
    { op: 'narrate', text: 'A rowboat pulled up from still water, oar shipped. Fog beads the seat.' },
  ],
  'script.coldfog_boat_ii': [
    { op: 'narrate', text: 'Another boat, put away neat as shoes by a door. Not needed again.' },
  ],
  'script.drownlight_boat': [
    { op: 'narrate', text: "The keeper's boat, beached by a sea with no tides. Its rope is coiled, ready." },
  ],
  // Doused lamp-posts take your flame for a breath, then gutter: Coldfog does
  // not put light out, it waits for light to stop (the canon, made felt).
  'script.coldfog_relight': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffd089', alpha: 0.16, ms: 400 },
    { op: 'narrate', text: 'The cold wick takes your flame. For one breath the post remembers its job.' },
    { op: 'tint', color: '#ffd089', alpha: 0, ms: 1000 },
    { op: 'sfx', key: 'world-star-gutter' },
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'Then the fog leans in, like a tired hand closing a book, and the flame goes out. Coldfog waits for light to stop.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'It holds. In the thin daylight it is hardly needed. It holds anyway.' },
  ],
  'script.coldfog_notice': [
    { op: 'narrate', text: "Neat lettering: 'NEIGHBOURS. Let the lamps rest. Let yourselves rest. Nothing here will fade again. Your friends of the Quiet.'" },
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'Pinned square, and recently. The fog has not curled the corners.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: "The paper has curled. Under it, in pencil: 'We kept watch anyway.'" },
  ],
  'script.coldfog_notice_works': [
    { op: 'narrate', text: "A card in a glass case: 'HOLLOWFEN STILLWORKS. Visitors welcome. Close the door gently. The lanterns are resting.'" },
  ],
  // The hollow-eyed villager on the blight line (hidden at dawn: gone home).
  'script.coldfog_villager': [
    { op: 'say', unless_flag: 'gleam:lunar', speaker: 'VILLAGER', text: "We had a festival once. Lanterns on the water... no. Nothing has to matter now." },
    { op: 'say', if_flag: 'gleam:lunar', speaker: 'VILLAGER', text: "Eight stars, they said. I counted twice. I don't know what to do with my hands." },
    { op: 'narrate', text: 'She smiles as at a stranger\'s dog, and walks on along the grey.' },
  ],
  // A Hollowing acolyte at the works' door — gentle, half-right, never cruel.
  'script.coldfog_acolyte': [
    { op: 'say', speaker: 'HOLLOWING ACOLYTE', text: "Oh, a lit lamp. I don't take them. I only help them rest when they're tired." },
    { op: 'say', unless_flag: 'gleam:lunar', speaker: 'HOLLOWING ACOLYTE', text: 'The works are just through there. We never stop anyone.' },
    { op: 'say', if_flag: 'gleam:lunar', speaker: 'HOLLOWING ACOLYTE', text: "The Crown is whole. The Warden says it changes nothing. ...He hasn't slept since." },
  ],

  // ===========================================================================
  // SUNVAULT CLIMB — the fallen sun-dial
  // ===========================================================================
  'script.sunvault_sundial': [
    { op: 'narrate', text: 'A toppled sun-dial, its gnomon snapped clean, its hour-lines gilded.' },
    { op: 'narrate', unless_flag: 'gleam:solar', text: 'The gilt holds no shadow. Not one hour in eleven years.' },
    { op: 'narrate', if_flag: 'gleam:solar', text: 'Under the Solar Gleam a thin gold shadow lies across it. Not on any hour. Near enough.' },
  ],

  // ===========================================================================
  // W-1 WITNESS — Brisa, the morning after the Ember flickered (a staged
  // replacement for npc.brisa_after on the tinderwick_lumenary map; the
  // SOUTH map's placement swap is listed in the West package report).
  // ===========================================================================
  'script.brisa_after_staged': [
    { op: 'dialogue', unless_flag: 'flag:great_null_known', ref: 'npc.brisa_after' },
    { op: 'say', if_flag: 'flag:great_null_known', unless_flag: 'gleam:lunar', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'neutral', text: 'The beacon went out on its own last night, dear. Only a breath. I relit it with shaking hands, after a thousand lightings.' },
    { op: 'say', if_flag: 'gleam:lunar', unless_flag: 'flag:dawn', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'warm', text: 'All eight, dear. The beacon hasn\'t blinked since. Old habits keep old lamps lit.' },
    { op: 'say', if_flag: 'flag:dawn', speaker: 'BRISA TALLOW', portrait: 'brisa', expr: 'proud', text: 'Morning, dear. I let the beacon go out at sunrise, on purpose. It felt like setting a bird free.' },
  ],
};

export const WEST_DIALOGUE: DialogueRegistry = { ...WEST_AFTER_DIALOGUE };
