/**
 * Party — the player's (or a trainer's) ordered team of up to six kin.
 *
 * The first entry is the battle lead. The party tracks who's active, finds the
 * first non-fainted member for auto-switching after a faint, and reports when
 * the whole team is down (the lose condition). It (de)serialises through the
 * same `KinInstanceData[]` the save uses, so it drops straight into a SaveGame.
 */
import { KinInstance } from './KinInstance';
import type { KinInstanceData } from '@game/systems/save/types';

export const MAX_PARTY = 6;

export class Party {
  private members: KinInstance[];
  /** Index of the kin currently sent out. */
  private activeIndex = 0;

  constructor(members: KinInstance[] = []) {
    this.members = members.slice(0, MAX_PARTY);
  }

  static fromData(data: KinInstanceData[]): Party {
    return new Party(data.map((d) => KinInstance.fromData(d)));
  }

  toData(): KinInstanceData[] {
    return this.members.map((m) => m.toData());
  }

  get all(): readonly KinInstance[] {
    return this.members;
  }

  get size(): number {
    return this.members.length;
  }

  get isFull(): boolean {
    return this.members.length >= MAX_PARTY;
  }

  get active(): KinInstance {
    return this.members[this.activeIndex];
  }

  get activeSlot(): number {
    return this.activeIndex;
  }

  at(index: number): KinInstance | undefined {
    return this.members[index];
  }

  /** Add a kin to the back of the party. Returns false if the party is full. */
  add(kin: KinInstance): boolean {
    if (this.isFull) return false;
    this.members.push(kin);
    return true;
  }

  /** True once every member has fainted (the battle-lose condition). */
  get allFainted(): boolean {
    return this.members.length > 0 && this.members.every((m) => m.isFainted);
  }

  /** First member that can still fight, or undefined if none. */
  firstHealthy(): KinInstance | undefined {
    return this.members.find((m) => !m.isFainted);
  }

  /** Index of the first non-fainted member, or -1. */
  firstHealthyIndex(): number {
    return this.members.findIndex((m) => !m.isFainted);
  }

  /**
   * Make the member at `index` the active kin. Refuses to switch to a fainted
   * kin, the current active kin, or an out-of-range slot. Resets the incoming
   * kin's per-battle volatile state.
   */
  switchTo(index: number): boolean {
    const target = this.members[index];
    if (!target || target.isFainted || index === this.activeIndex) return false;
    this.active.resetBattleState();
    this.activeIndex = index;
    target.resetBattleState();
    return true;
  }

  /** After a faint, auto-advance the active slot to the first healthy member. */
  promoteToHealthy(): boolean {
    const i = this.firstHealthyIndex();
    if (i < 0) return false;
    this.activeIndex = i;
    this.members[i].resetBattleState();
    return true;
  }

  /** Restore every member to full hp / charges / clear status (e.g. at a hearth). */
  healAll(): void {
    for (const m of this.members) m.fullHeal();
  }
}
