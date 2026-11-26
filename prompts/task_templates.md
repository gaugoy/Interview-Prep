# Task templates — copy a line, fill the <…>, send it

**Slash commands (Claude Code skills in `.claude/skills/`):** `/prep-add-question` · `/prep-improve` ·
`/prep-audit` · `/prep-find` · `/prep-check`. Plain-language requests below work too.

Short, specific requests keep token use low: the agent reads the router, **one** stack file,
the stack's index, and **only** the question block it needs.

| I want to… | Say this | What the agent does (minimal reads) |
|---|---|---|
| Add one question | `Python: add "<question>"` | `tools/find.py` for duplicates → pick topic file → add at end of the right Part → TOC + bank + README counts → Related links |
| Add a question I was asked | `Python: add "<question>" — asked in my interview` | as above + `⭐ Asked in my interview` in heading + row in `My_Interview_Questions.md` |
| Improve one answer | `Python 02_OOP Q12: answer too short / add theory / add example` | read only that block (`<a name="q12">` → `---`) → rewrite → validate |
| Trim an answer | `Django Short 08 Q5: too long, make it booklet-short` | read that block → shorten to the stack's depth rules |
| Fix a wrong answer | `DRF 07 Q4: <what's wrong>` | verify against docs/source → fix → note what changed |
| Link two topics | `Python: link "<question A>" with "<question B>"` | add **Related:** both ways using `#qN` anchors |
| Audit one file | `Django: audit Django ORM/08_Transactions.md` | read that file → audit report → rewrite weak answers |
| Continue the queue | `Django` / `Django Short` / `Python` / `React` (just the name) | take the next ⏳ item from AGENT_INDEX for that stack |
| New topic file | `Python: new topic "<name>" with questions on <list>` | create `NN_<Name>.md` in the standard format + README row + bank |
| Preview release notes | `show release notes since <tag>` | `python3 tools/release_notes.py --from-ref <tag>` (CI publishes them as a GitHub Release on push to `main`) |
| Commit & push | `commit and push` | branch if on `main`, one commit per module/topic, push, PR link |

**Tips for cheaper, better runs**
- Find before you ask: `python3 tools/find.py <words>` gives the exact file + Q-number to name.
- Name the file and Q-number when you know it (`Python 04_Concurrency Q27`) — no searching needed.
- One stack per request. Batch several small edits to the **same** file in one message.
- Say the depth you want if it differs from the stack default ("long", "booklet-short", "with example").
