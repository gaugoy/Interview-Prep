# 06 — LangChain & LangGraph (GenAI) · say **"LangChain"** or **"LangGraph"**

Inherits [`00_shared_rules.md`](./00_shared_rules.md).

| | |
|---|---|
| **Folder** | `LangChain LangGraph/` (14 topic files, `01_…` to `14_…`) |
| **Index to read first** | `LangChain LangGraph/Question_Bank.md` · `LangChain LangGraph/README.md` (topic table + counts) |
| **Reference answer** | [`06_RAG.md`](../LangChain%20LangGraph/06_RAG.md) is the gold-standard format and depth. Copy its shape |
| **Don't touch** | `Python Coding Round/` (separate folder for hands-on rounds) and the README project stories, unless I ask |
| **Versions** | LangChain 1.x, LangGraph 1.x, current `langchain-core`, `langgraph`, `langsmith` |

## Answer frame (in this order; skip a part only when it adds nothing)

1. **Answer:** 3–6 sentences I can say out loud in 20–30 seconds. Plain English first: what it is, why it exists, the trade-off.
2. **How it works:** steps, a short ASCII diagram, or a comparison table when there are 2+ options.
3. **Formula:** in a ```` ```text ```` block whenever the topic has one (similarity, BM25, RRF, recall@k, MRR, nDCG, MMR, faithfulness, token or cost budget, chunk count, storage). Explain every symbol in one line, then give a **worked example with real numbers**.
4. **Example:** a concrete input → output, preferably from the finance or SEC-filing domain or PNI Hub.
5. **Code:** short (≤ ~40 lines), runnable-looking, with correct imports. Only when it is the syntax interviewers expect or it makes the idea clearer. Never code on its own.
6. **Follow-up:** / **Gotcha:** one line each, only where interviewers commonly push.
7. Keep any existing **Simple version:**, **How to say it:** and **Tie to your project (Pn):** lines, and `*Source ID: F.N*` (F = file number, N = question number).

Depth by level: **(Easy)** Answer + 1–2 supporting parts · **(Medium)** full frame · **(Hard)** full frame plus trade-offs and production concerns (cost, latency, security, monitoring).

A **Formula cheat sheet** table sits under the intro of any file that uses formulas (see `06_RAG.md`).

## Correctness rules (LangChain moves fast)

- Use 1.x import paths: `langchain_core.*`, provider packages (`langchain_ollama`, `langchain_qdrant`, `langchain_openai`, `langchain_anthropic`, `langchain_postgres`), `langchain_text_splitters`, and `langchain.agents.create_agent`.
- Legacy retrievers, chains and memory live in **`langchain_classic`**: `EnsembleRetriever`, `ContextualCompressionRetriever`, `MultiQueryRetriever`, `ParentDocumentRetriever`, `MultiVectorRetriever`, `SQLRecordManager`, `CacheBackedEmbeddings`, `LLMChain`, `RetrievalQA`. Say so the first time a file uses one, and mention the 0.3 path (`langchain.retrievers`).
- No `AgentExecutor`, `initialize_agent`, `ConversationBufferMemory` or `LLMChain` in new answers, except to explain migration.
- LangGraph: `StateGraph`, `START`, `END`, `add_conditional_edges`, `Command`, `Send`, `interrupt()`, checkpointers (`InMemorySaver`, `PostgresSaver`), `thread_id` in `config["configurable"]`.
- When unsure of an API, check the installed package source or docs (`pip download langchain-classic` into the scratchpad) instead of guessing. Mark version-specific behaviour explicitly.
- Label made-up illustrative numbers as "(illustrative)". Never present them as the candidate's results.

## Candidate projects (from `LangChain LangGraph/README.md`; never invent metrics)

| Code | Project | Use for |
|---|---|---|
| P1 | Promotion workflow automation at Qualcomm (LangChain + LangGraph, human approval) | LangGraph, routing, HITL, checkpointing, structured output |
| P2 | FinSight RAG over SEC filings (Qdrant, BM25, rerank, Ollama, FinanceBench: 99% filing, 61% top-10 page) | RAG, chunking, hybrid, reranking, evaluation |
| P3 | MCP server over PNI Hub data | Tools, MCP, tool schemas, safe NL querying |
| P4 | PNI Hub platform (Django, DRF, Postgres + MSSQL, Redis, RabbitMQ, Azure AD, 10 scheduled jobs) | Production, auth, ACLs, queues, caching |

Only the numbers above are real. Every other metric stays as `\[Fill: …\]`. Keep existing `[Fill]` markers. Never delete them or fill them with guesses.

## Format

```text
<a name="qN"></a>
## QN. (Easy|Medium|Hard) <Question title>
**Answer:** ...

*Source ID: F.N*

---
```
- Numbering is continuous per file. TOC at the top: `N. (Level) [Title](#qN)`.
- Changing a **title** means updating the same line in `Question_Bank.md`, because the bank links by `./0F_File.md#qN` with the exact title.
- Cross-links use anchors only: `./08_LangGraph_Core.md#q5`, and one jump only.

## Workflow

1. Find the question with `tools/find.py` (or `Question_Bank.md`) and open **only** that block or file.
2. Improve in place, keeping title, anchor and Source ID unless I ask to change them.
3. New question: gap-check `Question_Bank.md`, append it at the end of the right topic file, update the file TOC, add a `Question_Bank.md` line, and update the **Questions** count in `LangChain LangGraph/README.md` (topic table and the "220 questions" total).
4. **Validate:** `python3 tools/validate.py --file "LangChain LangGraph/<file>.md"` → 0 errors (anchors, `**Answer:**`, python blocks parse, links, Question_Bank sync). Then `python3 tools/build_index.py`. Hooks run both automatically. Find questions with `python3 tools/find.py <words> --stack "LangChain LangGraph"`. When a file is fully reviewed, add it to `REVIEWED_FILES` in `tools/catalog.py`.
5. Finish with a short summary: what changed, how it was verified, which `[Fill]` items I still need to supply.

## Queue (suggested order, matching the README reading order)

- [x] `06_RAG.md`: theory, formulas, examples and code added
- [ ] `08_LangGraph_Core.md`
- [ ] `09_Checkpointing_and_HITL.md`
- [ ] `07_Tools_and_Agents.md`
- [ ] `04_Models_and_Structured_Output.md`
- [ ] `13_Production_and_Django.md`
- [ ] `12_LangSmith_and_Evaluation.md` (metrics formulas: link to `06_RAG.md#q11` instead of duplicating)
- [ ] `01`, `02`, `03`, `05`, `10`, `11`, `14`
