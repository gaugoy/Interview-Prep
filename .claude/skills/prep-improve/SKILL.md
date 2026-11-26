---
name: prep-improve
description: Improve, shorten, fix or add theory/examples to ONE existing interview answer, reading only that question block. Use for requests like "Python 02_OOP Q12 add theory", "trim Django Short 08 Q5", "this answer is wrong".
argument-hint: "<file or stack> Q<n>: <what to change>"
---

1. Locate it cheaply: `python3 tools/find.py --file "<file>" <words>` (or by Q-number) → note `file:line_start-line_end`.
2. Read ONLY those lines (Read with offset/limit). Read the stack file in `prompts/` for its depth rules.
3. Rewrite in place — keep the heading, anchor and number; theory first; code only if it helps.
   Verify facts against real docs/source when version-specific.
4. If the title changes, tell the user: the question id changes and its viewer tick resets.
5. `python3 tools/validate.py --file "<file>"` (hook runs it too); fix any errors. Summarise the change.
