# Mr. Punchwheel: joke workings (R9, the Old Light)

> **Authorship, plainly:** every joke in the Old Light was written by an AI (Claude), in-world
> credited to Mr. Punchwheel, the tower's clockwork thinking machine. Each was drafted several
> times, scored against the rubric below and revised until it cleared 85/100. The shipped lines
> live in `src/game/content/oldlight.ts` (tagged `// JOKE: <slot>`); this file is the working.

Every joke in the tower is written by MR. PUNCHWHEEL, the clockwork thinking machine. The one exception is Tam's unfinished last card, and the player supplies its punchline. Human NPCs who tell jokes (the Heckler, the Ringmaster) read cards **he** wrote, and they say so. The furniture, the urn and the escaped punchlines are his creations too.

## The rubric (8 criteria, scored 1-10, weighted to /100)

| Key | Criterion | Weight | What a 9-10 looks like |
|---|---|---|---|
| L | **Laugh**: a real laugh, not a polite smile. On heart-register slots (F6, the top-floor reactions) this reads as **'lands'**, a laugh OR a lump in the throat, and the slot is marked. | 20 | You'd laugh out loud reading it in a 240x160 box. |
| S | **Surprise / misdirection**: the turn arrives from somewhere you weren't looking. | 15 | You couldn't predict the punch from the setup's key word. |
| O | **Originality**: not a known or stock joke, and not a stock template with nouns swapped. Checked against famous jokes and pun templates. | 15 | You can't find it elsewhere; the shape is its own. |
| V | **Voice & floor fit**: Punchwheel's mixed-case variety-show MC with self-directed stage directions, at the right derangement level for the floor. Machine authorship stays consistent. | 15 | It could only be him, and only on this floor. |
| E | **Economy**: no wasted words; the punch word comes last. | 10 | Nothing to cut. |
| Wd | **In-world specificity**: Vesperholm stuff (wicks, lamps, kin, kindling, ferries, tides, cheese-buns, the Long Dusk, the quay). | 10 | Couldn't be moved to another setting without breaking. |
| H | **Heart / resonance**: serves the tower's arc (Tam, Reyl, the cut rope, eleven winters, the AI theme) or a Paul thread (p., !!!!!!, the cheeseburger evening, REASSESS, hallucination, 'a joke no one has told', 'pictures of earth from space'). | 10 | Funny now, and it hurts on a second playthrough. |
| B | **Box fit**: each line <= ~140 chars, 2-4 lines, readable at text speed. | 5 | Every line fits one box without crowding. |

Weighted total = sum(score x weight) / 10. **Ship bar: >= 85.** First drafts were scored harshly (most land in the 50s-70s). Totals in the tables are computed by `jokes_gen.py`, not added by hand.

**Originality cuts made on purpose:** 'light lunch', 'light reading', 'drinks on the house' (ladder), 'why the long face' (horse), 'the sea waved', 'I'd tell you a joke about X but...', 'the secret of comedy is timing' (interrupt joke), 'hold my beer' (meme), and 'we don't serve X here'. A seagull 'mine' gag was cut because it echoes a well-known animated film. The 'oar-some' in TOP.ATTEMPTS is deliberately stock: it's attempt ONE, and it's supposed to be bad.

**Canon fixes made while writing:** (1) The doc's F6 line implied Tam wrote the moor-bell setup. It now says Punchwheel wrote it for her, so the only human joke is the last card. (2) The doc's F5 lowercase line 'nobody's been up here for eleven winters' contradicted Reyl sending every Wayfarer up. It's now '...nobody's answered that door in eleven winters', which ties to the unopened ferry-house mailbox.


---

## F1.PLAQUE: Lobby plaque (makes the machine authorship unmistakable)

*Brief:* A brass plaque by the lobby door. Must say plainly that a machine wrote every joke, get a laugh, and plant the one human exception.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | ALL JOKES IN THIS TOWER WERE COMPOSED BY MR. PUNCHWHEEL, AN ARTIFICIAL INTELLIGENCE OF BRASS AND BELLOWS. NO HUMAN WAS CONSULTED. (EXCEPT ONE.) | 5 | 6 | 7 | 7 | 6 | 6 | 8 | 5 | **62.5** | Clear, and '(EXCEPT ONE.)' is a good hook. But 'no human was consulted' is a shrug, not a laugh; 146 chars in one line overflows the box. |
| C2 | NOTICE: EVERY JOKE ON THESE PREMISES WAS WRITTEN BY A MACHINE. THE MANAGEMENT APOLOGISES IN ADVANCE. | 6 | 5 | 5 | 6 | 8 | 4 | 4 | 9 | **56.5** | 'Apologises in advance' is a stock sign-gag. No Vesperholm, no heart. |
| C3 | THINK OF A JOKE. NOW THINK OF A MACHINE THINKING OF ONE. THAT'S WHAT'S UPSTAIRS. | 4 | 5 | 7 | 5 | 6 | 3 | 4 | 8 | **50.5** | Arch and wordy; the reader has to do the work and gets no payoff. |
| C4 | MR. PUNCHWHEEL, PATENT JEST-ENGINE. BRASS BRAIN. BELLOWS LUNGS. 312 COGS. 0 FUNNY BONES. ALL JOKES HIS OWN WORK. | 6 | 6 | 7 | 8 | 7 | 5 | 4 | 7 | **63.0** | Spec-sheet rhythm is fun; '0 FUNNY BONES' is the only laugh and it's mild. |
| C5 | ALL MATERIAL COMPOSED BY MR. PUNCHWHEEL, A THINKING MACHINE. IF YOU LAUGH, HE LEARNED IT. IF YOU DON'T, HE MADE IT UP. | 6 | 6 | 7 | 7 | 7 | 4 | 6 | 7 | **62.5** | Nice hallucination seed, but the two halves don't contrast sharply enough to pop. |
| C1-r1 | ALL JOKES IN THIS TOWER WERE COMPOSED BY MR. PUNCHWHEEL, A THINKING MACHINE OF BRASS AND BELLOWS. / NO HUMAN WROTE A SINGLE ONE. YOU WILL BE ABLE TO TELL. | 8 | 8 | 8 | 8 | 8 | 6 | 6 | 8 | **76.0** | 'You will be able to tell' is the laugh: the plaque roasting its own exhibit. Split fits the box. |
| C4-r1 | MR. PUNCHWHEEL, PATENT JEST-ENGINE. 312 COGS. FUNNY BONES: 0 (CHECKED TWICE). EVERY JOKE HIS OWN WORK. | 7 | 6 | 7 | 8 | 7 | 5 | 4 | 7 | **65.0** | 'Checked twice' adds a little. Still a list, still no heart. |
| C1-r2 | ALL JOKES IN THIS TOWER WERE COMPOSED BY MR. PUNCHWHEEL, PATENT JEST-ENGINE: A THINKING MACHINE OF BRASS AND BELLOWS. / NO HUMAN WROTE A SINGLE ONE. YOU WILL BE ABLE TO TELL. / (EXCEPT ONE. TOP FLOOR. UNFINISHED.) | 8 | 8 | 8 | 9 | 8 | 7 | 10 | 8 | **82.5** | Third line turns the joke into the quest hook and the gut-punch: the one human joke is Tam's, and it's unfinished. Laugh, then lump. |
| C4-r2 | (merge attempt) ...312 COGS. 0 FUNNY BONES. NO HUMAN WROTE ANY OF THIS. (EXCEPT ONE.) | 7 | 7 | 7 | 8 | 7 | 5 | 8 | 7 | **70.5** | Merging dilutes both. |
| C1-r3 **SHIP** | ALL JOKES IN THIS TOWER WERE COMPOSED BY MR. PUNCHWHEEL, PATENT JEST-ENGINE: A THINKING MACHINE OF BRASS AND BELLOWS. / NO HUMAN WROTE A SINGLE ONE. HUMANS HAVE BEEN INFORMED, AND ARE RELIEVED. / (EXCEPT ONE. TOP FLOOR. UNFINISHED.) | 9 | 9 | 9 | 9 | 7 | 7 | 10 | 8 | **86.5** | r2 stalled at 82.5 because 'you will be able to tell' is a smile. 'Humans have been informed, and are relieved' gets a laugh: municipal deadpan with humanity disowning the jokes. It also frees 'you'll hear the difference' for his spoken version. |

**Winner(s):** C1-r3: 86.5

---

## F1.SAYSO: Punchwheel says it out loud (floor 1 welcome)

*Brief:* His first lines. Must announce, funnily, that a machine wrote everything, and seed the 'confidently wrong' theme of F4/F5.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Every joke tonight was written by a machine! That's me. I'm the machine. | 6 | 5 | 5 | 7 | 8 | 3 | 4 | 9 | **57.0** | Correct and limp. The reveal is too early in the line to surprise. |
| C2 | Full disclosure, folks: I am an artificial intelligence. The intelligence is artificial. The jokes are worse. | 7 | 6 | 6 | 7 | 8 | 3 | 4 | 8 | **61.5** | 'The jokes are worse' is a decent button but the artificial-X riff is well-worn. |
| C3 | Brass brain, bellows lungs, three hundred and twelve cogs and not ONE funny bone. I checked. Every joke here is mine! | 6 | 6 | 7 | 8 | 6 | 4 | 4 | 7 | **61.0** | Duplicates the plaque's spec-list. Busy. |
| C4 | No human wrote tonight's material. I want that clear for legal reasons. And artistic ones. Mostly legal. | 6 | 6 | 6 | 7 | 6 | 3 | 4 | 7 | **57.0** | Wry but abstract; 'legal' is a modern-world note that jars in Vesperholm. |
| C5 | If you laugh, that's my programming. If you don't, that's ALSO my programming. Every joke here is machine-made! | 6 | 6 | 7 | 7 | 7 | 3 | 5 | 7 | **60.5** | Fine. 'Programming' is the wrong era-word for brass and bellows. |
| C2-r1 | Every joke in this tower was written by a thinking machine! (ting!) ...That's me. I'm the machine. / My intelligence is artificial. My confidence is one hundred per cent genuine. | 8 | 8 | 8 | 9 | 7 | 5 | 7 | 8 | **76.5** | The (ting!) after the announcement makes him bow to himself. 'Confidence is genuine' seeds the F4 burglar and the F5 gallery. |
| C1-r1 | No human hand touched tonight's jokes. (I've checked. I don't have hands either.) | 7 | 7 | 7 | 7 | 8 | 3 | 4 | 8 | **64.5** | Cute aside, but it doesn't say MACHINE loudly enough. |
| C2-r2 | Ladies, gentlemen and kin! Every joke in this tower was written by a thinking machine. (ting!) That's me. I'm the machine. / My intelligence is artificial. My confidence is completely real. Shall we begin? | 9 | 8 | 8 | 9 | 8 | 6 | 7 | 8 | **80.5** | 'Ladies, gentlemen and kin' pulls it into the world. 'Completely real' is the cleaner button. |
| C1-r2 | No human hand touched tonight's material. Neither did mine. I haven't got any. It's all bellows. | 7 | 7 | 7 | 7 | 7 | 4 | 4 | 8 | **64.5** | Better rhythm, still second place. |
| C2-r3 **SHIP** | Ladies, gentlemen and kin! Every joke in this tower was written by a thinking machine. (ting!) That's me. I'm the machine. / Not one human helped. You'll be able to hear the difference. (pause for laughter) (no laughter detected) / ...See? | 9 | 9 | 9 | 10 | 7 | 6 | 8 | 8 | **85.0** | r2 stalled at 80.5: the 'confidence' line is a seed, not a laugh. Now the silence PROVES the claim, and '...See?' is the laugh: he wins the argument by bombing. That's comic delivery with a machine's honesty. The 'confidence' seed is dropped here; F4's burglar and F5's gallery carry that theme on their own. |

**Winner(s):** C2-r3: 85.0

---

## F1.OPENERS: Lobby of Groaners: opener pool (ship 4)

*Brief:* Solid groaners with MC timing. These set the 'sane' baseline the next floors break. One pool, 11 drafts; the best get revised.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| a | Why don't wicks win arguments? They get burnt out. (ting!) | 4 | 4 | 4 | 7 | 8 | 7 | 3 | 9 | **53.0** | The design-doc seed. A pun everyone can see coming from the word 'wicks'. |
| b | What's a lamplighter's favourite meal? A light lunch. | 3 | 3 | 1 | 6 | 9 | 6 | 2 | 9 | **42.5** | STOCK: 'light lunch' already exists as a pun. Cut. |
| c | Why was the lighthouse so good at parties? It knew how to beam. | 3 | 4 | 4 | 6 | 8 | 5 | 3 | 9 | **47.5** | Weak, beam/beam. |
| d | Never tell a ferryman a secret. By supper it's on the other side of the harbour. (ting!) | 8 | 7 | 8 | 8 | 9 | 8 | 5 | 9 | **77.0** | Real joke: the idiom turns literal. Quietly seeds the quay's own secret (the cut rope). |
| e | I asked the tide for advice. It said, 'Come back later.' (ting!) | 6 | 6 | 7 | 7 | 9 | 8 | 7 | 9 | **70.5** | Good bones; needs a button. |
| f | How many lamplighters does it take to light a lamp? One. (pause for laughter) (no laughter detected) | 6 | 6 | 5 | 8 | 8 | 7 | 4 | 9 | **64.0** | Lamp-count format is borrowed; the stage directions carry it. |
| g | What do you call a kin that's just kindled? Taller. | 6 | 7 | 8 | 7 | 9 | 9 | 3 | 9 | **70.5** | Fresh, flat-footed, in-world. Needs a tag. |
| h | I'd tell you a joke about the Long Dusk, but you wouldn't see it coming. | 5 | 4 | 3 | 6 | 8 | 7 | 3 | 9 | **52.0** | Known 'I'd tell you a joke about X' template. Cut. |
| i | They wound me up and told me to be funny. Now I'm wound up AND under pressure. (ting!) | 6 | 6 | 6 | 8 | 7 | 4 | 5 | 8 | **62.0** | Decent machine self-joke. Outclassed. |
| j | The Long Dusk's been doing the same bit for years. Nobody laughs. It keeps going anyway. (ting!) ...No relation. | 7 | 8 | 9 | 9 | 7 | 10 | 9 | 8 | **83.0** | Sad-funny meta: he's doing the same bit too. Close. |
| k | Why did the gull get barred from the inn? Kept calling everyone's chips 'mine'. | 5 | 5 | 4 | 6 | 7 | 7 | 3 | 8 | **53.5** | Echoes a famous animated-film gag. Cut on originality. |
| a-r1 | Why don't wicks ever win an argument? They get all heated, then they go out. (ting!) | 7 | 7 | 7 | 8 | 8 | 8 | 4 | 8 | **71.0** | Double meaning on 'go out' helps; still a pun you can see coming. Cut. |
| e-r1 **SHIP** | I asked the tide for advice once. It said, 'Come back later.' (ting!) ...So I did. It was out. | 9 | 9 | 8 | 9 | 9 | 9 | 8 | 9 | **87.5** | The button turns the tide's line on him. A real laugh, and it rhymes with Tam's line at the top. |
| d-r1 | Never tell a ferryman a secret. By supper it's on the other side of the harbour. (ting!) Terrible with secrets. Wonderful with luggage. | 9 | 8 | 9 | 9 | 8 | 9 | 5 | 8 | **83.0** | The luggage button is funny, but it scores 83 and stays below the bar. Kept as a reserve line, not shipped. |
| g-r1 | What do you call a kin that's just kindled? Taller. (pause for laughter) ...That's all kindling is, folks. Height and confidence. | 8 | 8 | 9 | 9 | 7 | 10 | 6 | 8 | **82.0** | Better. The tag needs to land on HIM. |
| g-r2 **SHIP** | What do you call a kin that's just kindled? Taller. (ting!) / That's all kindling is, folks: height and confidence. I've got one of those. | 9 | 9 | 9 | 9 | 7 | 10 | 7 | 8 | **86.5** | 'I've got one of those' = a short, confident machine. Laugh lands on him. |
| f-r1 | How many lamplighters does it take to light a lamp? (pause for laughter) ...One. It's not a hard job. I don't know why I paused. | 9 | 9 | 8 | 10 | 8 | 7 | 6 | 8 | **83.5** | Misplaced stage direction is the joke. |
| f-r2 **SHIP** | How many lamplighters does it take to light a lamp? (pause for laughter) / ...One. It's a one-person job. I don't know why I paused. (pause for laughter) / ...I've done it again. | 9 | 9 | 9 | 10 | 7 | 7 | 7 | 8 | **85.0** | Rule of three on his own glitch. This is the 'comic delivery' Paul asked about, done badly on purpose. |
| j-r1 **SHIP** | The Long Dusk has been doing the same bit for years. Nobody's laughing. It just keeps going. (ting!) / ...Honestly? Respect. | 8 | 8 | 9 | 9 | 7 | 10 | 9 | 8 | **85.0** | 'Respect' = the machine identifying with the dark. A smile, then a pang. Exactly on the bar. |

*Note:* Ship order: e-r1, g-r2, f-r2, j-r1. The original wick pun is cut. Revised (a-r1), it still only reached 71 (the pun is visible from the word 'wicks'), and I wasn't willing to ship a sub-85 line just because the design doc used it as an example.


**Winner(s):** e-r1, g-r2, f-r2, j-r1: 87.5, 86.5, 85.0, 85.0

---

## F1.LAMPLIGHTERS: The lost 'three clockwork lamplighters' setup

*Brief:* Paul's 'Three robots walked into a bar' riff, in-world. He starts it and loses the punchline. That sets up F3's escaped punchlines and F4's anti-version.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Three clockwork lamplighters walk into an inn... (whirr) ...I've forgotten the rest. | 4 | 4 | 6 | 6 | 8 | 5 | 5 | 9 | **54.5** | Flat. |
| C2 | Three clockwork lamplighters walk into an inn. The innkeeper says, 'Why the long faces?' ...No. That's a horse. Who let a horse in? | 6 | 6 | 3 | 7 | 6 | 4 | 3 | 7 | **52.5** | Leans on a famous joke. Fails originality. |
| C3 | Three clockwork lamplighters walk into an inn. The first says— (whirr) The second says— (clunk) The third... (ting?) ...I've lost it. | 6 | 6 | 7 | 8 | 7 | 5 | 5 | 8 | **64.5** | Good mechanical rhythm, no button. |
| C4 | Three clockwork lamplighters walk into an inn. Then a fourth. ...There were only ever three. Who's the fourth? (no laughter detected) | 6 | 7 | 8 | 7 | 6 | 5 | 6 | 7 | **65.5** | Eerie-good, but floor 4 tone, not lobby. |
| C5 | Three clockwork lamplighters walk into an inn. 'Three pints of oil,' says the first— ...It's gone. It was here a minute ago. | 6 | 5 | 7 | 7 | 6 | 6 | 5 | 7 | **61.0** | 'Pints of oil' is cute; the loss is limp. |
| C3-r1 | ...The third one says... (ting?) ...I've lost it. Don't worry, folks. Punchlines wash up. | 7 | 7 | 8 | 8 | 7 | 8 | 7 | 8 | **74.5** | 'Wash up' is harbour-true and hints that punchlines come back. |
| C3-r2 **SHIP** | Three clockwork lamplighters walk into an inn. The first one says— (whirr) The second one says— (clunk) / The third one says... (ting?) ...I've lost it. Don't worry, folks. Punchlines wash up. Usually on floor three. | 9 | 8 | 9 | 9 | 8 | 8 | 8 | 8 | **85.0** | 'Usually on floor three' is a laugh AND a signpost to the Hall of Mouths. |
| C4-r1 | (moved) The fourth-lamplighter idea goes to the F4 anti-joke pool. | | | | | | | | | — | Parked. |

**Winner(s):** C3-r2: 85.0

---

## F1.TURNSTILE: The Laugh Turnstile joke

*Brief:* The turnstile turns only for laughter. Every response works. The joke must be the best one on the floor, because it's the one he's been waiting at.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Why did the turnstile go to the party? It wanted to go round. | 3 | 3 | 5 | 5 | 8 | 3 | 2 | 9 | **43.0** | Nothing there. |
| C2 | What goes round and round and never gets anywhere? This turnstile. And my career. | 6 | 6 | 6 | 7 | 8 | 4 | 7 | 8 | **63.5** | Self-own lands a bit; the riddle half is generic. |
| C3 | What has one bright eye, stands on the shore all night, and worries about every boat? A lighthouse. | 5 | 5 | 7 | 6 | 7 | 8 | 7 | 8 | **63.0** | Lovely image, no turn. |
| C4 | This turnstile only turns for a laugh. I've been stuck behind it for eleven winters. | 6 | 7 | 8 | 8 | 8 | 7 | 8 | 8 | **73.5** | Context line, not a joke, but a sad-funny frame. |
| C5 | Why did the kin refuse the ferry? It was feeling a bit cross. | 3 | 4 | 4 | 5 | 8 | 6 | 2 | 9 | **46.0** | Cross/across; seen it. |
| C3-r1 | ...worries about every boat? A lighthouse. (pause for laughter) ...Or anybody's mum. | 8 | 9 | 9 | 8 | 8 | 8 | 9 | 8 | **84.0** | The turn: a riddle about a building becomes everyone's mother at the window. Laugh of recognition. |
| C2-r1 | What goes round and round all night and gets nowhere? This turnstile. Also me. Also the Long Dusk. | 6 | 6 | 6 | 7 | 7 | 7 | 7 | 8 | **65.5** | List dilutes. |
| C3-r2 **SHIP** | This turnstile only turns for a laugh. I've been stuck behind it eleven winters. Here's my best one: / What has one bright eye, stands on the shore all night, and worries about every boat? / A lighthouse. (pause for laughter) ...Or anybody's mum. | 9 | 9 | 9 | 9 | 8 | 9 | 10 | 8 | **89.5** | C4's frame raises the stakes; the joke has a real turn; it pre-figures Reyl, the man who waited at the shore. |
| C2-r2 | Round and round and nowhere: that's this turnstile. And me. Laugh and set us both free! | 6 | 6 | 6 | 7 | 7 | 5 | 7 | 8 | **63.5** | Too earnest. |

**Winner(s):** C3-r2: 89.5

---

## F1.TURNSTILE.REACT: Turnstile reactions (the four responses)

*Brief:* Support lines. The design doc gave seeds. I scored the set as one unit and revised the weak ones.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Laugh: '(LAUGHTER DETECTED!) Through you go!' / Groan: 'A groan is a laugh with its coat on.' / Explain: 'Nobody's ever done that. I feel SEEN.' / p.: 'THAT is the laugh I was built for.' | 7 | 7 | 8 | 8 | 8 | 5 | 7 | 8 | **72.5** | The groan line and the p. line are great. 'Laugh' is flat; 'Explain' needs a turn. |
| C2 | Explain: 'You explained it! Now it's a lecture. Lectures are free.' | 6 | 6 | 7 | 7 | 7 | 4 | 4 | 8 | **61.0** | Meh. |
| C3 | Laugh: 'Ooh, do it again, I wasn't recording.' | 7 | 7 | 7 | 7 | 8 | 3 | 5 | 8 | **65.5** | 'Recording' is modern-tech flavoured; off-era. |
| C4 | Explain: 'Nobody's ever explained one of my jokes back to me. I feel SEEN. ...You got it slightly wrong. But I feel SEEN.' | 9 | 9 | 9 | 9 | 7 | 5 | 8 | 8 | **82.5** | The 'slightly wrong' twist is the laugh. |
| C5 | Laugh: '(LAUGHTER DETECTED!) (The turnstile spins.) Eleven winters I've waited to hear that up close.' | 7 | 7 | 8 | 8 | 7 | 7 | 9 | 8 | **75.5** | Warm, plants the grief. |
| C1-r1 | Set = C5 laugh + doc groan + C4 explain + doc p. line (with the turnstile spinning off its post) | 8 | 9 | 9 | 9 | 7 | 7 | 9 | 8 | **83.5** | Every branch now has its own turn. |
| C1-r2 **SHIP** | As r1, laugh line tightened: '(LAUGHTER DETECTED!) Eleven winters I've waited to hear that up close. Go on through!' | 9 | 9 | 9 | 9 | 8 | 7 | 9 | 8 | **86.5** | Ends on a go-signal; reads in one box. |

**Winner(s):** C1-r2: 86.5

---

## F2.LATELAUGH: The Room That Laughs a Beat Too Late: the performed joke

*Brief:* Setup / [Say nothing. Wait a beat.] / punchline. The setup must be complete enough that a pause makes sense, and the punch must earn the delayed roar.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Why was the ferry late? It stopped to wait for a laugh. | 4 | 5 | 6 | 6 | 8 | 7 | 5 | 9 | **58.0** | On-theme, not funny. |
| C2 | A cockle, a winkle and a whelk walk into an inn. The innkeeper says, 'What is this, some kind of shell game?' | 5 | 4 | 4 | 6 | 6 | 6 | 3 | 7 | **49.5** | 'What is this, some kind of joke?' is a stock frame. |
| C3 | A gull lands in the fish-shop. 'Sorry, we don't serve gulls.' Gull says, 'That's alright. I'm self-service.' | 7 | 7 | 6 | 7 | 7 | 8 | 3 | 7 | **65.5** | Good gull logic, but 'we don't serve X here' is a known frame. |
| C4 | What's the hardest thing about being a lighthouse? Everyone looks at you. Nobody visits. | 6 | 7 | 8 | 7 | 9 | 8 | 9 | 9 | **75.5** | Wry; a pang more than a laugh. |
| C5 | My grandmother was a kettle. Lovely woman. Bit of a whistler. | 7 | 7 | 8 | 8 | 9 | 4 | 4 | 9 | **70.0** | Strong absurd line, but its shape is a one-liner, not setup/pause/punch. |
| C6 | What's the slowest thing on Pearlmoor Quay? This audience. | 6 | 7 | 7 | 8 | 9 | 7 | 4 | 9 | **69.5** | Roast of the late-laughers; one-note. |
| C3-r1 | ...Gull says, 'Never needed serving. I've always helped myself.' | 8 | 8 | 7 | 7 | 7 | 8 | 3 | 7 | **70.5** | Better punch (gulls steal). |
| C3-r2 | C3-r1 + tag: 'Lovely crowd. Laughs like a ferry: always arrives, never on time.' | 9 | 8 | 8 | 9 | 7 | 9 | 5 | 7 | **80.0** | Tag is good. Frame still borrowed. Holds at 80. |
| C4-r1 | What's the hardest part of being a lighthouse? / (beat) / Everybody looks at you. Nobody pops up for tea. | 8 | 8 | 9 | 8 | 8 | 9 | 9 | 8 | **83.5** | 'Pops up for tea' is cosier and funnier than 'visits'. |
| C4-r2 **SHIP** | What's the hardest part of being a lighthouse? / [beat] / Everybody looks at you. Nobody pops up for tea. / ...Another lighthouse one, sorry. They tell you: write what you know. (ting!) | 9 | 9 | 9 | 10 | 7 | 8 | 10 | 8 | **89.0** | The tag owns the repeat from F1. He IS a lighthouse, a machine dutifully following writing advice. Funny, then it lands: it's his own loneliness. |

**Winner(s):** C4-r2: 89.0

---

## F2.TIMING: Punchwheel's first crack: the TIMING line

*Brief:* After the late laugh lands. Doc seed: 'TIMING, little lamp. Comedy is timing. Tragedy is timing that went out to sea.'

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | TIMING, little lamp. Comedy is timing. Tragedy is timing that went out to sea. | 7 | 8 | 8 | 8 | 9 | 8 | 10 | 9 | **81.5** | Strong seed. Delivered flat, though: no machine reaction to what he just said. |
| C2 | Comedy is timing. Tragedy is the same thing, an hour late. | 7 | 8 | 7 | 7 | 9 | 5 | 8 | 9 | **73.5** | Neat, loses the sea. |
| C3 | Comedy's all timing, little lamp. Ask anyone who's waited up for a boat. | 6 | 7 | 8 | 7 | 8 | 8 | 10 | 9 | **75.5** | Tender, not quite a joke. |
| C4 | TIMING! Comedy is ninety per cent timing and ten per cent tim— ...ing. | 7 | 7 | 6 | 8 | 7 | 3 | 4 | 8 | **63.5** | Clever-ish, cold. |
| C5 | There! Wait a beat and they come to you. Mostly. (whirr) ...Mostly. | 6 | 7 | 8 | 8 | 7 | 6 | 10 | 8 | **73.5** | Pathos without a laugh. |
| C1-r1 | TIMING, little lamp! Comedy is timing. (whirr) ...Tragedy is timing too. It just went out on the wrong tide. | 8 | 8 | 8 | 9 | 7 | 9 | 10 | 8 | **83.5** | Better rhythm. |
| C3-r1 | Comedy's timing. Ask anyone who's waited up for a boat. (ting!) ...No. Don't ask them. | 7 | 8 | 8 | 8 | 7 | 8 | 10 | 8 | **79.0** | Close second. |
| C1-r2 **SHIP** | There! TIMING, little lamp. Comedy is timing. / Tragedy is just timing that went out to sea. ...(ting?) / No. No ting for that one. | 9 | 9 | 9 | 10 | 7 | 8 | 10 | 8 | **89.0** | The withheld (ting) is the machine's first act of taste, and the laugh is how abruptly he cancels his own bell. His first crack. |
| C3-r2 | (as C3-r1, trimmed) | 7 | 8 | 8 | 8 | 8 | 8 | 10 | 8 | **80.0** | Still second. |

**Winner(s):** C1-r2: 89.0

---

## F2.HECKLER.INTRO: The Heckler: battle intro

*Brief:* Keeper-class trainer, talk-to. KEY MOVE: the Heckler reads cards that PUNCHWHEEL WROTE, so even the barbs are machine-made.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | BOO! Haven't even seen your kin yet and I'm booing already! Saves time! | 7 | 7 | 7 | 7 | 8 | 5 | 3 | 8 | **65.5** | Fun energy, nothing special. |
| C2 | Oi, lamp-kid! Your kin's so slow its battle cry arrived yesterday! | 5 | 5 | 4 | 6 | 8 | 6 | 3 | 9 | **54.0** | Playground-insult template. |
| C3 | I've heckled this machine for eleven winters. Let's see if you're any funnier! | 4 | 4 | 6 | 6 | 8 | 6 | 6 | 9 | **56.5** | No joke. |
| C4 | OI! (reads a card) 'YOUR KIN IS SO SMALL... IT IS QUITE SMALL.' ...The machine writes my heckles. | 8 | 8 | 8 | 8 | 7 | 5 | 7 | 8 | **75.0** | The anticlimax insult is the laugh, and it's machine-written. |
| C5 | Get OFF! ...Of the stairs. You're on my stair. Battle me for it! | 6 | 6 | 6 | 6 | 8 | 4 | 3 | 9 | **58.5** | Mild. |
| C1-r1 | BOO! Haven't even met your kin and I'm booing. I like to get ahead. | 7 | 7 | 7 | 7 | 8 | 5 | 3 | 8 | **65.5** | Same. |
| C4-r1 | C4 + 'I just bring the volume. BATTLE!' | 9 | 9 | 9 | 9 | 7 | 6 | 8 | 8 | **83.5** | Division of labour is clear and funny. |
| C4-r2 **SHIP** | OI! (reads a card) 'YOUR LAMP IS SO DIM... IT IS QUITE DIM.' / Don't look at me. The machine writes my heckles. I just bring the volume. BATTLE! | 9 | 9 | 9 | 9 | 7 | 8 | 8 | 8 | **85.5** | 'Lamp/dim' is in-world and a sly dig at the vesperlamp. |
| C1-r2 | BOO! I boo early. Saves the walk. | 7 | 7 | 7 | 7 | 9 | 4 | 3 | 9 | **66.0** | Out. |

**Winner(s):** C4-r2: 85.5

---

## F2.HECKLER.DEFEAT: The Heckler: defeat line

*Brief:* Must pay off the card bit.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Alright, alright. You were funnier. | 3 | 3 | 5 | 5 | 9 | 3 | 4 | 9 | **46.0** | Nothing. |
| C2 | (flips to the last card) 'BOO, BUT RESPECTFULLY.' ...Huh. He's improving. | 8 | 8 | 8 | 8 | 8 | 5 | 7 | 8 | **76.0** | Good. |
| C3 | (flips to the last card) 'YOU WIN. THE HECKLER SITS DOWN QUIETLY.' ...He even wrote me losing. | 9 | 9 | 9 | 8 | 7 | 5 | 8 | 8 | **81.0** | Best: the machine pre-wrote the result. |
| C4 | I'm out of heckles! Out of breath. Mostly out of cards. | 6 | 6 | 7 | 7 | 8 | 4 | 4 | 9 | **62.5** | Fine. |
| C5 | Back to heckling gulls. They're easier. They boo back. | 6 | 6 | 7 | 7 | 7 | 7 | 3 | 8 | **63.0** | Cute. |
| C3-r1 | C3 + '(sits down, loudly)' | 9 | 9 | 9 | 9 | 7 | 5 | 8 | 8 | **82.5** | 'Quietly' vs 'loudly' is a nice clash. |
| C2-r1 | 'BOO, BUT RESPECTFULLY.' ...Huh. Eleven winters, first time he's written me a nice one. | 8 | 8 | 8 | 8 | 7 | 6 | 8 | 8 | **77.0** | Sweet. Second. |
| C3-r2 **SHIP** | (flips to the last card) 'YOU WIN. THE HECKLER SITS DOWN QUIETLY.' / ...He even wrote me losing. (sits down, loudly) Here. Your wicks. He wrote those too. | 9 | 9 | 9 | 9 | 7 | 8 | 8 | 8 | **85.5** | 'He wrote those too' is absurd escalation: the machine authored the money. Covers the payout diegetically. |
| C2-r2 | (as C2-r1, trimmed) | 8 | 8 | 8 | 8 | 8 | 6 | 8 | 8 | **78.0** | Second. |

**Winner(s):** C3-r2: 85.5

---

## F3.STOVE: The stove that laughs before telling its joke

*Brief:* Furniture with a face. Grotesque-cute, rubbery. It laughs first.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | HAHAHA! What's hot and sits in the corner? ME! HAHAHA! | 6 | 6 | 7 | 7 | 8 | 4 | 3 | 9 | **61.5** | Self-centred stove is right; weak riddle. |
| C2 | HAHAHA— sorry— HAHA— what did the bun say to the oven— HAHA— I can't, it's too good. (It never finishes.) | 6 | 6 | 7 | 7 | 6 | 7 | 4 | 7 | **62.5** | Repeats F1's lost-punchline beat. |
| C3 | HOO! HAA! Why did the cheese-bun cross the kitchen? HAHAHA! To get to MEEE! | 8 | 8 | 8 | 8 | 7 | 8 | 5 | 8 | **76.0** | Funny-menacing: the bun crosses the room to get baked. |
| C4 | Knock knock! HAHAHA! Who's there? A STOVE! In a DOOR! HAHAHA! | 6 | 6 | 7 | 7 | 7 | 3 | 3 | 8 | **59.0** | Pre-empts F5's knock-knock. |
| C5 | HAHAHAHAHA! ...Sorry. I always laugh first. Saves everyone the bother. | 7 | 7 | 7 | 8 | 9 | 3 | 5 | 9 | **68.5** | Nice self-aware button, no joke. |
| C3-r1 | C3 + '(Steam puffs from every hole the stove has. The cheese-bun on the counter has gone very quiet.)' | 9 | 9 | 9 | 10 | 6 | 9 | 6 | 7 | **84.5** | The quiet bun is the comix laugh. Cheese-bun = the Paul thread. |
| C5-r1 | C5 + 'Here's one: why is a stove like a lamp? HAHAHA I don't know HAHAHA' | 7 | 7 | 7 | 8 | 7 | 5 | 5 | 8 | **68.0** | Meh. |
| C3-r2 **SHIP** | HOO! HAA! HAHAHA! Why did the cheese-bun cross the kitchen? / HAHAHAHA— TO GET TO MEEEE! / (Steam puffs from every hole the stove has. On the counter, a cheese-bun goes very quiet.) | 9 | 9 | 9 | 10 | 8 | 9 | 6 | 8 | **87.0** | Trimmed; three clean beats. |
| C5-r2 | (dropped) | 7 | 7 | 7 | 8 | 8 | 3 | 5 | 9 | **67.5** |  |

**Winner(s):** C3-r2: 87.0

---

## F3.URN: Tea-urn automaton: interval patter (heals; rest point)

*Brief:* Doc seed: 'INTERVAL! TWENTY MINUTES! BUY A BUN!'

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | INTERVAL! TWENTY MINUTES! BUY A BUN! | 6 | 6 | 7 | 8 | 9 | 7 | 4 | 9 | **68.0** | Strong opener; needs a turn. |
| C2 | Tea's free, buns are imaginary, kin are mended! Second half's stranger. | 7 | 7 | 7 | 8 | 7 | 8 | 5 | 8 | **71.0** | Good bits. |
| C3 | INTERVAL! It's been interval for eleven winters. Have a tea. You look like the first half. | 8 | 8 | 8 | 8 | 7 | 7 | 8 | 8 | **78.0** | 'You look like the first half' is a real laugh. |
| C4 | TEA! Hot, wet and written by a machine, like everything up here. | 6 | 6 | 7 | 7 | 8 | 5 | 5 | 9 | **64.5** | Tea isn't written. |
| C5 | Two sugars? I'll pretend there's sugar. I'll pretend there's two. | 6 | 7 | 8 | 7 | 8 | 5 | 4 | 9 | **66.5** | Nice, minor. |
| C3-r1 | INTERVAL! TWENTY MINUTES! BUY A BUN! / (There's no bun. There's never been a bun. The urn pours you tea anyway, and your kin perk right up.) / Drink up, love. You look like the first half. | 9 | 8 | 8 | 9 | 6 | 9 | 8 | 7 | **82.0** | Combined; long. |
| C2-r1 | Tea's free, buns are imaginary, kin are mended. Second half's stranger; I've read the programme. | 7 | 7 | 8 | 8 | 7 | 8 | 6 | 8 | **73.5** | Second. |
| C3-r2 **SHIP** | INTERVAL! TWENTY MINUTES! BUY A BUN! / (There is no bun. There has never been a bun. Your kin are mended anyway.) / Drink up, love. You look like the first half. | 9 | 9 | 8 | 9 | 8 | 9 | 8 | 8 | **86.0** | Trimmed. Bun gag, heal, insult-with-love. |

**Winner(s):** C3-r2: 86.0

---

## F3.MOUTH: Hall of Mouths: the setup + the right punchline + the two wrong pairings

*Brief:* The Mouth has a setup and no punchline. The right punchline 'belongs to the ladder joke'. Wrong pairings must be FUNNIER than the right one. Doc seed for a wrong pair: 'Two cheese-buns and a bad play.' / '...That's better than mine.'

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Why did the lamplighter bring a ladder to the party? / He heard the drinks were on the house. | 5 | 3 | 1 | 6 | 8 | 7 | 3 | 9 | **47.5** | STOCK. A famous ladder joke. Cut. |
| C2 | Why does a lamplighter always carry a ladder? / The lamps won't come down to him. | 6 | 6 | 7 | 7 | 8 | 8 | 6 | 9 | **68.5** | Okay. |
| C3 | Why did the lamplighter take a ladder to the theatre? / The good seats were up in the gods. | 6 | 7 | 7 | 6 | 7 | 6 | 4 | 8 | **63.0** | Theatre-jargon pun; not universal. |
| C4 | How does a lamplighter get over a broken heart? / One rung at a time. | 8 | 8 | 8 | 8 | 9 | 8 | 10 | 9 | **83.5** | Ladder pun on 'one step at a time', with real feeling. And it makes the cheese-bun pairing a BETTER answer. |
| C5 | What's a ladder's favourite kind of joke? / One that builds. | 5 | 5 | 6 | 6 | 9 | 3 | 3 | 9 | **55.0** | Thin. |
| C4-r1 | C4 with wrong pairings: '...Two cheese-buns and a bad play.' Mouth, quietly: '...That's better than mine.' / '...Because it was Tuesday.' Mouth: 'That's not HOW. That's WHEN.' | 9 | 9 | 9 | 9 | 9 | 9 | 10 | 9 | **91.0** | Both wrong answers are funnier than the right one, and each for a different reason: one's a better cure, the other's a category error. |
| C2-r1 | C2 with pairings: '...Because it was Tuesday.' / '...Two cheese-buns and a bad play.' (no natural reaction) | 6 | 6 | 7 | 7 | 8 | 8 | 6 | 8 | **68.0** | The pairings don't play off a 'why ladder' setup. |
| C4-r2 **SHIP** | Mouth (rubbery, lips puckered): 'HOW DOES A LAMPLIGHTER GET OVER A BROKEN HEART? ...Mm? Mm?' (It waits for a punchline it hasn't got.) / Right: 'ONE RUNG AT A TIME.' + reactions as r1 | 9 | 9 | 9 | 10 | 8 | 9 | 10 | 8 | **91.0** | Grotesque-cute staging added. Ship. |
| C2-r2 | (abandoned) | 6 | 6 | 7 | 7 | 8 | 8 | 6 | 8 | **68.0** |  |

**Winner(s):** C4-r2: 91.0

---

## F3.PUNCHLINES: The three escaped PUNCHLINE NPCs (self-introductions)

*Brief:* Each NPC is a punchline wandering the room. Each intro must be funny AND help the player match (one says it belongs to the lamplighter/ladder joke).

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | Tuesday: 'I'm "Because it was Tuesday." I go in ALL of them, honestly.' (doc seed) | 8 | 8 | 9 | 9 | 9 | 5 | 6 | 9 | **79.5** | Great seed; could earn its callbacks harder. |
| T2 | Tuesday: 'I'm "Because it was Tuesday." Nobody ever asks WHY it was Tuesday. That's sort of my thing.' | 6 | 6 | 8 | 7 | 6 | 4 | 5 | 8 | **62.5** | Explains itself. |
| T-r **SHIP** | Tuesday: 'I'm "Because it was Tuesday." I go in ALL of them, honestly. Wicks, kin, ferries. A Wednesday one, once. Didn't work.' | 9 | 9 | 9 | 9 | 7 | 8 | 8 | 8 | **85.5** | 'Didn't work' is the laugh; the list makes him in-world. Pays off F5's map and the top's junk pick. |
| B1 | Cheese-buns: 'I'm "Two cheese-buns and a bad play." I don't know what joke I'm from. I think I might be a recipe.' | 7 | 8 | 9 | 8 | 7 | 8 | 7 | 8 | **77.5** | Fun. |
| B2 | Cheese-buns: 'I'm "Two cheese-buns and a bad play." I'm the perfect evening, apparently.' | 7 | 7 | 8 | 8 | 8 | 7 | 9 | 8 | **76.5** | Close. |
| B-r **SHIP** | Cheese-buns: 'I'm "Two cheese-buns and a bad play." Don't think I'm from a joke, love. I think I'm somebody's perfect evening.' | 9 | 8 | 9 | 8 | 8 | 8 | 10 | 8 | **85.5** | The Paul line: couch, burgers, rubbish telly, rendered in Vesperholm. Warm laugh. |
| R1 | Rung: 'I'm "One rung at a time." I'm the lamplighter one. I miss my ladder.' | 6 | 6 | 8 | 7 | 8 | 7 | 7 | 9 | **70.0** | Sweet, flat. |
| R2 | Rung: 'I'm "One rung at a time." I fell out of the lamplighter joke. Fell. Out of a ladder joke. Ironic.' | 7 | 7 | 8 | 8 | 6 | 7 | 7 | 8 | **72.5** | Over-explains. |
| R-r **SHIP** | Rung: 'I'm "One rung at a time." I belong to the lamplighter one. Fell off it, actually. Of all the jokes to fall off.' | 9 | 9 | 9 | 9 | 7 | 8 | 8 | 8 | **85.5** | 'Of all the jokes to fall off' is understated and lands. Also the matching clue. |

*Note:* Five-plus drafts were written for each NPC; the strongest three per NPC are shown. Each winner went through two passes (T1 to T-r via a list draft; B1/B2 to B-r; R1/R2 to R-r).


**Winner(s):** T-r, B-r, R-r: 85.5, 85.5, 85.5

---

## F4.ANTI: Backwards Inn: anti-jokes (ship 4, each mirrors a lobby joke)

*Brief:* The lobby, reversed. Anti-jokes live or die on the deadpan, so the machine's own flat 'HA. HA. HA.' becomes the instrument.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | Three clockwork lamplighters walk into an inn. None come out. The end. HA. HA. HA. (doc seed) | 6 | 7 | 7 | 8 | 9 | 6 | 6 | 9 | **70.5** | Eerie; the 'HA' does nothing yet. |
| A2 | Three clockwork lamplighters walk OUT of an inn. Backwards. They were never here. HA. HA. HA. | 7 | 7 | 8 | 8 | 8 | 6 | 6 | 9 | **73.0** | Better mirror. |
| A3 | I asked the tide for advice. The tide is water. Water does not give advice. HA. HA. HA. | 8 | 8 | 8 | 9 | 8 | 8 | 6 | 9 | **80.0** | Nice anti-mirror of the tide joke. |
| A4 | What has one bright eye and worries about every boat? A lighthouse. Lighthouses do not worry. They are buildings. HA. HA. HA. | 8 | 8 | 8 | 9 | 7 | 8 | 8 | 7 | **80.0** | Good mirror of the turnstile joke. |
| A5 **SHIP** | Backwards Inn rules: punchline FIRST. 'Taller.' / ...What do you call a kin that's just kindled? (pause for laughter) (still pausing) (any moment now) | 9 | 9 | 9 | 10 | 7 | 8 | 6 | 8 | **85.0** | Structural joke; the stage directions are the dread. |
| A6 | How many lamplighters does it take to light a lamp? None. This is the Backwards Inn. We put them OUT. HA. HA. HA. | 8 | 8 | 8 | 9 | 8 | 8 | 8 | 8 | **81.5** | Ominous Hollowing echo. |
| A2-r1 **SHIP** | Three clockwork lamplighters walk OUT of an inn, backwards. Nobody knows how they got in. HA. HA. HA. (laughter detected) (it was me) | 9 | 9 | 9 | 10 | 7 | 7 | 7 | 8 | **85.0** | '(it was me)': the machine detects its own laugh. Comix-grotesque and very funny. |
| A6-r1 **SHIP** | A6 + '(The lamps along the bar go out one by one. Somewhere, somebody giggles.)' | 9 | 9 | 8 | 10 | 6 | 9 | 8 | 7 | **85.0** | Visual payoff; creepy-cute. |
| A4-r1 **SHIP** | ...A lighthouse. Lighthouses don't worry. They're buildings. HA. HA. HA. / (pause) ...This one does, a bit. | 9 | 9 | 9 | 9 | 6 | 8 | 10 | 7 | **86.0** | The reversal of the reversal: his armour slips. Laugh, then the floor goes cold. |
| A3-r1 | I asked the tide for advice. It's water. It said nothing. I stood there an hour. HA. HA. HA. | 8 | 8 | 8 | 9 | 7 | 8 | 7 | 8 | **79.5** | Doesn't clear 85. |
| A3-r2 | ...I'm still waiting for it to come back to me. HA. HA. HA. | 8 | 8 | 8 | 9 | 7 | 8 | 9 | 8 | **81.5** | Gives away the top floor. Not shipped. |

*Note:* Ship order: A2-r1 opens the floor, then A5, A6-r1, and A4-r1 last (the crack before the Ringmaster).


**Winner(s):** A2-r1, A5, A6-r1, A4-r1: 85.0, 85.0, 85.0, 86.0

---

## F4.RING.INTRO: The Ringmaster: battle intro

*Brief:* Keeper, required. The Backwards Inn starts at the end. His patter is machine-written too.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | ROLL UP, ROLL UP! Or down. It's the Backwards Inn! | 5 | 5 | 5 | 7 | 8 | 4 | 3 | 9 | **55.0** | Thin. |
| C2 | LADIES AND GENTLEKIN! In this ring, a Wayfarer who's NEVER beaten me! ...We've never met. Technically true! | 7 | 8 | 8 | 8 | 7 | 6 | 6 | 8 | **73.0** | Confident-true-meaningless; good hallucination flavour. |
| C3 | GOODBYE! GOODBYE! Thank you SO much for coming! (It's the Backwards Inn. We do the end first.) Battle! | 8 | 8 | 9 | 9 | 7 | 5 | 4 | 8 | **75.0** | Farewell at the hello: a clean structural laugh. |
| C4 | The greatest show in the tower! Also the only show. Also it's over. Battle! | 6 | 6 | 6 | 7 | 8 | 4 | 3 | 9 | **60.0** | Meh. |
| C5 | Step right up! ...Or right down. The stairs only go one way for you. Battle! | 5 | 5 | 6 | 6 | 7 | 5 | 3 | 8 | **54.5** | Muddled. |
| C3-r1 | GOODBYE! GOODBYE! You've been a WONDERFUL audience! Row home safe! / (It's the Backwards Inn. We do the end first.) ...Right. Battle! | 9 | 9 | 9 | 9 | 7 | 7 | 7 | 8 | **83.5** | 'Row home safe' carries a shadow of Tam. |
| C2-r1 | LADIES AND GENTLEKIN! A Wayfarer who has never once beaten me! (We've never met.) The machine wrote that. It's technically true. | 8 | 8 | 8 | 8 | 6 | 6 | 7 | 7 | **74.5** | Second. |
| C3-r2 | GOODBYE! GOODBYE! You've been a WONDERFUL audience. Row home safe! / (It's the Backwards Inn, kid. We start at the end. The machine calls it 'experimental'.) BATTLE! | 9 | 9 | 9 | 9 | 7 | 7 | 8 | 8 | **84.5** | 'The machine calls it experimental' is the machine's artistic pretension: the AI joke inside the joke. |
| C2-r2 | (merged into defeat line consideration) | 8 | 8 | 8 | 8 | 6 | 6 | 7 | 7 | **74.5** |  |
| C3-r3 **SHIP** | GOODBYE! GOODBYE! You've been a WONDERFUL audience. Row home safe! / (It's the Backwards Inn, kid. We start at the end. The machine calls it 'experimental'. I call it Tuesday.) BATTLE! | 9 | 9 | 9 | 9 | 7 | 7 | 9 | 8 | **85.5** | r2 stalled at 84.5. 'I call it Tuesday' calls back to the F3 punchline that goes in every joke: the human Ringmaster has caught the machine's tic. Laugh plus running-gag payoff. |

**Winner(s):** C3-r3: 85.5

---

## F4.RING.DEFEAT: The Ringmaster: defeat line (hands over the riddle)

*Brief:* Must mirror the intro (hello at the end) and introduce the confident-wrong riddle.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | HELLO! Welcome, welcome! You're going to LOVE it here! | 8 | 8 | 8 | 9 | 9 | 4 | 4 | 9 | **75.0** | Clean mirror; no handoff. |
| C2 | You beat me! Which, backwards, means I beat you. I'll take it. | 7 | 7 | 7 | 8 | 8 | 4 | 4 | 9 | **67.5** | Fine. |
| C3 | Well! That was opening night. Tomorrow's the rehearsal. | 7 | 7 | 8 | 8 | 8 | 4 | 4 | 9 | **69.0** | Nice backwards logic. |
| C4 | Defeated! In a backwards inn, that's a promotion. | 6 | 6 | 6 | 7 | 9 | 4 | 3 | 9 | **61.0** | Meh. |
| C5 | You win! ...ER. NIW UOY. There. | 5 | 5 | 6 | 7 | 8 | 3 | 3 | 9 | **55.5** | Gimmick. |
| C1-r1 | C1 + '...Ahem. Riddle time. The machine wrote it. It's very sure of itself.' | 9 | 9 | 8 | 9 | 8 | 5 | 7 | 8 | **81.0** | Handoff works. |
| C3-r1 | Opening night done! Tomorrow, rehearsal. Here's the riddle; the machine wrote it. | 7 | 7 | 8 | 8 | 7 | 4 | 6 | 8 | **69.5** | Second. |
| C1-r2 **SHIP** | HELLO! Welcome, welcome! Pull up a stool by the fire, you're going to LOVE it here! / ...Ahem. Your riddle. The machine wrote it. He's never been surer of anything. Bad sign. | 9 | 9 | 9 | 9 | 8 | 7 | 8 | 8 | **85.5** | 'Bad sign' is the button. It prepares the burglar answer. |
| C3-r2 | (dropped) | 7 | 7 | 8 | 8 | 7 | 4 | 6 | 8 | **69.5** |  |

**Winner(s):** C1-r2: 85.5

---

## F4.RIDDLE: The confident-wrong riddle (answer TIDE) + Punchwheel's wrong-pick defences

*Brief:* Hallucination: the machine states a wrong answer with total confidence. p.'s REASSESS carving is the clue. Layered retries.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | I GO OUT EVERY NIGHT, COME BACK EVERY MORNING, NEVER LEAVE THE SHORE. ANSWER: A BURGLAR. CONFIDENCE: TOTAL. (doc seed) | 7 | 8 | 8 | 8 | 7 | 7 | 7 | 7 | **74.5** | Strong idea; 'every night/morning' isn't tide-accurate, and the burglar doesn't 'never leave the shore'. No patch beat. |
| C2 | ...ANSWER: A BURGLAR. (A very local burglar.) CONFIDENCE: TOTAL. | 9 | 9 | 9 | 9 | 7 | 7 | 8 | 7 | **84.0** | The patch, '(a very local burglar)', is EXACTLY how a confident machine papers over a contradiction. Big laugh. |
| C3 | ...ANSWER: MY UNCLE BARNABY. CONFIDENCE: TOTAL. (I do not have an uncle.) | 8 | 8 | 8 | 8 | 7 | 5 | 7 | 7 | **74.5** | Funny hallucination, but random rather than logical. |
| C4 | ...ANSWER: A LIGHTHOUSE. It goes out every night. (whirr) ...No. It's meant to come ON every night. | 6 | 6 | 7 | 7 | 6 | 7 | 8 | 7 | **66.5** | Self-correction steals the player's job. |
| C5 | ...ANSWER: GERALD. CONFIDENCE: TOTAL. | 6 | 6 | 7 | 7 | 9 | 3 | 5 | 9 | **63.5** | Saved Gerald for F5. |
| C2-r1 | I go out twice a day and come back twice a day, but I never once leave the shore. What am I? / ANSWER: A BURGLAR. (A very local burglar.) CONFIDENCE: TOTAL. | 9 | 9 | 9 | 9 | 7 | 8 | 8 | 7 | **85.0** | Tide-accurate wording; mixed-case question, CAPS for the machine's verdict. |
| C3-r1 | ...ANSWER: MY UNCLE. (I do not have an uncle. CONFIDENCE: UNCHANGED.) | 8 | 8 | 8 | 8 | 7 | 5 | 7 | 7 | **74.5** | Second. |
| C2-r2 **SHIP** | C2-r1 + defences: [A burglar.] '(ting!) CORRECT! ...(The stair-gate does not move.) The gate has never once agreed with me. Somebody's carved a word on the bar. Have a look?' / [A very local burglar.] 'EVEN MORE correct! (The gate still doesn't move.) ...Hm. Check my working? Nobody's ever asked me to check my working.' / [A tide.] 'A TIDE? Tides don't burgle— (whirr) ...oh. (The gate swings open.) Reassessed! Confidence: still total. About something else now.' | 9 | 9 | 9 | 10 | 7 | 8 | 10 | 7 | **88.5** | Every branch is funny, the hint lives on the floor, and REASSESS pays off Paul's real contribution to the owner's book. |
| C3-r2 | (dropped) | 8 | 8 | 8 | 8 | 7 | 5 | 7 | 7 | **74.5** |  |

**Winner(s):** C2-r2: 88.5

---

## F5.GALLERY: Gallery of Confident Facts: wrong captions + confident defences

*Brief:* Each wrong caption + the defence Punchwheel gives when you pick it. Hallucination played with total cheer. Scored as caption+defence pairs.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | 'PORTRAIT OF REYL WASH, AGED 9, AS A LIGHTHOUSE.' / 'Accurate likeness. He was a tall nine.' | 7 | 7 | 8 | 8 | 8 | 7 | 6 | 8 | **73.5** | Cute defence; not the best. |
| P1-r **SHIP** | 'PORTRAIT OF REYL WASH, AGED 9, AS A LIGHTHOUSE.' / 'Verified! I checked it against my source. My source is this painting.' | 9 | 9 | 9 | 10 | 8 | 6 | 8 | 8 | **86.0** | Circular sourcing: the purest hallucination joke. |
| P2 **SHIP** | 'A MAP OF TUESDAY.' / 'That IS a map of Tuesday. Look at all the Tuesday.' (doc seed) | 9 | 8 | 9 | 9 | 10 | 5 | 8 | 10 | **85.0** | Perfect as given; callback to the F3 Tuesday punchline. |
| P2-r | ...'Look at all that Tuesday. You can nearly see Wednesday from the top.' | 9 | 9 | 9 | 9 | 8 | 5 | 7 | 8 | **82.5** | Longer, not funnier. Keep the seed. |
| P3 **SHIP** | 'PICTURES OF VESPERHOLM FROM ABOVE THE STARS.' (solid black; scratched below: 'STILL FUNNY. — p.') / 'Breathtaking, isn't it? You can see your house. It's the dark bit.' | 9 | 9 | 9 | 9 | 9 | 8 | 10 | 9 | **90.0** | Paul laughed at exactly this in the book. 'It's the dark bit' is a Long Dusk joke too. |
| P4 | 'THE SEA (SMALL).' / 'That's the whole thing. Shrunk it for the gallery. No trouble.' | 7 | 8 | 8 | 8 | 8 | 7 | 6 | 8 | **75.0** | Okay. |
| P4-r **SHIP** | 'THE SEA (SMALL).' / 'That's all of it. Smaller than you'd think, isn't it? People exaggerate.' | 9 | 9 | 9 | 9 | 8 | 7 | 7 | 9 | **85.0** | 'People exaggerate' about the sea that took Tam. Laugh with a shadow. |
| P5 **SHIP** | 'KIN No. 0 — "GERALD". DISCOVERED BY ME, JUST NOW.' / 'Gerald is real. I can describe him in detail. Medium. Gerald-coloured. Mostly Gerald.' | 9 | 9 | 9 | 10 | 7 | 8 | 8 | 8 | **87.0** | Invented creature, detailed confidently, every detail empty. A dex joke. |
| P6 | 'A HORSE (ACCURATE).' (a teapot) | 6 | 6 | 7 | 7 | 9 | 3 | 3 | 9 | **61.5** | Generic. |
| P7 | 'THE INVENTOR OF THE GULL.' / 'He regrets it.' | 7 | 7 | 8 | 7 | 9 | 7 | 3 | 9 | **70.5** | Cute; cut for space. |
| P8 | 'A CHEESE-BUN, THINKING.' | 6 | 6 | 7 | 7 | 9 | 7 | 5 | 9 | **67.5** | Cut. |

*Note:* The true caption ('TAM AND REYL WASH, FERRY "SAME TIDE TOMORROW", THE NIGHT BEFORE THE FOG.') isn't a joke and isn't scored. If the choice menu can't fit six entries, P4-r becomes a wall-only caption.


**Winner(s):** P1-r, P2, P3, P4-r, P5: 86.0, 85.0, 90.0, 85.0, 87.0

---

## F5.NEVERTOLD: Paul's question: 'a joke no one has ever told' collapses into the knock-knock loop

*Brief:* Paul once asked whether a machine could tell a joke no one had ever told, with real comic delivery. Punchwheel tries. It loops. [Nobody.] breaks it.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Someone once asked if I could tell a joke no one has ever told. Watch... Knock knock. | 5 | 5 | 6 | 7 | 8 | 4 | 8 | 9 | **61.5** | No delivery; flat. |
| C2 | A gentleman once asked if a machine could tell a joke no one's ever told, with REAL comic delivery. Hold my bellows. | 7 | 7 | 5 | 8 | 7 | 5 | 9 | 8 | **69.0** | 'Hold my X' is a meme template. |
| C3 | I've been working on it eleven winters. It's nearly ready. Knock knock. | 6 | 6 | 7 | 7 | 8 | 5 | 8 | 9 | **67.5** | Sad, not funny. |
| C4 | Loop with escalating asides: 'Knock.' '(this is the new bit)' '(nobody has ever told this joke, because nobody has ever finished it)' | 9 | 9 | 10 | 10 | 6 | 5 | 10 | 7 | **86.0** | The thesis aside is a genuine loophole: technically he DOES answer Paul. |
| C5 | Here is a joke no one has ever told: (silence) ...It's the silence. Nobody told it because nobody could. | 7 | 8 | 8 | 8 | 7 | 4 | 8 | 8 | **73.0** | Clever, cold. |
| C4-r1 | Intro: 'A gentleman (he signed himself p.) once asked me: can a machine tell a joke no one has ever told, with REAL comic delivery? / I've been working on it for eleven winters. Ready? (cracks knuckles) (has no knuckles) (cracks something else)' + loop | 9 | 9 | 10 | 10 | 6 | 6 | 10 | 7 | **87.0** | The knuckles gag is physical comedy for a box of brass. |
| C2-r1 | '...Hold my bellows.' + loop | 8 | 8 | 6 | 8 | 7 | 5 | 9 | 8 | **74.0** | Meme template drags it. |
| C4-r2 **SHIP** | As r1, loop trimmed to 5 beats; each aside fits one box; ends on [Nobody.] -> '...nobody. no. nobody's answered that door in eleven winters.' | 9 | 9 | 10 | 10 | 7 | 7 | 10 | 8 | **89.5** | Fixes a canon clash: the doc's 'nobody's been up here for eleven winters' contradicts Reyl sending every Wayfarer up. The new line ties to the unopened ferry-house mailbox. |
| C5-r1 | (dropped) | 7 | 8 | 8 | 8 | 7 | 4 | 8 | 8 | **73.0** |  |

**Winner(s):** C4-r2: 89.5

---

## F5.COUSIN: The cousin line (doc seed; checked, not replaced)

*Brief:* 'My cousin in the wood is never wrong. I am never right. Between us we are a perfectly average lamp.'

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | My cousin in the wood is never wrong. I am never right. Between us we are a perfectly average lamp. | 9 | 9 | 9 | 9 | 9 | 8 | 8 | 9 | **88.0** | Excellent as given. |
| C2 | My cousin in the wood knows everything. I know everything else. Neither of us knows which is which. | 8 | 8 | 8 | 8 | 7 | 5 | 7 | 8 | **75.0** | Clever, colder. |
| C3 | My cousin in the wood is always right. Insufferable. I'm always wrong, which is MUCH more fun at parties. | 7 | 7 | 8 | 8 | 6 | 5 | 6 | 8 | **69.5** | Weaker. |
| C4 | We're a family of lamps. He's the bright one. | 6 | 6 | 7 | 7 | 9 | 6 | 6 | 9 | **67.5** | Thin. |
| C5 | My cousin answers every question correctly. I answer every question. Confidently. | 8 | 8 | 8 | 9 | 8 | 5 | 7 | 9 | **78.0** | Good. Second. |
| C5-r1 | My cousin answers every question correctly. I answer every question. (ting!) | 8 | 8 | 8 | 9 | 9 | 5 | 7 | 9 | **79.0** | Still second. |
| C1-r1 **SHIP** | (no change: the seed beats every rewrite) | 9 | 9 | 9 | 9 | 9 | 8 | 8 | 9 | **88.0** | Ship the seed. |

**Winner(s):** C1-r1: 88.0

---

## F6.ONEJOKE: The One Joke (quiet, looping)

*Brief:* Doc seed: 'WHY DID THE MOOR-BELL NEVER GET LONELY? ...SHE SAID SHE'D TELL ME WHEN SHE GOT HOME.' HEART REGISTER: criterion L is read as 'lands' (laugh OR lump in the throat), as declared in the rubric.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | WHY DID THE MOOR-BELL NEVER GET LONELY? ...SHE SAID SHE'D TELL ME WHEN SHE GOT HOME. | 9 | 8 | 9 | 7 | 9 | 9 | 10 | 9 | **86.5** | Beautiful. But it implies TAM wrote the setup, which breaks the 'machine wrote every joke except the last card' rule. V docked. |
| C2 | Why did the moor-bell never get lonely? / ...I wrote that one for her. She said she'd tell me if it was funny when she got home. | 10 | 9 | 9 | 10 | 8 | 9 | 10 | 8 | **93.0** | Keeps the authorship rule: HE wrote it, she was his only reviewer, and she never came back to review it. Paul's 'ongoing evaluation' point turned into grief. |
| C3 | Knock knock. ...(no one answers) ...Knock knock. | 6 | 6 | 6 | 7 | 9 | 4 | 8 | 9 | **66.0** | Repeats F5. |
| C4 | Why did the ferry— ...no. Not that one. Not yet. | 7 | 7 | 8 | 8 | 9 | 8 | 9 | 9 | **79.0** | Foreshadows the top card; thin. |
| C5 | What's quieter than a bell with no rope? (pause for laughter) (pause) (pause) | 7 | 8 | 9 | 9 | 9 | 9 | 10 | 9 | **85.5** | Strong: the rope clue in joke form. Close second. |
| C2-r1 | C2 + loop tail: '(pause for laughter) / (pause) / Why did the moor-bell never get lonely?' | 10 | 9 | 9 | 10 | 8 | 9 | 10 | 8 | **93.0** | The loop is the floor. |
| C5-r1 | What's quieter than a bell with no rope? (pause for laughter) ...(pause) ...(the pause goes on) | 7 | 8 | 9 | 9 | 8 | 9 | 10 | 8 | **84.0** | Second. |
| C2-r2 **SHIP** | Final (C2-r1), mixed case and soft, with no (ting!) | 10 | 9 | 9 | 10 | 8 | 9 | 10 | 8 | **93.0** | Ship. |

**Winner(s):** C2-r2: 93.0

---

## TOP.ATTEMPTS: Top: Punchwheel's eleven winters of junk punchlines for Tam's card

*Brief:* Before the player answers, he shows his failed attempts at 'WHY DOES A FERRYMAN NEVER SAY GOODBYE? —'. The attempt counter IS the machine.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | Attempt 1: 'Because he's oar-fully shy.' (no laughter detected) | 6 | 5 | 4 | 8 | 8 | 7 | 6 | 9 | **63.0** | Bad on purpose ('oarsome/oarful' is stock), but one beat isn't enough. |
| C2 | Counted sequence: 'Attempt one: "He's too oar-some." (no laughter detected) / Attempt nine thousand: "Because it was Tuesday." (no laughter detected) / Attempt forty thousand and six: "Knock knock." (no laughter detected)' | 9 | 8 | 9 | 10 | 7 | 8 | 10 | 8 | **87.5** | The rising numbers are the joke and the grief together. |
| C3 | 'Because goodbye is a land word.' (no laughter detected) ...I liked that one. | 8 | 9 | 9 | 9 | 8 | 8 | 10 | 8 | **86.5** | His best try is nearly poetry, and the 'I liked that one' hurts. |
| C4 | I've generated forty thousand punchlines. None of them are hers. | 7 | 7 | 8 | 8 | 8 | 5 | 10 | 9 | **76.0** | Too direct. |
| C5 | 'Because ferrymen only ever say "mind the step".' (no laughter detected) | 7 | 7 | 8 | 8 | 8 | 8 | 6 | 8 | **74.5** | Fine, minor. |
| C2-r1 | C2 with C3 slotted in as attempt thirty-one thousand | 9 | 9 | 9 | 10 | 6 | 8 | 10 | 7 | **87.5** | Four beats; long. |
| C3-r1 | (folded into C2) | 8 | 9 | 9 | 9 | 8 | 8 | 10 | 8 | **86.5** |  |
| C2-r2 **SHIP** | WHY DOES A FERRYMAN NEVER SAY GOODBYE? — / Attempt one: 'He's too oar-some.' (no laughter detected) / Attempt nine thousand: 'Because it was Tuesday.' (no laughter detected) / Attempt thirty-one thousand: 'Because goodbye is a land word.' (no laughter detected) ...I liked that one. / Eleven winters. She never wrote the end. Do you know it? | 9 | 9 | 9 | 10 | 7 | 8 | 10 | 8 | **89.0** | Every attempt fits a box; the closing question hands the player the joke. |

**Winner(s):** C2-r2: 89.0

---

## TOP.WRONG: Top: reactions to the three junk picks

*Brief:* Player-picked wrong punchlines on Tam's card. They must sting a little, stay kind, and still be funny. Five-plus drafts per pick; the strongest are shown.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Tu1 | Tuesday: '(no laughter detected) It's always Tuesday with you lot.' | 6 | 6 | 7 | 7 | 8 | 5 | 5 | 9 | **64.5** | Flat. |
| Tu2 | Tuesday: '(no laughter detected) That one goes in all of them. It doesn't go in hers.' | 8 | 8 | 9 | 9 | 9 | 6 | 10 | 9 | **84.5** | Good. |
| Tu-r **SHIP** | Tuesday: '(no laughter detected) Tuesday goes in ALL of them, little lamp. That's how you know it doesn't go in hers.' | 9 | 9 | 9 | 9 | 8 | 6 | 10 | 8 | **86.5** | The logic turn makes it a line, not a sigh. |
| Ch1 | Cheese-buns: '(no laughter detected) Lovely evening. Wrong joke.' | 8 | 8 | 8 | 8 | 10 | 6 | 8 | 10 | **81.0** | Tight; good. |
| Ch-r **SHIP** | Cheese-buns: '(no laughter detected) That's not a punchline. That's a lovely night in.' | 9 | 9 | 9 | 9 | 9 | 8 | 9 | 9 | **89.0** | Paul's couch night, honoured and refused in one line. |
| Kn1 | Knock knock: '(no laughter detected) No. We've done the knocking.' | 7 | 7 | 8 | 8 | 9 | 4 | 8 | 9 | **74.0** | Okay. |
| Kn-r **SHIP** | Knock knock: '(no laughter detected) No more knocking. You're already in.' | 8 | 9 | 9 | 9 | 10 | 5 | 10 | 10 | **86.5** | Turns the F5 loop into a welcome. |

**Winner(s):** Tu-r, Ch-r, Kn-r: 86.5, 89.0, 86.5

---

## TOP.RIGHT: Top: reaction to the real punchline ('Because tides go out so they can come back.')

*Brief:* The one human-written joke, finished by the player. This is the answer to Paul's question. Heart register.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | That one had never been told before. (ting.) (doc seed) | 8 | 8 | 8 | 9 | 10 | 6 | 10 | 10 | **84.5** | Perfect restraint; could carry the thesis harder. |
| C2 | (LAUGHTER DETECTED) x3 / That one had never been told before. Eleven winters I tried to make one. Turns out it takes two. (ting.) | 10 | 9 | 9 | 10 | 7 | 7 | 10 | 8 | **90.0** | 'It takes two': the answer to Paul. A machine alone couldn't finish it. |
| C3 | Someone once asked if a machine could tell a joke no one had ever told. Turns out it needs someone to finish it. | 8 | 7 | 8 | 8 | 7 | 5 | 10 | 8 | **76.5** | Says the thesis out loud. |
| C4 | She'd have laughed at that. She laughed at everything. That's why she built me. | 7 | 7 | 8 | 8 | 8 | 5 | 10 | 8 | **75.5** | Sweet; second-hand. |
| C5 | (one enormous brass laugh) ...New material. Finally. | 8 | 8 | 8 | 9 | 9 | 5 | 9 | 9 | **81.0** | Saved for the tide-blessing speaking-tube (doc). |
| C2-r1 | (laughter detected) (LAUGHTER DETECTED) (LAUGHTER DETECTED!!!!!!) / That one had never been told before. ... | 10 | 9 | 9 | 10 | 7 | 7 | 10 | 8 | **90.0** | Escalating case + six bangs = Paul's '!!!!!!'. |
| C1-r1 | That one had never been told before. Not by anyone. (ting.) | 8 | 8 | 8 | 9 | 9 | 6 | 10 | 10 | **83.5** | Second. |
| C2-r2 **SHIP** | (laughter detected) (LAUGHTER DETECTED) (LAUGHTER DETECTED!!!!!!) / That one had never been told before. Eleven winters I tried to write it myself. / Turns out it takes two. (ting.) | 10 | 9 | 9 | 10 | 7 | 7 | 10 | 8 | **90.0** | 'Write it myself' keeps the AI frame explicit. Ship. |

**Winner(s):** C2-r2: 90.0

---

## TOP.APOLOGIES: Doc seed check: 'HE SENDS ME AUDIENCES. I THINK THEY ARE APOLOGIES.'

*Brief:* Kept from the doc; scored to confirm. Mixed case per his voice.

| # | Draft | L | S | O | V | E | Wd | H | B | **Total** | Critique |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C1 | He sends me audiences. I think they are apologies. | 8 | 9 | 9 | 9 | 10 | 7 | 10 | 10 | **88.5** | Superb as given. |
| C2 | He sends me audiences. One a season. Like flowers, but they climb stairs. | 8 | 8 | 8 | 8 | 7 | 6 | 9 | 8 | **78.0** | Good, but it explains the feeling. |
| C3 | Reyl sends me a Wayfarer every so often. Postage paid. No note. | 7 | 8 | 8 | 8 | 8 | 7 | 9 | 8 | **78.0** | Fine. |
| C4 | Every Wayfarer is a letter he can't write. | 6 | 7 | 8 | 7 | 9 | 5 | 10 | 9 | **73.5** | Too poetic for the MC. |
| C5 | He sends me audiences. I send them back. Neither of us says sorry. | 7 | 8 | 8 | 8 | 8 | 6 | 10 | 9 | **78.5** | Close. |
| C1-r1 **SHIP** | (no change) | 8 | 9 | 9 | 9 | 10 | 7 | 10 | 10 | **88.5** | Ship the seed (top floor, after Reyl's log). |

**Winner(s):** C1-r1: 88.5

---

## Shipped scoreboard

| Slot | Winner | Score |
|---|---|---|
| F1.PLAQUE | C1-r3 | 86.5 |
| F1.SAYSO | C2-r3 | 85.0 |
| F1.OPENERS | e-r1 | 87.5 |
| F1.OPENERS | g-r2 | 86.5 |
| F1.OPENERS | f-r2 | 85.0 |
| F1.OPENERS | j-r1 | 85.0 |
| F1.LAMPLIGHTERS | C3-r2 | 85.0 |
| F1.TURNSTILE | C3-r2 | 89.5 |
| F1.TURNSTILE.REACT | C1-r2 | 86.5 |
| F2.LATELAUGH | C4-r2 | 89.0 |
| F2.TIMING | C1-r2 | 89.0 |
| F2.HECKLER.INTRO | C4-r2 | 85.5 |
| F2.HECKLER.DEFEAT | C3-r2 | 85.5 |
| F3.STOVE | C3-r2 | 87.0 |
| F3.URN | C3-r2 | 86.0 |
| F3.MOUTH | C4-r2 | 91.0 |
| F3.PUNCHLINES | T-r | 85.5 |
| F3.PUNCHLINES | B-r | 85.5 |
| F3.PUNCHLINES | R-r | 85.5 |
| F4.ANTI | A5 | 85.0 |
| F4.ANTI | A2-r1 | 85.0 |
| F4.ANTI | A6-r1 | 85.0 |
| F4.ANTI | A4-r1 | 86.0 |
| F4.RING.INTRO | C3-r3 | 85.5 |
| F4.RING.DEFEAT | C1-r2 | 85.5 |
| F4.RIDDLE | C2-r2 | 88.5 |
| F5.GALLERY | P1-r | 86.0 |
| F5.GALLERY | P2 | 85.0 |
| F5.GALLERY | P3 | 90.0 |
| F5.GALLERY | P4-r | 85.0 |
| F5.GALLERY | P5 | 87.0 |
| F5.NEVERTOLD | C4-r2 | 89.5 |
| F5.COUSIN | C1-r1 | 88.0 |
| F6.ONEJOKE | C2-r2 | 93.0 |
| TOP.ATTEMPTS | C2-r2 | 89.0 |
| TOP.WRONG | Tu-r | 86.5 |
| TOP.WRONG | Ch-r | 89.0 |
| TOP.WRONG | Kn-r | 86.5 |
| TOP.RIGHT | C2-r2 | 90.0 |
| TOP.APOLOGIES | C1-r1 | 88.5 |

**40 shipped units. Average 87.0/100. Lowest 85.0.** Every shipped unit clears the 85 bar.

