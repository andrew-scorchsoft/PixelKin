/**
 * THE BOOJI-WOOJI MAN MILAGRO CARDS (2026-10) — Paul's own painted cards, recreated
 * from photos of the real deck (art: assets/milagros/ via tools/assets/gen_milagros.py
 * and, where the model refused, tools/assets/milagro_photo.py straight from the photo;
 * served from public/assets/milagros/<id>.webp).
 *
 * How they reach you: the Booji-Wooji Man left his cards lying about for strangers to
 * find, so 53 people across Vesperholm each hold one (`giver`). ~40 sit on the South path
 * (Tinderwick, the orchard, the coast road, Pearlmoor, the Old Light, the Lifting House,
 * the Wanderwood, Wayward Rise, Paul's house, the fair) and the rest in the wider world and hand
 * it over the first time you finish talking to them (WorldScene.maybeGiveMilagro). Each
 * giver is someone whose world the card belongs to, and shares something Paul would
 * enjoy as they do (a cup, a song, a bun, a good story). The card plays a small reveal
 * ceremony and its STORY (a guess at what's behind it), then lives in the pack: pause
 * menu -> MILAGROS. Paul's "Your cards?" gives the BOX (flag:milagro_pack): its lore
 * card explains the deck, and the first card, DESASOSIEGO.
 *
 * Hidden real-people content like the rest of Paul's: never in the changelog, guide or
 * music page. The card phrases are Paul's own; `altered` cards differ from his original
 * art (a disclaimer is baked onto the card by gen_milagros.py --pack).
 */

export interface MilagroCard {
  /** Art stem (public/assets/milagros/<id>.webp) and the flag suffix. */
  id: string;
  /** The phrase lettered round the card's border. */
  title: string;
  /** Who has it: the NPC placement id on that map. */
  giver?: { map: string; npc: string };
  /** Where to look, shown against the card's back in the pack until it's found. */
  hint: string;
  /** What the giver says as they hand it over (one box each). */
  found?: string[];
  /** The art differs from Paul's original (baked note on the card + a line in the viewer). */
  altered?: boolean;
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
    hint: 'Pearlmoor: someone at the dark lamp at the very end of the breakwater.',
    story:
      'The oldest card in the box, and the only one with no picture of a thing: just a small flame that will not ' +
      'sit still. It is the word for the restless unease that paces the kitchen at night until you get up and ' +
      'make something. Paul says it is not a sickness. It is the cure, turning up early. Every other card in the ' +
      'box was painted because of this one.',
  },
  {
    id: 'dogtag',
    title: 'I WONDER AT WHAT POINT THE FORM OF MY LIFE BECAME ITS CONTENT, DOUBLING BACK ON ITSELF?',
    giver: { map: 'tinderwick', npc: 'lt_old_fisher' },
    hint: 'Tinderwick: the old fisher who remembers the drowned village.',
    found: [
      '"Came up in my net off the drowned roofs, tied to a cork. Pretty, but it\'s no use to a fish."',
      '"The old village had a man who wore one of these his whole life. Best fish stew on the coast. I still ' +
        'make it his way, Fridays."',
    ],
    altered: true,
    story:
      'A tag of the sort a sailor wears so the sea can send him home. This one was worn so long that the name ' +
      'rubbed off it, and the man kept wearing it anyway: the tag stopped saying who he was and started being ' +
      'who he was. Somewhere along the way the shape of a life becomes the life. He noticed on a Tuesday, and ' +
      'painted it.',
  },
  {
    id: 'fish',
    title: 'DON\'T GET TOO CLOSE',
    giver: { map: 'gullwrack_hut', npc: 'hut_keeper' },
    hint: 'Gullwrack Rock: whoever keeps the bothy.',
    found: [
      '"Washed up in a bottle, eleventh winter in a row something has. This time a spotted fish that says keep ' +
        'back."',
      '"Gulls agree with it. Here: card for you, and a crust of the bothy loaf for the gulls, so they leave your ' +
        'hat alone."',
    ],
    story:
      'A spotted fish, every spot an eye. It swims a careful distance from everyone, not because it is unkind ' +
      'but because it can see them all at once, and that is a great deal to look at. It is the best company in ' +
      'the world, from about an arm\'s length away.',
  },
  {
    id: 'spool',
    title: 'FEAR SELLS',
    giver: { map: 'stillwater_lampmaker', npc: 'lampmaker' },
    hint: 'Stillwater: the lampmaker of the quiet village.',
    found: [
      '"Found it wedged in my thread-drawer. I don\'t sell fear. Shutters, mostly. ...Same thing, some days."',
    ],
    story:
      'An empty cotton spool. All the thread has been sold off, yard by yard, to people frightened of coming ' +
      'undone. The peddler did very well. The spool kept the hole in the middle, which was the only part worth ' +
      'having.',
  },
  {
    id: 'shadowdoll',
    title: 'I MAY NOT BE THE CENTRE OF THE UNIVERSE, BUT I\'M WITHIN WALKING DISTANCE OF IT',
    giver: { map: 'tinderwick_shop', npc: 'shopkeeper' },
    hint: 'Tinderwick: the shopkeeper.',
    found: [
      '"Found this under the counter when I swept up. A little shadow with button eyes. It\'s been sat there like ' +
        'it owned the place."',
      '"Take it, and a barley-sugar from the jar. On the house. Shadows like company."',
    ],
    altered: true,
    story:
      'A little shadow-sprite with button eyes, the kind that follows a child home from the lamplighting. It ' +
      'knows it is not the most important thing in any room. It also knows exactly how many steps it would take ' +
      'to get there.',
  },
  {
    id: 'dancer',
    title: 'I\'VE HAD A HOLE IN MY HEART FOR SO LONG!',
    giver: { map: 'pearlmoor_point', npc: 'ione' },
    hint: 'Lightkeeper\'s Point: the lightkeeper at the Point.',
    found: [
      '"Off the island boat, years back. The dancer who\'d sailed every port of the Farlamp run left it on the ' +
        'rail."',
      '"She said the hole in her heart was where the music got in. I keep a fiddle tune of hers. I\'ll hum it, if ' +
        'you\'re ever back."',
    ],
    story:
      'She danced on a boat that went round the islands, and every port took a little piece of her heart, until ' +
      'there was a space in it shaped like the sea. She says it is not an injury. It is where the music gets in.',
  },
  {
    id: 'whistle',
    title: 'A SCREAM OF MUTENESS',
    giver: { map: 'stillwater_quiet_hall', npc: 'hall_keeper' },
    hint: 'Stillwater: the keeper of the quiet hall.',
    found: [
      'They hold it out without a word, finger to their lips. The quiet hall keeps its quiet.',
    ],
    story:
      'A clay whistle, green as pond-weed, that no one has ever managed to blow a note from. You put your whole ' +
      'chest into it and nothing comes out, and that nothing is the loudest thing you have ever heard.',
  },
  {
    id: 'barkingman',
    title: 'CAN YOU HEAR THE DOGS BARKING?',
    giver: { map: 'dimglass_coast', npc: 'egg_walker' },
    hint: 'Dimglass Coast: a walker with a sandwich.',
    found: [
      '"Funny old card. A fellow in a green coat, hand to his ear. I hear dogs barking on this coast that aren\'t ' +
        'there."',
      '"Somebody left it on the bench where I eat my sandwiches. Cheese and pickle. Want half? You can have the ' +
        'card AND half."',
    ],
    altered: true,
    story:
      'An old man in a green coat who hears dogs that nobody else can. He says they bark at whatever is coming ' +
      'up the road before it arrives: weather, letters, good news. He tilts his head and grins, and three days ' +
      'later the thaw comes.',
  },
  {
    id: 'taxi',
    title: 'CATCH A RIDE ON THE VOODOO TAXI',
    giver: { map: 'dimglass_coast_ii', npc: 'oldlight_hint_road' },
    hint: 'Dimglass Coast: a road-joker heading for the Point.',
    found: [
      '"Three clockwork lamplighters walk into a cab— no, listen. This was on the cab seat. Blue token, stamped ' +
        'OP."',
      '"I asked the driver what it\'s for. He said: the ride\'s free, the stories cost extra. Best bargain I ever ' +
        'got."',
    ],
    story:
      'A round blue token stamped OP: the fare for a cab that only runs after midnight. You get in, it does not ' +
      'ask where you are going, and it takes you somewhere better. The driver tells stories the whole way. ' +
      'Nobody has ever paid more than one token, and nobody has ever minded the detour.',
  },
  {
    id: 'cowboy',
    title: 'CUIDA TUS DIENTES COMO TUS ARMAS',
    giver: { map: 'lowleaf_hollow', npc: 'marisol' },
    hint: 'Lowleaf Hollow: the cook from the sunny country.',
    found: [
      'Marisol: "Cuida tus dientes como tus armas. Look after your teeth like your weapons! My grandmother said ' +
        'it every night."',
      '"A traveller paid for a plate of pozole with this card. I think he got the better deal, but don\'t tell ' +
        'him. Take a spoon of salsa with it."',
    ],
    story:
      '"Look after your teeth like you look after your weapons." A little tin cowboy with his pistol raised, who ' +
      'in forty years of painted gunfights never once fired it. He did floss. Every night. It is the reason he ' +
      'is still smiling.',
  },
  {
    id: 'pig',
    title: 'GLOSSOLALIA',
    giver: { map: 'paul_house_3', npc: 'lottie' },
    hint: 'A crooked house up past the wood, in the attic: a girl who loves pigs (and chickens, separately).',
    found: [
      'Lottie: "LOOK. A GOLDEN PIG. It says GLOSSOLALIA, which Grandad says is when you talk and talk and nobody ' +
        'understands. That\'s ME."',
      '"You can have it, because you\'re my friend. I\'ve drawn you a pig as well. It\'s on the back of the toast. ' +
        'Eat round it."',
    ],
    story:
      'A golden pig that speaks in tongues: whole sermons of grunts that sound, if you are tired enough, like ' +
      'something important. People came from three valleys to listen. The pig only ever wanted an apple.',
  },
  {
    id: 'stringy',
    title: 'ART IN THE SERVICE OF DEGENERATE DISCOURSE',
    giver: { map: 'pearlmoor_oldlight_2', npc: 'late_b' },
    hint: 'The Old Light: another latecomer to the show.',
    found: [
      '"Pinned to the back of a stage flat. The critics called the show degenerate. The show called the critics ' +
        'worse. Lovely night."',
      '"Take the card. Take a custard pie too, they\'re for throwing but they\'re also very nice."',
    ],
    story:
      'A tangle of golden string that started out as a beast and argued itself into a knot. It was painted for a ' +
      'gallery that called it rude, and so it went happily and rudely on its way, being argued about in ' +
      'tea-houses forever.',
  },
  {
    id: 'wetnumbers',
    title: 'MY ROOM SMELLS OF WET NUMBERS',
    giver: { map: 'pearlmoor_shop', npc: 'chandler' },
    hint: 'Pearlmoor Chandlery: the chandler.',
    found: [
      '"Tucked in my stock-book, damp as the harbour. MY ROOM SMELLS OF WET NUMBERS. So does my shop, after a ' +
        'sea-fog."',
      '"I\'ve added it up twice and it still comes out as yours. Have a tin of the good mints with it."',
    ],
    story:
      'A clerk who kept the accounts of a damp office for thirty years, until the sums soaked into the walls. On ' +
      'wet mornings the whole room smells of sevens. He let his hair grow, wore his good boots, and walked out ' +
      'to find a room that smells of nothing at all.',
  },
  {
    id: 'bottle',
    title: 'FALL INTO THE NIGHT SKY AND CHASE AFTER KOKOPELLI',
    giver: { map: 'pearlmoor_wanderwood_far', npc: 'wander_mags' },
    hint: 'Beyond the old wood: whoever keeps the bar beyond the wood.',
    found: [
      'Mags: "A customer left this on the bar with a note: FOR THE NEXT ONE WHO WANDERS IN. That\'s you, love."',
      '"A blue bottle full of night. Chase it if you like. Or sit and have a glass of something warm first. I ' +
        'recommend the second."',
    ],
    story:
      'A blue bottle that holds a little of the night, stoppered. Uncork it and lie down on the grass, and you ' +
      'fall upward after the hunched flute-player who walks the sky playing everything into spring. You will not ' +
      'catch him. That is not the point.',
  },
  {
    id: 'eyemask',
    title: 'EMPIRE OF THE EYE',
    giver: { map: 'saltreach_fen_i', npc: 'ansel' },
    hint: 'Saltreach Fen: the ferryman of the blue lights.',
    found: [
      '"Left on the ferry\'s little stage between crossings. Every passenger thinks they\'re the one being ' +
        'watched."',
      '"Forty years on this water and the best show is still the faces in the blue light. Take it. I\'ve seen ' +
        'it."',
    ],
    story:
      'A mask that hides nothing but the eyes and so shows everything else. An emperor wore it to see his ' +
      'kingdom without being seen, and saw only people looking back at him, which is the trouble with empires.',
  },
  {
    id: 'sarabanda',
    title: 'YO SOY SARABANDA',
    giver: { map: 'lowleaf_hollow', npc: 'bloom_piper_lit' },
    hint: 'Lowleaf Hollow: a piper (once the Verdant\'s relit).',
    found: [
      '"I play this one as a tune. It doesn\'t mind. It says its own name over and over, like a drum."',
    ],
    story:
      '"I am Sarabanda." A round brass face, all spirals, that announces itself to anyone who will listen and ' +
      'many who will not. It is a dance, and a spirit, and a very stubborn piece of metal, and it would like you ' +
      'to know all three.',
  },
  {
    id: 'redheart',
    title: 'THE LAST RED LIGHT OF GOD',
    giver: { map: 'tinderwick_house', npc: 'house_parent_after' },
    hint: 'Tinderwick, at home: the apprentice\'s own home.',
    found: [
      '"I found this in the lamp-cupboard, behind the spare wicks. Somebody\'s little painting of a heart on ' +
        'fire."',
      '"Keep it somewhere warm, love. And take a slice of the seed-cake while you\'re at it: nobody walks out of ' +
        'this house hungry."',
    ],
    story:
      'A heart bound in blue thorns, flowering fire from the top. When the very last lamp in the world gutters, ' +
      'this is the colour it goes, a deep and stubborn red, and that is the moment someone always strikes ' +
      'another match.',
  },
  {
    id: 'stick',
    title: 'TERMS OF REFERENCE CHALLENGED',
    giver: { map: 'duskapple_orchard', npc: 'tamsin' },
    hint: 'Duskapple Orchard: someone pruning the orchard.',
    found: [
      '"A crooked stick, painted on a card. I found it hooked on the old tree while I was pruning. Terms of ' +
        'reference challenged, it says."',
      '"The tree challenged mine years ago. Take the card, and an apple. Duskapples are best eaten walking."',
    ],
    story:
      'A crooked stick, the kind a walker picks up and keeps for one hill. It was asked to be a measuring rod ' +
      'and refused on the grounds that nothing is straight. The committee is still meeting.',
  },
  {
    id: 'fogbird',
    title: 'WHY NOT WHIP THE FOG?',
    giver: { map: 'dimglass_coast', npc: 'egg_netmender' },
    hint: 'Dimglass Coast: a netmender out on the flats.',
    found: [
      '"Out on the flats, the fog came in so thick I could have whipped it. Next morning, this was in my nets."',
      '"Fat orange bird, grinning. I laughed so hard I dropped my flask. Tea everywhere. Worth it. Here."',
    ],
    story:
      'A fat orange bird with a green-scaled belly and a grin, who got so tired of the marsh fog that it beat it ' +
      'with its wings like cream until the fog went stiff and stood up in peaks. The marsh folk ate it with ' +
      'spoons.',
  },
  {
    id: 'monkey',
    title: 'SUMMONING THE SPIRIT IN THE CAULDRON WITH A BALINESE FROG DANCE',
    giver: { map: 'wakeful_fair', npc: 'goer_a' },
    hint: 'A striped tent up on the hill: a fair-goer near the sugar bowl.',
    found: [
      '"Summoning the spirit in the cauldron! That\'s exactly what it\'s like in here. A monkey dancing round the ' +
        'coffee urn."',
      '"Found it in the sugar bowl. Take it. Take a sugar lump. Take three, you\'ll need them."',
    ],
    story:
      'A long green monkey dancing the frog dance from an island far over the sea: knees out, hands wide, round ' +
      'and round the cooking pot until the steam itself gets up and dances too. The soup was excellent. Nobody ' +
      'can say why.',
  },
  {
    id: 'bat',
    title: 'SNORT POPCORN',
    giver: { map: 'tinderwick', npc: 'fair_piper' },
    hint: 'Tinderwick: the fair\'s piper (once the Ember\'s relit).',
    found: [
      '"Fell out of the popcorn barrel at the fair! A little bat that laughs through its nose. I\'ve played it a ' +
        'jig. It approved."',
      '"Go on, take it. And take a bag of the honey popcorn for the road, that\'s the real prize tonight."',
    ],
    story:
      'A little blue bat who lived over the lantern-show tent and grew fat on dropped popcorn. When it laughs, ' +
      'which is often, it snorts, and a puff of popcorn comes out, and the whole front row laughs too.',
  },
  {
    id: 'goat',
    title: 'I WANT TO CREATE MY OWN LANGUAGE BASED ON REAL THINGS',
    giver: { map: 'pearlmoor_allotment', npc: 'anth_done' },
    hint: 'Hillside Allotments: the allotment\'s other half.',
    found: [
      'Anth: "A goat that makes its own language out of real things. Rod and I have spoken nothing but marrows ' +
        'for forty years."',
      '"It turned up in the seed tin. Have it, and a jar of my chutney. That\'s marrow too. Everything here is ' +
        'marrow."',
    ],
    story:
      'A yellow goat that decided words were too slippery, and made a language out of things instead: a stone ' +
      'for no, a flower for yes, a boot for I am leaving. Conversations took a very long time and needed a cart.',
  },
  {
    id: 'bather',
    title: 'THIS MAY BE A DENIAL OF ACCESS SITUATION',
    giver: { map: 'pearlmoor_inn', npc: 'fisher_lit' },
    hint: 'Pearlmoor Quayside Inn: a fisher at the inn (once the Tide\'s relit).',
    found: [
      '"Floated up to my boat in a bottle, off the warm bit of the bay. A lady who won\'t come out of the water."',
      '"Can\'t say I blame her. Sit down, the chowder\'s on. This card\'s been the talk of the bar all week."',
    ],
    altered: true,
    story:
      'A cheerful lady floating on her back in the warm part of the bay, refusing to come out for anybody. The ' +
      'harbour-master wrote her a letter. She floated it back to him, folded into a little boat.',
  },
  {
    id: 'fool',
    title: 'NO HARM IN AN ALLOWED FOOL',
    giver: { map: 'pearlmoor_oldlight_1', npc: 'mime' },
    hint: 'The Old Light: a performer who never says a word.',
    found: [
      'The mime opens an invisible box, takes out a very visible card, and bows. Then he mimes eating an ' +
        'enormous sandwich, and offers you half.',
    ],
    story:
      'A little brass beast, the jester\'s mascot. In the old courts a licensed fool could tell the king ' +
      'anything, because it was only a joke, and everyone knew it was not. This one has told several kings ' +
      'exactly what they needed.',
  },
  {
    id: 'bones',
    title: 'ANGEL BONE\'S CONNECTED TO THE GOD BONE, GOD BONE\'S CONNECTED TO THE BONE BONE, AND THE BONE BONE\'S CONNECTED TO THE HAM BONE',
    giver: { map: 'pale_vault_undercroft', npc: 'undercroft_ward_a_after' },
    hint: 'Pale Vault Undercroft: a ward under the vault (after a bout).',
    found: [
      '"It was in the bone-crypt, singing. Well. It LOOKED like it was singing."',
    ],
    story:
      'A pair of golden legs from an old song about how everything is joined to everything else, sung by people ' +
      'putting a skeleton back together after a dance went on too long. It gets less holy the further down you ' +
      'go, which is the honest way round.',
  },
  {
    id: 'laughter',
    title: 'I FOUND MY RELIGION AND ITS PRAYER IS LAUGHTER',
    giver: { map: 'pearlmoor_oldlight_top', npc: 'moll_after' },
    hint: 'The Old Light: Tam\'s old stage partner, at the very top.',
    found: [
      'Moll: "Tam had this in his greasepaint box for years. He\'d want it walking about. He\'d want you laughing. ' +
        'Go on."',
    ],
    story:
      'A man in a skirt and sunglasses who went looking for something to believe in, tried the quiet places, and ' +
      'finally found it at the back of a clowns\' tent with tears running down his face. He has said his prayers ' +
      'loudly ever since.',
  },
  {
    id: 'skin',
    title: 'IT AIN\'T NO SIN TO TAKE OFF YOUR SKIN AND DANCE AROUND IN YOUR BONES',
    giver: { map: 'pearlmoor_wanderwood', npc: 'hob_done' },
    hint: 'The old wood behind the quay: the wanderer who is NOT lost.',
    found: [
      'Hob: "Found it on a root in the glade the night the lamp caught. A skeleton dancing in his poncho. I ' +
        'danced too. Don\'t tell anyone."',
      '"I\'m not lost, mind. I\'m dancing. There\'s a difference. Here: card, and a handful of the wood\'s ' +
        'blackberries."',
    ],
    story:
      'A skeleton in a striped poncho and a red hat, one boot raised, a little bottle in his hand. On the night ' +
      'of the remembering-fires he takes off everything heavy and dances, and the people who loved him dance ' +
      'back.',
  },
  {
    id: 'crow',
    title: 'THE WORLD SEEMS TO BE SINKING INTO DUST',
    giver: { map: 'saltreach_fen_i', npc: 'peril_fen_leaver' },
    hint: 'Saltreach Fen: someone packing up to leave the fen.',
    found: [
      '"A crow dropped it on my cart this morning as I loaded up. The world seems to be sinking into dust, eh? ' +
        'Crows know."',
      '"I\'m off to my sister\'s for a while. She does a pie that could talk a body out of anything. You keep the ' +
        'card."',
    ],
    story:
      'A black crow standing on the last dry hill, watching the dusk settle on everything like dust on a ' +
      'mantelpiece. Crows have seen the world end several times. They always stay to see what happens next.',
  },
  {
    id: 'nonsense',
    title: 'TRY TO MASTER NONSENSE',
    giver: { map: 'wickstead_green', npc: 'teacher_wicks' },
    hint: 'Wickstead Green: a teacher at the school.',
    found: [
      '"Our curriculum, in one card. Somebody left it in the staff room. Very cheeky. Very correct."',
    ],
    story:
      'A serious young man in a brown coat who studied nonsense at the highest level. He passed every exam by ' +
      'answering the questions nobody had asked. He now teaches it, badly, which is the only way.',
  },
  {
    id: 'edges',
    title: 'IT\'S THE PEOPLE ON THE EDGES WHO CAPTURE THE TRUTH',
    giver: { map: 'wrackline_path', npc: 'wrackline_drifter_after' },
    hint: 'Wrackline Path: a drifter on the wrack (after a bout).',
    found: [
      '"Found it on the very edge of the wrack. Where else? The best things wash up on the edges."',
      '"There\'s a song about that, the drifters\' one. Low and slow. I\'ll sing you a verse if you sit."',
    ],
    story:
      'A player in shirt number double-nought who never got picked, never got the ball, and stood at the ' +
      'touchline every match for twenty years. He is the only one who saw what really happened in all of them.',
  },
  {
    id: 'cherub',
    title: 'YOU ALWAYS HAVE THE RIGHT TO REMAIN A MYSTERY',
    giver: { map: 'tinderwick', npc: 'fair_kid' },
    hint: 'Tinderwick: a lantern-mad child at the fair.',
    found: [
      '"It was tangled in the fair bunting! A baby angel with a heart on a string. I asked it what it was for. ' +
        'It didn\'t say."',
      '"Gran says some things you\'re meant to wonder about forever. Like the toffee apples. How do they GET the ' +
        'toffee on?"',
    ],
    story:
      'A little winged cherub carrying a heart on a string, who turns up at weddings, funerals and fish markets ' +
      'and will not say why. People keep asking. It keeps smiling. Some questions are better as company than as ' +
      'answers.',
  },
  {
    id: 'lies',
    title: 'TELL ME SOME LIES',
    giver: { map: 'pearlmoor_oldlight_2', npc: 'late_a' },
    hint: 'The Old Light: a latecomer to the show.',
    found: [
      '"I found this in the tower, honest. ...I didn\'t. I made it. ...I didn\'t do that either."',
      '"Tell you what, it\'s yours if you tell me a good lie back. ...Too slow! Have it anyway."',
    ],
    story:
      'A cheerful red devil with a star in his hand who only wants a good story. True ones bore him. He sits by ' +
      'the fire and says "go on, then," and you tell him one, and somehow by the end of it you feel better.',
  },
  {
    id: 'cat',
    title: 'THE APOCALYPSE HAPPENED YESTERDAY',
    giver: { map: 'tinderwick', npc: 'peril_neighbour' },
    hint: 'Tinderwick: a worried neighbour.',
    found: [
      '"Funny thing. The night that star went out over the sea, this was pushed under my door. A black cat that ' +
        'couldn\'t care less."',
      '"My own cat slept through the whole fuss and wanted her supper. I\'ve decided she\'s right. Here, you have ' +
        'it. I\'ve got her."',
    ],
    story:
      'A black cat, arched and unbothered. The end of the world came through the village yesterday afternoon: a ' +
      'star went out, the neighbours stood in the street in their slippers. The cat slept through it, woke at ' +
      'teatime and wanted feeding. So everyone fed her, and put the kettle on, and the world carried on.',
  },
  {
    id: 'delirium',
    title: 'THE CODE OF DELIRIUM PROVES TO HAVE AN EXTRAORDINARY FLUIDITY',
    giver: { map: 'pearlmoor_quay', npc: 'oldlight_hint_luddite' },
    hint: 'Pearlmoor Quay: someone suspicious of the thinking machine.',
    found: [
      '"Came out of that thinking machine up the Old Light, they say. Printed on its paper. A code of delirium."',
      '"Machines writing poems. I ask you. ...It\'s quite a good poem. Don\'t tell anyone I said so."',
    ],
    story:
      'A little round-hatted doll from a fever, or from a machine that dreams in punched paper. It kept a ' +
      'codebook of everything the dreamer said one long night, and found the words flowed into each other like ' +
      'rivers. In the morning the code was gone, but the doll was still there, smiling like it had got the joke.',
  },
  {
    id: 'nun',
    title: 'IF THERE IS A GOD THEN I HAVE A FEW QUESTIONS TO ASK HIM',
    giver: { map: 'stillwater', npc: 'wall_elder' },
    hint: 'Stillwater: an elder by the village wall.',
    found: [
      '"I keep it in my prayer-book. I keep a lot of questions in there. This one has the best manners."',
    ],
    story:
      'A sister holding her book of hours, open at a page where she has written, very neatly, a list. Item one: ' +
      'the Long Dusk. Item two: wasps. She is a patient woman, and she has booked a long appointment.',
  },
  {
    id: 'blissful',
    title: 'A BLISSFUL MIND',
    giver: { map: 'wakeful_fair', npc: 'dennis' },
    hint: 'A striped tent up on the hill: the calmest man at the fair.',
    found: [
      'Dennis: "A blissful mind. Found it under my cup. It\'s the decaf, you see. Nobody believes me. Look how ' +
        'calm I am."',
      '"Have the card. Have a cup of decaf. Have a little sit-down. ...Bliss."',
    ],
    story:
      'A small winged figure with her hands folded and her eyes half closed, entirely content. She has no plans ' +
      'and no worries and nowhere she would rather be. People find this very difficult to be around.',
  },
  {
    id: 'puppets',
    title: 'RAISED BY PUPPETS AND LOST IN A WORLD OF GHOSTS',
    giver: { map: 'pearlmoor_oldlight_3', npc: 'punch_tuesday' },
    hint: 'The Old Light: the puppet booth.',
    found: [
      '"From the puppet booth. That\'s the way to do it. ...Sorry. Reflex."',
      '"There\'s sausages backstage if you want one. There are always sausages. Nobody knows why."',
    ],
    story:
      'A little tin robot brought up backstage by the puppets, who taught it everything they knew, which was ' +
      'mostly falling over and getting up again. Out in the world everyone seemed see-through by comparison. It ' +
      'misses the strings.',
  },
  {
    id: 'truthlie',
    title: 'SOMETIMES I TELL THE TRUTH AND SOMETIMES I LIE',
    giver: { map: 'pearlmoor_lifting_house', npc: 'abdul_after' },
    hint: 'The building at the top of the quay: a lifter with four true stories.',
    found: [
      'Abdul: "Four stories, all true. This card makes it five, and I can\'t vouch for that one. Somebody left it ' +
        'in the chalk bucket."',
      '"Sometimes I tell the truth and sometimes I lie. Well. I\'ll tell you the truth about the protein ' +
        'flapjacks: they\'re delicious. Have one."',
    ],
    story:
      'A round, laughing, beaded figure who answers every question with perfect calm, and only half the answers ' +
      'are true. People come to him anyway. Working out which half is the real lesson.',
  },
  {
    id: 'poetic',
    title: 'SOMETIMES DOING SOMETHING POETIC CAN BECOME POLITICAL AND SOMETIMES DOING SOMETHING POLITICAL CAN BECOME POETIC',
    giver: { map: 'stillwater_home_b', npc: 'maren' },
    hint: 'Stillwater: someone behind a shutter.',
    found: [
      '"I found it tucked into a shutter. It made me open the shutter. I think that was the idea."',
    ],
    story:
      'A quiet man in a black coat who once walked across a whole town pushing a block of ice until it melted. ' +
      'It was only a walk. Then it was a protest. Then it was a poem. The puddle is still talked about.',
  },
  {
    id: 'pedal',
    title: 'JUST SHUT UP AND PEDAL',
    giver: { map: 'pearlmoor_lifting_house', npc: 'andy_after' },
    hint: 'The building at the top of the quay: the runner who never gets off the treadmill.',
    found: [
      'Andy, still running: "JUST SHUT UP AND PEDAL. Found it tucked in the treadmill\'s cup-holder. Best advice ' +
        'I\'ve ever had."',
      '"Take it! I can\'t, I\'m mid-mile. There\'s banana bread on the side. Have some. Have mine. I\'m going to ' +
        'need it afterwards."',
    ],
    altered: true,
    story:
      'A bear cub on a tricycle at the top of a very long hill, full of reasons not to go. Wind, rain, knees. ' +
      'His grandad leaned down and said five words, and he is still going, and he has never been happier.',
  },
  {
    id: 'dragonfly',
    title: 'HOODOO VOODOO',
    giver: { map: 'saltreach_fen_i', npc: 'fen_warden' },
    hint: 'Saltreach Fen: the fen\'s warden.',
    found: [
      '"Dragonfly charm. Fen wives hang them over doors to stitch up bad luck. Somebody hung this one over MY ' +
        'door."',
      '"I\'ve plenty of bad luck to go round. Have the luck instead. And a twist of smoked eel, if you\'ve the ' +
        'stomach."',
    ],
    story:
      'A glass-winged dragonfly that the fen wives hang over doorways to stitch up bad luck. It darts about ' +
      'mending what it can, and charges nothing, and accepts payment only in pond-weed.',
  },
  {
    id: 'diver',
    title: 'HE\'S A CLOSET CHARISMATIC',
    giver: { map: 'undertide_iv', npc: 'undertide_diver_ondine' },
    hint: 'The Undertide: the Drowned Stair: a diver in the deepest tide-race.',
    found: [
      'Ondine: "Down in the deep a diver left this in a bottle. Sweetest man. Wouldn\'t say boo to a crab."',
    ],
    story:
      'A shy diver in a striped suit with a brass helmet, who will not speak above a whisper on land. ' +
      'Underwater, he is the life and soul of every reef. The fish adore him. He has never told anyone.',
  },
  {
    id: 'notgood',
    title: 'I\'M JUST NOT GOOD WITH PEOPLE I KNOW',
    giver: { map: 'pearlmoor_lifting_house_b1', npc: 'sid_after' },
    hint: 'The building at the top of the quay: Weights: a lifter downstairs.',
    found: [
      'Sid: "A devil who\'s lovely to strangers and can\'t talk to his own family. I felt seen. I felt attacked. I ' +
        'felt both."',
      '"Found it in my kit bag. You\'re a stranger, so I can manage this: here. Have a sip of my squash, it\'s ' +
        'blackcurrant."',
    ],
    story:
      'A horned red devil, very polite to strangers, warm with shopkeepers, charming on long coach journeys. At ' +
      'home with his own family he cannot think of a single thing to say. He sends them postcards from the next ' +
      'room.',
  },
  {
    id: 'shrimp',
    title: 'I LIKE STORIES ABOUT SHRIMP',
    giver: { map: 'pearlmoor_quay', npc: 'blessing_elder' },
    hint: 'Pearlmoor Quay: the elder who blesses the boats.',
    found: [
      '"Blessing the boats, I found this in the bait-tin. I LIKE STORIES ABOUT SHRIMP. Well, so do I."',
      '"Here\'s one: my grandad\'s boat once caught a shrimp that ate a lamp-wick and glowed a week. Paid for the ' +
        'pub all that week, it did."',
    ],
    story:
      'A pale spiralled shell, the castle of a shrimp who once ate a lamp-wick and glowed for a week. Islanders ' +
      'tell small stories about small things on long nights, and those turn out to be the stories that last.',
  },
  {
    id: 'seahorse',
    title: 'I WILL BE RARE FOR THOSE WHO CARE',
    giver: { map: 'driftholm_elder', npc: 'nan_creel' },
    hint: 'Driftholm: the islands\' oldest grandmother.',
    found: [
      'Nan Creel: "My mother gave me this, and hers gave it her. Now it\'s you. Don\'t lose it, petal."',
    ],
    story:
      'A golden seahorse, curled tight, that hides in the weed from anyone in a hurry. To someone who sits still ' +
      'long enough to notice, it comes out and does a slow, proud turn. It is only rare to the rushing.',
  },
  {
    id: 'moths',
    title: 'CHAPEL OF MOTHS',
    giver: { map: 'mirelight_landing', npc: 'nell' },
    hint: 'The Mirelights: someone at the ferry landing.',
    found: [
      '"Found it in the ferry chapel, under a candle. The moths were all over it. They\'ve good taste."',
    ],
    story:
      'A blue painted skull with flowered cheeks, sitting in a little chapel where one candle burns all night. ' +
      'The moths come to it like a congregation. They are not afraid of the flame. They are devoted to it.',
  },
  {
    id: 'failure',
    title: 'A FAITH IN FAILURE',
    giver: { map: 'penumbra_underways_b1', npc: 'clemency' },
    hint: 'Under the Penumbra Ring: an old woman keeping the last watch.',
    found: [
      'Clemency: "I have failed at almost everything down here, child. This card kept me company through all of ' +
        'it."',
    ],
    story:
      'A little pink angel, mid-tumble, wings all wrong. She has fallen off every cloud she ever stood on. She ' +
      'gets up every time, a bit better at falling, and that is the only kind of flying she has ever needed.',
  },
  {
    id: 'rooster',
    title: 'AIN\'T NOBODY\'S BUSINESS IF YOU DO',
    giver: { map: 'pearlmoor_lifting_house_b1', npc: 'rod' },
    hint: 'The building at the top of the quay: Weights: the strongest seventy-two-year-old on the coast.',
    found: [
      'Rod: "AIN\'T NOBODY\'S BUSINESS IF YOU DO! A rooster that struts where he likes. That\'s me, that is. Found ' +
        'it in the marrow bed."',
      '"Take it home and pin it up, and take a leek too. Biggest on the coast. Don\'t tell Anth I gave it away."',
    ],
    story:
      'A black painted rooster with hearts on his breast and a red comb like a flag. He crows when he likes, ' +
      'struts where he likes, and when the neighbours complain he crows a little louder, very sweetly, at them.',
  },
  {
    id: 'seal',
    title: 'THE CARPET IS PURRING',
    giver: { map: 'dimglass_coast_ii', npc: 'cockler' },
    hint: 'Dimglass Coast: the cockler who keeps a fire for travellers.',
    found: [
      '"A seal hauled out by my fire last night and lay on this like a rug. Purring, I swear it. Seals don\'t ' +
        'purr. This one did."',
      '"Sit a minute. There\'s cockles in the pan and a drop of tea in the pot. Long road, this."',
    ],
    story:
      'A seal balancing a ball on its nose in a warm front room, so content on the rug by the fire that the rug ' +
      'began to purr. Nobody in the house has ever been sure which of them it was.',
  },
  {
    id: 'loon',
    title: 'SYNCOPATED, AGITATED, PURPLE MOON, WHITE LOON',
    giver: { map: 'wayward_arms', npc: 'stranger' },
    hint: 'An inn up on the hill past the wood: a well-dressed stranger.',
    found: [
      '"Somebody left it propped on the piano. Syncopated, agitated. A song that never quite lands on the beat."',
      '"Best kind. Keep it. And pour yourself one: the bar\'s open, we\'ve been told we can help ourselves."',
    ],
    story:
      'A red dancer in a feathered crown, stamping out a tune that never quite lands on the beat, under a purple ' +
      'moon, while a white water-bird calls along off-key. It should not work. It is the best song on the lake.',
  },
  {
    id: 'pyramid',
    title: 'SOMETIMES THE TONGUE IS TIRED',
    giver: { map: 'duskapple_orchard', npc: 'percy' },
    hint: 'Duskapple Orchard: the man with the moka pot.',
    found: [
      '"Found it under a saucer at the stand. Somebody had three cups, tasted every one out loud, then went ' +
        'quiet and left this."',
      '"Sometimes the tongue is tired. Even mine. ...Not often. The eight-sided pot, you see, rests the palate ' +
        'because the pressure is gentle, which means—"',
      'He hands it over mid-sentence, and pours you a thimble of something dark and sweet while he finds his ' +
        'place again.',
    ],
    story:
      'A little blue pendant, pointed like a pyramid, worn by a storyteller who talked from one winter to the ' +
      'next over endless small cups of coffee. One evening she simply stopped, put her tongue to bed, drank her ' +
      'cup in silence, and let the quiet say the rest. It was her best story.',
  },
  {
    id: 'obsession',
    title: 'MEMORY AND OBSESSION',
    giver: { map: 'paul_house_1', npc: 'rose' },
    hint: 'A crooked house up past the wood: someone minding the kettle.',
    found: [
      'Rose: "Dad keeps this one in the button tin. Memory and obsession. He\'d say that\'s the whole house in ' +
        'three words."',
      '"He\'d want you to have it, I think. He\'d never say so. Here: and a cup of red-bush, the kettle\'s just ' +
        'boiled."',
    ],
    story:
      'A tin heart under a crown, pricked all over with little holes from being pinned and unpinned. A woman ' +
      'wore it for forty years for someone she would not stop remembering. The remembering wore the tin thin. It ' +
      'never wore out.',
  },
  {
    id: 'brujas',
    title: 'NOCHE DE BRUJAS',
    giver: { map: 'wakeful_fair_loft', npc: 'ottoline' },
    hint: 'A striped tent up on the hill, upstairs: the champion brewer, upstairs.',
    found: [
      'Ottoline: "Noche de brujas. The witches\' night. I brewed my champion cup on a night like that, under a ' +
        'moon like a peach."',
      '"A competitor slipped this into my apron. Sabotage or a love letter, I\'ve never decided. Yours now. And a ' +
        'taste of the champion\'s cup."',
    ],
    story:
      'The witches\' night: one night a year, when the moon comes up warm as a peach and every old woman in the ' +
      'mountains goes out flying, just to feel the wind. In the morning they come home and make everyone ' +
      'pancakes.',
  },
  {
    id: 'transition',
    title: 'REMEMBER I NEED SOME SPIRITUAL TRANSITION TIME, THAT\'S WHY I HAVE SO MUCH TROUBLE LEAVING THE HOUSE',
    giver: { map: 'crossroads_inn', npc: 'hesper' },
    hint: 'Vesper Crossroads Inn: Hesper, at the crossroads inn.',
    found: [
      'Hesper: "A guest left it on her pillow. She took three hours to leave this inn, and she was right to. ' +
        'Some leavings need tea first."',
      '"I keep the pot on for exactly that kind of traveller. Here: card, and a cup of red-bush. Go when you\'re ' +
        'ready, not before."',
    ],
    story:
      'A woman in a long dress standing just inside her own front door, coat on, ready to go out for the last ' +
      'three hours. She will go. She simply has to finish arriving at the idea first. The world can wait. It ' +
      'usually does.',
  },
];

export const MILAGROS_BY_GIVER = new Map(
  MILAGROS.filter((c) => c.giver).map((c) => [`${c.giver!.map}:${c.giver!.npc}`, c] as const),
);
