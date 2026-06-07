/**
 * ShellManager — the DOM chrome that lives OUTSIDE the Phaser canvas.
 *
 * Phaser renders the game at a fixed 240x160 and Scale.FIT upscales it inside
 * `#game-root`. The "shell" is everything around that: nothing here ever changes
 * the internal resolution — it only styles the DOM and overlays touch controls.
 *
 * Three modes (persisted via SaveManager settings):
 *   - 'device'  : an original handheld-style casing with a control cluster.
 *   - 'overlay' : full-bleed canvas with translucent on-screen controls.
 *   - 'plain'   : just the scaled canvas, no chrome.
 *
 * The on-screen controls don't know about Phaser. They emit abstract actions
 * ('up' | 'down' | 'left' | 'right' | 'confirm' | 'cancel' | 'menu') with an
 * isDown flag, both via `onAction(cb)` and as a `window` CustomEvent named
 * `pixelkin-input` (detail: { action, isDown }). The orchestrator subscribes and
 * feeds them into InputController (injectPress/injectRelease/injectTap).
 *
 * shells.css is imported here so Vite bundles it without touching global.css.
 */
import './shells.css';
import { SaveManager } from '@game/systems/save/SaveManager';
import type { ShellMode, Settings } from '@game/systems/save/SaveManager';

/** The abstract directional/button actions the on-screen controls emit. */
export type ShellAction = 'up' | 'down' | 'left' | 'right' | 'confirm' | 'cancel' | 'menu';

/** Payload of the `pixelkin-input` CustomEvent and the onAction callback. */
export interface ShellInputDetail {
  action: ShellAction;
  isDown: boolean;
}

/** The window CustomEvent name carrying shell control presses. */
export const SHELL_INPUT_EVENT = 'pixelkin-input';

type ActionListener = (action: ShellAction, isDown: boolean) => void;

/**
 * Keyboard equivalents per on-screen control, shown as a native hover tooltip so a
 * desktop player learns the shortcut for A/B (and the rest) without leaving the game.
 * Keep these in sync with the bindings in InputController.
 */
const KEY_HINTS: Record<ShellAction, string> = {
  up: 'Up  (↑ / W)',
  down: 'Down  (↓ / S)',
  left: 'Left  (← / A)',
  right: 'Right  (→ / D)',
  confirm: 'Confirm  (Z / Enter / Space)',
  cancel: 'Back  (X / Backspace)',
  menu: 'Menu  (Esc)',
};

const SHELL_CLASSES: Record<ShellMode, string> = {
  device: 'pk-shell-device',
  overlay: 'pk-shell-overlay',
  plain: 'pk-shell-plain',
};

class ShellManagerImpl {
  private settings: Settings = { shell: 'device', controlsVisible: true };
  private frameEl: HTMLDivElement | null = null;
  private controlsEl: HTMLDivElement | null = null;
  private readonly listeners = new Set<ActionListener>();
  private readonly held = new Set<ShellAction>();

  /** Read persisted settings and apply the saved shell. Call once from main.ts. */
  async init(): Promise<void> {
    this.settings = await SaveManager.loadSettings();
    this.render();
  }

  /** Current shell mode. */
  get shell(): ShellMode {
    return this.settings.shell;
  }

  /** Whether on-screen controls are currently shown. */
  get controlsVisible(): boolean {
    return this.settings.controlsVisible;
  }

  /** Switch shell live and persist. */
  async setShell(mode: ShellMode): Promise<void> {
    if (this.settings.shell === mode) return;
    this.settings = { ...this.settings, shell: mode };
    this.render();
    await SaveManager.saveSettings(this.settings);
  }

  /** Show/hide the on-screen controls live and persist. */
  async setControlsVisible(visible: boolean): Promise<void> {
    if (this.settings.controlsVisible === visible) return;
    this.settings = { ...this.settings, controlsVisible: visible };
    this.applyControlsVisibility();
    await SaveManager.saveSettings(this.settings);
  }

  /** Subscribe to control actions. Returns an unsubscribe function. */
  onAction(cb: ActionListener): () => void {
    this.listeners.add(cb);
    return () => this.listeners.delete(cb);
  }

  // --------------------------------------------------------------- rendering --

  private render(): void {
    const body = document.body;
    for (const cls of Object.values(SHELL_CLASSES)) body.classList.remove(cls);
    body.classList.add(SHELL_CLASSES[this.settings.shell]);

    this.ensureFrame();
    this.ensureControls();
    this.applyControlsVisibility();
  }

  /** The decorative casing backdrop — only meaningful for the device shell. */
  private ensureFrame(): void {
    if (this.settings.shell === 'device') {
      if (!this.frameEl) {
        const frame = document.createElement('div');
        frame.className = 'pk-shell-frame';
        const grille = document.createElement('div');
        grille.className = 'pk-grille';
        for (let i = 0; i < 12; i++) grille.appendChild(document.createElement('i'));
        frame.appendChild(grille);
        document.body.insertBefore(frame, document.body.firstChild);
        this.frameEl = frame;
      }
    } else if (this.frameEl) {
      this.frameEl.remove();
      this.frameEl = null;
    }
  }

  /** The d-pad / face-button / start cluster — shown for device + overlay. */
  private ensureControls(): void {
    const wantsControls = this.settings.shell !== 'plain';
    if (wantsControls) {
      if (!this.controlsEl) this.controlsEl = this.buildControls();
    } else if (this.controlsEl) {
      this.controlsEl.remove();
      this.controlsEl = null;
    }
  }

  private applyControlsVisibility(): void {
    if (!this.controlsEl) return;
    const hidden = !this.settings.controlsVisible || this.settings.shell === 'plain';
    this.controlsEl.classList.toggle('pk-hidden', hidden);
  }

  private buildControls(): HTMLDivElement {
    const root = document.createElement('div');
    root.className = 'pk-controls';

    // D-pad
    const dpad = document.createElement('div');
    dpad.className = 'pk-dpad';
    dpad.appendChild(this.button('pk-control pk-up', 'up'));
    dpad.appendChild(this.button('pk-control pk-down', 'down'));
    dpad.appendChild(this.button('pk-control pk-left', 'left'));
    dpad.appendChild(this.button('pk-control pk-right', 'right'));
    const center = document.createElement('div');
    center.className = 'pk-control pk-center';
    dpad.appendChild(center);
    root.appendChild(dpad);

    // Face buttons
    const face = document.createElement('div');
    face.className = 'pk-face';
    face.appendChild(this.button('pk-control pk-a', 'confirm', 'A'));
    face.appendChild(this.button('pk-control pk-b', 'cancel', 'B'));
    root.appendChild(face);

    // Start
    root.appendChild(this.button('pk-start', 'menu', 'START'));

    document.body.appendChild(root);
    return root;
  }

  /** Make a control element wired to press/release of an action. */
  private button(className: string, action: ShellAction, label?: string): HTMLDivElement {
    const el = document.createElement('div');
    el.className = className;
    if (label !== undefined) el.textContent = label;
    // Hovering a control reveals its keyboard shortcut (e.g. A → "Confirm (Z/Enter/Space)").
    el.title = KEY_HINTS[action];
    el.setAttribute('aria-label', KEY_HINTS[action]);

    const down = (ev: Event): void => {
      ev.preventDefault();
      el.classList.add('pk-active');
      this.press(action, true);
    };
    const up = (ev: Event): void => {
      ev.preventDefault();
      el.classList.remove('pk-active');
      this.press(action, false);
    };

    // Pointer events cover mouse + touch + pen uniformly.
    el.addEventListener('pointerdown', down);
    el.addEventListener('pointerup', up);
    el.addEventListener('pointercancel', up);
    el.addEventListener('pointerleave', up);
    el.addEventListener('contextmenu', (e) => e.preventDefault());
    return el;
  }

  private press(action: ShellAction, isDown: boolean): void {
    // De-dupe spurious repeats (pointerleave after pointerup, etc.).
    if (isDown) {
      if (this.held.has(action)) return;
      this.held.add(action);
    } else {
      if (!this.held.has(action)) return;
      this.held.delete(action);
    }
    this.emit(action, isDown);
  }

  private emit(action: ShellAction, isDown: boolean): void {
    for (const cb of this.listeners) cb(action, isDown);
    const detail: ShellInputDetail = { action, isDown };
    window.dispatchEvent(new CustomEvent<ShellInputDetail>(SHELL_INPUT_EVENT, { detail }));
  }
}

/** Singleton — one chrome layer per page. */
export const ShellManager = new ShellManagerImpl();
