# System Design
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Twelve design scenarios, from the ones asked most often to the less common. For every one, walk the same seven steps: clarify requirements and scale; sketch components; define the graph (state, nodes, edges); choose retrieval and tools; add human checkpoints and safety; plan evaluation; cover production (latency, cost, failure, monitoring). Spend the first two minutes asking questions.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Hard) [Design an internal knowledge assistant for 5,000 employees over Confluence, Jira and PDFs.](#q1)
2. (Hard) [Design an approval workflow agent (promotions, expenses, access requests).](#q2)
3. (Hard) [Design a natural-language-to-data interface ("ask your dashboard").](#q3)
4. (Hard) [Design a customer-support agent that can take actions (refunds, plan changes).](#q4)
5. (Hard) [Your RAG answers were good in testing but users complain in production. What do you do?](#q5)
6. (Hard) [Design a document-processing pipeline that extracts fields from thousands of PDFs a day.](#q6)
7. (Hard) [Design a code-review or engineering-assistant agent for your company.](#q7)
8. (Hard) [Design a research agent that writes a report from web and internal sources.](#q8)
9. (Hard) [Design a meeting-notes and action-items assistant.](#q9)
10. (Hard) [How would you migrate a working prototype (notebook) to production?](#q10)
11. (Hard) [How do you choose between RAG, fine-tuning and a bigger context window?](#q11)
12. (Hard) [Design for reliability: the LLM provider goes down for an hour.](#q12)

---

<a name="q1"></a>
## Q1. (Hard) Design an internal knowledge assistant for 5,000 employees over Confluence, Jira and PDFs.
**Answer:**

1. **Clarify:** sources, freshness, permissions, languages, QPS, citations required?
2. **Ingestion:** connectors, incremental sync, structure-aware chunking, metadata (source, ACL groups, updated date), vector store plus BM25.
3. **Query graph:** classify intent; retrieve (hybrid, ACL-filtered, reranked), call a live tool (Jira status) or ask a clarifying question; generate with citations; groundedness check.
4. **Security:** permission filter at retrieval time.
5. **Evaluation:** golden questions per department; recall@k and faithfulness; thumbs feedback into the dataset.
6. **Production:** caching, streaming, Postgres checkpointer for follow-ups, tracing.

**Tie to your project:** "FinSight's retrieval plus PNI Hub's integrations and Azure AD access control."

*Source ID: 14.1*

---

<a name="q2"></a>
## Q2. (Hard) Design an approval workflow agent (promotions, expenses, access requests).
**Answer:**

1. **State:** case id, requester, evidence, typed AI evaluation, approvals so far, status, audit log.
2. **Nodes:** intake and validation; parallel evidence collection; rule checks in code; LLM evaluation with structured output; route by outcome and risk; `interrupt()` per approver; notify; finalise.
3. **Rules first, LLM second:** eligibility in code; the LLM summarises and recommends with reasons.
4. **Persistence:** Postgres checkpointer; reminders via scheduled jobs; resume with `Command(resume=...)`.
5. **Fairness and audit:** store inputs, model and prompt versions, reasons; humans decide; monitor agreement and bias.

**Tie to your project (P1):** Your flagship story. Tell it as "here is what I built", then show the trade-offs. Have the real \[X%\] ready.

*Source ID: 14.2*

---

<a name="q3"></a>
## Q3. (Hard) Design a natural-language-to-data interface ("ask your dashboard").
**Answer:**

1. Curated, parameterised tools or a semantic layer first; text-to-SQL only on a read-only replica with schema allow-list, validation, row limits and timeouts.
2. Tools like `get_metric(name, team, date_range)` with good descriptions and examples.
3. Answer as a table or chart plus a sentence, with the query shown.
4. User's own permissions; no writes; PII masking.
5. Evaluate correct-result rate on a question set.

**Tie to your project (P3):** "This is my MCP server over PNI Hub." \[Fill: tool list, N teams.\]

*Source ID: 14.3*

---

<a name="q4"></a>
## Q4. (Hard) Design a customer-support agent that can take actions (refunds, plan changes).
**Answer:**

Intent routing; RAG over policy; account lookup and action tools; approval before refunds above a threshold; per-conversation limits; escalation to a human with a summary; evals on resolution rate and policy compliance; streaming; long-term memory of preferences in the Store.

*Source ID: 14.4*

---

<a name="q5"></a>
## Q5. (Hard) Your RAG answers were good in testing but users complain in production. What do you do?
**Answer:**

Pull failing traces and categorise: retrieval misses, generation errors, out-of-scope. Add them to the dataset. Fix by category (query rewriting, hybrid search, re-ingestion, table chunking, stricter prompt, groundedness check, "I don't know" path). Re-run evals before redeploying; keep monitoring.

**Tie to your project (P2):** "Same ablation discipline as FinSight, applied to production failures."

*Source ID: 14.5*

---

<a name="q6"></a>
## Q6. (Hard) Design a document-processing pipeline that extracts fields from thousands of PDFs a day.
**Answer:**

1. Queue-based ingestion (RabbitMQ or Celery); one job per document; idempotent by document hash.
2. Parse (layout-aware), classify document type, extract with a per-type Pydantic schema, validate (types, cross-field rules).
3. Confidence routing: high confidence auto-saves; low confidence or validation failures go to a human review queue.
4. Cheap model for classification, stronger model only for hard extractions; batch and cache.
5. Metrics: field-level accuracy on a labelled sample, review rate, cost per document.

**Tie to your project (P4):** "The internal data-extraction tools and SP-Report automation (2+ hours to seconds, 10,000+ reports) are the same pattern at scale."

*Source ID: 14.6*

---

<a name="q7"></a>
## Q7. (Hard) Design a code-review or engineering-assistant agent for your company.
**Answer:**

Tools: read diff, read files, run linters and tests in a sandbox, search internal docs; a planner that decides which checks to run; structured findings with file and line; comment only above a confidence threshold; humans approve posting. Evaluate on past PRs with known issues.

**Tie to your project:** "PNI Hub integrates Perforce and Jira, so the assistant could link findings to tickets."

*Source ID: 14.7*

---

<a name="q8"></a>
## Q8. (Hard) Design a research agent that writes a report from web and internal sources.
**Answer:**

Planner produces sub-questions; parallel researcher sub-agents (`Send`) search and summarise with citations; a reviewer checks coverage and contradictions; a writer produces the report; a human reviews before sharing. Control cost with step limits and source caps.

*Source ID: 14.8*

---

<a name="q9"></a>
## Q9. (Hard) Design a meeting-notes and action-items assistant.
**Answer:**

Transcribe; chunk by speaker turns; extract decisions and action items with a schema (owner, due date, source quote); confirm owners against the directory; create tasks in Jira only after human approval; store notes for later RAG.

**Tie to your project (P4):** "Jira and Active Directory are already integrated in PNI Hub, which covers owner lookup and task creation."

*Source ID: 14.9*

---

<a name="q10"></a>
## Q10. (Hard) How would you migrate a working prototype (notebook) to production?
**Answer:**

Wrap logic in a service module; add typed inputs and outputs; replace in-memory state with Postgres; add auth, rate limits and logging; add a fake-model test suite and an eval dataset; tracing; deploy behind an API with a feature flag; monitor cost and quality.

**How to say it:** This question tests whether you've shipped. Use PNI Hub's MVP-to-production story.

*Source ID: 14.10*

---

<a name="q11"></a>
## Q11. (Hard) How do you choose between RAG, fine-tuning and a bigger context window?
**Answer:**

RAG for changing knowledge, citations and permissions. Fine-tuning for consistent style, format or a narrow task at lower cost. Long context for a few large documents per request when cost and latency are acceptable. Often combine RAG with a modest context.

*Source ID: 14.11*

---

<a name="q12"></a>
## Q12. (Hard) Design for reliability: the LLM provider goes down for an hour.
**Answer:**

Fallback provider or local model behind the same interface; queue non-urgent jobs and retry later; degrade gracefully (show cached answers or "AI unavailable" while the rest of the app works); alert; circuit breaker to stop hammering the provider.

**Tie to your project (P2):** "FinSight already runs on Ollama or Claude behind one interface, which is exactly the fallback design."

*Source ID: 14.12*
