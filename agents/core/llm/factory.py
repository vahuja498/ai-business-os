import os
from agents.core.llm.anthropic_provider import AnthropicProvider
from agents.core.llm.base_provider import ModelProvider, MockModelProvider
from agents.core.llm.gemini_provider import GeminiProvider
from agents.core.llm.openai_provider import OpenAIProvider


class ModelProviderFactory:
    @staticmethod
    def get_provider(
        provider_type: str | None = None,
        model_name: str | None = None,
    ) -> ModelProvider:
        provider = (provider_type or os.getenv("MODEL_PROVIDER", "mock")).lower()
        model = model_name or os.getenv("MODEL_NAME")

        if provider == "openai":
            return OpenAIProvider(model_name=model or "gpt-4o-mini")
        elif provider == "gemini":
            return GeminiProvider(model_name=model or "gemini-1.5-flash")
        elif provider == "anthropic":
            return AnthropicProvider(model_name=model or "claude-3-5-sonnet-20241022")
        else:
            return MockModelProvider()
