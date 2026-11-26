---
name: prep-audit
description: Audit one content file for weak, thin, outdated or wrong answers and list what to fix (optionally fix them). Use when the user asks to audit/review a module or file.
argument-hint: "<file> [fix]"
---

1. Numbers first (no reading): `python3 tools/find.py --file "<file>" --thin --limit 100` and
   `python3 tools/validate.py --file "<file>"` → thin answers, anchor/link/code problems.
2. Read the file (or the thin blocks only, if it is large) and apply the stack's rules from `prompts/`.
3. Report: weak answers by Q# (why), missing high-frequency topics, factual errors.
4. If asked to fix: rewrite in place, one Part at a time; validate after each Part; update the
   stack's index files and `python3 tools/build_index.py`. Stop at a file boundary if context runs low.
