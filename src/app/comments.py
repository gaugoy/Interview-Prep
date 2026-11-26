"""
FUTURE HOOK — writing comments back into the source markdown.

Nothing here writes to disk yet. The viewer is READ-ONLY today.

Plan for when this is implemented:
  1. Look up the question by id in the ContentLibrary snapshot. Each
     ParsedQuestion already carries `line_start` / `line_end` (1-based,
     inclusive), which mark exactly where its answer ends in the file.
  2. Re-read the file and confirm its mtime/size still match the snapshot
     (refuse with 409 Conflict if it changed, so we never clobber edits).
  3. Insert a block such as

        > 💬 **Comment (2026-11-26):** <text>

     right after `line_end`, write to a temp file and `os.replace()` it in
     (atomic), then call `library.snapshot(force=True)`.
"""

from __future__ import annotations

from .library import ContentLibrary
from .models import CommentRequest


def append_comment(library: ContentLibrary, request: CommentRequest) -> None:
    # TODO: implement the steps in the module docstring.
    raise NotImplementedError("Comments are not implemented yet — the viewer is read-only.")
