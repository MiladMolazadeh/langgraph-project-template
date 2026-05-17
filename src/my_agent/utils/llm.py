from typing import Any
from functools import lru_cache

from langchain_core.language_models import BaseChatModel
from my_agent.config import settings, LLMProvider


@lru_cache(maxsize=8)
def _build_llm(provider: LLMProvider, model: str, temperature: float, max_tokens: int) -> BaseChatModel:
    from langchain_openai import ChatOpenAI

    kwargs: dict[str, Any] = {"temperature": temperature, "max_tokens": max_tokens}

    if provider == LLMProvider.DEEPSEEK:
        return ChatOpenAI(
            model=model,
            base_url="https://api.deepseek.com/v1",
            api_key=settings.deepseek_api_key,
            **kwargs,
        )

    if provider == LLMProvider.OPENAI:
        return ChatOpenAI(model=model, **kwargs)

    if provider == LLMProvider.OPENROUTER:
        return ChatOpenAI(
            model=model,
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
            **kwargs,
        )

    raise ValueError(f"Unsupported provider: {provider}")


def get_llm(tools: list[Any] | None = None) -> BaseChatModel:
    llm = _build_llm(
        provider=settings.llm_provider,
        model=settings.model_name,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
    )
    return llm.bind_tools(tools) if tools else llm
