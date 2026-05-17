from langchain_core.messages import SystemMessage
from my_agent.state import AgentState
from my_agent.prompts import PLANNER_PROMPT
from my_agent.utils.llm import get_llm

_llm = get_llm()


def planner_node(state: AgentState) -> dict:
    messages = [SystemMessage(content=PLANNER_PROMPT)] + state["messages"]
    response = _llm.invoke(messages)
    return {"plan": response.content, "messages": [response]}
