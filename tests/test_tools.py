from my_agent.tools.calculator import calculator_tool
from my_agent.tools.search import search_tool


def test_calculator_addition():
    result = calculator_tool.invoke({"expression": "2 + 2"})
    assert result == "4"


def test_calculator_handles_invalid_expression():
    result = calculator_tool.invoke({"expression": "import os"})
    assert "Error" in result


def test_search_tool_returns_string():
    result = search_tool.invoke({"query": "LangGraph tutorial"})
    assert isinstance(result, str)
    assert len(result) > 0
