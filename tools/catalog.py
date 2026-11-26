"""Shared catalog loader for the content tools.

Reuses the viewer's parser (`src/app/parser.py`) so the tools, the FastAPI app and the
agent all see the *same* questions with the *same* stable ids (title hash — survives
renumbering; editing a title creates a new id).

Pure standard library: runs in CI without installing FastAPI.
"""
from __future__ import annotations

import hashlib
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.app.parser import discover, parse_file  # noqa: E402

# --------------------------------------------------------------------------- #
# Per-stack configuration — the ONE place that says how each folder is checked.
# --------------------------------------------------------------------------- #
#   anchors:  every question must have `<a name="qN">` matching its position
#   answer:   every question must contain `**Answer:**`
#   code:     "error" | "warn" | "off" — ```python blocks must parse
#   bank:     question-bank file whose titles must match the content files
#   status:   default review status for questions in this stack
STACKS: dict[str, dict] = {
    "Python":           {"prompt": "prompts/04_python.md",       "anchors": True,  "answer": True,  "code": "error", "bank": "Python/Question_Bank.md",     "status": "reviewed"},
    "Django DRF":       {"prompt": "prompts/03_drf.md",          "anchors": True,  "answer": True,  "code": "error", "bank": "Django DRF/Question_Bank.md", "status": "reviewed"},
    "Django ORM Short": {"prompt": "prompts/02_django_short.md", "anchors": True,  "answer": True,  "code": "error", "bank": "Django ORM/Question_Bank.md", "status": "reviewed"},
    "Django ORM":       {"prompt": "prompts/01_django_long.md",  "anchors": False, "answer": False, "code": "warn",  "bank": "Django ORM/Question_Bank.md", "status": "draft"},
    "django":           {"prompt": "prompts/01_django_long.md",  "anchors": True,  "answer": True,  "code": "warn",  "bank": None,                          "status": "draft"},
    "React":            {"prompt": "prompts/05_react.md",        "anchors": False, "answer": False, "code": "off",   "bank": None,                          "status": "draft"},
}
#: files reviewed to the stack's standard even though the stack default is "draft"
REVIEWED_FILES = {"Django ORM/06_Query_Optimization.md"}
#: files / folders that are not question content (indexes, READMEs, banks)
META_NAMES = {"README.md", "Question_Bank.md", "index.md", "00_INDEX.md"}
#: root-level files that are content-adjacent and should be link-checked
LINK_CHECK_ROOT_FILES = ["README.md", "PROMPTS.md", "AGENT_INDEX.md", "CLAUDE.md", "My_Interview_Questions.md"]

ANCHOR_RE = re.compile(r'^<a name="(q\d+)"></a>\s*$')
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")
ASKED_MARK = "⭐ Asked in my interview"
ASKED_RE = re.compile(r"⭐?\s*Asked in my interview", re.I)
LEVELS = {1: "easy", 2: "medium", 3: "hard", 4: "hard", 5: "hard"}


@dataclass
class Question:
    id: str
    stack: str
    file: str            # path relative to repo root
    n: int               # 1-based position in the file
    title: str
    level: str           # easy | medium | hard | unknown
    stars: int           # raw difficulty (stars for DRF/django, 1-3 otherwise)
    section: str | None
    anchor: str | None   # "q12" if the file has explicit anchors
    line_start: int
    line_end: int
    asked: bool
    status: str
    words: int           # prose words (outside code fences)
    code_lines: int
    hash: str            # content hash of the answer (detects "updated" in release notes)
    links: list[str] = field(default_factory=list)   # raw link targets inside the answer
    related: list[str] = field(default_factory=list)  # resolved question ids

    def to_json(self) -> dict:
        d = self.__dict__.copy()
        d.pop("links")
        return d


def strip_code(md: str) -> tuple[str, int]:
    code = re.findall(r"```.*?```", md, flags=re.S)
    prose = re.sub(r"```.*?```", "", md, flags=re.S)
    return prose, sum(c.count("\n") - 1 for c in code)


def load(root: Path = ROOT) -> tuple[list[Question], dict[str, object]]:
    """Parse every content file. Returns (questions, parsed_files_by_relpath)."""
    questions: list[Question] = []
    files: dict[str, object] = {}
    for src in discover(root):
        if src.topic not in STACKS or src.name.split("/")[-1] in META_NAMES:
            continue
        pf = parse_file(src)
        files[src.rel_path] = pf
        lines = src.abs_path.read_text(encoding="utf-8").split("\n")
        cfg = STACKS[src.topic]
        for q in pf.questions:
            prev = lines[q.line_start - 2] if q.line_start >= 2 else ""
            m = ANCHOR_RE.match(prev.strip())
            prose, code_lines = strip_code(q.markdown)
            status = "reviewed" if src.rel_path in REVIEWED_FILES else cfg["status"]
            raw = lines[q.line_start - 1] if q.line_start >= 1 else ""
            tag = re.search(r"\((Easy|Medium|Hard)\)", raw)
            level = tag.group(1).lower() if tag else LEVELS.get(q.difficulty, "unknown")
            questions.append(Question(
                id=q.id, stack=src.topic, file=src.rel_path, n=q.index, title=q.title,
                level=level, stars=q.difficulty, section=q.section,
                anchor=m.group(1) if m else None, line_start=q.line_start, line_end=q.line_end,
                asked=bool(ASKED_RE.search(q.title)), status=status,
                words=len(re.findall(r"\w+", prose)), code_lines=code_lines,
                hash=hashlib.sha1(q.markdown.strip().encode()).hexdigest()[:12],
                links=[t for _, t in LINK_RE.findall(q.markdown)],
            ))
    _resolve_related(questions)
    return questions, files


def _resolve_related(questions: list[Question]) -> None:
    by_anchor = {(q.file, q.anchor): q.id for q in questions if q.anchor}
    for q in questions:
        base = Path(q.file).parent
        for target in q.links:
            path, _, frag = target.partition("#")
            if not frag.startswith("q") or path.startswith(("http:", "https:")):
                continue
            tfile = q.file if not path else (base / unquote(path)).as_posix()
            tfile = str(Path(tfile).as_posix())
            tfile = _norm(tfile)
            rid = by_anchor.get((tfile, frag))
            if rid and rid != q.id and rid not in q.related:
                q.related.append(rid)


def _norm(p: str) -> str:
    parts: list[str] = []
    for part in p.split("/"):
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return "/".join(parts)


def norm_title(t: str) -> str:
    t = ASKED_RE.sub("", t)
    t = re.sub(r"^\((Easy|Medium|Hard)\)\s*", "", t)
    t = re.sub(r"[`*_]", "", t)
    return re.sub(r"\s+", " ", t).strip().lower()


def similar(a: str, b: str, threshold: float = 0.6) -> bool:
    """Loose title match for links/TOCs (labels are often shortened)."""
    x, y = set(re.findall(r"\w+", norm_title(a))), set(re.findall(r"\w+", norm_title(b)))
    if not x or not y:
        return True
    return len(x & y) / len(x | y) >= threshold or x <= y or y <= x
