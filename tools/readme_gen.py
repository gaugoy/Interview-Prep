"""Generate the live parts of the root README.md from the question index.

Called by tools/build_index.py (so hooks, pre-commit and manual runs all refresh it).
Updates only the blocks between markers — the rest of README.md is hand-written:

  <!-- AUTO:CONTENTS:START --> … END     section table with live question counts
  <!-- AUTO:GLANCE:START --> … END       totals by difficulty, asked-in-interview count
  questions-<N>-blue badge                 total-question badge in the header

The README only changes when counts change. "What changed" lives in GitHub Releases
(tools/release_notes.py + .github/workflows/release-notes.yml), linked from the README.
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

# One row per README section. `stacks` = catalog stacks counted for this row.
SECTIONS = [
    ("🐍", "Python", "Python/README.md", ["Python"], "Python",
     "Fundamentals, OOP, functional & decorators, concurrency (GIL, threads, multiprocessing, asyncio), memory & GC, DSA, data & AI, testing",
     "Theory-first, topic clusters"),
    ("🗄️", "Django ORM — Short", "Django ORM Short/README.md", ["Django ORM Short"], "Django ORM Short",
     "20 ORM modules: queries, optimization, transactions, migrations, multi-DB, concurrency, scaling, internals, Lead scenarios",
     "⚡ Quick-revision booklet"),
    ("📖", "Django ORM — Deep", "Django ORM/README.md", ["Django ORM"], "Django ORM",
     "The same 700+ questions with long answers: mechanics, SQL, trade-offs, scaling",
     "🔬 Deep dive (rewrite in progress)"),
    ("🔌", "Django REST Framework", "Django DRF/README.md", ["Django DRF"], "Django DRF",
     "Serializers, validation, views & ViewSets, auth/JWT, permissions, throttling, pagination, testing, production scenarios",
     "⚡ Quick revision"),
    ("🌱", "Django (compact)", "django/index.md", ["django"], "django",
     "Core Django, ORM and DRF essentials — the most-asked set",
     "⭐ Frequency-ranked"),
    ("⚛️", "React & Web", "React/00_INDEX.md", ["React"], "React",
     "React fundamentals, hooks, state, performance, architecture, testing, web fundamentals, JavaScript",
     "🚧 Restructure planned"),
    ("🦜", "LangChain & LangGraph", "LangChain LangGraph/README.md", ["LangChain LangGraph"], "LangChain LangGraph",
     "GenAI: LCEL, prompts, structured output, memory, RAG, tools & agents, LangGraph, checkpointing & HITL, multi-agent, LangSmith, production, system design",
     "🤖 GenAI, project-tied answers"),
]
STACK_LABEL = {s[4]: s[1] for s in SECTIONS}
STACK_LABEL["Django ORM"] = "Django ORM — Deep"


def _link(path: str) -> str:
    return "./" + quote(path)


def _block(name: str, body: str) -> tuple[str, str]:
    return f"<!-- AUTO:{name}:START -->", f"<!-- AUTO:{name}:START -->\n{body}\n<!-- AUTO:{name}:END -->"


def _replace(text: str, name: str, body: str) -> str:
    start, block = _block(name, body)
    end = f"<!-- AUTO:{name}:END -->"
    if start in text and end in text:
        pre, rest = text.split(start, 1)
        return pre + block + rest.split(end, 1)[1]
    return text  # markers missing → leave README untouched


def render_readme(questions) -> str | None:
    if not README.exists():
        return None
    text = README.read_text(encoding="utf-8")
    per_stack = Counter(q.stack for q in questions)
    live = [q for q in questions if q.stack in {s for sec in SECTIONS for s in sec[3]}]
    total = len(live)

    rows = ["| | Section | What it covers | Questions | Style |", "|---|---|---|---:|---|"]
    for emoji, title, link, stacks, folder, desc, style in SECTIONS:
        n = sum(per_stack[s] for s in stacks)
        rows.append(f"| {emoji} | [**{title}**]({_link(link)}) | {desc} | {n} | {style} |")
    rows.append("| 🎯 | **Company guides** | Focused crash plans & theory sheets (e.g. `Fractal_AI_*.md`) | — | Targeted prep |")
    contents = "\n".join(rows) + f"\n\n> 📊 **{total} questions** in total · per-file counts and difficulty mix: [`index/INDEX.md`](./index/INDEX.md)"

    lv = Counter(q.level for q in live)
    asked = sum(q.asked for q in live)
    untagged = f" · ⚪ {lv['unknown']} untagged" if lv["unknown"] else ""
    glance = (f"🟢 **{lv['easy']}** easy · 🟡 **{lv['medium']}** medium · 🔴 **{lv['hard']}** hard{untagged}"
              f" · ⭐ **{asked}** asked in my interviews")

    text = _replace(text, "CONTENTS", contents)
    text = _replace(text, "GLANCE", glance)
    text = re.sub(r"(img\.shields\.io/badge/questions-)\d+(-blue)", rf"\g<1>{total}\g<2>", text)
    return text
