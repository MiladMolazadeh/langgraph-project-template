# LangGraph Project Template

A production-ready starting point for building LangGraph agents. Comes with a **planner → executor → reviewer** reference graph, multi-provider LLM support, observability wiring, and a uv-based dev setup.

## What's Included

| Area | What you get |
|---|---|
| **Graph** | Planner → Executor → Reviewer with tool-call loop and retry logic |
| **LLM providers** | DeepSeek (default), OpenAI, OpenRouter — swap via `.env` |
| **Observability** | LangSmith (zero-config) + Langfuse (optional callback) |
| **Dev server** | `langgraph dev` via `langgraph.json` |
| **Notebook** | Graph visualization + interactive invocation |
| **Tests** | pytest suite for nodes, graph, and tools |
| **Tooling** | uv, hatchling, ruff, mypy |

## Quickstart

```bash
git clone https://github.com/your-org/your-repo.git
cd your-repo
uv sync
cp .env.example .env   # fill in your API key
make dev               # starts LangGraph Studio
```

## Customising the Template

### 1. Rename the package

```bash
mv src/my_agent src/your_agent
```

Update references in `pyproject.toml`, `langgraph.json`, and `src/your_agent/__init__.py`.

### 2. Redefine the state

Edit `src/your_agent/state.py` — add or remove fields from `AgentState`.

### 3. Replace or add nodes

Each file in `src/your_agent/nodes/` is one node function. Add new files, register them in `agent.py`.

### 4. Adjust routing

Edit `src/your_agent/edges/routing.py` to change when the graph retries, calls tools, or exits.

### 5. Add tools

Drop new `@tool` functions into `src/your_agent/tools/` and register them in `agent.py`'s `ToolNode`.

## Graph Architecture

```
__start__
    │
    ▼
 planner ──(error)──────────────────────► __end__
    │
    ▼
 executor ──(tool_calls)──► tools ──► executor  (loop)
    │
    ▼
 reviewer ──(retry / revise)──► planner
    │
    ▼
 __end__
```

## LLM Providers

Switch provider in `.env` — no code changes needed:

```bash
# OpenRouter (default — deepseek/deepseek-v4-flash)
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-...
LLM_MODEL=deepseek/deepseek-v4-flash   # any OpenRouter model slug

# DeepSeek direct
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-...

# OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

## Observability

**LangSmith** — set in `.env`, works automatically:
```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=my-project
```

**Langfuse** — install and configure:
```bash
uv add langfuse
```
```bash
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
```
Pass `"callbacks": get_callbacks()` in your graph config to activate.

## Common Commands

```bash
make install     # uv sync
make dev         # langgraph dev (Studio + API)
make test        # pytest
make lint        # ruff check + format
make typecheck   # mypy
```

## Project Structure

```
src/my_agent/
├── config.py          # Provider/model settings (pydantic-settings)
├── agent.py           # Graph definition and compilation
├── state.py           # AgentState schema  ← start here
├── nodes/             # One file per node
├── edges/routing.py   # All conditional edge logic
├── tools/             # @tool functions
├── prompts/           # Prompt templates
└── utils/
    ├── llm.py         # Provider-agnostic LLM factory
    ├── tracing.py     # Langfuse / LangSmith callbacks
    └── helpers.py     # Shared helpers
```
