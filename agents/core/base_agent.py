from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Any
from agents.core.llm.base_provider import ModelProvider, MockModelProvider
from agents.core.models import AgentMetadata, AgentRunRecord
from tools.core.base_tool import ToolExecutionContext
from tools.core.registry import ToolRegistry


class BaseAgent(ABC):
    def __init__(
        self,
        metadata: AgentMetadata,
        model_provider: ModelProvider | None = None,
    ):
        self.metadata = metadata
        self.model_provider = model_provider or MockModelProvider()

    @property
    def agent_id(self) -> str:
        return self.metadata.agent_id

    @property
    def name(self) -> str:
        return self.metadata.name

    async def call_tool(
        self,
        tool_id: str,
        inputs: dict[str, Any],
        business_id: str | None = None,
        task_id: str | None = None,
    ) -> dict[str, Any]:
        """Verify agent tool allowance and delegate execution to the governed ToolRegistry."""
        if tool_id not in self.metadata.allowed_tools:
            raise PermissionError(
                f"Agent '{self.name}' is not allowed to use tool '{tool_id}'. Allowed: {self.metadata.allowed_tools}"
            )

        context = ToolExecutionContext(
            agent_id=self.agent_id,
            business_id=business_id,
            task_id=task_id,
            actor_autonomy_level=self.metadata.autonomy_level,
            granted_permissions=self.metadata.allowed_tools,
        )

        return await ToolRegistry.execute_tool(tool_id, inputs, context)

    @abstractmethod
    async def run(self, input_data: dict[str, Any], business_id: str | None = None, task_id: str | None = None) -> AgentRunRecord:
        """Execute the agent task and return a fully auditable AgentRunRecord."""
        pass
