"""
Pydantic models = the shape of every JSON response.

FastAPI uses these in two ways:
  * `response_model=...` on a route validates/serialises what we return, and
  * they show up automatically in the interactive docs at /docs.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

FileFormat = Literal["deep", "compact", "document"]


class QuestionSummary(BaseModel):
    """Light-weight question info for indexes and search results."""

    id: str = Field(description="Stable id, used as the localStorage key for coverage")
    index: int
    title: str
    difficulty: int = Field(ge=0, le=5, description="0 = unknown, else 1..5")
    section: str | None = None
    anchor: str = Field(description="DOM id to scroll to on the file page")
    topic: str
    file: str


class QuestionDetail(QuestionSummary):
    """A question plus its raw markdown answer (rendered in the browser)."""

    markdown: str
    line_start: int
    line_end: int


class TocEntry(BaseModel):
    level: int
    title: str
    anchor: str


class Note(BaseModel):
    """Non-question content shown between questions (not checkable)."""

    after: int = Field(description="Render after this many questions")
    title: str
    anchor: str
    markdown: str


class FileSummary(BaseModel):
    topic: str
    name: str = Field(description="Path relative to the topic folder")
    label: str = Field(description="Human friendly name for the sidebar")
    path: str = Field(description="Path relative to the content root")
    format: FileFormat
    title: str
    question_count: int
    size: int


class FileDetail(FileSummary):
    intro_markdown: str
    questions: list[QuestionDetail]
    toc: list[TocEntry]
    notes: list[Note]
    error: str | None = None


class TopicSummary(BaseModel):
    name: str
    slug: str
    file_count: int
    question_count: int
    files: list[FileSummary]


class FileStat(BaseModel):
    topic: str
    name: str
    question_ids: list[str]


class Stats(BaseModel):
    """Totals for the dashboard. Coverage itself lives only in the browser,
    so we ship the question ids and let the frontend intersect them with its
    localStorage ticks."""

    topic_count: int
    file_count: int
    question_count: int
    files: list[FileStat]


class RescanResult(BaseModel):
    topic_count: int
    file_count: int
    question_count: int
    seconds: float


class CommentRequest(BaseModel):
    """Payload for the (future) comment feature."""

    question_id: str
    text: str = Field(min_length=1, max_length=5000)


class CommentResponse(BaseModel):
    ok: bool
    detail: str
