# Interview Prep Viewer

A small, read-only web app for browsing the repo's markdown question banks and tracking which questions you've covered. It uses FastAPI with vanilla JS. There is no Node, no build step and no database.

## Run

From the **repo root**:

```bash
pip install -r src/app/requirements.txt
uvicorn src.app.main:app --reload
# open http://localhost:8000          (interactive API docs: http://localhost:8000/docs)
```

You can also run `./run.sh`, which does the same thing.

## What it does

- **Auto-discovery.** The app scans every `.md` under the repo root and skips `src/`, dot-folders, and the root meta files (`CLAUDE.md`, `AGENT_INDEX.md`, `PROMPTS.md`, `README.md`). Each top-level folder becomes a topic, and root-level files go under **General**. New or changed files show up when you reload the page. To force a full re-parse, use the ⟳ button (`POST /api/rescan`).
- **Parsing** (`parser.py`) uses plain regex and line splitting, and skips anything inside code fences.
  - **Deep**: blocks starting with `# Question` (Django ORM).
  - **Compact**: headings like `## Q3. ⭐⭐ Title`, `## Q3. (Hard) Title`, `### Q3. Title` under `## 🟡 Medium`, or `### Q: Title`. Content between questions that isn't a question (e.g. "Bonus: gotchas", a coding section) is kept and shown as a 📎 note.
  - **Document**: everything else is shown as one page with a heading table of contents. A document counts as 1 item for coverage.
  - Odd or unreadable files fall back to the document view. They never crash the app.
- **Stable ids**: `<topic>.<file>.<sha1(title)[:8]>`. The `Q<n>.` prefix and stars are ignored, so inserting or reordering questions keeps the existing ids. Editing a question's **title** gives it a new id, so its tick is lost.
- **Coverage** is stored only in your browser's `localStorage` (key `prep.coverage.v1`). Use **Export / Import** on the dashboard to move it between browsers.

## API

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/topics` | topics → files with counts (sidebar) |
| GET | `/api/files?topic=` | files in a topic |
| GET | `/api/questions?topic=&file=` | short list: id, title, difficulty, anchor (both params optional) |
| GET | `/api/file?topic=&file=` | one file with every question's raw markdown (one call per page) |
| GET | `/api/question/{id}` | one question with its raw markdown and line range |
| GET | `/api/stats` | totals plus question ids per file (the browser computes coverage) |
| POST | `/api/rescan` | drop the cache and re-parse everything |
| POST | `/api/comment` | **stub**: returns 501 (see `comments.py`) |

## Layout

```
src/app/
  main.py       FastAPI routes + static mount
  library.py    in-memory cache (re-parses only files whose mtime/size changed)
  parser.py     discovery + markdown → questions (pure Python, no FastAPI)
  models.py     Pydantic response models
  comments.py   FUTURE HOOK: plan + stub for writing comments back to .md
  static/       index.html, app.js, styles.css
```

## Offline use

`marked@12.0.2` and `highlight.js@11.10.0` load from jsDelivr. To work offline, download them into `src/app/static/vendor/`:

```bash
mkdir -p src/app/static/vendor
curl -o src/app/static/vendor/marked.min.js    https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js
curl -o src/app/static/vendor/highlight.min.js https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.10.0/build/highlight.min.js
```

`index.html` uses these files automatically when the CDN is unreachable. Without either source, answers show as raw markdown. The two highlight.js theme CSS files are optional: if they're missing, code just isn't coloured.

## Configuration

- `PREP_CONTENT_ROOT=/some/path`: scan a different folder (the default is the repo root).
