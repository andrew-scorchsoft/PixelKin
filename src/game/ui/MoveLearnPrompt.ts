/**
 * MoveLearnPrompt — the genre's classic "wants to learn a fifth move" choice,
 * shared by level-ups (BattleScene consumes `gainExp().pending`) and Star-chart
 * study (ItemsMenu). Built from the kit (DialogueBox + Menu), promise-based:
 *
 *   const learned = await new MoveLearnPrompt(scene, kin, move, sfx).run();
 *
 * Free slot → learns immediately. Four moves known → the player picks one to
 * set aside (shown with type/power so the choice is informed) or gives up on
 * the new move. Resolves true if the move was learned. The caller persists.
 */
import Phaser from 'phaser';
import { Menu, type MenuOption } from './Menu';
import { DialogueBox } from './DialogueBox';
import type { KinInstance } from '@game/systems/party/KinInstance';
import type { Move } from '@game/data/dex';
import type { Sfx } from '@game/systems/audio/Sfx';

/** One compact label a player can weigh a move by: name, type, power band. */
function moveLabel(move: Move): string {
  const power = move.power > 0 ? `${move.power}` : '—';
  return `${move.name}  ${move.type.toUpperCase()} ${power}`;
}

export class MoveLearnPrompt {
  constructor(
    private readonly scene: Phaser.Scene,
    private readonly kin: KinInstance,
    private readonly move: Move,
    private readonly sfx?: Sfx,
  ) {}

  /** Run the flow; resolves true if the kin knows the move afterwards. */
  async run(): Promise<boolean> {
    const { kin, move } = this;
    if (kin.knowsMove(move.id)) return true;

    // Room in the kit — learn outright.
    if (kin.learnMove(move)) {
      void this.sfx?.playVariant('progress-learn', ['a', 'b']);
      await this.say(`${kin.displayName} learned ${move.name}!`);
      return true;
    }

    // Four moves known — the player chooses what to set aside.
    await this.say(
      `${kin.displayName} wants to learn ${move.name}, but already knows four moves. Set one aside?`,
    );
    const opts: MenuOption[] = kin.moves.map((k, i) => ({
      label: moveLabel(k.move),
      value: String(i),
    }));
    opts.push({ label: `GIVE UP ON ${move.name.toUpperCase()}`, value: 'giveup' });
    const choice = await new Menu(this.scene, opts, { x: 8, y: 8, sfx: this.sfx, cancellable: true }).run();

    if (choice === null || choice === 'giveup') {
      await this.say(`${kin.displayName} held on to what it knows. ${move.name} was set aside.`);
      return false;
    }

    const old = kin.moves[Number(choice)].move;
    kin.replaceMove(Number(choice), move);
    void this.sfx?.playVariant('progress-learn', ['a', 'b']);
    await this.say(`${kin.displayName} set aside ${old.name}... and learned ${move.name}!`);
    return true;
  }

  private say(text: string): Promise<void> {
    return new DialogueBox(this.scene, this.sfx).run([{ text }]).then(() => undefined);
  }
}

export { moveLabel };
