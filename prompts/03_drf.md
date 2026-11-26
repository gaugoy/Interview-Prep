# 03 — DRF (quick revision) · say **"DRF"**

Inherits [`00_shared_rules.md`](./00_shared_rules.md).

| | |
|---|---|
| **Folder** | `Django DRF/` (16 section files) |
| **Index to read first** | `Django DRF/Question_Bank.md` · `Django DRF/README.md` |
| **Don't touch** | `django/03_DRF.md` (older compact set, owned by the Django stack) |

## Answer depth
- "What is X / X vs Y" → 2–6 lines / small table; code only if the syntax *is* the answer.
- "How do you…" → 1–3 lines + snippet ≤ ~15 lines of the exact syntax interviewers expect.
- Scenario / "it's broken" → cause first, then fix as short steps.
- Go deeper only where it's genuinely needed (JWT flow, writable nested serializers,
  `has_permission` vs `has_object_permission`). No project stories, no deep ORM internals
  (link to `Django ORM Short/` instead).

## Format
`<a name="qN"></a>` + `## QN. ⭐⭐⭐|⭐⭐|⭐ <Question>` + `**Answer:**`; `---` between; TOC at top.
⭐⭐⭐ almost every interview · ⭐⭐ common · ⭐ occasional. Section 16 = scenario / production issues.

## Workflow
Gap-check `Question_Bank.md` → edit the section file (append at end, continuous numbering) →
regenerate TOCs + `Question_Bank.md` from `## Q(\d+)\. (⭐+) (.+)` → update README counts + AGENT_INDEX.
