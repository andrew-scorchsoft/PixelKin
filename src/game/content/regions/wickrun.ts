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
    { op: 'say', speaker: 'PELL', unless_flag: RIDING, text: 'Runners! Two wheels, one brake, no regrets. Mountain to sea, nerve allowing.' },
    { op: 'say', speaker: 'PELL', unless_flag: RIDING, text: 'Fair warning: the run\'s kin are mountain-fed, and there\'s no pedalling back up. [[Lucan\'s lit stage]] first, if I were you.' },
    { op: 'say', speaker: 'PELL', if_flag: RIDING, text: 'You\'ve one of mine already. [[Through the gate and down]] — hand it in at the foot.' },
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
            { op: 'say', speaker: 'PELL', unless_flag: PAID, text: 'Three hundred wicks. No credit: the wax trade\'s been dead eleven winters.' },
            { op: 'run', ref: 'script.wickrun_hand_runner', if_flag: PAID },
            { op: 'setFlag', flag: PAID, value: false },
          ],
        },
        {
          label: 'RIBBON RIDE',
          if_flag: RIBBON,
          ops: [
            { op: 'say', speaker: 'PELL', text: 'Rook\'s ribbon! Gold riders ride free. House rule. As of now.' },
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
    { op: 'narrate', text: 'You got a RUNNER! [[Steer with left and right]]. The mountain does the rest.' },
    { op: 'say', speaker: 'PELL', text: 'Rules: [[no pedalling UP]], so don\'t miss anything. Hit a kicker straight and you fly. The lift only runs once someone up here [[lets the brake off]].' },
  ],
  'script.tallow_lift_top': [
    { op: 'narrate', unless_flag: FREED, text: 'THE TALLOW LIFT, chained. The rusted brake reads: HOLD UNTIL THE WAX RUNS.' },
    { op: 'say', speaker: 'PELL', unless_flag: FREED, text: 'The lift? Chained since the vines shut. Throw the brake. Let it breathe.' },
    { op: 'sfx', key: 'world-door', unless_flag: FREED },
    { op: 'shake', ms: 400, intensity: 0.004, unless_flag: FREED },
    { op: 'narrate', unless_flag: FREED, text: 'The brake groans free. Far below, the cable shivers. The lift runs again!' },
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
            { op: 'narrate', text: 'The car sinks along the cable, the run\'s lamps beside you, the sea below.' },
            { op: 'travel', map: LIFT_FOOT.map, to: LIFT_FOOT.to, facing: LIFT_FOOT.facing },
          ],
        },
        { label: 'STAY UP HERE', ops: [] },
      ],
    },
  ],
  'script.wickrun_crest_rest': [
    { op: 'narrate', text: 'The chandlery\'s old hearth, kept lit for the Runners before the drop.' },
    { op: 'heal', sleep: false },
    { op: 'narrate', text: 'You warm your hands and your kin curl up by the coals. Rested.' },
  ],

  // ---- the run --------------------------------------------------------------
  'script.wickrun_start': [
    { op: 'timer', id: 'wickrun', action: 'start' },
  ],
  'script.runner_vess': [
    { op: 'say', speaker: 'VESS', text: 'Hey! Nobody rolls past the Runners\' landing without a fight. Kin out!' },
    { op: 'battle', trainer: 'runner_vess' },
    { op: 'say', speaker: 'VESS', text: 'Tip: the east line\'s faster but has a kicker. Hit it straight or eat rock.' },
    { op: 'setFlag', flag: 'flag:runner_vess_beaten' },
  ],
  'script.runner_dace': [
    { op: 'say', speaker: 'DACE', text: 'Made the shelf? Nobody\'s a Runner till they\'ve lost to one. Let\'s fix that.' },
    { op: 'battle', trainer: 'runner_dace' },
    { op: 'say', speaker: 'DACE', text: '...Or beaten one. Rook\'s at the bottom with the record. He won\'t shut up about it.' },
    { op: 'setFlag', flag: 'flag:runner_dace_beaten' },
  ],
  'script.pickup_wickrun_ledge': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'lumen_drop', count: 1 },
    { op: 'say', text: 'Only a kicker lands you up here. In a wax-cart\'s old tool-box: a LUMEN DROP!' },
    { op: 'setFlag', flag: 'flag:picked_wickrun_ledge' },
  ],

  // ---- the trestles ---------------------------------------------------------
  'script.runner_tamsin': [
    { op: 'say', speaker: 'TAMSIN', text: 'Through the barrels clean? Show-off. Nobody rides the trestle past me.' },
    { op: 'battle', trainer: 'runner_tamsin' },
    { op: 'say', speaker: 'TAMSIN', text: 'Ugh. Go on, ride the boards — and duck on the way back. You\'ll see.' },
    { op: 'setFlag', flag: 'flag:runner_tamsin_beaten' },
  ],
  'script.runner_ossie': [
    { op: 'say', speaker: 'OSSIE', text: 'Round the long way, like everyone. Thought you could cut inside? Kin out!' },
    { op: 'battle', trainer: 'runner_ossie' },
    { op: 'say', speaker: 'OSSIE', text: 'The Spiral: OVER the gully, round, back UNDER itself. Why not go straight? Nobody knows.' },
    { op: 'setFlag', flag: 'flag:runner_ossie_beaten' },
  ],
  'script.pickup_wickrun_purse': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveMoney', amount: 300 },
    { op: 'say', text: 'A Runner\'s purse, shaken loose on the hop. Found 300 WICKS!' },
    { op: 'setFlag', flag: 'flag:picked_wickrun_purse' },
  ],

  // ---- the traverse ----------------------------------------------------------
  'script.runner_pip': [
    { op: 'say', speaker: 'PIP', text: 'You\'ve done the Spiral already? Fair game. Rook says I need practice.' },
    { op: 'battle', trainer: 'runner_pip' },
    { op: 'say', speaker: 'PIP', text: '[[Steer UP or DOWN]] in the rocks. Never east. East is uphill, for the lift.' },
    { op: 'setFlag', flag: 'flag:runner_pip_beaten' },
  ],
  'script.pickup_wickrun_wreck': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'beacon_charge', count: 1 },
    { op: 'say', text: 'Under a wrecked cart\'s spilled wax, still in its tin: a BEACON CHARGE!' },
    { op: 'setFlag', flag: 'flag:picked_wickrun_wreck' },
  ],

  // ---- the lower run -----------------------------------------------------------
  'script.runner_rook': [
    { op: 'say', speaker: 'ROOK', text: 'Heard you three bends back. You brake like a cart with a stuck wheel.' },
    { op: 'say', speaker: 'ROOK', text: 'I\'m Rook. The Runners run this hill, and I run them. Beat me first.' },
    { op: 'battle', trainer: 'runner_rook' },
    { op: 'say', speaker: 'ROOK', text: 'Hah! All right. You can ride. Now go and see if you can RACE.' },
    { op: 'say', speaker: 'ROOK', text: '[[Crest to sea under twenty-six seconds]] is gold. Do that, and I\'ll be at the foot with something for you.' },
    { op: 'setFlag', flag: ROOK_BEATEN },
  ],
  'script.pickup_wickrun_brake_hut': [
    { op: 'sfx', key: 'world-pickup' },
    { op: 'giveItem', item: 'wax_cake', count: 2 },
    { op: 'say', text: 'The carters\' brake-hut shelf, only reached off a kicker. Found 2 WAX CAKES!' },
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
    { op: 'narrate', text: `Another GOLD run. The kitty coughs up its day purse: ${WICKRUN_DAY_PURSE.gold} WICKS.` },
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
    { op: 'narrate', text: 'Three rings — a GOLD run! The Runners\' kitty pays out: 600 WICKS.' },
    { op: 'setFlag', flag: 'flag:wickrun_gold_paid' },
  ],
  'script.wickrun_prize_silver': [
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: WICKRUN_PRIZES.silver },
    { op: 'narrate', text: 'Two rings — your first SILVER run! The Runners\' kitty pays out: 400 WICKS.' },
    { op: 'setFlag', flag: 'flag:wickrun_silver_paid' },
  ],
  'script.wickrun_prize_bronze': [
    { op: 'sfx', key: 'world-wicks' },
    { op: 'giveMoney', amount: WICKRUN_PRIZES.bronze },
    { op: 'narrate', text: 'One ring — your first BRONZE run! The Runners\' kitty pays out: 200 WICKS.' },
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
    { op: 'say', speaker: 'PELL', text: 'The lift DOWN, with my runner? No. Leave it. Rent again when you\'re braver.' },
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
    { op: 'narrate', text: 'You got the RUNNER\'S RIBBON! From now on, [[Pell\'s runners are free]].' },
    { op: 'say', speaker: 'ROOK', text: 'Don\'t let it go to your head. The record\'s still mine — for now.' },
  ],
  'script.rook_foot': [
    { op: 'run', ref: 'script.rook_ribbon', if_flag: GOLD, unless_flag: RIBBON },
    { op: 'say', speaker: 'ROOK', if_flag: RIBBON, text: 'Ribbon-holder! The kids up top are making songs about you. Terrible songs.' },
    { op: 'say', speaker: 'ROOK', unless_flag: GOLD, text: '[[Under twenty-six seconds]] is gold. Right-hand gap through the barrels, every kicker square, no stopping for the view.' },
  ],
  'script.tallow_lift_foot': [
    { op: 'say', speaker: 'LIFT-KEEPER', unless_flag: FREED, text: 'The Tallow Lift? Car\'s been chained at the crest since the wax stopped.' },
    { op: 'say', speaker: 'LIFT-KEEPER', unless_flag: FREED, text: 'Someone has to [[let the brake off up top]]. Nobody walks UP the Wick-Run — come at it [[from the Sunvault side]].' },
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
            { op: 'narrate', text: 'The car climbs the cable, the sea shrinking, the run\'s lamps sliding past.' },
            { op: 'travel', map: LIFT_TOP.map, to: LIFT_TOP.to, facing: LIFT_TOP.facing },
          ],
        },
        { label: 'NOT NOW', ops: [{ op: 'say', speaker: 'LIFT-KEEPER', text: 'She\'ll be here. She\'s been here eleven winters.' }] },
      ],
    },
  ],
  'script.wickrun_foot_rest': [
    { op: 'narrate', text: 'The carters\' bench, worn smooth. The sea is loud; the lamps are warm.' },
    { op: 'heal', sleep: false },
    { op: 'narrate', text: 'You sit a while with your kin and listen to the waves. Rested.' },
  ],
};

export const WICKRUN_DIALOGUE: DialogueRegistry = {
  'npc.wickrun_gate_blocked': [
    { speaker: 'PELL', text: 'Oi! Nobody walks the run. [[Rent a runner]] first — or be a lesson.' },
  ],
  'npc.wickrun_runner_kid': [
    { text: 'Rook did the run in twenty-four seconds. TWENTY-FOUR. My kin got dizzy.' },
    { text: 'The wax came down this way in carts, Pell says. Carts! No brakes!' },
  ],
  'sign.wickrun_crest': [
    { text: 'THE WICK-RUN. Runners for hire. NO WALKERS. NO PEDALLING UP. NO REFUNDS.' },
  ],
  'sign.wickrun_runout': [
    { text: 'THE SHELF. Halfway. Trestles below: watch for the turn back under.' },
  ],
  'npc.runner_vess_after': [
    { speaker: 'VESS', text: 'Some of us like the landing. You can actually SEE the mountain from here.' },
  ],
  'npc.runner_dace_after': [
    { speaker: 'DACE', text: 'Breathe on the shelf while you can. The trestles don\'t give you a second.' },
  ],
  'sign.wickrun_trestle': [
    { text: 'THE SPIRAL TRESTLE. Over, round the knoll, back under. MIND YOUR HEADS.' },
  ],
  'sign.wickrun_steps': [
    { text: 'THE STEPS. Hop where the fence lets you. No climbing back — this means you, Pip.' },
  ],
  'sign.wickrun_traverse': [
    { text: 'THE TRAVERSE. ROCKS IN THE ROAD: steer, don\'t brake. Hit the end kickers square.' },
  ],
  'sign.wickrun_lower': [
    { text: 'THE LOWER RUN. The carts made the sea from here brakeless. So will you.' },
  ],
  'sign.wickrun_camp': [
    { text: 'RUNNERS\' CAMP. Last landing before the foot. Challengers welcome. — ROOK' },
  ],
  'sign.wickrun_foot_lift': [
    { text: 'TALLOW LIFT · FOOT STATION. Runs only when the crest brake is off.' },
  ],
  'sign.wickrun_foot': [
    { text: 'WICK-RUN FOOT. Hand runners in. EAST: [[Lightkeeper\'s Point, Pearlmoor]].' },
  ],
  'npc.wickrun_yard_hand': [
    { speaker: 'YARD-HAND', text: 'This yard was ankle-deep in wax once. Carts screamed out of that chute; we barrowed the cakes east to the boats.' },
    { speaker: 'YARD-HAND', text: 'Every wick in Vesperholm started on that mountain — the ones in your purse too. Then the vines shut, and here we are, lighting lamps on what\'s left.' },
  ],
  'npc.runner_tamsin_after': [
    { speaker: 'TAMSIN', text: 'Best view is mid-trestle. Stop to look and you\'ll get a wheel in the back.' },
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
