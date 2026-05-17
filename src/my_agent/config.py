from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMProvider(str, Enum):
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    OPENROUTER = "openrouter"


_DEFAULTS: dict[str, str] = {
    LLMProvider.DEEPSEEK: "deepseek-v4-flash",
    LLMProvider.OPENAI: "gpt-4o",
    LLMProvider.OPENROUTER: "deepseek/deepseek-v4-flash",
}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # LLM provider
    llm_provider: LLMProvider = LLMProvider.DEEPSEEK
    llm_model: str = ""
    llm_temperature: float = 0.0
    llm_max_tokens: int = 4096

    # API keys
    deepseek_api_key: str = ""
    openai_api_key: str = ""
    openrouter_api_key: str = ""

    # LangSmith (tracing is enabled automatically when langchain_tracing_v2=true)
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "my-langgraph-project"

    # Langfuse
    langfuse_secret_key: str = ""
    langfuse_public_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"

    @property
    def model_name(self) -> str:
        return self.llm_model or _DEFAULTS[self.llm_provider]


settings = Settings()
