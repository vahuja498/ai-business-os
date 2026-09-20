import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_phase5_validation_engine_end_to_end(async_client: AsyncClient):
    """End-to-end integration test for Phase 5 Validation Engine."""
    # 1. Populate Phase 4 opportunities
    res_pop = await async_client.post(
        "/opportunities/research",
        json={"objective": "Execute Phase 4 campaign", "capital_limit": 10000.0},
    )
    assert res_pop.status_code == 200
    assert res_pop.json()["count"] == 24

    # 2. Sync Validation Plans for all 24 opportunities
    res_sync = await async_client.post("/validation/sync")
    assert res_sync.status_code == 200
    sync_data = res_sync.json()
    assert sync_data["status"] == "SUCCESS"
    assert sync_data["data"]["total_synced"] == 24
    assert sync_data["data"]["created"] == 24

    # 3. List all validation plans
    res_plans = await async_client.get("/validation")
    assert res_plans.status_code == 200
    plans = res_plans.json()
    assert len(plans) == 24

    # Verify non-comparative confidence score and assumptions count
    for p in plans:
        assert 0.0 <= p["confidence_score"] <= 1.0
        assert p["material_assumptions_count"] >= 7
        assert 3 <= p["high_risk_assumptions_count"] <= 7
        assert p["total_budget_spent"] == 0.0
        assert p["total_budget_allocated"] > 0.0

    # 4. Retrieve single Validation Plan Detail
    first_plan = plans[0]
    opp_id = first_plan["opportunity_id"]
    res_detail = await async_client.get(f"/validation/{opp_id}")
    assert res_detail.status_code == 200
    detail = res_detail.json()

    assert detail["opportunity"]["id"] == opp_id
    assert len(detail["assumptions"]) >= 7
    assert len(detail["experiments"]) >= 3
    assert detail["budget"]["max_budget"] == 2500.0
    assert detail["budget"]["allocated_amount"] > 0.0

    # Verify all experiments adhere to <= ₹500 budget cap
    for exp in detail["experiments"]:
        assert exp["budget"] <= 500.0
        assert exp["pass_criteria"]
        assert exp["fail_criteria"]
        assert exp["inconclusive_criteria"]
        assert exp["is_simulation"] is True

    # 5. List Experiments
    res_exps = await async_client.get("/validation/experiments")
    assert res_exps.status_code == 200
    all_exps = res_exps.json()
    assert len(all_exps) >= 72  # at least 3 per plan * 24

    # 6. Run Experiment Simulation
    test_exp = all_exps[0]
    exp_id = test_exp["id"]

    res_run = await async_client.post(
        f"/validation/experiments/{exp_id}/run",
        json={
            "outcome": "PASS",
            "metric_observed": "4 out of 10 prospective respondents confirmed intent.",
            "cost_spent": min(100.0, test_exp["budget"]),
            "evidence_artifacts": ["sim_intake_log.json"],
            "notes": "Simulated intake diagnostic run.",
            "is_simulation": True,
            "update_assumption_to": "SUPPORTED_ESTIMATE",
            "justification": "Supported by empirical simulated inquiry logs.",
        },
    )
    assert res_run.status_code == 200
    run_data = res_run.json()
    assert run_data["status"] == "SUCCESS"
    assert run_data["outcome"] == "PASS"

    # 7. Check Results Log
    res_results = await async_client.get("/validation/results")
    assert res_results.status_code == 200
    results_list = res_results.json()
    assert len(results_list) >= 1
    assert results_list[0]["outcome"] == "PASS"
    assert results_list[0]["simulated"] is True

    # 8. Test Approvals Gate
    res_apprv = await async_client.get("/validation/approvals")
    assert res_apprv.status_code == 200
    apprv_list = res_apprv.json()
    assert len(apprv_list) > 0

    first_apprv = apprv_list[0]
    res_decide = await async_client.post(
        f"/validation/approvals/{first_apprv['id']}/decide",
        json={"action": "APPROVE", "decided_by": "TestReviewer"},
    )
    assert res_decide.status_code == 200
    assert res_decide.json()["decision"] == "APPROVED"

    # 9. Test Integrity Guardrail Violation (Reject UNKNOWN -> VERIFIED without empirical evidence)
    res_integrity_violation = await async_client.post(
        f"/validation/experiments/{exp_id}/run",
        json={
            "outcome": "PASS",
            "metric_observed": "Fabricated success",
            "cost_spent": 10.0,
            "evidence_artifacts": [],
            "notes": "No evidence",
            "is_simulation": True,
            "update_assumption_to": "VERIFIED",
            "justification": "",  # Missing empirical evidence and justification
        },
    )
    assert res_integrity_violation.status_code == 400
    assert "Integrity violation" in res_integrity_violation.json()["detail"]

    # 10. Test Spending Guardrail Violation (Cost > budget cap)
    res_budget_violation = await async_client.post(
        f"/validation/experiments/{exp_id}/run",
        json={
            "outcome": "PASS",
            "metric_observed": "Over budget",
            "cost_spent": 999.0,  # Exceeds max ₹500 cap
            "evidence_artifacts": [],
            "notes": "Cost violation",
            "is_simulation": True,
        },
    )
    assert res_budget_violation.status_code == 400
    assert "Spending guardrail" in res_budget_violation.json()["detail"]
