/**
 * THE KITCHENS (2026-10) — two optional food-and-talk corners. Pure colour:
 * nothing here gates anything, and both are repeatable.
 *
 *  * PERCY'S BREW-STAND — Duskapple Orchard, early doors (the satchel errand walks
 *    right past it). A man in an apron crouched over a tiny burner and an
 *    eight-sided moka pot, who will not stop telling you why it's the best way to
 *    make coffee. Menu: HISTORY / HOW IT WORKS / WHY IT'S THE BEST / a cup (once —
 *    the `moka_cup` medicine) / NO THANKS. Each topic has two "volumes" that
 *    alternate on repeat asks, so he never quite runs dry. Prop: `kitchens_moka_stall`
 *    (drawn by tools/maps/draw_moka_stall.py) at (12,10); Percy at (14,11).
 *
 *  * MARISOL'S KITCHEN — the south clearing of Lowleaf Hollow, by the Fen road in.
 *    A cook from a sunny country far to the south over the sea, serving its red,
 *    tomato-and-dried-chile dishes off a comal. ORDER a plate (CANTINA_PRICE wicks,
 *    the `pay` op — mirrored in tools/balance/progression.mjs PRICES.cantina_dish
 *    and docs/mechanics/10-economy.md) -> a short serving -> her provenance talk for
 *    THAT dish -> the party is restored (a courtesy heal, not a rest point). The
 *    first plate ever also comes with a jar of her salsa (`salsa_roja`, once).
 *    Props: `kitchens_cantina_stall` (6,26) + `kitchens_pozole_pot` (10,26);
 *    Marisol at (9,27).
 *
 * Placements live in tools/maps/hand_placed_data.py (both maps are shipped).
 * ORIGINALITY: no brand names, ever — it is "the moka pot" / "the eight-sided pot".
 * Spelling: always MOKA, as in the pot. Real places stay unnamed ("a hill-country far
 * across the sea", "a sunny country far to the south"); the food talk is real,
 * respectful food history, no costume clichés.
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const PERCY = 'PERCY';
const MARISOL = 'MARISOL';

/** Wicks per plate at Marisol's (mirror: progression.mjs PRICES.cantina_dish). */
export const CANTINA_PRICE = 60;

const p = (text: string): CutsceneStep => ({ op: 'say', speaker: PERCY, text });
const m = (text: string): CutsceneStep => ({ op: 'say', speaker: MARISOL, text });

/**
 * Two alternating "volumes" of one topic. Exactly one plays per ask:
 * `T` is cleared first; volume A (while `vol` is unset) sets `vol` + `T`, so
 * volume B — guarded `if vol, unless T` — can't follow it in the same ask;
 * next time A is skipped and B plays and clears `vol` again.
 */
function volumes(topic: string, a: CutsceneStep[], b: CutsceneStep[]): ScriptRegistry {
  const vol = `flag:moka_${topic}_vol2`;
  const turn = 'flag:moka_turn';
  return {
    [`script.moka_${topic}`]: [
      { op: 'setFlag', flag: turn, value: false },
      { op: 'run', ref: `script.moka_${topic}_a`, unless_flag: vol },
      { op: 'run', ref: `script.moka_${topic}_b`, if_flag: vol, unless_flag: turn },
    ],
    [`script.moka_${topic}_a`]: [...a, { op: 'setFlag', flag: vol }, { op: 'setFlag', flag: turn }],
    [`script.moka_${topic}_b`]: [...b, { op: 'setFlag', flag: vol, value: false }],
  };
}

/** One dish off Marisol's menu: pay -> the plate's own script, or a kind "not today". */
function order(dish: string): CutsceneStep[] {
  const paid = 'flag:cantina_paid';
  return [
    { op: 'setFlag', flag: paid, value: false },
    { op: 'pay', amount: CANTINA_PRICE, flag: paid },
    { op: 'run', ref: `script.cantina_${dish}`, if_flag: paid },
    {
      op: 'say',
      speaker: MARISOL,
      unless_flag: paid,
      text: "Ay, your purse is light. Come back with sixty wicks — the pot will still be on.",
    },
  ];
}

export const KITCHENS_SCRIPTS: ScriptRegistry = {
  // ---------------------------------------------------------------- PERCY
  'script.moka_percy': [
    { op: 'run', ref: 'script.moka_hello', unless_flag: 'flag:moka_met' },
    { op: 'run', ref: 'script.moka_again', if_flag: 'flag:moka_greeted' },
    { op: 'setFlag', flag: 'flag:moka_greeted' },
    {
      op: 'choice',
      speaker: PERCY,
      prompt: 'Ask me about the pot. Go on. Anything.',
      options: [
        { label: 'HISTORY', ops: [{ op: 'run', ref: 'script.moka_history' }] },
        { label: 'HOW IT WORKS', ops: [{ op: 'run', ref: 'script.moka_how' }] },
        { label: "WHY IT'S THE BEST", ops: [{ op: 'run', ref: 'script.moka_best' }] },
        { label: 'A CUP?', unless_flag: 'flag:moka_cup_given', ops: [{ op: 'run', ref: 'script.moka_cup' }] },
        {
          label: 'NO THANKS',
          ops: [p("No thanks? NO THANKS? ...Fair. The pot doesn't mind. The pot is patient. The pot will be here.")],
        },
      ],
    },
  ],

  'script.moka_hello': [
    { op: 'narrate', text: 'A bald man in an apron crouches over a tiny burner, glaring at a little eight-sided pot.' },
    p("Shh. Shh! Listen. ...Hear that? Not yet. Nearly. It's thinking."),
    { op: 'narrate', text: 'The pot gives a soft, throaty gurgle.' },
    { op: 'emote', actor: 'percy', emote: 'alert' },
    p('THERE. Off the flame. You hear that gurgle, you take it off. Every time. Write it down.'),
    p("Percy. Coffee. Well — moka. The moka pot! The eight-sided pot. Best way to make coffee there is."),
    p('And I will not be taking questions.'),
    p('...I will be taking questions. Please. Nobody ever asks.'),
    { op: 'setFlag', flag: 'flag:moka_met' },
  ],

  'script.moka_again': [p('Back again? Course you are. Nobody walks off from a moka pot mid-sentence.')],

  ...volumes(
    'history',
    [
      p('Born nigh on a hundred years ago, in a hill-country far across the sea.'),
      p("Folk there are SERIOUS about coffee. Argue-at-weddings serious."),
      p("A fellow watched the wash-boiler: water boils below, shoots up a pipe, pours over the laundry."),
      p('And he thought: what if that... but COFFEE.'),
      p('Cast it in aluminium. Light, cheap, heats in a blink.'),
      p('Within a generation there was one on near every stove in that country.'),
      p('A whole country, gurgling at breakfast. Imagine it. I do. Often.'),
    ],
    [
      p('Why EIGHT sides? The facets spread the flame round evenly, so all the water warms at once.'),
      p('No hot spot. No scorch. Just eight honest little walls.'),
      p("And they've barely changed it since. Same shape, near a hundred years. You don't fix perfect."),
      p("You just polish it. ...No! Don't polish it. Ask me WHY IT'S THE BEST. You'll see."),
    ],
  ),

  ...volumes(
    'how',
    [
      p('Three parts. Bottom: water. Middle: a basket for the grounds. Top: where the coffee comes up.'),
      p('Fill the water to just BELOW the valve. That little nub on the side? Safety valve.'),
      p('Cover the valve and the pot sulks. Or worse. Never cover the valve.'),
      p('Grounds: medium-fine. Finer than sand, coarser than flour. Level it off with a fingertip.'),
      p('And NEVER tamp it. Never press it down!'),
      p("Tamp it and the water can't get through. It goes bitter. It goes whistly. Don't make it whistle."),
    ],
    [
      p("Here's the magic. Heat the bottom. The water makes steam, and the steam's got nowhere to go."),
      p('So it PUSHES. Pushes the hot water up the funnel, through the grounds, and out the spout up top.'),
      p('Coffee, rising! A little fountain. Gentle flame. Lid up, if you like, to watch it come.'),
      p("Then — when it gurgles and sputters — OFF the flame. That's the last of the water."),
      p('Any longer and it burns. Some cool the base under cold water. I just take it off and say thank you.'),
    ],
  ),

  ...volumes(
    'best',
    [
      p("Now. It's not quite the short, fierce cup the great hissing machines make."),
      p("And that's the POINT. It's thick, it's bold, it's honest. No machine. No fuss. A flame and a pot."),
      p('It goes anywhere. A stove, a campfire, a burner on a crate in an orchard in the dark.'),
      p("Exhibit A: me. You can't take a hissing machine on your Wayfaring. You can take THIS."),
    ],
    [
      p('NEVER wash it with soap. Rinse it, dry it, done.'),
      p('The coffee oils season the inside, like a good iron pan. That seasoning IS the flavour.'),
      p('Scrub it shiny and it tastes of nothing for a month.'),
      p("I knew a man who scrubbed his. We don't speak of him. He knows what he did."),
      p("And they LAST. A good pot outlives its owner. This was my grandmother's."),
      p("New seal, new basket. Same pot. One day it'll be someone else's."),
      p("That's the other thing it makes, see. Not just coffee. Keeping."),
    ],
  ),

  'script.moka_cup': [
    p('A cup? You want a CUP? Hold out your hands. Both of them. Steady.'),
    { op: 'action', actor: 'percy', action: 'gift', holdMs: 700 },
    { op: 'giveItem', item: 'moka_cup', count: 1 },
    { op: 'say', text: 'He pours a short, dark cup with a little tan foam on top. Got a MOKA CUP!' },
    p('Kin like it too, a sip at a time. Perks them right up. Not too much. Look at me.'),
    { op: 'setFlag', flag: 'flag:moka_cup_given' },
  ],

  // -------------------------------------------------------------- MARISOL
  'script.cantina_marisol': [
    { op: 'run', ref: 'script.cantina_hello', unless_flag: 'flag:cantina_met' },
    { op: 'run', ref: 'script.cantina_again', if_flag: 'flag:cantina_greeted' },
    { op: 'setFlag', flag: 'flag:cantina_greeted' },
    {
      op: 'choice',
      speaker: MARISOL,
      prompt: "What'll it be? Sixty wicks a plate.",
      options: [
        { label: 'ENCHILADAS ROJAS 60W', ops: order('enchiladas') },
        { label: 'CHILAQUILES ROJOS 60W', ops: order('chilaquiles') },
        { label: 'POZOLE ROJO 60W', ops: order('pozole') },
        { label: 'ARROZ ROJO 60W', ops: order('arroz') },
        { label: 'ABOUT THE RED', ops: [{ op: 'run', ref: 'script.cantina_red' }] },
        { label: 'JUST LOOKING', ops: [m("Look all you like. Smelling's free, too.")] },
      ],
    },
  ],

  'script.cantina_hello': [
    { op: 'narrate', text: 'Woodsmoke and toasting chile. A cook in a bright headscarf flips tortillas on a wide iron griddle.' },
    m("Welcome, welcome! I'm Marisol. I came up from a sunny country far to the south, over the sea."),
    m("Back home every kitchen smells like this. Here, only mine. The whole hollow comes to sniff."),
    m("Tonight everything is red. Not from fire — from dried chiles and tomato. Sit. Eat. You'll leave warm."),
    { op: 'setFlag', flag: 'flag:cantina_met' },
  ],

  'script.cantina_again': [m('Hungry again? Good. The pot never sleeps, and neither does the griddle.')],

  // Every plate ends here: everyone restored (a courtesy heal, not a rest point),
  // and the very first plate comes with a jar of salsa for the road (once).
  'script.cantina_meal_end': [
    { op: 'heal', rest: false },
    { op: 'say', text: 'Warm right through. Your kin lick the plate clean and look ready for anything.' },
    { op: 'run', ref: 'script.cantina_salsa_gift', unless_flag: 'flag:cantina_salsa_given' },
  ],

  // Once only: the first plate comes with a jar of salsa.
  'script.cantina_salsa_gift': [
    m('Take this for the road: a jar of my salsa. On the house. A first plate earns a little extra.'),
    { op: 'giveItem', item: 'salsa_roja', count: 1 },
    { op: 'say', text: 'Got a jar of SALSA ROJA!' },
    { op: 'setFlag', flag: 'flag:cantina_salsa_given' },
  ],

  'script.cantina_enchiladas': [
    { op: 'narrate', text: 'She dips corn tortillas in brick-red sauce, warms them, and rolls them round cheese and onion.' },
    m("Enchiladas! The name only means 'put chile in it'. The whole recipe, in one word."),
    m("The sauce: dried red chiles, toasted a breath on the comal — my griddle — then soaked soft."),
    m('Then into the blender with tomato, garlic and a little onion. Simmer it till it shines.'),
    m("Toast the chiles too long and they go bitter. My grandmother could smell it from the next room."),
    m("'Marisol! They're SMOKING!' ...She was always right."),
    m('Folk rolled tortillas round a filling and dipped them in chile long before anyone wrote it down.'),
    m('Every town back home has its own way. This is my grandmother\'s.'),
    { op: 'run', ref: 'script.cantina_meal_end' },
  ],

  'script.cantina_chilaquiles': [
    { op: 'narrate', text: "Yesterday's tortillas, fried crisp, tumbled in red salsa and crowned with cream, cheese and an egg." },
    m('Chilaquiles! A breakfast born from thrift. Nobody back home throws away a tortilla.'),
    m("Yesterday's go stale, so you cut them up, fry them crisp and drown them in salsa."),
    m("And today they're the best thing on the table. That's a kitchen's whole trick, really."),
    m("Crunchy, or soft and soaked? Red or green? That's an argument at every family breakfast."),
    m("Red is right. I'm the cook."),
    m("It's what you eat after a long night. A festival. A wedding. A Wayfaring, maybe?"),
    { op: 'run', ref: 'script.cantina_meal_end' },
  ],

  'script.cantina_pozole': [
    { op: 'narrate', text: 'A deep bowl of brick-red broth, slow pork and fat white hominy, with cabbage, radish and lime.' },
    m('Pozole. This one is OLD — older than the cities back home.'),
    m('It was a feast dish, a ceremony, long before it was ever supper.'),
    m('Those big white kernels are hominy: maize cooked with slaked lime till they burst open like flowers.'),
    m('Slaked lime the mineral, mind. Not the fruit. The fruit goes on top.'),
    m("It's still for celebrating. Birthdays, feast days, a whole street on a holiday night."),
    m('Red, white or green, depending which valley your grandmother came from.'),
    m('You finish it yourself: cabbage, radish, a pinch of oregano, a squeeze of lime. Go on.'),
    { op: 'run', ref: 'script.cantina_meal_end' },
  ],

  'script.cantina_arroz': [
    { op: 'narrate', text: 'Rice fried golden, then simmered in tomato broth with garlic, peas and carrot. Fluffy as a cloud.' },
    m('Arroz rojo. Rice came over the sea to my country long ago, and we made it ours.'),
    m('Fry it first, then cook it in tomato. Frying the grains is the secret — every one stays apart.'),
    m("Stir it once the lid's on and I'll know. I will KNOW."),
    m('It sits beside everything. Every family thinks theirs is the best. Every family is right.'),
    { op: 'run', ref: 'script.cantina_meal_end' },
  ],

  'script.cantina_red': [
    m('Everything red here starts with the chiles. Dried long and wrinkled, nearly black.'),
    m('See them hanging off my awning? Back home they hang in long strings to dry in the sun.'),
    m('Toast them on the comal, soak them soft, blend them with tomato. That is the red.'),
    m('Some salsas are cooked and silky, some raw and chunky. Every house has its own secret.'),
    m('And corn! Nothing here works without corn.'),
    m('We cook the maize with lime — nixtamal, we call it — then grind it into masa, the tortilla dough.'),
    m('That trick is thousands of years old. It makes the corn kinder to the body.'),
    m('And it makes it taste like home.'),
  ],
};

export const KITCHENS_DIALOGUE: DialogueRegistry = {};
