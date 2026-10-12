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
    nar('Your foot finds something soft. It lets out a long, mournful note, like a tuba that has just heard bad news.'),
    pw('(from every speaking-tube at once) WHO DID THAT. ...Oh. The cushion. It is always the cushion. (ting!)'),
    { op: 'setFlag', flag: 'flag:oldlight_whoopee_sat' },
  ],
  'script.oldlight_mime': [
    nar('The MIME presses both palms flat against a wall that is not there. She looks at you. She points up the stairs.'),
    nar('She mimes climbing. And climbing. And climbing. She mimes a cup of tea, halfway up, and a very contented sigh.'),
    nar('Then she mimes being trapped in a box. You mime opening the lid for her.'),
    nar('She stares at you as if you have ruined her entire act.'),
  ],
  'script.oldlight_laugh_meter': [
    nar('A brass gauge on a stand: QUIET — CHUCKLE — GUFFAW — UPROAR. The needle is jammed hard against UPROAR.'),
    pw('Calibrated it myself! It has read UPROAR every minute for eleven winters. Morale has never been higher.'),
  ],
  'script.oldlight_laugh_track': [
    nar('Three clockwork dolls on a bench, wound tight, mouths open. A brass button is marked PRESS IF SHY.'),
    { op: 'sfx', key: 'ui-confirm' },
    nar('HA. HA. HA. — they laugh in perfect time, then stop, and turn slowly to look at one another, as if to ask who started it.'),
    pw('The laugh track! For when the audience is shy. Or absent. Or, most nights, both.'),
  ],
  'script.oldlight_jack_box': [
    nar('A jack-in-the-box, already sprung. Its little clown hangs out over the rim, quite out of breath.'),
    pw('Eleven winters he waited for someone to turn the handle. Then a draught did it. He has not spoken to the draught since.'),
  ],
  'script.oldlight_usher': bout('usher', 'USHER', [
    'TICKETS, please! ...No ticket? Then you pay the house\'s old price, same as everybody: one bout, best of whatever we\'ve got.',
  ], [
    '(He stamps the back of your hand. It reads: ADMIT ONE. Underneath, smaller: BRAVE.)',
  ]),

  // ---- F2: the Late Laugh ----------------------------------------------------------------
  'script.oldlight_laugh_track_late': [
    nar('Another bench of clockwork dolls. You press the button. Nothing at all happens.'),
    nar('You give up and turn to go.'),
    { op: 'wait', ms: 900 },
    nar('...HA. HA. HA.'),
  ],
  'script.oldlight_juggler': bout('juggler', 'JUGGLER', [
    'Watch this! Three cheese-buns, one hand! ...Two cheese-buns. ...One cheese-bun and a bit of floor.',
    'Battle me while I pick these up!',
  ], [
    'I can do four now. Well. I can DROP four. In a very juggly sort of way.',
  ]),

  // ---- F3: Intermission --------------------------------------------------------------------
  'script.oldlight_pie_thrower': bout('pie_thrower', 'PIE-THROWER', [
    'Interval special! One custard pie, delivered at speed, to the face of your choice!',
    '...No? Then I\'ll throw my kin at you instead. Less custard. More feelings.',
  ], [
    'Fair\'s fair — you\'ve earned a pie. Not to eat. Nobody eats them. They\'re for COMEDY.',
  ]),

  // ---- F4: the Backwards Inn -------------------------------------------------------------------
  'script.oldlight_mirror': bout('mirror', 'THE MIRROR', [
    'Nice coat. Same as mine. Same hair, same lamp, same face. Punchwheel built me to show visitors their best side.',
    'You\'re reaching for your lamp. I\'m reaching for my lamp. You blinked. I blinked.',
    '...Fine. I blinked first. BATTLE!',
  ], [
    '(He copies your bow. Then he starts copying you walking away, thinks better of it, and stays put.)',
  ]),

  // ---- F5: the Gallery of Confident Facts ---------------------------------------------------
  'script.oldlight_lectern': [
    nar('A lectern holding an enormous book: THE BIG BOOK OF FACTS, by MR. PUNCHWHEEL. It falls open where it is opened most.'),
    pw('FACT: the sea is salty because the fish have been crying ever since somebody told them about rain.'),
    pw('FACT: every lamp in Vesperholm is secretly the same lamp, moving very fast.'),
    pw('FACT: this book is one hundred per cent accurate. (CORRECTIONS ON PAGE FOUR.) (PAGE FOUR IS MISSING.)'),
  ],
  'script.oldlight_banana': [
    { op: 'sfx', key: 'world-bump' },
    nar('Your foot meets a banana peel. Time slows. Your whole life flashes past your eyes. Most of it was walking.'),
    nar('You do not fall. You do something far worse: you nearly fall, catch yourself, and look round to see whether anyone saw.'),
    pw('(from every speaking-tube at once) I SAW.'),
    { op: 'setFlag', flag: 'flag:oldlight_banana_slipped' },
  ],
  'script.oldlight_critic': bout('critic', 'THE CRITIC', [
    'Two stars. You haven\'t done anything yet — that\'s two stars for turning up. Battle me and I\'ll decide whether to take one back.',
  ], [
    'Four stars. It would have been five, but your kin didn\'t do an encore. They never do, these days.',
  ]),

  // ---- F6: the One Joke — the two cups (the floor's rest) ------------------------------------
  'script.oldlight_cups_rest': [
    nar('Two cups on the table. One has been washed every day for a long time. The other has never been moved.'),
    {
      op: 'choice',
      prompt: 'Sit a while?',
      options: [
        {
          label: 'Sit down.',
          ops: [
            nar('You take the chair that has never been moved. It is the most comfortable chair in the tower. Somebody chose it very carefully, a long time ago.'),
            { op: 'heal', sleep: false },
            nar('Your kin are rested. Across the table, the other cup stays exactly where it has always been.'),
          ],
        },
        { label: 'Leave it be.', ops: [] },
      ],
    },
  ],

  // ---- Lightkeeper's Point: PIP runs after you on the way out --------------------------------
  // Fires once, on the Point's one crossing back to the quay, if you've climbed the
  // tower (the floats are yours) but haven't had the rope yet.
  'script.oldlight_rope_reminder': [
    { op: 'emote', actor: 'pip', emote: 'alert', unless_flag: 'flag:q_south_has_rope' },
    { op: 'move', actor: 'pip', to: { tx: 17, ty: 8 }, unless_flag: 'flag:q_south_has_rope' },
    { op: 'say', speaker: 'PIP', text: 'WAIT! Wayfarer! Gran says you went UP the Old Light — all the way! Did you get her floats back off that machine?', unless_flag: 'flag:q_south_has_rope' },
    { op: 'say', speaker: 'PIP', text: 'Take them to her on the quay, by her nets! She\'s got the bell-rope put by. Then you can walk the whole breakwater, right out to the bell.', unless_flag: 'flag:q_south_has_rope' },
    { op: 'say', speaker: 'PIP', text: 'And go all the way to the END. Everyone says there\'s somebody out past the bell who... I don\'t know what he is. Nobody does! Go and SEE!', unless_flag: 'flag:q_south_has_rope' },
    { op: 'setFlag', flag: 'flag:oldlight_rope_reminded' },
  ],
  // ---- MOLL's two floors that notice your wins (the rest are plain dialogue) ----------
  'script.oldlight_moll_2': [
    say('MOLL', "Don't ask how I got here first. Sixty years of knowing where the back stairs are."),
    { ...say('MOLL', "And I heard you see off that heckler. Tam would've hired you on the spot."), if_flag: 'flag:oldlight_heckler_beaten' },
    say('MOLL', "This was our stage. Winter nights the whole quay squeezed in. Tam rowed the late ferry, then came on still dripping in her oilskins and did twenty minutes."),
    say('MOLL', "The audience laughed a beat late even then. 'Fog in their ears,' she said. You're doing grand. Keep climbing."),
  ],
  'script.oldlight_moll_4': [
    { ...say('MOLL', "The Ringmaster's still sulking. Good. He's needed a proper audience for years."), if_flag: 'flag:oldlight_ringmaster_beaten' },
    say('MOLL', "Everything's backwards on this floor. Tam's idea. 'People look their best laughing at themselves, Moll.'"),
    say('MOLL', "She'd pull faces at those mirrors till the mirrors gave up first."),
    say('MOLL', "You've a good face for this. A face that keeps going. That's the whole trick of comedy, and of most things."),
  ],
  // ---- F5: the waxed floor (a glare-ice flow across the hall's north lane) ----------------
  'script.oldlight_waxed_floor': [
    nar('The gallery floor gleams like a frozen pond. Someone has waxed it to a mirror shine.'),
    pw('(from a speaking-tube) MIND THE FLOOR! I polished it for the critics. Then I left some bananas on it. For the critics.'),
    nar('Step onto the shine and you will skid until something stops you. The dry boards either side are slower, and far less fun.'),
    { op: 'setFlag', flag: 'flag:oldlight_waxed_seen' },
  ],
};

export const JESTHOUSE_DIALOGUE: DialogueRegistry = {
  // ---- F1 ---------------------------------------------------------------------------------
  'sign.oldlight_applause': [
    sign('A lit box sign: APPLAUSE. Underneath, in smaller letters: (OR AT LEAST A KIND NOD.)'),
    sign('Underneath that, smaller still: (OR JUST STAY A WHILE. STAYING COUNTS.)'),
  ],
  'sign.oldlight_coats': [
    sign('The cloakroom. Every coat has a ticket pinned to it, and every ticket says: BACK IN FIVE MINUTES. The dust has been counting.'),
  ],
  'sign.oldlight_chickens': [
    sign('A hat-stand hung with rubber chickens. A card: ONE PER CUSTOMER. TO BE SQUEEZED IN EMERGENCIES ONLY. (A LONG SILENCE IS AN EMERGENCY.)'),
  ],
  'sign.oldlight_masks': [
    sign('Two masks on the wall, one laughing, one weeping. Somebody has drawn a tiny moustache on the weeping one. It looks much happier.'),
  ],
  'npc.oldlight_groaner': [
    line('GROANER', 'Ohhhhh. ...Sorry. Reflex.'),
    line('GROANER', 'I\'m the house groaner. Every good jest-house keeps one. When the machine lands a pun, somebody has to make the noise it deserves.'),
    line('GROANER', 'Eleven winters of it. The lamp-doctor says I\'ve the lungs of a man who\'s heard every pun twice.'),
  ],
  'npc.oldlight_usher_after': [
    line('USHER', 'Best seats are upstairs. Worst jokes too. It\'s a package.'),
  ],
  'trainer.oldlight_usher.defeat': [line('USHER', 'Ticket stamped, guest seated, usher flattened. A full night\'s work.')],

  // ---- F2 ---------------------------------------------------------------------------------
  'sign.oldlight_unicycle': [
    sign('A unicycle on a stand. A label: FOR THE ACT. A second label: THE ACT IS FALLING OFF A UNICYCLE.'),
    sign('A third label, in different handwriting: IT\'S A VERY GOOD ACT.'),
  ],
  'sign.oldlight_clown_shoes': [
    sign('A pair of enormous clown shoes. Inside one sits a smaller pair of clown shoes. Inside those, a note: IT\'S SHOES ALL THE WAY DOWN.'),
  ],
  'sign.oldlight_masks_late': [
    sign('Two masks. The weeping one is wincing at a joke the laughing one hasn\'t heard yet.'),
  ],
  'npc.oldlight_juggler_after': [
    line('JUGGLER', 'Want to see me juggle three kin? ...Neither do they. They\'ve made that very clear.'),
  ],
  'trainer.oldlight_juggler.defeat': [line('JUGGLER', 'I dropped the battle! I meant to do that. That was the act.')],

  // ---- F3 ---------------------------------------------------------------------------------
  'sign.oldlight_teacups': [
    sign('A tower of teacups stacked eleven high. A card at the bottom: DO NOT TAKE THE BOTTOM CUP.'),
    sign('A card at the top: WE KNOW YOU\'RE THINKING ABOUT IT.'),
  ],
  'sign.oldlight_pies': [
    sign('A table of custard pies. One is missing. There is a perfect pie-shaped mark on the ceiling. Nobody has explained it, and nobody will.'),
  ],
  'sign.oldlight_cogs': [
    sign('A heap of spare brass cogs, each one labelled. SPARE TIMING. FOR WHEN THE SMALL TALK STICKS. The biggest says: DO NOT LOSE. THIS ONE IS THE PUNCH.'),
  ],
  'npc.oldlight_pie_thrower_after': [
    line('PIE-THROWER', 'Interval\'s nearly over. Mind how you go upstairs — they don\'t have custard up there. Just feelings.'),
  ],
  'trainer.oldlight_pie_thrower.defeat': [line('PIE-THROWER', 'Splat. That one was mine, wasn\'t it.')],

  // ---- F4 ---------------------------------------------------------------------------------
  'sign.oldlight_clock_backwards': [
    sign('A wall clock with every number the wrong way round. By its reckoning, you left this room an hour from now, and you were very glad you did.'),
  ],
  'sign.oldlight_upside_chair': [
    sign('A chair standing on its head. A note tied to one leg: IT\'S FINE. IT\'S RESTING.'),
  ],
  'sign.oldlight_funhouse': [
    sign('A wobbly carnival mirror. In it you are seven feet tall and one inch wide. Your reflection gives you a thumbs-up you did not give it.'),
  ],
  'npc.oldlight_mirror_after': [
    line('THE MIRROR', 'Same time next week? ...I already said yes. You just hadn\'t asked yet.'),
  ],
  'trainer.oldlight_mirror.defeat': [line('THE MIRROR', 'You win. Which means I also— no. No, it doesn\'t work like that.')],

  // ---- F5 ---------------------------------------------------------------------------------
  'sign.oldlight_mallet': [
    sign('A giant wooden mallet. The handle reads: FOR EMERGENCY PUNCHLINES. Lower down, more firmly: NOT FOR THE AUDIENCE.'),
  ],
  'npc.oldlight_critic_after': [
    line('THE CRITIC', 'The tower? Three stars. The jokes are too long and the stairs are too many. I come every night.'),
  ],
  'trainer.oldlight_critic.defeat': [line('THE CRITIC', 'Five stars. Don\'t let it go to your head. I give the stairs five stars too.')],

  // ---- F6 ---------------------------------------------------------------------------------
  'sign.oldlight_old_confetti': [
    sign('A small heap of very old confetti, swept into a corner and then, it seems, never swept away. Somebody was keeping it for a celebration that hasn\'t come yet.'),
  ],
  'sign.oldlight_spring_can': [
    sign('A can of spring-snakes with its lid popped. Only one snake jumped. The rest are still inside, waiting for a better audience.'),
  ],

  // ---- MOLL: Tam's old stage partner, always one floor ahead (build_pearlmoor_oldlight.py
  // MOLL). Non-fighting: she cheers you on and tells Tam's story a floor at a time. The cut
  // rope stays Reyl's log's to tell (TOP) — Moll only names it once you've read it.
  'npc.oldlight_moll_1': [
    line('MOLL', "Oh! A Wayfarer. Reyl sends one up now and then. I send myself, once a winter."),
    line('MOLL', "I'm Moll. Forty years I was the straight half of a double act, right here in this lobby. Tam Wash was the funny half."),
    line('MOLL', "She built that clattering joke-box upstairs so there'd still be jokes when she was out on the water. Go on, love, up you go. I'll be right behind you."),
  ],
  'npc.oldlight_moll_3': [
    line('MOLL', "Interval! Tam's rule: nobody climbs on an empty stomach. She baked cheese-buns for the house. Two each. Three if you heckled well."),
    line('MOLL', "She used to say a lighthouse and a joke want the same thing: somebody out in the dark, coming home toward them."),
    line('MOLL', "Sit by the urn if you're flagging, love. I'm off up. My knees and I aren't on speaking terms."),
  ],
  'npc.oldlight_moll_5': [
    line('MOLL', "Her pictures, mostly. That's the old ferry. That's Reyl, young and scowling. He only ever smiled when he thought nobody was looking."),
    line('MOLL', "Eleven winters back the fog came in thick as wool. Tam was out with the late boat. ...The boats came home. She didn't."),
    line('MOLL', "Reyl rang that bell till his hands gave out. You'll understand more at the top. Go gently with him after, won't you? Nearly there."),
  ],
  'npc.oldlight_moll_6': [
    line('MOLL', "Hear it? The same joke, round and round. He wrote it for her, for when she got home."),
    line('MOLL', "I come up once a winter and sit with it a while. Somebody ought to laugh at it, and I never can."),
    line('MOLL', "Go on up and finish it for her. I'll be along. The last flight's the steepest, and I like to take it slow."),
  ],
  'sign.oldlight_mirror_maze': [
    sign('A card on a stand: MIRROR MAZE (SMALL). EXIT: THAT WAY.'),
    sign('Underneath, in the same hand: (THE OTHER THAT WAY.)'),
  ],
  'sign.oldlight_audience': [
    sign('Rows of stools, set out for an audience. Every one has been dusted. Not one has been sat on.'),
    sign('They all face the little table with the two cups.'),
  ],
  'npc.oldlight_moll_card': [
    line('MOLL', "(puffing) Couldn't sit with it down there. Not this time."),
    line('MOLL', "That's her card, jammed in the drum. Eleven winters it's been trying to finish her joke for her."),
    line('MOLL', "Go on, love. You've laughed all the way up. I'll be right here."),
  ],
  'npc.oldlight_moll_top': [
    line('MOLL', "(puffing) There. Made it. ...You finished her card, didn't you? I heard the drum stop turning."),
    line('MOLL', "If you've read his log, you know about the rope. He thinks nobody knows. The whole quay knows, love. We just let him carry it his own way."),
    line('MOLL', "Take those floats down to the netmender and ring that bell. Let the old man hear it rung by someone who laughed on the way up. ...Thank you. Truly."),
  ],
};
