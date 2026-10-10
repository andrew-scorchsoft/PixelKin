/**
 * R9 "The Old Light" — the joke-tower on Lightkeeper's Point (pearlmoor_point,
 * pearlmoor_oldlight_1..6, pearlmoor_oldlight_top; tools/maps/build_pearlmoor_oldlight.py).
 *
 * Eleven winters ago Reyl Wash took the lamp out of Pearlmoor's second lighthouse
 * and put Tam's clockwork joke-engine, MR. PUNCHWHEEL, where the light had been.
 * The climb is the middle leg of the Causeway Bell chain (walkthrough/01-south.md):
 *   script.reyl_quest (flag:q_south_bell) -> the tower (one riddle per floor,
 *   flag:oldlight_N_solved) -> the top floor (flag:picked_net_floats +
 *   flag:q_south_jest_done) -> the netmender's rope -> the bell -> Reyl.
 *
 * Every joke in the tower is the MACHINE's — the lobby plaque and Punchwheel's
 * first lines say so outright (the owner asked for "artificial intelligence" to
 * be unmistakable here; the plaque says "thinking machine"). The one human line
 * is Tam's unfinished card at the top, and the player supplies its punchline.
 *
 * Joke text is the scored final set (scratchpad jokes_final.md, slot ids
 * F1.PLAQUE … TOP.RIGHT) used verbatim; slot ids are noted per line as
 * `// JOKE: <slot>`. Lines tagged `// DRAFT:` are connective/functional text
 * the final set didn't cover.
 *
 * Riddles never dead-end: a wrong pick plays a joke + a hint and re-offers the
 * choice; after two misses Punchwheel "accidentally" blurts the answer and the
 * stair opens anyway. Cancelling simply steps away — the band re-offers. The
 * Tin Rower (flag:has_tin_rower, another agent's item) adds a free-hint option.
 */
import type { CutsceneChoice, CutsceneStep, DialogueLine, DialogueRegistry, ScriptRegistry } from './types';

const PW = 'PUNCHWHEEL';
const ROWER = 'flag:has_tin_rower';
const pw = (text: string): CutsceneStep => ({ op: 'say', speaker: PW, text });
const nar = (text: string): CutsceneStep => ({ op: 'narrate', text });
const line = (speaker: string, text: string): DialogueLine => ({ speaker, text });

/** The stair-gate opening — the shared tail of every solved riddle. */
function solved(n: number): CutsceneStep[] {
  return [
    { op: 'sfx', key: 'world-door' },
    nar('(Somewhere in the stairwell, a cog turns over. The stair-gate clicks open.)'), // DRAFT: stair_open
    { op: 'setFlag', flag: `flag:oldlight_${n}_solved` },
  ];
}

interface RiddleOpt {
  label: string;
  ops: CutsceneStep[];
  right?: boolean;
  if_flag?: string;
}

/**
 * A layered-retry riddle: `opts` (one marked `right`) offered as a choice; a
 * wrong pick plays its own lines, then (`levels` times) the re-prompt + choice
 * again; past the last level Punchwheel `blurt`s and `after` runs (the gate
 * opens anyway) — or, with `finalOnlyRight`, one last choice offering only the
 * right answer. The Tin Rower option (shown only with the toy) is a free win.
 */
function riddle(o: {
  prompt: string;
  speaker?: string;
  opts: RiddleOpt[];
  rower?: CutsceneStep[];
  blurt: CutsceneStep[];
  after: CutsceneStep[];
  levels?: number;
  finalOnlyRight?: boolean;
}): CutsceneStep {
  const levels = o.levels ?? 2;
  const right = o.opts.find((x) => x.right)!;
  const win = [...right.ops, ...o.after];
  const level = (k: number): CutsceneStep => {
    const options: CutsceneChoice[] = o.opts.map((x) => {
      if (x.right) return { label: x.label, ops: win, if_flag: x.if_flag };
      const tail: CutsceneStep[] =
        k + 1 < levels
          ? [level(k + 1)]
          : o.finalOnlyRight
            ? [...o.blurt, { op: 'choice', speaker: o.speaker ?? PW, prompt: o.prompt, options: [{ label: right.label, ops: win }] }]
            : [...o.blurt, ...o.after];
      return { label: x.label, ops: [...x.ops, ...tail], if_flag: x.if_flag };
    });
    if (o.rower) options.push({ label: 'Wind the Tin Rower.', if_flag: ROWER, ops: [...o.rower, ...win] });
    return { op: 'choice', speaker: o.speaker ?? PW, prompt: k === 0 ? undefined : o.prompt, options };
  };
  return level(0);
}

// ---- F5: the knock-knock loop (the joke no one has ever told) ---------------------
const NOBODY: CutsceneStep[] = [
  { op: 'musicFade', ms: 700 },
  { op: 'tint', color: '#3a5a8c', alpha: 0.32, ms: 700 },
  nar('(The machine stops. The gallery goes cool and quiet.)'), // JOKE: F5.NEVERTOLD
  pw("...nobody. no. nobody's answered that door in eleven winters."), // JOKE: F5.NEVERTOLD (the tower's only lowercase line)
  { op: 'setFlag', flag: 'flag:oldlight_knock_done' },
  { op: 'tint', color: '#3a5a8c', alpha: 0, ms: 1100 },
];
const LOOP5 = 'Knock. (delivery!) (delivery!!) (DELIVERY!!!) ...Knock knock.'; // JOKE: F5.NEVERTOLD loop 5+
function knockLoop(): CutsceneStep {
  const nobody = { label: 'Nobody.', ops: NOBODY };
  // loop 5+ re-offers until [Nobody.] (three more turns, then only Nobody remains)
  let tail: CutsceneStep = { op: 'choice', speaker: PW, options: [nobody] };
  for (let i = 0; i < 3; i++) {
    tail = {
      op: 'choice',
      speaker: PW,
      options: [
        { label: "Who's there?", ops: [pw('Knock.'), { op: 'choice', speaker: PW, options: [{ label: 'Knock who?', ops: [pw(LOOP5), tail] }] }] },
        nobody,
      ],
    };
  }
  const l4: CutsceneStep = {
    op: 'choice', speaker: PW,
    options: [{ label: "Who's there?", ops: [pw('Knock. (this is the new bit)'), { op: 'choice', speaker: PW, options: [{ label: 'Knock who?', ops: [pw(LOOP5), tail] }] }] }, nobody],
  };
  const l2: CutsceneStep = {
    op: 'choice', speaker: PW,
    options: [{ label: "Who's there?", ops: [pw('Knock. (this is the new bit)'), { op: 'choice', speaker: PW, options: [{ label: 'Knock who?', ops: [pw('Knock knock. (nobody has ever told this joke, because nobody has ever finished it)'), l4] }] }] }, nobody],
  };
  return {
    op: 'choice', speaker: PW,
    options: [
      { label: "Who's there?", ops: [pw('Knock.'), { op: 'choice', speaker: PW, options: [{ label: 'Knock who?', ops: [pw('Knock knock. (pause for laughter)'), l2] }] }] },
      nobody,
    ],
  };
}

const WELCOME: CutsceneStep[] = [
  pw("Ladies, gentlemen and kin! Every joke in this tower was written by a thinking machine. (ting!) That's me. I'm the machine."), // JOKE: F1.SAYSO
  pw("Not one human helped. You'll be able to hear the difference. (pause for laughter) (no laughter detected)"), // JOKE: F1.SAYSO
  pw('...See?'), // JOKE: F1.SAYSO
  pw('Three clockwork lamplighters walk into an inn. The first one says— (whirr) The second one says— (clunk)'), // JOKE: F1.LAMPLIGHTERS
  pw("The third one says... (ting?) ...I've lost it. Don't worry, folks. Punchlines wash up. Usually on floor three."), // JOKE: F1.LAMPLIGHTERS
  { op: 'setFlag', flag: 'flag:oldlight_welcomed' },
];

export const OLDLIGHT_SCRIPTS: ScriptRegistry = {
  // ---- F1: The Lobby of Groaners --------------------------------------------------
  'script.oldlight_welcome': WELCOME,
  // The Laugh Turnstile: EVERY option turns it (the floor teaches the rule: play along).
  'script.oldlight_1': [
    { op: 'run', ref: 'script.oldlight_welcome', unless_flag: 'flag:oldlight_welcomed' },
    pw("This turnstile only turns for a laugh. I've been stuck behind it eleven winters. Here's my best one:"), // JOKE: F1.TURNSTILE
    pw('What has one bright eye, stands on the shore all night, and worries about every boat?'), // JOKE: F1.TURNSTILE
    pw("A lighthouse. (pause for laughter) ...Or anybody's mum."), // JOKE: F1.TURNSTILE
    {
      op: 'choice',
      speaker: PW,
      options: [
        { label: 'Laugh.', ops: [pw("(LAUGHTER DETECTED!) Eleven winters I've waited to hear that up close. Go on through!"), ...solved(1)] }, // JOKE: F1.TURNSTILE.REACT
        { label: 'Groan.', ops: [pw('A groan is just a laugh with its coat on. (The turnstile turns, grudgingly.)'), ...solved(1)] }, // JOKE: F1.TURNSTILE.REACT
        {
          label: 'Explain the joke back.',
          ops: [
            pw("Nobody's ever explained one of my jokes back to me. I feel SEEN."), // JOKE: F1.TURNSTILE.REACT
            pw('...You got it slightly wrong. But I feel SEEN.'), // JOKE: F1.TURNSTILE.REACT
            ...solved(1),
          ],
        },
        {
          label: 'Laugh like PAUL!!!!!!',
          if_flag: 'flag:name_is_paul',
          ops: [
            { op: 'shake', ms: 600, intensity: 0.012 },
            nar('The turnstile shakes, whirls, and spins clean off its post.'), // JOKE: F1.TURNSTILE.REACT (Paul)
            pw('...THAT is the laugh I was built for.'), // JOKE: F1.TURNSTILE.REACT (Paul)
            ...solved(1),
          ],
        },
      ],
    },
  ],

  // ---- F2: The Room That Laughs a Beat Too Late ------------------------------------
  'script.oldlight_heckler': [
    { op: 'say', speaker: 'HECKLER', text: "OI! (reads a card) 'YOUR LAMP IS SO DIM... IT IS QUITE DIM.'" }, // JOKE: F2.HECKLER.INTRO
    { op: 'say', speaker: 'HECKLER', text: "Don't look at me. The machine writes my heckles. I just bring the volume. BATTLE!" }, // JOKE: F2.HECKLER.INTRO
    { op: 'battle', trainer: 'oldlight_heckler' },
    { op: 'setFlag', flag: 'flag:oldlight_heckler_beaten' },
  ],
  'script.oldlight_2': [
    pw("What's the hardest part of being a lighthouse?"), // JOKE: F2.LATELAUGH
    riddle({
      prompt: "What's the hardest part of being a lighthouse?",
      opts: [
        { label: 'Punchline straight away.', ops: [nar('The audience laughs, late, all over your punchline. (laughter detected... at the wrong bit) Give them a beat, little lamp.')] }, // JOKE: F2.LATELAUGH retry
        {
          label: 'Say nothing. Wait a beat.',
          right: true,
          ops: [
            nar('(The audience, one line late, finally laughs at the setup. The pause fills up with it.)'), // JOKE: F2.LATELAUGH
            pw('Everybody looks at you. Nobody pops up for tea.'), // JOKE: F2.LATELAUGH
            nar('(This time the late laugh lands right on the punchline. The pews rattle.)'), // JOKE: F2.LATELAUGH
            pw('...Another lighthouse one, sorry. They tell you: write what you know. (ting!)'), // JOKE: F2.LATELAUGH
            pw('There! TIMING, little lamp. Comedy is timing.'), // JOKE: F2.TIMING
            pw('Tragedy is just timing that went out to sea. ...(ting?)'), // JOKE: F2.TIMING
            pw('No. No ting for that one.'), // JOKE: F2.TIMING
          ],
        },
        { label: 'Explain the joke first.', ops: [nar('They laugh at the explanation. The punchline gets a cough. Close! Next time say nothing. Just wait.')] }, // JOKE: F2.LATELAUGH retry
      ],
      rower: [nar('The Tin Rower rows a slow circle and stops. Then nods. Then waits.')], // JOKE: F2.LATELAUGH (Tin Rower)
      blurt: [pw('(whispering) Pick the one where you say nothing.')], // JOKE: F2.LATELAUGH (after two misses)
      after: solved(2),
    }),
  ],

  // ---- F3: Intermission ------------------------------------------------------------
  // The tea-urn automaton: a full rest (and the climb's wake-point).
  'script.oldlight_urn': [
    { op: 'say', speaker: 'TEA-URN', text: 'INTERVAL! TWENTY MINUTES! BUY A BUN!' }, // JOKE: F3.URN
    { op: 'heal' },
    nar('(There is no bun. There has never been a bun. Your kin are mended anyway.)'), // JOKE: F3.URN
    { op: 'say', speaker: 'TEA-URN', text: 'Drink up, love. You look like the first half.' }, // JOKE: F3.URN
  ],
  'script.oldlight_3': [
    { op: 'say', speaker: 'THE MOUTH', text: 'HOW DOES A LAMPLIGHTER GET OVER A BROKEN HEART? ...Mm? Mm?' }, // JOKE: F3.MOUTH
    nar("(Its big rubbery lips pucker and wait for a punchline it hasn't got.)"), // JOKE: F3.MOUTH
    riddle({
      speaker: 'THE MOUTH',
      prompt: 'HOW DOES A LAMPLIGHTER GET OVER A BROKEN HEART? ...Mm? Mm?',
      opts: [
        {
          label: 'One rung at a time.',
          right: true,
          ops: [
            { op: 'say', speaker: 'THE MOUTH', text: '...One rung at a time. (The Mouth sighs, a long, happy, rubbery sigh. The stair-gate clicks.)' }, // JOKE: F3.MOUTH.RESULTS
            pw("(laughter detected) Reunited! I'd cry, but it's bad for the cogs. (ting!)"), // JOKE: F3.MOUTH.RESULTS
          ],
        },
        { label: 'Because it was Tuesday.', ops: [{ op: 'say', speaker: 'THE MOUTH', text: "No. That's not HOW. That's WHEN." }] }, // JOKE: F3.MOUTH.RESULTS
        { label: 'Two cheese-buns, bad play.', ops: [{ op: 'say', speaker: 'THE MOUTH', text: "(quietly) ...That's better than mine." }] }, // JOKE: F3.MOUTH.RESULTS
      ],
      rower: [nar('The Tin Rower rows off across the floor and bumps, very gently, into the punchline that belongs to the ladder.')], // DRAFT: f3_tin_rower
      blurt: [pw('(whispering) The ladder one. She fell off the ladder one.')], // JOKE: F3.MOUTH (after two misses)
      after: solved(3),
    }),
  ],

  // ---- F4: The Backwards Inn -------------------------------------------------------
  'script.oldlight_backwards': [
    pw('Three clockwork lamplighters walk OUT of an inn, backwards. Nobody knows how they got in. HA. HA. HA.'), // JOKE: F4.ANTI.1
    pw('(laughter detected) (it was me)'), // JOKE: F4.ANTI.1
    { op: 'setFlag', flag: 'flag:oldlight_4_opened' },
  ],
  'script.oldlight_lamps_out': [
    pw('How many lamplighters does it take to light a lamp? None. This is the Backwards Inn. Here, we put them OUT. HA. HA. HA.'), // JOKE: F4.ANTI.3
    { op: 'tint', color: '#0b1026', alpha: 0.4, ms: 400 },
    nar('(The lamps along the bar go out one by one. Somewhere, somebody giggles.)'), // JOKE: F4.ANTI.3
    { op: 'tint', color: '#0b1026', alpha: 0, ms: 600 },
  ],
  'script.oldlight_ringmaster': [
    { op: 'say', speaker: 'RINGMASTER', text: "GOODBYE! GOODBYE! You've been a WONDERFUL audience. Row home safe!" }, // JOKE: F4.RING.INTRO
    { op: 'say', speaker: 'RINGMASTER', text: "(It's the Backwards Inn, kid. We start at the end. The machine calls it 'experimental'. I call it Tuesday.) BATTLE!" }, // JOKE: F4.RING.INTRO
    { op: 'battle', trainer: 'oldlight_ringmaster' },
    { op: 'setFlag', flag: 'flag:oldlight_ringmaster_beaten' },
    // he poses the riddle at once (the band beside the stair re-offers it later)
    { op: 'run', ref: 'script.oldlight_4' },
  ],
  'script.oldlight_4': [
    pw('I go out twice a day and come back twice a day, but I never once leave the shore. What am I?'), // JOKE: F4.RIDDLE
    pw('ANSWER: A BURGLAR. (A very local burglar.) CONFIDENCE: TOTAL.'), // JOKE: F4.RIDDLE
    riddle({
      prompt: 'I go out twice a day and come back twice a day, but I never once leave the shore. What am I?',
      opts: [
        {
          label: 'A burglar.',
          ops: [
            pw('(ting!) CORRECT! ...(The stair-gate does not move.)'), // JOKE: F4.RIDDLE
            pw("The gate has never once agreed with me. Somebody's carved a word on the bar. Have a look?"), // JOKE: F4.RIDDLE
          ],
        },
        {
          label: 'A very local burglar.',
          ops: [
            pw("EVEN MORE correct! (The gate still doesn't move.)"), // JOKE: F4.RIDDLE
            pw("...Hm. Check my working? Nobody's ever asked me to check my working."), // JOKE: F4.RIDDLE
          ],
        },
        {
          label: 'A tide.',
          right: true,
          ops: [
            pw("A TIDE? Tides don't burgle— (whirr) ...oh."), // JOKE: F4.RIDDLE
            nar('(The stair-gate swings open.)'), // JOKE: F4.RIDDLE
            pw('Reassessed! Confidence: still total. About something else now.'), // JOKE: F4.RIDDLE
          ],
        },
      ],
      rower: [nar('The Tin Rower rows out... and back. Out... and back. It never leaves the table.')], // JOKE: F4.RIDDLE (Tin Rower)
      blurt: [pw('(whispering) Out and back, little lamp. Out and back.')], // JOKE: F4.RIDDLE (after two misses)
      after: solved(4),
    }),
  ],

  // ---- F5: The Gallery of Confident Facts -------------------------------------------
  'script.oldlight_5': [
    // Paul's question, once: can a machine tell a joke no one has ever told?
    { ...pw('A gentleman (he signed himself p.) once asked me: can a machine tell a joke no one has ever told, with REAL comic delivery?'), unless_flag: 'flag:oldlight_knock_done' }, // JOKE: F5.NEVERTOLD
    { ...pw("I've been working on it for eleven winters. Ready? (cracks knuckles) (has no knuckles) (cracks something else)"), unless_flag: 'flag:oldlight_knock_done' }, // JOKE: F5.NEVERTOLD
    { ...pw('Knock knock.'), unless_flag: 'flag:oldlight_knock_done' }, // JOKE: F5.NEVERTOLD
    { ...knockLoop(), unless_flag: 'flag:oldlight_knock_done' },
    pw('Which caption is TRUE?'), // JOKE: F5.GALLERY.TRUE (prompt)
    riddle({
      prompt: 'Which caption is TRUE?',
      opts: [
        { label: 'REYL, AGED 9, LIGHTHOUSE.', ops: [pw('Verified! I checked it against my source. My source is this painting.')] }, // JOKE: F5.GALLERY.1
        { label: 'A MAP OF TUESDAY.', ops: [pw('That IS a map of Tuesday. Look at all the Tuesday.')] }, // JOKE: F5.GALLERY.2
        { label: 'FROM ABOVE THE STARS.', ops: [pw("Breathtaking, isn't it? You can see your house. It's the dark bit.")] }, // JOKE: F5.GALLERY.3
        { label: "KIN No. 0, 'GERALD'.", ops: [pw('Gerald is real. I can describe him in detail. Medium. Gerald-coloured. Mostly Gerald.')] }, // JOKE: F5.GALLERY.5
        {
          label: 'TAM AND REYL, THE FERRY.',
          right: true,
          ops: [
            nar('The machine goes quiet. Somewhere behind the wall, a spring winds down and is wound back up.'), // DRAFT: f5_true_beat
            pw("...That one I didn't write. That one I just kept."), // DRAFT: f5_true_beat
          ],
        },
      ],
      rower: [nar('The Tin Rower rows a slow line along the gallery floor and stops under the picture with the ferry in it.')], // DRAFT: f5_tin_rower
      blurt: [pw('(whispering) The one with the ferry in it.')], // DRAFT: f5_blurt
      after: solved(5),
    }),
  ],

  // ---- F6: The One Joke (nothing to solve; the music drops out on first crossing) ----
  'script.oldlight_6': [
    pw('Why did the moor-bell never get lonely?'), // JOKE: F6.ONEJOKE
    pw("...I wrote that one for her. She said she'd tell me if it was funny when she got home."), // JOKE: F6.ONEJOKE
    pw('(pause for laughter)'), // JOKE: F6.ONEJOKE
    pw('(pause)'), // JOKE: F6.ONEJOKE
    pw('Why did the moor-bell never get lonely?'), // JOKE: F6.ONEJOKE
  ],
  'script.oldlight_one_joke': [
    { op: 'musicFade', ms: 1200 },
    { op: 'silence', ms: 600 },
    { op: 'run', ref: 'script.oldlight_6' },
    { op: 'setFlag', flag: 'flag:oldlight_6_heard' },
  ],

  // ---- TOP: The Winding Room --------------------------------------------------------
  'script.oldlight_log': [
    nar("A ship's log lies open on the table, in a careful seaman's hand. Reyl's."), // DRAFT: top_log_intro
    { op: 'say', speaker: "REYL'S LOG", text: "Night of the fog. Rang till my hands went. The boats came in. She didn't." },
    { op: 'say', speaker: "REYL'S LOG", text: "Cut the rope today. Told the quay the storm had it. The netmender knows. Spliced a new one anyway. Hasn't said a word. Hasn't needed to." },
    { op: 'say', speaker: "REYL'S LOG", text: "Wound Tam's box with every joke she ever told me and put it where the light was. If the Old Light can't shine, it can laugh." },
    { op: 'say', speaker: "REYL'S LOG", text: 'Eleven winters. The box is making up its own now. They\'re getting strange. So am I, a bit.' },
    pw('He sends me audiences. I think they are apologies.'), // JOKE: TOP.APOLOGIES
  ],
  'script.oldlight_top': [
    { op: 'letterbox', on: true, ms: 320 },
    { op: 'musicFade', ms: 800 },
    nar("Tam's card, jammed in the drum: WHY DOES A FERRYMAN NEVER SAY GOODBYE? —"), // JOKE: TOP.ATTEMPTS
    pw("Attempt one: 'He's too oar-some.' (no laughter detected)"), // JOKE: TOP.ATTEMPTS
    pw("Attempt nine thousand: 'Because it was Tuesday.' (no laughter detected)"), // JOKE: TOP.ATTEMPTS
    pw("Attempt thirty-one thousand: 'Because goodbye is a land word.' (no laughter detected) ...I liked that one."), // JOKE: TOP.ATTEMPTS
    pw('Eleven winters. She never wrote the end. Do you know it?'), // JOKE: TOP.ATTEMPTS
    riddle({
      prompt: 'WHY DOES A FERRYMAN NEVER SAY GOODBYE? — ...Do you know it?', // DRAFT: top_reprompt
      levels: 3,
      finalOnlyRight: true,
      opts: [
        { label: 'Because it was Tuesday.', ops: [pw("(no laughter detected) Tuesday goes in ALL of them, little lamp. That's how you know it doesn't go in hers.")] }, // JOKE: TOP.WRONG
        { label: 'Two cheese-buns, bad play.', ops: [pw("(no laughter detected) That's not a punchline. That's a lovely night in.")] }, // JOKE: TOP.WRONG
        { label: 'Knock knock.', ops: [pw("(no laughter detected) No more knocking. You're already in.")] }, // JOKE: TOP.WRONG
        {
          label: 'Tides go out to come back.',
          right: true,
          ops: [
            // (the menu row is short; the player says the whole line here)
            nar("You say it the way Reyl does, the way you've heard him say it all over the quay: \"Because tides go out so they can come back.\""), // DRAFT: top_say_it
            pw('(laughter detected) (LAUGHTER DETECTED) (LAUGHTER DETECTED!!!!!!)'), // JOKE: TOP.RIGHT
            { op: 'shake', ms: 900, intensity: 0.014 },
            nar('(The three tin lamplighters march. One enormous, warm laugh shakes the whole tower.)'), // JOKE: TOP.RIGHT
            pw('That one had never been told before. Eleven winters I tried to write it myself.'), // JOKE: TOP.RIGHT
            pw('Turns out it takes two. (ting.)'), // JOKE: TOP.RIGHT
          ],
        },
      ],
      blurt: [pw('(whispering) It\'s the one Reyl says. He says it all the time. He never says who said it first.')], // DRAFT: top_blurt
      after: [
        // the Tin Rower finds its slot in the drum (design: the empty boat-shaped gap)
        { ...nar('The Tin Rower whirs in your pack, clambers out, and clicks into the empty boat-shaped slot in the drum. It rows the circle with the lamplighters, nodding.'), if_flag: ROWER }, // DRAFT: top_tin_rower
        pw("Oh — and these. The netmender's. They washed up on my sill the night of the storm. I kept them for the act."), // DRAFT: top_floats
        { op: 'run', ref: 'script.pickup_net_floats', unless_flag: 'flag:picked_net_floats' },
        { ...pw("...You've already GOT her floats? Then I've been rehearsing with a spare. Typical. Take it to her anyway."), if_flag: 'flag:picked_net_floats' }, // DRAFT: top_floats_oldsave
        { op: 'setFlag', flag: 'flag:picked_net_floats' },
        { op: 'setFlag', flag: 'flag:q_south_jest_done' },
        { op: 'sfx', key: 'world-door' },
        nar("A hatch in the floor springs open with a cheerful BOING. Of course the Old Light has a slide. It's the last joke in the building."), // DRAFT: top_slide
        { op: 'musicCrossfade', key: 'pearlmoor-quay-c', ms: 900 },
        { op: 'letterbox', on: false, ms: 320 },
      ],
    }),
  ],
};

export const OLDLIGHT_DIALOGUE: DialogueRegistry = {
  // ---- Lightkeeper's Point -----------------------------------------------------------
  'door.oldlight_locked': [
    { text: 'The door\'s handle is a brass nose. It is cold, and it does not find you funny.' },
    { text: 'A card in the letter-slot: AUDIENCES BY APPOINTMENT. APPLY TO R. WASH, THE TIDE LUMENARY.' }, // DRAFT
  ],
  'sign.oldlight': [
    { text: "THE OLD LIGHT — PEARLMOOR'S JEST-HOUSE.\nSHUT FOR REPAIRS (11 WINTERS). PLEASE DO NOT TICKLE THE DOOR." },
  ],
  'sign.oldlight_chute': [
    { text: 'A brass mouth in the grass at the tower\'s foot, grinning up at you. Faint giggling comes from inside. It looks like the bottom of a slide.' }, // DRAFT
    { text: 'It only seems to let people come DOWN. For now.' }, // DRAFT
  ],
  'sign.wash_ferryhouse': [
    { text: 'The Wash ferry-house. The shutters are nailed and the step hasn\'t been swept in years.' },
    { text: 'A faded board over the door: SAME TIDE TOMORROW — FERRIES, MENDING, JOKES (FREE).' }, // DRAFT
  ],
  'sign.wash_mailbox': [
    { text: 'The mailbox is stuffed solid: eleven winters of the quay newsletter, every one unopened.' },
  ],
  'sign.point_bench': [
    { text: 'A bench facing the open sea. Two sets of initials are carved into the arm: R. and T.' }, // DRAFT
    { text: 'You sit a moment. Every buoy out there is dark.' }, // DRAFT
  ],

  // ---- In the tower ------------------------------------------------------------------
  'sign.oldlight_stairgate': [
    { text: "The stair-gate's cogs are waiting on a laugh. The speaking-tube by the stair is listening." },
  ],
  'sign.oldlight_plaque': [
    { text: 'ALL JOKES IN THIS TOWER WERE COMPOSED BY MR. PUNCHWHEEL, PATENT JEST-ENGINE: A THINKING MACHINE OF BRASS AND BELLOWS.' }, // JOKE: F1.PLAQUE
    { text: 'NO HUMAN WROTE A SINGLE ONE. HUMANS HAVE BEEN INFORMED, AND ARE RELIEVED.' }, // JOKE: F1.PLAQUE
    { text: '(EXCEPT ONE. TOP FLOOR. UNFINISHED.)' }, // JOKE: F1.PLAQUE
  ],
  'sign.oldlight_box_office': [
    line(PW, "I asked the tide for advice once. It said, 'Come back later.' (ting!)"), // JOKE: F1.OPENER.1
    line(PW, '...So I did. It was out.'), // JOKE: F1.OPENER.1
    line(PW, "What do you call a kin that's just kindled? Taller. (ting!)"), // JOKE: F1.OPENER.2
    line(PW, "That's all kindling is, folks: height and confidence. I've got one of those."), // JOKE: F1.OPENER.2
  ],
  'npc.oldlight_tube_1': [
    line(PW, 'How many lamplighters does it take to light a lamp? (pause for laughter)'), // JOKE: F1.OPENER.3
    line(PW, "...One. It's a one-person job. I don't know why I paused. (pause for laughter)"), // JOKE: F1.OPENER.3
    line(PW, "...I've done it again."), // JOKE: F1.OPENER.3
    line(PW, "The Long Dusk has been doing the same bit for years now. Nobody's laughing. It just keeps going. (ting!)"), // JOKE: F1.OPENER.4
    line(PW, '...Honestly? Respect.'), // JOKE: F1.OPENER.4
  ],
  // F2
  'npc.oldlight_heckler_block': [
    line('HECKLER', "OI! That tube's got a queue, and I'm it. Talk to ME first."), // DRAFT
  ],
  'npc.oldlight_heckler_after': [
    line('HECKLER', "(reads a card) 'THE HECKLER IS STILL SITTING DOWN.' ...I am, look. He thinks of everything."), // DRAFT
  ],
  'npc.oldlight_late_a': [line('AUDIENCE', '...HA! Oh — sorry, dear. That was for the fellow before you.')], // DRAFT
  'npc.oldlight_late_b': [line('AUDIENCE', "We're regulars. We laugh at everything. Eventually.")], // DRAFT
  'npc.oldlight_late_c': [line('AUDIENCE', '(a beat) (another beat) ...HA!')], // DRAFT
  'npc.oldlight_tube_2': [line(PW, '(the audience is still laughing at something from earlier) Lovely crowd. Late, but lovely.')], // DRAFT
  // F3
  'npc.oldlight_stove': [
    line('STOVE', 'HOO! HAA! HAHAHA! Why did the cheese-bun cross the kitchen?'), // JOKE: F3.STOVE
    line('STOVE', 'HAHAHAHA— TO GET TO MEEEE!'), // JOKE: F3.STOVE
    { text: '(Steam puffs from every hole the stove has. On the counter, a cheese-bun goes very quiet.)', style: 'narrate' }, // JOKE: F3.STOVE
  ],
  'npc.oldlight_bookcase': [line('BOOKCASE', "Ahem. AHEM. ...No, that's it. I just like clearing my throat.")], // DRAFT
  'sign.oldlight_p_note': [
    { text: 'A note tucked under the sugar bowl, in a spidery hand:', style: 'narrate' },
    { text: "\"Heard it. Laughed. Wasn't funny. Laughed anyway — somebody ought to. — p.\"" },
  ],
  'npc.oldlight_punch_tuesday': [
    line('TUESDAY', "I'm 'Because it was Tuesday.' I go in ALL of them, honestly."), // JOKE: F3.PUNCHLINES
    line('TUESDAY', "Wicks, kin, ferries. A Wednesday one, once. Didn't work."), // JOKE: F3.PUNCHLINES
  ],
  'npc.oldlight_punch_buns': [
    line('CHEESE-BUNS', "I'm 'Two cheese-buns and a bad play.' Don't think I'm from a joke, love."), // JOKE: F3.PUNCHLINES
    line('CHEESE-BUNS', "I think I'm somebody's perfect evening."), // JOKE: F3.PUNCHLINES
  ],
  'npc.oldlight_punch_ladder': [
    line('ONE RUNG', "I'm 'One rung at a time.' I belong to the lamplighter one."), // JOKE: F3.PUNCHLINES
    line('ONE RUNG', 'Fell off it, actually. Of all the jokes to fall off.'), // JOKE: F3.PUNCHLINES
  ],
  'npc.oldlight_tube_3': [line('THE MOUTH', '(contentedly) One rung at a time. One rung at a time.')], // DRAFT
  // F4
  'sign.oldlight_backwards_a': [{ text: '!NNI SDRAWKCAB EHT OT EMOCLEW' }], // DRAFT
  'sign.oldlight_backwards_b': [{ text: 'TUO GNIMOC ROF YLNO — NI YAW SIHT' }], // DRAFT
  'sign.oldlight_reassess': [
    { text: 'Carved into the bar, in a careful hand:', style: 'narrate' },
    { text: 'REASSESS. — p.' }, // JOKE: F4.RIDDLE (carving)
  ],
  'npc.oldlight_cart': [
    line(PW, "What has one bright eye and worries about every boat? A lighthouse. Lighthouses don't worry. They're buildings. HA. HA. HA."), // JOKE: F4.ANTI.4
    line(PW, '(pause) ...This one does, a bit.'), // JOKE: F4.ANTI.4
  ],
  'npc.oldlight_tube_4': [
    line(PW, "Backwards Inn rules: punchline FIRST. 'Taller.'"), // JOKE: F4.ANTI.2
    line(PW, "...What do you call a kin that's just kindled? (pause for laughter) (still pausing) (any moment now)"), // JOKE: F4.ANTI.2
  ],
  'npc.oldlight_ringmaster_block': [
    line('RINGMASTER', 'Ah-ah! Backwards Inn rules: you meet the Ringmaster LAST. Which means FIRST. Talk to me.'), // DRAFT
  ],
  'npc.oldlight_ringmaster_after': [
    line('RINGMASTER', "Arrived already? You've only just left! ...Eleven winters and I still can't tell which way round this place goes."), // DRAFT
  ],
  // F5
  'sign.oldlight_cap_reyl': [
    { text: 'PORTRAIT OF REYL WASH, AGED 9, AS A LIGHTHOUSE.' }, // JOKE: F5.GALLERY.1
    line(PW, 'Verified! I checked it against my source. My source is this painting.'), // JOKE: F5.GALLERY.1
  ],
  'sign.oldlight_cap_tuesday': [
    { text: 'A MAP OF TUESDAY.' }, // JOKE: F5.GALLERY.2
    line(PW, 'That IS a map of Tuesday. Look at all the Tuesday.'), // JOKE: F5.GALLERY.2
  ],
  'sign.oldlight_cap_stars': [
    { text: 'PICTURES OF VESPERHOLM FROM ABOVE THE STARS.' }, // JOKE: F5.GALLERY.3
    { text: '(Scratched underneath:) STILL FUNNY. — p.' }, // JOKE: F5.GALLERY.3
    line(PW, "Breathtaking, isn't it? You can see your house. It's the dark bit."), // JOKE: F5.GALLERY.3
  ],
  'sign.oldlight_cap_sea': [
    { text: 'THE SEA (SMALL).' }, // JOKE: F5.GALLERY.4
    line(PW, "That's all of it. Smaller than you'd think, isn't it? People exaggerate."), // JOKE: F5.GALLERY.4
  ],
  'sign.oldlight_cap_gerald': [
    { text: "KIN No. 0, 'GERALD'. DISCOVERED BY ME, JUST NOW." }, // JOKE: F5.GALLERY.5
    line(PW, 'Gerald is real. I can describe him in detail. Medium. Gerald-coloured. Mostly Gerald.'), // JOKE: F5.GALLERY.5
  ],
  'sign.oldlight_cap_tam': [
    { text: "TAM AND REYL WASH, FERRY 'SAME TIDE TOMORROW', THE NIGHT BEFORE THE FOG." }, // JOKE: F5.GALLERY.TRUE
  ],
  'npc.oldlight_tube_5': [
    line(PW, 'My cousin in the wood is never wrong. I am never right. Between us we are a perfectly average lamp.'), // JOKE: F5.COUSIN
  ],
  // F6
  'sign.oldlight_coat': [
    { text: 'Two coats on one peg. The blue one still has a reel of tinker\'s wire in the pocket.' }, // DRAFT
  ],
  'sign.oldlight_cups': [
    { text: 'Two cups on the table. One has been washed every day for a long time. The other has never been moved.' }, // DRAFT
  ],
  'sign.oldlight_window': [
    { text: "The window looks out across the harbour to the breakwater's end, where the moor-bell hangs silent." }, // DRAFT
  ],
  // TOP
  'sign.oldlight_rope': [
    { text: "An old bell-rope lies coiled on the sill. Its end isn't frayed. It's CUT — a net-knife's clean, straight line." },
  ],
  'npc.oldlight_punchwheel_after': [
    line(PW, "(ting.) I've started a NEW one. It's about a ferryman. It isn't finished yet. That's the good bit."), // DRAFT
  ],
  'sign.oldlight_slide_shut': [
    { text: 'A brass hatch in the floor, stencilled FOR AFTER THE ACT. It is firmly shut.' }, // DRAFT
  ],
};
