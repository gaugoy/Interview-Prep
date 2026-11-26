"""
Markdown discovery + parsing for the Interview Prep Viewer.

This module is deliberately *pure*: no FastAPI imports, no global state.
It only knows how to
  1. find `.md` files under a content root   -> `discover()`
  2. turn one file into questions             -> `parse_file()`

Everything is plain Python (regex + line splitting). We never render markdown
here — the browser does that with `marked` + `highlight.js`. We only need to
know where headings are so we can cut a file into questions.

Supported layouts (checked in this order):

* DEEP     – blocks that start with a level-1 heading `# Question`; the question
             text is the paragraph(s) right after it, and everything up to the
             next `# Question` is the answer (Django ORM/*.md).
* COMPACT  – a heading like `## Q12. ⭐⭐ Title`, `## Q3. (Hard) Title`,
             `### Q4. Title` or `### Q: Title`; the answer runs until the next
             question heading or a heading of a *higher* level (a new section).
* DOCUMENT – anything else: shown as one document with a heading-based TOC.

Stable ids: a question id is `<topic-slug>.<file-slug>.<hash>` where the hash
comes from the normalised question *title* (the `Q<n>.` prefix and stars are
stripped first). Reordering or inserting questions therefore never changes the
ids of existing ones, so the browser's saved checkboxes keep working.
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

# --------------------------------------------------------------------------- #
# Discovery configuration
# --------------------------------------------------------------------------- #

#: Directories skipped anywhere in the tree (plus every dot-directory).
EXCLUDED_DIRS = {"node_modules", "__pycache__", "venv", ".venv", "env"}
#: Directories skipped only at the content root.
EXCLUDED_ROOT_DIRS = {"src", "tools", "prompts", "index"}  # code + agent/index files, not content
#: Meta files at the content root that are not interview content.
EXCLUDED_ROOT_FILES = {"CLAUDE.md", "AGENT_INDEX.md", "PROMPTS.md", "README.md"}
#: Topic name used for `.md` files that live directly in the root.
GENERAL_TOPIC = "General"

FileFormat = Literal["deep", "compact", "document"]


@dataclass(frozen=True)
class SourceFile:
    """A markdown file found on disk (not parsed yet)."""

    topic: str  # top-level folder name, or GENERAL_TOPIC
    name: str  # path relative to the topic folder, posix style ("08_Transactions.md")
    rel_path: str  # path relative to the content root, posix style
    abs_path: Path
    mtime: float
    size: int


@dataclass
class ParsedQuestion:
    id: str
    index: int  # 1-based position in the file
    title: str
    difficulty: int  # 0 = unknown, 1..5 (stars / easy=1, medium=2, hard=3)
    section: str | None  # enclosing section heading, e.g. "🟡 Medium"
    anchor: str  # DOM id used for "jump to answer"
    markdown: str  # raw answer markdown (without the question heading)
    line_start: int  # 1-based, inclusive — first line of the question heading
    line_end: int  # 1-based, inclusive — last line of the answer
    # line_start/line_end are kept for the future "append comment" feature.


@dataclass
class TocEntry:
    level: int
    title: str
    anchor: str


@dataclass
class Note:
    """Non-question content inside a question file (e.g. a "Bonus: Gotchas"
    section). Rendered in place but not counted for coverage."""

    after: int  # number of questions that come before this note
    title: str
    anchor: str
    markdown: str


@dataclass
class ParsedFile:
    source: SourceFile
    format: FileFormat
    title: str
    intro_markdown: str
    questions: list[ParsedQuestion] = field(default_factory=list)
    toc: list[TocEntry] = field(default_factory=list)
    notes: list[Note] = field(default_factory=list)
    error: str | None = None


# --------------------------------------------------------------------------- #
# Small helpers
# --------------------------------------------------------------------------- #


def slugify(text: str) -> str:
    """'Django ORM' -> 'django-orm'. Keeps ids URL- and DOM-safe."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "x"


def short_hash(text: str) -> str:
    normalised = re.sub(r"\s+", " ", text.lower()).strip()
    return hashlib.sha1(normalised.encode("utf-8")).hexdigest()[:8]


def file_label(name: str) -> str:
    """'08_Transactions.md' -> '08 Transactions' (for the sidebar)."""
    stem = name.rsplit("/", 1)[-1]
    stem = re.sub(r"\.md$", "", stem, flags=re.I)
    return stem.replace("_", " ").strip()


def natural_key(text: str) -> list[object]:
    """Sort '2_x' before '10_x'."""
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", text)]


# --------------------------------------------------------------------------- #
# 1. Discovery
# --------------------------------------------------------------------------- #


def discover(root: Path) -> list[SourceFile]:
    """Recursively list every interview `.md` file under `root`."""
    found: list[SourceFile] = []
    root = root.resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        here = Path(dirpath)
        at_root = here == root

        # Prune in place so os.walk never descends into excluded folders.
        dirnames[:] = [
            d
            for d in dirnames
            if not d.startswith(".")
            and d not in EXCLUDED_DIRS
            and not (at_root and d in EXCLUDED_ROOT_DIRS)
        ]

        for filename in filenames:
            if not filename.lower().endswith(".md"):
                continue
            if at_root and filename in EXCLUDED_ROOT_FILES:
                continue

            abs_path = here / filename
            rel = abs_path.relative_to(root).as_posix()
            parts = rel.split("/")
            if len(parts) == 1:
                topic, name = GENERAL_TOPIC, rel
            else:
                topic, name = parts[0], "/".join(parts[1:])

            try:
                stat = abs_path.stat()
            except OSError:
                continue  # file vanished mid-scan — just skip it
            found.append(
                SourceFile(topic, name, rel, abs_path, stat.st_mtime, stat.st_size)
            )

    found.sort(key=lambda s: (natural_key(s.topic), natural_key(s.name)))
    return found


# --------------------------------------------------------------------------- #
# 2. Heading scanner (code-fence aware)
# --------------------------------------------------------------------------- #

_FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)(?:\s+#+)?\s*$")


@dataclass
class _Heading:
    line: int  # 0-based index into `lines`
    level: int
    text: str


def _scan_headings(lines: list[str]) -> list[_Heading]:
    """Return ATX headings that are *not* inside fenced code blocks.

    Without this, `# models.py` inside a ```python block would look like an H1.
    """
    headings: list[_Heading] = []
    fence_char: str | None = None
    fence_len = 0

    for i, line in enumerate(lines):
        fence = _FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_char is None:
                fence_char, fence_len = marker[0], len(marker)
            elif (
                marker[0] == fence_char
                and len(marker) >= fence_len
                and line.strip().strip(fence_char) == ""
            ):
                fence_char = None
            continue
        if fence_char is not None:
            continue

        m = _HEADING_RE.match(line)
        if m:
            headings.append(_Heading(i, len(m.group(1)), m.group(2).strip()))
    return headings


def _trim_block(lines: list[str]) -> list[str]:
    """Drop leading blank lines and trailing blank / `---` separator lines."""
    start, end = 0, len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and lines[end - 1].strip() in ("", "---", "***", "___"):
        end -= 1
    return lines[start:end]


# --------------------------------------------------------------------------- #
# 3. Difficulty + title helpers
# --------------------------------------------------------------------------- #

_LEVEL_WORDS = {"easy": 1, "medium": 2, "hard": 3}
_LEVEL_EMOJI = {"🟢": 1, "🟡": 2, "🔴": 3}
_PAREN_LEVEL_RE = re.compile(r"[\(\[]\s*(easy|medium|hard)\s*[\)\]]", re.I)
_COMPACT_Q_RE = re.compile(r"^Q(?:\s*(\d+))?\s*[.:)]\s*(.+)$")


def _difficulty_from_text(text: str, *, allow_bare_words: bool = False) -> int:
    stars = text.count("⭐")
    if stars:
        return min(stars, 5)
    m = _PAREN_LEVEL_RE.search(text)
    if m:
        return _LEVEL_WORDS[m.group(1).lower()]
    for emoji, level in _LEVEL_EMOJI.items():
        if emoji in text:
            return level
    if allow_bare_words:  # section headings such as "## Medium"
        for word, level in _LEVEL_WORDS.items():
            if re.search(rf"\b{word}\b", text, re.I):
                return level
    return 0


def _clean_title(text: str) -> str:
    text = text.replace("⭐", "")
    text = _PAREN_LEVEL_RE.sub("", text)
    for emoji in _LEVEL_EMOJI:
        text = text.replace(emoji, "")
    return re.sub(r"\s+", " ", text).strip(" -–—:")


class _IdMaker:
    """Builds stable, unique ids/anchors for the questions of one file."""

    def __init__(self, source: SourceFile) -> None:
        stem = re.sub(r"\.md$", "", source.name, flags=re.I)
        self.prefix = f"{slugify(source.topic)}.{slugify(stem)}"
        self.seen: dict[str, int] = {}

    def make(self, title: str) -> tuple[str, str]:
        h = short_hash(title)
        count = self.seen.get(h, 0) + 1
        self.seen[h] = count
        suffix = "" if count == 1 else f"-{count}"  # duplicate titles in one file
        return f"{self.prefix}.{h}{suffix}", f"q-{h}{suffix}"


# --------------------------------------------------------------------------- #
# 4. Format parsers
# --------------------------------------------------------------------------- #


def _first_title(headings: list[_Heading], fallback: str) -> str:
    for h in headings:
        if h.level == 1:
            return h.text
    return headings[0].text if headings else fallback


def _parse_deep(
    source: SourceFile, lines: list[str], headings: list[_Heading]
) -> ParsedFile | None:
    starts = [h for h in headings if h.level == 1 and h.text.lower().rstrip(":") == "question"]
    if not starts:
        return None

    ids = _IdMaker(source)
    questions: list[ParsedQuestion] = []
    heading_lines = sorted(h.line for h in headings)

    for idx, start in enumerate(starts):
        block_end = starts[idx + 1].line if idx + 1 < len(starts) else len(lines)
        # The question text runs from after "# Question" to the next heading.
        next_heading = next((ln for ln in heading_lines if ln > start.line), block_end)
        answer_start = min(next_heading, block_end)

        title_lines = [ln.strip() for ln in lines[start.line + 1 : answer_start] if ln.strip()]
        title = " ".join(title_lines) or f"Question {idx + 1}"
        body = _trim_block(lines[answer_start:block_end])

        qid, anchor = ids.make(title)
        questions.append(
            ParsedQuestion(
                id=qid,
                index=idx + 1,
                title=title,
                difficulty=_difficulty_from_text(title),
                section=None,
                anchor=anchor,
                markdown="\n".join(body),
                line_start=start.line + 1,
                line_end=start.line + 1 + _last_content_offset(lines, start.line, block_end),
            )
        )

    intro_headings = [h for h in headings if h.line < starts[0].line]
    return ParsedFile(
        source=source,
        format="deep",
        title=_first_title(intro_headings, file_label(source.name)),
        intro_markdown="\n".join(_trim_block(lines[: starts[0].line])),
        questions=questions,
    )


def _parse_compact(
    source: SourceFile, lines: list[str], headings: list[_Heading]
) -> ParsedFile | None:
    # Which headings are questions? Level 2-4 headings shaped like "Q<n>. ..." or "Q: ...".
    q_headings: list[tuple[_Heading, re.Match[str]]] = []
    for h in headings:
        if 2 <= h.level <= 4:
            m = _COMPACT_Q_RE.match(h.text)
            if m:
                q_headings.append((h, m))
    if not q_headings:
        return None

    ids = _IdMaker(source)
    questions: list[ParsedQuestion] = []
    q_line_set = {h.line for h, _ in q_headings}
    spans: list[tuple[int, int]] = []  # (heading line, end-exclusive) per question

    for idx, (h, m) in enumerate(q_headings):
        # Answer ends at the next question heading, or at any heading of a
        # higher level (e.g. "## 🔴 Hard" closes a "### Q7." answer).
        end = len(lines)
        for other in headings:
            if other.line <= h.line:
                continue
            if other.line in q_line_set or other.level < h.level:
                end = other.line
                break

        # Enclosing section = nearest previous heading with a higher level.
        section_heading = next(
            (o for o in reversed(headings) if o.line < h.line and o.level < h.level and o.level > 1),
            None,
        )
        section = section_heading.text if section_heading else None

        raw_title = m.group(2)
        difficulty = _difficulty_from_text(raw_title)
        if not difficulty and section:
            difficulty = _difficulty_from_text(section, allow_bare_words=True)

        title = _clean_title(raw_title) or f"Question {idx + 1}"
        qid, anchor = ids.make(title)
        body = _trim_block(lines[h.line + 1 : end])
        spans.append((h.line, end))
        questions.append(
            ParsedQuestion(
                id=qid,
                index=idx + 1,
                title=title,
                difficulty=difficulty,
                section=section,
                anchor=anchor,
                markdown="\n".join(body),
                line_start=h.line + 1,
                line_end=h.line + 1 + _last_content_offset(lines, h.line, end),
            )
        )

    first = q_headings[0][0].line
    intro_headings = [h for h in headings if h.line < first]
    return ParsedFile(
        source=source,
        format="compact",
        title=_first_title(intro_headings, file_label(source.name)),
        intro_markdown="\n".join(_trim_block(lines[:first])),
        questions=questions,
        notes=_collect_notes(lines, headings, spans),
    )


def _collect_notes(
    lines: list[str], headings: list[_Heading], spans: list[tuple[int, int]]
) -> list[Note]:
    """Keep content that sits between/after questions so nothing is hidden.

    Gaps that are only headings (section titles such as "## 🟡 Medium") are
    skipped — those already appear as each question's `section`.
    """
    heading_at = {h.line: h for h in headings}
    notes: list[Note] = []
    for i, (_, end) in enumerate(spans):
        gap_end = spans[i + 1][0] if i + 1 < len(spans) else len(lines)
        gap = _trim_block(lines[end:gap_end])
        has_body = any(
            ln.strip() and (end + j) not in heading_at for j, ln in enumerate(lines[end:gap_end])
            if ln.strip() not in ("---", "***", "___")
        )
        if not gap or not has_body:
            continue
        first_heading = next((heading_at[n] for n in range(end, gap_end) if n in heading_at), None)
        title = first_heading.text if first_heading else "Notes"
        notes.append(Note(after=i + 1, title=title, anchor=f"note-{i + 1}", markdown="\n".join(gap)))
    return notes


def _parse_document(
    source: SourceFile, lines: list[str], headings: list[_Heading], error: str | None = None
) -> ParsedFile:
    toc = [
        TocEntry(level=h.level, title=h.text, anchor=f"h-{i}-{slugify(h.text)[:40]}")
        for i, h in enumerate(headings)
        if h.level <= 3
    ]
    title = _first_title(headings, file_label(source.name))
    ids = _IdMaker(source)
    qid, _ = ids.make("__document__")
    # A whole document counts as ONE checkable item so coverage stays uniform.
    doc = ParsedQuestion(
        id=qid,
        index=1,
        title=title,
        difficulty=0,
        section=None,
        anchor="doc",
        markdown="\n".join(lines),
        line_start=1,
        line_end=len(lines),
    )
    return ParsedFile(
        source=source,
        format="document",
        title=title,
        intro_markdown="",
        questions=[doc],
        toc=toc,
        error=error,
    )


def _last_content_offset(lines: list[str], start: int, end: int) -> int:
    """Offset (from `start`) of the last non-separator line in [start, end)."""
    last = start
    for i in range(start, end):
        if lines[i].strip() not in ("", "---", "***", "___"):
            last = i
    return last - start


# --------------------------------------------------------------------------- #
# 5. Public entry point
# --------------------------------------------------------------------------- #


def parse_file(source: SourceFile) -> ParsedFile:
    """Parse one file. Never raises: odd files degrade to DOCUMENT format."""
    try:
        text = source.abs_path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return _parse_document(source, [f"> ⚠️ Could not read file: `{exc}`"], [], str(exc))

    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    try:
        headings = _scan_headings(lines)
        return (
            _parse_deep(source, lines, headings)
            or _parse_compact(source, lines, headings)
            or _parse_document(source, lines, headings)
        )
    except Exception as exc:  # noqa: BLE001 — a bad file must never crash the app
        return _parse_document(source, lines, [], f"parser error: {exc}")
