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
      text: 'Welcome to the Lamp-school, {name}! Every Wayfarer sat at these desks once.',
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
            { op: 'say', speaker: HEAD, text: 'Kin carry one or two of [[ten types]]: Ember, Tide, Verdant, Stone, Storm, Frost, Solar, Lunar — and the older Light and Dark.' },
            { op: 'say', speaker: HEAD, text: 'A move of the kin\'s [[OWN type]] hits half again as hard.' },
            { op: 'say', speaker: HEAD, text: 'Plain moves have no type: a fair blow against anyone.' },
          ],
        },
        {
          label: 'MATCHUPS',
          ops: [
            { op: 'say', speaker: HEAD, text: 'Some types hit others [[twice as hard]], some half as hard — and a few not at all.' },
            { op: 'say', speaker: HEAD, text: 'Ember burns Verdant and Frost, but Tide and Stone shrug it off. Tide douses Ember and Stone. Verdant drinks Tide and cracks Stone.' },
            { op: 'say', speaker: HEAD, text: 'Starters go round like a wheel: Ember beats Verdant beats Tide beats Ember.' },
            { op: 'say', speaker: HEAD, text: 'Mind Storm: it strikes Tide, Verdant and Solar, but can\'t touch Stone.' },
            { op: 'say', speaker: HEAD, text: 'In battle, [[listen to your lamp]]: it says how well each move landed.' },
          ],
        },
        {
          label: 'THE MIRRORS',
          ops: [
            { op: 'say', speaker: HEAD, text: 'Solar and Lunar, Light and Dark are [[MIRRORS]]: each hits the other twice as hard.' },
            { op: 'say', speaker: HEAD, text: 'So Solar against Lunar is a race: the first good blow usually wins.' },
            { op: 'say', speaker: HEAD, text: 'But Lunar can\'t touch Dark. The moon can\'t find what hides there.' },
          ],
        },
        {
          label: 'TWO TYPES',
          ops: [
            { op: 'say', speaker: HEAD, text: 'Two types? [[Multiply them]]. Strong against both: four times. One each way: even.' },
            { op: 'say', speaker: HEAD, text: 'Types are on each kin\'s card under [[KIN]]. Matchups are chalked on the board.' },
          ],
        },
        {
          label: 'THAT\'S ALL',
          ops: [{ op: 'say', speaker: HEAD, text: 'Off you go. Homework: a fuller REGISTER than you came in with!' }],
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
            { op: 'say', speaker: TOLLY, text: 'Choose [[LAMP]] in a wild battle. A PLAIN THROW is always free.' },
            { op: 'say', speaker: TOLLY, text: 'The lamp shakes... then settles, or the kin pops out and you try again.' },
            { op: 'say', speaker: TOLLY, text: 'Only WILD kin, mind. No LAMP in a trainer\'s bout — those kin are spoken for.' },
            { op: 'say', speaker: TOLLY, text: 'And a catch teaches your kin as much as a win.' },
          ],
        },
        {
          label: 'WEAKEN FIRST',
          ops: [
            { op: 'say', speaker: TOLLY, text: '[[Wear it down to the red]], gently, then throw. Full health is hard to coax.' },
            { op: 'say', speaker: TOLLY, text: 'Don\'t knock it out, though. A fainted kin can\'t be caught.' },
            { op: 'say', speaker: TOLLY, text: 'A status helps too. Old Quennell by the lamps knows his troubles.' },
          ],
        },
        {
          label: 'CHARGES',
          ops: [
            { op: 'say', speaker: TOLLY, text: '[[Charges]] boost one throw. Choose LAMP and pick one instead of a PLAIN THROW.' },
            { op: 'say', speaker: TOLLY, text: 'GLOW CHARGE, 200 wicks: half again as good. BEACON, 600: two and a half times — Tinderwick sells those once you\'ve a Gleam.' },
            { op: 'say', speaker: TOLLY, text: 'Rarer charms come from folk on the road. Read the labels.' },
          ],
        },
        {
          label: 'A FULL LAMP',
          ops: [
            { op: 'say', speaker: TOLLY, text: 'Your lamp holds [[six kin]]. A seventh catch goes to the Hearth.' },
            { op: 'say', speaker: TOLLY, text: 'The Hearthkeeper\'s by the fire today. Ask her.' },
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
      text: '[[Seven troubles]] can settle on a kin — only one at a time, mind.',
    },
    {
      op: 'choice',
      speaker: QUENNELL,
      prompt: 'Which troubles shall I tell you of?',
      options: [
        {
          label: 'SCORCH & BLIGHT',
          ops: [
            { op: 'say', speaker: QUENNELL, text: 'SCORCH burns: a nibble of health each turn, and physical attacks halved.' },
            { op: 'say', speaker: QUENNELL, text: 'BLIGHT creeps: worse each turn it lingers. Swap the kin out to reset it.' },
          ],
        },
        {
          label: 'DRENCH & NUMB',
          ops: [
            { op: 'say', speaker: QUENNELL, text: 'DRENCH soaks: slowed, and one turn in four its action fizzles.' },
            { op: 'say', speaker: QUENNELL, text: 'NUMB stings: slowed too, and one turn in four it can\'t move.' },
          ],
        },
        {
          label: 'DOZE & CHILL',
          ops: [
            { op: 'say', speaker: QUENNELL, text: 'DOZE puts a kin to sleep for one to three turns.' },
            { op: 'say', speaker: QUENNELL, text: 'CHILL freezes it stiff till it thaws — sooner if an Ember move hits it.' },
            { op: 'say', speaker: QUENNELL, text: 'A dozing or chilled wild kin is the [[easiest to lamp]]. Remember that.' },
          ],
        },
        {
          label: 'DAZZLE',
          ops: [
            { op: 'say', speaker: QUENNELL, text: 'DAZZLE leaves a kin seeing stars. A third of the time it hurts itself instead.' },
          ],
        },
        {
          label: 'CURING',
          ops: [
            { op: 'say', speaker: QUENNELL, text: 'Troubles outlast the battle — until the kin rests.' },
            { op: 'say', speaker: QUENNELL, text: 'A [[good rest]] cures them all — bed, inn, any rest point. Ask Mallow.' },
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
            { op: 'say', speaker: FERNLY, text: 'Take on enough light and a kin [[KINDLES]] into a brighter, stronger form.' },
            { op: 'say', speaker: FERNLY, text: 'Most kindle at a set level: a Tallowpup at 14, a Wickmoth at 18.' },
            { op: 'say', speaker: FERNLY, text: 'You\'ll be asked. Say "not yet" and it asks again next level.' },
          ],
        },
        {
          label: 'NEW MOVES',
          ops: [
            { op: 'say', speaker: FERNLY, text: 'Kin hold [[four moves]]. To learn a fifth, forget one — or skip it.' },
            { op: 'say', speaker: FERNLY, text: 'Star-charts teach moves too. Ask Bunce at the tuck-shop outside.' },
          ],
        },
        {
          label: 'BOND',
          ops: [
            { op: 'say', speaker: FERNLY, text: '[[BOND]] is trust. Win or catch, and every kin still standing grows closer.' },
            { op: 'say', speaker: FERNLY, text: 'Tending one with a balm from ITEMS warms it too.' },
            { op: 'say', speaker: FERNLY, text: 'Its card under KIN shows it: NEW, WARM, CLOSE... KINDRED.' },
            { op: 'say', speaker: FERNLY, text: 'A few, like the Hearthkit, kindle only once the bond runs that deep.' },
            { op: 'say', speaker: FERNLY, text: 'Bond never makes a kin hit harder. It isn\'t that sort of thing.' },
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
      text: 'Hello, pet. I keep the Hearth, where kin rest. Sit by the fire.',
    },
    {
      op: 'choice',
      speaker: KEEPER,
      prompt: 'What would you like to know?',
      options: [
        {
          label: 'THE HEARTH',
          ops: [
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'neutral', text: 'Past six, friends rest at my Hearth. None is ever lost.' },
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'warm', text: 'You can [[reach the Hearth]] from anywhere at all.' },
          ],
        },
        {
          label: 'A FULL LAMP',
          ops: [
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'neutral', text: 'Catch one with six in your lamp and it comes straight to me.' },
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'warm', text: 'A full lamp just means the next friend waits by the fire.' },
          ],
        },
        {
          label: 'MOVING KIN',
          ops: [
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'neutral', text: 'Press [[START]] and choose [[HEARTH]]. Lit kin travel; dim ones rest.' },
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'neutral', text: 'DEPOSIT or WITHDRAW. Keep one to six with you.' },
            { op: 'say', speaker: KEEPER, portrait: 'hearthkeeper', expr: 'warm', text: 'Before a big fight, bring the right types. The rest love the fire.' },
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
            { op: 'say', speaker: MALLOW, text: 'A [[proper rest]] heals your lamp: health, troubles, every move topped up.' },
            { op: 'say', speaker: MALLOW, text: 'Your bed at home, any inn, a few kind souls on the road.' },
          ],
        },
        {
          label: 'REST POINTS',
          ops: [
            { op: 'say', speaker: MALLOW, text: 'Lost? Open SETTINGS and choose [["Return to rest point"]].' },
            { op: 'say', speaker: MALLOW, text: 'Your lamp walks you back. Nobody stays lost long.' },
          ],
        },
        {
          label: 'IF YOU FALL',
          ops: [
            { op: 'say', speaker: MALLOW, text: 'Lose every kin and you wake at your [[last rest point]], a few wicks lighter.' },
            { op: 'say', speaker: MALLOW, text: 'Rather never fall? SETTINGS has a "Cannot die" switch. No shame in it.' },
          ],
        },
        {
          label: 'A LIE-DOWN',
          ops: [
            { op: 'say', speaker: MALLOW, text: 'The cot\'s clean. Rest a while; I\'ll mind the lamp.' },
            { op: 'heal' },
            { op: 'say', speaker: MALLOW, text: 'Right as rain. The school\'s one of your rest points now.' },
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
            { op: 'say', speaker: BUNCE, text: 'Wicks are coin. [[Beat a trainer]] in a fair bout and they\'ll pay you.' },
            { op: 'say', speaker: BUNCE, text: 'Wild kin carry no purses, but folk drop them in odd corners. Eyes open.' },
          ],
        },
        {
          label: 'SHOPS',
          ops: [
            { op: 'say', speaker: BUNCE, text: 'Talk to a town\'s keeper and choose [[BUY]]: balms for kin, charges for your lamp.' },
            { op: 'say', speaker: BUNCE, text: 'Stock improves with each Gleam, so look in again.' },
          ],
        },
        {
          label: 'SELLING',
          ops: [
            { op: 'say', speaker: BUNCE, text: 'Choose [[SELL]] at any counter for half the new price.' },
            { op: 'say', speaker: BUNCE, text: 'Pearls and odd stones fetch a lot. Key things can\'t be sold — no accidents.' },
          ],
        },
        {
          label: 'STAR-CHARTS',
          ops: [
            { op: 'say', speaker: BUNCE, text: 'A [[Star-chart]] teaches a kin one move, then burns out.' },
            { op: 'say', speaker: BUNCE, text: 'It must suit the kin: its type, Plain, or its own. Use it from [[ITEMS]].' },
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
            { op: 'say', speaker: ESK, text: 'Some Lampwardens teach your lamp a knack: a [[LANTERN GIFT]].' },
            { op: 'say', speaker: ESK, text: 'Six in all, each opening new ground — night-water, dark woods, cold fog...' },
          ],
        },
        {
          label: 'THIS POND',
          ops: [
            { op: 'face', actor: 'teacher_gifts', facing: 'left' },
            { op: 'say', speaker: ESK, text: 'This pond\'s night-water. Step in now and you\'d sink to your ears.' },
            { op: 'say', speaker: ESK, text: 'With [[TIDECALL]], Pearlmoor\'s Gift, the moon-tide carries you across.' },
            { op: 'say', speaker: ESK, text: 'Remember the [[places you couldn\'t reach]]. Come back with the right Gift.' },
          ],
        },
        {
          label: 'LAMPLIGHT',
          ops: [
            { op: 'say', speaker: ESK, text: 'Each Gleam brightens your lamp, showing hidden paths in dark places.' },
            { op: 'say', speaker: ESK, text: 'It never bars your way. It only rewards the curious.' },
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
      prompt: 'I\'m rubbish at sums but I know my menu. Press [[START or Esc]]! What d\'you want?',
      options: [
        {
          label: 'JOURNAL',
          ops: [
            { op: 'say', speaker: ODO, text: '[[JOURNAL]] keeps your quests: the Wayfaring on top, then every errand.' },
          ],
        },
        {
          label: 'MAP',
          ops: [
            { op: 'say', speaker: ODO, text: 'MAP shows Vesperholm, with a blinking dot for you. Arrows hop between places.' },
          ],
        },
        {
          label: 'LORE',
          ops: [
            { op: 'say', speaker: ODO, text: 'LORE\'s a book of words that fills in as you learn. I read it under the covers.' },
          ],
        },
        {
          label: 'REGISTER',
          ops: [
            { op: 'say', speaker: ODO, text: 'REGISTER is every kin you\'ve seen and caught. Seen-only ones are shadows.' },
            { op: 'say', speaker: ODO, text: 'CHARTS collects a picture of each new place you set foot in.' },
          ],
        },
        {
          label: 'SAVING',
          ops: [
            { op: 'say', speaker: ODO, text: '[[SAVE]] writes your journey down. SETTINGS has "Backup / restore" for a safe copy.' },
            { op: 'say', speaker: ODO, text: 'Stuck? [[Andrew]] sits on a fence in nearly every town. He always knows the way.' },
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
    { op: 'say', text: 'Lost property. Under a mitten and a chewed pencil: a TALLOW BALM!' },
    { op: 'setFlag', flag: 'flag:picked_school_lost_property' },
  ],
};

export const SCHOOL_DIALOGUE: DialogueRegistry = {
  'sign.wickstead_green': [
    { text: 'WICKSTEAD GREEN — The Lamp-school. East: [[Duskapple]], [[Tinderwick]].' },
  ],
  'sign.school_timetable': [
    { text: 'TODAY\'S LESSONS. INDOORS — Types: Pennyweather. Catching: Tolly. Statuses: Quennell. Kindling: Fernly.' },
    { text: 'Hearth: the Hearthkeeper, by the fire. Resting: Mallow, at the cot.' },
    { text: 'ON THE GREEN — Gifts: Esk. Wicks: Bunce. Menus: Odo (meant to be indoors).' },
  ],
  'sign.school_chalkboard': [
    { text: 'In a careful round hand: WHO BEATS WHOM (twice as hard).' },
    { text: 'EMBER beats Verdant, Frost. TIDE beats Ember, Stone. VERDANT beats Tide, Stone. STONE beats Ember, Storm.' },
    { text: 'STORM beats Tide, Verdant, Solar — and does NOTHING to Stone. FROST beats Verdant, Storm, Stone.' },
    { text: 'THE MIRRORS: Solar and Lunar beat each other. So do Light and Dark. Solar beats Frost and Dark too; Lunar beats Tide, but does NOTHING to Dark.' },
    { text: 'Below: "Own type: half again. Two types: MULTIPLY." Crossed out: "EMBER BEATS EVERYTHING".' },
  ],
  'sign.school_bookcase': [
    { text: 'Every Lampwarden in "Great Wardens of the South" has a drawn-on moustache.' },
  ],
  'npc.school_pupil_willa': [
    { speaker: 'WILLA', text: 'Shh! I\'m learning the wheel. Ember, Verdant, Tide... and round again!' },
  ],
  'npc.school_pupil_dob': [
    { speaker: 'DOB', text: 'I\'m not asleep. I\'m DOZING. It\'s a status. Very easy to lamp, me.' },
  ],
  'npc.school_yard_kid': [
    { speaker: 'LARK', text: 'Wind\'s up — and you can\'t fly a kite indoors! Don\'t tell the Mistress.' },
  ],
};
