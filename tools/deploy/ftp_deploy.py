#!/usr/bin/env python3
"""
Deploy PixelKin to the pixelk.in FTP host — the marketing site at the web root,
the game under /play/ — by syncing the assembled `release/` folder.

    release/index.php, assets/, includes/  ->  /public_html/
    release/play/                          ->  /public_html/play/

Why a sync and not a blind re-upload: the remote root is a live cPanel account
holding folders we do NOT own (cgi-bin, .well-known, mail dirs, ...), and the
game's bundles are content-hashed, so yesterday's `index-a1b2c3d4.js` has to be
REMOVED or `play/assets/` grows forever. So:

  * Only changed files upload. A manifest of sha1 hashes is kept on the server
    (`.pixelkin-deploy.json`, one per scope root), so any machine can pick up
    the sync — no local state to lose.
  * Stale files are pruned, but the pruning rule differs per scope:
      - game  -> "mirror": /public_html/play is ours end to end, so anything up
        there that isn't in the local build gets deleted (this is what clears
        old hashed bundles).
      - site  -> "manifest": only files WE previously deployed and have since
        removed locally are deleted. Unknown neighbours at the web root are
        never touched.
  * Upload order is assets-first, entry documents (*.html/*.php) last, deletes
    after that — so a half-finished deploy never serves markup pointing at a
    bundle that hasn't landed.

Credentials come from the environment (or a local .env):

    FTP_HOST (or FTP_IP)   host / IP
    FTP_USER               username
    FTP_PASS               password           (or FTP_PASS_B64, base64-encoded)
    FTP_PORT               default 21
    FTP_TLS                auto (default) | on | off     explicit FTPS control
    FTP_REMOTE_ROOT        default /public_html
    FTP_GAME_SUBDIR        default play

Usage:
    python3 tools/deploy/ftp_deploy.py --scope both --dry-run
    python3 tools/deploy/ftp_deploy.py --scope game
    python3 tools/deploy/ftp_deploy.py --scope site
    python3 tools/deploy/ftp_deploy.py --scope both --version 1.4.0

Exit codes: 0 ok, 1 error/refused, 2 nothing to do (already in sync).
"""

from __future__ import annotations

import argparse
import base64
import fnmatch
import ftplib
import hashlib
import io
import json
import os
import posixpath
import ssl
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

MANIFEST_NAME = ".pixelkin-deploy.json"

# Never uploaded, never considered for deletion.
DEFAULT_EXCLUDES = [
    ".DS_Store",
    "Thumbs.db",
    "*.map",
    ".git*",
    MANIFEST_NAME,
]

# Belt-and-braces: even in mirror mode these remote names are never deleted.
PROTECTED_NAMES = {
    "cgi-bin",
    ".well-known",
    ".htaccess",
    ".htpasswd",
    ".user.ini",
    "php.ini",
    "error_log",
    MANIFEST_NAME,
}


# --------------------------------------------------------------------------- #
# config
# --------------------------------------------------------------------------- #

def load_dotenv(root: Path) -> None:
    """Fill in missing env vars from a local .env (real env always wins)."""
    path = root / ".env"
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


@dataclass
class Creds:
    host: str
    user: str
    password: str
    port: int = 21
    tls: str = "auto"          # auto | on | off

    @classmethod
    def from_env(cls) -> "Creds":
        host = os.environ.get("FTP_HOST") or os.environ.get("FTP_IP") or ""
        user = os.environ.get("FTP_USER", "")
        password = os.environ.get("FTP_PASS", "")
        if not password and os.environ.get("FTP_PASS_B64"):
            password = base64.b64decode(os.environ["FTP_PASS_B64"]).decode("utf-8")
        missing = [n for n, v in (("FTP_HOST/FTP_IP", host), ("FTP_USER", user),
                                  ("FTP_PASS/FTP_PASS_B64", password)) if not v]
        if missing:
            die("missing FTP credentials in the environment: " + ", ".join(missing)
                + "\n       Set them in the environment or a local .env (see .env.example).")
        return cls(
            host=host,
            user=user,
            password=password,
            port=int(os.environ.get("FTP_PORT") or 21),
            tls=(os.environ.get("FTP_TLS") or "auto").lower(),
        )


# --------------------------------------------------------------------------- #
# small helpers
# --------------------------------------------------------------------------- #

def die(msg: str) -> "NoReturn":  # type: ignore[valid-type]
    print(f"ftp_deploy: {msg}", file=sys.stderr)
    sys.exit(1)


def sha1_of(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def excluded(rel: str, patterns: list[str]) -> bool:
    name = posixpath.basename(rel)
    return any(fnmatch.fnmatch(name, p) or fnmatch.fnmatch(rel, p) for p in patterns)


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f}{unit}" if unit == "B" else f"{n:.1f}{unit}"
        n /= 1024.0
    return f"{n:.1f}GB"


def upload_rank(rel: str) -> tuple[int, str]:
    """Assets first, entry documents last — so markup never outruns its bundles."""
    lower = rel.lower()
    if lower.endswith((".html", ".php", ".webmanifest")):
        return (2, rel)
    if posixpath.basename(lower) in ("sitemap.xml", "robots.txt"):
        return (1, rel)
    return (0, rel)


# --------------------------------------------------------------------------- #
# FTP session
# --------------------------------------------------------------------------- #

class Session:
    """A thin ftplib wrapper: reconnects on drop, knows how to walk + mkdir -p."""

    def __init__(self, creds: Creds, verbose: bool = False) -> None:
        self.creds = creds
        self.verbose = verbose
        self.ftp: ftplib.FTP | None = None
        self._mkdir_cache: set[str] = set()

    # -- connection ------------------------------------------------------- #

    def connect(self) -> None:
        creds = self.creds
        attempts: list[str] = []
        if creds.tls in ("auto", "on"):
            attempts.append("tls")
        if creds.tls in ("auto", "off"):
            attempts.append("plain")

        last: Exception | None = None
        for mode in attempts:
            try:
                if mode == "tls":
                    ftp = ftplib.FTP_TLS(context=ssl.create_default_context())
                    ftp.connect(creds.host, creds.port, timeout=45)
                    ftp.login(creds.user, creds.password)
                    ftp.prot_p()
                else:
                    ftp = ftplib.FTP()
                    ftp.connect(creds.host, creds.port, timeout=45)
                    ftp.login(creds.user, creds.password)
                ftp.set_pasv(True)
                self.ftp = ftp
                print(f"  connected: {creds.user}@{creds.host}:{creds.port} "
                      f"({'FTPS' if mode == 'tls' else 'plain FTP'})")
                return
            except Exception as exc:   # refused / no AUTH TLS / bad creds / timeout
                last = exc
                if self.verbose:
                    print(f"  · {mode} connect failed: {type(exc).__name__}: {exc}")
        die(f"could not connect to {creds.host}:{creds.port} — {type(last).__name__}: {last}")

    def close(self) -> None:
        if self.ftp is not None:
            try:
                self.ftp.quit()
            except Exception:
                try:
                    self.ftp.close()
                except Exception:
                    pass
            self.ftp = None

    def _reconnect(self) -> None:
        self.close()
        self._mkdir_cache.clear()
        time.sleep(2)
        self.connect()

    def _retry(self, fn, *args, tries: int = 3, **kwargs):
        last: Exception | None = None
        for attempt in range(1, tries + 1):
            try:
                return fn(*args, **kwargs)
            except ftplib.error_perm:
                raise                       # a real "no" from the server — don't retry
            except Exception as exc:        # transient: dropped data channel, timeout
                last = exc
                if attempt == tries:
                    break
                print(f"    retry {attempt}/{tries - 1} after {type(exc).__name__}: {exc}")
                self._reconnect()
        raise last  # type: ignore[misc]

    # -- listing ---------------------------------------------------------- #

    def entries(self, remote_dir: str) -> list[tuple[str, bool]]:
        """[(name, is_dir)] for one remote directory; [] if it doesn't exist."""
        assert self.ftp
        out: list[tuple[str, bool]] = []
        try:
            for name, facts in self.ftp.mlsd(remote_dir):
                if name in (".", ".."):
                    continue
                out.append((name, facts.get("type") == "dir"))
            return out
        except (ftplib.error_perm, ftplib.error_proto):
            pass  # server without MLSD — fall back to LIST parsing
        lines: list[str] = []
        try:
            self.ftp.retrlines(f"LIST {remote_dir}", lines.append)
        except ftplib.error_perm:
            return []
        for line in lines:
            parts = line.split(maxsplit=8)
            if len(parts) < 9:
                continue
            name = parts[8]
            if name in (".", ".."):
                continue
            out.append((name, line[0] == "d"))
        return out

    def walk(self, remote_dir: str, prefix: str = "") -> dict[str, None]:
        """Every FILE under remote_dir, keyed by path relative to it."""
        found: dict[str, None] = {}
        for name, is_dir in self.entries(remote_dir):
            rel = posixpath.join(prefix, name) if prefix else name
            if is_dir:
                found.update(self.walk(posixpath.join(remote_dir, name), rel))
            else:
                found[rel] = None
        return found

    def exists_dir(self, remote_dir: str) -> bool:
        assert self.ftp
        pwd = self.ftp.pwd()
        try:
            self.ftp.cwd(remote_dir)
            return True
        except ftplib.error_perm:
            return False
        finally:
            try:
                self.ftp.cwd(pwd)
            except Exception:
                pass

    # -- mutation --------------------------------------------------------- #

    def ensure_dir(self, remote_dir: str) -> None:
        if remote_dir in self._mkdir_cache or remote_dir in ("", "/"):
            return
        parent = posixpath.dirname(remote_dir)
        if parent and parent != remote_dir:
            self.ensure_dir(parent)
        assert self.ftp
        try:
            self.ftp.mkd(remote_dir)
        except ftplib.error_perm:
            pass  # already there (or no permission — the upload will report it)
        self._mkdir_cache.add(remote_dir)

    def upload(self, local: Path, remote_path: str) -> None:
        self.ensure_dir(posixpath.dirname(remote_path))

        def _put() -> None:
            assert self.ftp
            with local.open("rb") as fh:
                self.ftp.storbinary(f"STOR {remote_path}", fh, blocksize=1 << 17)

        self._retry(_put)

    def upload_bytes(self, data: bytes, remote_path: str) -> None:
        self.ensure_dir(posixpath.dirname(remote_path))

        def _put() -> None:
            assert self.ftp
            self.ftp.storbinary(f"STOR {remote_path}", io.BytesIO(data))

        self._retry(_put)

    def read_text(self, remote_path: str) -> str | None:
        assert self.ftp
        buf = io.BytesIO()
        try:
            self.ftp.retrbinary(f"RETR {remote_path}", buf.write)
        except ftplib.all_errors:
            return None
        return buf.getvalue().decode("utf-8", "replace")

    def delete(self, remote_path: str) -> None:
        assert self.ftp
        try:
            self.ftp.delete(remote_path)
        except ftplib.error_perm as exc:
            print(f"    ! could not delete {remote_path}: {exc}")

    def prune_empty_dirs(self, root: str) -> None:
        """Remove directories that the delete pass emptied out (best effort)."""
        for name, is_dir in self.entries(root):
            if not is_dir:
                continue
            child = posixpath.join(root, name)
            self.prune_empty_dirs(child)
            if not self.entries(child):
                assert self.ftp
                try:
                    self.ftp.rmd(child)
                    print(f"    - {child}/  (empty)")
                except ftplib.error_perm:
                    pass


# --------------------------------------------------------------------------- #
# the sync
# --------------------------------------------------------------------------- #

@dataclass
class Scope:
    name: str                # "site" | "game"
    local: Path
    remote: str
    prune: str               # "manifest" | "mirror" | "none"
    skip_dirs: set[str] = field(default_factory=set)   # local top-level dirs to leave alone


def scan_local(scope: Scope, excludes: list[str]) -> dict[str, tuple[Path, str, int]]:
    """rel path -> (local path, sha1, size)."""
    files: dict[str, tuple[Path, str, int]] = {}
    for path in sorted(scope.local.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(scope.local).as_posix()
        top = rel.split("/", 1)[0]
        if top in scope.skip_dirs:
            continue
        if excluded(rel, excludes):
            continue
        files[rel] = (path, sha1_of(path), path.stat().st_size)
    return files


def sync_scope(sess: Session, scope: Scope, *, dry_run: bool, version: str | None,
               excludes: list[str], force: bool) -> tuple[int, int]:
    print(f"\n[{scope.name}]  {scope.local}  ->  {scope.remote}   (prune: {scope.prune})")
    if not scope.local.is_dir():
        die(f"local folder {scope.local} not found — run `npm run release` first.")

    local = scan_local(scope, excludes)
    if not local:
        die(f"no files found under {scope.local}.")

    manifest_path = posixpath.join(scope.remote, MANIFEST_NAME)
    remote_hashes: dict[str, str] = {}
    raw = sess.read_text(manifest_path)
    if raw:
        try:
            remote_hashes = json.loads(raw).get("files", {}) or {}
            print(f"  manifest: {len(remote_hashes)} files recorded from the last deploy")
        except json.JSONDecodeError:
            print("  manifest: unreadable — treating this as a first deploy")
    else:
        print("  manifest: none on the server — this is a first deploy for this scope")

    # What to upload.
    uploads = [rel for rel, (_p, digest, _s) in local.items()
               if force or remote_hashes.get(rel) != digest]
    uploads.sort(key=upload_rank)

    # What to delete.
    deletes: list[str] = []
    if scope.prune == "manifest":
        deletes = sorted(set(remote_hashes) - set(local))
    elif scope.prune == "mirror":
        if sess.exists_dir(scope.remote):
            remote_files = sess.walk(scope.remote)
            deletes = sorted(rel for rel in remote_files
                             if rel not in local
                             and not excluded(rel, excludes)
                             and rel.split("/", 1)[0] not in PROTECTED_NAMES)
    deletes = [rel for rel in deletes if posixpath.basename(rel) not in PROTECTED_NAMES]

    unchanged = len(local) - len(uploads)
    bytes_up = sum(local[rel][2] for rel in uploads)
    print(f"  plan: {len(uploads)} upload, {len(deletes)} delete, {unchanged} unchanged "
          f"({human(bytes_up)} to send)")
    for rel in uploads[:40]:
        print(f"    + {rel}")
    if len(uploads) > 40:
        print(f"    + … and {len(uploads) - 40} more")
    for rel in deletes[:40]:
        print(f"    - {rel}")
    if len(deletes) > 40:
        print(f"    - … and {len(deletes) - 40} more")

    if dry_run:
        print("  (dry run — nothing sent)")
        return (len(uploads), len(deletes))

    if not uploads and not deletes:
        print("  already in sync.")
        return (0, 0)

    sess.ensure_dir(scope.remote)
    for i, rel in enumerate(uploads, 1):
        path = local[rel][0]
        remote_path = posixpath.join(scope.remote, rel)
        sess.upload(path, remote_path)
        print(f"    [{i}/{len(uploads)}] + {rel} ({human(local[rel][2])})")

    # Manifest lands after the uploads, before the deletes: if the run dies
    # mid-delete the next deploy still sees an accurate picture of what's up.
    manifest = {
        "version": version,
        "scope": scope.name,
        "deployed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": {rel: digest for rel, (_p, digest, _s) in local.items()},
    }
    sess.upload_bytes(json.dumps(manifest, indent=1).encode("utf-8"), manifest_path)

    for rel in deletes:
        remote_path = posixpath.join(scope.remote, rel)
        sess.delete(remote_path)
        print(f"    - {rel}")
    if deletes and scope.prune == "mirror":
        sess.prune_empty_dirs(scope.remote)

    print(f"  done: {len(uploads)} uploaded, {len(deletes)} deleted.")
    return (len(uploads), len(deletes))


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #

def main() -> int:
    root = Path(__file__).resolve().parents[2]
    load_dotenv(root)

    ap = argparse.ArgumentParser(description="Sync release/ to the pixelk.in FTP host.")
    ap.add_argument("--scope", choices=["site", "game", "both"], default="both",
                    help="what to upload (default: both)")
    ap.add_argument("--release-dir", default=str(root / "release"),
                    help="assembled release folder (default: ./release)")
    ap.add_argument("--remote-root", default=os.environ.get("FTP_REMOTE_ROOT", "/public_html"),
                    help="remote web root (default: /public_html)")
    ap.add_argument("--game-subdir", default=os.environ.get("FTP_GAME_SUBDIR", "play"),
                    help="game subfolder under the web root (default: play)")
    ap.add_argument("--site-prune", choices=["manifest", "mirror", "none"], default="manifest",
                    help="how to remove stale SITE files (default: manifest — only ever "
                         "deletes files this tool previously uploaded)")
    ap.add_argument("--game-prune", choices=["manifest", "mirror", "none"], default="mirror",
                    help="how to remove stale GAME files (default: mirror — play/ is ours "
                         "end to end, so old hashed bundles get cleared)")
    ap.add_argument("--exclude", action="append", default=[],
                    help="extra glob to skip (repeatable)")
    ap.add_argument("--version", default=None, help="version string to record in the manifest")
    ap.add_argument("--force", action="store_true",
                    help="re-upload every file, ignoring the manifest")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, send nothing")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    release = Path(args.release_dir).resolve()
    remote_root = "/" + args.remote_root.strip("/")
    game_remote = posixpath.join(remote_root, args.game_subdir.strip("/"))
    excludes = DEFAULT_EXCLUDES + args.exclude

    scopes: list[Scope] = []
    if args.scope in ("site", "both"):
        scopes.append(Scope(
            name="site",
            local=release,
            remote=remote_root,
            prune=args.site_prune,
            # the game lives in its own scope; never let the site pass touch it
            skip_dirs={args.game_subdir.strip("/")},
        ))
    if args.scope in ("game", "both"):
        scopes.append(Scope(
            name="game",
            local=release / args.game_subdir.strip("/"),
            remote=game_remote,
            prune=args.game_prune,
        ))

    print("ftp_deploy:")
    print(f"  release : {release}")
    print(f"  scope   : {args.scope}")
    if args.version:
        print(f"  version : {args.version}")
    if args.dry_run:
        print("  mode    : DRY RUN")

    creds = Creds.from_env()
    sess = Session(creds, verbose=args.verbose)
    sess.connect()
    total_up = total_del = 0
    try:
        for scope in scopes:
            up, dele = sync_scope(sess, scope, dry_run=args.dry_run, version=args.version,
                                  excludes=excludes, force=args.force)
            total_up += up
            total_del += dele
    finally:
        sess.close()

    print(f"\nftp_deploy: {total_up} uploaded, {total_del} deleted"
          f"{' (dry run)' if args.dry_run else ''}.")
    if not args.dry_run:
        print("  site → https://pixelk.in/     game → https://pixelk.in/play/")
    return 2 if (total_up == 0 and total_del == 0) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nftp_deploy: interrupted.", file=sys.stderr)
        sys.exit(1)
