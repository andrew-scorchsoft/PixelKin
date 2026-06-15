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
import type { ShellMode, ControlSize, Settings } from '@game/systems/save/SaveManager';
import {
  setAlwaysRun,
  setTextSpeed,
  setBattlePace,
  setMusicVolume,
  setSfxVolume,
} from '@game/ui/preferences';

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

/**
 * Touch-control scale per size step. The whole cluster (d-pad cross, A·B, Start)
 * derives every dimension from this one factor (see `--pk-cs` in shells.css), so
 * the buttons grow as a single, internally-aligned unit — no per-element drift.
 * Size 1 is the original compact geometry (1.0); 2 (default) and 3 step up.
 */
const CONTROL_SIZE_SCALE: Record<ControlSize, number> = {
  1: 1,
  2: 1.22,
  3: 1.45,
};

class ShellManagerImpl {
  private settings: Settings = { shell: 'device', controlsVisible: true };
  private frameEl: HTMLDivElement | null = null;
  private controlsEl: HTMLDivElement | null = null;
  private rotateHintEl: HTMLDivElement | null = null;
  private fsToggleEl: HTMLDivElement | null = null;
  private restoreEl: HTMLDivElement | null = null;
  private autoFsTried = false;
  private readonly listeners = new Set<ActionListener>();
  private readonly held = new Set<ShellAction>();

  /** Read persisted settings and apply the saved shell. Call once from main.ts. */
  async init(): Promise<void> {
    this.settings = await SaveManager.loadSettings();
    // Push the gameplay preferences into their live, per-frame home.
    setAlwaysRun(this.settings.alwaysRun ?? false);
    setTextSpeed(this.settings.textSpeed ?? 'cosy');
    setBattlePace(this.settings.battlePace ?? 'cosy');
    setMusicVolume(this.settings.musicVolume ?? 'full');
    setSfxVolume(this.settings.sfxVolume ?? 'full');
    this.applyControlSize();
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

  /** Current on-screen control size (1 small … 3 large; default 2). */
  get controlSize(): ControlSize {
    return this.settings.controlSize ?? 2;
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
    this.updateRestoreVisibility();
    await SaveManager.saveSettings(this.settings);
  }

  /**
   * Bring the player back to a controllable state. Without on-screen controls a
   * touch player has no START button to open the pause menu, so they can't reach
   * Settings to undo a Plain-shell / Hidden-controls choice — a soft lock-out. The
   * rescue button (built once, shown only on touch when controls are unavailable)
   * calls this: it leaves Plain for a controllable shell and re-shows the cluster.
   */
  async restoreControls(): Promise<void> {
    if (this.settings.shell === 'plain') await this.setShell('overlay');
    if (!this.settings.controlsVisible) await this.setControlsVisible(true);
    this.updateRestoreVisibility();
  }

  /** Set the on-screen control size live (1–3) and persist. */
  async setControlSize(size: ControlSize): Promise<void> {
    if (this.controlSize === size) return;
    this.settings = { ...this.settings, controlSize: size };
    this.applyControlSize();
    await SaveManager.saveSettings(this.settings);
  }

  /** Push the chosen size into the `--pk-cs` scale the control CSS multiplies by. */
  private applyControlSize(): void {
    const scale = CONTROL_SIZE_SCALE[this.controlSize] ?? 1;
    document.documentElement.style.setProperty('--pk-cs', String(scale));
    const toggle = this.controlsEl?.querySelector<HTMLElement>('.pk-size-toggle');
    if (toggle) toggle.textContent = String(this.controlSize);
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
    this.ensureRotateHint();
    this.ensureFullscreenToggle();
    this.ensureRestoreButton();
    this.applyControlsVisibility();
    this.updateRestoreVisibility();
  }

  // ---------------------------------------------------- restore-controls rescue --

  /**
   * A small "Show controls" button pinned to the bottom centre. Built once; CSS
   * shows it ONLY on a touch device (`pointer: coarse`) while controls are
   * unavailable (Plain shell, or controls Hidden) — i.e. exactly the soft lock-out
   * where there's no other way back. Tapping it restores a controllable state.
   */
  private ensureRestoreButton(): void {
    if (this.restoreEl) return;
    const btn = document.createElement('div');
    btn.className = 'pk-restore-controls';
    btn.setAttribute('role', 'button');
    btn.setAttribute('aria-label', 'Show the on-screen controls');
    btn.title = 'Show the on-screen controls';
    btn.textContent = '⌗ Show controls'; // ⌗ glyph + label

    btn.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      btn.classList.add('pk-active');
    });
    btn.addEventListener('pointerup', (e) => {
      e.preventDefault();
      btn.classList.remove('pk-active');
      void this.restoreControls();
    });
    btn.addEventListener('pointercancel', () => btn.classList.remove('pk-active'));
    btn.addEventListener('pointerleave', () => btn.classList.remove('pk-active'));
    btn.addEventListener('contextmenu', (e) => e.preventDefault());

    document.body.appendChild(btn);
    this.restoreEl = btn;
  }

  /** Toggle the body flag the rescue-button CSS keys on (controls unavailable). */
  private updateRestoreVisibility(): void {
    const unavailable = this.settings.shell === 'plain' || !this.settings.controlsVisible;
    document.body.classList.toggle('pk-controls-unavailable', unavailable);
  }

  // ----------------------------------------------------------- fullscreen --

  /** True where the browser exposes the element Fullscreen API (Android Chrome/
   *  Firefox, desktop). iOS Safari returns false — there it's "Add to Home
   *  Screen" (the manifest) that hides the chrome instead. */
  private fullscreenSupported(): boolean {
    return typeof document.documentElement.requestFullscreen === 'function';
  }

  private isFullscreen(): boolean {
    return document.fullscreenElement != null;
  }

  /** Begin a fullscreen request. Must be called from within a user gesture; the
   *  `requestFullscreen()` call is issued synchronously so the gesture still
   *  counts even though we await its promise. Silently degrades if blocked. */
  private async enterFullscreen(): Promise<void> {
    if (!this.fullscreenSupported() || this.isFullscreen()) return;
    try {
      await document.documentElement.requestFullscreen();
    } catch {
      /* User declined or unsupported — leave the page as-is. */
    }
  }

  private async exitFullscreen(): Promise<void> {
    if (!this.isFullscreen()) return;
    try {
      await document.exitFullscreen();
    } catch {
      /* no-op */
    }
  }

  /**
   * A small fullscreen toggle pinned to a free corner. Built once, only when the
   * Fullscreen API exists (so iOS — where tapping would do nothing — never shows a
   * dead button). CSS limits it to touch devices on the device/overlay shells.
   */
  private ensureFullscreenToggle(): void {
    if (!this.fullscreenSupported()) return;
    if (this.fsToggleEl) return;
    const btn = document.createElement('div');
    btn.className = 'pk-fs-toggle';
    btn.setAttribute('role', 'button');
    btn.setAttribute('aria-label', 'Toggle fullscreen');
    btn.title = 'Toggle fullscreen';

    const sync = (): void => {
      const on = this.isFullscreen();
      btn.textContent = on ? '✕' : '⛶'; // ✕ to exit / ⛶ to enter
      btn.classList.toggle('pk-fs-on', on);
    };
    sync();

    btn.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      void (this.isFullscreen() ? this.exitFullscreen() : this.enterFullscreen());
    });
    document.addEventListener('fullscreenchange', sync);

    document.body.appendChild(btn);
    this.fsToggleEl = btn;
  }

  /**
   * Best-effort auto-fullscreen on the player's FIRST control press in landscape
   * (Android in-browser): the gesture lets us claim the screen as soon as they
   * start playing. Tried once per session so it never fights a manual exit.
   */
  private maybeAutoFullscreen(): void {
    if (this.autoFsTried) return;
    if (!this.fullscreenSupported() || this.isFullscreen()) return;
    if (this.settings.shell === 'plain') return;
    const coarse = window.matchMedia?.('(pointer: coarse)').matches ?? false;
    const landscape = window.matchMedia?.('(orientation: landscape)').matches ?? false;
    if (!coarse || !landscape) return;
    this.autoFsTried = true;
    void this.enterFullscreen();
  }

  /**
   * The portrait "rotate to landscape" nudge. It's always in the DOM (built once);
   * CSS shows it only on a touch device held in portrait, for the device/overlay
   * shells. Tapping it asks for fullscreen + a landscape lock where supported.
   */
  private ensureRotateHint(): void {
    if (this.rotateHintEl) return;
    const hint = document.createElement('div');
    hint.className = 'pk-rotate-hint';
    hint.setAttribute('role', 'button');
    hint.setAttribute('aria-label', 'Rotate your device to landscape for the best view');

    const ico = document.createElement('span');
    ico.className = 'pk-rotate-ico';
    ico.textContent = '↻'; // ↻
    const label = document.createElement('span');
    label.textContent = 'Turn sideways for the best view';
    const close = document.createElement('span');
    close.className = 'pk-rotate-x';
    close.setAttribute('aria-label', 'Dismiss');
    close.textContent = '×'; // ×

    hint.append(ico, label, close);
    hint.addEventListener('click', (e) => {
      if ((e.target as HTMLElement)?.classList.contains('pk-rotate-x')) {
        hint.classList.add('pk-dismissed');
        return;
      }
      void this.requestLandscape();
    });

    document.body.appendChild(hint);
    this.rotateHintEl = hint;
  }

  /**
   * Best-effort "go landscape": request fullscreen, then lock orientation. Android
   * Chrome honours both; iOS Safari supports neither, so this degrades to a no-op
   * and the player simply rotates the device (the hint stays up until they do).
   */
  private async requestLandscape(): Promise<void> {
    this.autoFsTried = true; // an explicit request supersedes the auto attempt
    await this.enterFullscreen();
    try {
      const orientation = (screen as unknown as {
        orientation?: { lock?: (o: string) => Promise<void> };
      }).orientation;
      if (orientation?.lock) await orientation.lock('landscape');
    } catch {
      /* Unsupported (e.g. iOS) — the hint already tells them to turn the device. */
    }
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

    // In-game control-size cycler (top-left). Not an input action — it resizes
    // the controls, so it's wired by hand and steps the same ControlSize the
    // Settings menu uses.
    root.appendChild(this.buildSizeToggle());

    document.body.appendChild(root);
    return root;
  }

  /** The top-left "resize controls" cycler. Tapping steps the size 1 → 2 → 3. */
  private buildSizeToggle(): HTMLDivElement {
    const el = document.createElement('div');
    el.className = 'pk-size-toggle';
    el.setAttribute('role', 'button');
    el.setAttribute('aria-label', 'Resize the on-screen controls');
    el.title = 'Controls size (tap to resize)';
    el.textContent = String(this.controlSize);

    el.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      el.classList.add('pk-active');
    });
    el.addEventListener('pointerup', (e) => {
      e.preventDefault();
      el.classList.remove('pk-active');
      void this.cycleControlSize();
    });
    el.addEventListener('pointercancel', () => el.classList.remove('pk-active'));
    el.addEventListener('pointerleave', () => el.classList.remove('pk-active'));
    el.addEventListener('contextmenu', (e) => e.preventDefault());
    return el;
  }

  /** Step the control size 1 → 2 → 3 → 1 (reuses setControlSize: applies + persists). */
  private async cycleControlSize(): Promise<void> {
    const next = ((this.controlSize % 3) + 1) as ControlSize;
    await this.setControlSize(next);
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
      // The first landscape press is a user gesture — claim the screen with it.
      this.maybeAutoFullscreen();
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
