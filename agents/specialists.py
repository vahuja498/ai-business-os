from typing import Any
from agents.core.base_agent import BaseAgent
from agents.core.models import AgentMetadata, AgentRunRecord
from policies.autonomy import AutonomyLevel
from policies.risk_rules import RiskLevel


class SpecialistStubAgent(BaseAgent):
    def __init__(self, name: str, description: str, capabilities: list[str], allowed_tools: list[str]):
        metadata = AgentMetadata(
            name=name,
            description=description,
            capabilities=capabilities,
            allowed_tools=allowed_tools,
            system_policy="Standard specialist protocol.",
            risk_level=RiskLevel.LOW,
            autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )
        super().__init__(metadata=metadata)

    async def run(self, input_data: dict[str, Any], business_id: str | None = None, task_id: str | None = None) -> AgentRunRecord:
        record = AgentRunRecord(
            agent_id=self.agent_id,
            business_id=business_id,
            task_id=task_id,
            input_data=input_data,
            final_status="SUCCESS",
            outputs={"message": f"{self.name} stub executed successfully."},
        )
        return record


class GrowthAgent(SpecialistStubAgent):
    def __init__(self):
        super().__init__("GrowthAgent", "Manages user acquisition and marketing funnels", ["campaigns", "funnel_optimization"], ["web_search", "analytics"])


class SalesAgent(SpecialistStubAgent):
    def __init__(self):
        super().__init__("SalesAgent", "Executes customer sales outreach and conversion", ["lead_qualification", "pipeline_management"], ["crm", "messaging", "email"])


class OperationsAgent(SpecialistStubAgent):
    def __init__(self):
        super().__init__("OperationsAgent", "Coordinates vendor logistics and fulfilment", ["fulfilment", "vendor_coordination"], ["crm", "database"])


class FinanceAgent(SpecialistStubAgent):
    def __init__(self):
        super().__init__("FinanceAgent", "Monitors cash flow, margins, and transactions", ["ledger", "spend_tracking"], ["finance", "analytics"])


class AnalyticsAgent(SpecialistStubAgent):
    def __init__(self):
        super().__init__("AnalyticsAgent", "Tracks KPIs, cohort retention, and system metrics", ["kpi_tracking", "dashboard_metrics"], ["analytics", "database"])


class EngineeringAgent(SpecialistStubAgent):
    def __init__(self):
        super().__init__("EngineeringAgent", "Maintains integrations, schemas, and automation scripts", ["code_maintenance", "diagnostics"], ["database"])
