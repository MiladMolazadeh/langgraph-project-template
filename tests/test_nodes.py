from unittest.mock import MagicMock, patch
from my_agent.state import AgentState


def make_state(**kwargs) -> AgentState:
    defaults: AgentState = {
        "messages": [],
        "plan": "",
        "result": "",
        "error": None,
        "metadata": {},
    }
    return {**defaults, **kwargs}


@patch("my_agent.nodes.planner.llm")
def test_planner_node_returns_plan(mock_llm):
    from my_agent.nodes.planner import planner_node

    mock_llm.invoke.return_value = MagicMock(content="Step 1: do X. Step 2: do Y.")
    state = make_state(messages=[])

    result = planner_node(state)

    assert "plan" in result
    assert result["plan"] == "Step 1: do X. Step 2: do Y."


@patch("my_agent.nodes.executor.llm")
def test_executor_node_returns_result(mock_llm):
    from my_agent.nodes.executor import executor_node

    mock_llm.invoke.return_value = MagicMock(content="Task completed.")
    state = make_state(plan="Step 1: do X.", messages=[])

    result = executor_node(state)

    assert "result" in result


@patch("my_agent.nodes.reviewer.llm")
def test_reviewer_node_returns_message(mock_llm):
    from my_agent.nodes.reviewer import reviewer_node

    mock_llm.invoke.return_value = MagicMock(content="DONE: Task completed successfully.")
    state = make_state(messages=[])

    result = reviewer_node(state)

    assert "messages" in result
