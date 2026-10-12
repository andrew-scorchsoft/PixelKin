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
 */
import type { DialogueRegistry, ScriptRegistry } from '../types';

const RIDING = 'flag:wickrun_riding';
const PAID = 'flag:wickrun_rent_paid';
const FREED = 'flag:tallow_lift_freed';
const RIBBON = 'flag:runner_ribbon';

/** Where the lift sets you down at each end (the cars' platforms). */
export const LIFT_TOP = { map: 'wickrun_crest', to: { tx: 23, ty: 15 }, facing: 'down' as const };
export const LIFT_FOOT = { map: 'wickrun_foot', to: { tx: 16, ty: 12 }, facing: 'down' as const };

export const WICKRUN_SCRIPTS: ScriptRegistry = {
  // ---- the crest ------------------------------------------------------------
  'script.wickrun_rental': [
    { op: 'say', speaker: 'PELL', unless_flag: RIDING, text: 'Runners! Two wheels, one brake, no regrets. The Wick-Run\'s the old wax road — top of the mountain to the sea, if your nerve holds.' },
    { op: 'say', speaker: 'PELL', if_flag: RIDING, text: 'You\'ve got one of mine already. Off you go — through the gate and down. Hand it in at the foot; the lift-keeper sends them home.' },
    {
      op: 'choice',
      unless_flag: RIDING,
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
};

export const WICKRUN_DIALOGUE: DialogueRegistry = {
  'npc.wickrun_gate_blocked': [
    { speaker: 'PELL', text: 'Oi! Nobody goes down the run on foot. It\'s steep enough to make you a legend or a lesson. Rent a runner first.' },
  ],
  'npc.wickrun_runner_kid': [
    { text: 'Rook did the whole run in under a minute and a half. A MINUTE AND A HALF. My kin got dizzy just watching.' },
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
    { speaker: 'DACE', text: 'Shelf\'s the only flat bit till the foot. Catch your breath while you can.' },
  ],
};
