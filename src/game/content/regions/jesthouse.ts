/**
 * THE OLD LIGHT, R10 (2026-10) — the jest-house's new cast and gags.
 *
 * Playtest: "I went in the tower's ground floor. Nobody there, seemed empty and
 * not a funny place." R10 rebuilt the floors big (build_pearlmoor_oldlight.py:
 * the haunted-tower walk, a warped tileset and a more unhinged Punchwheel cue per
 * floor) and filled them with the house's REGULARS and PROPS, all written here:
 *
 *  F1 Lobby     the GROANER, the MIME, the USHER (optional sight trainer), the
 *               whoopee cushion, the laugh track, the jack-in-the-box, the
 *               applause sign, the rubber chickens, the laugh meter, the coats
 *  F2 Late      the JUGGLER (optional), the unicycle, the clown shoes, a late
 *               laugh track, the late masks
 *  F3 Interval  the PIE-THROWER (optional), the teacup tower, the custard pies,
 *               the spare cogs
 *  F4 Backwards THE MIRROR (optional), the backwards clock, the upside chair,
 *               the funhouse mirrors
 *  F5 Gallery   THE CRITIC (optional), the Big Book of Facts, the mallet, the
 *               banana peel
 *  F6 One Joke  the two cups become a REST (sit across from the empty chair),
 *               the old confetti, the one spring-snake
 *  Every floor  MOLL, Tam's old stage partner (non-fighting): one floor ahead,
 *               cheering you on and telling Tam's story a piece at a time
 *  Point        PIP, the netmender's grandson, runs after you on the way out if
 *               you've the floats but not the rope (so the breakwater — and what
 *               waits at its end — is never missed)
 *
 * Every joke is Mr. Punchwheel's (the tower's rule: the plaque says so) or a
 * regular reading his cards; the optional trainers are pitched 10 -> 14 so the
 * climb is the grind bed before Reyl (16) and the fen beyond. Pure colour except
 * the trainers' own beaten flags, the two once-flags and the rest point.
 */
import type { CutsceneStep, DialogueLine, DialogueRegistry, ScriptRegistry } from '../types';

const PW = 'PUNCHWHEEL';
const pw = (text: string): CutsceneStep => ({ op: 'say', speaker: PW, text });
const nar = (text: string): CutsceneStep => ({ op: 'narrate', text });
const say = (speaker: string, text: string): CutsceneStep => ({ op: 'say', speaker, text });
const line = (speaker: string, text: string): DialogueLine => ({ speaker, text });
const sign = (text: string): DialogueLine => ({ text });

/** An optional alcove regular: their lines, the bout, the beaten flag. */
function bout(tid: string, speaker: string, before: string[], after: string[]): CutsceneStep[] {
  return [
    ...before.map((t) => say(speaker, t)),
    { op: 'battle', trainer: `oldlight_${tid}` },
    ...after.map((t) => say(speaker, t)),
    { op: 'setFlag', flag: `flag:oldlight_${tid}_beaten` },
  ];
}

export const JESTHOUSE_SCRIPTS: ScriptRegistry = {
  // ---- F1: the Lobby of Groaners ------------------------------------------------------
  'script.oldlight_whoopee': [
    { op: 'sfx', key: 'battle-not-effective' },
    nar('Something soft underfoot lets out a long, mournful note, like a tuba hearing bad news.'),
    pw('(from every speaking-tube) WHO DID THAT. ...Oh. The cushion. It is always the cushion.'),
    { op: 'setFlag', flag: 'flag:oldlight_whoopee_sat' },
  ],
  'script.oldlight_mime': [
    nar('The MIME presses her palms to an invisible wall, points upstairs, and mimes climbing: a cup of tea halfway, then trapped in a box.'),
    nar('You mime opening the lid. She stares as if you have ruined her entire act.'),
  ],
  'script.oldlight_laugh_meter': [
    nar('A brass gauge: QUIET — CHUCKLE — GUFFAW — UPROAR. The needle is jammed on UPROAR.'),
    pw('Calibrated it myself! UPROAR every minute for eleven winters. Morale has never been higher.'),
  ],
  'script.oldlight_laugh_track': [
    nar('Three clockwork dolls on a bench, mouths open. A button: PRESS IF SHY.'),
    { op: 'sfx', key: 'ui-confirm' },
    nar('HA. HA. HA. — perfectly in time. Then they turn to each other, as if to ask who started it.'),
    pw('The laugh track! For when the audience is shy. Or absent. Usually both.'),
  ],
  'script.oldlight_jack_box': [
    nar('A jack-in-the-box, already sprung, its clown quite out of breath.'),
    pw('He waited eleven winters for someone to turn the handle. A draught did it. He hasn\'t spoken to it since.'),
  ],
  'script.oldlight_usher': bout('usher', 'USHER', [
    'TICKETS, please! ...No ticket? Then you pay the old price: one bout.',
  ], [
    '(He stamps your hand: ADMIT ONE. Underneath, smaller: BRAVE.)',
  ]),

  // ---- F2: the Late Laugh ----------------------------------------------------------------
  'script.oldlight_laugh_track_late': [
    nar('Another bench of clockwork dolls. You press the button. Nothing. You turn to go.'),
    { op: 'wait', ms: 900 },
    nar('...HA. HA. HA.'),
  ],
  'script.oldlight_juggler': bout('juggler', 'JUGGLER', [
    'Three cheese-buns, one hand! ...Two cheese-buns. ...One cheese-bun and a bit of floor.',
    'Battle me while I pick these up!',
  ], [
    'I can do four now. Well. I can DROP four.',
  ]),

  // ---- F3: Intermission --------------------------------------------------------------------
  'script.oldlight_pie_thrower': bout('pie_thrower', 'PIE-THROWER', [
    'Interval special! One custard pie, at speed, to the face of your choice!',
    '...No? Then I\'ll throw my kin at you. Less custard. More feelings.',
  ], [
    'You\'ve earned a pie. Not to eat. Nobody eats them. They\'re for COMEDY.',
  ]),

  // ---- F4: the Backwards Inn -------------------------------------------------------------------
  'script.oldlight_mirror': bout('mirror', 'THE MIRROR', [
    'Nice coat. Same as mine. You\'re reaching for your lamp. So am I.',
    'You blinked. I blinked. ...Fine. I blinked first. BATTLE!',
  ], [
    '(He copies your bow, starts copying you walking away, and thinks better of it.)',
  ]),

  // ---- F5: the Gallery of Confident Facts ---------------------------------------------------
  'script.oldlight_lectern': [
    nar('On a lectern: THE BIG BOOK OF FACTS, by MR. PUNCHWHEEL.'),
    pw('FACT: the sea is salty because the fish have been crying ever since they heard about rain.'),
    pw('FACT: this book is one hundred per cent accurate. (CORRECTIONS ON PAGE FOUR.) (PAGE FOUR IS MISSING.)'),
  ],
  'script.oldlight_banana': [
    { op: 'sfx', key: 'world-bump' },
    nar('A banana peel. Time slows. Your life flashes past. Most of it was walking.'),
    nar('You nearly fall, catch yourself, and look round to see if anyone saw.'),
    pw('(from every speaking-tube at once) I SAW.'),
    { op: 'setFlag', flag: 'flag:oldlight_banana_slipped' },
  ],
  'script.oldlight_critic': bout('critic', 'THE CRITIC', [
    'Two stars, just for turning up. Battle me and I\'ll decide whether to take one back.',
  ], [
    'Four stars. It would have been five, but your kin didn\'t do an encore.',
  ]),

  // ---- F6: the One Joke — the two cups (the floor's rest) ------------------------------------
  // ---- TOP: the headline act (the toll before the card — not the climax) ------------
  // Punchwheel guards Tam's card: eleven winters of "no laughter detected" and he can't
  // bear to hear it again. His three clowns stand in the only gap to the drum. Win and
  // they step aside; the music falls away; the card (script.oldlight_top) is the crescendo.
  'script.oldlight_headliners': [
    { op: 'emote', actor: 'act_jester', emote: 'alert' },
    pw('Ah-ah-AH. Not one step nearer. That is her card in the drum.'),
    pw('Eleven winters of "no laughter detected". I am not hearing it again.'),
    pw('Want the card? Sit through the act first. Ladies and lamp-tenders: MY HEADLINERS!'),
    nar('The Smiler beams. McClownface honks a brass horn. JesterHalf bows, about half sincerely.'),
    { op: 'battle', trainer: 'oldlight_headliners' },
    nar('The act takes three bows, none at the same time, and shuffles aside.'),
    { op: 'musicFade', ms: 1800 },
    pw('...Hm. You laughed. Twice. I counted.'),
    pw('Go on, then. The card is in the drum. She would have liked you.'),
    { op: 'setFlag', flag: 'flag:oldlight_headliners_beaten' },
  ],
  // ---- TOP: the green room (a rest point before the headline act) ----------------------
  'script.oldlight_greenroom': [
    nar('A battered green-room armchair: PERFORMERS ONLY, with PERFORMERS crossed out and ANYONE TIRED written in.'),
    {
      op: 'choice',
      prompt: 'Sit a while?',
      options: [
        {
          label: 'Sit down.',
          ops: [
            nar('You sink into it. Below, the whole tower ticks and laughs to itself.'),
            { op: 'heal', sleep: false },
            pw('(from the drum) Nerves? Everybody gets them. I get them, and I am mostly springs.'),
          ],
        },
        { label: 'Not now.', ops: [] },
      ],
    },
  ],
  // F4's rest, beside the Ringmaster (playtest: the bout came a long walk after F3's urn).
  'script.oldlight_urn_backwards': [
    { op: 'say', speaker: 'TEA-URN', text: 'NUB A YUB! ...SETUNIM YTNEWT! LAVRETNI!' },
    nar('(The tea-urn from downstairs, only backwards. The tea goes in before you are thirsty.)'),
    { op: 'heal', sleep: false },
    nar('Your kin are mended. The Ringmaster pretends not to see.'),
  ],
  'script.oldlight_cups_rest': [
    nar('Two cups on the table. One washed every day for years. The other never moved.'),
    {
      op: 'choice',
      prompt: 'Sit a while?',
      options: [
        {
          label: 'Sit down.',
          ops: [
            nar('You take the chair that has never been moved: the comfiest in the tower, chosen carefully long ago.'),
            { op: 'heal', sleep: false },
            nar('Your kin are rested. The other cup stays where it has always been.'),
          ],
        },
        { label: 'Leave it be.', ops: [] },
      ],
    },
  ],

  // ---- Lightkeeper's Point: PIP runs after you on the way out --------------------------------
  // Fires once, on the Point's one crossing back to the quay, if you've climbed the
  // tower (the floats are yours) but haven't had the rope yet.
  // ---- ANDREW outside the Old Light, once the act is done (owner's beat, 2026-10) -------
  // He runs up, says his piece about eggs and wonder, laughs and dashes off. Never says
  // WHAT the egg is (CLAUDE.md); {name} is the player's name, whatever they chose.
  'script.andrew_tower_wink': [
    { op: 'emote', actor: 'andrew_tower', emote: 'alert' },
    { op: 'move', actor: 'andrew_tower', to: { tx: 10, ty: 8 }, speed: 2 },
    { op: 'face', actor: 'andrew_tower', facing: 'left' },
    { op: 'face', actor: 'player', facing: 'right' },
    { op: 'say', speaker: 'ANDREW', text: "{name}! There you are. Isn't it funny? All this time you've been chasing that Easter egg..." },
    { op: 'say', speaker: 'ANDREW', text: "...when the whole game's been a little bit of an Easter egg all along, hasn't it? (wink, wink)" },
    { op: 'say', speaker: 'ANDREW', text: "Keep playing, though. You're not AT the Easter egg yet." },
    { op: 'say', speaker: 'ANDREW', text: "Isn't it funny? This game's been a bit of a wonder, hasn't it?" },
    { op: 'say', speaker: 'ANDREW', text: 'And though you might aspire to make ME wonder... it is YOU who is the one wandering through MY world.' },
    { op: 'action', actor: 'andrew_tower', action: 'laugh' },
    { op: 'say', speaker: 'ANDREW', text: 'Ha! Ha ha ha ha!' },
    { op: 'move', actor: 'andrew_tower', to: { tx: 19, ty: 8 }, speed: 2 },
    { op: 'hideActor', actor: 'andrew_tower' },
    { op: 'setFlag', flag: 'flag:andrew_tower_winked' },
  ],
  'script.oldlight_rope_reminder': [
    { op: 'emote', actor: 'pip', emote: 'alert', unless_flag: 'flag:q_south_rope_or_later' },
    { op: 'move', actor: 'pip', to: { tx: 17, ty: 8 }, unless_flag: 'flag:q_south_rope_or_later' },
    { op: 'say', speaker: 'PIP', text: 'WAIT! Wayfarer! Did you get Gran\'s floats back off that machine?', unless_flag: 'flag:q_south_rope_or_later' },
    { op: 'say', speaker: 'PIP', text: 'Take them to [[Gran, by her nets on the quay]]! She\'s got the bell-rope. Then [[walk the breakwater]] out to the bell.', unless_flag: 'flag:q_south_rope_or_later' },
    { op: 'say', speaker: 'PIP', text: 'And go right to the END. Everyone says there\'s somebody out past the bell who... nobody knows what he is! Go and SEE!', unless_flag: 'flag:q_south_rope_or_later' },
    { op: 'setFlag', flag: 'flag:oldlight_rope_reminded' },
  ],
  // ---- MOLL's two floors that notice your wins (the rest are plain dialogue) ----------
  'script.oldlight_moll_2': [
    say('MOLL', "Don't ask how I got here first. Sixty years of knowing the back stairs."),
    { ...say('MOLL', "I heard you see off that heckler. Tam would've hired you on the spot."), if_flag: 'flag:oldlight_heckler_beaten' },
    say('MOLL', "This was our stage. Tam rowed the late ferry, then came on dripping and did twenty minutes."),
    say('MOLL', "They laughed a beat late even then. 'Fog in their ears,' she said. Keep climbing."),
  ],
  'script.oldlight_moll_4': [
    { ...say('MOLL', "The Ringmaster's sulking. Good. He's needed a proper audience for years."), if_flag: 'flag:oldlight_ringmaster_beaten' },
    say('MOLL', "Everything's backwards here. Tam's idea: 'People look their best laughing at themselves, Moll.'"),
    say('MOLL', "She'd pull faces at those mirrors till they gave up first."),
    say('MOLL', "You've a face that keeps going. That's the whole trick of comedy, and of most things."),
  ],
  // ---- F5: the waxed floor (a glare-ice flow across the hall's north lane) ----------------
  'script.oldlight_waxed_floor': [
    nar('The gallery floor is waxed to a mirror shine.'),
    pw('(from a speaking-tube) MIND THE FLOOR! I polished it for the critics. Then I left bananas on it. For the critics.'),
    nar('[[Step onto the shine and you skid]] until something stops you. The dry boards are slower, and less fun.'),
    { op: 'setFlag', flag: 'flag:oldlight_waxed_seen' },
  ],
  // ---- F2: the audience laughs at you, late; F5: the meter has opinions now ----------------
  'script.oldlight_late_laugh': [
    nar('You walk past the audience. Nothing. Another step. Nothing.'),
    { op: 'wait', ms: 700 },
    nar('HA! HA HA HA! — they roar at something you did three steps ago.'),
    pw('(from the wings) They loved your walk. They\'ll say so tomorrow.'),
    { op: 'setFlag', flag: 'flag:oldlight_late_laughed' },
  ],
  'script.oldlight_laugh_meter_f5': [
    nar('A newer meter: DOUBTFUL — PLAUSIBLE — TRUE — CONFIDENT. The needle is bent past CONFIDENT.'),
    pw('It measures how sure I am. It has never gone below CONFIDENT. That is how you know it works.'),
  ],
};

export const JESTHOUSE_DIALOGUE: DialogueRegistry = {
  // ---- F1 ---------------------------------------------------------------------------------
  'sign.oldlight_applause': [
    sign('A lit sign: APPLAUSE. Smaller: (OR A KIND NOD.) Smaller still: (OR JUST STAY. STAYING COUNTS.)'),
  ],
  'sign.oldlight_coats': [
    sign('The cloakroom. Every ticket says BACK IN FIVE MINUTES. The dust has been counting.'),
  ],
  'sign.oldlight_chickens': [
    sign('Rubber chickens on a hat-stand: SQUEEZE IN EMERGENCIES ONLY. (A LONG SILENCE IS AN EMERGENCY.)'),
  ],
  'sign.oldlight_masks': [
    sign('Two masks, laughing and weeping. Someone has drawn a moustache on the weeping one. It looks much happier.'),
  ],
  'sign.oldlight_bench_reserved': [
    sign('A bench: RESERVED FOR LAUGHTER. Eleven winters, and laughter never turned up. Didn\'t even send word.'),
  ],
  'sign.oldlight_spotlight': [
    sign('A spotlight, aimed at the one spot nobody has ever stood. You stand in it. It swings away, embarrassed.'),
  ],
  'sign.oldlight_bunting': [
    sign('Bunting: GRAND OPEN NG. One flag has fallen. Everyone has noticed. Nobody has said anything.'),
  ],
  'npc.oldlight_groaner': [
    line('GROANER', 'Ohhhhh. ...Sorry. Reflex.'),
    line('GROANER', 'I\'m the house groaner. When the machine lands a pun, somebody has to make the noise it deserves.'),
  ],
  'npc.oldlight_usher_after': [
    line('USHER', 'Best seats are upstairs. Worst jokes too. It\'s a package.'),
  ],
  // the battle-screen OPENERS (trainer-intro beat): a fresh punchline once they're on the battle screen
  'trainer.oldlight_heckler.intro': [line("THE HECKLER", "BOO! ...Sorry. Reflex. I heckle everything. Battles especially.")],
  'trainer.oldlight_ringmaster.intro': [line("THE RINGMASTER", "Lamp-tenders and lamp-tenderesses! In THIS corner: me! In THAT corner: also quite good!")],
  'trainer.oldlight_usher.intro': [line("THE USHER", "Your seat faces my kin. Kindly dim all lanterns. ...No? Fine. Bout it is.")],
  'trainer.oldlight_juggler.intro': [line("THE JUGGLER", "Three balls, two hands, one battle. I've done worse sums.")],
  'trainer.oldlight_pie_thrower.intro': [line("THE PIE-THROWER", "Custard first, questions after!")],
  'trainer.oldlight_mirror.intro': [line("THE MIRROR", "Ready when you are. ...Ready when I am. ...Will you STOP copying me?")],
  'trainer.oldlight_critic.intro': [line("THE CRITIC", "Two stars, and you haven't even started. Change my mind.")],
  'trainer.oldlight_usher.defeat': [line('USHER', 'Ticket stamped, guest seated, usher flattened. A full night\'s work.')],

  // ---- F2 ---------------------------------------------------------------------------------
  'sign.oldlight_unicycle': [
    sign('A unicycle: FOR THE ACT. THE ACT IS FALLING OFF A UNICYCLE. Another hand adds: IT\'S A VERY GOOD ACT.'),
  ],
  'sign.oldlight_clown_shoes': [
    sign('Enormous clown shoes. Inside, a smaller pair. Inside those, a note: IT\'S SHOES ALL THE WAY DOWN.'),
  ],
  'sign.oldlight_masks_late': [
    sign('Two masks. The weeping one is wincing at a joke the laughing one hasn\'t heard yet.'),
  ],
  'sign.oldlight_props': [
    sign('A crate stencilled PROPS. A note on the lid: STOP LOOKING AT THE PROPS.'),
  ],
  'sign.oldlight_spotlight_late': [
    sign('This spotlight follows you, a step and a half behind. It\'s the late floor. It\'ll catch up.'),
  ],
  'npc.oldlight_juggler_after': [
    line('JUGGLER', 'Want to see me juggle three kin? ...Neither do they.'),
  ],
  'trainer.oldlight_juggler.defeat': [line('JUGGLER', 'I dropped the battle! I meant to do that. That was the act.')],

  // ---- F3 ---------------------------------------------------------------------------------
  'sign.oldlight_teacups': [
    sign('Teacups stacked eleven high: DO NOT TAKE THE BOTTOM CUP. At the top: WE KNOW YOU\'RE THINKING ABOUT IT.'),
  ],
  'sign.oldlight_pies': [
    sign('Custard pies, one missing, and a pie-shaped mark on the ceiling. Nobody will explain it.'),
  ],
  'sign.oldlight_cogs': [
    sign('Spare cogs labelled SPARE TIMING. The biggest: DO NOT LOSE. THIS ONE IS THE PUNCH.'),
  ],
  'npc.oldlight_pie_thrower_after': [
    line('PIE-THROWER', 'Mind how you go upstairs. No custard up there. Just feelings.'),
  ],
  'trainer.oldlight_pie_thrower.defeat': [line('PIE-THROWER', 'Splat. That one was mine, wasn\'t it.')],

  // ---- F4 ---------------------------------------------------------------------------------
  'sign.oldlight_clock_backwards': [
    sign('A clock with backwards numbers. By its reckoning, you left an hour from now, and were glad you did.'),
  ],
  'sign.oldlight_upside_chair': [
    sign('A chair standing on its head. A note tied to one leg: IT\'S FINE. IT\'S RESTING.'),
  ],
  'sign.oldlight_funhouse': [
    sign('A wobbly mirror: seven feet tall, one inch wide. Your reflection gives a thumbs-up you didn\'t give it.'),
  ],
  // one distortion per glass (build_pearlmoor_oldlight.py floor_4): every mirror bends you its own way
  'sign.oldlight_mirror_squat': [
    sign('A squat mirror: three feet tall, wide as a door. You\'d make an excellent wardrobe.'),
  ],
  'sign.oldlight_mirror_upside': [
    sign('In this one you stand on your head, and look at yourself as though YOU are doing it wrong.'),
  ],
  'sign.oldlight_mirror_bighead': [
    sign('Your head fills the glass like a harvest pumpkin. Far below, two tiny legs look worried.'),
  ],
  'sign.oldlight_mirror_wavy': [
    sign('This glass ripples. Your reflection flaps like washing on a line, and looks seasick.'),
  ],
  'sign.oldlight_mirror_late': [
    sign('A plain mirror. You wave. ...A moment later, so does your reflection. It goes red and pretends to swat a fly.'),
  ],
  'npc.oldlight_mirror_after': [
    line('THE MIRROR', 'Same time next week? ...I already said yes. You just hadn\'t asked yet.'),
  ],
  'trainer.oldlight_mirror.defeat': [line('THE MIRROR', 'You win. Which means I also— no. No, it doesn\'t work like that.')],

  // ---- F5 ---------------------------------------------------------------------------------
  'sign.oldlight_mallet': [
    sign('A giant mallet: FOR EMERGENCY PUNCHLINES. Lower down: NOT FOR THE AUDIENCE.'),
  ],
  'npc.oldlight_critic_after': [
    line('THE CRITIC', 'The tower? Three stars. Jokes too long, stairs too many. I come every night.'),
  ],
  'trainer.oldlight_critic.defeat': [line('THE CRITIC', 'Five stars. Don\'t let it go to your head. I give the stairs five stars too.')],

  // ---- F6 ---------------------------------------------------------------------------------
  // ---- F3/F4/F5/TOP: the extra props (2026-10, more jokes) -----------------------------------
  'sign.oldlight_bar_stool': [
    sign('A bar stool. It spins you round once, slowly, and stops with you facing the wall. It thinks it\'s a bit.'),
  ],
  'sign.oldlight_brazier': [
    sign('A brazier, burning merrily, giving no heat. Its tag: FOR DRAMATIC EFFECT ONLY.'),
  ],
  'sign.oldlight_viewing_bench': [
    sign('A VIEWING BENCH. You view the gallery. It views you back. Somewhere, the Critic writes: two stars.'),
  ],
  'sign.oldlight_plant': [
    sign('A potted plant: FACT: THIS IS A TREE. It isn\'t. It knows. It\'s doing its best.'),
  ],
  'sign.oldlight_jars': [
    sign('Oil jars: FUNNY, FUNNIER and NOT FOR LAMPS. The last is empty. The lamps here are giggling.'),
  ],

  'sign.oldlight_old_confetti': [
    sign('Old confetti swept into a corner, kept for a celebration that hasn\'t come yet.'),
  ],
  'sign.oldlight_spring_can': [
    sign('A can of spring-snakes. Only one jumped. The rest are waiting for a better audience.'),
  ],

  // ---- MOLL: Tam's old stage partner, always one floor ahead (build_pearlmoor_oldlight.py
  // MOLL). Non-fighting: she cheers you on and tells Tam's story a floor at a time. The cut
  // rope stays Reyl's log's to tell (TOP) — Moll only names it once you've read it.
  'npc.oldlight_moll_1': [
    line('MOLL', "Oh! A Wayfarer. Reyl sends one up now and then. I'm Moll: forty years the straight half of a double act, right here."),
    line('MOLL', "Tam Wash was the funny half. She built that joke-box upstairs for while she was on the water. Up you go, love. I'm right behind you."),
  ],
  'npc.oldlight_moll_3': [
    line('MOLL', "Interval! Tam's rule: nobody climbs hungry. Cheese-buns, two each. Three if you heckled well."),
    line('MOLL', "She said a lighthouse and a joke want the same thing: somebody out in the dark, coming home toward them."),
    line('MOLL', "[[Sit by the urn]] if you're flagging, love. I'm off up."),
  ],
  'npc.oldlight_moll_5': [
    line('MOLL', "Her pictures, mostly. The old ferry. Reyl, young and scowling. He only smiled when nobody was looking."),
    line('MOLL', "Eleven winters back the fog came in thick as wool. Tam was out with the late boat. ...The boats came home. She didn't."),
    line('MOLL', "Reyl rang that bell till his hands gave out. Go gently with him after, won't you? Nearly there."),
  ],
  'npc.oldlight_moll_6': [
    line('MOLL', "Hear it? The same joke, round and round. He wrote it for her, for when she got home."),
    line('MOLL', "I sit with it once a winter. Somebody ought to laugh at it, and I never can."),
    line('MOLL', "Go on up and finish it for her. I'll take the last flight slow."),
  ],
  'sign.oldlight_mirror_maze': [
    sign('MIRROR MAZE (SMALL). EXIT: THAT WAY. (THE OTHER THAT WAY.)'),
  ],
  'sign.oldlight_maze_end': [
    sign('A dead end and a tall mirror. Your reflection has its back to you, looking for the way out.'),
    sign('A chalk arrow on the glass points at you: EXIT. You are not the exit. You check twice.'),
  ],
  'sign.oldlight_audience': [
    sign('Rows of stools, every one dusted, not one sat on. They all face the little table with the two cups.'),
  ],
  'npc.oldlight_moll_card': [
    line('MOLL', "(puffing) Couldn't sit with it down there. Not this time."),
    line('MOLL', "That's her card in the drum. Eleven winters it's tried to finish her joke."),
    line('MOLL', "His headline act guards the drum now. [[Rest in the green-room chair]] by the stairs first."),
    line('MOLL', "Go on, love. I'll be right here."),
  ],
  'npc.oldlight_moll_top': [
    line('MOLL', "(puffing) Made it. ...You finished her card, didn't you? I heard the drum stop."),
    line('MOLL', "If you've read his log, you know about the rope. He thinks nobody knows. The whole quay knows. We let him carry it his own way."),
    line('MOLL', "Take those floats to [[the netmender]] and [[ring that bell]]. Let the old man hear it rung by someone who laughed on the way up. ...Thank you."),
  ],
};
