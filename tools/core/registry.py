import time
from typing import Any
from policies.autonomy import AutonomyLevel
from policies.risk_rules import RiskLevel
from tools.core.base_tool import BaseTool, ToolExecutionContext


class ToolRegistry:
    _tools: dict[str, BaseTool] = {}

    @classmethod
    def register(cls, tool: BaseTool) -> None:
        cls._tools[tool.tool_id] = tool

    @classmethod
    def get(cls, tool_id: str) -> BaseTool | None:
        return cls._tools.get(tool_id)

    @classmethod
    def list_tools(cls) -> list[dict[str, Any]]:
        return [
            {
                "tool_id": t.tool_id,
                "name": t.name,
                "description": t.description,
                "risk_level": t.risk_level.value,
                "required_permissions": t.required_permissions,
                "required_autonomy_level": t.required_autonomy_level.value,
            }
            for t in cls._tools.values()
        ]

    @classmethod
    async def execute_tool(
        cls,
        tool_id: str,
        inputs: dict[str, Any],
        context: ToolExecutionContext,
    ) -> dict[str, Any]:
        tool = cls.get(tool_id)
        if not tool:
            raise ValueError(f"Tool '{tool_id}' is not registered.")

        # Guard: BLOCKED risk level
        if tool.risk_level == RiskLevel.BLOCKED:
            raise PermissionError(f"Execution of tool '{tool_id}' is BLOCKED by safety policy.")

        # Guard: Autonomy level check
        if not AutonomyLevel.can_execute_autonomously(context.actor_autonomy_level, tool.required_autonomy_level):
            raise PermissionError(
                f"Tool '{tool_id}' requires {tool.required_autonomy_level.value}, but actor has {context.actor_autonomy_level.value}."
            )

        # Guard: Permission check
        for perm in tool.required_permissions:
            if perm not in context.granted_permissions:
                raise PermissionError(f"Missing required permission '{perm}' to execute tool '{tool_id}'.")

        start_time = time.perf_counter()
        try:
            result = await tool.execute(inputs, context)
            duration_ms = (time.perf_counter() - start_time) * 1000
            return {
                "status": "SUCCESS",
                "tool_id": tool_id,
                "duration_ms": duration_ms,
                "result": result,
                "error": None,
            }
        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            return {
                "status": "FAILED",
                "tool_id": tool_id,
                "duration_ms": duration_ms,
                "result": None,
                "error": str(e),
            }
