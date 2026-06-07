# Cut concepts — the idea bank

`cut-concepts.json` holds every concept from the ~463-strong brainstorm pool
that did **not** make the final 151, sorted by blended panel score (highest
first). They were cut by the constrained selection in
`tools/balance/select.py` (see `docs/mechanics/07-selection-process.md`) — almost
always because their dex slot (region / primary type / tier) was already filled
by a higher-scoring line, **not** because they're bad. Many score in the 70s–80s.

This is a deliberate, reusable resource:

- **Future regions / DLC / post-game expansions** can draw from here first.
- **Replacements:** if a chosen kin needs to be swapped, its slot's runner-up is
  already identified and scored.
- **Variety bank:** alternate forms, seasonal variants, sidequest kin.

Each entry keeps its full concept schema (`docs/mechanics/08-data-schema.md`)
plus `_score` (blended panel score) and `_panel` (raw mean panel score). Nothing
is deleted — every idea the design panel generated is preserved here.

The raw per-batch generation files and the two panel score files live in
`../pool/` for full provenance.
