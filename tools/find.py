#!/usr/bin/env python3
"""Find questions without reading whole files (cheap for humans and agents).

Examples:
  python3 tools/find.py select_related prefetch            # words, all stacks
  python3 tools/find.py gil --stack Python
  python3 tools/find.py --stack Python --thin               # answers that need theory
  python3 tools/find.py --asked                             # real interview questions
  python3 tools/find.py --id django-orm.06-query-optimization.ab12cd34
Prints: stack | file:line | anchor | level | title  (open just those lines to edit)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "index" / "catalog.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("words", nargs="*", help="all words must appear in the title (case-insensitive)")
    ap.add_argument("--stack"); ap.add_argument("--file"); ap.add_argument("--level")
    ap.add_argument("--id"); ap.add_argument("--thin", action="store_true")
    ap.add_argument("--asked", action="store_true"); ap.add_argument("--status")
    ap.add_argument("--limit", type=int, default=30)
    ap.add_argument("--json", action="store_true", help="print full records")
    a = ap.parse_args()

    if CATALOG.exists():
        records = json.loads(CATALOG.read_text(encoding="utf-8"))
    else:  # fall back to parsing live
        sys.path.insert(0, str(Path(__file__).parent))
        from catalog import load
        records = [q.to_json() for q in load()[0]]

    words = [w.lower() for w in a.words]
    hits = [r for r in records
            if all(w in r["title"].lower() for w in words)
            and (not a.stack or r["stack"].lower() == a.stack.lower())
            and (not a.file or a.file.lower() in r["file"].lower())
            and (not a.level or r["level"] == a.level.lower())
            and (not a.id or r["id"] == a.id)
            and (not a.thin or r["words"] < 45)
            and (not a.asked or r["asked"])
            and (not a.status or r["status"] == a.status)]
    for r in hits[: a.limit]:
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
        else:
            print(f"{r['stack']} | {r['file']}:{r['line_start']}-{r['line_end']} | {r['anchor'] or '-'} | {r['level']} | {r['title']}")
    if len(hits) > a.limit:
        print(f"... {len(hits) - a.limit} more (use --limit)")
    if not hits:
        print("no match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
