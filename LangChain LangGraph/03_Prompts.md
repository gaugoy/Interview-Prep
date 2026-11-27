# Prompts & Prompt Engineering
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Fifteen questions on prompt templates and prompt engineering. Interviewers use these to test whether you treat prompts as engineered, versioned artefacts rather than magic strings.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [What is the difference between PromptTemplate, ChatPromptTemplate and MessagesPlaceholder?](#q1)
2. (Easy) [What are partial variables and why use them?](#q2)
3. (Easy) [What is few-shot prompting and how do you do it in LangChain?](#q3)
4. (Easy) [What makes a good system prompt?](#q4)
5. (Medium) [What is chain-of-thought and should you use it?](#q5)
6. (Medium) [How do you handle prompt injection?](#q6)
7. (Medium) [How do you version and manage prompts?](#q7)
8. (Medium) [How do you test whether a prompt change is better?](#q8)
9. (Medium) [How do you put retrieved context into a prompt safely and efficiently?](#q9)
10. (Medium) [What is the "lost in the middle" problem?](#q10)
11. (Medium) [How do you write prompts that work across different models?](#q11)
12. (Medium) [How do you make the model say "I don't know"?](#q12)
13. (Hard) [What is prompt caching and how do you design for it?](#q13)
14. (Hard) [How do you build dynamic prompts based on user or context?](#q14)
15. (Hard) [What are the most common prompt failures you've seen?](#q15)

---

<a name="q1"></a>
## Q1. (Easy) What is the difference between PromptTemplate, ChatPromptTemplate and MessagesPlaceholder?
**Answer:** `PromptTemplate` formats one string. `ChatPromptTemplate` builds a list of role-tagged messages (system, human, ai), which chat models expect. `MessagesPlaceholder("history")` is a slot for a list of earlier messages (chat history, agent scratchpad).

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You evaluate promotion cases against these criteria:\n{criteria}"),
    MessagesPlaceholder("history"),
    ("human", "{evidence}"),
])
```

**Simple version:** A string template versus a conversation template with a hole for past messages.

**Tie to your project (P1):** "Criteria live in the system message and the candidate's evidence in the human message, so criteria can change without touching code." \[Adjust to how your prompts are stored.\]

*Source ID: 3.1*

---

<a name="q2"></a>
## Q2. (Easy) What are partial variables and why use them?
**Answer:** `prompt.partial(today=..., criteria=...)` fills some variables now and the rest at call time. Useful for values known at startup (company policy, date) or computed by a function each call.

**Simple version:** Fill in the parts of the form you already know.

*Source ID: 3.2*

---

<a name="q3"></a>
## Q3. (Easy) What is few-shot prompting and how do you do it in LangChain?
**Answer:** Include worked examples in the prompt so the model copies the pattern. `FewShotChatMessagePromptTemplate` formats examples as message pairs. With many examples, use an example selector (`SemanticSimilarityExampleSelector`) to pick the most relevant few per input, which saves tokens.

**How to say it:** "Few-shot examples fix format and edge cases better than longer instructions."

**Tie to your project (P3):** "For natural-language queries over PNI Hub, a few examples of question-to-tool-call mapping made tool selection much more reliable." \[Only if true.\]

*Source ID: 3.3*

---

<a name="q4"></a>
## Q4. (Easy) What makes a good system prompt?
**Answer:** Role and goal; the context the model needs; clear rules and constraints; output format; what to do when unsure ("say you don't know", "ask a clarifying question"); examples. Put stable instructions first (helps prompt caching), variable content last. Be specific; avoid contradictions.

**Simple version:** A good job description: who you are, what to do, what not to do, and what the result should look like.

*Source ID: 3.4*

---

<a name="q5"></a>
## Q5. (Medium) What is chain-of-thought and should you use it?
**Answer:** Asking the model to reason step by step before answering improves accuracy on multi-step problems. Modern reasoning models do this internally, so you often just enable reasoning or extended thinking instead. In production, don't show raw reasoning to users; return a structured answer plus short reasons.

**Tie to your project (P1):** "The evaluator returns a decision plus a list of reasons. That gives the benefit of reasoning and an explanation the approver can read."

*Source ID: 3.5*

---

<a name="q6"></a>
## Q6. (Medium) How do you handle prompt injection?
**Answer:** Treat retrieved documents, tool results and user text as untrusted data. Keep instructions in the system message and delimit untrusted content; give tools least privilege; validate tool arguments; require human approval for side effects; filter outputs; log for audit. No single defence is enough.

**How to say it:** "I design so a successful injection has a small blast radius."

**Tie to your project (P3):** "The MCP server exposes read-only, parameterised queries scoped to the user's permissions, never raw SQL." \[Confirm.\]

*Source ID: 3.6*

---

<a name="q7"></a>
## Q7. (Medium) How do you version and manage prompts?
**Answer:** Keep prompts in Git or the LangSmith prompt hub with tags (`prod`, `staging`); load by name and version; log the version on every trace; test every change against an eval set before promoting.

**Tie to your project (P2):** "FinSight fingerprints each run's config; prompts should be treated the same way, as versioned config."

*Source ID: 3.7*

---

<a name="q8"></a>
## Q8. (Medium) How do you test whether a prompt change is better?
**Answer:** Run old and new prompts over the same dataset, score both (code checks, LLM-as-judge, pairwise comparison), check cost and latency, and look at the examples that got worse, not just the average.

**Simple version:** An A/B test on a fixed set of questions before shipping.

*Source ID: 3.8*

---

<a name="q9"></a>
## Q9. (Medium) How do you put retrieved context into a prompt safely and efficiently?
**Answer:** Format chunks with ids and sources (`[doc 3, 10-K 2022 p.47] ...`), put them in a clearly delimited section, instruct "answer only from the context and cite ids", order the most relevant first (and last, because models attend less to the middle), and cap total tokens.

**Tie to your project (P2):** "FinSight's citations work because every chunk carries filing and page metadata into the prompt."

*Source ID: 3.9*

---

<a name="q10"></a>
## Q10. (Medium) What is the "lost in the middle" problem?
**Answer:** Models use information at the start and end of a long context better than the middle. Mitigate with reranking and fewer, better chunks, and by placing the most important chunks at the edges (`LongContextReorder` does this).

*Source ID: 3.10*

---

<a name="q11"></a>
## Q11. (Medium) How do you write prompts that work across different models?
**Answer:** Keep prompts simple and explicit, avoid provider-specific tricks, use structured output instead of format instructions, and keep a small eval set per model. Expect to tune per model; store model-specific variants if needed.

**Tie to your project (P2):** "I ran the same pipeline on Ollama models and Claude; smaller local models needed tighter instructions and more examples." \[Only if true.\]

*Source ID: 3.11*

---

<a name="q12"></a>
## Q12. (Medium) How do you make the model say "I don't know"?
**Answer:** Explicitly allow and request it, give an example of it, add a structured field like `answerable: bool`, and check groundedness after generation. Reward it in evals so prompt changes don't remove it.

*Source ID: 3.12*

---

<a name="q13"></a>
## Q13. (Hard) What is prompt caching and how do you design for it?
**Answer:** Providers cache the processed prefix of a prompt, which cuts cost and latency on repeated calls. Keep the stable parts (system prompt, tool definitions, long documents) first and identical across calls, and variable parts last.

**Simple version:** Keep the start of the prompt the same every time so the provider can reuse its work.

*Source ID: 3.13*

---

<a name="q14"></a>
## Q14. (Hard) How do you build dynamic prompts based on user or context?
**Answer:** Compute variables at runtime (user role, permissions, language) and pass them into the template; in `create_agent`, use dynamic-prompt middleware to change the system prompt per call based on state or runtime context.

**Tie to your project (P4):** "In PNI Hub, the user's team and role come from Azure AD, so a prompt could tailor answers to their team's data."

*Source ID: 3.14*

---

<a name="q15"></a>
## Q15. (Hard) What are the most common prompt failures you've seen?
**Answer:** Vague instructions, contradictions between rules, too much irrelevant context, asking for JSON in text instead of structured output, no "unknown" path, and examples that bias the model toward one answer. Fix by being specific, cutting context, and testing on hard cases.

**How to say it:** Name one you actually hit and how you fixed it. A real story beats a list.

*Source ID: 3.15*
