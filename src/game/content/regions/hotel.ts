/**
 * THE WAYWARD ARMS (2026-10) — the old country hotel on Wayward Rise, north of the
 * Wanderwood (`wayward_rise` + the `wayward_arms` interior; builders
 * tools/maps/build_wayward_rise.py / build_wayward_arms.py).
 *
 * A quiet reward beyond S5: the wood only opens on the waystone's word, and the
 * hotel waits past the glade. Inside there's an open bar, a corner chair, and a
 * well-dressed man standing beside it. The game never says who he is — a friend,
 * someone from the road, a long-lost brother? The mystery is the point; keep it.
 *
 * The scene is a REST: it ends in a `heal` (which sleeps, heals and banks the
 * Arms as a rest point), so the door wears the rest-lantern
 * (WorldScene.HEAL_ENTRANCE_MAPS). First visit plays the whole night; later
 * visits (`flag:wayward_night`) a short one. Never progression: nothing here
 * gates anything.
 *
 * Staging (tiles in wayward_arms): the stranger stands at (17,3) beside his green
 * armchair (seat 17,2); the corner chair's seat is (18,2). The bar walk is
 * single-axis `move` legs round the bar's open east end to (9,4), right under
 * the top shelf: (18,3) -> (18,8) -> (12,8) -> (12,4) -> (9,4), and back.
 * Alcohol stays understated: one bottle, two short glasses, no brands, no
 * drunkenness — a long talk by a fire.
 */
import type { CutsceneStep, DialogueRegistry, ScriptRegistry } from '../types';

const NIGHT = 'flag:wayward_night';
const STRANGER = 'STRANGER';
const PACE = 1.6;

/** Into the two armchairs: you in the corner, him in the green one beside it. */
const SIT_DOWN: CutsceneStep[] = [
  { op: 'move', actor: 'player', to: { tx: 18, ty: 3 }, speed: PACE },
  { op: 'move', actor: 'player', to: { tx: 18, ty: 2 }, speed: PACE },
  { op: 'face', actor: 'player', facing: 'down' },
  { op: 'move', actor: 'stranger', to: { tx: 17, ty: 2 } },
  { op: 'face', actor: 'stranger', facing: 'down' },
  { op: 'action', actor: 'player', action: 'sit', holdMs: 1400 },
];

export const HOTEL_SCRIPTS: ScriptRegistry = {
  // The stranger AND the corner chair both run this. Exactly one branch plays:
  // the return visit is checked FIRST, so the first night (which sets the flag
  // at its end) never falls through into it.
  'script.wayward_stranger': [
    { op: 'run', ref: 'script.wayward_again', if_flag: NIGHT },
    { op: 'run', ref: 'script.wayward_first', unless_flag: NIGHT },
  ],

  'script.wayward_first': [
    { op: 'narrate', text: 'A man stands beside the corner chair, one hand resting on its wing, as if he\'s been waiting a while. He looks up when you come in.' },
    { op: 'emote', actor: 'player', emote: 'question' },
    { op: 'narrate', text: 'Who\'s that? A friend? Someone you knew on the road, once?' },
    { op: 'narrate', text: '...A long-lost brother?' },
    { op: 'narrate', text: 'He doesn\'t say. He only nods at the empty chair in the corner.' },
    {
      op: 'choice',
      prompt: 'Sit down with him?',
      options: [
        {
          label: 'SIT DOWN',
          ops: [
            { op: 'say', speaker: STRANGER, text: 'Bar\'s open, by the way. Nobody\'s behind it tonight.' },
            { op: 'say', speaker: STRANGER, text: 'We\'ve been told we can help ourselves.' },
            // round the bar's open east end, to the spot under the top shelf
            { op: 'move', actor: 'player', to: { tx: 18, ty: 3 }, speed: PACE },
            { op: 'move', actor: 'player', to: { tx: 18, ty: 8 }, speed: PACE },
            { op: 'move', actor: 'player', to: { tx: 12, ty: 8 }, speed: PACE },
            { op: 'move', actor: 'player', to: { tx: 12, ty: 4 }, speed: PACE },
            { op: 'move', actor: 'player', to: { tx: 9, ty: 4 }, speed: PACE },
            { op: 'face', actor: 'player', facing: 'up' },
            { op: 'narrate', text: 'The top shelf keeps the good bottles, dusty-shouldered and older than the dark.' },
            { op: 'action', actor: 'player', action: 'raiseLamp', holdMs: 700 },
            { op: 'narrate', text: 'You reach up and take down the bourbon, and two short glasses.' },
            { op: 'move', actor: 'player', to: { tx: 12, ty: 4 }, speed: PACE },
            { op: 'move', actor: 'player', to: { tx: 12, ty: 8 }, speed: PACE },
            { op: 'move', actor: 'player', to: { tx: 18, ty: 8 }, speed: PACE },
            ...SIT_DOWN,
            { op: 'narrate', text: 'You sit down with him. Two fingers each, and the fire does the rest.' },
            { op: 'say', speaker: STRANGER, text: 'So. Where\'ve you come from?' },
            { op: 'narrate', text: 'You tell him. The coast road. The lamps. The long way round.' },
            { op: 'emote', actor: 'stranger', emote: 'ellipsis' },
            { op: 'say', speaker: STRANGER, text: '...' },
            { op: 'narrate', text: 'He tells you something back. It\'s a good story. It might even be true.' },
            { op: 'tint', color: '#0b1026', alpha: 0.38, ms: 1400 },
            { op: 'say', speaker: STRANGER, text: '...and THAT\'s why you never trust a lighthouse that hums...' },
            { op: 'emote', actor: 'player', emote: 'music' },
            { op: 'narrate', text: '...' },
            { op: 'narrate', text: 'The fire burns low. Neither of you gets up to mend it.' },
            { op: 'narrate', text: 'Somewhere past midnight the stories run out, and the talk keeps going anyway.' },
            // a REST: sleeps, heals, banks the Arms as a rest point
            { op: 'heal' },
            { op: 'setFlag', flag: NIGHT },
            { op: 'tint', color: '#ffd890', alpha: 0.18, ms: 700 },
            { op: 'narrate', text: 'You wake in the corner chair with a blanket over your knees. The glasses are washed. The fire\'s been banked.' },
            { op: 'tint', color: '#ffd890', alpha: 0, ms: 900 },
            { op: 'narrate', text: 'You feel rested. Your kin are rested too.' },
            { op: 'face', actor: 'player', facing: 'left' },
            { op: 'narrate', text: 'The man in the other chair is still there, or there again. He raises an empty glass to you.' },
            { op: 'narrate', text: 'Sometimes it\'s good to experience the fine and unexpected qualities of life.' },
          ],
        },
        {
          label: 'NOT TONIGHT',
          ops: [{ op: 'say', speaker: STRANGER, text: 'Another night, then. The chair will keep.' }],
        },
      ],
    },
  ],

  // Every visit after the first: the short version (still a rest point).
  'script.wayward_again': [
    { op: 'narrate', text: 'The man by the corner chair nods, as if you\'d only stepped out for a minute.' },
    {
      op: 'choice',
      prompt: 'Sit a while?',
      options: [
        {
          label: 'SIT A WHILE',
          ops: [
            { op: 'say', speaker: STRANGER, text: 'You know where it is.' },
            { op: 'narrate', text: 'Top shelf. You fetch it down, and two glasses.' },
            ...SIT_DOWN,
            { op: 'emote', actor: 'stranger', emote: 'ellipsis' },
            { op: 'narrate', text: '...' },
            { op: 'heal' },
            { op: 'narrate', text: 'You wake rested. The fire\'s banked; the glasses are washed.' },
            { op: 'narrate', text: 'Fine and unexpected, every time.' },
          ],
        },
        {
          label: 'NOT TONIGHT',
          ops: [{ op: 'say', speaker: STRANGER, text: 'The chair will keep.' }],
        },
      ],
    },
  ],
};

export const HOTEL_DIALOGUE: DialogueRegistry = {
  'sign.wayward_rise': [
    { text: 'THE WAYWARD ARMS. Rooms. Fires. An open door. All Wayfarers welcome, however far you\'ve wandered.' },
  ],
  'sign.wayward_bar': [
    { text: 'A card propped against the tumblers, in a neat hand: OPEN BAR TONIGHT. PLEASE HELP YOURSELVES.' },
  ],
  'sign.wayward_top_shelf': [
    { text: 'The top shelf. Squat amber bottles with brass caps, and one standing a little proud of the rest.' },
  ],
  'sign.wayward_stairs': [
    { text: 'The stair climbs to the rooms. Every door up there is shut and quiet, and someone has left a lamp burning on the landing.' },
  ],
  'sign.wayward_guestbook': [
    { text: 'The guest-book lies open: pages of names in a hundred different hands.' },
    { text: 'The last line just says: STAYED THE NIGHT. WORTH IT.' },
  ],
};
