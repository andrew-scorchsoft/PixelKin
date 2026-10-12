# Running a big change (the playbook that shipped v1.6–v1.7)

How we ran a game-wide quality pass — story, maps, art, audio, engine — with
parallel agents, without breaking the game. Written from what actually worked
and what bit us. Read this before any change that spans more than one region or
system.

## 1. Evidence first: panels and measurements, not hunches
- **Panel → ranked list → work packages.** An imagined expert panel (scoring
  rubric, a real debate, consolidated verdict) turns "make it better" into a ranked,
  region-split list with effort and constraints per item. Reviews live in
  `docs/reviews/` (`story-depth-panel.md`, `world-craft-panel.md`,
  `music-remaster-panel.md`). Describe influences by craft, never by brand.
- **Measure before you judge.** The world-craft audit measured all 101 maps
  (props per screen, beats per ten steps, scripted moments) and found the real
  problem ("nothing to stop for", not "too short"). Those numbers became a gate
  (`audit_visual.py`).
- **Baseline screenshots from a CLEAN worktree** of the starting commit
  (`git worktree add … HEAD`, symlink `node_modules`/`venv`) at fixed tiles, so
  every later "after" shot is an honest A/B at the same position.
  `tools/shots/shoot.mjs` drives the real game; LOOK at the images yourself.

## 2. Pilot, then fan out
Prove each method on ONE area before rolling it out: the ambient kit on Dimglass
Coast I, the sprite standard on Warden Còr, the South story swaps, the music on
three tracks. Only once the pilot looks right in-game do the parallel packages
start, and they build on the committed pilot.

## 3. Parallel agents: ownership rules
- **Isolated worktrees branch from `main`, not your feature branch.** First step
  of every worktree agent: reset onto the feature branch (`git reset --hard
  origin/<branch>` before any commit). Every agent this round had to discover this.
- **One owner per shared file.** Engine files (`WorldScene.ts`, the entity
  classes, `CutsceneRunner.ts`) belong to ONE lane at a time; tell other lanes
  to wait and SendMessage them when it frees up.
- **Per-region modules exist so lanes don't collide:**
  `tools/maps/worldcraft/<region>.py`, `src/game/content/regions/<region>.ts`.
  Shared tables (`LIGHT_SOURCES`/`CHIMNEYS` in `Ambience.ts`) are grouped under
  `// <region>` comments, so a merge conflict is a trivial union.
- **Generated files are never hand-merged.** On a conflict in
  `objects.manifest.json` (or any packed manifest), re-run the packer
  (`pack_objects.py`, `pack_trainers.py`).
- **Two runners can fight over the same field.** E.g. `add_peril_thread.py` and a
  world-craft sprite swap. The `--check` drift gates expose it; the fix goes in the
  OWNING runner's data.
- **Reviewers are read-only; the coordinator applies fixes.** Concurrent edits to
  the same file by two agents lose work. Never commit another lane's
  half-finished files; commit by explicit path, not `git add -A`.

### Merging lanes back (learned on the Wild Ways round, v1.13–1.15)
- **Registry conflicts are unions.** `content/regions/index.ts`, `glossary.ts`,
  `quests.ts`, `graph.ts`/`maps.ts` conflict on every merge because each lane appends
  at the same spot: keep BOTH sides, mind the `},` between array entries, then `tsc`.
- **Regenerate, don't merge, every generated file:** `objects.manifest.json`
  (`pack_objects.py`), `worldmap.json` (`world_layout.py`), species/dex
  (`build_species.py` → `gen_docs.py`), `web/assets/data/music.json`
  (`build_music_data.mjs`), and any map JSON (its builder + the four runners).
- **A lane that changes a shared KIT makes every other in-flight lane stale.** When the
  interior pass grew the wall kit 13 → 55 tiles and made `roomkit.finish` autotile, the
  Paul's-house lane (branched earlier) shipped maps built on the old kit;
  `check_rebuild` showed it as `tile_count 13 -> 55` + gid diffs. Fix: re-run that
  lane's builders + runners after the merge — never patch the JSON.
- **Gates added mid-round don't run in older worktrees.** A lane that branched before
  `audit_npc_footing` existed passes its own `npm run check` and fails yours. Always
  run the FULL check on the merged branch, not trust the lane's report.
- **Read a lane's caveats as work for you.** The Paul lane flagged "the Chickenpig stays
  leading afterwards — an engine change would fix it". The fix was six lines
  (`WorldScene.playScene`); lanes are told not to touch shared engine files, so the
  coordinator owns those follow-ups.
- **Show the result.** `tools/maps/render_world.py` stitches every outdoor map at its true
  position (+ `--sheet` for portal maps) — the fastest way to review a round's geography,
  and what the owner asks for at the end.

## 4. Gates: one command, mirrors CI
- `npm run check` runs every CI gate locally (it parses
  `.github/workflows/checks.yml`, so new gates are picked up automatically).
  Use `--fast` to skip the slow rebuild and balance-sim steps while iterating.
  Run the full set before every PR.
- **New class of bug → new gate, in CI the same day.** This round added
  `audit_visual`, `check_content`, `audit_journey`, `check_rebuild`, walkability,
  sprite standards and walk-facing. Each caught real bugs the old gates missed.
- **Green gates ≠ "you can get everywhere".** The walkability gate fails only when CONTENT
  is stranded; a sealed nook of grass or floor that looks inviting ships green. Before
  calling a round done, run `render_walkable.py --all --report-only`, eyeball every
  non-border pocket ≥ 4 tiles, and check props sitting on a lane's path fill.
- **Prove a new gate catches the failure.** Plant the fault in a scratch worktree
  (a pew in front of a warden, a sealed cache) and confirm it FAILs, naming the
  fault.

## 5. Asset lessons
- gpt-image-2.5 leaves a faint alpha haze (1–30), so measure bboxes on
  thresholded alpha.
- Sheets can look right as a grid and still break when the walk cycles: run
  `check_walk_facing.py` and look at the GIF.
- Old chroma-key art: fix it losslessly (`defringe.py`) rather than redrawing
  approved designs.
- Generate to temp paths; compare in-game before replacing a master.

## 6. Shipping
- **Bump the version at the end of every round** and add a `whatsnew.ts` entry.
  Returning players hear everything since their save's version.
- **PR → GitHub CI → merge → Cloudflare deploys `main` in a few minutes.** A tab
  opened before the deploy shows the old build until it's reloaded (HTML is
  `max-age=0, must-revalidate`), so don't chase a cache bug.
- **After the PR merges,** restart the branch from the new `origin/main` before
  any follow-up work, and open a NEW PR.
