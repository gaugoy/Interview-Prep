"""
Interview Prep Viewer — FastAPI entry point.

Run from the repo root:

    pip install -r src/app/requirements.txt
    uvicorn src.app.main:app --reload
    # open http://localhost:8000   (API docs: http://localhost:8000/docs)

The app is READ-ONLY with respect to the markdown content. It scans the repo,
parses questions in memory and serves JSON + a static single-page frontend.

Learning notes:
  * Routes are plain `def` (not `async def`) because they do blocking file
    I/O; FastAPI runs them in a thread pool automatically.
  * `response_model=` makes FastAPI validate and document each response.
  * `Query(...)` declares query-string params; FastAPI URL-decodes them, so
    "Django%20ORM" arrives as "Django ORM".
"""

from __future__ import annotations

import os
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .comments import append_comment
from .library import ContentLibrary
from .models import (
    CommentRequest,
    CommentResponse,
    FileDetail,
    FileStat,
    FileSummary,
    Note,
    QuestionDetail,
    QuestionSummary,
    RescanResult,
    Stats,
    TocEntry,
    TopicSummary,
)
from .parser import ParsedFile, ParsedQuestion, file_label, slugify

# --------------------------------------------------------------------------- #
# Setup
# --------------------------------------------------------------------------- #

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
# Content root = repo root (src/app/ -> src/ -> repo). Override with an env var.
CONTENT_ROOT = Path(os.environ.get("PREP_CONTENT_ROOT", APP_DIR.parents[1]))

library = ContentLibrary(CONTENT_ROOT)

app = FastAPI(
    title="Interview Prep Viewer",
    description="Read-only viewer for the markdown interview question banks.",
    version="1.0.0",
)


# --------------------------------------------------------------------------- #
# Converters: internal dataclasses -> Pydantic response models
# --------------------------------------------------------------------------- #


def _file_summary(f: ParsedFile) -> FileSummary:
    return FileSummary(
        topic=f.source.topic,
        name=f.source.name,
        label=file_label(f.source.name),
        path=f.source.rel_path,
        format=f.format,
        title=f.title,
        question_count=len(f.questions),
        size=f.source.size,
    )


def _question_summary(f: ParsedFile, q: ParsedQuestion) -> QuestionSummary:
    return QuestionSummary(
        id=q.id,
        index=q.index,
        title=q.title,
        difficulty=q.difficulty,
        section=q.section,
        anchor=q.anchor,
        topic=f.source.topic,
        file=f.source.name,
    )


def _question_detail(f: ParsedFile, q: ParsedQuestion) -> QuestionDetail:
    return QuestionDetail(
        **_question_summary(f, q).model_dump(),
        markdown=q.markdown,
        line_start=q.line_start,
        line_end=q.line_end,
    )


def _require_file(topic: str, file: str) -> ParsedFile:
    found = library.snapshot().by_key.get((topic, file))
    if found is None:
        raise HTTPException(status_code=404, detail=f"No file {file!r} in topic {topic!r}")
    return found


# --------------------------------------------------------------------------- #
# API routes
# --------------------------------------------------------------------------- #


@app.get("/api/topics", response_model=list[TopicSummary], tags=["content"])
def list_topics() -> list[TopicSummary]:
    """All topics with their files and question counts (drives the sidebar)."""
    snap = library.snapshot()
    result: list[TopicSummary] = []
    for topic in snap.topics:
        files = [_file_summary(f) for f in snap.files if f.source.topic == topic]
        result.append(
            TopicSummary(
                name=topic,
                slug=slugify(topic),
                file_count=len(files),
                question_count=sum(f.question_count for f in files),
                files=files,
            )
        )
    return result


@app.get("/api/files", response_model=list[FileSummary], tags=["content"])
def list_files(topic: str = Query(..., description="Topic name, e.g. 'Django ORM'")) -> list[FileSummary]:
    snap = library.snapshot()
    if topic not in snap.topics:
        raise HTTPException(status_code=404, detail=f"Unknown topic {topic!r}")
    return [_file_summary(f) for f in snap.files if f.source.topic == topic]


@app.get("/api/questions", response_model=list[QuestionSummary], tags=["content"])
def list_questions(
    topic: str | None = Query(None, description="Limit to one topic (omit for all)"),
    file: str | None = Query(None, description="Limit to one file (needs topic)"),
) -> list[QuestionSummary]:
    """Short question list (no answers). Used for the index and for search."""
    snap = library.snapshot()
    if file is not None:
        if topic is None:
            raise HTTPException(status_code=422, detail="'file' requires 'topic'")
        files = [_require_file(topic, file)]
    elif topic is not None:
        if topic not in snap.topics:
            raise HTTPException(status_code=404, detail=f"Unknown topic {topic!r}")
        files = [f for f in snap.files if f.source.topic == topic]
    else:
        files = snap.files
    return [_question_summary(f, q) for f in files for q in f.questions]


@app.get("/api/file", response_model=FileDetail, tags=["content"])
def get_file(topic: str = Query(...), file: str = Query(...)) -> FileDetail:
    """One file with every question's raw markdown — one request per page view."""
    f = _require_file(topic, file)
    return FileDetail(
        **_file_summary(f).model_dump(),
        intro_markdown=f.intro_markdown,
        questions=[_question_detail(f, q) for q in f.questions],
        toc=[TocEntry(level=t.level, title=t.title, anchor=t.anchor) for t in f.toc],
        notes=[Note(after=n.after, title=n.title, anchor=n.anchor, markdown=n.markdown) for n in f.notes],
        error=f.error,
    )


@app.get("/api/question/{question_id}", response_model=QuestionDetail, tags=["content"])
def get_question(question_id: str) -> QuestionDetail:
    hit = library.snapshot().by_id.get(question_id)
    if hit is None:
        raise HTTPException(status_code=404, detail="Unknown question id")
    return _question_detail(*hit)


@app.get("/api/stats", response_model=Stats, tags=["content"])
def get_stats() -> Stats:
    """Totals + every question id per file, so the browser can compute coverage."""
    snap = library.snapshot()
    return Stats(
        topic_count=len(snap.topics),
        file_count=len(snap.files),
        question_count=len(snap.by_id),
        files=[
            FileStat(topic=f.source.topic, name=f.source.name, question_ids=[q.id for q in f.questions])
            for f in snap.files
        ],
    )


@app.post("/api/rescan", response_model=RescanResult, tags=["admin"])
def rescan() -> RescanResult:
    """Drop the cache and re-parse every file from disk."""
    started = time.perf_counter()
    snap = library.snapshot(force=True)
    return RescanResult(
        topic_count=len(snap.topics),
        file_count=len(snap.files),
        question_count=len(snap.by_id),
        seconds=round(time.perf_counter() - started, 3),
    )


@app.post("/api/comment", response_model=CommentResponse, status_code=501, tags=["future"])
def add_comment(request: CommentRequest) -> CommentResponse:
    """STUB — TODO: append the comment into the source file (see comments.py)."""
    if request.question_id not in library.snapshot().by_id:
        raise HTTPException(status_code=404, detail="Unknown question id")
    try:
        append_comment(library, request)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc)) from exc
    return CommentResponse(ok=True, detail="saved")  # unreachable until implemented


# --------------------------------------------------------------------------- #
# Frontend (static files)
# --------------------------------------------------------------------------- #

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
