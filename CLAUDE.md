# CLAUDE.md

**Start with [`PROMPTS.md`](./PROMPTS.md)** — a short router. When I name a stack ("Django", "Django Short", "DRF", "Python", "React"), open only that stack's file in `prompts/`; every stack inherits [`prompts/00_shared_rules.md`](./prompts/00_shared_rules.md). If I don't name a stack, ask which.

- **How to work** → `prompts/` (shared rules, one file per stack, `candidate_profile.md`, `task_templates.md`).
- **What exists** → [`AGENT_INDEX.md`](./AGENT_INDEX.md) (folders, counts, progress queues) + each stack's `Question_Bank.md` / index file.
- Don't scan content folders to orient — use `python3 tools/find.py <words>` (generated index) and open only the question block you need. Validation (`tools/validate.py`) and indexing (`tools/build_index.py`) run automatically via hooks; see `tools/README.md`.
- Slash commands: `/prep-add-question`, `/prep-improve`, `/prep-audit`, `/prep-find`, `/prep-check`. After adding or changing questions, update the stack's index files and `AGENT_INDEX.md` (counts + date) in the same run.

Folders: `Django ORM/` (long ORM answers) · `Django ORM Short/` (short booklet, same questions) · `django/` (compact Django set) · `Django DRF/` (DRF quick revision) · `Python/` (all Python, topic files) · `React/` (React/Web/JS, not yet restructured). Never edit one stack's folder from another stack's prompt.
