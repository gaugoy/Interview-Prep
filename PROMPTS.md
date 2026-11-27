# PROMPTS.md — router (read this, then ONE stack file)

1. Find the stack I named below → open **only** its file in `prompts/`.
2. Every stack inherits [`prompts/00_shared_rules.md`](./prompts/00_shared_rules.md) (read order,
   no-duplication, anchors, validation, git). Change a rule there → it changes for all stacks.
3. No stack named? Ask which. Common request formats: [`prompts/task_templates.md`](./prompts/task_templates.md).

| Say | Stack file | Folder(s) it edits | Index it reads first | Status |
|---|---|---|---|---|
| **Django** | [`01_django_long.md`](./prompts/01_django_long.md) | `Django ORM/`, `django/` | `Django ORM/Question_Bank.md`, `django/index.md` | ✅ (module 06 rewritten) |
| **Django Short** | [`02_django_short.md`](./prompts/02_django_short.md) | `Django ORM Short/` | `Django ORM/Question_Bank.md`, `Django ORM Short/README.md` | ✅ complete |
| **DRF** | [`03_drf.md`](./prompts/03_drf.md) | `Django DRF/` | `Django DRF/Question_Bank.md` | ✅ complete |
| **Python** | [`04_python.md`](./prompts/04_python.md) | `Python/` | `Python/Question_Bank.md`, `Python/README.md` | ✅ (06–08 pending theory review) |
| **React** | [`05_react.md`](./prompts/05_react.md) | `React/` | `React/00_INDEX.md` | ⬜ restructure pending |
| **LangChain** / **LangGraph** | [`06_langchain.md`](./prompts/06_langchain.md) | `LangChain LangGraph/` | `LangChain LangGraph/Question_Bank.md`, `LangChain LangGraph/README.md` | 🟡 (06 RAG enriched; rest queued) |

**Shared references:** [`prompts/candidate_profile.md`](./prompts/candidate_profile.md) (who I am — single source) ·
[`AGENT_INDEX.md`](./AGENT_INDEX.md) (what exists: counts, progress queues) ·
[`My_Interview_Questions.md`](./My_Interview_Questions.md) (questions I was really asked).

**Adding a new stack:** create `prompts/0N_<stack>.md` with the same header table
(Folder · Index · Format · Workflow), start it with "Inherits `00_shared_rules.md`", and add a row above.
