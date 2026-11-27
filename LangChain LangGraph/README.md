# 🦜 LangChain & LangGraph — Interview Preparation (GenAI)

All LangChain and LangGraph interview questions, split by topic, from basics to system design (LangChain 1.x / LangGraph 1.x). Every answer follows the same frame: **the answer → a simple version → how to say it in the interview → how to tie it to your project (P1–P4)**. Difficulty: **(Easy)** · **(Medium)** · **(Hard)**.

- **[Question_Bank.md](./Question_Bank.md)** — every question in one list (fastest way to revise).
- Hands-on coding rounds live in [`../Python Coding Round/`](../Python%20Coding%20Round/README.md).

## Topic files

| File | What's inside | Questions |
|---|---|---|
| [LangChain Fundamentals](./01_LangChain_Fundamentals.md) | What LangChain is, packages, v1.0 changes, migration | 16 |
| [LCEL & Runnables](./02_LCEL_and_Runnables.md) | Runnables, pipe operator, Parallel/Lambda/Passthrough RAG chain | 15 |
| [Prompts & Prompt Engineering](./03_Prompts.md) | Templates, few-shot, injection, versioning, caching | 15 |
| [Models & Structured Output](./04_Models_and_Structured_Output.md) | Model choice, structured output, Pydantic, local models | 15 |
| [Memory & Chat History](./05_Memory_and_Chat_History.md) | Checkpointer memory, Store, trimming, summarising | 15 |
| [RAG (Retrieval-Augmented Generation)](./06_RAG.md) | Chunking, hybrid search, reranking, evaluation, FinSight numbers | 20 |
| [Tools & Agents](./07_Tools_and_Agents.md) | Tool calling, create\_agent, MCP, middleware, approvals | 18 |
| [LangGraph Core](./08_LangGraph_Core.md) | State, reducers, edges, Command, Send, subgraphs | 18 |
| [Checkpointing & Human-in-the-Loop](./09_Checkpointing_and_HITL.md) | Checkpointers, interrupt(), resume, time travel | 15 |
| [Multi-Agent Systems](./10_Multi_Agent_Systems.md) | Supervisor, swarm, handoffs, failure modes | 15 |
| [Streaming & Async](./11_Streaming_and_Async.md) | Stream modes, SSE vs WebSocket in Django, async | 15 |
| [LangSmith & Evaluation](./12_LangSmith_and_Evaluation.md) | Tracing, datasets, LLM-as-judge, CI evals | 15 |
| [Production & Django](./13_Production_and_Django.md) | DRF integration, workers, cost, security, scaling | 16 |
| [System Design](./14_System_Design.md) | Knowledge assistant, approval workflow, NL-to-data, and more | 12 |

## Suggested reading order

**RAG** ([06](./06_RAG.md)), **LangGraph core** ([08](./08_LangGraph_Core.md)) and **Checkpointing** ([09](./09_Checkpointing_and_HITL.md)) first, because they match your strongest projects. Then **Tools and agents** ([07](./07_Tools_and_Agents.md)), **Models and structured output** ([04](./04_Models_and_Structured_Output.md)) and **Production** ([13](./13_Production_and_Django.md)).

## How to use this guide

This guide has 220 questions across 14 topic files, from basics to system design, and every answer is tied to a project on your GenAI CV in Google Drive. Read one topic file a day, say the "How to say it" lines out loud, and fill in the \[bracketed\] numbers before your first interview.

**Hands-on coding round prep:** for the 10 to 15 minute Python coding rounds at service companies (strings, lists, numbers, patterns, dicts, regex), see [Python Coding Round](../Python%20Coding%20Round/README.md).

**Your four anchor projects** (from "Gaurav Goyal - Senior AI & Full-Stack Engineer (GenAI) CV"):

| Code | Project | What it proves |
| --- | --- | --- |
| P1 | Promotion workflow automation at Qualcomm (LangChain + LangGraph) | Stateful agents, routing, human approval, checkpointing |
| P2 | FinSight RAG over SEC filings (Qdrant, BM25, rerank, Ollama) | Retrieval quality, chunking, evaluation with real numbers: 99% filing, 61% top-10 page |
| P3 | MCP server over PNI Hub data | Tools, tool schemas, safe natural-language querying |
| P4 | PNI Hub platform (Django, DRF, Postgres + MSSQL, Redis, RabbitMQ, Azure AD) | Production engineering: APIs, auth, queues, caching, 7+ teams, 100% adoption |

Your CV also mentions internal LLM tools for data extraction and validation; this guide treats them as part of P1/P3 when talking about structured output.

**Fill these before interviewing** (they are blank on your CV): promotion effort saved \[X%\], hours saved \[X hours/week\], MCP adoption \[N teams\]. Interviewers always ask "how much did it help?"

**Guesses I made** (correct me and I will update the answers):

- I assumed FinSight RAG is written in plain Python, not LangChain. The answers show you how to say that as a strength.
- I assumed the promotion workflow has a human approval step (manager or committee) and runs behind your Django stack. The P1 stories describe that design.
- Version details assume LangChain 1.x and LangGraph 1.x (the 1.0 releases came out in Oct 2025). Check the docs for any API renamed after that.

**Answer framework for every question (say it in 60 to 90 seconds):**

1. Definition in one sentence.
2. How it works, in two or three steps.
3. A trade-off or a failure mode (this is what makes you sound senior).
4. "In my project…" with one concrete detail or number.

## Project stories and rapid-fire round

## Your 2-minute project stories (STAR format)

Practise each out loud until it takes under two minutes. Replace every \[bracket\] with a real fact.

**Story A: Promotion workflow automation (P1). Use for: "Tell me about a LangGraph project."**

- **Situation:** Engineering promotion evaluation at Qualcomm was manual: collecting evidence from several systems, checking criteria and routing approvals took \[X hours\] per case across \[N\] cases per cycle.
- **Task:** I owned automating it without taking the decision away from people.
- **Action:** I built a LangGraph workflow: evidence collection from systems PNI Hub already integrates, a structured-output evaluation against promotion criteria, conditional routing by outcome, and an interrupt for approver review, with state persisted so cases can wait for days. \[Name your real checkpointer, models and tools.\]
- **Result:** Manual processing effort down by \[X%\], with \[audit / consistency benefit\]. Approvers make every final decision.
- **What I'd improve:** an evaluation set comparing AI recommendations with final decisions, and bias monitoring.

**Story B: FinSight RAG (P2). Use for: "Tell me about a RAG system" or "How do you evaluate?"**

- **Situation:** Financial filings are long, table-heavy and full of exact terms; naive RAG retrieves the wrong page.
- **Task:** Build grounded, cited Q&A and prove retrieval quality with numbers.
- **Action:** Modular Python 3.12 pipeline, Qdrant plus BM25 with dense, sparse, hybrid and rerank modes behind a YAML CLI; ablations across 4 chunking strategies and two embedding models; config-fingerprinted runs; pytest.
- **Result:** 99% correct filing and 61% gold page in the top 10 on FinanceBench, running fully locally on Ollama.
- **What I'd improve:** table-aware chunking, metadata filters by company and year, a corrective-RAG loop in LangGraph.

**Story C: MCP server for PNI Hub (P3). Use for: "Tell me about tools or agents" or "something innovative".**

- **Situation:** Teams needed answers from PNI Hub data but had to use dashboards or ask someone to write SQL.
- **Action:** Built an MCP server exposing typed, permission-scoped tools over PNI Hub data, usable from Claude and any MCP client.
- **Result:** Adopted by \[N\] teams; \[example question that used to take X minutes\].

**Story D: PNI Hub ownership (P4). Use for: "Biggest system you've owned" or "production experience".**

- 52+ features, 40+ REST APIs, 7+ global teams, 100% adoption, Postgres + MSSQL with custom routers, 5+ enterprise integrations, SP-Report automation from 2+ hours to seconds (10,000+ reports). Close with: "This is the platform my AI work runs on, so I know how to put agents into a real production system, not just a notebook."

## Questions to expect about your CV (prepare these exact answers)

- "Why LangGraph and not just a LangChain agent for the promotion workflow?" (See [Tools & Agents · Q10](./07_Tools_and_Agents.md#q10).)
- "How did you make sure the AI didn't make unfair promotion decisions?" (Humans decide; structured reasons; audit trail; [System Design · Q2](./14_System_Design.md#q2) point 5.)
- "Why is top-10 page retrieval only 61%?" (See [RAG · Q12](./06_RAG.md#q12).)
- "Did you use LangChain in FinSight? Why or why not?" (See [Fundamentals · Q8](./01_LangChain_Fundamentals.md#q8).)
- "What does your MCP server expose, and how is it secured?" (See [Tools & Agents · Q7](./07_Tools_and_Agents.md#q7) and [Tools & Agents · Q16](./07_Tools_and_Agents.md#q16).)
- "How did you measure the \[X%\] effort reduction?" (Before/after time per case, number of cases.)

## Rapid-fire round (one-line answers)

| Question | One-line answer |
| --- | --- |
| `invoke` vs `stream` vs `batch`? | One input, one output / output in chunks / many inputs concurrently. |
| What does `add_messages` do? | Appends messages to state, replaces by id, handles removals. |
| Default state update without a reducer? | Overwrite the key. |
| What is `thread_id`? | The key the checkpointer uses to save and load one conversation or run. |
| What does `interrupt()` need? | A checkpointer and a `thread_id`. |
| How do you resume after an interrupt? | `invoke(Command(resume=value), config)`. |
| `Send` is used for? | Dynamic fan-out (map-reduce) with a runtime number of branches. |
| `Command` is used for? | Update state and choose the next node in one return; handoffs; resume. |
| Production checkpointer? | `PostgresSaver` / `AsyncPostgresSaver`. |
| Short-term vs long-term memory? | Checkpointer (per thread) vs Store (across threads). |
| `with_structured_output` uses what under the hood? | The provider's native structured output or tool calling. |
| Dense vs sparse retrieval? | Meaning via embeddings vs exact keywords via BM25. |
| RRF? | Reciprocal Rank Fusion: merge ranked lists by summing 1/(k + rank). |
| Cross-encoder vs bi-encoder? | Scores query and doc together (accurate, slow) vs embeds separately (fast). |
| Main agent API in LangChain 1.x? | `create_agent`. |
| Where did `LLMChain` go? | `langchain-classic` (legacy). |
| Stream LLM tokens from a graph? | `stream_mode="messages"`. |
| Stop infinite loops? | `recursion_limit` or call-limit middleware. |
| Visual graph debugger? | LangGraph Studio. |
| MCP in one sentence? | An open protocol to expose tools and data to any AI client. |
| Load MCP tools into LangGraph? | `langchain-mcp-adapters`. |
| Trace a non-LangChain function? | `@traceable` from LangSmith. |
| Evaluate an agent's path? | Trajectory evaluation: compare tool-call sequence to expected. |
| Temperature for extraction? | 0. |

## Your closing line

When asked "Any questions for us?", ask one that shows you build real systems: "How do you evaluate your LLM features before release today, and where do agents sit in your production stack?"
