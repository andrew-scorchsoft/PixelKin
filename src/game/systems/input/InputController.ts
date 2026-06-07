/**
 * Unified input — the seam that keeps the game source-agnostic.
 *
 * Both the keyboard and the on-screen VirtualDpad (touch) feed the same abstract
 * `InputAction` set, so nothing downstream (player movement, menus, battle) ever
 * asks "was this a key or a tap?". That single abstraction is what makes the
 * eventual Capacitor / mobile port cheap: swap the input source, not the game.
 */
import Phaser from 'phaser';

/** Every discrete thing the player can ask the game to do. */
export enum InputAction {
  Up = 'up',
  Down = 'down',
  Left = 'left',
  Right = 'right',
  Confirm = 'confirm', // A — talk / select / advance text
  Cancel = 'cancel', // B — back / run
  Menu = 'menu', // Start — open the pause/party menu
}

export const DIRECTION_ACTIONS = [
  InputAction.Up,
  InputAction.Down,
  InputAction.Left,
  InputAction.Right,
] as const;

/**
 * A digital input source. Keyboard implements this directly; VirtualDpad pushes
 * presses in through `injectPress`/`injectRelease` on a shared controller.
 */
export class InputController {
  private readonly down = new Set<InputAction>();
  private readonly pressedThisFrame = new Set<InputAction>();
  private readonly injected = new Set<InputAction>();
  private keys: Record<string, Phaser.Input.Keyboard.Key> = {};

  constructor(private readonly scene: Phaser.Scene) {
    const kb = scene.input.keyboard;
    if (kb) {
      this.keys = kb.addKeys(
        {
          up: Phaser.Input.Keyboard.KeyCodes.UP,
          up2: Phaser.Input.Keyboard.KeyCodes.W,
          down: Phaser.Input.Keyboard.KeyCodes.DOWN,
          down2: Phaser.Input.Keyboard.KeyCodes.S,
          left: Phaser.Input.Keyboard.KeyCodes.LEFT,
          left2: Phaser.Input.Keyboard.KeyCodes.A,
          right: Phaser.Input.Keyboard.KeyCodes.RIGHT,
          right2: Phaser.Input.Keyboard.KeyCodes.D,
          confirm: Phaser.Input.Keyboard.KeyCodes.ENTER,
          confirm2: Phaser.Input.Keyboard.KeyCodes.SPACE,
          confirm3: Phaser.Input.Keyboard.KeyCodes.Z,
          cancel: Phaser.Input.Keyboard.KeyCodes.X,
          cancel2: Phaser.Input.Keyboard.KeyCodes.BACKSPACE,
          menu: Phaser.Input.Keyboard.KeyCodes.ENTER, // also Start; Esc below
          menu2: Phaser.Input.Keyboard.KeyCodes.ESC,
        } as const,
      ) as unknown as Record<string, Phaser.Input.Keyboard.Key>;
    }
  }

  /** Call once per scene update, before reading actions. */
  update(): void {
    this.pressedThisFrame.clear();
    const prevDown = new Set(this.down);
    this.down.clear();

    const map: Array<[InputAction, string[]]> = [
      [InputAction.Up, ['up', 'up2']],
      [InputAction.Down, ['down', 'down2']],
      [InputAction.Left, ['left', 'left2']],
      [InputAction.Right, ['right', 'right2']],
      [InputAction.Confirm, ['confirm', 'confirm2', 'confirm3']],
      [InputAction.Cancel, ['cancel', 'cancel2']],
      [InputAction.Menu, ['menu2']],
    ];
    for (const [action, keyNames] of map) {
      if (keyNames.some((n) => this.keys[n]?.isDown)) this.down.add(action);
    }
    for (const a of this.injected) this.down.add(a);

    for (const a of this.down) {
      if (!prevDown.has(a)) this.pressedThisFrame.add(a);
    }
  }

  /** True while the action is held. */
  isDown(action: InputAction): boolean {
    return this.down.has(action);
  }

  /** True only on the frame the action transitions from up to down. */
  justPressed(action: InputAction): boolean {
    return this.pressedThisFrame.has(action);
  }

  /** The first held direction, in a stable priority order, or null. */
  heldDirection(): InputAction | null {
    for (const d of DIRECTION_ACTIONS) if (this.down.has(d)) return d;
    return null;
  }

  /** Touch/VirtualDpad hook: mark an action held until released. */
  injectPress(action: InputAction): void {
    this.injected.add(action);
  }

  injectRelease(action: InputAction): void {
    this.injected.delete(action);
  }

  /** Touch hook for momentary buttons (confirm/cancel/menu): one-frame press. */
  injectTap(action: InputAction): void {
    this.injected.add(action);
    this.scene.time.delayedCall(0, () => this.injected.delete(action));
  }
}
