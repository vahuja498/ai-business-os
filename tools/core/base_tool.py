from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel, Field
from policies.autonomy import AutonomyLevel
from policies.risk_rules import RiskLevel


class ToolExecutionContext(BaseModel):
    agent_id: str
    business_id: str | None = None
    task_id: str | None = None
    actor_autonomy_level: AutonomyLevel = AutonomyLevel.LEVEL_1_ASSIST
    granted_permissions: list[str] = Field(default_factory=list)


class BaseTool(ABC):
    def __init__(
        self,
        tool_id: str,
        name: str,
        description: str,
        risk_level: RiskLevel = RiskLevel.LOW,
        required_permissions: list[str] | None = None,
        required_autonomy_level: AutonomyLevel = AutonomyLevel.LEVEL_1_ASSIST,
    ):
        self.tool_id = tool_id
        self.name = name
        self.description = description
        self.risk_level = risk_level
        self.required_permissions = required_permissions or []
        self.required_autonomy_level = required_autonomy_level

    @abstractmethod
    async def execute(self, inputs: dict[str, Any], context: ToolExecutionContext) -> dict[str, Any]:
        """Execute the tool safely and return structured results."""
        pass
