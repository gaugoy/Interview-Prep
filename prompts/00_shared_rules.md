# 00 — Shared rules (every stack inherits these)

> Edit a rule **here** and it applies to Django, Django Short, DRF, Python and React at once.
> A stack file only lists what is *different* for that stack. If a stack rule conflicts with
> this file, the stack rule wins for that stack.

## 1. Read order (token budget)
1. `PROMPTS.md` (router) → the **one** stack file for the request.
2. **Find, don't read:** `python3 tools/find.py <words> [--stack X] [--file F] [--thin] [--asked]`
   searches the generated index (`index/catalog.json`) and prints `file:line-range` — open only
   that block. Use it for duplicate checks instead of reading `Question_Bank.md` files.
3. Open a content file only to edit it or to verify an answer you link to.
4. `AGENT_INDEX.md` + `index/INDEX.md` = *what exists* (generated counts, progress queues).
   `prompts/` = *how to work*. Don't re-derive either from the content files.

## 2. Scope
Edit only the folders listed in the active stack file, plus `AGENT_INDEX.md` and the stack's
index files. Never edit another stack's folder. Never touch: `pandas.md`, `Linked_list.py`,
`Fractal_AI_*`, `venv/`, `src/`, `run.sh`. Root `README.md` and `LICENSE` only when I ask — and never hand-edit the README's `<!-- AUTO:… -->` count blocks (`tools/build_index.py` regenerates them). "What changed" is never written into the README — it's published as a GitHub Release (`tools/release_notes.py`) on every push to `main`.

## 3. Answer quality (all stacks)
- Every answer must be **explainable out loud** — plain-English theory first; code supports it.
  An answer that is only code is not done.
- **Code only when it helps**: short, runnable, minimal (no production boilerplate).
- **Follow-up:** / **Gotcha:** — one line each, only where interviewers commonly push.
- Correct for current versions (Python 3.12–3.14, Django 5.x, DRF 3.15+, React 18/19). When
  unsure, check the real source/docs (e.g. `pip download django==5.1.*` into the scratchpad)
  instead of guessing. State version-specific behaviour explicitly.
- Never invent the candidate's metrics or experience (see `candidate_profile.md`).

## 4. No duplication
- Search the stack's index before adding anything. If the question exists → **improve it in
  place**. If two answers overlap → **merge** into the better one and repoint links.
- A question that belongs to another topic goes in the right file; link to it from elsewhere.

## 5. Anchors & links
- Every question has an explicit anchor on the line above its heading: `<a name="qN"></a>`.
- Link to the anchor, never to auto-generated heading slugs: `./file.md#qN` (same file `#qN`).
- One jump must be enough — no link chains. Before linking, verify the target answer is
  correct and complete; fix it first if not.
- Keep each file's Table of Contents in sync with its headings (regenerate it by script).

## 6. Real interview questions
If I say a question was **asked in my interview**: put the full answer in the right file, add
`⭐ Asked in my interview` to its heading, and add a row to root `My_Interview_Questions.md`.

## 7. Validation (automated — don't eyeball, don't hand-count)
- `python3 tools/validate.py [--file F]` checks anchors, `**Answer:**`, python code parse, links +
  anchors, link-title drift, question-bank sync, duplicate titles. **0 errors** before finishing.
- `python3 tools/build_index.py` regenerates `index/catalog.json`, `index/INDEX.md` and the counts
  block in `AGENT_INDEX.md` — never edit those counts by hand.
- Claude Code hooks run both automatically (after each edit / at stop); the git pre-commit hook
  and CI run them too. Per-stack rules: `STACKS` in `tools/catalog.py`. Details: `tools/README.md`.
- Still update the stack's own index files (`Question_Bank.md`, README tables/TOCs) in the same run.

## 8. Run size & reporting
- Work in file-sized steps; if context/output gets tight, stop at a file boundary and say
  exactly where to resume.
- Finish with a short summary: what changed, what was verified, what's next.

## 9. Git (only when I ask)
- Never commit unless asked. Never commit `run.sh`, `src/`, `venv/` or secrets.
- If on `main`, create a branch first. Make **one commit per module/topic** with
  `docs(<area>): …` messages; push; give me the PR link.
