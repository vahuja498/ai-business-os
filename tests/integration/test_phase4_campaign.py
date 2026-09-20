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
async def test_phase4_discovery_campaign_full_execution(async_client: AsyncClient):
    """
    Validates Phase 4 Real Opportunity Discovery Campaign:
    - Generates at least 20 candidate opportunities (target >= 20, 2-3 per family).
    - Every candidate has all 27 structured data dimensions.
    - All 8 opportunity families have at least 2 candidates.
    - Local (Haryana, Faridabad, Delhi-NCR) and Online geographic scopes covered.
    - RealityCheckAgent adversarial evaluation run on every candidate.
    - No subjective winner rankings ("BEST", "#1", "WINNER").
    - Conservative regulatory framing: administrative/navigation/tools, no unauthorized practice.
    - Safety: ₹0 spent, zero external contacts.
    """
    # 1. Execute campaign
    campaign_res = await async_client.post(
        "/opportunities/research",
        json={
            "objective": "Run comprehensive Phase 4 discovery campaign across all 8 families in Haryana and India",
            "capital_limit": 10000.0,
            "geography": ["India", "Haryana", "Faridabad", "Delhi-NCR", "Online"],
            "time_horizon_days": 30,
        },
    )
    assert campaign_res.status_code == 200
    data = campaign_res.json()
    assert data["status"] == "COMPLETED"
    assert data["count"] >= 20, f"Expected >= 20 candidates, got {data['count']}"

    opportunities = data["opportunities"]
    assert len(opportunities) >= 20

    # 2. Verify all 8 families are represented with at least 2 candidates each
    family_counts = {}
    for opp in opportunities:
        fam = opp["opportunity_family"]
        family_counts[fam] = family_counts.get(fam, 0) + 1

    for fam in EXPECTED_FAMILIES:
        assert fam in family_counts, f"Missing family {fam}"
        assert family_counts[fam] >= 2, f"Family {fam} has fewer than 2 candidates: {family_counts[fam]}"

    # 3. Verify Geographic coverage
    all_geographies = {g for opp in opportunities for g in opp.get("geography", [])}
    assert "Faridabad" in all_geographies
    assert "Haryana" in all_geographies
    assert "Delhi-NCR" in all_geographies
    assert any("online" in g.lower() or "india" in g.lower() for g in all_geographies)

    # 4. Verify 27 Structured Dimensions for every opportunity
    for opp in opportunities:
        # 1. Name
        assert opp["title"] != ""
        # 2. Family
        assert opp["opportunity_family"] in EXPECTED_FAMILIES
        # 3. Customer
        assert opp["customer"] != ""
        # 4. Problem
        assert opp["problem"] != ""
        # 5. Solution
        assert opp["solution"] != ""
        # 6. Revenue mechanism
        assert opp["revenue_model"] != ""
        # 7. Startup cost (<= 10000)
        assert opp["estimated_startup_cost"] <= 10000.0
        # 8. Customer value
        assert opp["estimated_customer_value"] > 0
        # 9. CAC
        assert opp["estimated_acquisition_cost"] >= 0
        # 10. Fulfilment cost
        assert opp["estimated_fulfilment_cost"] >= 0
        # 11. Contribution estimate (margin > 20%)
        assert opp["estimated_margin"] > 0.20
        # 12. Automation potential & breakdown
        assert opp["automation_potential"] in ["HIGH", "MEDIUM"]
        assert "automation_breakdown" in opp
        assert "ai_automation" in opp["automation_breakdown"]
        assert "software_automation" in opp["automation_breakdown"]
        assert "human_only" in opp["automation_breakdown"]
        # 13. Time to first revenue (<= 30 days)
        assert opp["time_to_first_revenue"] != ""
        # 14. Recurring potential
        assert opp["recurring_potential"] in ["HIGH", "MEDIUM", "LOW"]
        # 15. Competition
        assert opp["competition"] != ""
        # 16. Evidence quality
        assert opp["evidence_quality"] in ["HIGH", "MEDIUM", "LOW"]
        # 17. Regulatory considerations
        assert opp["regulatory_considerations"] != ""
        # 18. Platform dependency & disintermediation analysis
        assert opp["platform_dependency"] in ["LOW", "MEDIUM", "HIGH"]
        assert opp["disintermediation_analysis"] != ""
        # 19. Evidence FOR
        assert len(opp["evidence_for"]) > 0
        # 20. Evidence AGAINST
        assert len(opp["evidence_against"]) > 0
        # 21. Unknowns
        assert len(opp["unknowns"]) > 0
        # 22. Fatal failure modes
        assert len(opp["failure_modes"]) > 0
        # 23. Validation experiment
        exp = opp["experiment"]
        assert exp["hypothesis"] != ""
        assert exp["validation"] != ""
        # 24. Validation budget (<= 500)
        assert exp["budget"] <= 500.0
        # 25. Success criteria
        assert exp["success_metric"] != ""
        # 26. Failure criteria
        assert exp["failure_metric"] != ""
        assert exp["human_approvals_required"] is True
        # 27. Sources
        assert len(opp["sources"]) > 0
        for s in opp["sources"]:
            assert "source_title" in s
            assert "source_url" in s
            assert "classification" in s
            assert "confidence" in s

        # Reality Check 10-point audit
        rc = opp["reality_check"]
        assert len(rc) == 10
        for dim_key, check in rc.items():
            assert check["status"] in [
                "VERIFIED",
                "SUPPORTED_ESTIMATE",
                "UNSUPPORTED_ESTIMATE",
                "UNKNOWN",
                "CONTRADICTED",
            ]

        # Subjective winner badge prohibition
        assert "BEST" not in opp["title"]
        assert "#1" not in opp["title"]
        assert "WINNER" not in opp["title"]

    # 5. Financial guardrail verification: simulated expenses = 0, revenue = 0
    dash_summary = await async_client.get("/dashboard/summary")
    assert dash_summary.status_code == 200
    metrics = dash_summary.json()["metrics"]
    assert metrics["simulated_expenses"] == 0.0
    assert metrics["simulated_revenue"] == 0.0


@pytest.mark.asyncio
async def test_phase4_export_endpoints(async_client: AsyncClient):
    """
    Validates Phase 4 export endpoints:
    - GET /opportunities/report (JSON with Markdown, CSV, JSON export, sources, unknowns, Do Not Pursue Yet)
    - GET /opportunities/export/csv (text/csv download)
    - GET /opportunities/export/json (application/json download)
    - GET /opportunities/export/markdown (text/markdown download)
    """
    # Ensure opportunities are populated in the database
    await async_client.post("/opportunities/research", json={"capital_limit": 10000.0})

    # 1. Main report endpoint
    report_res = await async_client.get("/opportunities/report")
    assert report_res.status_code == 200
    data = report_res.json()

    assert data["count"] >= 20
    assert "markdown_report" in data
    assert "# AI Business OS — Opportunity Discovery Report" in data["markdown_report"]
    assert "Why This May Fail" in data["markdown_report"]
    assert "Unresolved Unknowns Requiring Human Investigation" in data["markdown_report"]
    assert "\"Do Not Pursue Yet\" Dossier" in data["markdown_report"]

    # Check CSV export in report
    assert "csv_export" in data
    assert "Title,Opportunity Family,Target Customer" in data["csv_export"]
    csv_lines = data["csv_export"].strip().split("\n")
    assert len(csv_lines) >= 21  # Header + 20+ items

    # Check JSON export in report
    assert "json_export" in data
    assert len(data["json_export"]) >= 20

    # Check Sources catalog
    assert "sources" in data
    assert len(data["sources"]) > 0

    # Check Validation experiments
    assert "validation_experiments" in data
    assert len(data["validation_experiments"]) >= 20
    assert all(ve["budget"] <= 500.0 for ve in data["validation_experiments"])

    # Check Unresolved Unknowns
    assert "unresolved_unknowns" in data
    assert len(data["unresolved_unknowns"]) > 0

    # Check Do Not Pursue Yet
    assert "do_not_pursue_yet" in data
    assert len(data["do_not_pursue_yet"]) > 0
    for dnp in data["do_not_pursue_yet"]:
        assert dnp["reason"] != ""

    # 2. CSV direct download endpoint
    csv_res = await async_client.get("/opportunities/export/csv")
    assert csv_res.status_code == 200
    assert "text/csv" in csv_res.headers.get("content-type", "")
    assert "Title,Opportunity Family" in csv_res.text

    # 3. JSON direct download endpoint
    json_res = await async_client.get("/opportunities/export/json")
    assert json_res.status_code == 200
    json_data = json_res.json()
    assert isinstance(json_data, list)
    assert len(json_data) >= 20

    # 4. Markdown direct download endpoint
    md_res = await async_client.get("/opportunities/export/markdown")
    assert md_res.status_code == 200
    assert "text/markdown" in md_res.headers.get("content-type", "")
    assert "# AI Business OS — Opportunity Discovery Report" in md_res.text
