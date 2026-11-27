# LCEL & Runnables
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Fifteen questions on the Runnable interface and LCEL composition. Interviewers often ask you to write a chain on the whiteboard, so practise 2.4 and 2.5 by hand.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [What is a Runnable?](#q1)
2. (Easy) [What is LCEL and how does the pipe operator work?](#q2)
3. (Easy) [Explain RunnableParallel, RunnablePassthrough, RunnableLambda and RunnableBranch.](#q3)
4. (Easy) [Walk me through a RAG chain using RunnableLambda, RunnableParallel and RunnablePassthrough.](#q4)
5. (Medium) [What does `RunnablePassthrough.assign` do? Give an example.](#q5)
6. (Medium) [How do you add retries, fallbacks and timeouts?](#q6)
7. (Medium) [What does `batch` do and when is it better than a loop?](#q7)
8. (Medium) [What is the difference between `stream`, `astream` and `astream_events`?](#q8)
9. (Medium) [Which steps stream and which block?](#q9)
10. (Medium) [How do you make parts of a chain configurable at runtime?](#q10)
11. (Medium) [How do you route between chains in LCEL?](#q11)
12. (Medium) [How do you debug an LCEL chain?](#q12)
13. (Hard) [LCEL versus LangGraph: when do you use which?](#q13)
14. (Hard) [How do you write a custom Runnable?](#q14)
15. (Hard) [How do you bind arguments to a Runnable?](#q15)

---

<a name="q1"></a>
## Q1. (Easy) What is a Runnable?
**Answer:** The common interface every LangChain component implements (prompts, models, parsers, retrievers, tools, chains). Every Runnable has `invoke`, `batch`, `stream` and async versions `ainvoke`, `abatch`, `astream`, plus `astream_events`. Because the interface is shared, any component composes with any other, and you get streaming, batching and tracing without extra code.

**Simple version:** A Python function with a standard contract, so anything plugs into anything.

**Tie to your project (P4):** "Same idea as DRF serializers: one contract, so everything validates the same way."

*Source ID: 2.1*

---

<a name="q2"></a>
## Q2. (Easy) What is LCEL and how does the pipe operator work?
**Answer:** LangChain Expression Language composes Runnables with `|`. `prompt | model | parser` builds a `RunnableSequence`: each step's output is the next step's input. It is good for short linear chains; for loops, state and human pauses, move to LangGraph.

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chat_models import init_chat_model

model = init_chat_model("anthropic:claude-sonnet-4-5")  # example id
prompt = ChatPromptTemplate.from_messages([
    ("system", "You summarise engineering reports."),
    ("human", "{report}"),
])
chain = prompt | model | StrOutputParser()
```

**Simple version:** A Unix pipe for LLM steps.

**Tie to your project (P1):** "Small steps inside the promotion graph, like format evidence, call model, parse score, are LCEL chains inside a LangGraph node."

*Source ID: 2.2*

---

<a name="q3"></a>
## Q3. (Easy) Explain RunnableParallel, RunnablePassthrough, RunnableLambda and RunnableBranch.
**Answer:**

- **RunnableParallel** (or a plain dict) runs several Runnables on the same input at once and returns a dict.
- **RunnablePassthrough** passes input through unchanged; `.assign()` adds keys while keeping existing ones.
- **RunnableLambda** wraps a Python function so it becomes a chain step.
- **RunnableBranch** picks a chain by condition (simple if/else routing).

**One-line difference:** Lambda changes the data, Parallel splits it into named branches, Passthrough carries it forward untouched, Branch chooses a path.

*Source ID: 2.3*

---

<a name="q4"></a>
## Q4. (Easy) Walk me through a RAG chain using RunnableLambda, RunnableParallel and RunnablePassthrough.
**Answer:**

```python
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough

def clean_question(q: str) -> str:
    return " ".join(q.strip().split())

def format_docs(docs) -> str:
    return "\n\n".join(d.page_content for d in docs)

prompt = ChatPromptTemplate.from_template(
    "Answer only from the context.\n\nContext:\n{context}\n\nQuestion: {question}"
)

chain = (
    RunnableLambda(clean_question)                    # 1. change the data
    | RunnableParallel(                               # 2. split into named branches
        context=retriever | RunnableLambda(format_docs),
        question=RunnablePassthrough(),               # 3. carry the question through
    )
    | prompt
    | llm
    | StrOutputParser()
)
chain.invoke("  What was 3M's FY2022 capex?  ")
```

**How to say it:** "The cleaned question goes into a parallel step: one branch retrieves and formats context, the other passes the question through. Both land in the prompt as `context` and `question`. Because it's one LCEL chain, I get streaming, batching and tracing for free."

**Tie to your project (P2):** "This is the shape of FinSight's query path: fetch context while the question passes through, with cleaning and formatting as RunnableLambdas." \[If FinSight is plain Python, say "this is how I'd express FinSight's query path in LCEL."\]

*Source ID: 2.4*

---

<a name="q5"></a>
## Q5. (Medium) What does `RunnablePassthrough.assign` do? Give an example.
**Answer:** It takes a dict input, keeps all existing keys and adds computed ones. Common use: return sources alongside the answer.

```python
rag_with_sources = (
    RunnableParallel(context=retriever, question=RunnablePassthrough())
    .assign(answer=(lambda x: {"context": format_docs(x["context"]), "question": x["question"]})
            | prompt | llm | StrOutputParser())
)
# returns {"context": [docs], "question": "...", "answer": "..."}
```

**Simple version:** Add a new column to the row without losing the old columns.

**Tie to your project (P2):** "FinSight returns citations, so I need the retrieved documents and the answer together. `.assign` is how you'd do that in LCEL."

*Source ID: 2.5*

---

<a name="q6"></a>
## Q6. (Medium) How do you add retries, fallbacks and timeouts?
**Answer:** `.with_retry(stop_after_attempt=3)` for transient errors; `.with_fallbacks([backup])` to switch models on failure; `timeout` and `max_retries` on the chat model; `.with_config(run_name=..., tags=[...])` to label runs. In agents, model-fallback and call-limit middleware do the same.

**Tie to your project (P2):** "FinSight supports Ollama and Claude, so a fallback between them is one line."

*Source ID: 2.6*

---

<a name="q7"></a>
## Q7. (Medium) What does `batch` do and when is it better than a loop?
**Answer:** Runs many inputs concurrently (thread pool, or asyncio with `abatch`). `config={"max_concurrency": 5}` protects you from rate limits. Use `batch_as_completed` to process results as they finish.

**Tie to your project (P4):** "For bulk extraction across enterprise records I'd batch with a concurrency cap, like we spread load with RabbitMQ workers in PNI Hub."

*Source ID: 2.7*

---

<a name="q8"></a>
## Q8. (Medium) What is the difference between `stream`, `astream` and `astream_events`?
**Answer:** `stream` yields output chunks of the final step (sync). `astream` is the async version. `astream_events(version="v2")` yields events from every inner step (model tokens, retriever results, tool start/end), which is useful when you want tokens from a model in the middle of a chain.

**Simple version:** Stream the final answer, or stream everything happening inside.

*Source ID: 2.8*

---

<a name="q9"></a>
## Q9. (Medium) Which steps stream and which block?
**Answer:** Streaming flows through steps that can process input chunk by chunk (models, string parsers, `JsonOutputParser` with partial JSON). A plain `RunnableLambda` waits for full input and breaks the stream after it. Use a generator function (one that yields) to keep streaming through custom steps.

**How to say it:** This is a good "I've debugged this" detail: "A lambda after the model killed token streaming, so I rewrote it as a generator."

*Source ID: 2.9*

---

<a name="q10"></a>
## Q10. (Medium) How do you make parts of a chain configurable at runtime?
**Answer:** `configurable_fields` (change a parameter like temperature per call) and `configurable_alternatives` (swap a whole component, for example the model). Then call with `config={"configurable": {"llm": "ollama"}}`. With `init_chat_model` you can also make the model itself configurable.

**Tie to your project (P2):** "FinSight does this with YAML config; in LCEL it's configurable alternatives."

*Source ID: 2.10*

---

<a name="q11"></a>
## Q11. (Medium) How do you route between chains in LCEL?
**Answer:** Classify first (a small model with structured output returning a label), then use `RunnableBranch` or a `RunnableLambda` that returns the chosen chain. For more than two or three routes, or routes that loop back, use LangGraph conditional edges, which are easier to read and trace.

*Source ID: 2.11*

---

<a name="q12"></a>
## Q12. (Medium) How do you debug an LCEL chain?
**Answer:** LangSmith traces show every step's input and output. Locally, `chain.get_graph().print_ascii()` shows the structure, `set_debug(True)` prints everything, and you can `invoke` each sub-step alone. Name steps with `.with_config(run_name=...)` so traces are readable.

*Source ID: 2.12*

---

<a name="q13"></a>
## Q13. (Hard) LCEL versus LangGraph: when do you use which?
**Answer:** LCEL for linear, stateless pipelines (prompt, model, parse; simple RAG). LangGraph when you need state across steps, loops, conditional routing, human approval, persistence or multi-agent coordination. They combine: LCEL chains often live inside LangGraph nodes.

**Tie to your project (P1):** "The promotion workflow is LangGraph; small transformations inside nodes are LCEL."

*Source ID: 2.13*

---

<a name="q14"></a>
## Q14. (Hard) How do you write a custom Runnable?
**Answer:** Usually wrap a function with `RunnableLambda` or the `@chain` decorator. For more control, subclass `Runnable` and implement `invoke` (and optionally `stream`, `ainvoke`). Prefer lambdas and generators; subclassing is rarely needed.

*Source ID: 2.14*

---

<a name="q15"></a>
## Q15. (Hard) How do you bind arguments to a Runnable?
**Answer:** `.bind(...)` fixes keyword arguments for every call, for example `model.bind(stop=["\n\n"])`. `bind_tools` is a specialised version that attaches tool schemas to a chat model.

**Simple version:** Pre-fill some arguments so callers don't have to.

*Source ID: 2.15*
