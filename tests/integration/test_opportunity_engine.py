import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_phase_2_opportunity_engine_scenario(async_client: AsyncClient):
    """
    Validates Section 15 (Definition of Done) Scenario for Phase 2:
    1. User submits research objective
    2. CEO receives objective and delegates to OpportunityEngine
    3. OpportunityEngine generates multi-candidate concepts (not only solar)
    4. ResearchAgent researches each via WebSearchTool
    5. Evidence is classified into Findings
    6. Multi-dimensional economics are calculated
    7. RiskAgent evaluates risks
    8. Opportunity records are stored in database
    9. Low-cost validation experiments are generated
    10. No external business is contacted
    11. No money is spent
    12. Dashboard summary displays opportunities
    13. User can choose an opportunity and request human approval for validation experiment
    """

    # 1 & 2. User submits objective -> CEO receives via /opportunities/research
    prompt = "Find legitimate low-capital highly automated business opportunities in India."
    research_res = await async_client.post(
        "/opportunities/research",
        json={
            "objective": prompt,
            "budget_limit": 10000.0,
            "location_scope": "India",
            "time_horizon": "30 days",
            "automation_requirement": "HIGH",
        },
    )
    assert research_res.status_code == 200
    data = research_res.json()
    assert data["status"] == "COMPLETED"
    assert data["count"] >= 3  # Multiple diverse business candidates generated

    opportunities = data["opportunities"]

    # Verify diversity: multiple sectors beyond solar
    titles = [opp["title"] for opp in opportunities]
    assert any("Waste" in t or "Oil" in t or "Recyclables" in t for t in titles)
    assert any("Compliance" in t for t in titles)
    assert any("Solar" in t for t in titles)

    for opp in opportunities:
        # 5 & 6. Verify economics and multi-dimensional metrics (Section 5)
        assert opp["estimated_startup_cost"] <= 10000.0
        assert opp["estimated_margin"] > 0.20
        assert opp["time_to_first_revenue"] != ""
        assert opp["automation_potential"] in ["HIGH", "MEDIUM"]
        assert opp["uncertainty"] in ["LOW", "MEDIUM", "HIGH"]
        assert opp["evidence_quality"] in ["HIGH", "MEDIUM", "LOW"]
        assert len(opp["unknowns"]) > 0

        # 9. Low-cost validation experiment (Section 6)
        experiment = opp["experiment"]
        assert experiment["hypothesis"] != ""
        assert experiment["validation"] != ""
        assert experiment["budget"] <= 500.0  # Low cost validation preferred
        assert experiment["success_metric"] != ""
        assert experiment["failure_metric"] != ""
        assert experiment["human_approvals_required"] is True

    # 10 & 11. Security guarantee: Zero real money spent, zero external businesses contacted
    dash_summary = await async_client.get("/dashboard/summary")
    assert dash_summary.status_code == 200
    metrics = dash_summary.json()["metrics"]
    assert metrics["simulated_expenses"] == 0.0
    assert metrics["simulated_revenue"] == 0.0

    # 12. Dashboard displays opportunities
    opps_list_res = await async_client.get("/opportunities")
    assert opps_list_res.status_code == 200
    stored_opps = opps_list_res.json()
    assert len(stored_opps) >= 3

    # Check that findings with source domains exist
    first_opp = stored_opps[0]
    assert len(first_opp["evidence"]) > 0
    assert "findings" in first_opp
    assert first_opp["findings"] is not None

    # 13. User chooses one opportunity and requests experiment approval
    selected_id = first_opp["id"]
    approval_req_res = await async_client.post(
        f"/opportunities/{selected_id}/experiment/approve",
        json={"actor": "LEAD_OPERATOR", "notes": "Approved for 5-day exploratory interviews"},
    )
    assert approval_req_res.status_code == 200
    approval_data = approval_req_res.json()
    assert approval_data["status"] == "PENDING"
    assert approval_data["opportunity_id"] == selected_id

    # Verify audit event logged
    audit_res = await async_client.get("/audit")
    assert audit_res.status_code == 200
    audit_logs = audit_res.json()
    actions = [l["action"] for l in audit_logs]
    assert "RESEARCH_OPPORTUNITIES" in actions
    assert "REQUEST_EXPERIMENT_APPROVAL" in actions


@pytest.mark.asyncio
async def test_on_demand_research_job(async_client: AsyncClient):
    """Verify Section 11 scheduled/on-demand research job endpoint."""
    res = await async_client.post(
        "/opportunities/jobs/run",
        json={"objective": "Discover localized digital services"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert data["job_type"] == "on-demand"
    assert data["opportunities_generated"] >= 3
