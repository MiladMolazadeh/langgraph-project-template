from langgraph.graph import END
from my_agent.state import AgentState
from my_agent.utils import get_last_message


def route_after_planning(state: AgentState) -> str:
    if state.get("error"):
        return END
    return "executor"


def route_executor(state: AgentState) -> str:
    last_message = get_last_message(state)
    if last_message and getattr(last_message, "tool_calls", None):
        return "tools"
    return "reviewer"


def route_after_review(state: AgentState) -> str:
    last_message = get_last_message(state)
    content = last_message.content.lower() if last_message else ""

    if "retry" in content or "revise" in content:
        return "planner"
    return END
