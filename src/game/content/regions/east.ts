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
    { op: 'say', speaker: 'BOWER-KEEPER', text: "Every bunk's spoken for and three walkers are asleep in the hall, but there's always a bower for whoever woke the Elder Bed. In you go." },
    { op: 'heal' },
    { op: 'say', speaker: 'BOWER-KEEPER', text: "There. Kin bright-eyed, boots dry. The moss in the eaves glowed all night, first time since the cold spring. Not one guest complained about the light." },
  ],
  'script.shop_cinderhead_staged': [
    { op: 'dialogue', ref: 'npc.cinderhead_provisioner', unless_flag: STONE },
    { op: 'dialogue', ref: 'npc.cinderhead_provisioner_lit', if_flag: STONE },
    { op: 'shop', shop: 'cinderhead_provisioner' },
  ],
  'script.cinderhead_rest_lit': [
    { op: 'say', speaker: 'VIGIL COOK', text: "Sit by the vigil-fire, Wayfarer. We've let it burn high tonight, and nobody here can remember the last time we did. Warm your kin and your hands both." },
    { op: 'heal' },
    { op: 'say', speaker: 'VIGIL COOK', text: "There. Rested and ready. The dark's still long. Tonight, for once, the fire's ahead." },
  ],
};

const EAST_AFTER_DIALOGUE: DialogueRegistry = {
  // --- Lowleaf Hollow (gleam:verdant) ---------------------------------------
  'npc.bloom_piper_lit': [
    { speaker: 'BLOOM PIPER', text: "The ring's turning round a GREEN bed this year. I've played the crowning reel four times over and they won't let me stop. My fingers have gone to moss." },
  ],
  'npc.bloom_fencer_lit': [
    { speaker: 'FESTIVAL AUNTIE', text: "Well. The Elder Bed's gone green as a frog and the whole hollow is looking at me. Beds have bad years, I said. I never said they couldn't have good ones." },
    { speaker: 'FESTIVAL AUNTIE', text: "Have a moss-cake. I'm told I owe the town one apiece, and you're first in the queue." },
  ],
  'npc.bloom_kid_a_lit': [
    { speaker: 'MOSS KID', text: "My glow-mote wish came true! Not the Fennlight one. The other one. I wished the big bed would wake up." },
    { speaker: 'MOSS KID', text: "Don't tell the moss I wished twice. It might want one of them back." },
  ],
  'npc.bloom_kid_b_lit': [
    { speaker: 'FERN KID', text: "You walked into the deep wood like it was our back garden. I watched the WHOLE time. Mum says I can't copy you till I've got a lamp of my own." },
  ],
  'npc.lowleaf_provisioner_lit': [
    { speaker: 'PROVISIONER', text: "Spore-bread's back on the shelf! The deep wood's sending spores again now the bed's awake. I've baked until the oven sulked." },
    { speaker: 'PROVISIONER', text: "And the counter's open, Verdant slate and all: Spore Puff, Root Strike, Lifedrain. Festival prices. Which are still regular prices." },
  ],
  'npc.bower_guest_lit': [
    { speaker: 'BLOOM GUEST', text: "Twice a year I walk in from Pearlmoor, and this time I walked under two lit stars: the Tide at my back and the Verdant ahead. I've half a mind to stay till the next Bloom and spare my boots." },
  ],
  // --- Cinderhead Mine (gleam:stone) ----------------------------------------
  'npc.vigil_elder_lit': [
    { speaker: 'VIGIL ELDER', text: "We lowered the lamps and lit them again, same as ever. Only this year the second half felt like the point." },
    { speaker: 'VIGIL ELDER', text: "The old crew's lamp stands at the shaft-head, still burning. Go up gentle, Wayfarer. A mine remembers who carried its light." },
  ],
  'npc.vigil_miner_a_lit': [
    { speaker: 'MINER', text: "The cowled folk came back down the road after the Stone stood up. No talk this time. They stood at the shaft-head and looked at it." },
    { speaker: 'MINER', text: "One asked could he stay for the next Lamp-down. We said yes. A miner keeps a light in the dark, and the dark is welcome to watch." },
  ],
  'npc.vigil_miner_b_lit': [
    { speaker: 'MINER', text: "You out-lasted him. Otho's been telling the bout at the vigil-fire all night, in about five words. For Otho, that's a saga." },
  ],
  'npc.cinderhead_provisioner_lit': [
    { speaker: 'PIT-PROVISIONER', text: "Every crew's re-trimming at once since the Stone came back. I'm down to my last crate of wicks and I've never sold any gladder. Balms, charges, a chart or two for the deep." },
  ],
  'npc.cinderhead_deep_warden_lit': [
    { speaker: 'DEEP-WARDEN', text: "Your friend Wren came back up the shaft while you were with Otho. Stood under the Stone a long while, then walked on north without a word. Lighter, I thought. Not light. Lighter." },
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
    { op: 'say', speaker: 'EEL-WIFE', text: "Mind the punt, it bites. ...No, it doesn't. My man cut reed on this water forty winters. I cut it now, and the eels pay the rent." },
    { op: 'say', speaker: 'EEL-WIFE', text: 'There was a village out on the lagoon once. Lantern Staithe. The fen took it a house a year, so slowly nobody thought to leave.' },
    { op: 'say', speaker: 'EEL-WIFE', text: 'Every dusk they walked the reed-lamps out along the old road, so the boats could find home. The posts are still there, going under one by one.' },
    { op: 'say', unless_flag: 'flag:fen_lostreed_3', speaker: 'EEL-WIFE', text: 'Their last three lantern-reeds stand dark by the drowned cottage. Light them from the landing outward, the way they did, and you might read the name over its door.' },
    { op: 'say', if_flag: 'flag:fen_lostreed_3', speaker: 'EEL-WIFE', text: 'You lit the Staithe line. I watched it from my step. Sixty years on this water, and I never once saw all three burn.' },
    { op: 'say', unless_flag: 'flag:fen_netweights_seen', speaker: 'EEL-WIFE', text: "If you're idling, count my net-weights on the rack. Lead goes missing. So do eels." },
  ],
  'script.fen_netweights': [
    { op: 'narrate', if_flag: 'flag:fen_netweights_seen', text: 'Nineteen lead weights in a row. You make it nineteen. She will say twenty.' },
    { op: 'narrate', unless_flag: 'flag:fen_netweights_seen', text: 'Lead net-weights hang from the rack in a neat row — and under it one board of the staging sits proud of the rest.' },
    { op: 'emote', unless_flag: 'flag:fen_netweights_seen', actor: 'player', emote: 'alert' },
    { op: 'narrate', unless_flag: 'flag:fen_netweights_seen', text: 'Something has been tucked beneath it, out of the wet.' },
    { op: 'setFlag', flag: 'flag:fen_netweights_seen' },
  ],
  'script.pickup_fen_netweights': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'warm_balm', count: 1 },
    { op: 'say', text: "Under the loose board: a waxed tin and a note in a firm hand. 'IF YOU COUNTED, KEEP IT.' Found a WARM BALM!" },
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
    { op: 'narrate', text: 'The lantern-reed takes your flame and keeps it — a small amber globe over the black water, where the old road goes under.' },
    { op: 'tint', color: '#ffb86b', alpha: 0, ms: 600 },
  ],
  'script.fen_lostreed_2': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'action', actor: 'player', action: 'raiseLamp' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'tint', color: '#ffb86b', alpha: 0.18, ms: 400 },
    { op: 'setFlag', flag: 'flag:fen_lostreed_2' },
    { op: 'narrate', text: 'The second answers the first across the reeds. Two lights now, walking out from the landing the way they used to.' },
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
    { op: 'narrate', unless_flag: 'flag:fen_lostreed_3', text: 'A drowned cottage: two gables and a chimney standing out of the reeds. There is carving over the door, but it is too dark to read.' },
    { op: 'narrate', if_flag: 'flag:fen_lostreed_3', text: 'By the light of the three reeds you can read the carving over the door: LANTERN STAITHE — WE KEEP THE ROAD LIT.' },
    { op: 'wait', if_flag: 'flag:fen_lostreed_3', ms: 600 },
    { op: 'narrate', if_flag: 'flag:fen_lostreed_3', text: "Under it, scratched later and smaller: 'Gone to Pearlmoor. Back for the lamps in spring.'" },
  ],

  // --- Glowmoss Deep: E-1, the acolyte's dropped cinder ------------------------
  // Seen after the relight (object requires met_hollowing); silent before it.
  // At dawn it has woken into a shard (the world's cinders do, 08-peril).
  'script.glowmoss_cinder': [
    { op: 'narrate', if_flag: 'flag:met_hollowing', unless_flag: 'flag:dawn', text: "A star-cinder, like the one in Wendel's orchard — cold, faintly blue in its cracks." },
    { op: 'narrate', if_flag: 'flag:met_hollowing', unless_flag: 'flag:dawn', text: 'The Hollowing were carrying it somewhere. Carefully — the way you carry something you mean to bury.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'The cinder the acolyte dropped has woken in the dawn: a shard of warm, pale light, humming against the moss.' },
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
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'unsure', text: "...What if they're not wrong? Mum's village went quiet in the spring. She writes that nobody's hurt. She writes that it's peaceful. She used to write PAGES." },
    { op: 'face', actor: 'wren_glowmoss', facing: 'left' },
    { op: 'say', speaker: 'WREN', portrait: 'wren', expr: 'soft', text: 'Forget it. Race you to the mine. ...I am not racing. Walk with me a bit?' },
  ],

  // --- Glowmoss B1F: an acolyte sits with a doused null-lantern ---------------
  'script.b1f_acolyte': [
    { op: 'emote', actor: 'b1f_acolyte', emote: 'ellipsis' },
    { op: 'wait', ms: 500 },
    { op: 'face', actor: 'b1f_acolyte', facing: 'down' },
    { op: 'say', speaker: 'ACOLYTE', text: "Oh. You're the one who lit the Fennlight's lantern upstairs. ...No, I'm not cross. I came down to sit with this one instead." },
    { op: 'say', speaker: 'ACOLYTE', text: "It holds a little dark, the way yours holds a little light. I don't think either of us is wrong, exactly. I think one of us is tired." },
    { op: 'face', actor: 'b1f_acolyte', facing: 'up' },
    { op: 'narrate', text: 'She does not light it. She does not leave it.' },
    { op: 'say', if_flag: 'gleam:verdant', speaker: 'ACOLYTE', text: 'The Verdant came back. I felt it through the roots. ...It was very beautiful. I wish that made this easier.' },
  ],

  // --- Cinderhead: E-3, the roof-fault cinder ---------------------------------
  'script.cinderhead_fault_cinder': [
    { op: 'narrate', unless_flag: 'flag:dawn', text: 'A cinder the size of a fist, sunk in the cavern floor under a split in the roof. Nobody has swept around it. Nobody has swept it up, either.' },
    { op: 'narrate', if_flag: 'flag:dawn', text: 'The roof-fault cinder has woken into a shard. The miners have set a ring of pit-lamps round it, as if it might want the company.' },
    // A fall for the pass-walker's map (West W-4): counts once, now or when it opens.
    { op: 'run', unless_flag: 'flag:fall_seen_cinderhead', ref: 'script.passmap_tick' },
    { op: 'setFlag', flag: 'flag:fall_seen_cinderhead' },
  ],
  'script.cinderhead_fault_miner': [
    { op: 'face', actor: 'fault_miner', facing: 'up' },
    { op: 'wait', ms: 600 },
    { op: 'say', speaker: 'MINER', text: "Came down through that fault the winter the bad year started. Lit the whole gallery blue for a breath, then went cold." },
    { op: 'face', actor: 'fault_miner', facing: 'left' },
    { op: 'say', speaker: 'MINER', text: "We don't move it. Seemed rude." },
    { op: 'say', if_flag: 'gleam:stone', speaker: 'MINER', text: 'The Stone came back through that same crack, you know. Like it knew the way.' },
  ],

  // --- Cinderhead Deep B2F: Cass, who comes down to listen to the vigil-lamp ---
  'script.b2f_miner': [
    { op: 'emote', actor: 'b2f_miner', emote: 'music', unless_flag: 'flag:q_east_vigil_lamp' },
    { op: 'say', unless_flag: 'flag:q_east_vigil_lamp', speaker: 'CASS', text: "Shh — listen. You can hear it ticking in its cage, the vigil-lamp. I come down some shifts just to hear it's still going." },
    { op: 'say', unless_flag: 'flag:q_east_vigil_lamp', speaker: 'CASS', text: "Could lift it myself. Won't. Otho wants it carried up by someone who chose to come down for it." },
    { op: 'say', if_flag: 'flag:q_east_vigil_lamp', speaker: 'CASS', text: "Go on, then, slow on the ladders. I'll find my own way up. I count the lamps — I always get home." },
    { op: 'wait', ms: 500 },
    { op: 'face', actor: 'b2f_miner', facing: 'up' },
    { op: 'say', speaker: 'CASS', text: 'This was the Grist-Gallery seam. Eight in that crew. Harl carried all eight lamps home the bad year.' },
    { op: 'say', speaker: 'CASS', text: "Then he took one of them up the mountain, and a hook's hung empty since. We still dim for the crew at the Lamp-down. We don't say his name." },
  ],
};

export const EAST_DIALOGUE: DialogueRegistry = {
  ...EAST_AFTER_DIALOGUE,
  'npc.fen_lostreed_wait': [
    { text: 'A dark lantern-reed. It leans toward the landing, as if waiting for the one before it.', style: 'narrate' },
  ],
  // E-3: Harl's eight hooks (Cinderhead's west terrace)
  'sign.cinderhead_hooks': [
    { text: 'Eight brass hooks on one rail. Seven small pit-lamps hang there, lit low. The eighth hook is empty.', style: 'narrate' },
    { text: 'THE GRIST-GALLERY CREW\nWe dim for them at the Lamp-down. Harl keeps his own vigil, elsewhere.' },
  ],
};
