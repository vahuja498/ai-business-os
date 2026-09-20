import pytest
from httpx import AsyncClient

EXPECTED_FAMILIES = {
    "INFORMATION_ARBITRAGE",
    "LEAD_GENERATION",
    "SERVICE_ARBITRAGE",
    "PROCESS_AUTOMATION",
    "DISTRIBUTION_ARBITRAGE",
    "LEGITIMATE_INCENTIVE_SERVICES",
    "DIGITAL_PRODUCTS",
    "MARKETPLACE_ARBITRAGE",
}


@pytest.mark.asyncio
async def test_phase3_real_discovery_campaign_scenario(async_client: AsyncClient):
    """
    Validates Phase 3 Definition of Done:
    A real research campaign runs and produces at least 10 structured opportunities across
    multiple opportunity families with evidence, economics, uncertainties, contradictions,
    risks, validation experiment, and estimated automation potential.
    """
    # 1. Execute campaign across all 8 families
    campaign_payload = {
        "capital_limit": 10000.0,
        "geography": ["India", "Haryana", "Faridabad", "Online"],
        "time_horizon_days": 30,
        "opportunity_families": list(EXPECTED_FAMILIES),
    }

    res = await async_client.post("/opportunities/research", json=campaign_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "COMPLETED"
    assert data["count"] >= 10  # Must produce at least 10 opportunities per Definition of Done

    opportunities = data["opportunities"]
    assert len(opportunities) >= 10

    # 2. Verify all 8 Opportunity Families are covered
    found_families = {opp["opportunity_family"] for opp in opportunities}
    for fam in EXPECTED_FAMILIES:
        assert fam in found_families, f"Missing opportunity family: {fam}"

    # 3. Verify Local & Online geographical coverage (Section 6)
    all_geographies = {geo for opp in opportunities for geo in opp.get("geography", [])}
    assert "Haryana" in all_geographies
    assert "Faridabad" in all_geographies
    assert "Online" in all_geographies

    for opp in opportunities:
        # Verify required structured fields (Section 4 & 10)
        assert opp["title"] != ""
        assert opp["customer"] != ""
        assert opp["problem"] != ""
        assert opp["solution"] != ""
        assert opp["revenue_model"] != ""
        assert opp["estimated_startup_cost"] <= 10000.0
        assert opp["estimated_margin"] > 0.20
        assert opp["time_to_first_revenue"] != ""
        assert opp["automation_potential"] in ["HIGH", "MEDIUM"]
        assert opp["recurring_potential"] in ["HIGH", "MEDIUM", "LOW", "NONE"]

        # Verify Adversarial Reality Check (Section 7)
        assert "failure_modes" in opp
        assert len(opp["failure_modes"]) > 0  # "Why this may fail"
        assert "contradicting_evidence" in opp
        assert "reality_check" in opp
        assert len(opp["reality_check"]) == 10  # 10-point interrogation

        # Verify Low-Cost Validation Experiment (Section 8)
        exp = opp["experiment"]
        assert exp["hypothesis"] != ""
        assert exp["validation"] != ""
        assert exp["budget"] <= 500.0  # Max ₹500 validation budget
        assert exp["success_metric"] != ""
        assert exp["failure_metric"] != ""

        # Section 9 Rule: Must NOT rank opportunities with subjective winner badges
        assert "BEST" not in opp["title"]
        assert "#1" not in opp["title"]
        assert "WINNER" not in opp["title"]

    # 4. Verify Exportable Report Endpoint (Section 10)
    report_res = await async_client.get("/opportunities/report")
    assert report_res.status_code == 200
    report_data = report_res.json()
    assert report_data["count"] >= 10
    assert "markdown_report" in report_data
    assert "# AI Business OS — Opportunity Discovery Report" in report_data["markdown_report"]
    assert "Why This May Fail" in report_data["markdown_report"]

    # 5. Safety verification: Zero external actions and zero money spent
    dash_summary = await async_client.get("/dashboard/summary")
    assert dash_summary.status_code == 200
    dash_metrics = dash_summary.json()["metrics"]
    assert dash_metrics["simulated_expenses"] == 0.0
    assert dash_metrics["simulated_revenue"] == 0.0


@pytest.mark.asyncio
async def test_filter_opportunities_by_family(async_client: AsyncClient):
    """Verify filtering opportunities by specific opportunity family."""
    # Ensure opportunities are populated
    await async_client.post("/opportunities/research", json={"capital_limit": 10000.0})

    filter_res = await async_client.get("/opportunities?opportunity_family=PROCESS_AUTOMATION")
    assert filter_res.status_code == 200
    filtered = filter_res.json()
    assert len(filtered) > 0
    assert all(o["opportunity_family"] == "PROCESS_AUTOMATION" for o in filtered)
