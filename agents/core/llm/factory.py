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
        role: str | None = None,  # "research", "ceo", "classification", or None
    ) -> ModelProvider:
        provider = (provider_type or os.getenv("MODEL_PROVIDER", "mock")).lower()

        # Dynamic role-based model resolution without hard-coding historical model strings
        if not model_name:
            if role == "research":
                model_name = os.getenv("RESEARCH_MODEL") or os.getenv("MODEL_NAME", "standard-model")
            elif role == "ceo":
                model_name = os.getenv("CEO_MODEL") or os.getenv("MODEL_NAME", "standard-model")
            elif role == "classification":
                model_name = os.getenv("CLASSIFICATION_MODEL") or os.getenv("MODEL_NAME", "standard-model")
            else:
                model_name = os.getenv("MODEL_NAME", "standard-model")

        if provider == "openai":
            return OpenAIProvider(model_name=model_name)
        elif provider == "gemini":
            return GeminiProvider(model_name=model_name)
        elif provider == "anthropic":
            return AnthropicProvider(model_name=model_name)
        else:
            return MockModelProvider()
