from typing import Any
from policies.autonomy import AutonomyLevel
from policies.risk_rules import RiskLevel
from tools.core.base_tool import BaseTool, ToolExecutionContext
from tools.web.search_provider import MockWebSearchProvider, WebSearchProvider


class WebSearchTool(BaseTool):
    def __init__(self, provider: WebSearchProvider | None = None):
        super().__init__(
            tool_id="web_search",
            name="Governed Web Search",
            description="Searches web sources for business evidence with rate limiting, timeouts, and normalization.",
            risk_level=RiskLevel.LOW,
            required_permissions=["web:search"],
            required_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )
        self.provider = provider or MockWebSearchProvider()

    async def execute(self, inputs: dict[str, Any], context: ToolExecutionContext) -> dict[str, Any]:
        query = inputs.get("query", "").strip()
        if not query:
            return {"query": "", "results": []}

        search_results = await self.provider.search(query)

        # Map to standard output dictionary
        normalized_data = [res.model_dump() for res in search_results]

        # For backward compatibility with tests expecting results list with claim_type / content
        compat_results = [
            {
                "source": r.source_url,
                "claim_type": r.classification_hint,
                "title": r.source_title,
                "content": r.evidence_text,
                "domain": r.source_domain,
                "publication_date": r.publication_date,
                "relevance_score": r.relevance_score,
                "retrieved_at": r.retrieved_at,
            }
            for r in search_results
        ]

        return {
            "query": query,
            "results": compat_results,
            "normalized_findings": normalized_data,
        }
