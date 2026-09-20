import pytest
from agents.ceo.ceo_agent import CEOAgent
from agents.research.research_agent import ResearchAgent
from agents.risk.risk_agent import RiskAgent


@pytest.mark.asyncio
async def test_research_agent_opportunity_synthesis():
    agent = ResearchAgent()
    run_record = await agent.run(input_data={"objective": "solar leads discovery"})

    assert run_record.final_status == "SUCCESS"
    assert "opportunity" in run_record.outputs

    opp = run_record.outputs["opportunity"]
    assert opp["title"].startswith("Opportunity:")
    assert opp["estimated_margin"] > 0.20
    assert opp["status"] == "IDENTIFIED"

    # Verify classified evidence types
    evidence = opp["evidence"]
    assert len(evidence) > 0
    evidence_types = {e["type"] for e in evidence}
    assert any(t in evidence_types for t in ["FACT", "CLAIM", "ESTIMATE"])

    # Verify assumptions exist
    assert len(opp["assumptions"]) > 0


@pytest.mark.asyncio
async def test_risk_agent_approval_gating():
    agent = RiskAgent()
    # High risk action with amount
    run_record = await agent.run(
        input_data={
            "action_type": "launch_experiment",
            "description": "Allocate budget for ad campaign",
            "amount": 500.0,
        }
    )

    assert run_record.final_status == "SUCCESS"
    assert run_record.outputs["requires_human_approval"] is True
    assert len(run_record.approval_requests) == 1
    req = run_record.approval_requests[0]
    assert req["amount"] == 500.0
    assert req["status"] == "PENDING"


@pytest.mark.asyncio
async def test_risk_agent_blocks_prohibited_action():
    agent = RiskAgent()
    run_record = await agent.run(
        input_data={
            "action_type": "customer_acquisition",
            "description": "Create fake account to scrape vendor contact info",
        }
    )

    assert run_record.final_status == "FAILED"
    assert any("Blocked action" in err for err in run_record.errors)


@pytest.mark.asyncio
async def test_ceo_agent_decomposition_and_risk_gating():
    ceo = CEOAgent()
    run_record = await ceo.run(input_data={"objective": "Launch rooftop solar lead gen test"})

    assert run_record.final_status == "PENDING_APPROVAL"
    tasks = run_record.outputs["tasks"]
    assert len(tasks) == 2
    assert tasks[0]["assigned_agent"] == "ResearchAgent"
    assert tasks[1]["assigned_agent"] == "RiskAgent"

    # Risk gate should have generated an approval request
    assert len(run_record.approval_requests) == 1
    assert run_record.outputs["opportunity"]["status"] == "PENDING_APPROVAL"
