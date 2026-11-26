"""
In-memory content cache.

`ContentLibrary` owns the parsed state of the repo:
  * a cheap filesystem walk (`os.walk` + `stat`) finds files,
  * each file is parsed only when it is new or its mtime/size changed,
  * look-up dicts make every API call O(1).

The walk re-runs at most every `ttl` seconds when the API is hit, so new
files show up on a normal browser reload. `POST /api/rescan` forces a full
re-parse.

FastAPI runs plain `def` routes in a thread pool, so access is guarded by a
lock.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from pathlib import Path

from .parser import GENERAL_TOPIC, ParsedFile, ParsedQuestion, SourceFile, discover, parse_file


@dataclass
class _Snapshot:
    files: list[ParsedFile]
    by_key: dict[tuple[str, str], ParsedFile]  # (topic, name) -> file
    by_id: dict[str, tuple[ParsedFile, ParsedQuestion]]
    topics: list[str]


class ContentLibrary:
    def __init__(self, root: Path, ttl: float = 2.0) -> None:
        self.root = root.resolve()
        self.ttl = ttl
        self._lock = threading.Lock()
        self._parsed: dict[str, tuple[float, int, ParsedFile]] = {}  # rel_path -> (mtime, size, parsed)
        self._snapshot: _Snapshot | None = None
        self._last_walk = 0.0

    # ------------------------------------------------------------------ #
    def snapshot(self, force: bool = False) -> _Snapshot:
        """Return fresh-enough parsed content, refreshing if needed."""
        with self._lock:
            stale = time.monotonic() - self._last_walk > self.ttl
            if force or stale or self._snapshot is None:
                self._refresh(force)
            assert self._snapshot is not None
            return self._snapshot

    def _refresh(self, force: bool) -> None:
        if force:
            self._parsed.clear()

        sources = discover(self.root)
        parsed_files: list[ParsedFile] = []
        live: set[str] = set()

        for src in sources:
            live.add(src.rel_path)
            parsed_files.append(self._get_or_parse(src))

        # Forget files that were deleted from disk.
        for gone in set(self._parsed) - live:
            del self._parsed[gone]

        by_key = {(f.source.topic, f.source.name): f for f in parsed_files}
        by_id = {q.id: (f, q) for f in parsed_files for q in f.questions}
        topics = sorted({f.source.topic for f in parsed_files}, key=_topic_sort_key)

        self._snapshot = _Snapshot(parsed_files, by_key, by_id, topics)
        self._last_walk = time.monotonic()

    def _get_or_parse(self, src: SourceFile) -> ParsedFile:
        cached = self._parsed.get(src.rel_path)
        if cached and cached[0] == src.mtime and cached[1] == src.size:
            return cached[2]
        parsed = parse_file(src)
        self._parsed[src.rel_path] = (src.mtime, src.size, parsed)
        return parsed


def _topic_sort_key(name: str) -> tuple[int, str]:
    # Real folders alphabetically, the root-level "General" bucket last.
    return (1 if name == GENERAL_TOPIC else 0, name.lower())
