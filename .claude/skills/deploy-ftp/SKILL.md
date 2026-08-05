---
name: deploy-ftp
description: Deploy PixelKin to the live pixelk.in host over FTP — the marketing site at the web root, the playable game under /play/ — bumping the version, building, and syncing only what changed (pruning stale hashed bundles). Use whenever the user asks to deploy, publish, ship, release, upload to FTP, or "push it live".
---

# Deploy to pixelk.in over FTP

Ships what's in the working tree to the live cPanel host:

```
release/  (assembled)              ->  remote
  index.php, assets/, includes/    ->  /public_html/        = https://pixelk.in/
  play/                            ->  /public_html/play/   = https://pixelk.in/play/
```

The remote root is a **live account with folders that aren't ours** (`cgi-bin`,
`.well-known`, `mail`, `logs`, `tmp`, `ssl`, `www`). Never mirror-delete the web
root. The tooling already encodes that; don't hand-roll an upload.

## Step 1 — ask the two questions FIRST

Use `AskUserQuestion` with **both** questions in one call (unless the user
already stated the answers in their message, in which case skip straight to
step 2 and say what you're assuming):

1. **Scope** — "What should I upload?"
   - `Both` (site + game) — recommended default
   - `Game only` — rebuilds `dist/`, syncs `/public_html/play/`
   - `Site only` — refreshes the `web/` pages, leaves `play/` untouched
2. **Version bump** — "Bump the version?"
   - `Minor` — **recommended default** (1.3.0 → 1.4.0)
   - `Major` — 1.3.0 → 2.0.0
   - `None` — deploy on the current version
   - (`Patch` is available too if they ask: 1.3.0 → 1.3.1)

A site-only deploy with no game change still normally wants a bump — the version
shows in-game, so mention it but let the answer stand.

## Step 2 — bump the version

```bash
node tools/build/bump_version.mjs minor      # or major | patch | none
```

Writes both places at once: `package.json` `version` and `src/game/version.ts`
`GAME_VERSION` (the title-screen / tab-title string, `major.minor`). It prints
`version=X.Y.Z` on the last line — keep that for the commit message and the
deploy manifest. Skip this step entirely on `none`.

## Step 3 — build and assemble `release/`

Match the build to the scope so you don't rebuild the game for a copy tweak:

| Scope | Command | What it does |
|-------|---------|--------------|
| Both | `npm run release` | typecheck + Vite build + audio shrink + strip sourcemaps, then site + `dist/` → `release/` |
| Game only | `npm run release:game` | same build, drops `dist/` into `release/play/` only |
| Site only | `npm run release:site` | copies `web/` → `release/` and **leaves `release/play/` alone** |

If the build fails, stop and report it — never deploy a partial `release/`.

## Step 4 — dry run, show the plan, then upload

Always dry-run first and show the user the plan (counts + a sample of the
adds/deletes) before sending anything:

```bash
python3 tools/deploy/ftp_deploy.py --scope both --dry-run --version 1.4.0
```

Then, once it looks right:

```bash
python3 tools/deploy/ftp_deploy.py --scope both --version 1.4.0
```

`--scope` takes `both | site | game`. There are npm wrappers that do build +
deploy in one (`npm run deploy`, `deploy:site`, `deploy:game`, `deploy:dry`) —
use the explicit commands above when you're bumping a version, since the
wrappers don't pass `--version`.

**Deletions are real.** If the dry run proposes deleting something that looks
like it isn't ours, stop and ask before running for real.

## Step 5 — commit and report

Commit the version bump (and any content changes) on the working branch with a
message like `chore(release): v1.4.0 — deploy site + game`, push, then tell the
user what landed: version, scope, files uploaded/deleted, and the two URLs.
Suggest a hard-refresh (Ctrl/Cmd-Shift-R) if they're checking straight away —
`index.html` is not content-hashed, so a browser cache can hide a new build for
a minute.

## How the sync decides what to send (so you can explain it)

- Every file's sha1 goes into a manifest stored **on the server** at each scope
  root (`.pixelkin-deploy.json`). Next deploy compares against it, so only
  changed files upload — a copy tweak sends a couple of KB, not the whole
  ~100MB bundle. `--force` re-uploads everything.
- **Pruning differs per scope, deliberately:**
  - `game` → **mirror**: `/public_html/play` is ours end to end, so anything up
    there that isn't in the new build is deleted. This is what clears the old
    content-hashed `assets/index-<hash>.js` bundles, and it prunes the
    directories it empties.
  - `site` → **manifest**: only deletes files *this tool previously uploaded*
    and that no longer exist locally. Unknown neighbours at the web root are
    never touched. Don't switch the site to mirror.
- Upload order is assets first, `*.html` / `*.php` / `*.webmanifest` last, then
  deletes — so a half-finished run never serves markup pointing at a bundle
  that hasn't landed.
- `.map` files, `.DS_Store`, and dotfiles like `.git*` are excluded.

## Credentials

From the environment (or a local `.env`, which is git-ignored):

```
FTP_HOST (or FTP_IP)   FTP_USER   FTP_PASS (or FTP_PASS_B64)
FTP_PORT=21            FTP_TLS=auto|on|off
FTP_REMOTE_ROOT=/public_html        FTP_GAME_SUBDIR=play
```

`FTP_TLS=auto` tries FTPS (explicit `AUTH TLS`) and falls back to plain FTP.
**Never print the password, and never commit it.**

## Gotchas

- **Plain FTP is port 21 and is often blocked in sandboxed/remote sessions.**
  If the connect times out, the network is the problem, not the script — say so
  and give the user the exact command to run locally rather than retrying.
- `--scope site` does *not* rebuild the game, and `release:site` deliberately
  leaves a staged `release/play/` in place. If someone asks for "site only"
  right after a game change, the game does **not** go live.
- Exit code `2` means "nothing to do — already in sync". That's success, not a
  failure.
- Only `web/` and `dist/` content is deployed. Editing a file under `public/`
  or `src/` requires a rebuild (step 3) before it can ship.
