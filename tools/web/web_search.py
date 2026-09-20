from typing import Any
from policies.autonomy import AutonomyLevel
from policies.risk_rules import RiskLevel
from tools.core.base_tool import BaseTool, ToolExecutionContext


class WebSearchTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="web_search",
            name="Web Search",
            description="Searches public web information for market research and competitive data.",
            risk_level=RiskLevel.LOW,
            required_permissions=["web:search"],
            required_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )

    async def execute(self, inputs: dict[str, Any], context: ToolExecutionContext) -> dict[str, Any]:
        query = inputs.get("query", "").lower()

        # Deterministic mock results based on domain query
        if "solar" in query:
            return {
                "query": query,
                "results": [
                    {
                        "source": "https://gov.in/solar-tariffs-benchmark",
                        "claim_type": "FACT",
                        "title": "State Electricity Regulatory Commission Rooftop Solar Policy 2024",
                        "content": "Average residential electricity tariff is 7.50 INR/kWh. Commercial tariff averages 11.20 INR/kWh.",
                    },
                    {
                        "source": "https://market-research-reports.internal/solar-lead-costs",
                        "claim_type": "ESTIMATE",
                        "title": "India Rooftop Solar EPC Lead Generation Report",
                        "content": "EPC installers pay between 800 INR and 2,500 INR for verified site-visit-ready rooftop leads. Average conversion rate is 8-12%.",
                    },
                    {
                        "source": "https://industry-forum.internal/epc-survey",
                        "claim_type": "CLAIM",
                        "title": "Vendor Survey on Installer Bottlenecks",
                        "content": "Vendors report that 70% of inbound digital leads are unviable due to low monthly power bills (<1500 INR).",
                    },
                ],
            }

        return {
            "query": query,
            "results": [
                {
                    "source": "https://internal-knowledge.ai/general-market-data",
                    "claim_type": "FACT",
                    "title": f"Market Data for '{query}'",
                    "content": f"Verified market indicators for {query} indicate viable demand with 25-40% gross margins.",
                }
            ],
        }
