/**
 * THE WILD WAYS (2026-10, docs/world/walkthrough/09-the-wild-ways.md) — the
 * Wick-Run (A): the downhill runner run, the Tallow Lift, the Runners.
 * This area's lane OWNS this file: new scripts + dialogue only, spread into the
 * registries via regions/index.ts (a ref here must be NEW, never an override).
 *
 * Flags this file owns:
 *   flag:wickrun_riding     a rented runner is out (the start-gate key); cleared at the foot
 *   flag:wickrun_rent_paid  transient: the `pay` op's receipt, cleared at once
 *   flag:tallow_lift_freed  the lift's brake is off — the lift runs both ways
 *   flag:runner_ribbon      Rook's ribbon for a gold run — rentals are free after
 *   flag:wickrun_rented     you've rented a runner once (opens the JOURNAL entry)
 *   flag:wickrun_gold/_silver/_bronze   the run clock's tiers (set by the `timer` op)
 *   flag:wickrun_gold_paid/_silver_paid/_bronze_paid   each tier's one-time prize paid
 *   flag:runner_<name>_beaten   the Runners (pt.trainer_beat), Rook the captain last
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

const RIDING = 'flag:wickrun_riding';
const PAID = 'flag:wickrun_rent_paid';
const FREED = 'flag:tallow_lift_freed';
const RIBBON = 'flag:runner_ribbon';
const RENTED = 'flag:wickrun_rented';
const GOLD = 'flag:wickrun_gold';
const SILVER = 'flag:wickrun_silver';
const BRONZE = 'flag:wickrun_bronze';
const ROOK_BEATEN = 'flag:runner_rook_beaten';

/**
 * The run clock's tiers (fastest first). Measured, not guessed: the fastest
 * line from the start gate to the finish band is ~17.1 s of riding at the
 * runner's 64 ms a tile (the slope carry runs at the same pace; leaps add
 * 60 ms) plus four map changes at ~1.5 s each — so ~23 s flat out. Gold sits
 * just above that; silver ~+25%, bronze ~+60%. (09-the-wild-ways §2 A.)
 */
export const WICKRUN_TIERS = [
  { ms: 26_000, flag: GOLD, label: 'GOLD' },
  { ms: 32_500, flag: SILVER, label: 'SILVER' },
  { ms: 41_500, flag: BRONZE, label: 'BRONZE' },
];
/** Each tier pays once (mirrored in tools/balance/progression.mjs). */
export const WICKRUN_PRIZES = { gold: 600, silver: 400, bronze: 200 } as const;
/** Repeat runs at a tier already prized pay this day purse. Optional income outside every
 *  solvency leg, so not modelled in progression.mjs (10-economy §2 lists it). */
export const WICKRUN_DAY_PURSE = { gold: 250, silver: 100 } as const;

/** Where the lift sets you down at each end (the cars' platforms). */
export const LIFT_TOP = { map: 'wickrun_crest', to: { tx: 23, ty: 15 }, facing: 'down' as const };
export const LIFT_FOOT = { map: 'wickrun_foot', to: { tx: 21, ty: 13 }, facing: 'down' as const };

export const WICKRUN_SCRIPTS: ScriptRegistry = {
  // ---- the crest ------------------------------------------------------------
  'script.wickrun_rental': [
    { op: 'say', speaker: 'PELL', unless_flag: RIDING, text: 'Runners! Two wheels, one brake, no regrets. The Wick-Run\'s the old wax road — top of the mountain to the sea, if your nerve holds.' },
    { op: 'say', speaker: 'PELL', unless_flag: RIDING, text: 'Fair warning: the kin on the run are mountain-fed — tougher than the Solarium\'s garden lot — and there\'s no pedalling back up. Lucan\'s lit stage first, if I were you.' },
    { op: 'say', speaker: 'PELL', if_flag: RIDING, text: 'You\'ve got one of mine already. Off you go — through the gate and down. Hand it in at the foot; the lift-keeper sends them home.' },
    { op: 'run', ref: 'script.wickrun_rental_offer', unless_flag: RIDING },
  ],
  // Walking into the start-gate without a runner (playtest 2026-10): Pell calls
  // out and offers the rental right there, instead of sending you back up the
  // crest to find him — rent one and the engine carries you on through the gate.
  'script.wickrun_gate_offer': [
    { op: 'emote', actor: 'pell', emote: 'alert' },
    { op: 'dialogue', ref: 'npc.wickrun_gate_blocked' },
    { op: 'run', ref: 'script.wickrun_rental_offer' },
  ],
  'script.wickrun_rental_offer': [
    {
      op: 'choice',
      speaker: 'PELL',
      prompt: 'Rent a runner? (300 wicks)',
      options: [
        {
          label: 'RENT ONE',
          unless_flag: RIBBON,
          ops: [
            { op: 'pay', amount: 300, flag: PAID },
            { op: 'say', speaker: 'PELL', unless_flag: PAID, text: 'Three hundred wicks, and I don\'t do credit. The wax trade\'s been dead eleven winters — I\'m not starting tabs now.' },
            { op: 'run', ref: 'script.wickrun_hand_runner', if_flag: PAID },
            { op: 'setFlag', flag: PAID, value: false },
          ],
        },
        {
          label: 'RIBBON RIDE',
          if_flag: RIBBON,
          ops: [
            { op: 'say', speaker: 'PELL', text: 'Rook\'s ribbon! Put your wicks away — gold riders ride free on Pell\'s runners. House rule. As of now.' },
            { op: 'run', ref: 'script.wickrun_hand_runner' },
          ],
        },
        { label: 'NOT TODAY', ops: [{ op: 'say', speaker: 'PELL', text: 'Sensible. Boring, but sensible.' }] },
      ],
    },
  ],
  'script.wickrun_hand_runner': [
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'runner' },
    { op: 'setFlag', flag: RIDING },
    { op: 'setFlag', flag: RENTED },
    { op: 'narrate', text: 'You got a RUNNER! Two wheels of waxed ash and brass. On the Wick-Run you\'ll ride it — steer with left and right; the mountain does the rest.' },
    { op: 'say', speaker: 'PELL', text: 'Rules: you can\'t pedal UP the run, so don\'t miss anything you want. Hit a kicker straight and you\'ll fly. And the lift at the bottom only runs once someone up here\'s let the brake off.' },
  ],
  'script.tallow_lift_top': [
    { op: 'narrate', unless_flag: FREED, text: 'THE TALLOW LIFT. A great drum of cable, and a car hanging at the platform, chained fast. A rusted brake-lever reads: HOLD UNTIL THE WAX RUNS.' },
    { op: 'say', speaker: 'PELL', unless_flag: FREED, text: 'The lift? Chained the winter the vines shut — no wax to send down, no reason to haul the carts back up. Throw the brake if you like. Might as well let the old thing breathe.' },
    { op: 'sfx', key: 'world-door', unless_flag: FREED },
    { op: 'shake', ms: 400, intensity: 0.004, unless_flag: FREED },
    { op: 'narrate', unless_flag: FREED, text: 'The brake comes free with a groan. Far below, the cable shivers all the way down to the sea. The Tallow Lift is running again — both ways.' },
    { op: 'setFlag', flag: FREED },
    {
      op: 'choice',
      prompt: 'Ride the Tallow Lift down to the foot?',
      options: [
        {
          label: 'RIDE DOWN',
          ops: [
            { op: 'run', ref: 'script.wickrun_hand_in_top', if_flag: RIDING },
            { op: 'musicSting', key: 'tallow-lift' },
            { op: 'narrate', text: 'The car lurches off the platform and sinks along the cable — the run\'s lamps drawing a crooked line down the dark mountain beside you, the sea opening below.' },
            { op: 'travel', map: LIFT_FOOT.map, to: LIFT_FOOT.to, facing: LIFT_FOOT.facing },
          ],
        },
        { label: 'STAY UP HERE', ops: [] },
      ],
    },
  ],
  'script.wickrun_crest_rest': [
    { op: 'narrate', text: 'The chandlery\'s old rendering hearth. Someone keeps a fire in it for the Runners — the last warm spot before a long way down.' },
    { op: 'heal', sleep: false },
    { op: 'narrate', text: 'You warm your hands and your kin curl up by the coals. Rested.' },
  ],

  // ---- the run --------------------------------------------------------------
  'script.wickrun_start': [
    { op: 'timer', id: 'wickrun', action: 'start' },
  ],
  'script.runner_vess': [
    { op: 'say', speaker: 'VESS', text: 'Hey! You can\'t just roll past the Runners\' landing. That\'s a challenge where I come from. Wheels down, kin out!' },
    { op: 'battle', trainer: 'runner_vess' },
    { op: 'say', speaker: 'VESS', text: 'Fine, fine. Tip: the east line\'s faster, but there\'s a kicker on it. Hit it straight or eat a boulder.' },
    { op: 'setFlag', flag: 'flag:runner_vess_beaten' },
  ],
  'script.runner_dace': [
    { op: 'say', speaker: 'DACE', text: 'Made it to the shelf in one piece? Rook says nobody\'s a Runner till they\'ve lost to one. Let\'s fix that.' },
    { op: 'battle', trainer: 'runner_dace' },
    { op: 'say', speaker: 'DACE', text: '...Or till they\'ve beaten one. Rook\'s waiting at the bottom. He\'s got the record and he won\'t shut up about it.' },
    { op: 'setFlag', flag: 'flag:runner_dace_beaten' },
  ],
  'script.pickup_wickrun_ledge': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'Only a rider off a kicker could land up here. Tucked in a wax-cart\'s old tool-box: a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:picked_wickrun_ledge' },
  ],

  // ---- the trestles ---------------------------------------------------------
  'script.runner_tamsin': [
    { op: 'say', speaker: 'TAMSIN', text: 'Through the barrels without a scratch? Show-off. Nobody rides the trestle till they\'ve got past me.' },
    { op: 'battle', trainer: 'runner_tamsin' },
    { op: 'say', speaker: 'TAMSIN', text: 'Ugh. Go on, then. Ride the boards — and duck on the way back. You\'ll see what I mean.' },
    { op: 'setFlag', flag: 'flag:runner_tamsin_beaten' },
  ],
  'script.runner_ossie': [
    { op: 'say', speaker: 'OSSIE', text: 'Round the knoll the long way, like everyone. Bet you thought you could cut inside. Kin out!' },
    { op: 'battle', trainer: 'runner_ossie' },
    { op: 'say', speaker: 'OSSIE', text: 'The old carters called this the Spiral. The wax went OVER the gully, round, and back UNDER itself. Nobody knows why they didn\'t just go straight.' },
    { op: 'setFlag', flag: 'flag:runner_ossie_beaten' },
  ],
  'script.pickup_wickrun_purse': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: 'Wedged behind a stone where the steps begin — a Runner\'s purse, shaken loose on the hop. Found 300 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_wickrun_purse' },
  ],

  // ---- the traverse ----------------------------------------------------------
  'script.runner_pip': [
    { op: 'say', speaker: 'PIP', text: 'Wait wait wait — you came down the Spiral already? Then you\'re fair game. Rook says I need practice.' },
    { op: 'battle', trainer: 'runner_pip' },
    { op: 'say', speaker: 'PIP', text: 'Steer UP or DOWN through the rocks — never think about east. East is uphill. Uphill is for the lift.' },
    { op: 'setFlag', flag: 'flag:runner_pip_beaten' },
  ],
  'script.pickup_wickrun_wreck': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'The cart left the road eleven winters ago and nobody came back for it. Under the spilled wax, still in its tin: a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_wickrun_wreck' },
  ],

  // ---- the lower run -----------------------------------------------------------
  'script.runner_rook': [
    { op: 'say', speaker: 'ROOK', text: 'There you are. I heard you coming three bends back — you brake like a cart with a stuck wheel.' },
    { op: 'say', speaker: 'ROOK', text: 'I\'m Rook. I run the Runners, and the Runners run this hill. Nobody reaches the foot without getting past the camp. House rule.' },
    { op: 'battle', trainer: 'runner_rook' },
    { op: 'say', speaker: 'ROOK', text: 'Hah! All right. You can ride. Now go and see if you can RACE.' },
    { op: 'say', speaker: 'ROOK', text: 'Crest to sea under twenty-six seconds is gold. Do that, and I\'ll be waiting at the foot with something for you.' },
    { op: 'setFlag', flag: ROOK_BEATEN },
  ],
  'script.pickup_wickrun_brake_hut': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'wax_cake', count: 2 },
    { op: 'say', text: 'The carters\' old brake-hut shelf — you only reach it off a kicker. Two pressed rounds of chandlery wax, still stamped: 2 WAX CAKES!' },
    { op: 'setFlag', flag: 'flag:picked_wickrun_brake_hut' },
  ],

  // ---- the foot ------------------------------------------------------------------
  'script.wickrun_finish': [
    { op: 'timer', id: 'wickrun', action: 'stop', tiers: WICKRUN_TIERS },
    // The Runners' DAY PURSE (2026-10 economy review): a repeat run at a tier whose
    // one-time prize was paid on an EARLIER run (these run before the prizes, so
    // the first gold never pays twice). Best tier only; silver waits for the ribbon
    // (free rentals) — before it, the 300w rental would make a silver lap a loss.
    { op: 'run', ref: 'script.wickrun_purse_gold', if_flag: 'flag:wickrun_gold_now' },
    { op: 'run', ref: 'script.wickrun_purse_silver', if_flag: 'flag:wickrun_silver_now', unless_flag: 'flag:wickrun_gold_now' },
    { op: 'run', ref: 'script.wickrun_prize_gold', if_flag: GOLD, unless_flag: 'flag:wickrun_gold_paid' },
    { op: 'run', ref: 'script.wickrun_prize_silver', if_flag: SILVER, unless_flag: 'flag:wickrun_silver_paid' },
    { op: 'run', ref: 'script.wickrun_prize_bronze', if_flag: BRONZE, unless_flag: 'flag:wickrun_bronze_paid' },

    { op: 'run', ref: 'script.wickrun_hand_in', if_flag: RIDING },
    { op: 'run', ref: 'script.rook_ribbon_check', if_flag: GOLD, unless_flag: RIBBON },
  ],
  'script.wickrun_purse_gold': [
    { op: 'run', ref: 'script.wickrun_purse_gold_pay', if_flag: 'flag:wickrun_gold_paid' },
  ],
  'script.wickrun_purse_gold_pay': [
    { op: 'giveMoney', amount: WICKRUN_DAY_PURSE.gold },
    { op: 'narrate', text: `Another GOLD run. The Runners' kitty coughs up its day purse: ${WICKRUN_DAY_PURSE.gold} WICKS.` },
  ],
  'script.wickrun_purse_silver': [
    { op: 'run', ref: 'script.wickrun_purse_silver_pay', if_flag: 'flag:wickrun_silver_paid' },
  ],
  'script.wickrun_purse_silver_pay': [
    { op: 'run', ref: 'script.wickrun_purse_silver_give', if_flag: RIBBON },
  ],
  'script.wickrun_purse_silver_give': [
    { op: 'giveMoney', amount: WICKRUN_DAY_PURSE.silver },
    { op: 'narrate', text: `A tidy SILVER run. The kitty spares ${WICKRUN_DAY_PURSE.silver} WICKS.` },
  ],
  'script.wickrun_prize_gold': [
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: WICKRUN_PRIZES.gold },
    { op: 'narrate', text: 'The lift-keeper rings the finish bell three times — a GOLD run! The Runners\' kitty pays out: 600 WICKS.' },
    { op: 'setFlag', flag: 'flag:wickrun_gold_paid' },
  ],
  'script.wickrun_prize_silver': [
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: WICKRUN_PRIZES.silver },
    { op: 'narrate', text: 'Twice on the finish bell — your first SILVER run. The Runners\' kitty pays out: 400 WICKS.' },
    { op: 'setFlag', flag: 'flag:wickrun_silver_paid' },
  ],
  'script.wickrun_prize_bronze': [
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: WICKRUN_PRIZES.bronze },
    { op: 'narrate', text: 'One ring on the finish bell — your first BRONZE run. The Runners\' kitty pays out: 200 WICKS.' },
    { op: 'setFlag', flag: 'flag:wickrun_bronze_paid' },
  ],
  'script.wickrun_hand_in': [
    { op: 'takeItem', item: 'runner' },
    { op: 'setFlag', flag: RIDING, value: false },
    { op: 'say', speaker: 'LIFT-KEEPER', text: 'I\'ll take that runner. It goes up on the next car — Pell counts them like hens.' },
  ],
  'script.wickrun_hand_in_top': [
    { op: 'timer', id: 'wickrun', action: 'cancel' },
    { op: 'takeItem', item: 'runner' },
    { op: 'setFlag', flag: RIDING, value: false },
    { op: 'say', speaker: 'PELL', text: 'Riding the lift DOWN? With my runner? No. Leave it here — rent it again when your nerve comes back.' },
  ],
  'script.rook_ribbon_check': [
    { op: 'run', ref: 'script.rook_ribbon', if_flag: ROOK_BEATEN },
  ],
  'script.rook_ribbon': [
    { op: 'say', speaker: 'ROOK', text: 'GOLD. Under twenty-six. Huh. I thought that was mine.' },
    { op: 'say', speaker: 'ROOK', text: 'Fine. A promise is a promise.' },
    { op: 'sfx', key: 'world-keyitem' },
    { op: 'giveItem', item: 'runner_ribbon' },
    { op: 'setFlag', flag: RIBBON },
    { op: 'narrate', text: 'You got the RUNNER\'S RIBBON! Waxed red silk on a brass pin. Pell will rent you runners for free from now on.' },
    { op: 'say', speaker: 'ROOK', text: 'Don\'t let it go to your head. The record\'s still mine — for now.' },
  ],
  'script.rook_foot': [
    { op: 'run', ref: 'script.rook_ribbon', if_flag: GOLD, unless_flag: RIBBON },
    { op: 'say', speaker: 'ROOK', if_flag: RIBBON, text: 'Ribbon-holder! The kids up top are making up songs about you. Terrible songs. You should hear them.' },
    { op: 'say', speaker: 'ROOK', unless_flag: GOLD, text: 'Crest to sea under twenty-six seconds — that\'s gold. Gap on the right through the barrels, hit every kicker square, and don\'t stop for the view.' },
  ],
  'script.tallow_lift_foot': [
    { op: 'say', speaker: 'LIFT-KEEPER', unless_flag: FREED, text: 'The Tallow Lift? Car\'s up at the crest, chained to the top house. Has been since the vines shut and the wax stopped coming down.' },
    { op: 'say', speaker: 'LIFT-KEEPER', unless_flag: FREED, text: 'Someone up there has to let the brake off. And nobody walks UP the Wick-Run — it\'s all chute. Come at it from the Sunvault side, if you ever get that high.' },
    {
      op: 'choice',
      if_flag: FREED,
      speaker: 'LIFT-KEEPER',
      prompt: 'Ride the Tallow Lift up to the crest?',
      options: [
        {
          label: 'RIDE UP',
          ops: [
            { op: 'musicSting', key: 'tallow-lift' },
            { op: 'narrate', text: 'The car shudders off its platform and climbs the cable — the sea shrinking below, the run\'s lamps sliding past in a crooked line, up into the dark of the mountain.' },
            { op: 'travel', map: LIFT_TOP.map, to: LIFT_TOP.to, facing: LIFT_TOP.facing },
          ],
        },
        { label: 'NOT NOW', ops: [{ op: 'say', speaker: 'LIFT-KEEPER', text: 'She\'ll be here. She\'s been here eleven winters.' }] },
      ],
    },
  ],
  'script.wickrun_foot_rest': [
    { op: 'narrate', text: 'The yard bench, worn smooth by the carters who waited here for the lift. The sea is loud and the lamps are warm.' },
    { op: 'heal', sleep: false },
    { op: 'narrate', text: 'You sit a while with your kin and listen to the waves. Rested.' },
  ],
};

export const WICKRUN_DIALOGUE: DialogueRegistry = {
  'npc.wickrun_gate_blocked': [
    { speaker: 'PELL', text: 'Oi! Nobody goes down the run on foot. It\'s steep enough to make you a legend or a lesson. Rent a runner first.' },
  ],
  'npc.wickrun_runner_kid': [
    { text: 'Rook did the whole run, crest to sea, in twenty-four seconds. TWENTY-FOUR. My kin got dizzy just watching.' },
    { text: 'The wax used to come down this way in carts, Pell says. Can you imagine? Carts! No brakes!' },
  ],
  'sign.wickrun_crest': [
    { text: 'THE WICK-RUN. The old wax road, Sunvault to the sea. Runners for hire. NO WALKERS. NO PEDALLING UP. NO REFUNDS.' },
  ],
  'sign.wickrun_runout': [
    { text: 'THE SHELF. Halfway down. The trestles are below — keep your line on the boards and watch for the turn back under.' },
  ],
  'npc.runner_vess_after': [
    { speaker: 'VESS', text: 'Some of us like the landing. You can actually SEE the mountain from here.' },
  ],
  'npc.runner_dace_after': [
    { speaker: 'DACE', text: 'Catch your breath on the shelf while you can. The trestles below don\'t give you a second.' },
  ],
  'sign.wickrun_trestle': [
    { text: 'THE SPIRAL TRESTLE. Ride the boards over the gully, round the knoll, and back under. MIND YOUR HEADS. — the Carters\' Guild' },
  ],
  'sign.wickrun_steps': [
    { text: 'THE STEPS. Three drops to the traverse. Hop where the fence lets you. No climbing back — this means you, Pip.' },
  ],
  'sign.wickrun_traverse': [
    { text: 'THE TRAVERSE. The road turns west across the flank. ROCKS IN THE ROAD. Steer, don\'t brake. Kickers at the far end — hit them square.' },
  ],
  'sign.wickrun_lower': [
    { text: 'THE LOWER RUN. The long straight. The carts used to make the sea from here without touching a brake. So do the Runners. So will you.' },
  ],
  'sign.wickrun_camp': [
    { text: 'RUNNERS\' CAMP. Last landing before the foot. Visitors welcome. Challengers more welcome. — ROOK' },
  ],
  'sign.wickrun_foot_lift': [
    { text: 'THE TALLOW LIFT · FOOT STATION. Empties up, Runners up. The car runs only when the crest brake is off.' },
  ],
  'sign.wickrun_foot': [
    { text: 'WICK-RUN FOOT. The finish. Runners hand in here. The beach road runs east to Lightkeeper\'s Point and Pearlmoor.' },
  ],
  'npc.wickrun_yard_hand': [
    { speaker: 'YARD-HAND', text: 'This yard used to be ankle-deep in wax. The carts came screaming out of that chute, and we\'d barrow the cakes east to the Pearlmoor boats before they cooled.' },
    { speaker: 'YARD-HAND', text: 'Every wick in Vesperholm started up on that mountain, you know. The wicks in your purse too. Then the vines shut, the wax stopped, and here we all are — keeping the lamps lit on what\'s left.' },
  ],
  'npc.runner_tamsin_after': [
    { speaker: 'TAMSIN', text: 'Best view on the hill is from the middle of the trestle. Don\'t stop to look, though. You\'ll get a wheel in the back.' },
  ],
  'npc.runner_ossie_after': [
    { speaker: 'OSSIE', text: 'Over, round, under. Over, round, under. I say it in my sleep.' },
  ],
  'npc.runner_pip_after': [
    { speaker: 'PIP', text: 'One day I\'m going to clear the whole rockfall in one go. One day.' },
  ],
  'npc.runner_rook_after': [
    { speaker: 'ROOK', text: 'The camp\'s the last flat ground before the sea. Breathe. Then go fast.' },
  ],
};
