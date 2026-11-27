# Memory & Chat History
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Fifteen questions on conversation memory, long-term memory and context management. A common trap: answering with the old `ConversationBufferMemory` classes. Lead with the modern LangGraph approach and mention the legacy one only for contrast.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [How does memory work in LangChain and LangGraph today?](#q1)
2. (Easy) [Show a minimal chatbot with memory.](#q2)
3. (Easy) [What were the legacy memory classes and why were they replaced?](#q3)
4. (Easy) [The conversation exceeds the context window. What do you do?](#q4)
5. (Medium) [Trimming versus summarising: trade-offs?](#q5)
6. (Medium) [How do you design long-term memory?](#q6)
7. (Medium) [What are semantic, episodic and procedural memory?](#q7)
8. (Medium) [How do you keep memory per user in a multi-user Django app?](#q8)
9. (Medium) [Where do you store chat history for the UI?](#q9)
10. (Medium) [How do you handle privacy and deletion in memory?](#q10)
11. (Medium) [How do you make memory useful but not noisy?](#q11)
12. (Medium) [How does memory interact with tools and agents?](#q12)
13. (Hard) [What is the difference between state and memory in LangGraph?](#q13)
14. (Hard) [How would you test memory?](#q14)
15. (Hard) [How do you summarise long evidence instead of long chat?](#q15)

---

<a name="q1"></a>
## Q1. (Easy) How does memory work in LangChain and LangGraph today?
**Answer:** LLMs are stateless; memory means storing messages and sending the relevant ones back each turn. Two kinds:

- **Short-term (thread) memory:** the conversation in one thread, kept in graph state and saved by a **checkpointer** keyed by `thread_id`. `create_agent` uses it automatically when you pass a checkpointer.
- **Long-term memory:** facts across threads (preferences, past decisions), kept in the LangGraph **Store** by namespace, such as `("users", user_id)`, with optional semantic search.

**Simple version:** Short-term = this conversation's chat log; long-term = a notebook about the user that every conversation can read.

**Tie to your project (P1):** "Each promotion case is one thread, so its history survives restarts; reusable knowledge like criteria per role belongs in a store." \[Guess.\]

*Source ID: 5.1*

---

<a name="q2"></a>
## Q2. (Easy) Show a minimal chatbot with memory.
**Answer:**

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(model, tools=[], checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "user42:chat1"}}
agent.invoke({"messages": [{"role": "user", "content": "I'm Gaurav"}]}, cfg)
agent.invoke({"messages": [{"role": "user", "content": "What's my name?"}]}, cfg)  # remembers
```

**How to say it:** "Same `thread_id` = same memory. In production, swap `InMemorySaver` for `PostgresSaver`."

*Source ID: 5.2*

---

<a name="q3"></a>
## Q3. (Easy) What were the legacy memory classes and why were they replaced?
**Answer:** `ConversationBufferMemory` (all messages), `ConversationBufferWindowMemory` (last k), `ConversationSummaryMemory` (running summary), `ConversationSummaryBufferMemory` (summary plus recent), `ConversationEntityMemory`, and `RunnableWithMessageHistory` for LCEL. They were tied to old chains, hard to persist across workers and didn't handle tool messages well. LangGraph persistence covers all of these patterns.

*Source ID: 5.3*

---

<a name="q4"></a>
## Q4. (Easy) The conversation exceeds the context window. What do you do?
**Answer:**

1. **Trim** with `trim_messages` (by tokens), always keep the system message, never split a tool call from its result.
2. **Summarise** older turns (`SummarizationMiddleware` does it automatically at a token threshold).
3. **Retrieve** relevant old turns or facts instead of sending everything.
4. **Delete** with `RemoveMessage(id=...)` in LangGraph.

**How to say it:** Mention the tool-call pairing rule. It separates people who built it from people who read about it.

*Source ID: 5.4*

---

<a name="q5"></a>
## Q5. (Medium) Trimming versus summarising: trade-offs?
**Answer:** Trimming is cheap and exact but forgets old facts. Summarising keeps the gist but costs an extra LLM call and can lose or distort details. Common mix: summary of old turns plus the last N messages verbatim, plus long-term facts stored separately.

*Source ID: 5.5*

---

<a name="q6"></a>
## Q6. (Medium) How do you design long-term memory?
**Answer:** Decide what to remember (profile facts, preferences, past decisions, learned instructions), when to write (in the hot path via a tool the agent calls, or in the background after the conversation), how to retrieve (by key, or semantic search in the Store), and how to update or forget (overwrite, timestamps, user-visible delete).

**Simple version:** Choose what goes into the notebook, when you write it, and how you find it later.

*Source ID: 5.6*

---

<a name="q7"></a>
## Q7. (Medium) What are semantic, episodic and procedural memory?
**Answer:** Semantic = facts ("Gaurav uses Django"). Episodic = past experiences or examples ("last time this query failed because..."), often used as few-shot examples. Procedural = how to behave (instructions or prompts the agent updates over time).

*Source ID: 5.7*

---

<a name="q8"></a>
## Q8. (Medium) How do you keep memory per user in a multi-user Django app?
**Answer:** `thread_id` per conversation (for example `f"{user_id}:{conversation_id}"`), `user_id` in runtime context for Store namespaces, a durable shared checkpointer (`PostgresSaver`), and an ownership check in the API before resuming a thread.

**Tie to your project (P4):** "Identity comes from Azure AD via MSAL and RBAC; I reuse that user id for thread ownership so AI features follow the platform's access rules."

*Source ID: 5.8*

---

<a name="q9"></a>
## Q9. (Medium) Where do you store chat history for the UI?
**Answer:** Either read it from the checkpointer (`graph.get_state(config).values["messages"]`) or keep your own `Conversation` and `Message` Django models for listing, search and retention. Many teams do both: checkpointer for the agent, Django models as the system of record.

*Source ID: 5.9*

---

<a name="q10"></a>
## Q10. (Medium) How do you handle privacy and deletion in memory?
**Answer:** Don't store secrets or unneeded PII; redact before saving; set retention periods; support user delete (delete thread checkpoints and Store items by namespace); encrypt at rest; restrict who can read traces.

*Source ID: 5.10*

---

<a name="q11"></a>
## Q11. (Medium) How do you make memory useful but not noisy?
**Answer:** Store only facts that change future answers, de-duplicate, keep timestamps so newer facts win, cap how many memories you inject per call, and evaluate: does memory improve answers on a test set?

*Source ID: 5.11*

---

<a name="q12"></a>
## Q12. (Medium) How does memory interact with tools and agents?
**Answer:** Tool calls and results are messages in state too, so they consume context. Large tool outputs should be summarised or stored outside state (return an id, not 10,000 rows). Agents can also get memory tools such as `save_memory` and `search_memory`.

**Tie to your project (P3):** "PNI Hub queries can return thousands of rows, so tools return summaries or the top N rows plus a count, not raw dumps."

*Source ID: 5.12*

---

<a name="q13"></a>
## Q13. (Hard) What is the difference between state and memory in LangGraph?
**Answer:** State is the data flowing through one run (messages plus your fields). With a checkpointer, that state persists per thread, which is short-term memory. The Store is separate, cross-thread long-term memory.

*Source ID: 5.13*

---

<a name="q14"></a>
## Q14. (Hard) How would you test memory?
**Answer:** Scripted multi-turn conversations in tests: tell a fact in turn 1, ask in turn 5, assert it's used; test that different `thread_id`s don't leak into each other; test trimming keeps tool pairs valid.

*Source ID: 5.14*

---

<a name="q15"></a>
## Q15. (Hard) How do you summarise long evidence instead of long chat?
**Answer:** Same idea: summarise each source once in its own step, store the summary in state, and pass summaries forward instead of raw text.

**Tie to your project (P1):** "Promotion evidence (Jira history, reviews) can be long, so I summarise each source once and pass the summaries forward." \[Guess.\]

*Source ID: 5.15*
