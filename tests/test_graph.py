from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage


@patch("my_agent.nodes.planner.llm")
@patch("my_agent.nodes.executor.llm")
@patch("my_agent.nodes.reviewer.llm")
def test_graph_runs_end_to_end(mock_reviewer_llm, mock_executor_llm, mock_planner_llm):
    from my_agent.agent import graph

    mock_planner_llm.invoke.return_value = MagicMock(content="Step 1: search for data.")
    mock_executor_llm.invoke.return_value = MagicMock(content="Found the data.", tool_calls=[])
    mock_reviewer_llm.invoke.return_value = MagicMock(content="DONE: task complete.")

    result = graph.invoke(
        {"messages": [HumanMessage(content="Find population of France")]},
        config={"configurable": {"thread_id": "test-1"}},
    )

    assert "messages" in result
    assert len(result["messages"]) > 0
