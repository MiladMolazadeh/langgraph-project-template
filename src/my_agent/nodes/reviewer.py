from langchain_core.messages import SystemMessage
from my_agent.state import AgentState
from my_agent.prompts import REVIEWER_PROMPT
from my_agent.utils.llm import get_llm

_llm = get_llm()


def reviewer_node(state: AgentState) -> dict:
    messages = [SystemMessage(content=REVIEWER_PROMPT)] + state["messages"]
    response = _llm.invoke(messages)
    return {"messages": [response]}
