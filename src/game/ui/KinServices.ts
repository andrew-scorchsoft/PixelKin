/**
 * KinServices — the "do something to one of your kin" counter services, shared by
 * every NPC who offers them through the `kinService` cutscene op:
 *
 *   rename   — give a kin a new name (the Namewright's house; a name set at the
 *              catch is otherwise kept for good).
 *   relearn  — bring back a move the kin's line has known or could have known by
 *              now (its level-up moves up to its level, plus its kindling moves),
 *              for a fee in wicks, charged only if a move is actually learned.
 *   forget   — let a move go (a kin always keeps at least one).
 *   read     — how close a kin is to kindling, and how warm its bond runs.
 *
 * Also `offerNickname` — the "give it a name?" ask after a catch or a gift.
 * Promise-based, built from the kit (DialogueBox + Menu + NameEntry); the caller
 * owns the party data and persists.
 */
import Phaser from 'phaser';
import { Menu, type MenuOption } from './Menu';
import { DialogueBox } from './DialogueBox';
import { NameEntry } from './NameEntry';
import { MoveLearnPrompt } from './MoveLearnPrompt';
import { bondTier } from './PartyMenu';
import { MOVE_BY_ID, SPECIES_BY_ID, type Move } from '@game/data/dex';
import type { KinInstance } from '@game/systems/party/KinInstance';
import type { Sfx } from '@game/systems/audio/Sfx';

export type KinServiceKind = 'rename' | 'relearn' | 'forget' | 'read';

export interface KinServiceOptions {
  /** Wicks a relearned move costs (0 = free). */
  cost?: number;
  /** Who's speaking the service's lines (shown as the speaker). */
  speaker?: string;
  /** The wallet: read it, and take a fee (false if short). */
  money?: () => number;
  pay?: (amount: number) => boolean;
}

/** The moves a kin could remember: its line's level-up moves up to its level and
 *  its kindling moves, that it doesn't know now. Oldest first. */
export function rememberableMoves(kin: KinInstance): Move[] {
  const ids: string[] = [];
  for (const e of kin.species.learnset.levelup) if (e.level <= kin.level) ids.push(e.move);
  ids.push(...kin.species.learnset.kindling);
  const out: Move[] = [];
  for (const id of ids) {
    const m = MOVE_BY_ID.get(id);
    if (m && !kin.knowsMove(id) && !out.includes(m)) out.push(m);
  }
  return out;
}

export async function runKinService(
  scene: Phaser.Scene,
  kind: KinServiceKind,
  party: KinInstance[],
  sfx: Sfx | undefined,
  opts: KinServiceOptions = {},
): Promise<void> {
  const say = (text: string): Promise<void> =>
    new DialogueBox(scene, sfx).run([{ speaker: opts.speaker, text }]);
  if (party.length === 0) {
    await say('No kin walk with you just now.');
    return;
  }
  switch (kind) {
    case 'rename': {
      const kin = await pickKin(scene, party, sfx, () => true);
      if (!kin) return;
      await askName(scene, kin, sfx);
      await say(`${kin.displayName}. A good name. It suits them.`);
      return;
    }
    case 'relearn': {
      const kin = await pickKin(scene, party, sfx, (k) => rememberableMoves(k).length > 0);
      if (!kin) return;
      const moves = rememberableMoves(kin);
      const cost = Math.max(0, opts.cost ?? 0);
      const opt: MenuOption[] = moves.map((m) => ({
        label: m.name,
        value: m.id,
        right: m.type.slice(0, 3).toUpperCase(),
      }));
      const pick = await new Menu(scene, opt, { x: 8, y: 8, sfx, maxVisible: 9 }).run();
      if (!pick) return;
      const move = MOVE_BY_ID.get(pick);
      if (!move) return;
      if (cost > 0 && (opts.money?.() ?? 0) < cost) {
        await say(`That one wants ${cost} wicks of lamp-oil, and your purse is lighter than that.`);
        return;
      }
      const learned = await new MoveLearnPrompt(scene, kin, move, sfx).run();
      if (learned && cost > 0) opts.pay?.(cost);
      if (learned) await say(`There. ${kin.displayName} remembers ${move.name}.`);
      return;
    }
    case 'forget': {
      const kin = await pickKin(scene, party, sfx, (k) => k.moves.length > 1);
      if (!kin) return;
      const pick = await new Menu(
        scene,
        kin.moves.map((k, i) => ({ label: k.move.name, value: String(i) })),
        { x: 8, y: 8, sfx },
      ).run();
      if (pick === null) return;
      const name = kin.moves[Number(pick)]?.move.name;
      kin.forgetMove(Number(pick));
      await say(`${kin.displayName} lets ${name} go. It isn't lost, only resting; it can be remembered again.`);
      return;
    }
    case 'read': {
      const kin = await pickKin(scene, party, sfx, () => true);
      if (!kin) return;
      await new DialogueBox(scene, sfx).run(readKin(kin).map((text) => ({ speaker: opts.speaker, text })));
      return;
    }
  }
}

/** The reading: kindling forecast + bond warmth, in plain words. */
export function readKin(kin: KinInstance): string[] {
  const lines: string[] = [];
  const k = kin.species.kindling;
  const into = k ? SPECIES_BY_ID.get(k.into)?.name ?? 'something new' : null;
  if (!k) {
    lines.push(`${kin.displayName} has kindled as far as its light goes. Nothing left to become but more itself.`);
  } else if (k.trigger.kind === 'level' && k.trigger.level) {
    const gap = k.trigger.level - kin.level;
    lines.push(gap > 0
      ? `${kin.displayName} will kindle into ${into} at level ${k.trigger.level}. That's ${gap} level${gap === 1 ? '' : 's'} to go.`
      : `${kin.displayName} is ready to kindle into ${into}. The next time it grows a level, it will ask you.`);
  } else if (k.trigger.kind === 'bond') {
    const need = k.trigger.min ?? 160;
    lines.push(kin.bond >= need
      ? `${kin.displayName} trusts you enough to kindle into ${into}. It's only waiting for the moment.`
      : `${kin.displayName} will kindle into ${into} when it trusts you completely. Fight beside it; tend it when it's hurt.`);
  } else {
    lines.push(`${kin.displayName} will kindle into ${into}, but not by growing alone. Something in the world will light it.`);
  }
  const tier = bondTier(kin.bond).word;
  const warmth: Record<string, string> = {
    NEW: 'Your bond is new yet. Give it time.',
    WARM: 'Your bond runs warm. It likes having you near.',
    CLOSE: 'Your bond runs close. It would follow you anywhere.',
    KINDRED: 'Your bond is kindred. I don\'t see that often.',
  };
  lines.push(warmth[tier] ?? '');
  return lines.filter(Boolean);
}

/**
 * The "give it a name?" ask, for a new catch or a gift. YES opens the name box
 * (NameEntry never commits an EMPTY box: a lone space, or the species name itself,
 * keeps the species name). A name set here is kept; only the
 * Namewright changes it after.
 */
export async function offerNickname(scene: Phaser.Scene, kin: KinInstance, sfx?: Sfx): Promise<void> {
  await new DialogueBox(scene, sfx).run([{ text: `Give ${kin.species.name} a name of its own?` }]);
  const yes = await new Menu(scene, [
    { label: 'YES', value: 'yes' },
    { label: 'NO', value: 'no' },
  ], { x: 8, y: 8, sfx }).run();
  if (yes === 'yes') await askName(scene, kin, sfx);
}

async function askName(scene: Phaser.Scene, kin: KinInstance, sfx?: Sfx): Promise<void> {
  const name = (await new NameEntry(scene, {
    title: `NAME ${kin.species.name.toUpperCase()}`,
    initial: kin.nickname ?? '',
    fallback: kin.species.name,
    sfx,
  }).run()).trim();
  kin.nickname = !name || name.toLowerCase() === kin.species.name.toLowerCase() ? undefined : name;
}

/** Pick one party kin (rows not matching `ok` are greyed). */
async function pickKin(
  scene: Phaser.Scene,
  party: KinInstance[],
  sfx: Sfx | undefined,
  ok: (k: KinInstance) => boolean,
): Promise<KinInstance | null> {
  if (!party.some(ok)) {
    await new DialogueBox(scene, sfx).run([{ text: 'None of your kin needs that just now.' }]);
    return null;
  }
  const pick = await new Menu(scene, party.map((k, i) => ({
    label: k.displayName,
    value: String(i),
    enabled: ok(k),
    right: `Lv${k.level}`,
  })), { x: 8, y: 8, sfx }).run();
  return pick === null ? null : party[Number(pick)] ?? null;
}
