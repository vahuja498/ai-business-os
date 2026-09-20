from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from agents.ceo.ceo_agent import CEOAgent
from agents.research.opportunity_engine import DEFAULT_RESEARCH_TEMPLATE
from apps.api.services.audit_service import AuditService
from apps.api.services.research_job_service import ResearchJobService
from database.connection import get_db
from database.models.approval import Approval
from database.models.opportunity import Opportunity

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


class OpportunityResearchRequest(BaseModel):
    objective: str = DEFAULT_RESEARCH_TEMPLATE
    budget_limit: float = 10000.0
    location_scope: str = "India"
    time_horizon: str = "30 days"
    automation_requirement: str = "HIGH"
    business_id: str | None = None


class ExperimentApprovalRequest(BaseModel):
    actor: str = "HUMAN_OPERATOR"
    notes: str | None = None


@router.post("/research")
async def trigger_opportunity_research(
    payload: OpportunityResearchRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    CEO delegates strategic market research to the OpportunityEngine (Section 9).
    Generates candidate opportunities, gathers web evidence, classifies findings,
    calculates multi-dimensional economics, and formulates low-cost validation experiments.
    """
    ceo = CEOAgent()
    try:
        opportunities = await ceo.delegate_opportunity_research(
            db=db,
            objective=payload.objective,
            business_id=payload.business_id,
        )
        return {
            "status": "COMPLETED",
            "objective": payload.objective,
            "count": len(opportunities),
            "opportunities": opportunities,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research execution failed: {str(e)}")


@router.post("/jobs/run")
async def run_manual_research_job(
    payload: OpportunityResearchRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Run on-demand research job (Section 11).
    """
    try:
        res = await ResearchJobService.run_research_job(
            db=db,
            objective=payload.objective,
            business_id=payload.business_id,
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{opportunity_id}/experiment/approve")
async def request_experiment_approval(
    opportunity_id: str,
    payload: ExperimentApprovalRequest = ExperimentApprovalRequest(),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a formal human approval record to greenlight the opportunity's validation experiment.
    """
    stmt = select(Opportunity).where(Opportunity.id == opportunity_id)
    res = await db.execute(stmt)
    opp = res.scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    experiment = opp.recommended_experiment or {}
    budget = experiment.get("budget", 0.0)

    approval = Approval(
        business_id=opp.business_id or "global",
        agent_id="OpportunityEngine",
        action_type="approve_validation_experiment",
        description=f"Approve low-cost experiment for '{opp.title}': {experiment.get('hypothesis')}",
        risk_level="MEDIUM" if budget == 0 else "HIGH",
        amount=budget,
        reason=f"Human authorization to begin low-cost validation (Hypothesis: {experiment.get('hypothesis')})",
        evidence=opp.evidence,
        status="PENDING",
    )
    db.add(approval)
    opp.status = "PENDING_APPROVAL"
    await db.commit()
    await db.refresh(approval)

    await AuditService.record_event(
        db=db,
        actor=payload.actor,
        business_id=opp.business_id,
        action="REQUEST_EXPERIMENT_APPROVAL",
        target=f"Opportunity:{opp.id}",
        result="PENDING",
        approval_id=approval.id,
        metadata={"budget": budget, "hypothesis": experiment.get("hypothesis")},
    )

    return {
        "approval_id": approval.id,
        "opportunity_id": opp.id,
        "status": approval.status,
        "amount": approval.amount,
        "risk_level": approval.risk_level,
    }


@router.get("")
async def list_opportunities(business_id: str | None = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Opportunity).order_by(Opportunity.created_at.desc())
    if business_id:
        stmt = stmt.where(Opportunity.business_id == business_id)
    result = await db.execute(stmt)
    opps = result.scalars().all()
    return [
        {
            "id": o.id,
            "business_id": o.business_id,
            "title": o.title,
            "description": o.description,
            "target_market": o.target_market,
            "revenue_model": o.revenue_model,
            "estimated_startup_cost": o.estimated_startup_cost,
            "estimated_customer_value": o.estimated_customer_value,
            "estimated_acquisition_cost": o.estimated_acquisition_cost,
            "estimated_fulfilment_cost": o.estimated_fulfilment_cost,
            "estimated_margin": o.estimated_margin,
            "automation_potential": o.automation_potential,
            "time_to_first_revenue": o.time_to_first_revenue,
            "regulatory_complexity": o.regulatory_complexity,
            "platform_dependency": o.platform_dependency,
            "uncertainty": o.uncertainty,
            "evidence_quality": o.evidence_quality,
            "risk_level": o.risk_level,
            "evidence": o.evidence,
            "findings": o.findings,
            "assumptions": o.assumptions,
            "unknowns": o.unknowns,
            "recommended_experiment": o.recommended_experiment,
            "status": o.status,
            "created_at": o.created_at,
        }
        for o in opps
    ]


@router.get("/{opportunity_id}")
async def get_opportunity(opportunity_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Opportunity).where(Opportunity.id == opportunity_id)
    res = await db.execute(stmt)
    opp = res.scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return {
        "id": opp.id,
        "business_id": opp.business_id,
        "title": opp.title,
        "description": opp.description,
        "target_market": opp.target_market,
        "revenue_model": opp.revenue_model,
        "estimated_startup_cost": opp.estimated_startup_cost,
        "estimated_customer_value": opp.estimated_customer_value,
        "estimated_acquisition_cost": opp.estimated_acquisition_cost,
        "estimated_fulfilment_cost": opp.estimated_fulfilment_cost,
        "estimated_margin": opp.estimated_margin,
        "automation_potential": opp.automation_potential,
        "time_to_first_revenue": opp.time_to_first_revenue,
        "regulatory_complexity": opp.regulatory_complexity,
        "platform_dependency": opp.platform_dependency,
        "uncertainty": opp.uncertainty,
        "evidence_quality": opp.evidence_quality,
        "risk_level": opp.risk_level,
        "evidence": opp.evidence,
        "findings": opp.findings,
        "assumptions": opp.assumptions,
        "unknowns": opp.unknowns,
        "recommended_experiment": opp.recommended_experiment,
        "status": opp.status,
        "created_at": opp.created_at,
    }
