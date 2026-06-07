# PixelKin — Music Direction: *2–3 options for every area & route*

> The auditionable soundtrack plan for **Vesperholm — "The Long Dusk."** For
> **every world-map area and route**, this gives **2–3 distinct music options**,
> each a ready-to-build **[`generate-midi`](../../.claude/skills/generate-midi/SKILL.md)**
> brief. It expands the single per-area brief in [`atlas.md`](./atlas.md) into a
> set of real choices, all grounded in each place's mood, element, and setting.
>
> **Read first:** the score's *why* and its cohesion rules live in the skill's
> **[`pixelkin-soundtrack.md`](../../.claude/skills/generate-midi/references/pixelkin-soundtrack.md)**
> (the PixelKin score bible) — the Vesper motif, the per-element sonic
> signatures, the voice/era policy, and the dusk→dawn key arc that keep all of
> these briefs sounding like *one composer wrote them*. All music is **original**
> per [`../../VISION.md`](../../VISION.md): inspired by the cartridge-era handheld
> monster-RPG soundtracks, a copy of nothing.

---

## How to read each entry

Every area/route lists **2–3 options** — different *valid readings of the same
place*, not three drafts of one idea — so the team can build, listen, and pick:

- **Option A — Anchor:** the canonical reading; matches the `atlas.md` brief. Build this first.
- **Option B — Mood sibling:** a different emotional lean (more melancholy vs more playful; sparser vs warmer; a different meter).
- **Option C — Diegetic/structural variant:** a relit/brightened version, a post-dawn day-form, a festival, a sparser "explore-light" ambient take, or a richer `gba`/`snes` register for a big moment.

Each option is a `generate-midi` brief — *preset · era · tempo, meter, key/mood ·
lead / harmony-arp / bass / percussion · loop length* — plus its **concept**, its
**Vesper-motif** treatment, and the **GBC nod** (the era function it echoes,
originally). The cohesion shorthand (the Vesper motif, the light signatures, the
voice palette, the dawn arc) is defined once in the score bible linked above.

> **Production order:** a first pass builds **one loop per area from its Option A**;
> B/C are generated when a place wants auditioning. Battle, Lumenary (arena), and
> victory/level-up stings are **shared cross-region cues** — scored once, reused.

---

## South region — *the blue-hour start (wistful major)*

### 1 · Tinderwick — *the candle-lit cradle of the whole score*
*Town · south · Ember + Light · a lullaby sung over a sleeping sea — hopeful, a little homesick.*

**Option A — "Lantern Lullaby" (anchor).**
`generate-midi` brief: *preset `town` · era `gbc` · 92 BPM, 4/4, C major with a wistful turn to A minor in the answer phrase · **lead:** soft `pulse25`, full slow statement of the Vesper motif (G3→C4→D4 lift … E4→D4→C4 settle), legato, breathing rests between phrases · **harmony/arp:** `pulse12` slow "music-box" broken-chord arpeggio (C–E–G, then A–C–E under the minor turn), low gain, sparkly · **bass:** `tri_bass` a warm rocking root–fifth "hearth" pulse, two notes per bar, never busy · **percussion:** `drums` almost absent — a single soft noise "tick" on bar downbeats, like a clock by the fire · loop body 16 bars (~28s).*
- **Concept:** The canonical reading and the literal source theme of the game. AABA-leaning: state the motif tender and bare, repeat it, then the A-minor answer is the homesick catch in the throat before it resolves home. This is the melody every later town variation is measured against.
- **Vesper motif:** First and most naked statement in the whole score — slow, tender, exactly as written. Everything downstream is a transform of these four bars.
- **GBC nod:** The town-theme function — gentle, warm, mid-tempo, front-loaded hook in bars 1–2 so the constant loop point reads as "home."

**Option B — "Embers Banked Low" (mood sibling).**
`generate-midi` brief: *preset `town` · era `gbc` · 80 BPM, 6/8, A minor leaning to its relative C major only at the very last bar · **lead:** `pulse25` plays the Vesper contour but contracted — the hopeful leap undershoots and lingers, more sigh than lift · **harmony/arp:** `pulse12` slow rolling 6/8 arpeggio, fewer notes, more air between them · **bass:** `tri_bass` gentle dotted lilt on the compound pulse, like slow breathing · **percussion:** none, or one felt brush at phrase ends · loop body 16 bars (~32s).*
- **Concept:** The melancholy lean — same cottages, later at night, fire burned down to coals. The 6/8 sway and minor home make it the more homesick reading for a quiet/rainy variant or a reflective story beat, without losing the lullaby's warmth.
- **Vesper motif:** Same contour, transformed minor and contracted — the lift "doesn't quite reach the sky," which is the whole melancholy thesis of the dawn arc's starting point.
- **GBC nod:** The minor-tinted town reprise trick — same leitmotif, recoloured by mode and meter so the place can feel two ways without a new tune.

**Option C — "First Light on the Water" (explore-light / Light-leaning ambient).**
`generate-midi` brief: *preset `town` · era `gbc` · 88 BPM, 4/4, C Lydian-tinted major (raised 4th for wonder) · **lead:** sparse `pulse25`, only the motif's lift fragment (G3→C4→D4) answered by silence — fewer notes than Option A · **harmony/arp:** `pulse12` bright bell-timbre ascending sparkle figures (the Light signature) glinting like candle-windows on the sea · **bass:** `tri_bass` very slow sustained roots, almost a drone · **percussion:** a single soft noise shimmer at the loop seam · loop body 16 bars (~26s).*
- **Concept:** A pared-back, Light-forward ambient take for first-arrival wandering or menus over the title sea — leans the Light element (bell sparkle) more than the Ember warmth, so the player feels the blue-hour wonder before the full lullaby earns its place.
- **Vesper motif:** Only the rising-lift half is stated, left unanswered — it "asks the question" the rest of the game (and Dawnstead) will answer.
- **GBC nod:** The sparse, hook-fragment ambient loop — a town theme reduced to its motto so it never tires across long, slow exploration.

### 2 · Dimglass Coast — *the road that teaches you to wander*
*Route · south · Tide + Light · the first open path — airy, optimistic, lanterns strung along the dark water.*

**Option A — "Lanterns Along the Tide" (anchor).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 120 BPM, 4/4, G major (relative-major neighbour to Tinderwick's C/A-minor world) · **lead:** `pulse25` wandering walking-pace melody that bounces the Vesper contour — the hopeful leap now springy and onward-leaning · **harmony/arp:** `pulse12` quick Tide-bell-buoy arpeggios, chiming offbeats like buoys passing · **bass:** `tri_bass` steady rocking root–fifth "gentle wave" bass, propulsive but soft-edged · **percussion:** `drums` light noise pattern shaped like lapping foam — soft kick on 1 & 3, a brushy "wash" hat, a small fill at the loop seam · loop body 24 bars (~32s).*
- **Concept:** The canonical signature travel theme — brisk, optimistic "let's-go" energy, the very first feeling of freedom. ABAC walking form with the hook front-loaded so the constant loop reads instantly as "the road."
- **Vesper motif:** The route's job — it *bounces* the motif: same contour, faster and rhythmically perky, turning the lullaby's tender lift into a stride.
- **GBC nod:** The signature route leitmotif — short, hummable, propulsive, the tune you associate forever with "leaving the start town."

**Option B — "Salt Wind, Last Light" (mood sibling).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 112 BPM, 4/4, E minor (relative minor of the anchor's G) · **lead:** `pulse25` the same wandering line but wistful — longer held notes, the leap reaching out over the dark water rather than skipping · **harmony/arp:** `pulse12` slower, airier Tide arpeggios with more gaps · **bass:** `tri_bass` a deeper, more rolling wave swell · **percussion:** sparser foam-wash noise, no fills — just tide · loop body 24 bars (~34s).*
- **Concept:** The pensive lean — same cliffside, but the melancholy of a long road at dusk, the sea going dark. Slightly slower and minor for a windier/lonelier stretch or a story-tinged first crossing, keeping the travel pulse but trading optimism for awe.
- **Vesper motif:** Contour intact in minor, the lift stretched and yearning — a sibling to Tinderwick's "Embers Banked Low" so town and route share the same homesick color.
- **GBC nod:** The relative-minor variant of an established route tune — the cartridge trick for one road feeling brighter or lonelier by mode alone.

**Option C — "Buoy-Light Drift" (sparser explore-light ambient).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 104 BPM, 4/4, G major, Light-leaning · **lead:** thin `pulse25` stating only the motif's lift fragment, widely spaced, answered by bell sparkle · **harmony/arp:** `pulse12` bright ascending bell figures (Light signature) over slow Tide chimes · **bass:** `tri_bass` slow sustained roots, drifting · **percussion:** a single soft foam-wash brush per bar · loop body 16 bars (~28s).*
- **Concept:** A becalmed, low-stimulus take for fishing, shore-spur exploration (Gullcry Rock / Tideglass Cavern), or quiet backtracking — the same road with the engine idling, leaning the Light element through bell sparkle.
- **Vesper motif:** Lift-fragment only, drifting and unhurried — the route's hook reduced to a glint so it never fatigues during slow play.
- **GBC nod:** The "calm version" of a route loop — same identity, thinned for long stretches without encounters.

### 3 · Pearlmoor Quay — *a waltz on wet boardwalks under a cyan moon*
*Town · south · Tide + Light · cosy, salt-aired, lilting — lantern-strings swaying between the masts.*

**Option A — "Moonlit Quay Waltz" (anchor).**
`generate-midi` brief: *preset `town` · era `gbc` · 100 BPM, 3/4, F major (warm, a comfortable neighbour to the south's keys) · **lead:** `pulse25` accordion-flavoured lilting waltz melody, the Vesper contour reshaped to swing on the downbeat-and-lift of 3/4 · **harmony/arp:** `pulse12` Tide bell-buoy chimes on beats 2 & 3, the rocking "oom-pah-pah" upper voice · **bass:** `tri_bass` classic waltz bass — root on 1, gentle rocking fifths on 2 & 3, like a moored hull · **percussion:** `drums` soft noise brush only on beat 1, the boardwalk creak · loop body 24 bars (~43s at 3/4).*
- **Concept:** The canonical reading — the 3/4 accordion lilt is the town's whole identity. The Tide signature (compound/triple meter + bell-buoy chimes + rocking bass) is fully foregrounded; warm, salt-aired, unmistakably this port.
- **Vesper motif:** Stated as a waltz — the rising lift lands on the downbeat of a new bar, the settle sways back over beats 2–3. Same four-note spine, dressed for a dockside dance.
- **GBC nod:** The town leitmotif as a meter-flip — a place defined by *how* it moves (the waltz) as much as by its tune.

**Option B — "Low Tide, Lantern Strings" (mood sibling).**
`generate-midi` brief: *preset `town` · era `gbc` · 92 BPM, 3/4, D minor (relative minor of the anchor's F) · **lead:** `pulse25` the same waltz line, slower and bare, the accordion lilt now a lonely sway · **harmony/arp:** `pulse12` sparse bell-buoy chimes ringing into the gaps · **bass:** `tri_bass` slower rocking waltz bass, deeper, like a tide gone out · **percussion:** none — just the creak of empty boards implied by space · loop body 24 bars (~47s).*
- **Concept:** The melancholy lean — the quay late and near-empty, moon high, most lanterns dimmed. Same waltz, minor and slowed, for a night/closing-time variant or a quiet character beat on the docks.
- **Vesper motif:** The waltz contour in minor, the lift hesitant — a sibling sadness to Tinderwick B and Dimglass B, tying the whole south region into one wistful blue-hour family.
- **GBC nod:** The relative-minor town reprise — the cosy theme recoloured lonely without writing a second tune.

**Option C — "Festival of the Floating Lights" (festival variant).**
`generate-midi` brief: *preset `town` · era `gbc` · 116 BPM, 3/4, F major, bright · **lead:** lively `pulse25` waltz, the motif ornamented with quick grace-note runs, celebratory · **harmony/arp:** `pulse12` busier Tide bell-buoy chimes plus bright Light sparkle on phrase ends, more festive ring · **bass:** `tri_bass` bouncier waltz bass with a little anticipation into beat 1 · **percussion:** `drums` light noise brush on 1 with a cheerful tambourine-style hat on 2 & 3, a fill at the seam · loop body 24 bars (~37s).*
- **Concept:** A brighter, faster festival take — the same waltz lit up for a lantern-festival event or a relit-Tide-constellation celebration, leaning both Tide (chimes) and Light (sparkle) for payoff energy without leaving the GBC band.
- **Vesper motif:** The waltz contour ornamented and quickened — the town's hook in its happiest dress, a small step up the dawn-arc's brightness ladder.
- **GBC nod:** The event/festival reskin of a town theme — same melody, more voices busy, the classic "the town is celebrating" version.

---

## East region — *wonder & discovery (modal colour)*

### 4 · Saltreach Fen — *a slow drift through reed shallows where mist breathes and water laps*
*Route · east · Tide · cosy-melancholy wandering, lanterns floating on dark water.*

**Option A — "Reedwalk Lull" (anchor).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 104 BPM, 4/4, gentle D natural minor · **lead:** breathy woodwind-flavoured `pulse25` line, long-held notes with soft turns, leaving rests for the water to answer · **harmony/arp:** slow `pulse12` rocking two-note figure (root–fifth) imitating lapping water, never busy · **bass:** `tri_bass` gentle rocking root-fifth, soft on-beat sway · **percussion:** very sparse `drums` — a soft brush/hat on offbeats, a single low tap per bar, lots of silence · loop body 24 bars (~28s).*
- **Concept:** The literal atlas reading — a slow marsh wander, woodwind over lapping water, melancholy but never sad. The "lead leaves gaps, water fills them" call-and-response is the whole identity.
- **Vesper motif:** States the spine in minor — the hopeful rising leap (A3→D4→E4) is the lead's opening, but the stepwise settle home (F4→E4→D4) sags a half-step longer than usual, the melancholy lean.
- **GBC nod:** The functional "slow connective route" loop — short, hummable, front-loaded hook at the loop point, the pulse-lead-over-soft-pad texture of a low-stakes travel theme.

**Option B — "Bone Mist" (mood sibling).**
`generate-midi` brief: *preset `cave`→atmospheric · era `gbc` · 92 BPM, 6/8, suspended D Dorian (raised 6th glints over minor) · **lead:** sparser `pulse25`, a single drifting phrase per two bars, more questioning than walking · **harmony/arp:** `pulse12` faint bell-buoy chime arpeggio (compound-meter triplet lilt) glinting once or twice a phrase · **bass:** `tri_bass` deep, slow, lilting compound rocking — the Tide rocking-bass signature · **percussion:** almost none — one soft noise "wash" swell per phrase, like mist moving · loop body 20 bars (~26s).*
- **Concept:** The same fen, lonelier and more interior — leans into the bone-mist and the night, slower, in lilting 6/8 so it rocks like a boat rather than walks. Tide-meter forward, pace pulled back.
- **Vesper motif:** Fragments the spine — only the rising leap survives (A3→D4→E4), hanging unresolved; the settle-home is withheld until the very last bar, where it finally falls to D and voice-leads into the loop.
- **GBC nod:** The sparse-and-spacious dungeon-adjacent loop — silence as an instrument, atmosphere over hook, the "between places" mood.

**Option C — "Tidecall Channels" (relit/deep-water variant).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 108 BPM, 6/8, brightening D major with a wistful minor turn · **lead:** clearer, warmer `pulse25` lilting waltz-feel line, more confident than A · **harmony/arp:** `pulse12` proper bell-buoy chime arpeggios (fast broken major triads = the chip "chord"), dewy and ringing · **bass:** `tri_bass` rocking compound bass, a touch more propulsion now the deep channels are open · **percussion:** `drums` soft kick-on-one with a light offbeat hat, a chime-tap at the seam · loop body 24 bars (~26s).*
- **Concept:** Segment II — once Tidecall opens the deep channels, the fen brightens from minor toward major and gains the bell-buoy lilt of open water; the same place, a shade relit, rewarding the traversal unlock per the dawn arc.
- **Vesper motif:** States the spine cleanly in major (A3→D4→E4 … F#4→E4→D4) — the overshoot now lands hopeful, the first east-region taste of warming.
- **GBC nod:** The classic "Route 1 → Route 2" pay-off — the next stretch of road getting its own slightly brighter, more propulsive variant of the same leitmotif.

### 5 · Lowleaf Hollow — *a dim-green glowmoss forest where every dewdrop catches cyan light*
*Route/town · east · Verdant + Light · mysterious, dewy wonder; a hush full of soft glow.*

**Option A — "Glowmoss Wonder" (anchor).**
`generate-midi` brief: *preset `cave`→atmospheric · era `gbc` · 88 BPM, 4/4, Lydian-tinged G major (raised 4th = C#) · **lead:** glassy `pulse12` bell timbre, slow wondering phrases that hang on the #4 before resolving, dewy and curious · **harmony/arp:** second `pulse25` glassy bell arpeggio, slow broken major chords with the Lydian glint, sparkling under the lead · **bass:** soft `tri_bass`, low and breathy, long notes (the "breathy pad" stand-in) · **percussion:** barely-there `drums` — a single soft tap per bar, occasional dew-drip noise tick · loop body 24 bars (~33s).*
- **Concept:** The atlas reading exactly — lydian-tinged glassy bells over breathy bass, the Verdant signature, mysterious and full of soft wonder. The raised 4th is the magic.
- **Vesper motif:** The spine floats up through the Lydian (D4→G4→A4 … the settle B4→A4→G4), the overshoot stretched by the #4 so the "home" feels luminous, not safe.
- **GBC nod:** The special-area modal-wonder loop — the forest/sacred-grove sound that uses mode (not minor, not bright major) to mark "this place is enchanted," front-loaded glassy hook.

**Option B — "The Hollow Sleeps" (mood sibling, town-leaning).**
`generate-midi` brief: *preset `town` · era `gbc` · 84 BPM, 3/4, warm G major with a gentle minor turn · **lead:** rounded `pulse25` music-box lullaby melody, cosier and more tuneful than A, a settled village hush · **harmony/arp:** `pulse12` soft music-box arpeggio, slow and even, less glassy-bell, more hearth · **bass:** `tri_bass` gentle waltz root-fall-fifth, rocking and warm · **percussion:** soft `drums` brush on beats 2–3, a single chime per phrase · loop body 20 bars (~29s).*
- **Concept:** The Hollow as the small Lumenary *town*, not the forest — cosier, a lantern-lit lullaby in a waltz, the safe glow at the heart of the dark forest. Same place, warmer and more homely; trades wonder for hearth.
- **Vesper motif:** The spine becomes the lullaby's hook in lilting 3/4 (D4→G4→A4 … B4→A4→G4), rounded and even, the cosy "you're home" reading of the theme.
- **GBC nod:** The town/village leitmotif — relaxed, hummable, a tight cosy loop you hear constantly without it grating, the hearth-music of a small settlement.

**Option C — "Deep Glimmer" (richer-register / explore-light variant).**
`generate-midi` brief: *preset `cave`→atmospheric · era `gba` (richer register, Option C only) · 90 BPM, 4/4, Lydian-tinged G major · **lead:** glassy bell lead with a soft breathy pad genuinely sustaining underneath (now affordable) · **harmony/arp:** shimmering bell arpeggio + a faint second counter-bell answering across the stereo · **bass:** warm sustained low pad-bass with light echo · **percussion:** sparse soft taps + a gentle dew-shimmer noise swell, more room ambience · loop body 24 bars (~32s).*
- **Concept:** The Glowmoss Deep interior past Glimmerstep — a richer GBA register lets the "breathy pad" be a real pad and adds reverb depth, for the glowing-dark deep-forest exploration take. Sparser, more ambient, more cathedral.
- **Vesper motif:** Same Lydian ascent as A, but the counter-bell echoes the spine a bar late and a fifth up — the motif heard as glimmers answering across the dark, the "fragment into sparse echoes" treatment.
- **GBC nod:** Functionally the deep-interior "explore-light" ambient loop — the lush sample-voice grand-RPG forest that sets a place even through a tiny speaker, here in the era's richer voice budget.

### 6 · Cinderhead Mine — *ink-black galleries where crystal veins and lamp-fire are the only light*
*Cave · east · Stone (+ Storm, Light) · sparse, echoing, claustrophobic but faintly warm.*

**Option A — "Veinlight" (anchor).**
`generate-midi` brief: *preset `cave` · era `gbc` · 80 BPM, 4/4, A natural minor · **lead:** low `pulse25` drone-lead — long held low notes that move only a step or two, faintly tense-but-warm, never hurried · **harmony/arp:** a sparse `pulse12` crystal-chime — a single bright broken-triad glint every two to four bars, far up the register against the low drone · **bass:** `tri_bass` deep slow drone, root held long, the cave's floor · **percussion:** distant `drums` pick-tap — a dry knock every bar or two, occasional doubled tap echoing, vast silence between · loop body 28 bars (~33s, long loop).*
- **Concept:** The atlas reading — low drones, distant pick-tap percussion, the occasional crystal chime, sparse and echoing. Warmth comes only from the fire-lamps: the rare high chime is the diamond vein catching the light.
- **Vesper motif:** Fragmented to its bones — only the rising leap (E3→A3→B3) sounds, low and slow in the drone-lead; the settle-home never fully arrives, leaving the loop unresolved and uneasy. The crystal chime alone, far above, briefly voices the *settle* phrase (C5→B4→A4) as a glint of hope.
- **GBC nod:** The classic dungeon loop — slow, minor, mostly silence, atmosphere over melody, a long loop body so the emptiness reads as depth rather than repetition.

**Option B — "Pressure & Spark" (mood sibling, more tense).**
`generate-midi` brief: *preset `cave` · era `gbc` · 96 BPM, 4/4, A harmonic minor (raised 7th = G#) · **lead:** staccato `pulse25` low motif, terse and recurring, a held-breath pulse rather than a melody · **harmony/arp:** `pulse12` fast nervous arpeggio flickers in short bursts (the Sparkrat static), then cuts to silence · **bass:** `tri_bass` driving low ostinato, a steady tense walk under the silence · **percussion:** `drums` dry pick-tap plus an occasional gust/static noise swell — the Storm element leaking in · loop body 24 bars (~30s).*
- **Concept:** The same mine but leaning Storm and claustrophobic — the timbers groan, the air is charged, Sparkrats spark in the dark. Faster, more driven, more tense; trades the warm sparkle for held-breath pressure.
- **Vesper motif:** The rising leap is clipped into a staccato stab (E3→A3→B3) that repeats like a nervous tic; the harmonic-minor G# under it sharpens the unease — the motif under strain.
- **GBC nod:** The "deep-dungeon, something stirs" loop — driving bass under silence, the noise channel as threat (gusts/static), tension built from economy rather than density.

**Option C — "Crystal Gallery" (relit / Light-leaning variant).**
`generate-midi` brief: *preset `cave` · era `gbc` · 82 BPM, 4/4, A minor warming toward C major (relative-major lift) · **lead:** brighter bell-timbre `pulse25`, the crystal chime promoted to lead — an ascending sparkle line, hopeful · **harmony/arp:** `pulse12` glassy ascending bell arpeggios catching light, the Light signature, fuller than A · **bass:** `tri_bass` drone that rises stepwise to the relative major and warms · **percussion:** soft `drums` pick-tap, a bright chime-shimmer at the seam · loop body 24 bars (~29s).*
- **Concept:** The deep galleries past Glimmerstep where Glowpan's lantern-light and dense crystal turn the dark luminous — the relit/brightened reading, minor warming to its relative major, the Stone cave touched by Light. Same gallery, the moment it gleams.
- **Vesper motif:** States the spine ascending into the relative-major lift (E3→A3→B3 … then resolving up C5→B4→**C5**) — the overshoot finally allowed to land bright, the east region's hopeful "discovery" beat in the dawn arc.
- **GBC nod:** The treasure-room / glittering-cavern variant of a dungeon theme — the same cave's leitmotif rewarding the player with a brighter, sparkle-led reading once they reach the deep.

---

## North region — *energy & cold beauty*

### 7 · Galehigh Terraces — *kite-strung cliff-farms where the wind never sleeps*
*Route/town · north · Storm + Light · the giddy lift of standing high in the wind as the last fire-light drains into night-blue.*

**Option A — "Updraft" (anchor).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 138 BPM, 4/4, energetic D major · **lead:** `pulse25`, staccato darting line that springs up on the downbeat and skips back, restless and bright · **harmony/arp:** `pulse12` fast broken triads (D–F#–A), a flickering kite-tail shimmer above the lead · **bass:** `tri_bass` driving steady eighths, walking under the changes for forward push · **percussion:** `drums` brisk kick-snare with hat sixteenths; a noise-channel "gust" swell that rises and cuts every 4 bars · loop body 16 bars (~28s).*
- **Concept:** The canonical Galehigh read — pure propulsion and altitude, the "let's-go" route theme with wind constantly buffeting the groove. Front-loaded hook in the first two bars.
- **Vesper motif:** Routes "bounce" it — the spine (rising leap that overshoots, stepwise settle) is rhythmically chopped into staccato hops in bars 1–2, the overshoot landing on a cheeky offbeat.
- **GBC nod:** Echoes the brisk walking-pace overworld route function — short hummable loop, percussive lead — with an original springy contour.

**Option B — "Lanterns on the Wind" (mood sibling).**
`generate-midi` brief: *preset `town` · era `gbc` · 112 BPM, 4/4, warm D major with a wistful B-minor turn · **lead:** `pulse25` rounder, more lyrical melody, longer held notes that lean into the breeze · **harmony/arp:** `pulse12` gentle rolling arpeggio, slower and warmer than A · **bass:** `tri_bass` relaxed quarter-note pulse, settled rather than driving · **percussion:** `drums` soft brush-like kick/hat, sparse; one quiet noise swell per phrase, distant not gusty · loop body 20 bars (~43s).*
- **Concept:** The cliff-town reading rather than the route — same windy cliff, but seen from inside the warm farmstead at dusk. Cosier, a touch melancholy, the wind softened to a background sigh.
- **Vesper motif:** Stated nearly straight and tender — the hopeful leap and settle sung at walking pace, with the wistful minor turn coloring the "settle home."
- **GBC nod:** The town leitmotif function — gentle, warm, relaxed loop a player rests in between climbs.

**Option C — "Skyborne" (soaring/relit register).**
`generate-midi` brief: *preset `overworld` · era `gba` · 134 BPM, 4/4, radiant D major (Lydian-tinged G#) · **lead:** bright `pulse25` lead with wider, soaring intervals; a second airy counter-lead trades the hook · **harmony/arp:** shimmering arpeggio plus a sustained pad for the "lift" only the richer register allows · **bass:** `tri_bass` driving, with light reverb glue · **percussion:** `drums` energetic, plus a smooth wide "aurora-adjacent" noise swoosh as the updraft catches · loop body 24 bars (~43s).*
- **Concept:** Galehigh with the Storm constellation relit — fuller, lifted, the kites genuinely flying. Reserved gba pads/swells justify the brighter, soaring lean; the dawn arc warms one notch here.
- **Vesper motif:** Soaring transform — the rising leap is widened (a sixth or octave) and the line floats up before its settle, the motif literally taking flight.
- **GBC nod:** The climbing/cliff-route "building, airy, soaring" function, pushed into a fuller GBA voice for the brightened state.

### 8 · Windward Stair — *a switchback stair into the open sky*
*Route · north · Stone/Storm · the patient, breath-quickening climb from cliff-foot to crag, fire-sunset bleeding into night above.*

**Option A — "The Long Climb" (anchor).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 132 BPM, 4/4, bright A major · **lead:** high `pulse25` line that climbs in stepwise terraces then leaps a step higher each phrase — a melody that gains altitude as it loops · **harmony/arp:** `pulse12` steady ascending arpeggio, rung like footsteps on stone · **bass:** `tri_bass` firm, even quarter-to-eighth tread, the reliable climbing pulse · **percussion:** `drums` steady marching kick/hat; a wind-swell on the noise channel cresting each switchback (every 4 bars) · loop body 16 bars (~29s).*
- **Concept:** The canonical climbing-route read: airy and building, each phrase nudging higher so the loop *feels* like ascent. The connective Galehigh↔Pale Vault bridge in sound.
- **Vesper motif:** Climbing transform — the spine is sequenced upward, each repeat starting a scale-step higher, so the "rising leap" keeps re-launching from a new ledge.
- **GBC nod:** The classic cliff/mountain route function — high register, building, airy wind-swells — with an original terraced-ascent contour.

**Option B — "Stone & Gust" (mood sibling).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 126 BPM, 6/8, bright A major with a grounded F#-minor lean · **lead:** `pulse25`, a lilting compound-meter melody that rocks like a careful step-step-rest gait · **harmony/arp:** `pulse12` arpeggio in rolling triplet figures, lighter touch · **bass:** `tri_bass` dotted 6/8 pattern, weightier and more deliberate (the Stone half of the route) · **percussion:** `drums` swung 6/8 kick/hat; intermittent gust swells, less frequent, lonelier · loop body 18 bars (~33s).*
- **Concept:** Same stair, different meter and weight — leaning into the Stone element with a swaying 6/8 that feels like effortful, measured footing on cold rock, more solitary than triumphant.
- **Vesper motif:** Reset into compound meter — the leap-and-settle becomes a step-step-leap-settle gait figure, the overshoot landing softly on a triplet.
- **GBC nod:** Routes with a distinctive meter to set them apart from their neighbours; a hummable hook adapted to a walking-rhythm 6/8.

### 9 · Pale Vault Glacier — *aurora over an ice field that has forgotten the sun*
*Route/town · north · Frost + Light · glacial, shimmering, lonely-beautiful — the most still and tender place in the north.*

**Option A — "Aurora Vault" (anchor).**
`generate-midi` brief: *preset `emotional` · era `gbc` · 72 BPM, 4/4, suspended C major (sus2/sus4, no firm thirds) · **lead:** `pulse25` slow, sparse glassy chime-melody — a few long notes per phrase, lots of rest between · **harmony/arp:** `pulse12` widely-spaced suspended/quartal arpeggio drifting up like cold light · **bass:** `tri_bass` very slow, sustained low pedal tones, barely moving · **percussion:** minimal `drums`; a wide noise "aurora swoosh" swell rising and fading every 4 bars in place of a beat · loop body 16 bars (~53s).*
- **Concept:** The atlas read exactly — suspended harmony, glassy chimes, the aurora swoosh as the only "rhythm." Lonely-beautiful, the dawn arc still cold and mid-journey.
- **Vesper motif:** Frozen/stretched transform — the spine is slowed to long suspended tones, the "settle home" hanging unresolved on a sus2 so it never quite lands, suspended in the cold.
- **GBC nod:** The cold/ice-area function (slow, glassy, sparse, lonely) honoring chip discipline — harmony implied by slow broken intervals, never stacked.

**Option B — "Snow-Hushed Town" (mood sibling).**
`generate-midi` brief: *preset `emotional` · era `gbc` · 80 BPM, 4/4, gentle A minor warming toward C major · **lead:** `pulse25` a faint, tender hummable melody — more melodic and human than A, a small song against the cold · **harmony/arp:** `pulse12` soft music-box arpeggio, slow and rounded · **bass:** `tri_bass` slow steady half-notes, a quiet heartbeat of warmth · **percussion:** sparse soft `drums`, a single muffled pulse on the downbeat; one distant aurora swell per phrase · loop body 18 bars (~54s).*
- **Concept:** The ice-town rather than the open field — there are people and lanterns here. More melancholy and intimate, a warm small melody framed by the cold, leaning into the "lanterns in the dark" tone.
- **Vesper motif:** Tender minor reading — the leap-and-settle sung softly and nearly complete, the minor coloring the hope as fragile rather than triumphant.
- **GBC nod:** A cosy town leitmotif slowed and cooled — hummable hook front-loaded, kept within the 4-voice band.

**Option C — "Glasslight" (lush ambient register).**
`generate-midi` brief: *preset `emotional`/ambient · era `snes` · 66 BPM, 4/4, suspended C major (Lydian-tinged F#) · **lead:** soft bell-pad lead with warm reverb, long shimmering tones · **harmony/arp:** layered glassy chime arpeggio over a sustained sus pad — the chords the chip eras couldn't stack, now ringing in full · **bass:** warm sustained low pad, deep and still · **percussion:** none, or a single soft reversed-cymbal "aurora swoosh" swell per 4 bars; echo glues it all · loop body 16 bars (~58s).*
- **Concept:** The glacier as a lush cinematic ambient piece — the explicit "richer register" option. SNES pads, reverb, and real suspended chords deliver the wide aurora shimmer the atlas describes more fully than chip can; the standout audition candidate for this area.
- **Vesper motif:** Suspended and luminous — the spine appears as slow bell entries, the rising leap blooming into a sustained chord-swell, the settle dissolving into reverb rather than resolving.
- **GBC nod:** Still echoes the cold-area function (slow, glassy, lonely-beautiful) but reaches into the era reserved for big emotional moments, exactly where the style guide permits pads, chords, and warm echo.

---

## West region — *reaching for dawn (the night at its most charged)*

### 10 · Hushfrost Pass — *a lone lamp in a frozen canyon, the cold at your back*
*Route · west · Frost (+ Dark near the coldfog) · cold and sparse, tender enough to keep walking.*

**Option A — "Lamp in the Canyon" (anchor).**
`generate-midi` brief: *preset `emotional` · era `gbc` · 68 BPM, 4/4, suspended F minor · **lead:** a single `pulse25` bell-voice melody, wide spacing, long held notes with rests between — a lone call answered by silence · **harmony/arp:** `pulse12` very-slow suspended arpeggio (sus2/sus4 figures, no firm third), glassy and cold, low gain · **bass:** `tri_bass` pedal drone on the tonic, almost still, moving only at phrase ends · **percussion:** `drums` muffled heartbeat — soft kick on beat 1 and a faint pulse on the "and" of 3, nothing else · loop body 16 bars (~28s).*
- **Concept:** Literal atlas reading — lone bell, low pad, faint heartbeat. Maximum negative space; the silences are the instrument, the lamp the only warmth.
- **Vesper motif:** the rising leap is preserved but stretched and made fragile — the overshoot lands a beat too long and hangs unresolved before the stepwise settle, so "hopeful" reads as "holding on."
- **GBC nod:** echoes the function of a sparse handheld ice/cave cue — atmosphere over hook — but the contour is original.

**Option B — "Numbed at the Throat" (mood sibling, more Dark).**
`generate-midi` brief: *preset `emotional` · era `gbc` · 66 BPM, 4/4, unresolved F Locrian-leaning minor · **lead:** `pulse25` lead that gutters — notes that start clean then waver in pitch/duty (detuned drift), trailing off mid-phrase · **harmony/arp:** `pulse12` cold cluster arpeggio that refuses to resolve, dropping out for whole bars · **bass:** `tri_bass` low, faltering, occasionally a beat late · **percussion:** `drums` heartbeat slowed and thinned — every other bar it skips, as if the pulse is failing · loop body 16 bars (~29s).*
- **Concept:** The segment-II push toward the Hollowing's coldfog. Same place, but leaning into the numbed ex-Ember kin — the Frost beauty going hollow at the edges. Long silences and detuned guttering signal Dark without abandoning the canyon's identity.
- **Vesper motif:** the motif appears, then *fails to land* — the rising leap reaches up and the settle never completes, dissolving into a rest. Hope half-spoken.
- **GBC nod:** the era trick of a single channel "breaking up" to suggest dread, done by duty/pitch wobble rather than a real effect.

**Option C — "Aurora Over Ice" (sparser ambient / Frost-forward variant).**
`generate-midi` brief: *preset `emotional`/ambient · era `gbc` · 70 BPM, 4/4, suspended C minor with a lifted, aurora-bright color · **lead:** `pulse25` very high glassy chimes, sparse and shimmering, more sparkle than tune · **harmony/arp:** `pulse12` suspended arpeggio that slowly sweeps up and back down like an aurora ribbon — a wide "swoosh" of arpeggiated motion · **bass:** `tri_bass` soft sustained low note, mostly still · **percussion:** `drums` almost absent — a single soft hat shimmer at the loop seam, no heartbeat · loop body 16 bars (~27s).*
- **Concept:** The cold-beauty reading rather than the tense one — the sheltered hollows and the aurora above (sibling to Pale Vault Glacier, the town it connects from). Frost signature pushed to the front: glassy chimes, suspended arps, no fear.
- **Vesper motif:** the rising leap becomes the bottom of an ascending sparkle run — the motif used as an *upward shimmer* rather than a melody, vast and impersonal.
- **GBC nod:** the function of a shimmering ice-field ambient loop, contour original; ties timbrally to the Pale Vault track for region cohesion.

### 11 · Sunken Solarium — *a drowned summer that still glows under the water*
*Route/ruin · west · Solar (+ Tide/Verdant) · warm light remembered in a flooded place.*

**Option A — "Remembered Summer" (anchor).**
`generate-midi` brief: *preset `emotional` · era `gbc` · 96 BPM, 4/4, nostalgic G major with one wistful borrowed minor turn · **lead:** `pulse25` wistful melody, warm and singing, phrases that rise then sigh down a step · **harmony/arp:** `pulse12` soft harp-like pluck arpeggio (broken major triads), the radiant-but-remembered Solar signature, gentle and rolling · **bass:** `tri_bass` slow warm root-fifth motion, unhurried · **percussion:** `drums` very soft — a brushed kick on 1 and 3, a faint hat, like light lapping on water · loop body 24 bars (~30s).*
- **Concept:** The canonical atlas reading — major-key warmth, wistful pulse melody, soft arpeggio. Stored daylight under water: bright, but everything is past tense.
- **Vesper motif:** stated warmly and fully in major as the lead's opening — the rising leap radiant, the settle home tender. This is one of the score's clearest "the warmth is returning" statements.
- **GBC nod:** echoes the function of a sun-garden/remembered-place cue from the cartridge era — a hummable melancholy-major hook, front-loaded; original line.

**Option B — "Drowned Halls" (mood sibling, more melancholy / Tide-forward).**
`generate-midi` brief: *preset `emotional` · era `gbc` · 88 BPM, 4/4, G major slipping toward its relative E minor · **lead:** `pulse25` slower, more spacious melody, more rests, sinking phrases that don't always climb back · **harmony/arp:** `pulse12` arpeggio slowed and "submerged" — a watery, rolling figure, lower in register, Tide-cool against the Solar warmth · **bass:** `tri_bass` deeper, with a gentle swelling pulse like a slow tide · **percussion:** `drums` minimal — a soft low thud and an occasional droplet-tick hat · loop body 24 bars (~33s).*
- **Concept:** Same garden, but the water wins the emotional balance — half-flooded, cooler, lonelier. The Solar glow is dimmer and the Tide presence (Glentide) felt more. More melancholy than playful.
- **Vesper motif:** the motif appears in the relative minor — the same rising contour, now wistful and water-darkened; the settle lands lower than home, a half-step short of comfort.
- **GBC nod:** the era habit of recoloring a major theme into its relative minor to shift mood without a new tune.

**Option C — "Sunsketch Bloom" (relit / brightened variant).**
`generate-midi` brief: *preset `emotional`→`overworld` · era `gba` · 100 BPM, 4/4, radiant G major · **lead:** `pulse25` brighter, more active melody, the wistful sighs replaced with lifts · **harmony/arp:** `pulse12` faster harp-like arpeggio + a soft `gba` warm pad underneath for bloom (richer register) · **bass:** `tri_bass` warm, walking gently forward with more motion · **percussion:** `drums` a fuller soft kit, light shaker hat — gentle forward groove · 2nd voice: a soft warm `gba` counter-pulse echoing the lead a bar later · loop body 24 bars (~29s).*
- **Concept:** The diegetic relit reading — the Sunsketch sun-vine bridges blooming open, daylight surging back into the drowned garden. Reserved `gba` register earns the pads/2nd lead; this is the "dawn arc reaching west" version of the place.
- **Vesper motif:** stated in full radiant major and then *answered* by the warm counter-voice — call-and-response, the motif sung twice, the second time brighter: the score reaching toward dawn.
- **GBC nod:** the warmer GBA register used the way late-era handheld scores opened up for emotional peaks — pads and a doubled lead, contour still original.

### 12 · Sunvault Climb — *terraces of golden vines, climbing toward the stars*
*Route · west · Solar/Verdant (+ Light) · warm, ascending, hopeful — the road that lifts you upward.*

**Option A — "Vines to the Sky" (anchor).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 112 BPM, 4/4, radiant D major · **lead:** `pulse25` major arpeggio lead — a bright, ascending broken-chord melody that keeps stepping up, soft-brass-ish round tone · **harmony/arp:** `pulse12` harp-like pluck arpeggio rolling upward beneath the lead, fast and shimmering (Solar warmth + Light sparkle) · **bass:** `tri_bass` purposeful walking bass, propulsive walking-pace climb · **percussion:** `drums` brisk, steady kick-snare-hat keeping a confident walking groove · loop body 24 bars (~26s).*
- **Concept:** The canonical reading — warm, ascending, hopeful, propulsive. Every phrase climbs like the terraces themselves; the harp and brass-pulse make it the sunniest route in the region.
- **Vesper motif:** the motif *bounced* and made to climb — the rising leap becomes an arpeggiated launch, repeated up the scale a step higher each phrase, so the whole loop feels like ascending toward the Observatory.
- **GBC nod:** classic brisk-walking route function — a propulsive, hummable hook front-loaded in bar 1; original contour.

**Option B — "Morning on the Terraces" (mood sibling, warmer / more pastoral).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 108 BPM, 4/4, gentle Lydian-tinged D major · **lead:** `pulse25` more lyrical, singing melody (less pure-arpeggio, more tune), Lydian raised-4th lift for dewy Verdant wonder · **harmony/arp:** `pulse12` softer, slower glassy-bell arpeggio — sun-vines and growth rather than sparkle · **bass:** `tri_bass` rounder, gently bouncing rather than driving · **percussion:** `drums` lighter — soft kick + brushed hat, an easier stroll · loop body 24 bars (~28s).*
- **Concept:** Same climb, but a strolling pastoral warmth instead of a propulsive ascent — leaning Verdant (the overgrown golden terraces, the bees and seedlings) over Solar drive. Warmer and more wondering.
- **Vesper motif:** the motif sung lyrically with a Lydian raised note on the overshoot — the hopeful leap glints with wonder before the gentle settle; growth, not urgency.
- **GBC nod:** the era's pastoral-route flavor — a Lydian lift implying a sun-dappled meadow; original line, sibling to the Lowleaf Hollow glowmoss color.

**Option C — "First Light at the Top" (Light-forward / brightened variant).**
`generate-midi` brief: *preset `overworld` · era `gba` · 116 BPM, 4/4, brilliant D major · **lead:** `pulse25` lead carrying the arpeggio melody, doubled at the octave by a high bright bell `pulse12` for ascending sparkle (true-starlight Light signature) · **harmony/arp:** secondary `gba` warm pad sustaining underneath the climb for bloom; harp arp continues over it · **bass:** `tri_bass` strong forward walking bass · **percussion:** `drums` full bright kit, crash/fill at the loop seam · loop body 24 bars (~25s).*
- **Concept:** The top of the climb where Solar warmth meets the first true starlight — the route's hand-off into the sky-forward Observatory. Reserved `gba` register for the richer bloom; the dawn arc at its most upward and bright.
- **Vesper motif:** the climbing motif reaches its highest statement — leap and settle both an octave up, doubled in bell timbre, sparkling; the score audibly arriving at the sky.
- **GBC nod:** octave-doubled lead + ascending bell sparkle, the GBA-era trick for a triumphant route peak; contour original, and it timbrally pre-echoes the Observatory's Light bells for a smooth town transition.

### 13 · Nightreach Observatory — *the sky-forward town, vast and lonely under the densest stars*
*Town · west · Lunar (+ Light) · vast, lonely, wondrous — the most haunted Lumenary, reaching for dawn.*

**Option A — "Under the Whole Sky" (anchor).**
`generate-midi` brief: *preset `town`/reverent · era `gbc` · 84 BPM, 4/4, contemplative A minor resolving toward C major · **lead:** `pulse25` a lonely, spacious lead — long notes, wide intervals, lots of air, a single voice under a vast sky · **harmony/arp:** `pulse12` slow arpeggiated pad-figure (broken chords played slowly enough to read as a pad), the Lunar dreamlight signature · **bass:** `tri_bass` deep, slow, sustained roots · **percussion:** `drums` faint clockwork — a soft, dry tick on a steady subdivision (the telescope/observatory mechanism), no kit groove · loop body 24 bars (~34s).*
- **Concept:** The canonical reading — vast, lonely, wondrous, with the faint ticking clockwork and the minor→major lift. Sky-forward: the lead floats and the arpeggio opens space rather than filling it.
- **Vesper motif:** made *vast and arpeggiated* — the rising leap unfolds slowly across the slow arp figure, the settle resolving from minor into major at the loop's turn: hope dawning over the haunted town.
- **GBC nod:** the era's star-temple/lonely-town function — sparse, reverent, wide-spaced — within the 4-voice budget; original contour, light reverb only.

**Option B — "The Haunted Lumenary" (mood sibling, more melancholy / Lunar-dark).**
`generate-midi` brief: *preset `town`/reverent · era `gbc` · 80 BPM, 4/4, held A minor that never fully resolves · **lead:** `pulse25` a thinner, more isolated lead — a lonelier, sadder line that trails into long rests · **harmony/arp:** `pulse12` slow arpeggio kept in minor, occasionally a dissonant suspension before resolving · **bass:** `tri_bass` low, sparse, with long silences between roots · **percussion:** `drums` the clockwork tick made unsteady — slightly irregular, a clock running down · loop body 24 bars (~36s).*
- **Concept:** This is the 8th and most haunted Lumenary — the melancholy-forward reading that stays in minor, dwelling on the loneliness and the night-at-its-most-charged before withholding the major lift. The Lunar dreamlight at its most solitary.
- **Vesper motif:** the motif appears but the settle home is *denied* — the rising leap reaches up and resolves to a suspension instead of the tonic, hanging unresolved across the loop seam: hope present but not yet earned.
- **GBC nod:** the era's haunted/reverent-town trick of an unresolved minor loop that keeps you uneasy without a battle cue.

**Option C — "Skyweave" (lush gba/snes richer register).**
`generate-midi` brief: *preset `town`/reverent · era `snes` · 84 BPM, 4/4, contemplative A minor blooming to C major · **lead:** `pulse25` lonely lead, now with warm reverb/echo, answered by a soft `snes` 2nd lead a phrase later (call-and-response across the dome) · **harmony/arp:** lush `snes` pad chords (chords allowed here) under a glassy bell arpeggio — the densest, most orchestral texture in the region · **bass:** `tri_bass`/`wave` deep sustained low end with the warm SNES echo · **percussion:** `drums` faint clockwork tick + a soft distant timpani-ish swell at section turns; light shimmer at the seam · loop body 24–28 bars (~36s).*
- **Concept:** The explicit "richer register" Option C the area flags for — the big domed room, telescope brass, the densest starfield in the game. Reserved `snes` voices/reverb/chords earn their place at the score's most sky-forward, dawn-reaching moment.
- **Vesper motif:** stated vast and arpeggiated by lead one, then *answered* by the 2nd lead in full major over the pads — the motif's clearest, most orchestral bloom in the whole west: the score plainly reaching toward the coming true dawn.
- **GBC nod:** the grand-RPG approach of opening into pads, echo, and a counter-lead for a town that has to feel like standing under the entire sky — original melody, the lush register reserved exactly for this peak.

---

## Outer ring — *the connective tissue & the drained places*

### 14 · Vesper Crossroads — *lanterns at the fork; the place you always come back to*
*Hub · outer · Light · cosy and dependable, the soundtrack's warm front porch.*

**Option A — "The Signpost Tune" (anchor).**
`generate-midi` brief: *preset `town` · era `gbc` · 108 BPM, 4/4, comfortable C major · **lead:** round `pulse25` melody stating the Vesper motif up front, friendly and singable, small range C4–A4 · **harmony/arp:** `pulse12` light bell-like arpeggios outlining I–vi–IV–V, sparkly on top · **bass:** `tri_bass` simple rooted walk, gently bouncing on beats 1 and 3 · **percussion:** soft `drums`, brushy hat + light kick, never busy · loop body 16 bars (~35s).*
- **Concept:** The canonical homey waystation read — tight, instantly recognisable, engineered to never grate on the hundredth hearing. The shortest, most "settled" loop in the score.
- **Vesper motif:** Stated plainly and complete in bars 1–2 (rising hopeful leap that overshoots, then steps home) — this is the motif's cosy home base; every other area is a transform of what's heard here.
- **GBC nod:** The constantly-heard friendly hub loop — short, warm, four channels working clean, the kind of waystation tune you hum without noticing.

**Option B — "Quiet Hours at the Inn" (mood sibling).**
`generate-midi` brief: *preset `town` · era `gbc` · 96 BPM, 4/4, warm C major with one wistful turn to vi · **lead:** sparser `pulse25`, more rests between phrases, music-box feel · **harmony/arp:** `pulse12` slow rolled arpeggios, fewer notes, ringing longer · **bass:** `tri_bass` half-note pillars, restful · **percussion:** very minimal `drums` or a soft heartbeat-rate kick only · loop body 16 bars (~40s).*
- **Concept:** Lonelier, lamplit, after-dark lean — the same inn at 2am with one window still glowing. More melancholy, more silence, same comfort underneath.
- **Vesper motif:** The same contour stretched and slowed, the settle-home phrase lingering on its final note before resolving — tender rather than chipper.
- **GBC nod:** The "town at night" variant cartridge scores sometimes used — same place, lower energy, the genre's cosy-melancholy register.

**Option C — "Four-Way Nexus" (relit late-game variant).**
`generate-midi` brief: *preset `town` · era `gbc` · 116 BPM, 4/4, bright C major · **lead:** `pulse25` motif now confident and fuller, with a small answering counter-phrase · **harmony/arp:** `pulse12` busier ascending-sparkle arpeggios (the Light bell signature), more movement · **bass:** `tri_bass` walking eighths, propulsive · **percussion:** fuller `drums` — kick/snare/hat with a fill at the seam · loop body 24 bars (~50s).*
- **Concept:** Post-`hub_unlocked` reprise: once the four cardinal roads open, the sleepy fork becomes a bustling crossroads. Same tune, more traffic, more joy — the payoff of having reconnected the region.
- **Vesper motif:** Stated brighter and busier, now harmonised by a counter-line — the home-base motif "grown up" to match the relit world.
- **GBC nod:** The genre's habit of swapping a location's track for a livelier arrangement once the world opens up — the reward-state reprise.

### 15 · Coldfog Marches — *snuffed lanterns; the drained place*
*Route · outer · Dark (Hollowing) · hollow and faltering, grief made of mist — never grim-violent.*

**Option A — "Snuffed" (anchor).**
`generate-midi` brief: *preset `boss` · era `gbc` · 70 BPM, 4/4 (felt loose), unresolved A minor · **lead:** a single `pulse25` melody, detuned slightly flat, guttering — phrases that start then trail off into rests, never completing · **harmony/arp:** sparse `pulse12`, a cold detuned drone note or two, mostly absent · **bass:** `tri_bass` low, slow, holding one ominous root for bars at a time · **percussion:** almost none — a faint, irregular noise "drip" instead of a beat · loop body 24 bars with heavy silence (~55s).*
- **Concept:** The canonical drained-zone sound: near-silence, long gaps, a lone melody that can't finish its thought. Unsettling through absence, not menace.
- **Vesper motif:** The motif appears FRAGMENTED — the hopeful rising leap is attempted but the settle-home never resolves; it gutters out on the overshoot, detuned. The melody you know, broken.
- **GBC nod:** The genre's "tainted zone" / corrupted-area sound — detuned pulses, dead air, a tune that's been hollowed out.

**Option B — "Ink That Swallows Colour" (mood sibling).**
`generate-midi` brief: *preset `boss` · era `gbc` · 66 BPM, 4/4, suspended A minor (no resolution) · **lead:** even sparser than A — one or two faltering `pulse25` notes per phrase, more breath than melody · **harmony/arp:** a single sustained detuned `pulse12` fog-drone, swelling and fading like mist breathing · **bass:** `tri_bass` barely-there pedal tone, sub-felt · **percussion:** none, or a single hollow noise "thud" at long intervals · loop body 24 bars (~60s).*
- **Concept:** Less melody, more dread-as-weather. Where A still has a guttering tune, B is mostly the fog itself — the emptiness of a place where light has been taken. The lonelier, emptier read.
- **Vesper motif:** Barely a ghost — only the first interval of the rising leap surfaces once per loop, unanswered, before the drone reclaims it. The motif almost erased.
- **GBC nod:** The ambient "dead place" cue — atmosphere over melody, the genre's quietest, eeriest register.

**Option C — "Emberward Pushing Through" (as-it-relights variant).**
`generate-midi` brief: *preset `boss` · era `gbc` · 74 BPM, 4/4, A minor warming toward C major · **lead:** the faltering `pulse25` melody from A, but now finding its footing — phrases begin to complete · **harmony/arp:** hopeful `pulse12` bell notes (the brightening cue) creep IN over the detuned drone, warming and steadying it · **bass:** `tri_bass` lifts off its single root and begins a gentle walk · **percussion:** a soft, slow heartbeat kick appears and steadies · loop body 24 bars (~50s).*
- **Concept:** The "as it relights" state once Emberward burns the coldfog back — bells and warmth bleed into the hollow drone; the drained place starting to breathe again. Hope arriving, not yet won.
- **Vesper motif:** The fragmented motif finally RESOLVES — the settle-home phrase that guttered out in A completes for the first time, in warming major. The repair of the broken theme.
- **GBC nod:** The brightening transition cue — hopeful notes creeping into a previously hollow soundscape, the genre's "the curse is lifting" moment.

### 16 · Lanternway — *the cosy country lane home*
*Route (hub spokes) · outer · Light/Verdant · the game's most-heard walking music — the purest, hummable optimism in the score.*

**Option A — "The Walking Tune" (anchor).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 120 BPM, 4/4, comfortable G major · **lead:** plucky `pulse25` lead, the most singable hook in the game, walking-pace phrasing with a confident bounce, range G4–D5 · **harmony/arp:** `pulse12` light bell arpeggios on the off-beats (the Light signature), skipping along · **bass:** `tri_bass` springy walking eighths, the engine of the groove · **percussion:** `drums` brisk kick/snare/hat with a little fill before the loop seam · loop body 32 bars AABA (~32s).*
- **Concept:** The signature cosy travel loop — the soundtrack's beating heart, optimistic and endlessly repeatable. If one tune defines PixelKin's mood on the road, it's this.
- **Vesper motif:** This is the motif's BOUNCING form — the hopeful rising leap rendered springy and skipping, the settle-home turned into a cheerful little hop. The hub states it; Lanternway makes it dance.
- **GBC nod:** The quintessential overworld route theme — front-loaded hook, tight AABA, four channels in lockstep, the tune that *is* the journey.

**Option B — "Long Lane Home" (mood sibling).**
`generate-midi` brief: *preset `overworld` · era `gbc` · 112 BPM, 4/4, warm G major with a gentle vi lean · **lead:** the same `pulse25` hook but softer, more legato, a touch wistful — evening-walk rather than morning-stroll · **harmony/arp:** `pulse12` arpeggios slower and rounder, fewer sparkle notes · **bass:** `tri_bass` walking but relaxed, quarter-note feel · **percussion:** lighter `drums`, brushed feel, no fills · loop body 32 bars (~38s).*
- **Concept:** Same beloved tune, dialled to "lanterns coming on at dusk" — cosier and a shade melancholy, for the walk back rather than the walk out. Warmer, lonelier sibling of A.
- **Vesper motif:** The bouncing motif relaxed into a strolling version — the hop becomes a gentle sway, the overshoot softened, the settle-home savoured.
- **GBC nod:** The mellower route variant — the genre's trick of giving its main travel theme a softer evening colour without losing the hook.

---

## Central region — *darkest, then the turn*

### 17 · Penumbra Ring — *the wall of ink that recedes wedge by wedge*
*Route (barrier) · central · no kin (they refuse the dark) · dark drone gaining hope, your lamp the only colour.*

**Option A — "Wall of Ink" (anchor / early-dark state).**
`generate-midi` brief: *preset `boss` · era `gbc` · 60 BPM, 4/4 (felt as slow pulse), dark D minor unresolved · **lead:** almost none — one lonely, low `pulse25` note swelling out of the drone every few bars, no real melody yet · **harmony/arp:** `pulse12` low evolving fog-pad, dark and slowly shifting, detuned at the edges · **bass:** `tri_bass` deep pedal drone, oppressive and still · **percussion:** a sparse `drums` heartbeat — a single soft kick every two bars, the only sign of life · loop body 24 bars (~60s).*
- **Concept:** The first, darkest crossing — almost no melody, just the breathing wall and your own pulse. With Coldfog, the least-resolved point in the whole score: the bottom of the dawn arc.
- **Vesper motif:** Withheld — only its lowest root note glows once per loop, like a memory of a tune you can't yet reach inside the dark.
- **GBC nod:** The deepest "tainted barrier" ambient — drone, heartbeat, and dread, the genre's most stripped-back tension cue.

**Option B — "Wedge by Wedge" (mood sibling / late-receding state).**
`generate-midi` brief: *preset `boss` · era `gbc` · 64 BPM, 4/4, D minor brightening toward F major · **lead:** the lonely `pulse25` note has grown into hopeful phrases — tentative ascending bell-tipped lines (the brightening cue) creeping over the drone · **harmony/arp:** the `pulse12` fog-pad lightens, detune resolving, warm intervals opening up · **bass:** `tri_bass` drone lifts into slow, hopeful root movement · **percussion:** the heartbeat `drums` strengthens and steadies, a soft hat joining · loop body 24 bars (~58s).*
- **Concept:** The same place after several constellations are relit — the fog has receded and hope has bled into the drone. The evolving-state pair to A: same DNA, audibly thawing.
- **Vesper motif:** Emerges for the first time — the rising hopeful leap surfaces out of the pad, incomplete but reaching, foreshadowing its full triumphant return at the Spire.
- **GBC nod:** The brightening-as-you-progress cue — hopeful notes creeping into a dark drone, the audible reward of clearing the barrier.

### 18 · Umbral Spire — *the dead Lumenary and the Ninth Lantern; the climax*
*Cave/hub · central · Dark vs Light (Keystar) · dread building to soaring — the soundtrack's biggest moment, the dawn finally turning.*

**Option A — "Crown of Null" (anchor — the structured boss piece).**
`generate-midi` brief: *preset `boss` · era `snes` · 60 BPM intro building to ~150 BPM, 4/4, A minor → triumphant A major · **lead:** layered `pulse25` lead booming the Vesper motif in dark minor; **counter-lead:** a second pulse line answering it · **harmony/arp:** real chords + a swelling reverbed pad under it, the SNES echo gluing the space · **bass:** driving `tri_bass`/wave, urgent and relentless in the loop · **percussion:** full driving `drums`, building from sparse intro to pounding loop, crash at the resolve · structured: **intro (dread, ~16 bars) → loop (driving battle, 24–32 bars) → resolve (triumphant major, 16 bars)** total ~50s+.*
- **Concept:** The canonical climax — the one place reaching for the richer SNES register (pads, chords, reverb, second lead). Tense intro, driving battle loop, then the major resolve at the Keystar relight. The score's biggest single moment.
- **Vesper motif:** The whole game's payoff — BOOMED in dark minor through the intro and loop, then RESOLVED into triumphant A major at the Keystar relight. The broken/withheld motif from Coldfog and Penumbra finally made whole and glorious.
- **GBC nod:** The genre's structured final-boss theme (tense intro → driving loop → triumphant resolve) stepped up to the richer console register for the climax — the soundtrack's biggest swing.

**Option B — "The Black Ascent" (mood sibling — dread loop, pre-resolve).**
`generate-midi` brief: *preset `boss` · era `gba` · ~140 BPM, 4/4, relentless A minor (no resolution) · **lead:** `pulse25` driving the minor motif hard, anxious and climbing · **counter-lead:** a second darting line raising tension · **harmony/arp:** tense reverbed pad, anti-light shimmer (a detuned high voice for the leaking null-lanterns) · **bass:** pounding driving bass, no rest · **percussion:** full relentless `drums`, fills ratcheting tension · loop body 32 bars, deliberately unresolved (~55s).*
- **Concept:** The pure dread/ascent loop for the climb itself — Còr's null-lanterns leaking anti-light, the fight against the dark before the win. All tension, no release; the darkest energy in the score.
- **Vesper motif:** Driven in hard minor, urgent and overshooting, the settle-home repeatedly DENIED — it never resolves, holding the tension until Option A's (or the game's) major payoff.
- **GBC nod:** The genre's driving dread loop — the relentless central-evil theme that withholds resolution so the eventual major hits all the harder.

**Option C — "First True Dawn" (triumphant-resolve variant).**
`generate-midi` brief: *preset `victory`→`boss` · era `snes` · ~120 BPM, 4/4, radiant A major · **lead:** `pulse25` singing the Vesper motif in full, complete and soaring; **counter-lead:** a harmonising second line · **harmony/arp:** lush warm chords + harp-like arpeggio + swelling pad, generous reverb · **bass:** warm, full, grounded bass · **percussion:** triumphant `drums`, big but joyful, a final crash · loop body 24 bars (~50s), or one-shot fanfare if used as a sting.*
- **Concept:** The Keystar-relight resolution lifted out as its own cue — the moment dark turns to dawn, Keylumen radiant, the Skyweave Crown completing overhead. The emotional peak that sets up the Dawnstead epilogue. (Shares its "First True Dawn" name and major key with Dawnstead's Option C — they're meant to be the same resolution, heard first at the summit, then settled into in the epilogue town.)
- **Vesper motif:** The total payoff — the motif that was cosy at the hub, broken at Coldfog, withheld at the Penumbra, and minor at the Spire is now stated WHOLE in triumphant major, fully harmonised. The entire score resolving its central thread.
- **GBC nod:** The genre's transformation of a dark motif into a triumphant major reprise at the finale — the soundtrack's payoff moment, given full console warmth.

---

## Epilogue

### 19 · Dawnstead — *the lullaby finally meets the sun*
*Town (post-game epilogue) · south, near Tinderwick · Ember → Solar/Light · the payoff — Tinderwick's lullaby blooming into radiant, fully-instrumented daylight.*

**Option A — "Dawnstead — The Lullaby in Full" (anchor).**
`generate-midi` brief: *preset `victory`→`town` · era `gbc` · 100 BPM, 4/4, C major, radiant, no minor turn · **lead:** bright `pulse25` plays Tinderwick's "Lantern Lullaby" melody whole — but now confident, mid-tempo, the wistful A-minor answer resolved to a glowing C-major answer instead · **harmony/arp:** `pulse12` the old "music-box" arpeggio now opened into a flowing harp-like ascending arpeggio (Light sparkle) · **bass:** `tri_bass` warm, full, walking root-motion bass — the hearth pulse grown into a confident stride · **percussion:** `drums` gentle, present groove — soft kick/brush, a warm fill at the seam · loop body 24 bars (~38s).*
- **Concept:** The canonical dawn payoff, held inside the GBC house band so it reads as the *same town, same melody, finally in daylight.* Every wistful element of Tinderwick A is here resolved: the minor turn made major, the sparse arp made flowing, the clock-tick made a real heartbeat groove.
- **Vesper motif:** The full bloom — the complete Vesper motif and the Tinderwick lullaby reprised in unclouded major, the lift now reaching the sky it only reached for in the start town.
- **GBC nod:** The radiant-major reprise of the source town theme — the cartridge-era "and the world is whole again" transformation of a leitmotif you've heard sad all game.

**Option B — "Warm Shadows, Open Sky" (mood sibling).**
`generate-midi` brief: *preset `town` · era `gbc` · 96 BPM, 4/4, C major, tender-radiant · **lead:** `pulse25` the lullaby melody, but gentler and more intimate than A — joy with a tear in it, the memory of the long night still warm in the major · **harmony/arp:** `pulse12` soft flowing arpeggio, less sparkle, more glow · **bass:** `tri_bass` warm rocking hearth pulse (closer to Tinderwick A's), not a busy stride · **percussion:** very light, a soft heartbeat brush · loop body 24 bars (~40s).*
- **Concept:** The bittersweet lean of the payoff — the sun is up but the player remembers every dark mile. Radiant *and* tender, for a softer epilogue mood (quiet town-living after credits) where triumph gives way to contentment.
- **Vesper motif:** Full and major, but stated tenderly rather than triumphantly — the bloom "exhaled" instead of declared, so it can sit under quiet post-game wandering.
- **GBC nod:** The intimate major reprise — same payoff theme, the homey town-living version rather than the curtain-call version.

**Option C — "First True Dawn" (richer gba/snes register — the curtain-call).**
`generate-midi` brief: *preset `victory`→`town` · era `snes` · 100 BPM, 4/4, C major, fully radiant, warm reverb · **lead:** `pulse25`-warm lead carries the lullaby melody · **counter-lead:** a second voice (soft warm 2nd lead) weaves a counter-melody quoting the Dimglass route's bounced motif — town and road themes embracing at the finish · **harmony/arp:** flowing harp arpeggio (the brief's named harp) plus a soft sustained pad bed for genuine chords · **bass:** warm full bass with real low-end motion · **percussion:** `drums` a fuller, gentle groove with a triumphant fill and crash at the seam · loop body 32 bars (~51s).*
- **Concept:** The big-moment register the atlas explicitly invites — lead + counter-lead + harp arpeggio + warm pad bass, with SNES reverb and real chords. The single track in the south allowed to break the chip band, because it *is* the emotional summit of the whole dawn arc. Still renders on the chip engine for cohesion.
- **Vesper motif:** Bloomed in full radiant major across two voices at once — the lullaby in the lead, its route-bounce contour answering in the counter-lead, the entire south score resolving into one chord of daylight.
- **GBC→SNES nod:** The era-step-up earned by the finale — the cartridge "epilogue theme that finally adds the strings/pads the whole soundtrack withheld," landing the payoff the score has been promising since Tinderwick's first wistful loop.

---

## Cross-region shared cues (score once, reuse)

These aren't world-map areas, but they bind the soundtrack and should be planned
alongside it. Compose each **once** and reuse everywhere (don't re-score per
area). Each can still carry the **Vesper motif** so the whole score stays kin:

- **Wild battle** — `battle`, `gbc`, ~150–160 BPM, urgent minor; a 16–32-bar loop. (Several produced drafts already exist in `public/assets/audio/music/` — `battle-emberfall`, `battle-nightfall`, `battle-veil`, `battle-main-dusk-duel`.)
- **Lumenary / Lampwarden duel** — `boss`, `gbc`/`gba`, ~160 BPM, a heroic B-section; the "earn the Gleam" arena theme, reused for all eight with light per-element recolouring.
- **Hollowing encounter** — `boss`, detuned/uneasy, the antagonist cue (sibling to Coldfog/Penumbra).
- **Victory fanfare** — `victory`, one-shot (`loop:false`), 2–6 s, hard tonic resolution; states the Vesper motif's *settle home* triumphantly.
- **Stings** — level-up, item/Gleam-get, evolution (`loop:false` jingles per `style-guide.md`).

> Existing drafts of record (battle set above) are already in
> `public/assets/audio/music/`; the area loops in this doc are the next pass.
