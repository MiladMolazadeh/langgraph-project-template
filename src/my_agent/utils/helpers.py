from langchain_core.messages import BaseMessage
from my_agent.state import AgentState


def get_last_message(state: AgentState) -> BaseMessage | None:
    messages = state.get("messages", [])
    return messages[-1] if messages else None


def format_messages(messages: list[BaseMessage]) -> str:
    return "\n".join(
        f"{msg.__class__.__name__}: {msg.content}"
        for msg in messages
    )
