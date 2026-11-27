# Production & Django
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Sixteen questions on running LLM features in production, with a Django focus. This is where 7 years of PNI Hub-style engineering sets you apart from candidates who only built notebooks.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [How do you integrate a LangGraph agent into a Django/DRF app?](#q1)
2. (Easy) [Where should the graph run: web process or worker?](#q2)
3. (Easy) [Celery or RabbitMQ consumers for agent jobs?](#q3)
4. (Easy) [LangSmith Deployment (formerly LangGraph Platform) or self-host?](#q4)
5. (Medium) [How do you control cost and latency?](#q5)
6. (Medium) [What is semantic caching and when is it risky?](#q6)
7. (Medium) [How do you handle errors in production agents?](#q7)
8. (Medium) [How do you secure an LLM feature in an enterprise app?](#q8)
9. (Medium) [How do you test LangChain and LangGraph code?](#q9)
10. (Medium) [How do you deploy and version agents safely?](#q10)
11. (Medium) [How do you scale to many concurrent users?](#q11)
12. (Medium) [How do you make agent outputs auditable?](#q12)
13. (Hard) [How do you handle multi-tenancy?](#q13)
14. (Hard) [How do you expose an agent as an API?](#q14)
15. (Hard) [What are guardrails and how do you add them?](#q15)
16. (Hard) [What would you monitor on day one after launch?](#q16)

---

<a name="q1"></a>
## Q1. (Easy) How do you integrate a LangGraph agent into a Django/DRF app?
**Answer:**

1. **API layer (DRF):** authenticate (Azure AD / OAuth), authorise, validate with a serializer, map user and case to a `thread_id`.
2. **Service layer:** build and compile the graph once at startup with a shared Postgres checkpointer.
3. **Execution:** short runs in an async view; long runs in a worker (Celery or RabbitMQ consumer); return a run id and stream or poll progress.
4. **Tools call your existing services** (ORM, internal APIs) so permissions and business rules apply.
5. **Results** (decisions, audit) go into your own Django models.

**Simple version:** Django is the front door and rulebook; LangGraph is a worker behind it.

**Tie to your project (P4 and P1):** "That's how the promotion workflow sits in our stack: DRF with Azure AD, graph behind it, tools reading Jira, Perforce and Workfront data through PNI Hub's integrations." \[Adjust to real architecture.\]

*Source ID: 13.1*

---

<a name="q2"></a>
## Q2. (Easy) Where should the graph run: web process or worker?
**Answer:** Web process for short interactive runs (seconds) with streaming. Worker for anything long, batchy or waiting on external systems, so web workers aren't tied up and retries are controlled. Human-waiting runs don't need a process at all; they sit in the checkpointer until resumed.

*Source ID: 13.2*

---

<a name="q3"></a>
## Q3. (Easy) Celery or RabbitMQ consumers for agent jobs?
**Answer:** Celery (with RabbitMQ or Redis as broker) gives retries, scheduling, routing and monitoring out of the box. Raw consumers give more control. Either way: idempotent tasks, timeouts, a dead-letter queue, and job status stored in the DB.

**Tie to your project (P4):** "PNI Hub already uses RabbitMQ and scheduled jobs, so agent jobs fit the existing pattern."

*Source ID: 13.3*

---

<a name="q4"></a>
## Q4. (Easy) LangSmith Deployment (formerly LangGraph Platform) or self-host?
**Answer:** Managed gives task queues, persistence, streaming endpoints, cron, double-texting handling and Studio without infra work. Self-hosting in Django or FastAPI keeps data inside the network and reuses your auth, but you build queues and scaling. Enterprise internal data usually pushes to self-hosting.

**Tie to your project:** "Internal data and Azure AD made self-hosting the natural choice." \[Guess.\]

*Source ID: 13.4*

---

<a name="q5"></a>
## Q5. (Medium) How do you control cost and latency?
**Answer:** Route simple tasks to small models; cache responses (Redis, `set_llm_cache`) and embeddings; shrink prompts; parallelise; stream; batch offline work; cap tokens; track cost per request.

**Tie to your project (P4 and P2):** "PNI Hub's Redis and cache-warming jobs can serve an LLM cache; FinSight runs on Ollama at zero API cost."

*Source ID: 13.5*

---

<a name="q6"></a>
## Q6. (Medium) What is semantic caching and when is it risky?
**Answer:** Reuse an earlier answer when a new question's embedding is very similar. Risky when small wording changes matter ("FY2022" vs "FY2023"), when answers depend on the user's permissions, or when data changes. Scope caches per permission set and set expiry.

*Source ID: 13.6*

---

<a name="q7"></a>
## Q7. (Medium) How do you handle errors in production agents?
**Answer:** Retries with backoff, model fallbacks, tools returning helpful errors, structured-output validation with a retry or human route, recursion and time limits, idempotent side effects, an explicit "needs human" end state, and alerts on error and fallback rates.

*Source ID: 13.7*

---

<a name="q8"></a>
## Q8. (Medium) How do you secure an LLM feature in an enterprise app?
**Answer:** AuthN/AuthZ in the API; tools scoped to the caller; read-only by default with approval for writes; PII redaction or local models; secrets in a vault; audit logs; trace retention rules; prompt-injection defences.

**Tie to your project (P3 and P4):** "PNI Hub uses Azure AD, OAuth 2.0, MSAL and RBAC; the MCP server and agents reuse that identity."

*Source ID: 13.8*

---

<a name="q9"></a>
## Q9. (Medium) How do you test LangChain and LangGraph code?
**Answer:** Unit-test nodes as plain functions; fake chat models (`GenericFakeChatModel`) for deterministic routing and tool tests; compiled-graph tests with `InMemorySaver`; separate, non-blocking LLM-quality evals.

**Tie to your project (P2):** "FinSight has pytest coverage; model-dependent evals run as separate experiments."

*Source ID: 13.9*

---

<a name="q10"></a>
## Q10. (Medium) How do you deploy and version agents safely?
**Answer:** Versioned prompts and graph code, feature flags, canary or shadow mode (run the new version on real traffic without showing results), compare metrics, then roll out. Keep old graph versions for in-flight threads.

*Source ID: 13.10*

---

<a name="q11"></a>
## Q11. (Medium) How do you scale to many concurrent users?
**Answer:** Stateless web workers (state in the checkpointer), async I/O, connection pooling for Postgres (the checkpointer is write-heavy), horizontal scaling of workers, rate limiting per user, and queueing for bursts. Watch provider rate limits; they are often the real ceiling.

**Tie to your project (P4):** "PNI Hub uses custom Django DB routers and connection pooling across Postgres and MSSQL; the checkpointer is one more heavy writer to plan for."

*Source ID: 13.11*

---

<a name="q12"></a>
## Q12. (Medium) How do you make agent outputs auditable?
**Answer:** Store inputs, retrieved sources, tool calls, model and prompt versions, outputs and human decisions per run, linked to the trace id. Keep it in your own DB, because traces may expire.

**Tie to your project (P1):** "For promotions, audit is a requirement, not a nice-to-have."

*Source ID: 13.12*

---

<a name="q13"></a>
## Q13. (Hard) How do you handle multi-tenancy?
**Answer:** Tenant id in every thread id, Store namespace, vector metadata filter and cache key; per-tenant rate limits and cost tracking; never share caches across tenants.

*Source ID: 13.13*

---

<a name="q14"></a>
## Q14. (Hard) How do you expose an agent as an API?
**Answer:** A DRF or FastAPI endpoint with request and response serializers, run id, sync and streaming variants, idempotency keys for retries, and OpenAPI docs. Or expose it as an MCP server for AI clients.

**Tie to your project (P4 and P3):** "I've built 40+ DRF endpoints and an MCP server, so both front doors are familiar."

*Source ID: 13.14*

---

<a name="q15"></a>
## Q15. (Hard) What are guardrails and how do you add them?
**Answer:** Checks on input (topic allow-list, injection detection, PII) and output (schema, policy, groundedness, toxicity) before results reach users or tools. In 1.x, add them as middleware (`before_model`, `after_model`) or as dedicated graph nodes.

*Source ID: 13.15*

---

<a name="q16"></a>
## Q16. (Hard) What would you monitor on day one after launch?
**Answer:** Error rate, p95 latency, cost per request, fallback rate, user feedback, escalation rate, and a daily sample of traces reviewed by a human. Set alerts on sudden changes.

**Tie to your project (P4):** "For PNI Hub launches I watched adoption and errors first; for AI features I add cost and quality."

*Source ID: 13.16*
