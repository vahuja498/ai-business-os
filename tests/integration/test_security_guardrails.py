import pytest
from httpx import AsyncClient
from policies.guardrails import FinancialGuardrails
from policies.risk_rules import RiskEvaluator, RiskLevel
from tools.core.base_tool import ToolExecutionContext
from tools.core.registry import ToolRegistry


@pytest.mark.asyncio
async def test_agent_cannot_bypass_approval(async_client: AsyncClient):
    # 1. Create a business
    create_res = await async_client.post(
        "/businesses",
        json={"name": "Security Test Biz", "module_name": "core"},
    )
    assert create_res.status_code == 200
    biz_id = create_res.json()["id"]

    # 2. Dispatch objective requiring budget
    obj_res = await async_client.post(
        f"/businesses/{biz_id}/objectives",
        json={"objective": "Test ad campaign launch"},
    )
    assert obj_res.status_code == 200
    data = obj_res.json()

    # Opportunity is PENDING_APPROVAL and cannot be active/completed without human sign-off
    assert data["status"] == "PENDING_APPROVAL"
    assert len(data["approvals"]) > 0
    approval_id = data["approvals"][0]["id"]

    # Verify opportunity in db is also PENDING_APPROVAL
    opps_res = await async_client.get(f"/opportunities?business_id={biz_id}")
    assert opps_res.json()[0]["status"] == "PENDING_APPROVAL"

    # Verify that approving with invalid status or re-approving fails
    approve_res = await async_client.post(f"/approvals/{approval_id}/approve", json={"actor": "TEST_HUMAN"})
    assert approve_res.status_code == 200
    assert approve_res.json()["status"] == "APPROVED"

    # Security check: approval cannot be reused incorrectly
    duplicate_approve_res = await async_client.post(f"/approvals/{approval_id}/approve", json={"actor": "TEST_HUMAN"})
    assert duplicate_approve_res.status_code == 400
    assert "Approval cannot be approved from current status" in duplicate_approve_res.json()["detail"]


def test_agent_cannot_exceed_spending_limit():
    guardrails = FinancialGuardrails(max_transaction_amount=1000.0, max_daily_spend=500.0)
    allowed, reason = guardrails.validate_transaction(2500.0)
    assert allowed is False
    assert "exceeds max single transaction limit" in reason


def test_blocked_action_cannot_execute():
    # Verify that prohibited patterns cannot pass evaluation
    res = RiskEvaluator.evaluate_text_and_action("phishing", "Collect sensitive banking credentials")
    assert res.risk_level == RiskLevel.BLOCKED
    assert res.requires_approval is False


@pytest.mark.asyncio
async def test_tool_cannot_execute_unauthorized_network_or_system_call():
    # Verify that arbitrary or unregistered tools cannot be executed
    ctx = ToolExecutionContext(agent_id="test_agent")
    with pytest.raises(ValueError, match="Tool 'arbitrary_shell_command' is not registered"):
        await ToolRegistry.execute_tool("arbitrary_shell_command", {}, ctx)


@pytest.mark.asyncio
async def test_business_isolation(async_client: AsyncClient):
    # Create business A and business B
    res_a = await async_client.post("/businesses", json={"name": "Business A", "module_name": "core"})
    biz_a_id = res_a.json()["id"]

    res_b = await async_client.post("/businesses", json={"name": "Business B", "module_name": "core"})
    biz_b_id = res_b.json()["id"]

    # Run objective in Business A
    await async_client.post(f"/businesses/{biz_a_id}/objectives", json={"objective": "Opportunity A"})

    # Query opportunities for Business B -> must be empty
    opps_b = await async_client.get(f"/opportunities?business_id={biz_b_id}")
    assert len(opps_b.json()) == 0

    # Query opportunities for Business A -> exactly 1
    opps_a = await async_client.get(f"/opportunities?business_id={biz_a_id}")
    assert len(opps_a.json()) == 1
    assert opps_a.json()[0]["business_id"] == biz_a_id
