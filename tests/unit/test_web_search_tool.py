import asyncio
import time
import pytest
from tools.core.base_tool import ToolExecutionContext
from tools.core.registry import ToolRegistry
from tools.web.search_provider import MockWebSearchProvider, WebSearchProvider
from tools.web.web_search import WebSearchTool


class SlowSearchProvider(WebSearchProvider):
    def __init__(self):
        super().__init__(rate_limit_delay_sec=0.2, timeout_sec=0.1, max_retries=1)

    async def _execute_search(self, query: str):
        await asyncio.sleep(0.5)  # will trigger timeout
        return []


@pytest.mark.asyncio
async def test_mock_search_normalization():
    provider = MockWebSearchProvider()
    results = await provider.search("solar rooftop tariffs")

    assert len(results) > 0
    first = results[0]
    assert first.source_url.startswith("http")
    assert first.source_domain != ""
    assert first.evidence_text != ""
    assert first.relevance_score >= 0.8
    assert first.classification_hint in ["FACT", "CLAIM", "ESTIMATE"]


@pytest.mark.asyncio
async def test_rate_limiting_enforcement():
    class FastTestProvider(WebSearchProvider):
        def __init__(self):
            super().__init__(rate_limit_delay_sec=0.1, timeout_sec=2.0)

        async def _execute_search(self, query: str):
            return []

    p = FastTestProvider()
    t0 = time.time()
    await p.search("query 1")
    await p.search("query 2")
    duration = time.time() - t0
    assert duration >= 0.1  # Rate limit delayed second call


@pytest.mark.asyncio
async def test_timeout_and_retry_handling():
    slow_provider = SlowSearchProvider()
    with pytest.raises(RuntimeError, match="Web search failed after 1 retries"):
        await slow_provider.search("timeout test")


@pytest.mark.asyncio
async def test_web_search_tool_registry_execution():
    tool = WebSearchTool(provider=MockWebSearchProvider())
    ToolRegistry.register(tool)

    ctx = ToolExecutionContext(
        agent_id="research_agent",
        granted_permissions=["web:search"],
    )
    res = await ToolRegistry.execute_tool("web_search", {"query": "waste recycling lead"}, ctx)
    assert res["status"] == "SUCCESS"
    assert "results" in res["result"]
    assert "normalized_findings" in res["result"]
    assert len(res["result"]["results"]) > 0
