# Multi-Agent Systems
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Fifteen questions on multi-agent architectures. Your CV doesn't claim a multi-agent system, so present P1 and P3 as the basis and describe extensions honestly as "how I would extend it".

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [What multi-agent architectures do you know?](#q1)
2. (Easy) [When should you use multiple agents instead of one?](#q2)
3. (Easy) [How would you extend your promotion workflow into a multi-agent system?](#q3)
4. (Easy) [How do you build a supervisor in LangGraph?](#q4)
5. (Medium) [What is a handoff?](#q5)
6. (Medium) [How do agents share context without blowing up the context window?](#q6)
7. (Medium) [What are the failure modes of multi-agent systems?](#q7)
8. (Medium) [How do you evaluate a multi-agent system?](#q8)
9. (Medium) [Supervisor versus swarm: how do you choose?](#q9)
10. (Medium) [How do you run agents in parallel and combine results?](#q10)
11. (Medium) [Can different agents use different models?](#q11)
12. (Medium) [How do you prevent one agent from doing something it shouldn't?](#q12)
13. (Hard) [What is the role of MCP in multi-agent systems?](#q13)
14. (Hard) [What is A2A (agent-to-agent protocol)?](#q14)
15. (Hard) [How do you debug a multi-agent run?](#q15)

---

<a name="q1"></a>
## Q1. (Easy) What multi-agent architectures do you know?
**Answer:**

- **Supervisor:** a central agent routes work to specialists and decides when done (`langgraph-supervisor` or custom). Easy to reason about; can bottleneck.
- **Swarm / handoffs:** agents pass control directly with handoff tools (`langgraph-swarm`, `Command(goto=...)`). Fewer hops, harder to trace.
- **Hierarchical:** supervisors of supervisors, each team a subgraph.
- **Agents as tools:** a main agent calls sub-agents as tools and gets back only their final answer.
- **Network:** anyone calls anyone; rarely wise in production.

**Simple version:** A manager with a team, colleagues passing a ticket, or an org chart.

*Source ID: 10.1*

---

<a name="q2"></a>
## Q2. (Easy) When should you use multiple agents instead of one?
**Answer:** When one agent has too many tools (roughly over 10 to 15), domains need very different instructions, context grows too large, or parts can run in parallel. Otherwise one agent with good tools is cheaper, faster and easier to debug.

**How to say it:** "I start with one agent and split only when I see tool confusion or context overload in traces."

*Source ID: 10.2*

---

<a name="q3"></a>
## Q3. (Easy) How would you extend your promotion workflow into a multi-agent system?
**Answer:** A supervisor with an evidence agent (using the PNI Hub MCP tools), a policy agent (knows promotion criteria, cites them), and a writer agent (drafts feedback). The supervisor enforces the fixed process and the human approval interrupt.

**Tie to your project (P1 and P3):** Say clearly: "This is a proposed extension, not what's deployed."

*Source ID: 10.3*

---

<a name="q4"></a>
## Q4. (Easy) How do you build a supervisor in LangGraph?
**Answer:** A supervisor node (LLM with structured output choosing the next worker or FINISH), worker nodes (each a `create_agent` or subgraph), edges from every worker back to the supervisor, and a conditional edge from the supervisor to the chosen worker or END. Or use `create_supervisor(agents=[...], model=...)` from `langgraph-supervisor`.

*Source ID: 10.4*

---

<a name="q5"></a>
## Q5. (Medium) What is a handoff?
**Answer:** One agent transfers control to another, usually via a tool like `transfer_to_billing` that returns `Command(goto="billing", graph=Command.PARENT, update={...})`. The update decides what context the next agent receives.

**Simple version:** "I'm passing you this ticket, here are my notes."

*Source ID: 10.5*

---

<a name="q6"></a>
## Q6. (Medium) How do agents share context without blowing up the context window?
**Answer:** Choose per design: full shared message history (simple, costly), only final outputs, or private message lists per agent plus a shared structured state for facts (ids, decisions). Sub-agents as tools return only a summary.

**Simple version:** Pass meeting notes, not the full recording.

*Source ID: 10.6*

---

<a name="q7"></a>
## Q7. (Medium) What are the failure modes of multi-agent systems?
**Answer:** Handoff loops, duplicated work, lost context, higher cost and latency (each hop is an LLM call), and hard-to-trace errors. Mitigate with recursion limits, clear responsibilities, structured handoff payloads, per-agent tracing, and evaluating each agent alone first.

*Source ID: 10.7*

---

<a name="q8"></a>
## Q8. (Medium) How do you evaluate a multi-agent system?
**Answer:** Unit-evaluate each agent on its own dataset, evaluate routing accuracy (did the supervisor pick the right worker?), then end-to-end task success, cost and step count. Look at traces for wasted hops.

*Source ID: 10.8*

---

<a name="q9"></a>
## Q9. (Medium) Supervisor versus swarm: how do you choose?
**Answer:** Supervisor when you need central control, auditability and a fixed process (enterprise workflows). Swarm when agents are peers and conversations move naturally between specialities (customer support). Supervisor is the safer default.

**Tie to your project (P1):** "For promotions I'd pick a supervisor: auditability matters more than saving a hop."

*Source ID: 10.9*

---

<a name="q10"></a>
## Q10. (Medium) How do you run agents in parallel and combine results?
**Answer:** Fan out with `Send` or static edges to several agent subgraphs, write results into a list with a reducer, then a synthesiser node combines them. Example: research agents each covering one source.

*Source ID: 10.10*

---

<a name="q11"></a>
## Q11. (Medium) Can different agents use different models?
**Answer:** Yes, and they should when it saves cost: a strong model for the supervisor or planner, smaller ones for narrow workers (extraction, formatting), maybe a local model for sensitive data.

*Source ID: 10.11*

---

<a name="q12"></a>
## Q12. (Medium) How do you prevent one agent from doing something it shouldn't?
**Answer:** Give each agent only its own tools and permissions, validate outputs at handoffs, and put human approval in front of side-effecting agents. Never let a worker escalate its own privileges.

*Source ID: 10.12*

---

<a name="q13"></a>
## Q13. (Hard) What is the role of MCP in multi-agent systems?
**Answer:** MCP servers become shared tool backends: several agents (and teams) use the same server, with consistent auth and logging, instead of each re-implementing integrations.

**Tie to your project (P3):** "The PNI Hub MCP server can serve any agent we build, not just one."

*Source ID: 10.13*

---

<a name="q14"></a>
## Q14. (Hard) What is A2A (agent-to-agent protocol)?
**Answer:** An emerging standard for agents from different systems to discover and call each other (agent cards, tasks). MCP connects agents to tools and data; A2A connects agents to other agents. Mention it as awareness; details may change.

*Source ID: 10.14*

---

<a name="q15"></a>
## Q15. (Hard) How do you debug a multi-agent run?
**Answer:** LangSmith traces with each agent as a named sub-run, stream with `subgraphs=True` to see which agent is active, log handoff payloads, and replay from checkpoints.

*Source ID: 10.15*
