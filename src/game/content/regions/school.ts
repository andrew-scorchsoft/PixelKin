/**
 * THE WICKSTEAD LAMP-SCHOOL (2026-10) — the optional tutorial zone one step WEST
 * of Duskapple Orchard (`wickstead_green` + the `wickstead_school` interior;
 * builders tools/maps/build_wickstead_green.py / build_wickstead_school.py).
 *
 * A teacher per desk/corner, each ONE mechanic, re-askable through a `choice`
 * menu. Never progression: nothing here gates the golden thread. Every teacher
 * banks `flag:school_visited` (unlocks the LORE entry for the school). Every
 * claim below is checked against the code/data it describes:
 *   types       — src/game/data/type-chart.json, systems/battle/damage.ts (STAB 1.5,
 *                 dual types multiply, Plain is neutral), BattleScene's effectiveness text
 *   catching    — docs/mechanics/04-capture.md (hpTerm 1/3 at full HP; status ×2.5 / ×1.5),
 *                 content/items.ts (Glow ×1.5 200w, Beacon ×2.5 600w on gleam:ember),
 *                 BattleScene (no LAMP vs trainers; PLAIN THROW free; overflow to the Hearth)
 *   statuses    — the constants atop systems/battle/BattleEngine.ts (03-moves.md table)
 *   kindling    — species kindling triggers (Tallowpup 14, Wickmoth 18, Hearthkit bond 160),
 *                 KindlePrompt re-offers, MoveLearnPrompt, PartyMenu bond tiers
 *   the Hearth  — ui/HearthMenu.ts (DEPOSIT/WITHDRAW, keep ≥1, ≤6), catch overflow
 *   resting     — KinInstance.fullHeal, the `heal` op + rest points, FAINT_TITHE_RATE 0.1 (halving per repeat loss, HEARTH_FLOOR),
 *                 Settings "Return to rest point" / "Cannot die"
 *   wicks       — content/economy.ts (SELL_RATE 0.5), shops.ts, Star-chart compatibility
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

const VISITED = 'flag:school_visited';

const HEAD = 'MISTRESS PENNYWEATHER';
const TOLLY = 'MASTER TOLLY';
const QUENNELL = 'OLD QUENNELL';
const FERNLY = 'TUTOR FERNLY';
const KEEPER = 'HEARTHKEEPER';
const MALLOW = 'MASTER MALLOW';
const BUNCE = 'BUNCE';
const ESK = 'WAYFARER ESK';
const ODO = 'ODO';

export const SCHOOL_SCRIPTS: ScriptRegistry = {
  // ---------------------------------------------------------------- TYPES
  'script.school_types': [
    {
      op: 'say', unless_flag: VISITED, speaker: HEAD,
      text: 'Welcome to the Wickstead Lamp-school, {name}! Every Wayfarer in the South has sat at these desks. Old ones come back, too — nobody remembers everything.',
    },
    {
      op: 'say', if_flag: VISITED, speaker: HEAD,
      text: 'Back for more chalk-dust, {name}? Good. Sit, sit.',
    },
    { op: 'setFlag', flag: VISITED },
    {
      op: 'choice',
      speaker: HEAD,
      prompt: 'Which lesson, dear?',
      options: [
        {
          label: 'THE TEN TYPES',
          ops: [
            { op: 'say', speaker: HEAD, text: 'Every kin carries one or two of ten types. Eight are the constellation elements: Ember, Tide, Verdant, Stone, Storm, Frost, Solar and Lunar.' },
            { op: 'say', speaker: HEAD, text: 'The last two are older than any constellation: Light and Dark.' },
            { op: 'say', speaker: HEAD, text: 'Every move has a type too. A move of the kin\'s OWN type hits half again as hard — so a fire-kin\'s Ember moves burn brightest.' },
            { op: 'say', speaker: HEAD, text: 'Plain moves belong to no type at all. They never hit harder, and never softer — a fair blow against anyone.' },
          ],
        },
        {
          label: 'MATCHUPS',
          ops: [
            { op: 'say', speaker: HEAD, text: 'Some types hit others twice as hard. Some only half as hard. And a very few do nothing at all.' },
            { op: 'say', speaker: HEAD, text: 'Ember burns Verdant and Frost — but Tide, Stone and Solar shrug it off. Tide douses Ember and wears down Stone. Verdant drinks up Tide and cracks Stone.' },
            { op: 'say', speaker: HEAD, text: 'So the three starter elements go round like a wheel: Ember beats Verdant, Verdant beats Tide, Tide beats Ember.' },
            { op: 'say', speaker: HEAD, text: 'And mind Storm: it strikes Tide, Verdant and Solar — but against Stone it has no effect whatsoever.' },
            { op: 'say', speaker: HEAD, text: 'In battle, listen to your lamp. It will tell you "It\'s super effective!", "It\'s not very effective..." or "It had no effect...".' },
          ],
        },
        {
          label: 'THE MIRRORS',
          ops: [
            { op: 'say', speaker: HEAD, text: 'Two pairs of types are MIRRORS: Solar and Lunar, Light and Dark. Each hits its mirror twice as hard — and is hit twice as hard back.' },
            { op: 'say', speaker: HEAD, text: 'So Solar against Lunar is a race. Whoever lands the first good blow usually wins it.' },
            { op: 'say', speaker: HEAD, text: 'One catch: Lunar moves do nothing at all to Dark. The moon cannot find what hides in the dark — and Dark hits Lunar hard besides.' },
          ],
        },
        {
          label: 'TWO TYPES',
          ops: [
            { op: 'say', speaker: HEAD, text: 'Plenty of kin carry two types. Then BOTH count, multiplied together.' },
            { op: 'say', speaker: HEAD, text: 'A move strong against both hits four times as hard. Strong against one and weak against the other? It comes out even.' },
            { op: 'say', speaker: HEAD, text: 'You\'ll find a kin\'s types on its card under KIN. I\'ve chalked the main matchups on the board, too — have a read.' },
          ],
        },
        {
          label: 'THAT\'S ALL',
          ops: [{ op: 'say', speaker: HEAD, text: 'Off you go, then. And bring back your homework: a fuller REGISTER than you left with!' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------- CATCHING
  'script.school_catching': [
    { op: 'setFlag', flag: VISITED },
    {
      op: 'choice',
      speaker: TOLLY,
      prompt: 'Catching\'s my subject. What d\'you want to know?',
      options: [
        {
          label: 'THE THROW',
          ops: [
            { op: 'say', speaker: TOLLY, text: 'Your vesperlamp doesn\'t trap a kin — it offers its light somewhere warm to rest. In a wild battle, choose LAMP. A PLAIN THROW is free, and never runs out.' },
            { op: 'say', speaker: TOLLY, text: 'The lamp shakes... and either it settles, or the kin pops back out. Then you try again.' },
            { op: 'say', speaker: TOLLY, text: 'Only WILD kin, mind. Another Wayfarer\'s kin are spoken for — there\'s no LAMP in a trainer\'s bout.' },
            { op: 'say', speaker: TOLLY, text: 'And a catch teaches your kin as much as a win would. Collecting never costs you levels.' },
          ],
        },
        {
          label: 'WEAKEN FIRST',
          ops: [
            { op: 'say', speaker: TOLLY, text: 'A kin at full health is hard to coax — about a third as easy as one that\'s nearly spent. Wear it down to the red first, gently, then throw.' },
            { op: 'say', speaker: TOLLY, text: 'Don\'t knock it out, though. A fainted kin has nothing left to catch.' },
            { op: 'say', speaker: TOLLY, text: 'A status helps too. Dozing or chilled kin are easiest of all; any other trouble helps a little. Old Quennell by the lamps can tell you about those.' },
          ],
        },
        {
          label: 'CHARGES',
          ops: [
            { op: 'say', speaker: TOLLY, text: 'Charges are one-throw boosts for your lamp. When you choose LAMP with charges in your pack, you can pick one instead of a PLAIN THROW.' },
            { op: 'say', speaker: TOLLY, text: 'A GLOW CHARGE makes a throw half again as likely — 200 wicks at a general store. A BEACON CHARGE is two and a half times as good, 600 wicks; Tinderwick stocks them once you\'ve a Gleam.' },
            { op: 'say', speaker: TOLLY, text: 'Folk on the road give out rarer charms for special kin. Read their labels — some only work in the right place.' },
          ],
        },
        {
          label: 'A FULL LAMP',
          ops: [
            { op: 'say', speaker: TOLLY, text: 'Your lamp carries six kin at most. Catch a seventh and it doesn\'t vanish — it goes straight to the Hearth to rest.' },
            { op: 'say', speaker: TOLLY, text: 'The Hearthkeeper\'s in the nook by the fire today. Ask her about it.' },
          ],
        },
        {
          label: 'THAT\'S ALL',
          ops: [{ op: 'say', speaker: TOLLY, text: 'Weaken, status, throw. Say it back to me on the road.' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------- STATUSES
  'script.school_status': [
    { op: 'setFlag', flag: VISITED },
    {
      op: 'say', speaker: QUENNELL,
      text: 'Seven troubles can settle on a kin. Only one at a time, mind — a kin that\'s already troubled can\'t catch a second.',
    },
    {
      op: 'choice',
      speaker: QUENNELL,
      prompt: 'Which troubles shall I tell you of?',
      options: [
        {
          label: 'SCORCH & BLIGHT',
          ops: [
            { op: 'say', speaker: QUENNELL, text: 'SCORCH is a burn: it nibbles a little health every turn, and halves the kin\'s physical attacks.' },
            { op: 'say', speaker: QUENNELL, text: 'BLIGHT creeps: a little harm the first turn, more the next, more again the longer it lingers. Swap the kin out and it starts small again.' },
          ],
        },
        {
          label: 'DRENCH & NUMB',
          ops: [
            { op: 'say', speaker: QUENNELL, text: 'DRENCH soaks a kin through: it\'s slowed, and one turn in four its action fizzles out.' },
            { op: 'say', speaker: QUENNELL, text: 'NUMB is a stinging jolt: slowed as well, and one turn in four it simply can\'t move.' },
          ],
        },
        {
          label: 'DOZE & CHILL',
          ops: [
            { op: 'say', speaker: QUENNELL, text: 'DOZE puts a kin to sleep for one to three turns.' },
            { op: 'say', speaker: QUENNELL, text: 'CHILL freezes it stiff: no moves at all until it thaws — a small chance each turn, or at once if an Ember move hits it.' },
            { op: 'say', speaker: QUENNELL, text: 'A dozing or chilled wild kin is the easiest of all to lamp. Remember that.' },
          ],
        },
        {
          label: 'DAZZLE',
          ops: [
            { op: 'say', speaker: QUENNELL, text: 'DAZZLE leaves a kin muddled and seeing stars. A third of the time it hurts itself instead of doing as it\'s told.' },
          ],
        },
        {
          label: 'CURING',
          ops: [
            { op: 'say', speaker: QUENNELL, text: 'Troubles don\'t end with the battle. A scorched kin stays scorched on the road, until it rests.' },
            { op: 'say', speaker: QUENNELL, text: 'A good night\'s rest cures every one — your own bed, an inn, any rest point. Master Mallow by the cot knows all about resting. A few kin know a cleansing move, too.' },
          ],
        },
        {
          label: 'THAT\'S ALL',
          ops: [{ op: 'say', speaker: QUENNELL, text: 'Seven troubles, one cure: rest. Off you go.' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------- KINDLING & BOND
  'script.school_kindling': [
    { op: 'setFlag', flag: VISITED },
    {
      op: 'choice',
      speaker: FERNLY,
      prompt: 'Growing things is my subject. Kin grow too, you know.',
      options: [
        {
          label: 'KINDLING',
          ops: [
            { op: 'say', speaker: FERNLY, text: 'When a kin has taken on enough light, it KINDLES — it blazes up into a brighter, stronger form.' },
            { op: 'say', speaker: FERNLY, text: 'Most kindle at a certain level. A Tallowpup at level 14, say, or a Wickmoth at 18.' },
            { op: 'say', speaker: FERNLY, text: 'When the moment comes, you\'ll be asked. Say "not yet" and it will ask again at the next level — some folk like their kin small a while longer.' },
          ],
        },
        {
          label: 'NEW MOVES',
          ops: [
            { op: 'say', speaker: FERNLY, text: 'Kin learn new moves as they grow. A kin can hold four moves at most.' },
            { op: 'say', speaker: FERNLY, text: 'To learn a fifth it must forget one — you choose which, or give up the new move and keep the four it has.' },
            { op: 'say', speaker: FERNLY, text: 'Star-charts can teach a move, too. Bunce at the tuck-shop outside will tell you about those.' },
          ],
        },
        {
          label: 'BOND',
          ops: [
            { op: 'say', speaker: FERNLY, text: 'BOND is how much a kin trusts you. Win a battle or make a catch, and every kin still standing at the end grows a little closer.' },
            { op: 'say', speaker: FERNLY, text: 'Tending a kin with a balm from your ITEMS warms it a little, too.' },
            { op: 'say', speaker: FERNLY, text: 'Look on a kin\'s card under KIN: NEW, then WARM, CLOSE... and KINDRED.' },
            { op: 'say', speaker: FERNLY, text: 'A few kin won\'t kindle by level at all — only once the bond runs that deep. A Hearthkit is one.' },
            { op: 'say', speaker: FERNLY, text: 'Bond never makes a kin hit harder, mind. It isn\'t that sort of thing.' },
          ],
        },
        {
          label: 'THAT\'S ALL',
          ops: [{ op: 'say', speaker: FERNLY, text: 'Patience and sunlight — or lamplight, these days. Off you go.' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------- THE HEARTH
  'script.school_hearth': [
    { op: 'setFlag', flag: VISITED },
    {
      op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'warm',
      text: 'Hello, pet. I keep the Hearth — the warm keep where kin rest when they aren\'t travelling in your lamp. The school\'s borrowed me to explain it. Sit by the fire.',
    },
    {
      op: 'choice',
      speaker: KEEPER,
      prompt: 'What would you like to know?',
      options: [
        {
          label: 'THE HEARTH',
          ops: [
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'neutral', text: 'Your vesperlamp carries six kin. Every other friend you make rests at my Hearth, safe and warm, for as long as you like. Nothing you befriend is ever lost.' },
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'warm', text: 'And it\'s never far. Your lamp\'s light runs all the way home to my fire, so you can reach the Hearth from anywhere at all.' },
          ],
        },
        {
          label: 'A FULL LAMP',
          ops: [
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'neutral', text: 'Catch a kin with six already in your lamp, and it comes straight to me. No fuss, no choosing in the middle of the grass.' },
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'warm', text: 'So never fear a full lamp. A full lamp just means the next friend waits by the fire.' },
          ],
        },
        {
          label: 'MOVING KIN',
          ops: [
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'neutral', text: 'Open your menu — START, or Esc — and choose HEARTH. Every kin you own is listed: a lit mark for those in your lamp, a dim one for those resting with me.' },
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'neutral', text: 'Pick one of your lamp kin to DEPOSIT it here. Pick a resting one to WITHDRAW it. Keep at least one at your side, and no more than six.' },
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'warm', text: 'An old keeper\'s tip: before a big fight, bring the right types to your side. The others won\'t mind a sit by the fire.' },
          ],
        },
        {
          label: 'THAT\'S ALL',
          ops: [{ op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'warm', text: 'Go on, then. I\'ll keep a place warm for whoever you meet.' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------- RESTING
  'script.school_rest': [
    { op: 'setFlag', flag: VISITED },
    {
      op: 'choice',
      speaker: MALLOW,
      prompt: 'Sick-bay\'s my corner. Resting, that\'s my lesson.',
      options: [
        {
          label: 'A GOOD REST',
          ops: [
            { op: 'say', speaker: MALLOW, text: 'A proper rest heals every kin in your lamp: health back, troubles gone, every move topped up.' },
            { op: 'say', speaker: MALLOW, text: 'Your own bed at home does it. So does any inn, and a few kind souls along the road.' },
          ],
        },
        {
          label: 'REST POINTS',
          ops: [
            { op: 'say', speaker: MALLOW, text: 'Every place you rest is remembered. Lost, or a long way from a bed? Open SETTINGS and choose "Return to rest point".' },
            { op: 'say', speaker: MALLOW, text: 'Your lamp will walk you back to any of them. Nobody needs to be lost for long.' },
          ],
        },
        {
          label: 'IF YOU FALL',
          ops: [
            { op: 'say', speaker: MALLOW, text: 'If every kin in your lamp faints, a kind light carries you all back to the last place you rested. It keeps a tithe for the trouble — a tenth of your wicks, never more than a modest sum, less each time the same foe beats you again, and never your last few.' },
            { op: 'say', speaker: MALLOW, text: 'And if you\'d rather never fall at all, SETTINGS has a "Cannot die" switch. No shame in it. The road\'s long enough.' },
          ],
        },
        {
          label: 'A LIE-DOWN',
          ops: [
            { op: 'say', speaker: MALLOW, text: 'Go on, then — the cot\'s clean. Rest a while; I\'ll mind the lamp.' },
            { op: 'heal' },
            { op: 'say', speaker: MALLOW, text: 'There. Right as rain. And the school\'s a rest point of yours now, too.' },
          ],
        },
        {
          label: 'THAT\'S ALL',
          ops: [{ op: 'say', speaker: MALLOW, text: 'Rest when you can. The dark keeps; you don\'t have to.' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------- WICKS & SHOPS (the green)
  'script.school_wicks': [
    { op: 'setFlag', flag: VISITED },
    {
      op: 'choice',
      speaker: BUNCE,
      prompt: 'Tuck-shop\'s shut till break, love. Ask me about money instead.',
      options: [
        {
          label: 'WICKS',
          ops: [
            { op: 'say', speaker: BUNCE, text: 'Wicks are coin: waxed lamp-wicks, brass-capped and bundled. Win a fair bout against a trainer — a road-trainer, a rival, a Lampwarden — and they\'ll pay you for it.' },
            { op: 'say', speaker: BUNCE, text: 'Wild kin don\'t carry purses. But folk drop them, in out-of-the-way corners. Keep your eyes open.' },
          ],
        },
        {
          label: 'SHOPS',
          ops: [
            { op: 'say', speaker: BUNCE, text: 'Every town has a counter. Talk to the keeper, choose BUY, and pick your stock: balms to mend kin, charges for your lamp.' },
            { op: 'say', speaker: BUNCE, text: 'Shops put out better stock as you earn Gleams, so look in again after each one.' },
          ],
        },
        {
          label: 'SELLING',
          ops: [
            { op: 'say', speaker: BUNCE, text: 'Choose SELL at any counter and you\'ll get half what a thing costs new.' },
            { op: 'say', speaker: BUNCE, text: 'Some finds — pearls, odd stones — are worth a great deal and good for nothing else. Key things and quest charms never go on the counter, so you can\'t sell those by accident.' },
          ],
        },
        {
          label: 'STAR-CHARTS',
          ops: [
            { op: 'say', speaker: BUNCE, text: 'A Star-chart is a pressed chart of one little constellation. A kin that studies it learns a move — and the chart burns out. One use.' },
            { op: 'say', speaker: BUNCE, text: 'It has to suit the kin: the move shares one of its types, or it\'s a Plain move anyone can learn, or it\'s one the kin would learn anyway. Use it from your ITEMS.' },
          ],
        },
        {
          label: 'THAT\'S ALL',
          ops: [{ op: 'say', speaker: BUNCE, text: 'Spend wise, love. A wick saved is a wick for later.' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------- LANTERN GIFTS (the pond)
  'script.school_gifts': [
    { op: 'setFlag', flag: VISITED },
    {
      op: 'choice',
      speaker: ESK,
      prompt: 'I sat at those desks once. Now I teach the road. Ask away.',
      options: [
        {
          label: 'LANTERN GIFTS',
          ops: [
            { op: 'say', speaker: ESK, text: 'When a Lampwarden relights their constellation, some teach you a knack with your lamp as well: a LANTERN GIFT.' },
            { op: 'say', speaker: ESK, text: 'Each Gift opens ground you couldn\'t walk before. Six of them, all told — night-water, woods too dark to enter, cold fog, and stranger things.' },
          ],
        },
        {
          label: 'THIS POND',
          ops: [
            { op: 'face', actor: 'teacher_gifts', facing: 'left' },
            { op: 'say', speaker: ESK, text: 'See this pond? Night-water. Step in now and you\'d sink to your ears.' },
            { op: 'say', speaker: ESK, text: 'With TIDECALL — the Gift of Pearlmoor\'s Lampwarden — the moon-tide answers your lamp, and you can cross water like this.' },
            { op: 'say', speaker: ESK, text: 'So remember the places you couldn\'t reach. Come back with the right Gift and they\'ll be waiting, every one.' },
          ],
        },
        {
          label: 'LAMPLIGHT',
          ops: [
            { op: 'say', speaker: ESK, text: 'Your vesperlamp grows brighter with every Gleam you earn. A brighter lamp shows more in dark places: tucked-away paths, hidden things.' },
            { op: 'say', speaker: ESK, text: 'It never bars your way, mind. It only rewards the curious.' },
          ],
        },
        {
          label: 'THAT\'S ALL',
          ops: [{ op: 'say', speaker: ESK, text: 'Walk far. You\'ll come round again — everyone does.' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------- THE MENUS (the green)
  'script.school_menus': [
    { op: 'setFlag', flag: VISITED },
    {
      op: 'choice',
      speaker: ODO,
      prompt: 'I\'m rubbish at sums but I know my menu. Press START — or Esc! What d\'you want?',
      options: [
        {
          label: 'JOURNAL',
          ops: [
            { op: 'say', speaker: ODO, text: 'JOURNAL keeps your quests. The Wayfaring\'s at the top — where your next Gleam is — and every errand folk have asked of you, ticked off as you go.' },
          ],
        },
        {
          label: 'MAP',
          ops: [
            { op: 'say', speaker: ODO, text: 'MAP shows all of Vesperholm, with a blinking dot for you. Hop between places with the arrows to see their names.' },
          ],
        },
        {
          label: 'LORE',
          ops: [
            { op: 'say', speaker: ODO, text: 'LORE\'s a little book of words: Gleam, Lumenary, the Hearth, all that. New words fill in as you learn them. I read it under the covers.' },
          ],
        },
        {
          label: 'REGISTER',
          ops: [
            { op: 'say', speaker: ODO, text: 'REGISTER is every kin you\'ve seen and caught. The ones you\'ve only seen are just shadows till they\'re yours.' },
            { op: 'say', speaker: ODO, text: 'And CHARTS collects pictures of places — the first time you set foot somewhere new, you get its picture.' },
          ],
        },
        {
          label: 'SAVING',
          ops: [
            { op: 'say', speaker: ODO, text: 'SAVE writes your journey down. SETTINGS has "Backup / restore" to keep a copy somewhere safe.' },
            { op: 'say', speaker: ODO, text: 'And if you\'re ever stuck, there\'s a man called Andrew on a fence in nearly every town. He always knows where you ought to be going.' },
          ],
        },
        {
          label: 'THAT\'S ALL',
          ops: [{ op: 'say', speaker: ODO, text: 'Don\'t tell the Mistress I\'m out here.' }],
        },
      ],
    },
  ],

  // ---------------------------------------------------------------- the lost-property box
  'script.pickup_school_lost_property': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'tallow_balm', count: 1 },
    { op: 'say', text: 'The school\'s lost-property box. Under a single mitten and a chewed pencil: a TALLOW BALM! Nobody has claimed it since the dusk fell.' },
    { op: 'setFlag', flag: 'flag:picked_school_lost_property' },
  ],
};

export const SCHOOL_DIALOGUE: DialogueRegistry = {
  'sign.wickstead_green': [
    { text: 'WICKSTEAD GREEN — The Lamp-school. All Wayfarers welcome, however old. East: Duskapple Orchard and Tinderwick.' },
  ],
  'sign.school_timetable': [
    { text: 'TODAY\'S LESSONS, pinned up in chalky fingerprints:' },
    { text: 'IN THE SCHOOLROOM — Types: Mistress Pennyweather, at the board. Catching: Master Tolly. Statuses: Old Quennell. Kindling & Bond: Tutor Fernly.' },
    { text: 'The Hearth: the Hearthkeeper, visiting, by the fire. Resting: Master Mallow, at the cot.' },
    { text: 'ON THE GREEN — Lantern Gifts: Wayfarer Esk, by the pond. Wicks & Shops: Bunce, at the tuck-shop. Your Menus: ask Odo (he\'s meant to be indoors).' },
  ],
  'sign.school_chalkboard': [
    { text: 'Chalked on the board in a careful round hand: WHO BEATS WHOM (twice as hard).' },
    { text: 'EMBER beats Verdant, Frost. TIDE beats Ember, Stone. VERDANT beats Tide, Stone. STONE beats Ember, Storm.' },
    { text: 'STORM beats Tide, Verdant, Solar — and does NOTHING to Stone. FROST beats Verdant, Storm, Stone.' },
    { text: 'THE MIRRORS: Solar and Lunar beat each other. So do Light and Dark. Solar beats Frost and Dark too; Lunar beats Tide, but does NOTHING to Dark.' },
    { text: 'Underneath, smaller: "Own type = half again harder. Two types? MULTIPLY." And in a pupil\'s hand, crossed out: "EMBER BEATS EVERYTHING".' },
  ],
  'sign.school_bookcase': [
    { text: 'Primers, mostly. "My First Constellations." "Kin, and How to Befriend Them." "A Hundred Uses for a Wick."' },
    { text: 'Someone has drawn a moustache on every Lampwarden in "Great Wardens of the South".' },
  ],
  'npc.school_pupil_willa': [
    { speaker: 'WILLA', text: 'Shh! I\'m learning the wheel. Ember beats Verdant, Verdant beats Tide, Tide beats Ember... and round again!' },
  ],
  'npc.school_pupil_dob': [
    { speaker: 'DOB', text: 'I\'m not asleep. I\'m DOZING. It\'s a status. Mistress says that makes me very easy to lamp.' },
  ],
  'npc.school_yard_kid': [
    { speaker: 'LARK', text: 'School\'s on, but the wind\'s up — and you can\'t fly a kite indoors! Don\'t tell the Mistress.' },
  ],
};
