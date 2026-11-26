# 02 — Django Short (revision booklet) · say **"Django Short"**

Inherits [`00_shared_rules.md`](./00_shared_rules.md).

| | |
|---|---|
| **Folder** | `Django ORM Short/` (same file names + numbering as `Django ORM/`) |
| **Index to read first** | `Django ORM/Question_Bank.md` (titles, read-only) · `Django ORM Short/README.md` |
| **Never edit** | `Django ORM/` (long answers live there) |

## Answer depth (match the question)
- Concept / "difference between" → 2–6 lines, bullets or small table, **no code**.
- "How do you…" → 1–3 lines + one snippet ≤ ~12 lines (minimal models).
- SQL only when the SQL *is* the point (≤ 4 lines). Internals → plain words.
- Scenario / Lead questions → 3–6 short steps.
- **Do not include:** scaling tables, STAR stories, `[fill-in]`, invented numbers, EXPLAIN dumps, 12-heading template.

## Format
```
<a name="qN"></a>
## QN. (Easy|Medium|Hard) <same wording as Question_Bank.md>
**Answer:** …
**Follow-up:** <question> → <short answer>     ← optional
```
File title `# Module NN: <Name> (Short Answers)` + links line
(`[← All modules](./README.md) · [Long answers](../Django%20ORM/<file>)`) + TOC.

## Workflow
All 20 modules exist (705 Q). Runs now: add short versions of new long-set questions, or
fix/trim a module I name. Validate titles/count against `Question_Bank.md` (ignore the
`⭐ Asked in my interview` suffix). Update `README.md` + AGENT_INDEX.
