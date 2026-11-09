/**
 * EAST world-craft content (docs/reviews/world-craft-panel.md §6): this region's
 * package OWNS this file — new optional scripts + dialogue only, spread into the
 * registries via regions/index.ts. Map placements that reference these refs ride
 * tools/maps/worldcraft/east.py (run through tools/maps/add_world_craft.py) and,
 * for Saltreach Fen I's nook + lost village, tools/maps/build_saltreach_fen_i.py.
 *
 * Everything here is OPTIONAL colour (no required step, no gate): the fen's
 * eel-wife + her net-weights find, the Lantern Staithe line, the acolyte's
 * dropped cinder (story panel E-1), Wren's acted A3 (E-2), Harl's eight hooks
 * and the roof-fault cinder (E-3), and the two dungeon-floor vignettes.
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

// ---------------------------------------------------------------------------
// AFTER-GLEAM (2026-10): Lowleaf and Cinderhead answer their Gleams. Placements
// ride tools/maps/worldcraft/east.py (`after` twins, `talk` re-points); the
// pre-Gleam branch of every staged script is the original ref, untouched.
// ---------------------------------------------------------------------------
const VERDANT = 'gleam:verdant';
const STONE = 'gleam:stone';

const EAST_AFTER_SCRIPTS: ScriptRegistry = {
  'script.shop_lowleaf_staged': [
    { op: 'dialogue', ref: 'npc.lowleaf_provisioner', unless_flag: VERDANT },
    { op: 'dialogue', ref: 'npc.lowleaf_provisioner_lit', if_flag: VERDANT },
    { op: 'shop', shop: 'lowleaf_provisioner' },
  ],
  'script.lowleaf_rest_lit': [
    { op: 'say', speaker: 'BOWER-KEEPER', text: "Bunks are full, but there's always a bower for whoever woke the Elder Bed." },
    { op: 'heal' },
    { op: 'say', speaker: 'BOWER-KEEPER', text: "The moss in the eaves glowed all night. Nobody complained." },
  ],
  'script.shop_cinderhead_staged': [
    { op: 'dialogue', ref: 'npc.cinderhead_provisioner', unless_flag: STONE },
    { op: 'dialogue', ref: 'npc.cinderhead_provisioner_lit', if_flag: STONE },
    { op: 'shop', shop: 'cinderhead_provisioner' },
  ],
  'script.cinderhead_rest_lit': [
    { op: 'say', speaker: 'VIGIL COOK', text: "Sit by the vigil-fire. We've let it burn high tonight. Warm your kin." },
    { op: 'heal' },
    { op: 'say', speaker: 'VIGIL COOK', text: "There. The dark's still long. Tonight, for once, the fire's ahead." },
  ],
};

const EAST_AFTER_DIALOGUE: DialogueRegistry = {
  // --- Lowleaf Hollow (gleam:verdant) ---------------------------------------
  'npc.bloom_piper_lit': [
    { speaker: 'BLOOM PIPER', text: "A GREEN bed! Four crowning reels and they won't let me stop. My fingers are moss." },
  ],
  'npc.bloom_fencer_lit': [
    { speaker: 'FESTIVAL AUNTIE', text: "Green as a frog! Beds have bad years, I said. Never said they couldn't have good ones." },
    { speaker: 'FESTIVAL AUNTIE', text: "Have a moss-cake. I owe the town one apiece, and you're first." },
  ],
  'npc.bloom_kid_a_lit': [
    { speaker: 'MOSS KID', text: "My glow-mote wish came true! I wished the big bed would wake up." },
    { speaker: 'MOSS KID', text: "Don't tell the moss I wished twice. It might want one of them back." },
  ],
  'npc.bloom_kid_b_lit': [
    { speaker: 'FERN KID', text: "You walked into the deep wood like it was our back garden!" },
  ],
  'npc.lowleaf_provisioner_lit': [
    { speaker: 'PROVISIONER', text: "Spore-bread's back! I've baked till the oven sulked." },
    { speaker: 'PROVISIONER', text: "Spore Puff, Root Strike, Lifedrain charts. Festival prices — which are regular prices." },
  ],
  'npc.bower_guest_lit': [
    { speaker: 'BLOOM GUEST', text: "Two lit stars on my walk from Pearlmoor. I might stay till next Bloom." },
  ],
  // --- Cinderhead Mine (gleam:stone) ----------------------------------------
  'npc.vigil_elder_lit': [
    { speaker: 'VIGIL ELDER', text: "Lamps down, lamps lit again. This year the second half felt like the point." },
    { speaker: 'VIGIL ELDER', text: "The old crew's lamp still burns. A mine remembers who carried its light." },
  ],
  'npc.vigil_miner_a_lit': [
    { speaker: 'MINER', text: "The cowled folk came back. No talk. They stood at the shaft-head and looked." },
    { speaker: 'MINER', text: "One asked to stay for the Lamp-down. We said yes. The dark's welcome to watch." },
  ],
  'npc.vigil_miner_b_lit': [
    { speaker: 'MINER', text: "Otho's told your bout all night, in about five words. For Otho, a saga." },
  ],
  'npc.cinderhead_provisioner_lit': [
    { speaker: 'PIT-PROVISIONER', text: "Last crate of wicks, and never sold gladder. Balms, charges, charts." },
  ],
  'npc.cinderhead_deep_warden_lit': [
    { speaker: 'DEEP-WARDEN', text: "Wren came up the shaft while you were with Otho. Stood under the Stone a long while, then walked on north. Lighter, I thought. Not light. Lighter." },
  ],
};

export const EAST_SCRIPTS: ScriptRegistry = {
  ...EAST_AFTER_SCRIPTS,
  // Georgina's intro never set q_east_georgina_met, which the lost kitten and her
  // waiting placement both require — the side quest could not be finished.
  'script.georgina_meet': [
    { op: 'run', ref: 'script.georgina_intro' },
    { op: 'setFlag', flag: 'flag:q_east_georgina_met' },
  ],
  // --- Saltreach Fen I: the fishing-stilt nook (world-craft §4 #1b) ----------
  // The reed-cutter's widow by the stilt hut. One fen story (the drowned
  // village) that points at the Staithe line, and the net-weights hook.
  'script.fen_eelwife': [
    { op: 'emote', actor: 'fen_eelwife', emote: 'music' },
    { op: 'face', actor: 'fen_eelwife', facing: 'right' },
    { op: 'say', speaker: 'EEL-WIFE', text: "Mind the punt, it bites. ...No, it doesn't. My man cut reed here forty winters. Now I do, and the eels pay the rent." },
    { op: 'say', speaker: 'EEL-WIFE', text: 'A village stood on the lagoon once: Lantern Staithe. The fen took it a house a year, so slowly nobody thought to leave.' },
    { op: 'say', speaker: 'EEL-WIFE', text: 'Every dusk they walked reed-lamps out along the old road so the boats found home. The posts are going under, one by one.' },
    { op: 'say', unless_flag: 'flag:fen_lostreed_3', speaker: 'EEL-WIFE', text: 'Their last [[three lantern-reeds]] stand dark by the drowned cottage. [[Light them from the landing outward]] and you might read its door.' },
    { op: 'say', if_flag: 'flag:fen_lostreed_3', speaker: 'EEL-WIFE', text: 'You lit the Staithe line. Sixty years, and I never saw all three burn.' },
    { op: 'say', unless_flag: 'flag:fen_netweights_seen', speaker: 'EEL-WIFE', text: "Idling? [[Count my net-weights]]. Lead goes missing. So do eels." },
  ],
  'script.fen_netweights': [
    { op: 'narrate', if_flag: 'flag:fen_netweights_seen', text: 'Nineteen lead weights in a row. You make it nineteen. She will say twenty.' },
    { op: 'narrate', unless_flag: 'flag:fen_netweights_seen', text: 'Net-weights in a neat row — and under the rack, one board sits proud.' },
    { op: 'emote', unless_flag: 'flag:fen_netweights_seen', actor: 'player', emote: 'alert' },
    { op: 'narrate', unless_flag: 'flag:fen_netweights_seen', text: 'Something is tucked beneath it, out of the wet.' },
    { op: 'setFlag', flag: 'flag:fen_netweights_seen' },
  ],
  'script.pickup_fen_netweights': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: "Under the board: a waxed tin and a note. 'IF YOU COUNTED, KEEP IT.' Found a WARM BALM!" },
    { op: 'setFlag', flag: 'flag:picked_fen_netweights' },
  ],

  // --- Saltreach Fen I: the Lantern Staithe line (world-craft §4 #1c) --------
  // Three dark lantern-reeds, lit from home outward (the fen's own rule — the
  // fisher in Fen II says it too). Every one TAKES; the contrast with Fen II's
  // third reed, which won't, is the point.
  'script.fen_lostreed_1': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffb86b', alpha: 0.18, ms: 400 },
    { op: 'setFlag', flag: 'flag:fen_lostreed_1' },
    { op: 'narrate', text: 'The reed takes your flame: a small amber globe where the old road goes under.' },
    { op: 'tint', color: '#ffb86b', alpha: 0, ms: 600 },
  ],
  'script.fen_lostreed_2': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffb86b', alpha: 0.18, ms: 400 },
    { op: 'setFlag', flag: 'flag:fen_lostreed_2' },
    { op: 'narrate', text: 'The second answers the first. Two lights, walking out from the landing.' },
    { op: 'tint', color: '#ffb86b', alpha: 0, ms: 600 },
  ],
  'script.fen_lostreed_3': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffb86b', alpha: 0.24, ms: 500 },
    { op: 'setFlag', flag: 'flag:fen_lostreed_3' },
    { op: 'wait', ms: 500 },
    { op: 'narrate', text: 'The third, at the drowned cottage step. Three lamps in a line, and for a moment the water remembers it was a road.' },
    { op: 'tint', color: '#ffb86b', alpha: 0, ms: 800 },
  ],
  'script.fen_lost_village': [
    { op: 'narrate', unless_flag: 'flag:fen_lostreed_3', text: 'A drowned cottage in the reeds. Carving over the door, too dark to read.' },
    { op: 'narrate', if_flag: 'flag:fen_lostreed_3', text: 'By the light of the three reeds you can read the carving over the door: LANTERN STAITHE — WE KEEP THE ROAD LIT.' },
    { op: 'wait', if_flag: 'flag:fen_lostreed_3', ms: 600 },
    { op: 'narrate', if_flag: 'flag:fen_lostreed_3', text: "Under it, scratched later and smaller: 'Gone to Pearlmoor. Back for the lamps in spring.'" },
  ],

  // --- Glowmoss Deep: E-1, the acolyte's dropped cinder ------------------------
  // Seen after the relight (object requires met_hollowing); silent before it.
  // At dawn it has woken into a shard (the world's cinders do, 08-peril).
  'script.glowmoss_cinder': [
    { op: 'narrate', if_flag: 'flag:met_hollowing', unless_flag: 'flag:dawn', text: "A star-cinder, like the one in Wendel's orchard — cold, faintly blue in its cracks." },
    { op: 'narrate', if_flag: 'flag:met_hollowing', unless_flag: 'flag:dawn', text: 'The Hollowing were carrying it carefully — the way you carry something you mean to bury.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'The acolyte\'s cinder has woken in the dawn: a shard of warm, pale light, humming against the moss.' },
  ],

  // --- Glowmoss Deep: E-2, Wren A3 with a reason (promotes npc.wren_glowmoss) -
  // Pays off the South seed ("Mum's village is past Pearlmoor, and her letters
  // have gone very short"). Acted: she looks back at the grey chamber first.
  'script.wren_glowmoss': [
    { op: 'face', actor: 'wren_glowmoss', facing: 'up' },
    { op: 'wait', ms: 500 },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'You woke it up. Good. I think.' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: 'They did not fight us. They apologised. Who apologises while they... while they do that?' },
    { op: 'wait', ms: 700 },
    { op: 'emote', actor: 'wren_glowmoss', emote: 'ellipsis' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: "...What if they're not wrong? Mum's village went quiet in the spring. She writes it's peaceful. She used to write PAGES." },
    { op: 'face', actor: 'wren_glowmoss', facing: 'left' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'soft', text: 'Forget it. Race you to the mine. ...I am not racing. Walk with me a bit?' },
  ],

  // --- Glowmoss B1F: an acolyte sits with a doused null-lantern ---------------
  'script.b1f_acolyte': [
    { op: 'emote', actor: 'b1f_acolyte', emote: 'ellipsis' },
    { op: 'wait', ms: 500 },
    { op: 'face', actor: 'b1f_acolyte', facing: 'down' },
    { op: 'say', speaker: 'ACOLYTE', text: "Oh. You lit the Fennlight's lantern. ...I'm not cross. I came to sit with this one." },
    { op: 'say', speaker: 'ACOLYTE', text: "It holds a little dark, the way yours holds a little light. I don't think either of us is wrong, exactly. I think one of us is tired." },
    { op: 'face', actor: 'b1f_acolyte', facing: 'up' },
    { op: 'narrate', text: 'She does not light it. She does not leave it.' },
    { op: 'say', if_flag: 'gleam:verdant', speaker: 'ACOLYTE', text: 'The Verdant came back. I felt it through the roots. ...It was very beautiful. I wish that made this easier.' },
  ],

  // --- Cinderhead: E-3, the roof-fault cinder ---------------------------------
  'script.cinderhead_fault_cinder': [
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'A fist-sized cinder under a split in the roof. Nobody has swept it up.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'The roof-fault cinder is a shard now, ringed with pit-lamps for company.' },
    // A fall for the pass-walker's map (West W-4): counts once, now or when it opens.
    { op: 'run', unless_flag: 'flag:fall_seen_cinderhead', ref: 'script.passmap_tick' },
    { op: 'setFlag', flag: 'flag:fall_seen_cinderhead' },
  ],
  'script.cinderhead_fault_miner': [
    { op: 'face', actor: 'fault_miner', facing: 'up' },
    { op: 'wait', ms: 600 },
    { op: 'say', speaker: 'MINER', text: "Came through that fault the bad year. Lit the gallery blue, then went cold." },
    { op: 'face', actor: 'fault_miner', facing: 'left' },
    { op: 'say', speaker: 'MINER', text: "We don't move it. Seemed rude." },
    { op: 'say', if_flag: 'gleam:stone', speaker: 'MINER', text: 'The Stone came back through that same crack, you know. Like it knew the way.' },
  ],

  // --- Cinderhead Deep B2F: Cass, who comes down to listen to the vigil-lamp ---
  'script.b2f_miner': [
    { op: 'emote', actor: 'b2f_miner', emote: 'music', unless_flag: 'flag:q_east_vigil_lamp' },
    { op: 'say', unless_flag: 'flag:q_east_vigil_lamp', speaker: 'CASS', text: "Shh. Hear the vigil-lamp ticking? I come down to check it's still going." },
    { op: 'say', unless_flag: 'flag:q_east_vigil_lamp', speaker: 'CASS', text: "Could lift it myself. Won't. Otho wants it [[carried up]] by someone who chose to come down for it." },
    { op: 'say', if_flag: 'flag:q_east_vigil_lamp', speaker: 'CASS', text: "Go on, then, slow on the ladders. I count the lamps — I always get home." },
    { op: 'wait', ms: 500 },
    { op: 'face', actor: 'b2f_miner', facing: 'up' },
    { op: 'say', speaker: 'CASS', text: 'This was the Grist-Gallery seam. Eight in that crew. Harl carried all eight lamps home the bad year.' },
    { op: 'say', speaker: 'CASS', text: "Then he took one up the mountain, and a hook's hung empty since. We dim for the crew at the Lamp-down. We don't say his name." },
  ],
};

export const EAST_DIALOGUE: DialogueRegistry = {
  ...EAST_AFTER_DIALOGUE,
  'npc.fen_lostreed_wait': [
    { text: 'A dark lantern-reed, leaning toward the landing as if waiting.', style: 'narrate' },
  ],
  // E-3: Harl's eight hooks (Cinderhead's west terrace)
  'sign.cinderhead_hooks': [
    { text: 'Eight brass hooks. Seven pit-lamps, lit low. The eighth hook is empty.', style: 'narrate' },
    { text: 'THE GRIST-GALLERY CREW\nWe dim for them at the Lamp-down. Harl keeps his own vigil, elsewhere.' },
  ],
};
