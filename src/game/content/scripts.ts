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
    { op: 'move', actor: 'mentor', to: { tx: 6, ty: 4 } },
    { op: 'face', actor: 'mentor', facing: 'down' },
    { op: 'say', speaker: 'MENTOR', text: 'Steady, now. Another light went out of the sky last night.' },
    { op: 'say', speaker: 'MENTOR', text: 'It is time for your Wayfaring. Take this — your vesperlamp.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'giveItem', item: 'vesperlamp', count: 1 },
    { op: 'say', speaker: 'MENTOR', text: 'And a companion to walk the dark with you. Choose.' },
    { op: 'giveStarter' },
    { op: 'say', speaker: 'MENTOR', text: 'Good. Tend the light, and it will tend you. Off you go.' },
    { op: 'setFlag', flag: 'flag:has_vesperlamp' },
    { op: 'setFlag', flag: 'flag:has_starter' },
  ],
};

export function getScript(ref: string): import('./types').CutsceneStep[] | undefined {
  return SCRIPTS[ref];
}
