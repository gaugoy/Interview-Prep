#!/usr/bin/env python3
"""Build release notes: which questions were added, updated or removed since a previous version.

Compares two versions of index/catalog.json by stable question id (title hash) and content hash.

Usage
  python3 tools/release_notes.py --from-ref <tag|commit>          # vs. that git ref (preview locally)
  python3 tools/release_notes.py --from-ref release-2026.11.26-3 --out notes.md
  python3 tools/release_notes.py                                   # no previous release → initial notes
Exit codes: 0 = notes written (there are changes), 3 = nothing changed (no release needed).

Used by .github/workflows/release-notes.yml to publish a GitHub Release on every push to main.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "index" / "catalog.json"
LIST_LIMIT = 40   # max questions listed per section per change type
SECTION_ORDER = ["Python", "Django ORM Short", "Django ORM", "Django DRF", "django", "React"]
SECTION_NAME = {"Python": "🐍 Python", "Django ORM Short": "🗄️ Django ORM — Short", "Django ORM": "📖 Django ORM — Deep",
                "Django DRF": "🔌 Django REST Framework", "django": "🌱 Django (compact)", "React": "⚛️ React & Web"}


def load_catalog_text(text: str) -> dict[str, dict]:
    return {r["id"]: r for r in json.loads(text)}


def catalog_at(ref: str) -> dict[str, dict] | None:
    res = subprocess.run(["git", "show", f"{ref}:index/catalog.json"], cwd=ROOT, capture_output=True, text=True)
    return load_catalog_text(res.stdout) if res.returncode == 0 else None


def repo_blob_base() -> str | None:
    repo = os.environ.get("GITHUB_REPOSITORY")
    sha = os.environ.get("GITHUB_SHA")
    if not repo:
        url = subprocess.run(["git", "remote", "get-url", "origin"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        if "github.com" in url:
            repo = url.split("github.com")[-1].lstrip(":/").removesuffix(".git")
    if not sha:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    return f"https://github.com/{repo}/blob/{sha}" if repo and sha else None


def clean(title: str) -> str:
    return re.sub(r"\s*⭐?\s*Asked in my interview", "", title).strip()


def link(r: dict, base: str | None) -> str:
    title = clean(r["title"]).replace("|", "\\|").replace("[", "(").replace("]", ")")
    if not base:
        return title
    frag = f"#{r['anchor']}" if r.get("anchor") else ""
    return f"[{title}]({base}/{quote(r['file'])}{frag})"


def build(old: dict | None, new: dict, base: str | None, title: str) -> tuple[str, int]:
    per = lambda rs: {s: sorted([r for r in rs if r["stack"] == s], key=lambda r: (r["file"], r["n"])) for s in SECTION_ORDER}  # noqa: E731
    now_count = defaultdict(int)
    for r in new.values():
        now_count[r["stack"]] += 1

    if old is None:   # initial release: summary only
        lines = [f"# {title}", "", "**Initial release** of the interview question bank.", "",
                 "| Section | Questions |", "|---|---:|"]
        lines += [f"| {SECTION_NAME.get(s, s)} | {now_count[s]} |" for s in SECTION_ORDER if now_count[s]]
        lines += [f"| **Total** | **{len(new)}** |"]
        return "\n".join(lines) + "\n", len(new)

    added = [r for i, r in new.items() if i not in old]
    removed = [r for i, r in old.items() if i not in new]
    updated = [r for i, r in new.items() if i in old and old[i].get("hash") and r.get("hash") and old[i]["hash"] != r["hash"]]
    changes = len(added) + len(updated) + len(removed)
    if not changes:
        return "", 0

    A, U, R = per(added), per(updated), per(removed)
    lines = [f"# {title}", "",
             f"**{len(added)} added · {len(updated)} updated · {len(removed)} removed** — {len(new)} questions in total.", "",
             "| Section | ➕ Added | ✏️ Updated | ➖ Removed | Total now |", "|---|---:|---:|---:|---:|"]
    for s in SECTION_ORDER:
        if A[s] or U[s] or R[s]:
            lines.append(f"| {SECTION_NAME.get(s, s)} | {len(A[s]) or ''} | {len(U[s]) or ''} | {len(R[s]) or ''} | {now_count[s]} |")

    def section(heading: str, groups: dict, with_links: bool) -> None:
        if not any(groups.values()):
            return
        lines.extend(["", f"## {heading}"])
        for s in SECTION_ORDER:
            rs = groups[s]
            if not rs:
                continue
            lines.extend(["", f"**{SECTION_NAME.get(s, s)}**", ""])
            for r in rs[:LIST_LIMIT]:
                star = " ⭐ *asked in a real interview*" if r.get("asked") else ""
                lines.append(f"- {link(r, base) if with_links else clean(r['title'])}{star}")
            if len(rs) > LIST_LIMIT:
                lines.append(f"- …and {len(rs) - LIST_LIMIT} more")

    section("➕ Added", A, True)
    section("✏️ Updated answers", U, True)
    section("➖ Removed or renamed", R, False)
    lines += ["", "_Generated by `tools/release_notes.py` from `index/catalog.json`. A renamed question appears as removed + added._"]
    return "\n".join(lines) + "\n", changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-ref", help="previous release tag/commit (omit for an initial release)")
    ap.add_argument("--title", default="Release notes")
    ap.add_argument("--out", help="write markdown here (default: stdout)")
    a = ap.parse_args()

    new = load_catalog_text(CATALOG.read_text(encoding="utf-8"))
    old = catalog_at(a.from_ref) if a.from_ref else None
    if a.from_ref and old is None:
        print(f"warning: no index/catalog.json at {a.from_ref}; writing initial-release notes", file=sys.stderr)
    text, changes = build(old, new, repo_blob_base(), a.title)
    if not changes:
        print("No question changes since", a.from_ref, file=sys.stderr)
        return 3
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
