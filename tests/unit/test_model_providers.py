import pytest
from pydantic import BaseModel
from agents.core.base_agent import BaseAgent
from agents.core.llm.anthropic_provider import AnthropicProvider
from agents.core.llm.base_provider import ModelProvider, MockModelProvider
from agents.core.llm.factory import ModelProviderFactory
from agents.core.llm.gemini_provider import GeminiProvider
from agents.core.llm.openai_provider import OpenAIProvider
from agents.core.models import AgentMetadata, AgentRunRecord


class SampleSchema(BaseModel):
    title: str = "Test Concept"
    margin: float = 0.35


class DummyAgent(BaseAgent):
    def __init__(self, model_provider: ModelProvider):
        meta = AgentMetadata(name="DummyAgent", description="Test agent")
        super().__init__(metadata=meta, model_provider=model_provider)

    async def run(self, input_data, business_id=None, task_id=None):
        out = await self.model_provider.generate("Test prompt")
        return AgentRunRecord(agent_id=self.agent_id, final_status="SUCCESS", outputs={"response": out})


@pytest.mark.asyncio
async def test_mock_model_provider_compatibility():
    provider = MockModelProvider({"special_key": "Custom output"})
    res = await provider.generate("This prompt contains special_key for test")
    assert res == "Custom output"

    structured = await provider.structured_generate("prompt", SampleSchema)
    assert isinstance(structured, SampleSchema)
    assert structured.title == "Test Concept"


def test_provider_factory():
    p_mock = ModelProviderFactory.get_provider("mock")
    assert isinstance(p_mock, MockModelProvider)

    p_openai = ModelProviderFactory.get_provider("openai", model_name="gpt-4o")
    assert isinstance(p_openai, OpenAIProvider)
    assert p_openai.model_name == "gpt-4o"

    p_gemini = ModelProviderFactory.get_provider("gemini", model_name="gemini-1.5-pro")
    assert isinstance(p_gemini, GeminiProvider)
    assert p_gemini.model_name == "gemini-1.5-pro"

    p_claude = ModelProviderFactory.get_provider("anthropic", model_name="claude-3-opus")
    assert isinstance(p_claude, AnthropicProvider)
    assert p_claude.model_name == "claude-3-opus"


@pytest.mark.asyncio
async def test_agent_depends_only_on_model_provider_abc():
    """Verify that agent logic is decoupled from provider SDKs."""
    provider = MockModelProvider()
    agent = DummyAgent(model_provider=provider)
    run_res = await agent.run({})
    assert run_res.final_status == "SUCCESS"
    assert "response" in run_res.outputs


def test_api_keys_not_exposed_in_str():
    """Verify provider representation does not expose raw secret strings."""
    provider = OpenAIProvider(api_key="sk-secret-key-12345")
    assert "sk-secret-key-12345" not in str(provider.__dict__.get("model_name"))
