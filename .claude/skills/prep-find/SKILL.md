---
name: prep-find
description: Find interview questions by words, stack, file, difficulty, thin answers or "asked in interview" using the generated index — instead of reading question banks or content files.
argument-hint: "<words> [--stack X] [--thin] [--asked] [--level hard]"
---

Run `python3 tools/find.py $ARGUMENTS` and show the matches (stack | file:line | anchor | level | title).
If `index/catalog.json` looks stale (recent edits), run `python3 tools/build_index.py` first.
To open a match, read only its line range.
