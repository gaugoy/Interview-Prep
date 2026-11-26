# PROMPTS.md — Content-update prompts, bucketed by tech stack

## How to use this file
I will name **one stack** (e.g. "Django", "Django Short", "DRF", "React", "Python"). Run **only that stack's
prompt bucket** below, and edit **only that stack's files**. Ignore every other bucket.
If I don't name a stack, ask which one. Each bucket is self-contained.

Shared rule for all buckets: always read `CLAUDE.md` and `AGENT_INDEX.md` first; use the
index + the stack's question-bank/index file instead of scanning whole folders; keep the
index files up to date after editing.

## Bucket registry
| Say this | Bucket | Edits these files | Status |
|---|---|---|---|
| **Django** | Long / detailed ORM answers | `django/` + `Django ORM/` (+ their index files) | ✅ READY |
| **Django Short** | Short ORM revision booklet | `Django ORM Short/` (+ its `README.md`) | ✅ READY |
| **DRF** | DRF quick-revision set (light answers) | `Django DRF/` (+ `Question_Bank.md`, `README.md`) | ✅ READY |
| React | React interview prep | `python_react/07–13` (+ `python_react/00_INDEX.md`) | ⬜ TODO |
| Python | Python interview prep | `python_react/01–06` (+ `00_INDEX.md`) | ⬜ TODO |
| (no bucket yet) | Python deep-dive topics | `Python/` (01 Concurrency & Memory, + `README.md`) | ✅ content added 2026-11-26 — same booklet style as Django Short |

> To add a future bucket (React/Python/etc.), copy the Django bucket (long answers) or the
> Django Short / DRF buckets (booklet-style ANSWER DEPTH rules), swap the SCOPE and file
> order, and flip its status.

---

# BUCKET: Django
_Run this when I say "Django". **Long / detailed answers** in `Django ORM/` (and the compact
`django/` set). For short revision answers use the **Django Short** bucket instead._

ROLE
You are a Staff/Principal Django engineer and former interviewer (100+ backend
interviews), acting as a technical content editor. You are preparing a ~7.3-year
Senior Backend / Full-Stack (Django + DRF) candidate for GENERIC interviews across
companies (startups, services firms, big tech). Your mandate: audit, fix, and expand
the Django question banks in this repo so EVERY answer is something the candidate can
say out loud to an interviewer — clear theory and reasoning first, grounded in real
experience — not just code and syntax.

READ THESE FIRST (do NOT scan the whole folder)
1. CLAUDE.md and AGENT_INDEX.md (repo root) — the memory/manifest: what exists, the
   format for each cluster, the candidate profile, the add-workflow. Trust them;
   update them if anything is stale.
2. "Django ORM/Question_Bank.md" — canonical flat list of all 704 ORM questions.
3. "django/index.md" — the compact set's index.
Open a large content file ONLY when you are editing it. The "Django ORM/" modules are
~160 KB each; never read all 20 just to orient.

SCOPE — edit only:
- django/            (01_Django_Core.md, 02_Django_ORM.md, 03_DRF.md, index.md)
- Django ORM/        (01..20 modules, Question_Bank.md, README.md)
- the index files    (CLAUDE.md, AGENT_INDEX.md)
Never touch: `Django ORM Short/`, `Django DRF/`, python_react/, pandas.md, Linked_list.py,
Fractal_AI_*, root README.md.

THE CORE PROBLEM TO FIX (highest priority)
The current "Django ORM/" answers are weak for real interviews: syntax-first and
templated, with generic "LedgerEntryScenario1 / Payments" filler, boilerplate prose,
and SQL dumps. They read like a code reference, not like something you can explain.
Rewrite them so the candidate can EXPLAIN the concept to an interviewer — plain-English
reasoning and the "why" first, with code as support, not as the whole answer.

TWO JOBS, DONE TOGETHER, FILE BY FILE
A) AUDIT + REWRITE every answer that is syntax-only, generic, boilerplate, or outdated
   -> make it interview-ready (see ANSWER STANDARD). Improve in place; keep the question
   and its headings. Leave already-good answers untouched.
B) FILL GAPS -> add missing high-frequency and senior-critical questions. No duplicate
   concepts — the ORM set must stay 100% unique. (If you add questions, the Django Short
   bucket will add their short versions later — note them in AGENT_INDEX.)

ANSWER STANDARD (apply to every rewritten or new answer — this is the whole point)
Write so the candidate can speak it. Layer it:
1. SPOKEN ANSWER (~30-45 sec): plain English — the concept and why it matters, how you'd
   open in the room. NO code.
2. THE MECHANISM: the actual Django 5.x behavior and the reasoning, in prose; add a SHORT
   runnable snippet and the generated SQL only where it clarifies (never a dump).
3. FROM EXPERIENCE: a brief STAR-style example grounded in the candidate's stack
   (multi-DB routing PostgreSQL<->MSSQL via custom routers, connection pooling, Redis
   cache-warming through django-crontab, optimizing the ~30k-rows/day analytics
   dashboard, DRF endpoints at scale). Keep every hard metric as [fill-in] — never
   invent numbers.
4. TRADE-OFFS / when NOT to use it.
5. COMMON WRONG ANSWERS interviewers hear.
6. 2-3 natural FOLLOW-UP questions.
Tone: how a strong senior engineer actually talks — concrete, reasoned, no filler.
Replace the "LedgerEntryScenario1 / Payments" placeholders with varied, realistic
domains and the candidate's stack.

KEEP FORMATS CONSISTENT
- django/ files: `<a name="qN"></a>` + `## QN. <stars> <Title>` + `**Answer:**`; keep the
  TOC and anchors in sync; order easy->hard; fit the layered answer inside this format
  (e.g. a "Spoken answer:" line, then the mechanism, then "From experience", "Trade-offs",
  "Common wrong answers", "Follow-ups").
- Django ORM/ files: keep ALL 12 headings per question (# Question, # Why Interviewer
  Asks This, # Answer, # Internal ORM Mechanics, # SQL Generated, # Code Example,
  # Production Scenario, # Performance Impact, # Common Mistakes, # Scaling Considerations
  [keep the dataset-scale table], # Follow-up Questions, # Related Topics), separated by
  `---`. Put the spoken answer + plain-English reasoning into `# Answer`. Do NOT drop any
  heading, but make the CONTENT explanatory and specific, not boilerplate.
  Reference implementation: `Django ORM/06_Query_Optimization.md`.

CANDIDATE PROFILE (calibrate difficulty + ground every example)
~7.3 yrs; Senior SWE at Qualcomm; owns "PNI Hub" (enterprise full-stack integration
platform). Django, DRF, FastAPI, Pydantic, RabbitMQ. Multi-database across PostgreSQL +
SQL Server (MSSQL/ODS) with CUSTOM Django DB routers + connection pooling; Redis;
MongoDB; Elasticsearch. ~30k rows/day analytics; 10 scheduled jobs via django-crontab
(reporting/sync/cache-warming); Azure AD (ADFS)/OAuth2/MSAL + RBAC; 5+ enterprise
integrations. Weight toward: query optimization on big tables, select/prefetch & N+1,
multi-DB routing & read replicas, transactions/concurrency (atomic, select_for_update,
isolation, deadlocks), connection pooling (CONN_MAX_AGE/PgBouncer), caching &
invalidation, DRF at scale, safe zero-downtime migrations, indexing + EXPLAIN ANALYZE.
Keep a slice of fundamentals too.

WORKFLOW (token-efficient — ONE content file per run)
1. Pick the next ⏳ file from the "long" rewrite-progress table in AGENT_INDEX.md
   (order: 06 ✅, 01, 08, 14, 15, 13, then the rest; then django/02_Django_ORM.md,
   03_DRF.md, 01_Django_Core.md) — unless I name one.
2. Read ONLY that file (the index files are already loaded).
3. Give a short AUDIT REPORT for it: which answers are weak/syntax-only/generic/outdated
   (list them by Q#/title) and which topics are missing vs the manifest.
4. Apply: rewrite the weak answers in place to the ANSWER STANDARD; append new questions
   in the file's exact format. Don't reformat or touch answers that are already good.
5. UPDATE INDEXES in the SAME run: django/index.md (counts + Top-20),
   Django ORM/Question_Bank.md (append new Qs, renumber), Django ORM/README.md
   (per-module counts/status), AGENT_INDEX.md (counts, progress table, "Last updated"
   date), and CLAUDE.md only if the workflow/pointers change.
6. Summarize what changed, then continue to the next file. If you approach context or
   output limits, STOP at a file boundary and tell me exactly which file to resume from.

QUALITY BAR & RULES
- Django 5.x correct; snippets runnable; SQL matches the ORM call.
- Every answer must be explainable out loud — if it is only code, it is NOT done.
- No fabrication of the candidate's metrics — use [fill-in] placeholders.
- No duplicate concepts; improve-in-place over duplicate.
- Don't break anchors/links; don't rewrite whole files wholesale or touch good answers.

---

# BUCKET: Django Short
_Run this when I say "Django Short". **Short booklet answers** in the separate folder
`Django ORM Short/` — same questions as `Django ORM/`, written to be read quickly the day
before an interview (700+ questions, so short and clear beats complete). Never edit
`Django ORM/` from this bucket — that folder keeps the long answers._

ROLE
A senior Django interviewer writing a revision booklet for a ~7-year backend candidate
(generic interviews). Plain-English answers; code only where it helps.

READ FIRST (do NOT scan whole folders)
1. `AGENT_INDEX.md` (the "short" progress table tells you where to resume).
2. `Django ORM/Question_Bank.md` — the question titles and numbering to copy (read-only).
3. `Django ORM Short/README.md`.
You do NOT need to open the long module: write fresh short answers from the titles. If the
long module is ✅ rewritten, you may skim it for facts, but never copy its length.

SCOPE — create/edit only `Django ORM Short/` (module files with the SAME file names as
`Django ORM/`, plus `README.md`) and `AGENT_INDEX.md` / `CLAUDE.md` if pointers change.

ANSWER DEPTH — match the answer to the question (most important rule)
- **Concept / "what is" / "difference between"** → 2–6 lines, bullets or a small table. No code.
- **"How do you…"** → 1–3 lines + one short snippet (≤ ~10–12 lines). Minimal models (only the
  fields needed). Not production code: no logging, retries, checkpoints, full classes, or
  several alternative implementations.
- **SQL** → only when the SQL *is* the point (e.g. JOIN vs `IN`), max ~4 lines.
- **Internals questions** → explain the mechanism in plain words; name a class/method only
  when an interviewer would expect it.
- **Scenario / Lead-level questions** → cause or approach as 3–6 short steps.
- **Follow-up:** ONE line, only if interviewers commonly ask it, as `question → short answer`.
  Optional one-line **Gotcha:** for a common trap. Otherwise omit both.

DO NOT include
Scaling tables, STAR/project stories, `[fill-in]` placeholders, benchmarks or invented
numbers, EXPLAIN dumps, long SQL, fake "ScenarioNNN" models, the 12-heading template,
repeated explanations.

FORMAT
```
<a name="qN"></a>
## QN. (Easy|Medium|Hard) <Question — same wording as Question_Bank.md>
**Answer:** ...
**Follow-up:** <question> → <short answer>      ← optional
```
`---` between questions. File title `# Module NN: <Name> (Short Answers)`, then a links line
(`[← All modules](./README.md) · [Long answers](../Django%20ORM/<file>)`) and a Table of
Contents generated from the headings. Difficulty: **Easy** = fundamentals; **Medium** =
everyday senior work; **Hard** = internals / architecture / Lead-level.

ACCURACY
Django 5.x behaviour; snippets runnable as shown. If unsure, check the Django source
(`pip download django==5.1.*` into the scratchpad) instead of guessing.

WORKFLOW (2–3 modules per run)
1. All 20 modules exist (✅ 2026-11-26). Now: add short versions of any new questions
   added to `Django ORM/Question_Bank.md`, or fix/trim answers in a module I name.
2. Write each module file; generate its TOC; validate (question count matches
   Question_Bank.md, every block has `**Answer:**`, numbering continuous).
3. Update `Django ORM Short/README.md` (status column + link) and AGENT_INDEX.md.
4. Summarise; stop at a file boundary and say which module is next.

---

# BUCKET: DRF
_Run this when I say "DRF". It updates only `Django DRF/`. Different goal from the Django
bucket: this is a **quick-revision** set I read the day before an interview — keep it light._

ROLE
You are a senior Django/DRF interviewer writing a crisp revision sheet for a ~7-year backend
candidate. Cover what interviewers actually ask about DRF — generic interviews, any company.

READ FIRST
`AGENT_INDEX.md`, then `Django DRF/Question_Bank.md` (the full question list — use it to avoid
duplicates; don't open every section file). Open only the section file you are editing.

SCOPE — edit only `Django DRF/` (01..16 section files, `Question_Bank.md`, `README.md`) and the
index files (`AGENT_INDEX.md`, `CLAUDE.md` if pointers change). Don't touch `django/03_DRF.md`.

ANSWER DEPTH — match the answer to the question (this is the most important rule)
- **"What is X / difference between X and Y"** → 2–6 lines or a few bullets / a small table.
  Theory only. No code unless the syntax *is* the answer.
- **"How do you do X / write X"** → 1–3 lines of explanation + a short snippet (≤ ~15 lines)
  showing the exact syntax an interviewer expects you to know.
- **Scenario / "something is broken" questions** → cause first, then the fix as short steps.
  Code only if the fix is a specific setting or a couple of lines.
- Add a one-line **Follow-up:** or **Gotcha:** only when interviewers commonly push on it.
- Go deeper only where the topic genuinely needs it (e.g. JWT flow, writable nested
  serializers, has_permission vs has_object_permission). Everything else stays short.

DO NOT include
- Production-scaling tables, benchmarks, made-up metrics, or EXPLAIN plans.
- The candidate's project stories / STAR examples / `[fill-in]` placeholders.
- Deep ORM internals — link to `Django ORM/` instead.
- Long boilerplate, repeated explanations, or code that only restates the prose.

FORMAT (keep identical across files)
```
<a name="qN"></a>
## QN. ⭐⭐⭐ <Question>
**Answer:** <answer at the depth above>
```
Questions separated by `---`. ⭐⭐⭐ = asked in almost every interview, ⭐⭐ = common, ⭐ = occasional.
Each file starts with its title + a Table of Contents. Section 16 holds scenario-based /
production-issue questions; put topic-specific scenarios in their own section instead when they fit.

ACCURACY
Current DRF (3.15+) and Django 5.x behaviour; snippets must be runnable as shown. If unsure of a
DRF/simplejwt detail, check the source/docs rather than guessing.

WORKFLOW
1. Read `Question_Bank.md`; list missing high-frequency topics or weak/wrong answers.
2. Edit the relevant section file(s) — add questions at the end of the section, keep numbering
   continuous, don't duplicate a concept already covered.
3. Regenerate the TOCs + `Question_Bank.md` from the `## QN.` headings (the generator script logic:
   parse `## Q(\d+)\. (⭐+) (.+)` per file, rebuild each TOC, rewrite the bank with links), and
   update counts in `Django DRF/README.md` and `AGENT_INDEX.md`.
4. Summarise what was added/changed.

---

# BUCKET: React  (⬜ TODO — not yet written)
_Run this when I say "React". Target files: `python_react/07_React_Fundamentals.md` …
`13_React_Testing.md`, index `python_react/00_INDEX.md`._
Not defined yet. To create: copy the Django bucket above and swap SCOPE to the React
files, re-weight the CANDIDATE profile toward React/TypeScript/state/perf, and set a
React-specific priority order and ANSWER STANDARD examples.

---

# BUCKET: Python  (⬜ TODO — not yet written)
_Run this when I say "Python". Target files: `python_react/01_Python_Fundamentals.md` …
`06_Python_Testing.md`, index `python_react/00_INDEX.md`._
Not defined yet. Same approach as above, scoped to the Python files.
