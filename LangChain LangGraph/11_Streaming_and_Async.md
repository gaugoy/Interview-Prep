# Streaming & Async
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Fifteen questions on streaming and async. Your WebSocket work at Dashakrit and your Django/Nginx stack at Qualcomm give you strong practical answers here.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [Why stream LLM output?](#q1)
2. (Easy) [What streaming modes does LangGraph support?](#q2)
3. (Easy) [How do you emit custom progress events?](#q3)
4. (Easy) [How do you stream only tokens from one node?](#q4)
5. (Medium) [How do you stream from LangGraph to a browser through Django?](#q5)
6. (Medium) [SSE versus WebSockets?](#q6)
7. (Medium) [How do you handle the user cancelling mid-stream?](#q7)
8. (Medium) [What is double-texting and how do you handle it?](#q8)
9. (Medium) [Sync versus async: when does it matter?](#q9)
10. (Medium) [How do you run many LLM calls concurrently with a limit?](#q10)
11. (Medium) [How do you stream structured output?](#q11)
12. (Medium) [How do you stream tool calls?](#q12)
13. (Hard) [Does Gunicorn work for streaming?](#q13)
14. (Hard) [How do you stream from subgraphs?](#q14)
15. (Hard) [How do you test streaming?](#q15)

---

<a name="q1"></a>
## Q1. (Easy) Why stream LLM output?
**Answer:** LLM responses take seconds; streaming shows the first tokens in under a second, which feels much faster, and lets users stop early. For agents, streaming progress ("searching Jira...") builds trust.

*Source ID: 11.1*

---

<a name="q2"></a>
## Q2. (Easy) What streaming modes does LangGraph support?
**Answer:** `stream_mode=`: `"values"` (full state after each step), `"updates"` (what each node changed), `"messages"` (LLM tokens plus metadata about the node), `"custom"` (your events via `get_stream_writer()`), `"debug"` (everything). Pass a list to get several.

**How to say it:** "For chat I stream `messages` for tokens and `updates` or `custom` for step progress."

*Source ID: 11.2*

---

<a name="q3"></a>
## Q3. (Easy) How do you emit custom progress events?
**Answer:**

```python
from langgraph.config import get_stream_writer

def collect_evidence(state):
    writer = get_stream_writer()
    writer({"stage": "jira", "msg": "Fetching Jira tickets"})
    ...
    return {"evidence": items}
```

**Tie to your project (P1):** "Approvers could watch evidence collection progress for a case live."

*Source ID: 11.3*

---

<a name="q4"></a>
## Q4. (Easy) How do you stream only tokens from one node?
**Answer:** With `stream_mode="messages"`, each chunk comes with metadata including `langgraph_node`; filter on it (for example only the `answer` node), or tag the model with `.with_config(tags=["final"])` and filter on tags.

*Source ID: 11.4*

---

<a name="q5"></a>
## Q5. (Medium) How do you stream from LangGraph to a browser through Django?
**Answer:** Server-Sent Events from an async view returning `StreamingHttpResponse` with an async generator, on an ASGI server (Uvicorn, Daphne), with Nginx buffering off for that route (`X-Accel-Buffering: no`). WebSockets via Django Channels when you need two-way messages. For long jobs, run the graph in a worker and publish progress over Redis pub/sub.

```python
async def chat_stream(request):
    config = {"configurable": {"thread_id": request.GET["thread"]}}
    async def gen():
        async for chunk, meta in app.astream({"messages": [...]}, config, stream_mode="messages"):
            yield f"data: {json.dumps({'token': chunk.content})}\n\n"
    return StreamingHttpResponse(gen(), content_type="text/event-stream")
```

**Tie to your project:** "I built REST plus WebSocket real-time messaging between an ML backend and a web server in 3RD-AI; PNI Hub runs Gunicorn behind Nginx, so I'd add an ASGI path and disable buffering."

*Source ID: 11.5*

---

<a name="q6"></a>
## Q6. (Medium) SSE versus WebSockets?
**Answer:** SSE: one-way server to client, plain HTTP, auto-reconnect, simple through proxies; ideal for token streaming. WebSockets: two-way, good for cancel, approve mid-run or collaborative UIs, but more infrastructure (Channels, Redis layer).

**Simple version:** SSE is a radio broadcast; WebSocket is a phone call.

*Source ID: 11.6*

---

<a name="q7"></a>
## Q7. (Medium) How do you handle the user cancelling mid-stream?
**Answer:** Detect client disconnect (the async generator gets cancelled), stop the graph run (cancel the task), and since state is checkpointed per step, the thread is consistent at the last completed step. Don't run side effects after the user cancels.

*Source ID: 11.7*

---

<a name="q8"></a>
## Q8. (Medium) What is double-texting and how do you handle it?
**Answer:** The user sends a new message while the previous run is still going. Options: reject the new one, queue it, interrupt the current run and start the new one, or rollback and restart. Pick per product; implement with a per-thread lock or run status in Redis or the DB.

*Source ID: 11.8*

---

<a name="q9"></a>
## Q9. (Medium) Sync versus async: when does it matter?
**Answer:** LLM calls are slow and I/O-bound; async (`ainvoke`, `astream`, async nodes, `AsyncPostgresSaver`) lets one process serve many concurrent conversations. Blocking calls inside async nodes freeze the event loop; use async clients or `asyncio.to_thread`. In Django, use async views and `sync_to_async` for the ORM.

**Simple version:** One waiter serving many tables instead of standing at one table while the kitchen cooks.

**Tie to your project (P4):** "PNI Hub's ORM code is sync, so in async nodes I'd wrap it with `sync_to_async`, or keep nodes sync and run the graph in a worker."

*Source ID: 11.9*

---

<a name="q10"></a>
## Q10. (Medium) How do you run many LLM calls concurrently with a limit?
**Answer:** `abatch` with `max_concurrency`, or `asyncio.gather` with an `asyncio.Semaphore`. Combine with a rate limiter on the model.

*Source ID: 11.10*

---

<a name="q11"></a>
## Q11. (Medium) How do you stream structured output?
**Answer:** Some providers stream partial JSON for structured output; with TypedDict or JSON schema you get progressively filled dicts. Useful to show fields as they arrive; validate only the final object.

*Source ID: 11.11*

---

<a name="q12"></a>
## Q12. (Medium) How do you stream tool calls?
**Answer:** Tool-call chunks arrive as `tool_call_chunks` in `AIMessageChunk`s; LangChain merges them. In the UI, show "calling get\_open\_bugs..." when a tool call starts and the result when the `ToolMessage` arrives (visible in `updates` mode).

*Source ID: 11.12*

---

<a name="q13"></a>
## Q13. (Hard) Does Gunicorn work for streaming?
**Answer:** Sync Gunicorn workers hold a worker per open stream, which doesn't scale. Use Uvicorn workers (`gunicorn -k uvicorn.workers.UvicornWorker`) with an ASGI Django app, or a separate FastAPI service for streaming endpoints.

**Tie to your project (P4):** A concrete production detail from your own stack.

*Source ID: 11.13*

---

<a name="q14"></a>
## Q14. (Hard) How do you stream from subgraphs?
**Answer:** `app.stream(..., subgraphs=True)` yields `(namespace, chunk)` tuples so you know which subgraph or agent produced each event.

*Source ID: 11.14*

---

<a name="q15"></a>
## Q15. (Hard) How do you test streaming?
**Answer:** Collect chunks in a test with a fake streaming model, assert order and content, check the final assembled message, and test that disconnects don't leave runs half-applied.

*Source ID: 11.15*
