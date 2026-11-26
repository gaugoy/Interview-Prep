# AGENT_INDEX — Django Interview Prep (read this FIRST)

> **Purpose:** This file is the memory/manifest for the Django question banks.
> Read **this file only** to understand what exists and how to extend it.
> **Do NOT scan all the content files** — they are large (the `Django ORM/` modules
> are ~160 KB each). Open a content file only when you are actually appending to it.
> **After you add or change questions, update this file** (counts + any new topics) in
> the same run.

_Last updated: 2026-11-26 (Module 06 rewritten + 4 new Qs; django/index.md counts fixed; new `Django DRF/` set, 131 Q; `Django ORM Short/` complete; new `Python/` concurrency & memory file) · Scope: Django interview prep only._

---

## 1. Where things live (edit only these four clusters)

| Cluster | What it is | Files |
|---|---|---|
| `django/` | Compact, interview-frequency focused (easy→hard, ⭐ difficulty) | `01_Django_Core.md`, `02_Django_ORM.md`, `03_DRF.md`, `index.md` |
| `Django ORM/` | Deep Senior/Lead/Architect set, rigid 12-heading template | `01_..md` … `20_..md`, `Question_Bank.md`, `README.md` |
| `Django ORM Short/` | **Short booklet answers** for the same ORM questions (same file names/numbering as `Django ORM/`); difficulty tag (Easy/Medium/Hard), code only when needed | `01_..md` … `20_..md` (created progressively), `README.md` |
| `Django DRF/` | **Light quick-revision** DRF set (one-day-before reading); depth matches the question, no project stories/scaling tables | `01_..md` … `16_..md`, `Question_Bank.md`, `README.md` |

**Never touch:** `python_react/`, `pandas.md`, `Linked_list.py`, `Fractal_AI_*`, `README.md` (root).

**Cheap path to "what already exists" (no full-folder scan):**
- `django/` questions → the title list in section 3 below (or `grep '^## Q' django/*.md`).
- `Django ORM/` questions → **`Django ORM/Question_Bank.md`** is the canonical flat list of all 705. Read that one file, not the 20 modules.

---

## 2. Format to follow (keep each cluster consistent)

**`django/` files** — per question:
```
<a name="qN"></a>
## QN. ⭐/⭐⭐/⭐⭐⭐ <Title>
**Answer:**
<prose + runnable code>
```
Keep the top Table of Contents + anchors in sync; order easy→hard. ⭐ = rare, ⭐⭐ = common, ⭐⭐⭐ = most asked.

**`Django ORM/` files** — per question, ALL 12 headings, separated by `---`:
`# Question` · `# Why Interviewer Asks This` · `# Answer` · `# Internal ORM Mechanics` · `# SQL Generated` · `# Code Example` · `# Production Scenario` · `# Performance Impact` · `# Common Mistakes` · `# Scaling Considerations` (keep the dataset-scale table) · `# Follow-up Questions` · `# Related Topics`. Questions must stay **100% unique** — no duplicate concept across the 20 modules.

**Preferred answer shape for NEW/rewritten answers (both clusters):** a ~30-sec spoken answer → the real mechanism (Django 5.x API + short runnable code + generated SQL) → a short "from experience" STAR example grounded in the candidate's stack with any metric as `[fill-in]` → trade-offs / when-not-to → common wrong answers → 2–3 follow-ups.

**How that shape maps onto the 12 ORM headings** (reference implementation: `Django ORM/06_Query_Optimization.md` — copy its style):
- `# Why Interviewer Asks This` → 1–2 sentences on the signal being tested (no "Evaluates X" one-liners).
- `# Answer` → `**Spoken answer:** "…"` (quoted, no code) + `**The reasoning:**` bullets.
- `# Internal ORM Mechanics` → real Django 5.x internals in prose (method/class names).
- `# SQL Generated` → SQL that matches the ORM call shown; `# Code Example` → realistic models in varied domains (shop, helpdesk, iot, hr, cms, PNI Hub `pni_`/`ops_` apps) — **never** `XxxScenarioNNN` / Ledger / Payments filler.
- `# Production Scenario` → `**From experience (STAR):** **S** … **T** … **A** … **R** …` grounded in PNI Hub; every number is `[fill-in]`.
- `# Performance Impact` → cost bullets + `**Trade-offs / when NOT to use it:**`.
- `# Common Mistakes` → `**Common wrong answers interviewers hear:**` bullets.
- `# Scaling Considerations` → keep the 5-column dataset-scale table, but fill it with technique-specific, qualitative content (no fake ms figures).
- `# Related Topics` → `* Module NN QN — short topic` lines.
- Verify Django internals against real source when unsure (e.g. `pip download django==5.1.*` into the scratchpad); don't guess.

---

## 3. Current coverage manifest

### `django/` (frequency set)
- **01_Django_Core.md — 20 Q:** MVT · Project vs App · URL routing/path converters · FBV vs CBV · Middleware · Signals · Forms/validation · Templates/tags · Auth system · Permissions/authz · Sessions · Caching · Static/media · Admin customization · Management commands · Security best practices · Settings/environments · Context processors · Generic CBVs · Request/Response lifecycle.
- **02_Django_ORM.md — 18 Q:** Fields/model creation · Relationships · QuerySet API/chaining · Filtering/lookups · Q objects · Aggregation/annotation · select_related/prefetch_related · N+1 · Raw SQL · Transactions · Custom managers/QuerySets · Migrations · Indexing · F-expressions/atomic updates · Model inheritance · Bulk ops · QuerySet evaluation/caching · values/values_list/defer/only.
- **03_DRF.md — 18 Q:** DRF components · Serializers/ModelSerializer · Nested/writable · Custom validation · APIView/GenericAPIView/ViewSet · Routers · Auth methods · JWT · Permissions · Throttling · Pagination · Filtering/search/order · Versioning · Renderers/parsers · Testing · CRUD build · Exception handling · Settings.

### `Django ORM/` (deep set) — 20 modules = **705 Q** (35 each; Module 06 has 39, Module 08 has 36)
Canonical titles live in `Django ORM/Question_Bank.md`. Modules:
01 ORM Fundamentals · 02 Model Design · 03 Field Types · 04 Model Meta Options · 05 Managers & QuerySets · 06 Query Optimization · 07 Relationships · 08 Transactions · 09 Aggregation & Annotation · 10 Subquery & Exists · 11 Database Functions · 12 Indexing · 13 Migrations · 14 Multi-Database · 15 Concurrency · 16 Scaling Strategies · 17 ORM Internals · 18 Architecture Questions · 19 Production Issues · 20 Lead-Level Scenarios.

**Module 06 additions (Q36–Q39):** N+1 regression tests in CI (`assertNumQueries`/`CaptureQueriesContext`, flat-count tests) · N+1 in DRF serializers (`setup_eager_loading`, annotations instead of `SerializerMethodField`) · duplicate rows from multi-valued joins, `distinct()` cost vs `Exists` · sync jobs without per-row `get()`/`update_or_create()` (`in_bulk`, diff, `bulk_create(update_conflicts=True)`). Don't re-add these concepts elsewhere.

**Module 08 Q36 (ACID properties)** — a question asked in the candidate's real interview; short answer exists in `Django ORM Short/08_Transactions.md`, long version in `Django ORM/08_Transactions.md` still pending (add it when the long 08 is rewritten). Real interview questions are tracked in root `My_Interview_Questions.md` and marked "⭐ Asked in my interview" in their heading.

### Long-answer rewrite progress (PROMPTS.md "Django" bucket — one file per run, in this order)
Audit finding (2026-11-26): the original `Django ORM/` answers are 100% templated (identical "Internal Mechanics" sentence, `XxxScenarioNNN` models, SQL unrelated to the question, generic mistakes/scaling text). Every module in ⏳ state needs a **full per-question rewrite** — expect all 35 answers to be weak.

| Order | File | Status |
|---|---|---|
| 1 | `Django ORM/06_Query_Optimization.md` | ✅ Rewritten 2026-11-26 (35 rewritten + 4 new = 39) |
| 2 | `Django ORM/01_ORM_Fundamentals.md` | ⏳ **Next — resume here** |
| 3 | `Django ORM/08_Transactions.md` | ⏳ |
| 4 | `Django ORM/14_Multi_Database.md` | ⏳ |
| 5 | `Django ORM/15_Concurrency.md` | ⏳ |
| 6 | `Django ORM/13_Migrations.md` | ⏳ |
| 7 | remaining `Django ORM/` modules (02–05, 07, 09–12, 16–20) | ⏳ |
| 8 | `django/02_Django_ORM.md`, then `03_DRF.md`, then `01_Django_Core.md` | ⏳ (not yet audited) |

**Known fix-ups:** ~~`django/index.md` 30/25/25 claim~~ fixed 2026-11-26 (now 20/18/18 = 56, Top-20 links to real anchors). ~~`Django ORM/README.md` broken `file:///` links~~ fixed (now relative). When rewriting a module, check its `# Related Topics` against the titles in `Question_Bank.md` — old ones were generic placeholders.

---

### Short-answer progress (PROMPTS.md "Django Short" bucket → `Django ORM Short/`, 2–3 modules per run)
Independent of the long rewrite: short answers are written fresh from `Django ORM/Question_Bank.md` titles. The long files in `Django ORM/` are never edited by this bucket.

**Status: ✅ all 20 modules done (705 Q, 2026-11-26)** — titles and numbering validated against `Django ORM/Question_Bank.md`. Future "Django Short" runs: only add short versions of new questions added to the long set, or fix errors.

Short format: `<a name="qN"></a>` + `## QN. (Easy|Medium|Hard) <Question>` + `**Answer:**` (+ optional one-line `**Follow-up:**` / `**Gotcha:**`), `---` between questions, TOC at top. Depth rules: PROMPTS.md → BUCKET: Django Short.

### `Django DRF/` (quick-revision set) — 16 sections, **131 Q**
Canonical list: `Django DRF/Question_Bank.md` (generated from the `## QN.` headings). Sections: 01 Basics & Request/Response (13) · 02 Serializers (15) · 03 Validation (9) · 04 Relations & Nested (8) · 05 Views & ViewSets (12) · 06 Routers (5) · 07 Authentication/JWT/OAuth2 (11) · 08 Permissions (8) · 09 Throttling (4) · 10 Pagination (5) · 11 Filtering/Search/Ordering (5) · 12 Versioning/Parsers/File upload (5) · 13 Exception handling (5) · 14 Testing (5) · 15 Performance & Caching (6) · 16 Scenario-based & production issues (15).
Format: `<a name="qN"></a>` + `## QN. ⭐… <Q>` + `**Answer:**`, `---` between questions, TOC at top. Depth rules live in `PROMPTS.md` → BUCKET: DRF. Overlaps with `django/03_DRF.md` (18 Q, older compact set) are intentional; don't edit that file from the DRF bucket.

---

### `Python/` (topic deep-dives, booklet style) — 2 files, **59 new Q** (+ links to existing `python_react/` questions)
`01_Concurrency_and_Memory.md` (54 headings: 36 new, 18 link to `python_react/01,04` with an optional "Extra" line): Part A GIL & basics · B threading · C multiprocessing · D asyncio/async-await · E scenarios · F memory management & GC. Format: `<a name="qN"></a>` + `## QN. (Easy|Medium|Hard) <Q>` + `**Answer:**` + small example, TOC at top. Separate from `python_react/` (don't duplicate there). `02_OOP_and_Decorators.md` (23 new Q): Part A = link tables to existing `python_react/01,03,04` questions (no duplication), Part B OOP, Part C decorators. **Rule for new Python files: check `python_react/` first and link existing questions (GitHub heading slugs) instead of rewriting them.** New topic files go here as `03_...md` and get a row in `Python/README.md`.

---

## 4. Candidate profile (calibrate difficulty + ground examples)

~7.3 yrs; Senior SWE at Qualcomm, owns "PNI Hub" (enterprise full-stack integration platform). Django + DRF + FastAPI + Pydantic + RabbitMQ. **Multi-database** across PostgreSQL + SQL Server (MSSQL/ODS) with **custom Django DB routers + connection pooling**; Redis caching; MongoDB; Elasticsearch. ~30k rows/day analytics; 10 scheduled jobs via **django-crontab** (reporting/sync/cache-warming); Azure AD (ADFS)/OAuth2/MSAL + RBAC; 5+ enterprise integrations. → Weight new questions toward: query optimization on big tables, select/prefetch & N+1, multi-DB routing & read replicas, transactions/concurrency, connection pooling, caching/invalidation, DRF at scale, background jobs, safe zero-downtime migrations, indexing + EXPLAIN. Keep some fundamentals too.

---

## 5. Workflow to add future questions (token-efficient)

1. Read **this file** + `Django ORM/Question_Bank.md` (+ `django/index.md`) — not the module files.
2. Pick a target file; list the gap (missing/thin/outdated topics) vs the manifest above.
3. Open **only that one file**, append new questions in its exact format (improve weak ones in place; never duplicate a concept).
4. Update indexes in the same run: `django/index.md` counts/Top-20, `Django ORM/Question_Bank.md`, `Django ORM/README.md`, **and section 3 + the date in this file**.
5. One content file per run (the ORM modules are too big to batch). For a full rewrite, write the new questions in batches to scratchpad part files, concatenate, then validate (39/35 `# Question` blocks, all 12 headings outside code fences, a `**Spoken answer:**` in every block, scaling table present, zero `Scenario\d+` leftovers) before updating the indexes.
6. Update the **Rewrite progress** table in §3 so the next run knows where to resume.
