import uuid
from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field
from policies.autonomy import AutonomyLevel
from policies.risk_rules import RiskLevel


class AgentMetadata(BaseModel):
    agent_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    capabilities: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    system_policy: str = ""
    business_scope: str | None = None
    execution_mode: str = "AUTONOMOUS"
    risk_level: RiskLevel = RiskLevel.LOW
    autonomy_level: AutonomyLevel = AutonomyLevel.LEVEL_1_ASSIST


class AgentRunRecord(BaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_id: str
    task_id: str | None = None
    business_id: str | None = None
    input_data: dict[str, Any] = Field(default_factory=dict)
    actions: list[str] = Field(default_factory=list)
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    outputs: dict[str, Any] = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
    approval_requests: list[dict[str, Any]] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: datetime | None = None
    final_status: str = "PENDING"  # SUCCESS, FAILED, PENDING_APPROVAL
