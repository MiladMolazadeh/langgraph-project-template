from typing import Any

from my_agent.config import settings


def get_callbacks() -> list[Any]:
    """Return active tracing callbacks based on environment configuration.

    LangSmith is enabled automatically via LANGCHAIN_TRACING_V2 env var — no callback needed.
    Langfuse requires explicit callback injection via this function.

    Usage:
        graph.invoke(state, config={"configurable": {...}, "callbacks": get_callbacks()})
    """
    callbacks: list[Any] = []

    if settings.langfuse_secret_key and settings.langfuse_public_key:
        try:
            from langfuse.callback import CallbackHandler
            callbacks.append(
                CallbackHandler(
                    secret_key=settings.langfuse_secret_key,
                    public_key=settings.langfuse_public_key,
                    host=settings.langfuse_host,
                )
            )
        except ImportError:
            import warnings
            warnings.warn("langfuse not installed — skipping. Run: uv add langfuse", stacklevel=2)

    return callbacks
