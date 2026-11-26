# CLAUDE.md

**Before any work on the Django interview question banks, read [`AGENT_INDEX.md`](./AGENT_INDEX.md) first.**

When I name a stack (e.g. "Django", "Django Short", "DRF", "React", "Python"), run that stack's bucket from [`PROMPTS.md`](./PROMPTS.md) and edit only that stack's files. If I don't name one, ask which.

It is the memory/manifest: what already exists, the format for each cluster, the candidate profile, and the add-workflow. Use it (plus `Django ORM/Question_Bank.md` for the full ORM question list) instead of scanning the content files — the `Django ORM/` modules are ~160 KB each, so only open a module when you are actually appending to it. After adding or changing questions, update `AGENT_INDEX.md` (counts + date) in the same run.

The `Django DRF/` folder is a light quick-revision set — use `Django DRF/Question_Bank.md` as its index and follow the depth rules in PROMPTS.md → BUCKET: DRF (no project stories, no scaling tables).

Two ORM folders: `Django ORM/` = long/detailed answers ("Django" bucket); `Django ORM Short/` = short booklet answers for the same questions ("Django Short" bucket). Never edit one folder from the other folder's bucket.
