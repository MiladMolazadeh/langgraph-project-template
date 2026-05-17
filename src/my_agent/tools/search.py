from langchain_core.tools import tool


@tool
def search_tool(query: str) -> str:
    """Search the web for information about a given query."""
    # Replace with a real search integration (e.g. Tavily, SerpAPI)
    return f"Search results for: {query}"
