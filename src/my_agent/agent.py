from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from my_agent.state import AgentState
from my_agent.nodes import planner_node, executor_node, reviewer_node
from my_agent.edges import route_after_planning, route_executor, route_after_review
from my_agent.tools import search_tool, calculator_tool


def build_graph() -> StateGraph:
    builder = StateGraph(AgentState)

    builder.add_node("planner", planner_node)
    builder.add_node("executor", executor_node)
    builder.add_node("tools", ToolNode([search_tool, calculator_tool]))
    builder.add_node("reviewer", reviewer_node)

    builder.set_entry_point("planner")

    builder.add_conditional_edges("planner", route_after_planning)
    builder.add_conditional_edges("executor", route_executor)
    builder.add_edge("tools", "executor")  # loop back after tool execution
    builder.add_conditional_edges("reviewer", route_after_review)

    return builder


checkpointer = MemorySaver()
graph = build_graph().compile(checkpointer=checkpointer)
