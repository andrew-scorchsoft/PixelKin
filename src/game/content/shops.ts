/**
 * Shop registry — each town keeper's counter. A shop is a *selection*, not a
 * price list: prices live on the ItemDefs (one price across Vesperholm), so a
 * shop entry is just the item ids it stocks, in display order. A keeper opens
 * their counter via the cutscene op `{ op: 'shop', shop: '<id>' }` at the end
 * of their dialogue script — adding/retuning a shop is a data edit here.
 *
 * Stocking rules (docs/mechanics/10-economy.md §5): every Lumenary town shop
 * carries the medicine + lamp tier for its stop on the curve, 2–4 Star-charts
 * (the region's elements + a Plain utility), and keeps the previous tier
 * available so a struggling player can stock up cheap.
 */
import type { ShopDef, ShopRegistry } from './types';
import { ITEMS } from './items';

export const SHOPS: ShopRegistry = {
  // Tinderwick General Store — the first counter; humble, warm, everything a
  // brand-new Wayfarer can afford within their first hour.
  tinderwick_general: {
    id: 'tinderwick_general',
    name: 'TINDERWICK GENERAL',
    stock: ['tallow_balm', 'vesperlamp', 'chart_cinder_spit', 'chart_mist_spray'],
  },

  // Pearlmoor Chandlery — the crossing outfitter; first bright lamps, the
  // mid salve, and the South's Standard-band charts before Reyl's bond-test.
  pearlmoor_chandlery: {
    id: 'pearlmoor_chandlery',
    name: 'PEARLMOOR CHANDLERY',
    stock: [
      'tallow_balm',
      'warm_balm',
      'vesperlamp',
      'bright_lamp',
      'chart_wave_crash',
      'chart_hearth_pulse',
      'chart_gust_up',
      'chart_focus_mind',
    ],
  },
};

export function getShop(id: string): ShopDef | undefined {
  return SHOPS[id];
}

// Fail fast in dev if a shop stocks something unpriced/unknown — a silent bad
// id would otherwise surface as a blank row at the counter.
for (const shop of Object.values(SHOPS)) {
  for (const id of shop.stock) {
    const def = ITEMS[id];
    if (!def) console.warn(`Shop ${shop.id} stocks unknown item '${id}'`);
    else if (def.price === undefined) console.warn(`Shop ${shop.id} stocks unpriced item '${id}'`);
  }
}
