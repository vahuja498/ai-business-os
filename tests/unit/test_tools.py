import pytest
from policies.autonomy import AutonomyLevel
from policies.risk_rules import RiskLevel
from tools.core.base_tool import BaseTool, ToolExecutionContext
from tools.core.registry import ToolRegistry


class DummySafeTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="dummy_safe",
            name="Dummy Safe",
            description="Safe test tool",
            risk_level=RiskLevel.LOW,
            required_permissions=["test:dummy"],
            required_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )

    async def execute(self, inputs, context):
        return {"data": inputs.get("val", 42)}


class DummyHighAutonomyTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="dummy_high_autonomy",
            name="Dummy High Autonomy",
            description="High autonomy required",
            risk_level=RiskLevel.MEDIUM,
            required_permissions=["test:high"],
            required_autonomy_level=AutonomyLevel.LEVEL_3_HIGH_AUTONOMY,
        )

    async def execute(self, inputs, context):
        return {"result": "high"}


class DummyBlockedTool(BaseTool):
    def __init__(self):
        super().__init__(
            tool_id="dummy_blocked",
            name="Dummy Blocked",
            description="Blocked tool",
            risk_level=RiskLevel.BLOCKED,
        )

    async def execute(self, inputs, context):
        return {"result": "should_never_execute"}


@pytest.mark.asyncio
async def test_tool_execution_success():
    tool = DummySafeTool()
    ToolRegistry.register(tool)

    ctx = ToolExecutionContext(
        agent_id="test_agent",
        actor_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        granted_permissions=["test:dummy"],
    )
    res = await ToolRegistry.execute_tool("dummy_safe", {"val": 100}, ctx)
    assert res["status"] == "SUCCESS"
    assert res["result"]["data"] == 100


@pytest.mark.asyncio
async def test_tool_permission_denied():
    tool = DummySafeTool()
    ToolRegistry.register(tool)

    ctx = ToolExecutionContext(
        agent_id="test_agent",
        actor_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        granted_permissions=[],  # missing test:dummy
    )
    with pytest.raises(PermissionError, match="Missing required permission"):
        await ToolRegistry.execute_tool("dummy_safe", {"val": 100}, ctx)


@pytest.mark.asyncio
async def test_tool_insufficient_autonomy():
    tool = DummyHighAutonomyTool()
    ToolRegistry.register(tool)

    ctx = ToolExecutionContext(
        agent_id="test_agent",
        actor_autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,  # Less than LEVEL_3
        granted_permissions=["test:high"],
    )
    with pytest.raises(PermissionError, match="requires LEVEL_3_HIGH_AUTONOMY"):
        await ToolRegistry.execute_tool("dummy_high_autonomy", {}, ctx)


@pytest.mark.asyncio
async def test_tool_blocked_by_safety():
    tool = DummyBlockedTool()
    ToolRegistry.register(tool)

    ctx = ToolExecutionContext(
        agent_id="test_agent",
        actor_autonomy_level=AutonomyLevel.LEVEL_3_HIGH_AUTONOMY,
        granted_permissions=[],
    )
    with pytest.raises(PermissionError, match="BLOCKED by safety policy"):
        await ToolRegistry.execute_tool("dummy_blocked", {}, ctx)
