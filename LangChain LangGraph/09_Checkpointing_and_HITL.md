# Checkpointing & Human-in-the-Loop
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Fifteen questions on persistence, interrupts and human approval. This maps directly onto your promotion workflow's approval routing, so it's where you can sound most experienced.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [What is a checkpointer and what does it give you?](#q1)
2. (Easy) [How do you set up the Postgres checkpointer?](#q2)
3. (Easy) [How do you implement human-in-the-loop?](#q3)
4. (Easy) [What is the biggest gotcha with `interrupt()`?](#q4)
5. (Medium) [What human-in-the-loop patterns exist?](#q5)
6. (Medium) [How do you show pending approvals in a UI?](#q6)
7. (Medium) [What are static breakpoints?](#q7)
8. (Medium) [What is time travel?](#q8)
9. (Medium) [How do you edit state from outside the graph?](#q9)
10. (Medium) [Checkpointer versus Store?](#q10)
11. (Medium) [What is durable execution?](#q11)
12. (Medium) [How long can a thread wait, and what about schema changes?](#q12)
13. (Hard) [How do you add reminders or timeouts for approvals?](#q13)
14. (Hard) [How do you clean up old checkpoints?](#q14)
15. (Hard) [How do you test interrupts?](#q15)

---

<a name="q1"></a>
## Q1. (Easy) What is a checkpointer and what does it give you?
**Answer:** It saves a snapshot of graph state after every super-step, keyed by `thread_id` (`config={"configurable": {"thread_id": ...}}`). Implementations: `InMemorySaver` (tests), `SqliteSaver`, `PostgresSaver` / `AsyncPostgresSaver` (production), Redis and others. It enables memory, human-in-the-loop, fault tolerance and time travel.

**Simple version:** Autosave in a video game after every level.

**Tie to your project (P1):** "A promotion case can wait days for approval; with a Postgres checkpointer it survives deploys, and we already run Postgres in PNI Hub." \[Confirm which checkpointer.\]

*Source ID: 9.1*

---

<a name="q2"></a>
## Q2. (Easy) How do you set up the Postgres checkpointer?
```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup()          # once, creates tables
    app = graph.compile(checkpointer=checkpointer)
```

**Answer:** Use a connection pool in production, run `setup()` at deploy (like a migration), and use `AsyncPostgresSaver` with async graphs.

*Source ID: 9.2*

---

<a name="q3"></a>
## Q3. (Easy) How do you implement human-in-the-loop?
**Answer:** Call `interrupt(payload)` in a node. The graph saves state and stops, returning the payload under `__interrupt__`. Resume with `graph.invoke(Command(resume=value), config)`; the node re-runs from the start and `interrupt()` returns the value. A checkpointer is required.

```python
def manager_review(state):
    answer = interrupt({"employee_id": state["employee_id"],
                        "evaluation": state["evaluation"],
                        "question": "Approve, reject or edit?"})
    return {"decision": answer["action"]}

# Django view handling the manager's click:
app.invoke(Command(resume={"action": "approve"}), {"configurable": {"thread_id": case_id}})
```

**Tie to your project (P1):** "The graph interrupts at manager review, PNI Hub shows the evaluation, and the click resumes the thread. The AI recommends; people approve." \[Guess about your UI flow.\]

*Source ID: 9.3*

---

<a name="q4"></a>
## Q4. (Easy) What is the biggest gotcha with `interrupt()`?
**Answer:** On resume the whole node re-runs from its start, so any side effect before `interrupt()` (sending an email, writing to the DB) runs twice. Put interrupts at the top of a node, or in their own node, and make earlier steps idempotent. Also: multiple interrupts in one node are matched by order, so don't put them inside changing loops.

**How to say it:** This single detail signals real experience. Say it unprompted.

*Source ID: 9.4*

---

<a name="q5"></a>
## Q5. (Medium) What human-in-the-loop patterns exist?
**Answer:** Approve or reject (before a sensitive action), edit state (fix a draft or arguments), review output, ask for missing input, and multi-level approvals (a chain of interrupts or a loop over approvers).

**Tie to your project (P1):** "Promotions can need manager then committee approval: one interrupt per level, with the decision stored in state each time."

*Source ID: 9.5*

---

<a name="q6"></a>
## Q6. (Medium) How do you show pending approvals in a UI?
**Answer:** Store case status in your own Django model when the graph interrupts (or query `get_state(config).tasks` / `interrupts`), list pending cases per approver, and resume via an API endpoint that checks the approver's permission first.

**How to say it:** "The checkpointer holds graph state; my Django models hold business status and who must act."

*Source ID: 9.6*

---

<a name="q7"></a>
## Q7. (Medium) What are static breakpoints?
**Answer:** `compile(interrupt_before=["node"], interrupt_after=[...])` pauses at fixed nodes. Mainly for debugging and stepping through; dynamic `interrupt()` is preferred for real approvals because it can carry a payload and be conditional.

*Source ID: 9.7*

---

<a name="q8"></a>
## Q8. (Medium) What is time travel?
**Answer:** `get_state_history(config)` lists every checkpoint. Resume from an old `checkpoint_id`, or `update_state()` to change state and fork. Uses: debugging, replay after a bug fix, auditing.

**Tie to your project (P1):** "Auditability: we can show exactly what evidence and evaluation led to each recommendation."

*Source ID: 9.8*

---

<a name="q9"></a>
## Q9. (Medium) How do you edit state from outside the graph?
**Answer:** `app.update_state(config, {"evaluation": corrected}, as_node="evaluate")` writes an update as if a node produced it, then continue with `invoke(None, config)`. Useful for admin corrections.

*Source ID: 9.9*

---

<a name="q10"></a>
## Q10. (Medium) Checkpointer versus Store?
**Answer:** Checkpointer = one thread's state over time. Store = cross-thread key-value documents with namespaces and optional vector search.

*Source ID: 9.10*

---

<a name="q11"></a>
## Q11. (Medium) What is durable execution?
**Answer:** After a crash you resume the thread from the last checkpoint. Durability mode (`"exit"`, `"async"`, `"sync"`) trades speed for how often checkpoints are written. Wrap side effects in tasks or make them idempotent so replays don't repeat them.

**Tie to your project (P4):** "Same discipline as PNI Hub's scheduled jobs and RabbitMQ consumers: idempotent steps, so retries are safe."

*Source ID: 9.11*

---

<a name="q12"></a>
## Q12. (Medium) How long can a thread wait, and what about schema changes?
**Answer:** Indefinitely; it's just rows in the database. The risk is code changes: if you rename nodes or change state fields, old checkpoints may not resume. Add fields with defaults, keep old node names during migration, or finish in-flight cases on the old version.

**How to say it:** This is a senior-level concern; raising it shows you've run long-lived workflows.

*Source ID: 9.12*

---

<a name="q13"></a>
## Q13. (Hard) How do you add reminders or timeouts for approvals?
**Answer:** LangGraph doesn't wake itself. Use a scheduled job (cron, Celery beat) that finds cases waiting too long and notifies or escalates, possibly resuming with `Command(resume={"action": "escalate"})`.

**Tie to your project (P4):** "PNI Hub already runs scheduled jobs; approval reminders fit there."

*Source ID: 9.13*

---

<a name="q14"></a>
## Q14. (Hard) How do you clean up old checkpoints?
**Answer:** Delete threads once cases close (`checkpointer.delete_thread(thread_id)`), or run a retention job; copy anything needed for audit into your own tables first.

*Source ID: 9.14*

---

<a name="q15"></a>
## Q15. (Hard) How do you test interrupts?
**Answer:** Use `InMemorySaver`, invoke until `__interrupt__` appears, assert on its payload, then invoke `Command(resume=...)` and assert the final state. Test approve, reject and edit paths separately.

*Source ID: 9.15*
