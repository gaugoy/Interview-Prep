# tools/ — index & validation for the question banks

Pure standard-library Python (3.10+). They reuse the viewer's parser (`src/app/parser.py`), so the
tools, the FastAPI app and the agent all see the same questions and the same stable ids.

| Command | What it does | When |
|---|---|---|
| `python3 tools/find.py <words> [--stack X] [--file F] [--level hard] [--thin] [--asked]` | Search question titles via `index/catalog.json`; prints `file:line` to open just that block | Before adding (duplicate check) or editing |
| `python3 tools/build_index.py` | Regenerates `index/catalog.json`, `index/INDEX.md` and the live-counts block in `AGENT_INDEX.md` | After content changes (hooks run it) |
| `python3 tools/build_index.py --check` | Fails if the generated files are stale; lists question ids that disappeared (title edits) | CI / pre-commit |
| `python3 tools/validate.py [--file F] [--changed] [--strict]` | Anchors, `**Answer:**`, python code parse, link + anchor existence, link-title drift, question-bank sync, duplicate titles | After every edit (hooks), before commit |

**Per-stack rules** live in one place: `STACKS` in `tools/catalog.py` (anchors required? `**Answer:**`
required? code errors or warnings? which bank? default review status). Add a new stack there.

**Automation**
- Claude Code hooks (`.claude/settings.json`): after an Edit/Write of a content `.md` →
  `tools/hooks/post_edit.py` validates that file and feeds errors back to the agent; on Stop →
  `tools/hooks/on_stop.py` rebuilds the index and validates changed files.
- Git: `git config core.hooksPath .githooks` enables `.githooks/pre-commit` (rebuild index + validate).
- CI: `.github/workflows/content-checks.yml` runs `build_index.py --check` and `validate.py`.

**Warnings vs errors:** errors block (hooks, commit, CI). Warnings are known content debt, e.g. broken
code in the templated `Django ORM/` modules — they disappear as modules are rewritten.

**Ids:** `<topic>.<file>.<hash(title)>` — survives renumbering; editing a title creates a new id
(the viewer's coverage tick for it resets; `build_index.py --check` lists such ids).
