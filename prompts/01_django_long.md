# 01 — Django (long answers) · say **"Django"**

Inherits [`00_shared_rules.md`](./00_shared_rules.md). Uses [`candidate_profile.md`](./candidate_profile.md).

| | |
|---|---|
| **Folders** | `Django ORM/` (20 modules, deep set) · `django/` (compact 56-Q set) |
| **Index to read first** | `Django ORM/Question_Bank.md` (all titles) · `django/index.md` · AGENT_INDEX "Long-answer rewrite progress" table |
| **Reference implementation** | `Django ORM/06_Query_Optimization.md` |
| **Not this stack** | short answers → `02_django_short.md`; DRF quick set → `03_drf.md` |

## Goal
Old `Django ORM/` answers are templated (fake `ScenarioNNN` models, unrelated SQL, boilerplate).
Rewrite each so I can **explain it out loud** in a senior interview; add missing senior-critical
questions. Keep the set 100% unique.

## Answer layers (inside `# Answer` and the other headings)
1. **Spoken answer** (~30–45 s, no code). 2. **Mechanism** — real Django 5.x behaviour; short
snippet + matching SQL only where it clarifies. 3. **From experience** — STAR example from the
candidate profile, every metric `[fill-in]`. 4. **Trade-offs / when not to use.**
5. **Common wrong answers.** 6. **2–3 follow-ups.**

## Format
- `Django ORM/` — keep all **12 headings** per question (`# Question`, `# Why Interviewer Asks This`,
  `# Answer`, `# Internal ORM Mechanics`, `# SQL Generated`, `# Code Example`,
  `# Production Scenario`, `# Performance Impact`, `# Common Mistakes`, `# Scaling Considerations`
  [5-column dataset-scale table, qualitative], `# Follow-up Questions`, `# Related Topics`), `---` between.
- `django/` — `<a name="qN"></a>` + `## QN. ⭐… Title` + `**Answer:**`; TOC in sync; easy→hard.

## Workflow (one module per run)
1. Next ⏳ module from AGENT_INDEX (order 06 ✅ → 01 → 08 → 14 → 15 → 13 → rest → `django/02,03,01`), unless I name one.
2. Read only that module → short **audit report** (weak answers by Q#, missing topics).
3. Rewrite weak answers in place; append new questions in the exact format.
4. Update `Django ORM/Question_Bank.md`, `Django ORM/README.md`, `django/index.md`, AGENT_INDEX
   (progress + counts). New questions → also note them for the Django Short stack.
5. Big rewrites: write questions in batches to scratchpad part files, concatenate, then validate
   (question count, all 12 headings outside code fences, a spoken answer in every block,
   scaling table present, zero `Scenario\d+` leftovers) before updating the indexes.
