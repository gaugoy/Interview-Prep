# LangChain Fundamentals
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Sixteen questions on what LangChain is, how it is packaged and when to use it. These are often the warm-up questions, so answer crisply and move to your projects quickly. Project codes: P1 promotion workflow, P2 FinSight RAG, P3 PNI Hub MCP server, P4 PNI Hub platform.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [What is LangChain and why use it instead of calling the LLM API directly?](#q1)
2. (Easy) [How is LangChain packaged in v1.x?](#q2)
3. (Easy) [What is the difference between LangChain, LangGraph and LangSmith?](#q3)
4. (Easy) [What are the core components of LangChain?](#q4)
5. (Medium) [What are messages and what message types exist?](#q5)
6. (Medium) [What changed in LangChain 1.0?](#q6)
7. (Medium) [How do you migrate from `AgentExecutor` or `LLMChain` to 1.x?](#q7)
8. (Medium) [When would you NOT use LangChain?](#q8)
9. (Medium) [What are common criticisms of LangChain, and how do you respond?](#q9)
10. (Medium) [What is a document loader and a text splitter?](#q10)
11. (Medium) [What is the `Document` object?](#q11)
12. (Medium) [What is the difference between an LLM and a chat model in LangChain?](#q12)
13. (Hard) [What are callbacks?](#q13)
14. (Hard) [What is `RunnableConfig` and what can you pass in it?](#q14)
15. (Hard) [How do you keep LangChain upgrades from breaking production?](#q15)
16. (Hard) [Is LangChain only for Python?](#q16)

---

<a name="q1"></a>
## Q1. (Easy) What is LangChain and why use it instead of calling the LLM API directly?
**Answer:** LangChain is an open-source framework that gives one standard interface for chat models, prompts, tools, retrievers and vector stores, plus ready-made patterns (RAG, agents). It saves you from writing provider-specific plumbing, lets you swap providers in one line, and gives LangSmith tracing for free. Skip it when the task is one prompt and one API call.

**Simple version:** LangChain is like Django for LLM apps: standard parts so you don't hand-write the plumbing every time.

**How to say it:** "I treat LangChain as an integration and abstraction layer. I use it where it saves real work, like model swapping and tool calling, and drop to the raw SDK when the abstraction gets in the way."

**Tie to your project (P2):** "FinSight runs on Ollama locally with Claude as an optional provider. A provider-neutral model interface is exactly what LangChain gives you."

*Source ID: 1.1*

---

<a name="q2"></a>
## Q2. (Easy) How is LangChain packaged in v1.x?
**Answer:**

- `langchain-core`: base abstractions (Runnables, messages, prompts, tools interface). Small and stable.
- `langchain`: `create_agent`, middleware, `init_chat_model`, high-level helpers.
- Provider packages: `langchain-openai`, `langchain-anthropic`, `langchain-ollama`, `langchain-qdrant`, and so on.
- `langchain-community`: community-maintained integrations.
- `langchain-classic`: legacy chains (`LLMChain`, `RetrievalQA`) and memory classes.
- `langgraph` and `langsmith` are separate packages.

**Simple version:** A small core, one package per provider, and the old stuff moved to a "classic" box.

**How to say it:** "Splitting providers into their own packages means I only install what I use and can pin versions per provider."

*Source ID: 1.2*

---

<a name="q3"></a>
## Q3. (Easy) What is the difference between LangChain, LangGraph and LangSmith?
**Answer:** LangChain = building blocks and `create_agent`. LangGraph = low-level runtime for stateful, multi-step workflows with persistence, interrupts and streaming (LangChain 1.x agents run on it). LangSmith = tracing, evaluation, prompt management and deployment.

**Simple version:** The parts, the engine, and the dashboard.

**Tie to your project (P1):** "The promotion workflow needed fixed steps, routing and an approval pause, so I built it in LangGraph rather than a plain agent loop."

*Source ID: 1.3*

---

<a name="q4"></a>
## Q4. (Easy) What are the core components of LangChain?
**Answer:** Chat models, messages, prompt templates, output parsers and structured output, document loaders, text splitters, embeddings, vector stores, retrievers, tools, agents and middleware. Everything that runs implements the Runnable interface.

**How to say it:** Name them in the order data flows: load, split, embed, store, retrieve, prompt, model, parse.

**Tie to your project (P2):** "FinSight has the same stages: PDF parsing, chunking, embeddings, Qdrant and BM25 indexing, retrieval, then a grounded, cited answer."

*Source ID: 1.4*

---

<a name="q5"></a>
## Q5. (Medium) What are messages and what message types exist?
**Answer:** Chat models take and return lists of messages. `SystemMessage` (instructions), `HumanMessage` (user input), `AIMessage` (model output, may contain `tool_calls`), `ToolMessage` (result of a tool, linked by `tool_call_id`). In v1, messages carry standard `content_blocks` (text, reasoning, images, citations, tool calls) so they look the same across providers. Messages also carry `usage_metadata` with token counts.

**Simple version:** A chat log where each line is tagged with who said it.

**How to say it:** Mention that a `ToolMessage` must follow the `AIMessage` that requested it, or the provider rejects the request. That detail shows hands-on experience.

*Source ID: 1.5*

---

<a name="q6"></a>
## Q6. (Medium) What changed in LangChain 1.0?
**Answer:** `create_agent` replaces `initialize_agent`, `AgentExecutor` and LangGraph's `create_react_agent`; middleware hooks into the agent loop; standard content blocks; structured output built into the agent loop via `response_format`; legacy chains and memory moved to `langchain-classic`; Python 3.10+.

**How to say it:** "In 1.x I build agents with `create_agent` and add behaviour through middleware instead of custom executors."

**Tie to your project:** If parts of your Qualcomm code predate 1.0, say so: "I know how 0.x patterns map to 1.x."

*Source ID: 1.6*

---

<a name="q7"></a>
## Q7. (Medium) How do you migrate from `AgentExecutor` or `LLMChain` to 1.x?
**Answer:** `LLMChain(prompt, llm)` becomes `prompt | llm | parser`. `RetrievalQA` becomes an LCEL RAG chain or a small LangGraph. `AgentExecutor` becomes `create_agent(model, tools, system_prompt=...)`; custom loop logic moves into middleware; memory moves to a checkpointer with `thread_id`. Pin versions, migrate one chain at a time, and compare outputs on an eval set before switching.

**Simple version:** Replace old wrappers with pipes and the new agent function, and test before and after.

*Source ID: 1.7*

---

<a name="q8"></a>
## Q8. (Medium) When would you NOT use LangChain?
**Answer:** One LLM call; latency-critical paths; a provider feature the wrapper doesn't expose yet; or a team that can't keep up with library changes. Many teams use LangGraph for orchestration but call SDKs directly inside nodes.

**Tie to your project (P2):** "I built FinSight's retrieval in plain Python for full control during ablations. I'd wrap it as a LangChain retriever when plugging it into an agent." \[Assumption: FinSight doesn't use LangChain.\]

*Source ID: 1.8*

---

<a name="q9"></a>
## Q9. (Medium) What are common criticisms of LangChain, and how do you respond?
**Answer:** Too many abstractions, fast-moving APIs, hard-to-read stack traces, and outdated tutorials. v1 answered much of this: smaller core, one agent API, stable `langchain-core`. Mitigations: pin versions, use only the pieces you need, read traces in LangSmith, and wrap LangChain behind your own service interface so you can replace it.

**How to say it:** Balanced, not defensive. "I use it deliberately, behind my own interfaces."

*Source ID: 1.9*

---

<a name="q10"></a>
## Q10. (Medium) What is a document loader and a text splitter?
**Answer:** Loaders read sources into `Document` objects (`page_content` + `metadata`): PDFs (`PyPDFLoader`), web pages, Confluence, CSV, and many more. Splitters cut documents into chunks: `RecursiveCharacterTextSplitter` (most common), token-based splitters, Markdown/HTML header splitters, and semantic chunkers.

**Tie to your project (P2):** "PDF parsing for SEC filings was the hardest loader problem: tables and multi-column layouts. That's why chunking strategy was one of my ablation axes."

*Source ID: 1.10*

---

<a name="q11"></a>
## Q11. (Medium) What is the `Document` object?
**Answer:** A simple container with `page_content` (text) and `metadata` (dict: source, page, section, dates, ACL tags). Metadata drives filtering, citations and access control, so you design it deliberately.

**Simple version:** A chunk of text with a label on it saying where it came from.

*Source ID: 1.11*

---

<a name="q12"></a>
## Q12. (Medium) What is the difference between an LLM and a chat model in LangChain?
**Answer:** Old "LLM" classes took a string and returned a string (completion models). Chat models take messages and return an `AIMessage`, and support tool calling and structured output. Modern code uses chat models only.

*Source ID: 1.12*

---

<a name="q13"></a>
## Q13. (Hard) What are callbacks?
**Answer:** Hooks fired on events (chain start or end, LLM start, new token, tool start, error). Used for logging, streaming tokens, cost tracking and custom monitoring. Passed via `config={"callbacks": [...]}`. In practice, LangSmith tracing and `astream_events` cover most needs.

**Tie to your project (P4):** "It's similar to Django signals: you react to events without changing the core code."

*Source ID: 1.13*

---

<a name="q14"></a>
## Q14. (Hard) What is `RunnableConfig` and what can you pass in it?
**Answer:** A dict passed to `invoke(input, config)`: `tags`, `metadata`, `callbacks`, `run_name`, `max_concurrency`, `recursion_limit`, and `configurable` (for example `thread_id`, or runtime-selectable fields). It flows through every nested step.

**How to say it:** "I put user id and request id in metadata so every trace in LangSmith can be tied back to a Django request."

*Source ID: 1.14*

---

<a name="q15"></a>
## Q15. (Hard) How do you keep LangChain upgrades from breaking production?
**Answer:** Pin exact versions, read release notes, run deterministic tests (fake models) plus an eval set before upgrading, upgrade in a branch, watch deprecation warnings, and roll out behind a feature flag.

**Tie to your project (P4):** "Same as Django upgrades in PNI Hub: pinned versions, CI tests, staged rollout."

*Source ID: 1.15*

---

<a name="q16"></a>
## Q16. (Hard) Is LangChain only for Python?
**Answer:** No. There is LangChain.js / LangGraph.js with near-parity APIs. Python is the main ecosystem for data and ML work.

**Tie to your project:** "With my React and TypeScript background, I could use LangGraph.js for front-end-adjacent features, but I'd keep agents in Python next to our Django services."

*Source ID: 1.16*
