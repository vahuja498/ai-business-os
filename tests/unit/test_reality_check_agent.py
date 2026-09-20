import pytest
from agents.reality_check.reality_check_agent import (
    RealityCheckAgent,
    RealityCheckStatus,
)


@pytest.mark.asyncio
async def test_reality_check_adversarial_evaluation():
    agent = RealityCheckAgent()
    candidate = {
        "title": "Industrial Solar EPC Lead Pre-Qualification",
        "opportunity_family": "LEAD_GENERATION",
        "customer": "Licensed Solar EPC Installers",
        "target_market": "Solar vendors in NCR",
        "customer_value": 2000.0,
        "cac": 450.0,
        "startup_cost": 4500.0,
        "estimated_margin": 0.65,
        "evidence": [
            "State electricity tariff reports show strong demand for industrial solar in Haryana.",
            "Installers spend an estimated 1500 INR on customer acquisition.",
        ],
    }

    output = await agent.evaluate_candidate(candidate)

    # Verify all 10 core dimensions are interrogated
    assert len(output.reality_check) == 10
    dimensions = set(output.reality_check.keys())
    assert "real_customer_demand" in dimensions
    assert "evidence_customers_pay" in dimensions
    assert "realistic_price" in dimensions
    assert "supported_cac" in dimensions
    assert "margins_supported" in dimensions
    assert "competitor_activity" in dimensions
    assert "fatal_failure_risks" in dimensions
    assert "unknown_information" in dimensions

    # Verify status distinctions
    assert output.reality_check["real_customer_demand"].status in [
        RealityCheckStatus.VERIFIED,
        RealityCheckStatus.SUPPORTED_ESTIMATE,
    ]
    assert output.reality_check["unknown_information"].status == RealityCheckStatus.UNKNOWN

    # Verify failure modes ("Why this may fail") and contradicting evidence exist
    assert len(output.failure_modes) > 0
    assert len(output.contradicting_evidence) > 0
    assert len(output.unknowns) > 0


@pytest.mark.asyncio
async def test_unknown_information_is_never_converted_to_estimate():
    """
    Section 2 & 7 Rule:
    The agent must distinguish UNKNOWN and must NOT manufacture missing numbers
    or convert UNKNOWN into an estimate.
    """
    agent = RealityCheckAgent()
    candidate_with_missing_data = {
        "title": "Hypothetical Unproven Opportunity",
        "opportunity_family": "DIGITAL_PRODUCTS",
        "customer": "Unknown Buyers",
        "evidence": [],  # No evidence provided
        "customer_value": 0.0,  # Unknown price
        "cac": 0.0,
        "startup_cost": 5000.0,
        "estimated_margin": 0.0,
    }

    output = await agent.evaluate_candidate(candidate_with_missing_data)
    # Price without evidence must be classified as UNKNOWN rather than estimated
    assert output.reality_check["realistic_price"].status == RealityCheckStatus.UNKNOWN
    assert output.reality_check["evidence_customers_pay"].status == RealityCheckStatus.UNKNOWN


@pytest.mark.asyncio
async def test_reality_check_agent_run_execution():
    agent = RealityCheckAgent()
    run_record = await agent.run({
        "title": "B2B Waste Scrap Matchmaking",
        "target_market": "Workshops",
        "estimated_margin": 0.75,
    })

    assert run_record.final_status == "SUCCESS"
    assert "reality_check" in run_record.outputs
    assert "failure_modes" in run_record.outputs
    assert "adversarial_verdict" in run_record.outputs
