/**
 * Tolerant, lazy loader for packed creature (kin) sprites.
 *
 * The art masters under assets/creatures/ are packed into served lossless-WebP files plus
 * a manifest by `.claude/skills/generate-sprite-sheet/scripts/pack_creatures.py`. This
 * module is the engine's read side: it imports that manifest and lazily loads a kin's view
 * into a Phaser texture on demand, mirroring the tolerant load pattern in
 * `systems/world/MapRenderer.ts` (`tryLoadAtlas`) and `systems/audio/loadAudio.ts` — a kin
 * or view that isn't packed yet resolves to null rather than throwing, so battle/menus can
 * fall back to a placeholder without special-casing.
 *
 * Content is data-driven: packing the remaining kin is one re-run of the packer, no code
 * change here. Not wired into any scene yet — the orchestrator swaps it into Battler /
 * StarterSelect / the overworld during a review pass.
 */
import Phaser from 'phaser';
import manifest from '../../../../public/assets/sprites/creatures/creatures.manifest.json';

/** The five standard creature views (docs/art-style.md §4). */
export type CreatureView = 'front' | 'back' | 'icon' | 'overworld' | 'portrait';

interface PackedView {
  path: string;
  width: number;
  height: number;
}

interface CreatureEntry {
  slug: string;
  front?: PackedView;
  back?: PackedView;
  icon?: PackedView;
  overworld?: PackedView;
  portrait?: PackedView;
}

interface CreatureManifest {
  creatures: Record<string, CreatureEntry>;
}

const CREATURES: Record<string, CreatureEntry> = (manifest as CreatureManifest).creatures;

function entry(id: number): CreatureEntry | undefined {
  return CREATURES[String(id)];
}

function view(id: number, v: CreatureView): PackedView | undefined {
  return entry(id)?.[v];
}

/** True if a packed sprite exists for this kin id and view. */
export function hasCreatureSprite(id: number, v: CreatureView): boolean {
  return view(id, v) !== undefined;
}

/** Deterministic Phaser texture key for a kin view, e.g. `kin_1_front`. */
export function creatureTextureKey(id: number, v: CreatureView): string {
  return `kin_${id}_${v}`;
}

/** Served path (no public/ prefix) for a kin view, or null if not packed. */
export function creatureSpritePath(id: number, v: CreatureView): string | null {
  return view(id, v)?.path ?? null;
}

/**
 * Lazily load a kin's view into a Phaser texture, resolving its texture key on success or
 * null if the kin/view isn't packed or the file fails to load. Safe to call repeatedly —
 * an already-loaded texture resolves immediately without re-fetching.
 */
export function loadCreatureSprite(
  scene: Phaser.Scene,
  id: number,
  v: CreatureView,
): Promise<string | null> {
  const packed = view(id, v);
  if (!packed) return Promise.resolve(null);

  const key = creatureTextureKey(id, v);
  return new Promise((resolve) => {
    if (scene.textures.exists(key)) {
      resolve(key);
      return;
    }
    const onFile = (fileKey: string): void => {
      if (fileKey === key) {
        cleanup();
        resolve(key);
      }
    };
    const onError = (file: Phaser.Loader.File): void => {
      if (file.key === key) {
        cleanup();
        resolve(null);
      }
    };
    const cleanup = (): void => {
      scene.load.off(Phaser.Loader.Events.FILE_COMPLETE, onFile);
      scene.load.off(Phaser.Loader.Events.FILE_LOAD_ERROR, onError);
    };
    scene.load.on(Phaser.Loader.Events.FILE_COMPLETE, onFile);
    scene.load.on(Phaser.Loader.Events.FILE_LOAD_ERROR, onError);
    scene.load.image(key, packed.path);
    scene.load.start();
  });
}
