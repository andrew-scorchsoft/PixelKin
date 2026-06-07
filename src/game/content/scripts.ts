/**
 * Cutscene script registry — keyed by the `ref` cutscene/script triggers use
 * (EventTrigger.ref, e.g. 'script.intro_mentor'). Each is an ordered list of
 * CutsceneStep the CutsceneRunner interprets. Adding a scene is a data edit here.
 */
import type { ScriptRegistry } from './types';

export const SCRIPTS: ScriptRegistry = {
  // The opening beat: the mentor crosses to you, gives the vesperlamp, and lets you
  // choose a companion from the founding trio. Sets the flags later content checks.
  // C1 (walkthrough/01-south §2): Star-tender Fenn — warm, unhurried, never a "Professor".
  // Fenn waits on the lit spine at (13,12); the player triggers this from (13,11), one tile
  // north. Fenn turns up to the apprentice and gifts the vesperlamp + a starter.
  'script.intro_mentor': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'mentor', facing: 'up' },
    { op: 'say', speaker: 'FENN', text: 'There you are. The sky lost another light in the small hours — I felt it go.' },
    { op: 'say', speaker: 'FENN', text: 'So. It is time for your Wayfaring, at last. Every Wayfarer leaves Tinderwick with two things.' },
    { op: 'say', speaker: 'FENN', text: 'The first — a lamp, to carry the light home. Take it. Your vesperlamp.' },
    { op: 'sfx', key: 'world-lantern-light' },
    { op: 'giveItem', item: 'vesperlamp', count: 1 },
    { op: 'say', speaker: 'FENN', text: 'And the second — a friend, to share the walk through the dark. Go on. Choose.' },
    { op: 'giveStarter' },
    { op: 'say', speaker: 'FENN', text: 'Mind you tend them both, and they will tend you. Off into the dusk with you.' },
    { op: 'say', speaker: 'FENN', text: 'Brisa keeps the Lumenary up the square. Catch a kin first — then go earn her Ember Gleam.' },
    { op: 'setFlag', flag: 'flag:has_vesperlamp' },
    { op: 'setFlag', flag: 'flag:has_starter' },
  ],

  // First Lumenary (now a proper enterable chamber — tinderwick_lumenary): the player steps
  // up the aisle to Brisa Tallow's altar, hears her out, battles her, and on victory relights
  // the Ember constellation — the first Gleam, wrapped in the Lantern-fair's warmth (Arc E).
  // The trainer reward_flags ('gleam:ember', 'crown_south') are applied by the BattleScene on
  // a win; here we add the diegetic Gleam cue and the closing beat.
  'script.lumenary_tinderwick': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'brisa', facing: 'down' },
    { op: 'say', speaker: 'BRISA TALLOW', text: 'The lamp-tender sent you up, did she. Come closer — let me see what spark you carry.' },
    { op: 'say', speaker: 'BRISA TALLOW', text: 'A small flame is no lesser thing, dear. Show me you have kept yours steady.' },
    { op: 'battle', trainer: 'lampwarden_tinderwick' },
    { op: 'gleam', element: 'ember' },
    { op: 'say', speaker: 'BRISA TALLOW', text: 'There — the Ember Gleam burns again in the southern sky. Let it stand up there a while. Carry it well, Wayfarer.' },
  ],

  // Second Lumenary (pearlmoor_lumenary): the player crosses the sea-shrine chamber to
  // old ferryman Reyl Wash, hears him out, battles him, and on victory relights the Tide
  // constellation — the second Gleam, wrapped in the Tide-blessing festival (Arc E). The
  // trainer's reward_flags ('gleam:tide', 'crown_south') AND reward_abilities ('tidecall')
  // are applied by the BattleScene on a win; here we add the diegetic Gleam cue and the
  // closing beat handing over the Lantern Gift.
  'script.lumenary_pearlmoor': [
    { op: 'face', actor: 'player', facing: 'up' },
    { op: 'face', actor: 'reyl', facing: 'down' },
    { op: 'say', speaker: 'REYL WASH', text: 'Came on foot, did you — no need of the tides to reach my door. Good. The light should be free to all who seek it.' },
    { op: 'say', speaker: 'REYL WASH', text: 'Now. Read the water with me, Wayfarer, and we shall see if the sea will listen to you.' },
    { op: 'battle', trainer: 'lampwarden_pearlmoor' },
    { op: 'gleam', element: 'tide' },
    { op: 'say', speaker: 'REYL WASH', text: 'The Tide Gleam stands up over Pearlmoor again. And the Tidecall is yours — go on, ask the shallows to part. The harbour keeps its secrets for those who can cross.' },
  ],
};

export function getScript(ref: string): import('./types').CutsceneStep[] | undefined {
  return SCRIPTS[ref];
}
