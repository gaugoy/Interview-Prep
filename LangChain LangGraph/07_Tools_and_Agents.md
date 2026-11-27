# Tools & Agents
### [← LangChain & LangGraph index](./README.md) · [Question Bank](./Question_Bank.md)

Eighteen questions on tools, tool calling, agents and MCP. Your MCP server (P3) is a differentiator, so bring it up whenever tools come up.

**Topics:** [Fundamentals](./01_LangChain_Fundamentals.md) · [LCEL](./02_LCEL_and_Runnables.md) · [Prompts](./03_Prompts.md) · [Models](./04_Models_and_Structured_Output.md) · [Memory](./05_Memory_and_Chat_History.md) · [RAG](./06_RAG.md) · [Tools & Agents](./07_Tools_and_Agents.md) · [LangGraph](./08_LangGraph_Core.md) · [Checkpointing](./09_Checkpointing_and_HITL.md) · [Multi-agent](./10_Multi_Agent_Systems.md) · [Streaming](./11_Streaming_and_Async.md) · [LangSmith](./12_LangSmith_and_Evaluation.md) · [Production](./13_Production_and_Django.md) · [System Design](./14_System_Design.md)

## Table of Contents

1. (Easy) [What is a tool and how does tool calling work?](#q1)
2. (Easy) [How do you define a tool?](#q2)
3. (Easy) [What makes a good tool design?](#q3)
4. (Easy) [What is a ReAct agent and how does `create_agent` work?](#q4)
5. (Easy) [What is MCP and how does it relate to LangChain tools?](#q5)
6. (Medium) [What are MCP tools, resources and prompts?](#q6)
7. (Medium) [How do you secure an MCP server?](#q7)
8. (Medium) [How do you stop an agent looping forever or calling the wrong tool?](#q8)
9. (Medium) [How do you handle tool errors?](#q9)
10. (Medium) [When do you choose an agent versus a fixed workflow?](#q10)
11. (Medium) [What is middleware in LangChain 1.x?](#q11)
12. (Medium) [How do you require human approval before a tool runs?](#q12)
13. (Medium) [How does the model choose between many tools? What if there are 100?](#q13)
14. (Medium) [What are parallel tool calls?](#q14)
15. (Hard) [What is `ToolNode` and `tools_condition`?](#q15)
16. (Hard) [How do you give a tool access to state, config or the user id?](#q16)
17. (Hard) [What is a planning agent (plan-and-execute)?](#q17)
18. (Hard) [How do you evaluate an agent?](#q18)

---

<a name="q1"></a>
## Q1. (Easy) What is a tool and how does tool calling work?
**Answer:** A function the model can ask to run, described by name, description and argument schema. Flow: bind tools to the model, the model returns an `AIMessage` with `tool_calls` (name + JSON args), your code runs the function, you send back a `ToolMessage` with the matching `tool_call_id`, and the model answers or calls more tools. The model never executes anything itself.

**Simple version:** The model writes a request slip; your code does the work and hands back the result.

*Source ID: 7.1*

---

<a name="q2"></a>
## Q2. (Easy) How do you define a tool?
```python
from langchain.tools import tool
from pydantic import BaseModel, Field

class BugQuery(BaseModel):
    team: str = Field(description="Team name, e.g. 'QA' or 'Integration'")
    days: int = Field(30, ge=1, le=365)

@tool(args_schema=BugQuery)
def get_open_bugs(team: str, days: int = 30) -> list[dict]:
    """Return open Jira bugs for a team created in the last N days."""
    ...
```

**Answer:** `@tool` uses the docstring and type hints as the schema; `args_schema` gives full Pydantic validation. `StructuredTool.from_function` and `BaseTool` subclasses also work.

**How to say it:** "The description is a prompt. Most tool bugs come from vague descriptions or overlapping tools."

**Tie to your project (P3):** "In the MCP server I spent real effort on names, descriptions and typed parameters so the client model picks the right tool."

*Source ID: 7.2*

---

<a name="q3"></a>
## Q3. (Easy) What makes a good tool design?
**Answer:** One clear job per tool, distinct names, descriptions that say when to use it and when not to, typed and constrained arguments, small outputs (summaries, top N plus counts), helpful error messages, idempotency for writes, and least privilege.

**Simple version:** Tools should be like good API endpoints: obvious, narrow and safe.

**Tie to your project (P4):** "I've designed 40+ REST endpoints for PNI Hub; the same API-design discipline applies to tools."

*Source ID: 7.3*

---

<a name="q4"></a>
## Q4. (Easy) What is a ReAct agent and how does `create_agent` work?
**Answer:** Reason + Act loop: think, call a tool, observe, repeat. `create_agent(model, tools, system_prompt=..., middleware=[...], checkpointer=..., response_format=...)` builds this as a LangGraph graph: model node, tools node, and a conditional edge that loops while there are tool calls.

**How to say it:** "The loop is simple; the engineering is in stopping conditions, tool design, error handling and observability."

*Source ID: 7.4*

---

<a name="q5"></a>
## Q5. (Easy) What is MCP and how does it relate to LangChain tools?
**Answer:** The Model Context Protocol is an open standard for exposing tools, resources and prompts to any AI client through a server (stdio or streamable HTTP). A LangChain tool lives in one app; an MCP server serves Claude Desktop, IDEs and your agents alike. `langchain-mcp-adapters` (`MultiServerMCPClient`) loads MCP tools as LangChain tools.

**Simple version:** A USB port for AI tools.

**Tie to your project (P3):** "I built an MCP server over PNI Hub so teams can ask platform questions in natural language from any MCP client. Adopted by \[N\] teams."

*Source ID: 7.5*

---

<a name="q6"></a>
## Q6. (Medium) What are MCP tools, resources and prompts?
**Answer:** Tools = actions the model can call. Resources = read-only data the client can load into context (files, records). Prompts = reusable prompt templates the server offers. Servers declare capabilities; clients discover them at connection time.

*Source ID: 7.6*

---

<a name="q7"></a>
## Q7. (Medium) How do you secure an MCP server?
**Answer:** Authenticate clients (OAuth for remote servers), authorise per user, scope tools to read-only where possible, validate arguments, rate-limit, log every call, never return secrets, and require confirmation for writes.

**Tie to your project (P3 and P4):** "Our server reuses PNI Hub's Azure AD identity so users only see data they could see in the UI." \[Confirm.\]

*Source ID: 7.7*

---

<a name="q8"></a>
## Q8. (Medium) How do you stop an agent looping forever or calling the wrong tool?
**Answer:** `recursion_limit` or call-limit middleware; a small, non-overlapping toolset (split into sub-agents beyond roughly 10 to 15 tools); helpful error messages; Pydantic argument validation; watch traces for repeated calls.

*Source ID: 7.8*

---

<a name="q9"></a>
## Q9. (Medium) How do you handle tool errors?
**Answer:** Catch exceptions in the tool and return a clear message the model can act on ("team 'qa' not found; valid teams: QA, Integration"). In `create_agent`, tool-error handling can be customised with `wrap_tool_call` middleware. Re-raise only for errors the model can't fix (auth failures), and route those to a human or an error state.

*Source ID: 7.9*

---

<a name="q10"></a>
## Q10. (Medium) When do you choose an agent versus a fixed workflow?
**Answer:** Workflow when the process is known and must be auditable (approvals, compliance, ETL). Agent when the path can't be known ahead (open research, data exploration). Most production systems are mostly workflow with small agentic pieces.

**Tie to your project (P1 vs P3):** "Promotions are a workflow; the LLM only evaluates and drafts. MCP querying is agentic because users ask anything."

*Source ID: 7.10*

---

<a name="q11"></a>
## Q11. (Medium) What is middleware in LangChain 1.x?
**Answer:** Hooks around the agent loop: `before_model`, `after_model`, `wrap_model_call`, `wrap_tool_call`. Built-ins include summarisation, human-in-the-loop, PII redaction, model fallback, call limits and tool retries. You can write your own with decorators or classes.

**Simple version:** Like Django middleware, but around each model and tool call.

*Source ID: 7.11*

---

<a name="q12"></a>
## Q12. (Medium) How do you require human approval before a tool runs?
**Answer:** `HumanInTheLoopMiddleware(interrupt_on={"send_email": True, "delete_record": True})` in `create_agent` with a checkpointer. The agent pauses before those tools; a human approves, edits the arguments or rejects; you resume with `Command(resume=...)`. In a custom graph, call `interrupt()` inside the tool or a review node.

*Source ID: 7.12*

---

<a name="q13"></a>
## Q13. (Medium) How does the model choose between many tools? What if there are 100?
**Answer:** It reads names, descriptions and schemas, so overlap confuses it and many tools cost tokens. For large toolsets: group tools into sub-agents, or retrieve the most relevant tools per request (tool RAG) and bind only those. Dynamic tool selection is possible with middleware.

*Source ID: 7.13*

---

<a name="q14"></a>
## Q14. (Medium) What are parallel tool calls?
**Answer:** Modern models can return several tool calls in one message; the tools node runs them concurrently, then all results go back together. Disable with `parallel_tool_calls=False` when order matters or tools have side effects.

*Source ID: 7.14*

---

<a name="q15"></a>
## Q15. (Hard) What is `ToolNode` and `tools_condition`?
**Answer:** LangGraph prebuilts for custom graphs: `ToolNode(tools)` executes the tool calls in the last AI message and returns `ToolMessage`s; `tools_condition` is a router that goes to the tools node if there are tool calls, else to END.

*Source ID: 7.15*

---

<a name="q16"></a>
## Q16. (Hard) How do you give a tool access to state, config or the user id?
**Answer:** Don't put them in the model-visible arguments. Use injected arguments: `ToolRuntime` (or `InjectedState`, `InjectedToolArg`) to access state, context (like `user_id`) and the store inside the tool, hidden from the schema the model sees.

**How to say it:** "The model should never be able to pick the user id. Identity is injected from the request context."

**Tie to your project (P3):** "That's how per-user scoping works: identity comes from auth, not from the prompt."

*Source ID: 7.16*

---

<a name="q17"></a>
## Q17. (Hard) What is a planning agent (plan-and-execute)?
**Answer:** A planner model writes a list of steps, an executor runs them (with tools), and a re-planner adjusts after results. Fewer calls to the expensive model and clearer progress, but less flexible than ReAct for surprises. Built easily in LangGraph.

*Source ID: 7.17*

---

<a name="q18"></a>
## Q18. (Hard) How do you evaluate an agent?
**Answer:** Final answer correctness, trajectory (right tools in sensible order), tool-argument accuracy, number of steps and cost, and safety (no forbidden actions). Run on a dataset in LangSmith with code and LLM-judge evaluators.

**Tie to your project (P3):** "For the MCP server, a question set with the expected tool and arguments would measure tool-selection accuracy."

*Source ID: 7.18*
