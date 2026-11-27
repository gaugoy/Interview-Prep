# LangGraph Core
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Eighteen questions on LangGraph's building blocks. Expect to be asked to sketch a graph; use your promotion workflow (8.4) as the example every time.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [What is LangGraph and why was it created?](#q1)
2. (Easy) [How do you define state? What are reducers?](#q2)
3. (Easy) [Explain nodes, normal edges and conditional edges.](#q3)
4. (Easy) [Sketch a real graph you built.](#q4)
5. (Easy) [What is `Command` and when do you use it?](#q5)
6. (Medium) [How do you run nodes in parallel? What is `Send`?](#q6)
7. (Medium) [What is a super-step and how does parallel execution handle failures?](#q7)
8. (Medium) [What are subgraphs and how do they share state?](#q8)
9. (Medium) [What are input, output and private state schemas?](#q9)
10. (Medium) [What is the Functional API?](#q10)
11. (Medium) [What is the recursion limit?](#q11)
12. (Medium) [How do you add retries and caching to nodes?](#q12)
13. (Medium) [How do you pass runtime context (user id, DB connection) to nodes?](#q13)
14. (Medium) [How do you visualise and debug a graph?](#q14)
15. (Hard) [How does LangGraph compare with CrewAI, AutoGen or plain Python?](#q15)
16. (Hard) [What is `MessagesState` versus a custom state?](#q16)
17. (Hard) [How do you design state well?](#q17)
18. (Hard) [Graph API versus `create_agent`: which first?](#q18)

---

<a name="q1"></a>
## Q1. (Easy) What is LangGraph and why was it created?
**Answer:** A low-level orchestration framework for long-running, stateful agents and workflows. You model the app as a graph: state (shared data), nodes (functions returning updates) and edges (what runs next). It adds loops, branching, persistence, interrupts, streaming and durable execution. Execution runs in Pregel-style super-steps.

**Simple version:** A flowchart that can loop, remember where it is, pause for a person, and pick up after a crash.

**Tie to your project (P1):** "Promotion evaluation has fixed stages, branching on outcome and an approval pause: nodes, conditional edges and an interrupt."

*Source ID: 8.1*

---

<a name="q2"></a>
## Q2. (Easy) How do you define state? What are reducers?
**Answer:** Usually a `TypedDict` (or Pydantic / dataclass). Nodes return partial updates; by default an update overwrites the key. A reducer declared with `Annotated` merges instead: `operator.add` appends, `add_messages` appends, replaces by id and handles `RemoveMessage`. `MessagesState` is a prebuilt with `messages`.

```python
class PromotionState(TypedDict):
    messages: Annotated[list, add_messages]
    employee_id: str
    evidence: Annotated[list[dict], operator.add]
    evaluation: dict | None
    decision: str | None
```

**How to say it:** "Reducers matter most with parallel nodes; without one, two branches writing the same key in one step raise an error."

*Source ID: 8.2*

---

<a name="q3"></a>
## Q3. (Easy) Explain nodes, normal edges and conditional edges.
**Answer:** A node is `(state) -> dict`. `add_edge("a", "b")` always goes a to b. `add_conditional_edges("a", router)` calls the router and goes to the node it returns. `START` and `END` mark entry and exit. `compile(checkpointer=...)` returns a Runnable.

**Simple version:** Boxes, arrows, and diamond-shaped decision boxes.

*Source ID: 8.3*

---

<a name="q4"></a>
## Q4. (Easy) Sketch a real graph you built.
**Answer:**

```python
def route(state):
    d = state["evaluation"]["decision"]
    return {"recommend": "manager_review", "not_ready": "draft_feedback"}.get(d, "hr_review")

g = StateGraph(PromotionState)
for name, fn in [("collect_evidence", collect_evidence), ("evaluate", evaluate),
                 ("manager_review", manager_review), ("draft_feedback", draft_feedback),
                 ("hr_review", hr_review)]:
    g.add_node(name, fn)
g.add_edge(START, "collect_evidence")
g.add_edge("collect_evidence", "evaluate")
g.add_conditional_edges("evaluate", route)
for n in ["manager_review", "draft_feedback", "hr_review"]:
    g.add_edge(n, END)
app = g.compile(checkpointer=checkpointer)
```

**Tie to your project (P1):** \[Replace node names with your real ones and practise drawing it in under a minute.\]

*Source ID: 8.4*

---

<a name="q5"></a>
## Q5. (Easy) What is `Command` and when do you use it?
**Answer:** A node returns `Command(update={...}, goto="next")` to update state and choose the next node in one step. Used for routing decided inside node logic, multi-agent handoffs (`graph=Command.PARENT` to jump in the parent graph), and resuming interrupts (`Command(resume=...)`). Annotate the return type (`Command[Literal["a", "b"]]`) so the graph can be drawn.

**How to say it:** "I prefer conditional edges for simple routing so the graph stays readable; `Command` when routing and updates belong together."

*Source ID: 8.5*

---

<a name="q6"></a>
## Q6. (Medium) How do you run nodes in parallel? What is `Send`?
**Answer:** Static fan-out: edges from one node to several, which run in the same super-step and join after. Dynamic map-reduce: a conditional edge returns `[Send("node", payload) for item in items]`; results merge through a reducer.

**Tie to your project (P1):** "Evaluating a batch of candidates is a `Send` map-reduce: one branch per candidate."

*Source ID: 8.6*

---

<a name="q7"></a>
## Q7. (Medium) What is a super-step and how does parallel execution handle failures?
**Answer:** A super-step is one round where all scheduled nodes run, then updates are applied together. If one parallel node fails, the super-step fails; with a checkpointer, successful nodes' writes are saved as pending writes, so a retry only re-runs the failed node.

*Source ID: 8.7*

---

<a name="q8"></a>
## Q8. (Medium) What are subgraphs and how do they share state?
**Answer:** A compiled graph used as a node. If parent and child share keys, add the child directly as a node; otherwise call it inside a node function and map state in and out. Subgraphs can have their own checkpointer namespace and can be streamed with `subgraphs=True`.

**Simple version:** A function call, but for graphs.

*Source ID: 8.8*

---

<a name="q9"></a>
## Q9. (Medium) What are input, output and private state schemas?
**Answer:** `StateGraph(State, input_schema=In, output_schema=Out)` restricts what callers send and receive; nodes can also read or write private channels not exposed outside. This keeps the public API small and hides internal fields.

**Tie to your project (P4):** "Like a DRF serializer that exposes only some model fields."

*Source ID: 8.9*

---

<a name="q10"></a>
## Q10. (Medium) What is the Functional API?
**Answer:** `@entrypoint` and `@task` decorators give checkpointing, interrupts and streaming with normal Python control flow. Good for adding persistence to existing code; the Graph API is better when you want structure visible.

*Source ID: 8.10*

---

<a name="q11"></a>
## Q11. (Medium) What is the recursion limit?
**Answer:** A cap on super-steps per run to stop infinite loops, set in config: `{"recursion_limit": 50}`. Exceeding it raises `GraphRecursionError`. Check your version's default.

*Source ID: 8.11*

---

<a name="q12"></a>
## Q12. (Medium) How do you add retries and caching to nodes?
**Answer:** `add_node("call_api", fn, retry_policy=RetryPolicy(max_attempts=3))` retries a node on failure; node caching (`cache_policy`) skips re-running expensive nodes with the same input.

*Source ID: 8.12*

---

<a name="q13"></a>
## Q13. (Medium) How do you pass runtime context (user id, DB connection) to nodes?
**Answer:** Define a context schema (`StateGraph(State, context_schema=Ctx)`) and pass `context=...` at invoke; nodes read it via the runtime. Keep non-serialisable things (connections, clients) out of state, because state is checkpointed.

**How to say it:** "State is data that should be saved; context is environment that shouldn't."

*Source ID: 8.13*

---

<a name="q14"></a>
## Q14. (Medium) How do you visualise and debug a graph?
**Answer:** `app.get_graph().draw_mermaid()` or `draw_mermaid_png()` for a diagram; LangGraph Studio for interactive runs, state inspection and editing; LangSmith traces; `stream_mode="debug"` locally.

*Source ID: 8.14*

---

<a name="q15"></a>
## Q15. (Hard) How does LangGraph compare with CrewAI, AutoGen or plain Python?
**Answer:** LangGraph is low-level and explicit: you control state and flow, with strong persistence and HITL. CrewAI and AutoGen are higher-level role- or conversation-based multi-agent frameworks, faster to start but less control. Plain Python is fine until you need persistence, resume and streaming, which you'd end up rebuilding.

**How to say it:** "I chose LangGraph because the promotion process needed durable state and human approval, which are first-class there."

*Source ID: 8.15*

---

<a name="q16"></a>
## Q16. (Hard) What is `MessagesState` versus a custom state?
**Answer:** `MessagesState` gives only `messages` with `add_messages`. Extend it (`class S(MessagesState): case_id: str`) or write your own when you need structured fields. Structured fields are better than hiding data inside messages, because routing code can read them directly.

*Source ID: 8.16*

---

<a name="q17"></a>
## Q17. (Hard) How do you design state well?
**Answer:** Keep it minimal and serialisable, use typed fields for decisions and ids, use reducers for lists built by several nodes, store large blobs outside (return references), and version the schema because old checkpoints must still load.

**How to say it:** Mention schema versioning; it is a real production pain point.

*Source ID: 8.17*

---

<a name="q18"></a>
## Q18. (Hard) Graph API versus `create_agent`: which first?
**Answer:** `create_agent` for a standard tool-calling assistant; it already runs on LangGraph and accepts middleware and a checkpointer. Write a custom graph when steps, routing, approvals or parallelism are fixed by the business process.

**Tie to your project (P1 vs P3):** "Promotions got a custom graph; an MCP-backed Q&A assistant is a `create_agent` job."

*Source ID: 8.18*
