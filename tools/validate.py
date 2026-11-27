#!/usr/bin/env python3
"""Validate the interview content against the per-stack rules in tools/catalog.py.

Checks
  anchors   `<a name="qN">` present and matching position        (stacks with anchors=True)
  answer    every question has `**Answer:**`                       (stacks with answer=True)
  code      ```python blocks parse with ast.parse                  (error / warn / off per stack)
  links     every relative link's file exists and its #anchor exists in the target
  titles    a link that names a question (TOC, bank, "— title") points to THAT question
            (catches positional #qN links that drifted after renumbering)
  bank      question banks list exactly the questions in the files (count + titles)
  dupes     the same question title twice in one stack             (warning)

Usage
  python3 tools/validate.py                 # everything
  python3 tools/validate.py --file Python/02_OOP.md   # one file (fast, used by hooks)
  python3 tools/validate.py --changed       # files changed vs HEAD (+ untracked)
  python3 tools/validate.py --strict        # warnings count as errors
Exit code 1 if any error.
"""
from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

from catalog import (ANCHOR_RE, LINK_CHECK_ROOT_FILES, LINK_RE, META_NAMES, ROOT, STACKS,
                     _norm, load, norm_title, similar)

PY_BLOCK_RE = re.compile(r"```python\n(.*?)```", re.S)
NAMED_ANCHOR_RE = re.compile(r'<a\s+(?:name|id)="([^"]+)"')
HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$", re.M)
QLINK_TEXT_RE = re.compile(r"^[\w &]+ · Q(\d+)$")


class Report:
    def __init__(self, strict: bool):
        self.strict, self.items = strict, []

    def error(self, where, msg): self.items.append(("ERROR", where, msg))
    def warn(self, where, msg): self.items.append(("ERROR" if self.strict else "WARN", where, msg))

    def emit(self) -> int:
        for level, where, msg in sorted(self.items, key=lambda x: (x[0] != "ERROR", x[1])):
            print(f"{level} {where}: {msg}")
        errors = sum(1 for i in self.items if i[0] == "ERROR")
        warns = len(self.items) - errors
        print(f"\n{errors} error(s), {warns} warning(s).")
        return 1 if errors else 0


def gh_slug(text: str) -> str:
    return re.sub(r"[^\w\- ]", "", text.strip().lower()).replace(" ", "-")


_anchor_cache: dict[Path, set[str]] = {}


def anchors_of(path: Path) -> set[str]:
    if path not in _anchor_cache:
        text = path.read_text(encoding="utf-8", errors="replace")
        names = set(NAMED_ANCHOR_RE.findall(text)) | {gh_slug(h) for h in HEADING_RE.findall(text)}
        _anchor_cache[path] = names
    return _anchor_cache[path]


def changed_files() -> set[str]:
    out = subprocess.run(["git", "status", "--porcelain", "-uall"], cwd=ROOT, capture_output=True, text=True).stdout
    files = set()
    for line in out.splitlines():
        p = line[3:].split(" -> ")[-1].strip().strip('"')
        if p.endswith(".md"):
            files.add(p)
    return files


def link_files(scope: set[str] | None) -> list[Path]:
    paths = []
    for stack in STACKS:
        paths += sorted((ROOT / stack).rglob("*.md"))
    paths += sorted((ROOT / "prompts").glob("*.md")) + [ROOT / "index" / "INDEX.md"]
    paths += [ROOT / f for f in LINK_CHECK_ROOT_FILES]
    paths = [p for p in paths if p.exists()]
    if scope is not None:
        paths = [p for p in paths if p.relative_to(ROOT).as_posix() in scope]
    return paths


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", action="append", help="limit to these files (repo-relative)")
    ap.add_argument("--changed", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    rep = Report(a.strict)

    scope = None
    if a.file:
        scope = {Path(f).resolve().relative_to(ROOT).as_posix() if Path(f).is_absolute() else f for f in a.file}
    elif a.changed:
        scope = changed_files()
        if not scope:
            print("No changed .md files."); return 0

    questions, files = load()
    by_file = defaultdict(list)
    for q in questions:
        by_file[q.file].append(q)
    in_scope = lambda f: scope is None or f in scope  # noqa: E731

    # ---- per-question rules
    for f, qs in by_file.items():
        if not in_scope(f):
            continue
        cfg = STACKS[qs[0].stack]
        pf = files[f]
        if getattr(pf, "error", None):
            rep.error(f, f"parse error: {pf.error}")
        for q in qs:
            where = f"{f}:{q.line_start}"
            if cfg["anchors"] and q.anchor != f"q{q.n}":
                rep.error(where, f"anchor should be <a name=\"q{q.n}\"> (found {q.anchor or 'none'})")
            pq = pf.questions[q.n - 1]
            if cfg["answer"] and "**Answer:**" not in pq.markdown:
                rep.error(where, "missing **Answer:**")
            if cfg["code"] != "off":
                for i, code in enumerate(PY_BLOCK_RE.findall(pq.markdown), 1):
                    try:
                        ast.parse(code)
                    except SyntaxError as e:
                        msg = f"python block {i} does not parse: {e.msg} (line {e.lineno})"
                        (rep.error if cfg["code"] == "error" else rep.warn)(where, msg)

    # ---- duplicate titles inside a stack
    seen = defaultdict(list)
    for q in questions:
        seen[(q.stack, norm_title(q.title))].append(q)
    for (stack, _), qs in seen.items():
        if len(qs) > 1 and any(in_scope(q.file) for q in qs):
            rep.warn(f"{qs[0].file}:{qs[0].line_start}", f"same title also in {', '.join(f'{x.file}:{x.line_start}' for x in qs[1:])}")

    # ---- links (existence + anchor + named-question title)
    q_by_anchor = {(q.file, q.anchor): q for q in questions if q.anchor}
    for path in link_files(scope):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        in_code = False
        for ln_no, line in enumerate(text.split("\n"), 1):
            if line.lstrip().startswith("```"):
                in_code = not in_code
            if in_code:
                continue
            scan = re.sub(r"`[^`]*`", "", line)   # links inside inline code are examples
            for m in LINK_RE.finditer(scan):
                label, target = m.group(1), m.group(2)
                if target.startswith(("http://", "https://", "mailto:", "file://")):
                    continue
                tpath, _, frag = target.partition("#")
                tgt = path if not tpath else (path.parent / unquote(tpath))
                where = f"{rel}:{ln_no}"
                if not tgt.exists():
                    rep.error(where, f"broken link → {target} (file not found)"); continue
                if tgt.is_dir() or not frag:
                    continue
                if frag not in anchors_of(tgt):
                    rep.error(where, f"broken link → {target} (anchor #{frag} not found)"); continue
                tq = q_by_anchor.get((_norm(tgt.resolve().relative_to(ROOT).as_posix()), frag))
                if not tq:
                    continue
                qm = QLINK_TEXT_RE.match(label.strip())
                if qm:   # "[Topic · Q12](...) — Title"
                    if int(qm.group(1)) != tq.n:
                        rep.error(where, f"link text says Q{qm.group(1)} but #{frag} is Q{tq.n}")
                    after = scan[m.end():]
                    tm = re.match(r"\s*—\s*(.+?)(?=\s+·\s+\[|$)", after)
                    if tm and not similar(tm.group(1), tq.title):
                        rep.error(where, f"link title '{tm.group(1)[:50]}' ≠ target '{tq.title[:50]}'")
                else:
                    lab = re.sub(r"^(⭐+|\((Easy|Medium|Hard)\))\s*", "", label.strip())
                    if len(lab.split()) >= 4 and not similar(lab, tq.title):
                        rep.error(where, f"link text '{lab[:50]}' ≠ target '{tq.title[:50]}'")

    # ---- question banks
    check_banks(questions, rep, in_scope)
    return rep.emit()


def check_banks(questions, rep, in_scope):
    # Link-style banks (Python, DRF, LangChain): every question listed once, nothing extra
    for stack in ("Python", "Django DRF", "LangChain LangGraph"):
        bank = ROOT / STACKS[stack]["bank"]
        qs = [q for q in questions if q.stack == stack]
        if not bank.exists() or not (in_scope(bank.relative_to(ROOT).as_posix()) or any(in_scope(q.file) for q in qs)):
            continue
        listed = set()
        for t in LINK_RE.findall(bank.read_text(encoding="utf-8")):
            tp, _, frag = t[1].partition("#")
            if frag:
                listed.add((_norm((bank.parent / unquote(tp)).relative_to(ROOT).as_posix()), frag))
        for q in qs:
            if (q.file, q.anchor) not in listed:
                rep.error(f"{bank.relative_to(ROOT)}", f"missing {q.file} {q.anchor}: {q.title[:60]}")
    # Title-list bank (Django ORM): module NN titles == short + long module titles
    bank = ROOT / "Django ORM" / "Question_Bank.md"
    if not bank.exists():
        return
    mods, cur = defaultdict(list), None
    for line in bank.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^## Module (\d+)", line)
        if m:
            cur = m.group(1); continue
        m = re.match(r"^\d+\.\s+(.+)$", line)
        if m and cur:
            mods[cur].append(norm_title(m.group(1)))
    for stack, severity in (("Django ORM Short", rep.error), ("Django ORM", rep.warn)):
        per = defaultdict(list)
        for q in questions:
            if q.stack == stack and in_scope(q.file):
                per[(q.file, Path(q.file).name[:2])].append(norm_title(q.title))
        for (f, mod), titles in per.items():
            want = mods.get(mod, [])
            if len(titles) != len(want):
                severity(f, f"{len(titles)} questions but Question_Bank module {mod} lists {len(want)}")
            for i, (got, exp) in enumerate(zip(titles, want), 1):
                if got != exp:
                    severity(f"{f} Q{i}", f"title differs from Question_Bank: '{got[:50]}' vs '{exp[:50]}'")


if __name__ == "__main__":
    sys.exit(main())
