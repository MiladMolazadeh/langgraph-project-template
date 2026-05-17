from langchain_core.messages import SystemMessage
from my_agent.state import AgentState
from my_agent.prompts import EXECUTOR_PROMPT
from my_agent.tools import search_tool, calculator_tool
from my_agent.utils.llm import get_llm

_llm = get_llm(tools=[search_tool, calculator_tool])


def executor_node(state: AgentState) -> dict:
    messages = [SystemMessage(content=EXECUTOR_PROMPT.format(plan=state["plan"]))] + state["messages"]
    response = _llm.invoke(messages)
    return {"result": response.content, "messages": [response]}
