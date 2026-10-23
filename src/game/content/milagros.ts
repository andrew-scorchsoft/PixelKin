/**
 * THE BOOJI-WOOJI MAN MILAGRO CARDS (2026-10) — Paul's own painted cards, recreated
 * from photos of the real deck (art: assets/milagros/ via tools/assets/gen_milagros.py,
 * served from public/assets/milagros/<id>.webp).
 *
 * How they reach you: Paul hands over the BOX ("Your cards?" on his lamp menu, once
 * you've met him) with its lore card and the first card, DESASOSIEGO
 * (flag:milagro_pack). The lore card asks you to leave the cards lying about for
 * strangers to find, and somebody always has: every other card is held by one
 * person somewhere in Vesperholm (`giver`), who hands it over the first time you
 * talk to them once the box is yours (WorldScene.maybeGiveMilagro). Each card has
 * a STORY, a guess at what's behind it, which plays when you get it and stays in
 * the pack (pause menu -> MILAGROS).
 *
 * Hidden real-people content like the rest of Paul's: never in the changelog,
 * guide or music page. The card phrases are Paul's own (one lyric line reworded:
 * `skin`); the subjects the briefs re-draw are noted in briefs.json.
 */

export interface MilagroCard {
  /** Art stem (public/assets/milagros/<id>.webp) and the flag suffix. */
  id: string;
  /** The phrase lettered round the card's border. */
  title: string;
  /** Who has it: the NPC placement id on that map. */
  giver?: { map: string; npc: string };
  /** What the giver says as they hand it over. */
  found: string;
  /** The story behind the card — a guess, told as one. Paged in the viewer. */
  story: string;
}

export const MILAGRO_PACK_FLAG = 'flag:milagro_pack';
export const milagroFlag = (id: string): string => `milagro:${id}`;
export const milagroArt = (id: string): string => `assets/milagros/${id}.webp`;

/** The little lore card in the box (the real one, carried into Vesperholm). */
export const MILAGRO_LORE =
  'The Milagro Cards you now hold were made by a somewhat mysterious figure known as the Booji-Wooji Man. ' +
  'Rumour has it he once kept a little apothecary in a river-mouth town far over the western sea, where the bands ' +
  'play in the streets, and sold herbs alongside small objects he swore could help folk suffering a variety of ills. ' +
  'Milagros, he called them: little charms found on his many wanderings, that he believed had healing power. ' +
  'These days he can often be found under the old arches of a smoky town, in the early mornings, in need of a ' +
  'musical hook for that evening\'s performance. Sometimes he sets up a small table and sells a few of his remaining ' +
  'milagros, and chants and road-songs to travelling musicians who might need one. ' +
  'The cards are his small paintings, with phrases from his road-songs. You can build a little house of cards from ' +
  'them, or fly them across a room if so inclined. In times of uncertainty, or in need of what he calls "a cosmic ' +
  'roadside sign", draw one at random and let it speak to you. ' +
  'He asks one thing: when you are finished with them, leave the cards lying about. In tea-houses, on the ' +
  'Lantern-cars, in bookshops, wherever you may wander. His hope is that people will find them and laugh, or at ' +
  'the very least be confused.';

export const MILAGROS: MilagroCard[] = [
  {
    id: 'desasosiego',
    title: 'DESASOSIEGO',
    found: 'Paul turns the top card over without looking. It was always going to be this one.',
    story:
      'The oldest card in the box, and the only one with no picture of a thing: just a small flame that will not sit ' +
      'still. It is the word for the restless unease that paces the kitchen at night until you get up and make ' +
      'something. Paul says it is not a sickness. It is the cure, turning up early. Every other card in the box was ' +
      'painted because of this one.',
  },
  {
    id: 'dogtag',
    title: 'I WONDER AT WHAT POINT THE FORM OF MY LIFE BECAME ITS CONTENT, DOUBLING BACK ON ITSELF?',
    giver: { map: 'pearlmoor_quay', npc: 'fisher_lit' },
    found: '"Came up in my net, tied to a cork. Pretty, but it\'s no use to a fish."',
    story:
      'A tag of the sort a sailor wears so the sea can send him home. This one was worn so long that the name rubbed ' +
      'off it, and the man kept wearing it anyway: the tag stopped saying who he was and started being who he was. ' +
      'Somewhere along the way the shape of a life becomes the life. He noticed on a Tuesday, and painted it.',
  },
  {
    id: 'fish',
    title: "DON'T GET TOO CLOSE",
    giver: { map: 'driftholm_chandlery', npc: 'chandler' },
    found: '"Somebody used it as a bookmark in the tide-tables. I kept the tide-tables. You have the card."',
    story:
      'A spotted fish, every spot an eye. It swims a careful distance from everyone, not because it is unkind but ' +
      'because it can see them all at once, and that is a great deal to look at. It is the best company in the ' +
      'world, from about an arm\'s length away.',
  },
  {
    id: 'spool',
    title: 'FEAR SELLS',
    giver: { map: 'stillwater_lampmaker', npc: 'lampmaker' },
    found: '"Found it wedged in my thread-drawer. I don\'t sell fear. Shutters, mostly. ...Same thing, some days."',
    story:
      'An empty cotton spool. All the thread has been sold off, yard by yard, to people frightened of coming ' +
      'undone. The peddler did very well. The spool kept the hole in the middle, which was the only part worth having.',
  },
  {
    id: 'shadowdoll',
    title: "I MAY NOT BE THE CENTRE OF THE UNIVERSE, BUT I'M WITHIN WALKING DISTANCE OF IT",
    giver: { map: 'galehigh_home', npc: 'home_kid_lit' },
    found: '"It was under my pillow! I think it walked there. Do you want it? It\'s very small but it\'s very sure."',
    story:
      'A little shadow-sprite with button eyes, the kind that follows a child home from the lamplighting. It knows it ' +
      'is not the most important thing in any room. It also knows exactly how many steps it would take to get there.',
  },
  {
    id: 'dancer',
    title: "I'VE HAD A HOLE IN MY HEART FOR SO LONG!",
    giver: { map: 'pearlmoor_inn', npc: 'fisher_lit' },
    found: '"Tucked in the frame of the inn mirror. Whoever left it danced all night. Badly. Gloriously."',
    story:
      'She danced on a boat that went round the islands, and every port took a little piece of her heart, until there ' +
      'was a space in it shaped like the sea. She says it is not an injury. It is where the music gets in.',
  },
  {
    id: 'whistle',
    title: 'A SCREAM OF MUTENESS',
    giver: { map: 'stillwater_quiet_hall', npc: 'hall_keeper' },
    found: 'They hold it out without a word, finger to their lips. The quiet hall keeps its quiet.',
    story:
      'A clay whistle, green as pond-weed, that no one has ever managed to blow a note from. You put your whole chest ' +
      'into it and nothing comes out, and that nothing is the loudest thing you have ever heard.',
  },
  {
    id: 'barkingman',
    title: 'CAN YOU HEAR THE DOGS BARKING?',
    giver: { map: 'hushfrost_pass_ii', npc: 'caretaker_after' },
    found: '"Left on the hut table, weighed down with a stone. The dogs up here bark at it. Take it before they eat it."',
    story:
      'An old man in a green coat who hears dogs that nobody else can. He says they bark at whatever is coming up the ' +
      'road before it arrives: weather, letters, good news. He tilts his head and grins, and three days later the thaw comes.',
  },
  {
    id: 'taxi',
    title: 'CATCH A RIDE ON THE VOODOO TAXI',
    giver: { map: 'wickrun_foot', npc: 'lift_keeper' },
    found: '"Fare token, or near enough. Somebody paid me with it. It got them to the top, so I\'m not complaining."',
    story:
      'A blue fare-token for a cab that only runs after midnight. You get in, it does not ask where you are going, and ' +
      'it takes you somewhere better. The meter ticks in a language of clicks. Nobody has ever paid more than one token.',
  },
  {
    id: 'cowboy',
    title: 'CUIDA TUS DIENTES COMO TUS ARMAS',
    giver: { map: 'wickrun_crest', npc: 'pell' },
    found: '"Found it in a rented runner\'s saddlebag. Tooth-advice from the sun country, I\'m told. Sound advice."',
    story:
      '"Look after your teeth like you look after your weapons." A little tin cowboy with his pistol raised, who in ' +
      'forty years of painted gunfights never once fired it. He did floss. Every night. It is the reason he is still smiling.',
  },
  {
    id: 'pig',
    title: 'GLOSSOLALIA',
    giver: { map: 'pearlmoor_allotment', npc: 'anth_done' },
    found: '"Turned it up with the leeks. Rod reckons it\'s a sign. Rod reckons everything is a sign."',
    story:
      'A golden pig that speaks in tongues: whole sermons of grunts that sound, if you are tired enough, like ' +
      'something important. People came from three valleys to listen. The pig only ever wanted an apple.',
  },
  {
    id: 'stringy',
    title: 'ART IN THE SERVICE OF DEGENERATE DISCOURSE',
    giver: { map: 'sunken_solarium_lumenary', npc: 'prompter_lit' },
    found: '"Pinned to the back of the stage curtain. The critics hated the play. The card was the best part."',
    story:
      'A tangle of golden string that started out as a beast and argued itself into a knot. It was painted for a ' +
      'gallery that called it rude, and so it went happily and rudely on its way, being argued about in tea-houses forever.',
  },
  {
    id: 'wetnumbers',
    title: 'MY ROOM SMELLS OF WET NUMBERS',
    giver: { map: 'reckoning_works', npc: 'ketterly' },
    found: '"It was in a ledger, page four hundred. Everyone who opens that ledger has the same complaint."',
    story:
      'A clerk who kept the accounts of a damp office for thirty years, until the sums soaked into the walls. On wet ' +
      'mornings the whole room smells of sevens. He let his hair grow, wore his good boots, and walked out to find a ' +
      'room that smells of nothing at all.',
  },
  {
    id: 'bottle',
    title: 'FALL INTO THE NIGHT SKY AND CHASE AFTER KOKOPELLI',
    giver: { map: 'nightreach_observatory', npc: 'fenn_after' },
    found: 'Fenn: "Found it pressed in a star-atlas. Somebody marked the constellation of the flute-player. Good company."',
    story:
      'A blue bottle that holds a little of the night, stoppered. Uncork it and lie down on the grass, and you fall ' +
      'upward after the hunched flute-player who walks the sky playing everything into spring. You will not catch him. ' +
      'That is not the point.',
  },
  {
    id: 'eyemask',
    title: 'EMPIRE OF THE EYE',
    giver: { map: 'sunken_solarium', npc: 'troupe_mask_after' },
    found: '"From the costume trunk. Every mask in there is watching something. This one is watching YOU."',
    story:
      'A mask that hides nothing but the eyes and so shows everything else. An emperor wore it to see his kingdom ' +
      'without being seen, and saw only people looking back at him, which is the trouble with empires.',
  },
  {
    id: 'sarabanda',
    title: 'YO SOY SARABANDA',
    giver: { map: 'lowleaf_hollow', npc: 'bloom_piper_lit' },
    found: '"I play this one as a tune. It doesn\'t mind. It says its own name over and over, like a drum."',
    story:
      '"I am Sarabanda." A round brass face, all spirals, that announces itself to anyone who will listen and many ' +
      'who will not. It is a dance, and a spirit, and a very stubborn piece of metal, and it would like you to know all three.',
  },
  {
    id: 'redheart',
    title: 'THE LAST RED LIGHT OF GOD',
    giver: { map: 'tinderwick_house', npc: 'house_parent_after' },
    found: '"It was in the lamp-cupboard, behind the spare wicks. I think it\'s meant to be kept somewhere warm."',
    story:
      'A heart bound in blue thorns, flowering fire from the top. When the very last lamp in the world gutters, ' +
      'this is the colour it goes, a deep and stubborn red, and that is the moment someone always strikes another match.',
  },
  {
    id: 'stick',
    title: 'TERMS OF REFERENCE CHALLENGED',
    giver: { map: 'windward_stair_ii', npc: 'crag_tender_rounds' },
    found: '"Wedged in the rope-rail. A stick, painted on a card. Up here that counts as philosophy."',
    story:
      'A crooked stick, the kind a walker picks up and keeps for one hill. It was asked to be a measuring rod and ' +
      'refused on the grounds that nothing is straight. The committee is still meeting.',
  },
  {
    id: 'fogbird',
    title: 'WHY NOT WHIP THE FOG?',
    giver: { map: 'coldfog_marches_i', npc: 'marsh_hermit' },
    found: '"The fog brought it. Fog brings all sorts. Mostly regret. This was a nice change."',
    story:
      'A fat orange bird with a green-scaled belly and a grin, who got so tired of the marsh fog that it beat it with ' +
      'its wings like cream until the fog went stiff and stood up in peaks. The marsh folk ate it with spoons.',
  },
  {
    id: 'monkey',
    title: 'SUMMONING THE SPIRIT IN THE CAULDRON WITH A BALINESE FROG DANCE',
    giver: { map: 'lowleaf_bower', npc: 'bloom_guest_lit' },
    found: '"It fell out of a recipe book. The recipe was for soup. I think the card is the better recipe."',
    story:
      'A long green monkey dancing the frog dance from an island far over the sea: knees out, hands wide, round and ' +
      'round the cooking pot until the steam itself gets up and dances too. The soup was excellent. Nobody can say why.',
  },
  {
    id: 'bat',
    title: 'SNORT POPCORN',
    giver: { map: 'cinderhead_mine', npc: 'vigil_miner_a_lit' },
    found: '"Found it down the third gallery with a bat asleep on it. The bat let me have it. Eventually."',
    story:
      'A little blue bat who lived over the lantern-show tent and grew fat on dropped popcorn. When it laughs, ' +
      'which is often, it snorts, and a puff of popcorn comes out, and the whole front row laughs too.',
  },
  {
    id: 'goat',
    title: 'I WANT TO CREATE MY OWN LANGUAGE BASED ON REAL THINGS',
    giver: { map: 'wickstead_school', npc: 'teacher_types' },
    found: '"A pupil handed it in as homework. It was, I have to say, the best homework I\'ve had."',
    story:
      'A yellow goat that decided words were too slippery, and made a language out of things instead: a stone for ' +
      'no, a flower for yes, a boot for I am leaving. Conversations took a very long time and needed a cart.',
  },
  {
    id: 'bather',
    title: 'THIS MAY BE A DENIAL OF ACCESS SITUATION',
    giver: { map: 'tinderwick_bay', npc: 'bay_diver_after' },
    found: '"Floated by me in the bay. I followed it for a while. It knew where it was going better than I did."',
    story:
      'A cheerful lady floating on her back in the warm part of the bay, refusing to come out for anybody. The ' +
      'harbour-master wrote her a letter. She floated it back to him, folded into a little boat.',
  },
  {
    id: 'fool',
    title: 'NO HARM IN AN ALLOWED FOOL',
    giver: { map: 'pearlmoor_oldlight_1', npc: 'mime' },
    found: 'The mime opens an invisible box, takes out a very visible card, and bows.',
    story:
      'A little brass beast, the jester\'s mascot. In the old courts a licensed fool could tell the king anything, ' +
      'because it was only a joke, and everyone knew it was not. This one has told several kings exactly what they needed.',
  },
  {
    id: 'bones',
    title: "ANGEL BONE'S CONNECTED TO THE GOD BONE, GOD BONE'S CONNECTED TO THE BONE BONE, AND THE BONE BONE'S CONNECTED TO THE HAM BONE",
    giver: { map: 'pale_vault_undercroft', npc: 'undercroft_ward_a_after' },
    found: '"It was in the bone-crypt, singing. Well. It LOOKED like it was singing."',
    story:
      'A pair of golden legs from an old song about how everything is joined to everything else, sung by people ' +
      'putting a skeleton back together after a dance went on too long. It gets less holy the further down you go, ' +
      'which is the honest way round.',
  },
  {
    id: 'laughter',
    title: 'I FOUND MY RELIGION AND ITS PRAYER IS LAUGHTER',
    giver: { map: 'pearlmoor_oldlight_top', npc: 'moll_after' },
    found: 'Moll: "Tam had this in his greasepaint box for years. He\'d want it walking about. Go on."',
    story:
      'A man in a skirt and sunglasses who went looking for something to believe in, tried the quiet places, and ' +
      'finally found it at the back of a clowns\' tent with tears running down his face. He has said his prayers loudly ever since.',
  },
  {
    id: 'skin',
    title: 'SHAKE OFF THE DAY AND DANCE AROUND IN YOUR BONES',
    giver: { map: 'mourning_fields', npc: 'mournfields_ines_after' },
    found: '"It was on a grave out here, propped like a letter. The fields are glad of a dancer."',
    story:
      'A skeleton in a striped poncho and a red hat, one boot raised, a little bottle in his hand. On the night of ' +
      'the remembering-fires he takes off everything heavy and dances, and the people who loved him dance back.',
  },
  {
    id: 'crow',
    title: 'THE WORLD SEEMS TO BE SINKING INTO DUST',
    giver: { map: 'penumbra_ring', npc: 'gone_quiet_elder' },
    found: '"A crow dropped it at my feet. Crows trade. I gave it a button. Fair\'s fair."',
    story:
      'A black crow standing on the last dry hill, watching the dusk settle on everything like dust on a mantelpiece. ' +
      'Crows have seen the world end several times. They always stay to see what happens next.',
  },
  {
    id: 'nonsense',
    title: 'TRY TO MASTER NONSENSE',
    giver: { map: 'wickstead_green', npc: 'teacher_wicks' },
    found: '"Our curriculum, in one card. Somebody left it in the staff room. Very cheeky. Very correct."',
    story:
      'A serious young man in a brown coat who studied nonsense at the highest level. He passed every exam by ' +
      'answering the questions nobody had asked. He now teaches it, badly, which is the only way.',
  },
  {
    id: 'edges',
    title: "IT'S THE PEOPLE ON THE EDGES WHO CAPTURE THE TRUTH",
    giver: { map: 'wrackline_path', npc: 'wrackline_drifter_after' },
    found: '"Found it on the very edge of the wrack. Where else?"',
    story:
      'A player in shirt number double-nought who never got picked, never got the ball, and stood at the touchline ' +
      'every match for twenty years. He is the only one who saw what really happened in all of them.',
  },
  {
    id: 'cherub',
    title: 'YOU ALWAYS HAVE THE RIGHT TO REMAIN A MYSTERY',
    giver: { map: 'georgina_cottage', npc: 'georgina_after' },
    found: 'Georgina: "Isn\'t it DARLING? It came in a sunflower seed packet. I don\'t ask, darling. I just keep."',
    story:
      'A little winged cherub carrying a heart on a string, who turns up at weddings, funerals and fish markets and ' +
      'will not say why. People keep asking. It keeps smiling. Some questions are better as company than as answers.',
  },
  {
    id: 'lies',
    title: 'TELL ME SOME LIES',
    giver: { map: 'pearlmoor_oldlight_2', npc: 'late_a' },
    found: '"I found this in the tower, honest. ...I didn\'t. I made it. ...I didn\'t do that either."',
    story:
      'A cheerful red devil with a star in his hand who only wants a good story. True ones bore him. He sits by the ' +
      'fire and says "go on, then," and you tell him one, and somehow by the end of it you feel better.',
  },
  {
    id: 'cat',
    title: 'THE APOCALYPSE HAPPENED YESTERDAY',
    giver: { map: 'nightreach_home', npc: 'home_elder_lit' },
    found: '"The cat brought it in. The cat does not seem worried about anything, ever. I take my cue from her."',
    story:
      'A black cat, arched and unbothered. The end of the world came through the village yesterday afternoon. The ' +
      'cat slept through it, woke at teatime, and wanted feeding. So everyone fed her, and the world carried on.',
  },
  {
    id: 'delirium',
    title: 'THE CODE OF DELIRIUM PROVES TO HAVE AN EXTRAORDINARY FLUIDITY',
    giver: { map: 'sunvault_climb_iv', npc: 'hill_watcher' },
    found: '"Up here you get light-headed. That card made complete sense for about an hour. Your turn."',
    story:
      'A little round-hatted doll from a fever. It kept a codebook of everything the dreamer said that night, and ' +
      'found the words flowed into each other like rivers. In the morning the code was gone, but the doll was still there.',
  },
  {
    id: 'nun',
    title: 'IF THERE IS A GOD THEN I HAVE A FEW QUESTIONS TO ASK HIM',
    giver: { map: 'stillwater', npc: 'wall_elder' },
    found: '"I keep it in my prayer-book. I keep a lot of questions in there. This one has the best manners."',
    story:
      'A sister holding her book of hours, open at a page where she has written, very neatly, a list. Item one: the ' +
      'Long Dusk. Item two: wasps. She is a patient woman, and she has booked a long appointment.',
  },
  {
    id: 'blissful',
    title: 'A BLISSFUL MIND',
    giver: { map: 'lowleaf_lumenary', npc: 'sable_after' },
    found: 'Sable: "Somebody left it on the bloom-altar. I don\'t know whose mind it was. They should come back for it."',
    story:
      'A small winged figure with her hands folded and her eyes half closed, entirely content. She has no plans and ' +
      'no worries and nowhere she would rather be. People find this very difficult to be around.',
  },
  {
    id: 'puppets',
    title: 'RAISED BY PUPPETS AND LOST IN A WORLD OF GHOSTS',
    giver: { map: 'pearlmoor_oldlight_3', npc: 'punch_tuesday' },
    found: '"From the puppet booth. That\'s the way to do it. ...Sorry. Reflex."',
    story:
      'A little tin robot brought up backstage by the puppets, who taught it everything they knew, which was mostly ' +
      'falling over and getting up again. Out in the world everyone seemed see-through by comparison. It misses the strings.',
  },
  {
    id: 'truthlie',
    title: 'SOMETIMES I TELL THE TRUTH AND SOMETIMES I LIE',
    giver: { map: 'galehigh_inn', npc: 'guest_lit' },
    found: '"Won it at cards. Or I found it. One of those. You\'ll never know, will you?"',
    story:
      'A round, laughing, beaded figure who answers every question with perfect calm, and only half the answers are ' +
      'true. People come to him anyway. Working out which half is the real lesson.',
  },
  {
    id: 'poetic',
    title: 'SOMETIMES DOING SOMETHING POETIC CAN BECOME POLITICAL AND SOMETIMES DOING SOMETHING POLITICAL CAN BECOME POETIC',
    giver: { map: 'stillwater_home_b', npc: 'maren' },
    found: '"I found it tucked into a shutter. It made me open the shutter. I think that was the idea."',
    story:
      'A quiet man in a black coat who once walked across a whole town pushing a block of ice until it melted. It ' +
      'was only a walk. Then it was a protest. Then it was a poem. The puddle is still talked about.',
  },
  {
    id: 'pedal',
    title: 'JUST SHUT UP AND PEDAL',
    giver: { map: 'wickrun_crest', npc: 'runner_kid' },
    found: '"I found it on the downhill! It was going faster than me! ...You can have it. I need both hands."',
    story:
      'A bear cub on a tricycle at the top of a very long hill, full of reasons not to go. Wind, rain, knees. His ' +
      'grandad leaned down and said five words, and he is still going, and he has never been happier.',
  },
  {
    id: 'dragonfly',
    title: 'HOODOO VOODOO',
    giver: { map: 'saltreach_fen_i', npc: 'fen_eelwife' },
    found: '"Dragonfly charm. Fen folk swear by them. I swear AT them. Here — it\'s more yours than mine."',
    story:
      'A glass-winged dragonfly that the fen wives hang over doorways to stitch up bad luck. It darts about mending ' +
      'what it can, and charges nothing, and accepts payment only in pond-weed.',
  },
  {
    id: 'diver',
    title: "HE'S A CLOSET CHARISMATIC",
    giver: { map: 'undertide_iv', npc: 'undertide_diver_ondine' },
    found: 'Ondine: "Down in the deep a diver left this in a bottle. Sweetest man. Wouldn\'t say boo to a crab."',
    story:
      'A shy diver in a striped suit with a brass helmet, who will not speak above a whisper on land. Underwater, ' +
      'he is the life and soul of every reef. The fish adore him. He has never told anyone.',
  },
  {
    id: 'notgood',
    title: "I'M JUST NOT GOOD WITH PEOPLE I KNOW",
    giver: { map: 'pale_vault_inn', npc: 'guest_lit' },
    found: '"A stranger gave me this. Lovely conversation. Never seen them again. That\'s the best kind."',
    story:
      'A horned red devil, very polite to strangers, warm with shopkeepers, charming on long coach journeys. At home ' +
      'with his own family he cannot think of a single thing to say. He sends them postcards from the next room.',
  },
  {
    id: 'shrimp',
    title: 'I LIKE STORIES ABOUT SHRIMP',
    giver: { map: 'driftholm', npc: 'bram' },
    found: '"Fell out of the net-loft. You ever hear a good shrimp story? ...Me neither. That\'s why I like them."',
    story:
      'A pale spiralled shell, the castle of a shrimp who once ate a lamp-wick and glowed for a week. Islanders tell ' +
      'small stories about small things on long nights, and those turn out to be the stories that last.',
  },
  {
    id: 'seahorse',
    title: 'I WILL BE RARE FOR THOSE WHO CARE',
    giver: { map: 'driftholm_elder', npc: 'nan_creel' },
    found: 'Nan Creel: "My mother gave me this, and hers gave it her. Now it\'s you. Don\'t lose it, petal."',
    story:
      'A golden seahorse, curled tight, that hides in the weed from anyone in a hurry. To someone who sits still ' +
      'long enough to notice, it comes out and does a slow, proud turn. It is only rare to the rushing.',
  },
  {
    id: 'moths',
    title: 'CHAPEL OF MOTHS',
    giver: { map: 'mirelight_landing', npc: 'nell' },
    found: '"Found it in the ferry chapel, under a candle. The moths were all over it. They\'ve good taste."',
    story:
      'A blue painted skull with flowered cheeks, sitting in a little chapel where one candle burns all night. The moths ' +
      'come to it like a congregation. They are not afraid of the flame. They are devoted to it.',
  },
  {
    id: 'failure',
    title: 'A FAITH IN FAILURE',
    giver: { map: 'penumbra_underways_b1', npc: 'clemency' },
    found: 'Clemency: "I have failed at almost everything down here, child. This card kept me company through all of it."',
    story:
      'A little pink angel, mid-tumble, wings all wrong. She has fallen off every cloud she ever stood on. She gets ' +
      'up every time, a bit better at falling, and that is the only kind of flying she has ever needed.',
  },
  {
    id: 'rooster',
    title: "AIN'T NOBODY'S BUSINESS IF YOU DO",
    giver: { map: 'galehigh_lumenary', npc: 'hall_festival' },
    found: '"Festival bunting had this pegged on it. Bright little bird. Doesn\'t care who\'s looking."',
    story:
      'A black painted rooster with hearts on his breast and a red comb like a flag. He crows when he likes, struts ' +
      'where he likes, and when the neighbours complain he crows a little louder, very sweetly, at them.',
  },
  {
    id: 'seal',
    title: 'THE CARPET IS PURRING',
    giver: { map: 'dimglass_coast_ii', npc: 'wayfarer_a_after' },
    found: '"It was on the flats with a seal lying on it. The seal was purring. I swear it was purring."',
    story:
      'A seal balancing a ball on its nose in a warm front room, so content on the rug by the fire that the rug began to ' +
      'purr. Nobody in the house has ever been sure which of them it was.',
  },
  {
    id: 'loon',
    title: 'SYNCOPATED, AGITATED, PURPLE MOON, WHITE LOON',
    giver: { map: 'lanternway_nightreach', npc: 'lane_lamplighter_a' },
    found: '"Hung on a lamp-post like a ticket. It had a rhythm to it. I\'ve been humming it for weeks."',
    story:
      'A red dancer in a straw sun-hat, stamping out a tune that never quite lands on the beat, under a purple ' +
      'moon, while a white water-bird calls along off-key. It should not work. It is the best song on the lake.',
  },
  {
    id: 'pyramid',
    title: 'SOMETIMES THE TONGUE IS TIRED',
    giver: { map: 'crossroads_inn', npc: 'hesper' },
    found: 'Hesper: "A guest left it under her teacup. She\'d talked all night. I think she was apologising."',
    story:
      'A little blue pendant, pointed like a pyramid, worn by a storyteller who talked from one winter to the next. One ' +
      'evening she simply stopped, put her tongue to bed, and let the quiet say the rest. It was her best story.',
  },
  {
    id: 'obsession',
    title: 'MEMORY AND OBSESSION',
    giver: { map: 'pale_vault_home', npc: 'home_elder_lit' },
    found: '"Kept it in the button tin for years. Couldn\'t stop looking at it. Better you take it now."',
    story:
      'A tin heart under a crown, pricked all over with little holes from being pinned and unpinned. A woman wore it ' +
      'for forty years for someone she would not stop remembering. The remembering wore the tin thin. It never wore out.',
  },
  {
    id: 'brujas',
    title: 'NOCHE DE BRUJAS',
    giver: { map: 'rimeway_fold', npc: 'tender_hale' },
    found: '"Found it in the snow by the Rime Gate on the longest night. The witches must\'ve dropped it."',
    story:
      'The witches\' night: one night a year, when the moon comes up warm as a peach and every old woman in the ' +
      'mountains goes out flying, just to feel the wind. In the morning they come home and make everyone pancakes.',
  },
  {
    id: 'transition',
    title: "REMEMBER I NEED SOME SPIRITUAL TRANSITION TIME, THAT'S WHY I HAVE SO MUCH TROUBLE LEAVING THE HOUSE",
    giver: { map: 'stillwater_shutter', npc: 'inn_guest' },
    found: '"I\'ve been meaning to go out and give this to somebody for weeks. And here you are. You came in. Perfect."',
    story:
      'A woman in a long dress standing just inside her own front door, coat on, ready to go out for the last three ' +
      'hours. She will go. She simply has to finish arriving at the idea first. The world can wait. It usually does.',
  },
];

export const MILAGROS_BY_GIVER = new Map(
  MILAGROS.filter((c) => c.giver).map((c) => [`${c.giver!.map}:${c.giver!.npc}`, c] as const),
);
