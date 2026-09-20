import os
import pytest
from agents.core.llm.factory import ModelProviderFactory
from agents.core.llm.openai_provider import OpenAIProvider
from agents.core.llm.gemini_provider import GeminiProvider
from agents.core.llm.anthropic_provider import AnthropicProvider


def test_model_id_independence_from_historical_names(monkeypatch):
    """
    Section 1 Requirement:
    The code must not assume that GPT-4o, Gemini 1.5, Claude 3.5 Sonnet,
    or any other historical model remains available.
    """
    monkeypatch.setenv("MODEL_PROVIDER", "openai")
    monkeypatch.setenv("MODEL_NAME", "future-nextgen-model-2026")
    monkeypatch.setenv("RESEARCH_MODEL", "future-deep-researcher-v2")

    # Base provider
    p_base = ModelProviderFactory.get_provider()
    assert isinstance(p_base, OpenAIProvider)
    assert p_base.model_name == "future-nextgen-model-2026"

    # Role-based research model
    p_research = ModelProviderFactory.get_provider(role="research")
    assert isinstance(p_research, OpenAIProvider)
    assert p_research.model_name == "future-deep-researcher-v2"


def test_role_based_model_resolution(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "gemini")
    monkeypatch.setenv("CEO_MODEL", "gemini-custom-planner-pro")
    monkeypatch.setenv("CLASSIFICATION_MODEL", "gemini-custom-classifier-lite")

    p_ceo = ModelProviderFactory.get_provider(role="ceo")
    assert isinstance(p_ceo, GeminiProvider)
    assert p_ceo.model_name == "gemini-custom-planner-pro"

    p_class = ModelProviderFactory.get_provider(role="classification")
    assert isinstance(p_class, GeminiProvider)
    assert p_class.model_name == "gemini-custom-classifier-lite"


def test_anthropic_custom_model_resolution(monkeypatch):
    monkeypatch.setenv("MODEL_PROVIDER", "anthropic")
    monkeypatch.setenv("MODEL_NAME", "claude-next-frontier-custom")

    p_anthropic = ModelProviderFactory.get_provider()
    assert isinstance(p_anthropic, AnthropicProvider)
    assert p_anthropic.model_name == "claude-next-frontier-custom"
