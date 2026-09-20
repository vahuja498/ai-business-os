import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_first_vertical_slice_end_to_end(async_client: AsyncClient):
    """
    Test the complete First Vertical Slice per Section 30 of the Master Specification:
    1. User creates a business
    2. CEO receives objective
    3. Research Agent creates an opportunity
    4. Risk Agent evaluates it
    5. Approval request is generated
    6. Human approves
    7. Opportunity status changes to APPROVED
    8. Audit event is created
    9. Dashboard displays the result
    """

    # 1. User creates a business
    create_biz_res = await async_client.post(
        "/businesses",
        json={
            "name": "Apex Solar Leads",
            "description": "Autonomous solar lead generation business",
            "module_name": "solar_leads",
            "target_customer": "Urban rooftop owners",
        },
    )
    assert create_biz_res.status_code == 200
    biz_data = create_biz_res.json()
    business_id = biz_data["id"]
    assert biz_data["name"] == "Apex Solar Leads"
    assert biz_data["status"] == "DRAFT"

    # Verify audit event created for business creation
    audit_res_1 = await async_client.get(f"/audit?business_id={business_id}")
    assert audit_res_1.status_code == 200
    logs_1 = audit_res_1.json()
    assert any(log["action"] == "CREATE_BUSINESS" for log in logs_1)

    # 2. CEO receives objective
    objective = "Investigate rooftop solar lead generation viability in tier-1 metro areas"
    dispatch_res = await async_client.post(
        f"/businesses/{business_id}/objectives",
        json={"objective": objective},
    )
    assert dispatch_res.status_code == 200
    dispatch_data = dispatch_res.json()

    # 3. Research Agent created opportunity
    assert dispatch_data["opportunity"] is not None
    opportunity_id = dispatch_data["opportunity"]["id"]
    assert dispatch_data["opportunity"]["margin"] > 0.20
    assert dispatch_data["decomposed_tasks_count"] == 2

    # 4. Risk Agent evaluated it & 5. Approval request is generated
    assert dispatch_data["status"] == "PENDING_APPROVAL"
    assert len(dispatch_data["approvals"]) == 1
    approval = dispatch_data["approvals"][0]
    approval_id = approval["id"]
    assert approval["risk_level"] == "HIGH"
    assert approval["status"] == "PENDING"
    assert approval["amount"] == 500.0

    # Verify opportunity is currently PENDING_APPROVAL
    opp_res = await async_client.get(f"/opportunities/{opportunity_id}")
    assert opp_res.status_code == 200
    assert opp_res.json()["status"] == "PENDING_APPROVAL"

    # Verify dashboard summary shows pending approval
    dash_before = await async_client.get("/dashboard/summary")
    assert dash_before.status_code == 200
    assert dash_before.json()["metrics"]["pending_approvals"] >= 1

    # 6. Human approves
    approve_res = await async_client.post(
        f"/approvals/{approval_id}/approve",
        json={"actor": "OPERATOR_ALICE", "reason": "Market research economics validated and within trial budget."},
    )
    assert approve_res.status_code == 200
    assert approve_res.json()["status"] == "APPROVED"
    assert approve_res.json()["approved_by"] == "OPERATOR_ALICE"

    # 7. Opportunity status changes to APPROVED
    opp_after_res = await async_client.get(f"/opportunities/{opportunity_id}")
    assert opp_after_res.status_code == 200
    assert opp_after_res.json()["status"] == "APPROVED"

    # 8. Audit event is created
    audit_after = await async_client.get(f"/audit?business_id={business_id}")
    assert audit_after.status_code == 200
    logs_after = audit_after.json()
    action_types = [log["action"] for log in logs_after]
    assert "CREATE_BUSINESS" in action_types
    assert "EXECUTE_OBJECTIVE" in action_types
    assert "APPROVE_REQUEST" in action_types

    # 9. Dashboard displays the result
    dash_after = await async_client.get("/dashboard/summary")
    assert dash_after.status_code == 200
    dash_data = dash_after.json()
    assert dash_data["metrics"]["active_businesses"] >= 1
    assert dash_data["metrics"]["open_opportunities"] >= 1
    assert dash_data["metrics"]["pending_approvals"] == 0  # cleared after approval!
    approved_opps = [o for o in dash_data["recent_opportunities"] if o["id"] == opportunity_id]
    assert len(approved_opps) == 1
    assert approved_opps[0]["status"] == "APPROVED"
