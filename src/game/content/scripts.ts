/**
 * Cutscene script registry — keyed by the `ref` cutscene/script triggers use
 * (EventTrigger.ref, e.g. 'script.intro_mentor'). Each is an ordered list of
 * CutsceneStep the CutsceneRunner interprets. Adding a scene is a data edit here.
 */
import type { ScriptRegistry } from './types';

export const SCRIPTS: ScriptRegistry = {
  // The opening beat: the mentor crosses to you, gives the vesperlamp, and lets you
  // choose a companion from the founding trio. Sets the flags later content checks.
  'script.intro_mentor': [
    { op: 'face', actor: 'player', facing: 'up' },
    // The mentor waits on the lit spine at (12,11); the player triggers this from (12,10),
    // one tile north. Step down to stand face-to-face, then turn to the apprentice.
    { op: 'move', actor: 'mentor', to: { tx: 12, ty: 11 } },
    { op: 'face', actor: 'mentor', facing: 'up' },
    { op: 'say', speaker: 'MENTOR', text: 'Steady, now. Another light went out of the sky last night.' },
    { op: 'say', speaker: 'MENTOR', text: 'It is time for your Wayfaring. Take this — your vesperlamp.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'giveItem', item: 'vesperlamp', count: 1 },
    { op: 'say', speaker: 'MENTOR', text: 'And a companion to walk the dark with you. Choose.' },
    { op: 'giveStarter' },
    { op: 'say', speaker: 'MENTOR', text: 'Good. Tend the light, and it will tend you. Off you go.' },
    { op: 'say', speaker: 'MENTOR', text: 'Brisa keeps the Lumenary up the square. Earn her Gleam when your kin is ready.' },
    { op: 'setFlag', flag: 'flag:has_vesperlamp' },
    { op: 'setFlag', flag: 'flag:has_starter' },
  ],

  // First Lumenary: walk into Brisa Tallow's hall, hear her out, battle her, and on
  // victory relight the Ember constellation — the first Gleam. The trainer reward_flags
  // ('gleam:ember', 'crown_south') are applied by the BattleScene on a win; here we add
  // the diegetic Gleam cue and the closing beat.
  'script.lumenary_tinderwick': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'say', speaker: 'BRISA TALLOW', text: 'The lamp-tender sent you, then. Step into the Lumenary — let us see your spark.' },
    { op: 'battle', trainer: 'lampwarden_tinderwick' },
    { op: 'gleam', element: 'ember' },
    { op: 'say', speaker: 'BRISA TALLOW', text: 'There — the Ember Gleam burns again in the southern sky. Carry it well, Wayfarer.' },
  ],
};

export function getScript(ref: string): import('./types').CutsceneStep[] | undefined {
  return SCRIPTS[ref];
}
