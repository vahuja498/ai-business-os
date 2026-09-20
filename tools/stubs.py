from typing import Any
from policies.autonomy import AutonomyLevel
from policies.risk_rules import RiskLevel
from tools.core.base_tool import BaseTool, ToolExecutionContext


class CRMTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="crm",
            name="CRM Management",
            description="Manage customer, lead, and contact records.",
            risk_level=RiskLevel.LOW,
            required_permissions=["crm:write"],
            required_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )

    async def execute(self, inputs: dict[str, Any], context: ToolExecutionContext) -> dict[str, Any]:
        return {"status": "ok", "action": inputs.get("action", "record_updated"), "details": inputs}


class FinanceTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="finance",
            name="Finance & Payments",
            description="Execute payments, record expenses, and check ledger balances.",
            risk_level=RiskLevel.HIGH,
            required_permissions=["finance:transact"],
            required_autonomy_level=AutonomyLevel.LEVEL_2_CONTROLLED_AUTONOMY,
        )

    async def execute(self, inputs: dict[str, Any], context: ToolExecutionContext) -> dict[str, Any]:
        amount = inputs.get("amount", 0.0)
        return {
            "status": "simulated_success",
            "amount": amount,
            "currency": inputs.get("currency", "INR"),
            "transaction_type": inputs.get("type", "expense"),
        }


class MessagingTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="messaging",
            name="Messaging & Chat",
            description="Send direct chat notifications or customer messages.",
            risk_level=RiskLevel.MEDIUM,
            required_permissions=["messaging:send"],
            required_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )

    async def execute(self, inputs: dict[str, Any], context: ToolExecutionContext) -> dict[str, Any]:
        return {"status": "queued", "recipient": inputs.get("recipient"), "message_length": len(inputs.get("text", ""))}


class EmailTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="email",
            name="Email Communication",
            description="Send transactional or outreach emails.",
            risk_level=RiskLevel.MEDIUM,
            required_permissions=["email:send"],
            required_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )

    async def execute(self, inputs: dict[str, Any], context: ToolExecutionContext) -> dict[str, Any]:
        return {"status": "simulated_sent", "to": inputs.get("to"), "subject": inputs.get("subject")}


class DatabaseTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="database",
            name="Internal Database Query",
            description="Safely query internal tables and business metrics.",
            risk_level=RiskLevel.LOW,
            required_permissions=["db:read"],
            required_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )

    async def execute(self, inputs: dict[str, Any], context: ToolExecutionContext) -> dict[str, Any]:
        return {"status": "ok", "table": inputs.get("table", "unknown"), "rows_returned": 0}


class AnalyticsTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="analytics",
            name="Analytics & Reporting",
            description="Compute conversion rates, margins, and operational KPIs.",
            risk_level=RiskLevel.LOW,
            required_permissions=["analytics:read"],
            required_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )

    async def execute(self, inputs: dict[str, Any], context: ToolExecutionContext) -> dict[str, Any]:
        return {"status": "ok", "metrics": {"conversion_rate": 0.10, "estimated_margin": 0.35}}


class BrowserTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="browser",
            name="Automated Browser",
            description="Render pages and extract DOM content safely.",
            risk_level=RiskLevel.LOW,
            required_permissions=["browser:scrape"],
            required_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )

    async def execute(self, inputs: dict[str, Any], context: ToolExecutionContext) -> dict[str, Any]:
        return {"status": "ok", "url": inputs.get("url"), "title": "Page Content Placeholder"}
