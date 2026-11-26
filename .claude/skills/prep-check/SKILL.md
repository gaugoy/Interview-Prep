---
name: prep-check
description: Rebuild the question index and run all content validation (anchors, links, titles, code blocks, question banks). Use before committing or when the user asks to check/validate the repo.
---

1. `python3 tools/build_index.py` — regenerates `index/catalog.json`, `index/INDEX.md`, AGENT_INDEX counts.
2. `python3 tools/validate.py` — report errors first (must be 0), then a one-line summary of warnings
   (warnings = known content debt, e.g. templated `Django ORM/` code).
3. If errors: fix them (each line has `file:line`), re-run until 0 errors.
