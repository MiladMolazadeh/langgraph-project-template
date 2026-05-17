# my-langgraph-project

A LangGraph agent with a **planner → executor → reviewer** architecture, with support for multiple LLM providers and optional observability via LangSmith and Langfuse.

## Graph Architecture

```
__start__
    │
    ▼
 planner ──(error)──► __end__
    │
    ▼
 executor ──(tool_calls)──► tools ──► executor
    │
    ▼
 reviewer ──(retry/revise)──► planner
    │
    ▼
 __end__
```

Run `graph.get_graph().print_ascii()` in the notebook for a live view.

## Project Structure

```
src/my_agent/
├── config.py         # Provider/model settings (pydantic-settings)
├── agent.py          # Graph definition and compilation
├── state.py          # AgentState schema
├── nodes/            # planner, executor, reviewer
├── edges/            # Conditional routing logic
├── tools/            # LangChain tools
├── prompts/          # Prompt templates
└── utils/
    ├── llm.py        # LLM factory (provider-agnostic)
    ├── tracing.py    # Langfuse / LangSmith callbacks
    └── helpers.py    # Shared helpers
```

## Setup

```bash
uv sync
cp .env.example .env  # then fill in your keys
```

### Choose your LLM provider

Edit `.env`:

```bash
# DeepSeek (default — deepseek-v4-flash)
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-...

# OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# OpenRouter (access any model via one key)
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
LLM_MODEL=deepseek/deepseek-v3   # any OpenRouter model slug
```

## Run (LangGraph dev server)

```bash
make dev
# or directly:
uv run langgraph dev
```

This starts the LangGraph Studio UI and API server using `langgraph.json`.

## Observability

### LangSmith

Set in `.env` — no code changes needed:

```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=my-langgraph-project
```

### Langfuse

Install and configure:

```bash
uv add langfuse
```

```bash
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```

Pass callbacks when invoking the graph:

```python
from my_agent.utils.tracing import get_callbacks

graph.invoke(
    {"messages": [HumanMessage(content="Your task")]},
    config={
        "configurable": {"thread_id": "session-1"},
        "callbacks": get_callbacks(),
    },
)
```

## Test

```bash
make test
```

## LangGraph Platform

Deploy to LangGraph Cloud:

```bash
langgraph build
langgraph deploy
```
