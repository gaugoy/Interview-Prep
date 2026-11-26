---
name: prep-add-question
description: Add one interview question to the right stack file without creating a duplicate. Use when the user says "add question", "add this to Python/DRF/Django", or mentions a question they were asked in an interview.
argument-hint: "<Stack>: <question text> [— asked in my interview]"
---

1. Read `PROMPTS.md` → open only the named stack file in `prompts/` (it inherits `prompts/00_shared_rules.md`).
2. Duplicate check — don't read banks: `python3 tools/find.py <2-4 key words> --stack "<Stack>"`.
   - Already exists → improve that answer instead (open just its block via the printed `file:line`).
3. Pick the topic file + Part from the stack's index (`Python/README.md`, `Django DRF/README.md`, …).
   Append the question at the end of that Part / file using the stack's exact format and depth rules.
   Use the next `<a name="qN">` number; never renumber existing questions.
4. If "asked in my interview": add `⭐ Asked in my interview` to the heading and a row in `My_Interview_Questions.md`.
5. Add **Related:** links both ways where the stack uses them (`[Topic · QN](./file.md#qN) — title`).
6. Regenerate the file's TOC and the stack's `Question_Bank.md` entry, then run `python3 tools/build_index.py`
   and `python3 tools/validate.py --changed` (the hooks also do this). Report file, Q-number and anchor.
