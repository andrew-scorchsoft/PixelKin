/**
 * Item registry. Inventory only stores counts; this maps an item id to its
 * definition. New item = an entry here. The vesperlamp is the player's core
 * capture device (PixelKin's original equivalent of the genre's capture tool).
 */
import type { ItemDef, ItemRegistry } from './types';

export const ITEMS: ItemRegistry = {
  vesperlamp: {
    id: 'vesperlamp',
    name: 'Vesperlamp',
    desc: 'Your lamp-tender\'s lantern. Coaxes a wild kin to walk with you.',
    category: 'lamp',
    catch_bonus: 1.0,
  },
  bright_lamp: {
    id: 'bright_lamp',
    name: 'Bright Lamp',
    desc: 'A keener flame. Better odds of befriending a wild kin.',
    category: 'lamp',
    catch_bonus: 1.5,
  },
  tallow_balm: {
    id: 'tallow_balm',
    name: 'Tallow Balm',
    desc: 'A warm salve that mends a kin a little. Restores some health.',
    category: 'medicine',
    heal: 20,
  },
  tide_charm: {
    id: 'tide_charm',
    name: 'Tide Charm',
    desc: 'A wave-worn charm lashed to a lamp-frame; the sea trusts it. The surest catch in the South.',
    category: 'lamp',
    catch_bonus: 2.0,
  },
};

export function getItem(id: string): ItemDef | undefined {
  return ITEMS[id];
}
