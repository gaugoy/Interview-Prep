# Models & Structured Output
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Fifteen questions on choosing chat models and getting reliable structured output. Structured output is one of the most asked practical topics, so know 4.4 to 4.8 well.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [How do you create and swap models? What is `init_chat_model`?](#q1)
2. (Easy) [How do you choose a model for a task?](#q2)
3. (Easy) [What do temperature, top\_p and max\_tokens control?](#q3)
4. (Easy) [How do you get reliable structured output?](#q4)
5. (Medium) [Pydantic versus TypedDict versus JSON schema: which do you use?](#q5)
6. (Medium) [What happens when structured output fails validation?](#q6)
7. (Medium) [How do field descriptions and enums help?](#q7)
8. (Medium) [How do you extract structured data from long documents?](#q8)
9. (Medium) [What is `bind_tools` and how is it related to structured output?](#q9)
10. (Medium) [How do you handle rate limits and provider outages?](#q10)
11. (Medium) [How do you track token usage and cost?](#q11)
12. (Medium) [When would you use a local model like Ollama?](#q12)
13. (Hard) [What are embeddings models and how do you choose one?](#q13)
14. (Hard) [What are multimodal inputs and how does LangChain represent them?](#q14)
15. (Hard) [What are reasoning models and how do they change your design?](#q15)

---

<a name="q1"></a>
## Q1. (Easy) How do you create and swap models? What is `init_chat_model`?
**Answer:** `init_chat_model("provider:model", temperature=0)` creates any supported chat model from a string, so the model can come from config. You can also import provider classes directly (`ChatAnthropic`, `ChatOpenAI`, `ChatOllama`).

**Tie to your project (P2):** "FinSight is YAML-configured: I switch embedding models and LLM providers without code changes, and every run is fingerprinted by its config."

*Source ID: 4.1*

---

<a name="q2"></a>
## Q2. (Easy) How do you choose a model for a task?
**Answer:** Weigh quality, cost, latency, context window, tool-calling reliability and data privacy. Use a strong model for planning and reasoning, a small fast one for classification and extraction, and a local model (Ollama) for private or offline work. Decide with an eval set, not benchmarks alone.

**Simple version:** The cheapest model that passes your tests.

*Source ID: 4.2*

---

<a name="q3"></a>
## Q3. (Easy) What do temperature, top\_p and max\_tokens control?
**Answer:** Temperature controls randomness (0 for extraction, evaluation and tool calling; higher for creative text). top\_p limits sampling to the most likely tokens. max\_tokens caps output length and cost. Some reasoning models fix or ignore temperature.

*Source ID: 4.3*

---

<a name="q4"></a>
## Q4. (Easy) How do you get reliable structured output?
**Answer:** `model.with_structured_output(Schema)` with a Pydantic model, TypedDict or JSON schema. It uses the provider's native structured output or tool calling, which is far more reliable than asking for JSON in text. In `create_agent`, pass `response_format=Schema` and read `result["structured_response"]`.

```python
from pydantic import BaseModel, Field
from typing import Literal

class Evaluation(BaseModel):
    decision: Literal["recommend", "not_ready", "needs_review"]
    score: int = Field(ge=1, le=5)
    reasons: list[str] = Field(description="Evidence-based reasons, max 5")

evaluator = model.with_structured_output(Evaluation)
```

**How to say it:** "I never regex-parse LLM output in production. Schema-bound output, Pydantic validation, and a defined path when validation fails."

**Tie to your project (P1):** "The promotion evaluator returns a typed decision, score and reasons, so the next node routes on `decision`."

*Source ID: 4.4*

---

<a name="q5"></a>
## Q5. (Medium) Pydantic versus TypedDict versus JSON schema: which do you use?
**Answer:** Pydantic gives validation (types, ranges, custom validators) and returns an object; best for production. TypedDict is lighter, returns a dict and supports streaming partial output more easily. JSON schema is for when the schema comes from elsewhere (an API spec).

*Source ID: 4.5*

---

<a name="q6"></a>
## Q6. (Medium) What happens when structured output fails validation?
**Answer:** Options: retry with the validation error in the prompt (the model usually fixes it), fall back to a stronger model, use `include_raw=True` to inspect the raw response, or route to a human. Count failures as a metric. Keep schemas simple: fewer nested levels and clear field descriptions reduce failures.

**Tie to your project (P4):** "For the data-extraction tools, a failed validation never writes to the database; it goes to a review queue." \[Confirm.\]

*Source ID: 4.6*

---

<a name="q7"></a>
## Q7. (Medium) How do field descriptions and enums help?
**Answer:** The schema is part of the prompt. Field descriptions tell the model what each field means; `Literal` enums restrict values so routing code never sees surprises; `Optional` fields let the model leave out what isn't present instead of inventing it.

**Simple version:** A form with dropdowns gets better answers than a form with blank boxes.

*Source ID: 4.7*

---

<a name="q8"></a>
## Q8. (Medium) How do you extract structured data from long documents?
**Answer:** Chunk the document, extract per chunk with a schema that allows empty results, then merge and de-duplicate (map-reduce). For very long documents use a model with a big context but still verify. Keep a source reference (page, chunk id) for every extracted field so humans can check it.

**Tie to your project (P4 and P2):** "The internal data-automation tools extract and validate fields across enterprise records, and FinSight deals with long filings, so I've handled both sides: extraction and long-document retrieval."

*Source ID: 4.8*

---

<a name="q9"></a>
## Q9. (Medium) What is `bind_tools` and how is it related to structured output?
**Answer:** `bind_tools` attaches tool schemas so the model can return tool calls. Structured output is often implemented as a forced call to a single "tool" whose arguments are your schema. `tool_choice` can force a specific tool or any tool.

*Source ID: 4.9*

---

<a name="q10"></a>
## Q10. (Medium) How do you handle rate limits and provider outages?
**Answer:** Client-side rate limiter (`InMemoryRateLimiter` on the model), retries with exponential backoff, `max_concurrency` in batch, fallbacks to another model or provider, and queues for bulk jobs.

**Tie to your project (P4):** "Bulk work goes through RabbitMQ workers with a concurrency cap, the same way PNI Hub handles scheduled jobs."

*Source ID: 4.10*

---

<a name="q11"></a>
## Q11. (Medium) How do you track token usage and cost?
**Answer:** `AIMessage.usage_metadata` gives input and output tokens per call; LangSmith aggregates cost per trace, project and user. Log usage with request ids and set alerts or budgets per feature.

*Source ID: 4.11*

---

<a name="q12"></a>
## Q12. (Medium) When would you use a local model like Ollama?
**Answer:** Sensitive data that can't leave the network, offline development, cost-free experimentation, and predictable latency without rate limits. Trade-offs: weaker quality and tool calling than top hosted models, and you manage hardware.

**Tie to your project (P2):** "FinSight runs fully locally on Apple Silicon through Ollama, with Claude as an optional provider. That let me run many ablations at zero API cost."

*Source ID: 4.12*

---

<a name="q13"></a>
## Q13. (Hard) What are embeddings models and how do you choose one?
**Answer:** Models that turn text into vectors for similarity search. Choose by retrieval quality on your data, dimension (storage and speed), max input length, language support, cost and whether it can run locally. Never mix embeddings from different models in one index.

**Tie to your project (P2):** "I compared bge-small (local, small) with Gemini embeddings on FinanceBench as one of my ablation axes." \[Fill: which won and by how much.\]

*Source ID: 4.13*

---

<a name="q14"></a>
## Q14. (Hard) What are multimodal inputs and how does LangChain represent them?
**Answer:** Images, audio or PDFs passed to models that accept them, represented as content blocks in a `HumanMessage` (text block plus image block with URL or base64). Use cases: reading scanned documents, charts and screenshots.

**Tie to your project:** "My earlier video-analytics work (3RD-AI) was classic computer vision; today I'd consider a multimodal model for parts of that pipeline."

*Source ID: 4.14*

---

<a name="q15"></a>
## Q15. (Hard) What are reasoning models and how do they change your design?
**Answer:** Models that think internally before answering (extended thinking). They are better at planning and multi-step logic but slower and pricier. Use them for planner or evaluator nodes and cheaper models for routine steps. Reasoning content may come back as a separate content block; don't show it to end users by default.

*Source ID: 4.15*
