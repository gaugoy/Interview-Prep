# LangSmith & Evaluation
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Fifteen questions on observability and evaluation. Senior interviews care a lot about "how do you know it works?", and FinSight's benchmark discipline is your best answer.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [What is LangSmith and what do you use it for?](#q1)
2. (Easy) [How do you evaluate an LLM app or agent?](#q2)
3. (Easy) [How do you build a good evaluation dataset?](#q3)
4. (Easy) [What is LLM-as-judge and what are its pitfalls?](#q4)
5. (Medium) [Offline versus online evaluation?](#q5)
6. (Medium) [What metrics do you track in production?](#q6)
7. (Medium) [How do you debug an agent that gives a wrong answer?](#q7)
8. (Medium) [How do you evaluate an agent's trajectory?](#q8)
9. (Medium) [How do you collect user feedback?](#q9)
10. (Medium) [How do you run evaluations in CI?](#q10)
11. (Medium) [How do you manage prompts across environments?](#q11)
12. (Medium) [How do you handle sensitive data in traces?](#q12)
13. (Hard) [What is an annotation queue?](#q13)
14. (Hard) [How do you compare two models or prompts?](#q14)
15. (Hard) [What are RAGAS and other evaluation tools?](#q15)

---

<a name="q1"></a>
## Q1. (Easy) What is LangSmith and what do you use it for?
**Answer:** An observability and evaluation platform for LLM apps (with or without LangChain). Enable tracing with `LANGSMITH_TRACING=true`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT`, or `@traceable` on plain functions. You get a tree of every step (prompts, outputs, tool calls, latency, tokens, cost), plus datasets, experiments, online evaluators, annotation queues, prompt hub, dashboards, alerts and deployment.

**Simple version:** A flight recorder plus a test lab.

**Tie to your project (P1):** "Traces give a record of exactly what evidence the model saw for each promotion decision." \[If you used Langfuse or logging plus Grafana, say so.\]

*Source ID: 12.1*

---

<a name="q2"></a>
## Q2. (Easy) How do you evaluate an LLM app or agent?
**Answer:**

1. Build a dataset (start with 30 to 100 real examples; grow it from production failures).
2. Choose evaluators: code checks, reference-based, LLM-as-judge with a rubric, human review.
3. For agents: final answer, trajectory and single-step evaluation.
4. Run experiments on every change, compare with a baseline, gate in CI.
5. Monitor online with sampled scoring and alerts.

**Tie to your project (P2):** "FinSight is my evaluation story: a public benchmark, ablations, config-fingerprinted runs, pytest."

*Source ID: 12.2*

---

<a name="q3"></a>
## Q3. (Easy) How do you build a good evaluation dataset?
**Answer:** Real user questions (not just ones you invent), covering common cases, edge cases and known failures; expected outputs or grading criteria per example; labels reviewed by a domain expert; versioned; split by category so you see where quality changes.

**Tie to your project (P2):** "FinanceBench gave me gold evidence pages, which made retrieval metrics exact."

*Source ID: 12.3*

---

<a name="q4"></a>
## Q4. (Easy) What is LLM-as-judge and what are its pitfalls?
**Answer:** A model grades outputs against a rubric. Pitfalls: position bias (prefers the first answer), verbosity bias (prefers longer), self-preference, and inconsistency. Mitigate: clear rubric with examples, binary or small scales, randomise order in pairwise tests, use a strong judge model, and validate against a few dozen human labels.

**How to say it:** "I don't trust a judge until I've measured its agreement with humans."

*Source ID: 12.4*

---

<a name="q5"></a>
## Q5. (Medium) Offline versus online evaluation?
**Answer:** Offline: fixed dataset before release (regression testing). Online: score real traffic after release (sampled LLM-judge, user feedback, business metrics). You need both: offline catches regressions, online catches what your dataset didn't imagine.

*Source ID: 12.5*

---

<a name="q6"></a>
## Q6. (Medium) What metrics do you track in production?
**Answer:** Latency (p50, p95, time to first token), cost per request, error and fallback rates, tool error rate, step count per run, user feedback (thumbs, edits), task success, groundedness scores on a sample, and escalation-to-human rate.

**Tie to your project (P4):** "I've run Grafana and Prometheus monitoring before; LLM metrics just add cost and quality signals to the same dashboards."

*Source ID: 12.6*

---

<a name="q7"></a>
## Q7. (Medium) How do you debug an agent that gives a wrong answer?
**Answer:** Walk the trace: input right? retrieval right? tool choice and arguments right? tool output right? did the final prompt contain it? Fix the earliest broken step and add the case to the dataset.

*Source ID: 12.7*

---

<a name="q8"></a>
## Q8. (Medium) How do you evaluate an agent's trajectory?
**Answer:** Compare the sequence of tool calls with an expected sequence (exact, subset, or unordered match), or have an LLM judge whether the path was reasonable. Also check step count and forbidden tools.

*Source ID: 12.8*

---

<a name="q9"></a>
## Q9. (Medium) How do you collect user feedback?
**Answer:** Thumbs up/down or ratings in the UI, linked to the run id; `client.create_feedback(run_id, key="user_score", score=1)` in LangSmith. Route negative feedback to an annotation queue; reviewed cases go into the dataset.

**Tie to your project (P1):** "The approver's final decision is natural feedback: agreement between AI recommendation and human decision." \[Fill: whether you measured it.\]

*Source ID: 12.9*

---

<a name="q10"></a>
## Q10. (Medium) How do you run evaluations in CI?
**Answer:** A small, fast dataset runs on every PR with deterministic checks and a few LLM-judged metrics; thresholds fail the build on regression. A larger suite runs nightly or before release. Use pytest integration or `evaluate()` from the LangSmith SDK.

*Source ID: 12.10*

---

<a name="q11"></a>
## Q11. (Medium) How do you manage prompts across environments?
**Answer:** Version in Git or the prompt hub with tags, test every change against the eval set, log the prompt version on each trace.

*Source ID: 12.11*

---

<a name="q12"></a>
## Q12. (Medium) How do you handle sensitive data in traces?
**Answer:** Mask inputs and outputs (LangSmith supports hiding or custom anonymisers), self-host or use a regional deployment if required, restrict access, and set retention periods.

**Tie to your project:** "Qualcomm promotion data is sensitive, so tracing would need masking and restricted access."

*Source ID: 12.12*

---

<a name="q13"></a>
## Q13. (Hard) What is an annotation queue?
**Answer:** A list of runs for humans to review and label (correct, incorrect, edited answer). It's how you turn production traffic into high-quality dataset examples.

*Source ID: 12.13*

---

<a name="q14"></a>
## Q14. (Hard) How do you compare two models or prompts?
**Answer:** Run both as experiments on the same dataset, compare metrics side by side, use pairwise LLM-judge on the same inputs, and check cost and latency. Look at individual regressions, not only averages.

**Tie to your project (P2):** "That's exactly how I compared bge-small versus Gemini embeddings."

*Source ID: 12.14*

---

<a name="q15"></a>
## Q15. (Hard) What are RAGAS and other evaluation tools?
**Answer:** RAGAS provides RAG metrics (faithfulness, answer relevance, context precision and recall). Others: DeepEval, TruLens, Langfuse, Arize Phoenix, OpenAI Evals. Concepts transfer; pick what fits your stack.

*Source ID: 12.15*
