from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query
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
    capital_limit: float = 10000.0
    geography: list[str] = Field(default_factory=lambda: ["India", "Haryana", "Faridabad", "Online"])
    time_horizon_days: int = 30
    opportunity_families: list[str] | None = None
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
    CEO delegates real-world opportunity discovery campaign to the OpportunityEngine (Sections 4, 9, 12).
    Investigates across the 8 Opportunity Families, runs adversarial RealityCheckAgent evaluations,
    and returns structured opportunities without launching any autonomous real-world actions.
    """
    ceo = CEOAgent()
    try:
        from agents.research.opportunity_engine import OpportunityEngine
        engine = OpportunityEngine(model_provider=ceo.model_provider)
        opportunities = await engine.execute_research(
            db=db,
            objective=payload.objective,
            business_id=payload.business_id,
            capital_limit=payload.capital_limit,
            geographies=payload.geography,
            opportunity_families=payload.opportunity_families,
        )
        return {
            "status": "COMPLETED",
            "objective": payload.objective,
            "capital_limit": payload.capital_limit,
            "geography": payload.geography,
            "count": len(opportunities),
            "opportunities": opportunities,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research campaign failed: {str(e)}")


@router.get("/report")
async def generate_opportunity_report(
    opportunity_family: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Generate an exportable structured Opportunity Report per Section 10 specification.
    Includes full economics, failure modes, counter-evidence, and validation experiments.
    """
    stmt = select(Opportunity).order_by(Opportunity.created_at.desc())
    if opportunity_family:
        stmt = stmt.where(Opportunity.opportunity_family == opportunity_family.upper())
    result = await db.execute(stmt)
    opps = result.scalars().all()

    # Build markdown report
    md_lines = [
        "# AI Business OS — Opportunity Discovery Report",
        f"*Generated structured evaluation of {len(opps)} candidate business opportunities.*\n",
        "---",
    ]

    for o in opps:
        exp = o.recommended_experiment or {}
        md_lines.extend([
            f"## {o.title}",
            f"**Opportunity Family**: `{o.opportunity_family}`",
            f"**Target Customer**: {o.customer or o.target_market}",
            f"**Customer Problem**: {o.problem}",
            f"**Proposed Solution**: {o.solution}",
            f"**Revenue Model**: {o.revenue_model}",
            "",
            "### Financial Economics & Viability",
            f"- **Startup Cost**: ₹{o.estimated_startup_cost:,.2f}",
            f"- **Estimated Customer Value**: ₹{o.estimated_customer_value:,.2f}",
            f"- **Estimated CAC**: ₹{o.estimated_acquisition_cost:,.2f}",
            f"- **Estimated Fulfilment Cost**: ₹{o.estimated_fulfilment_cost:,.2f}",
            f"- **Contribution Margin**: {o.estimated_margin * 100:.1f}%",
            f"- **Automation Potential**: {o.automation_potential}",
            f"- **Time to First Revenue**: {o.time_to_first_revenue}",
            f"- **Recurring Revenue Potential**: {o.recurring_potential}",
            f"- **Competition**: {o.competition}",
            f"- **Geography**: {', '.join(o.geography) if o.geography else 'India'}",
            f"- **Evidence Quality**: {o.evidence_quality} ({len(o.evidence or [])} sources)",
            "",
            "### Adversarial Reality Check (Why This May Fail)",
            f"- **Fatal Failure Modes**: {', '.join(o.failure_modes or ['None specified'])}",
            f"- **Unanswered Unknowns**: {', '.join(o.unknowns or ['None specified'])}",
            f"- **Contradicting Evidence**: {', '.join([c.get('claim', str(c)) for c in (o.contradicting_evidence or [])]) or 'None found'}",
            f"- **Regulatory Considerations**: {o.regulatory_complexity} complexity",
            "",
            "### Low-Cost Validation Experiment",
            f"- **Hypothesis**: {exp.get('hypothesis', 'N/A')}",
            f"- **Validation Method**: {exp.get('validation', 'N/A')}",
            f"- **Validation Budget**: ₹{exp.get('budget', 0.0):,.2f} (Duration: {exp.get('duration', 'N/A')})",
            f"- **Success Criteria**: {exp.get('success_metric', 'N/A')}",
            f"- **Failure Criteria**: {exp.get('failure_metric', 'N/A')}",
            "\n---\n",
        ])

    return {
        "count": len(opps),
        "markdown_report": "\n".join(md_lines),
        "opportunities": [
            {
                "title": o.title,
                "opportunity_family": o.opportunity_family,
                "customer": o.customer,
                "problem": o.problem,
                "solution": o.solution,
                "revenue_model": o.revenue_model,
                "startup_cost": o.estimated_startup_cost,
                "customer_value": o.estimated_customer_value,
                "acquisition_cost": o.estimated_acquisition_cost,
                "fulfilment_cost": o.estimated_fulfilment_cost,
                "contribution_estimate": o.estimated_margin,
                "automation_potential": o.automation_potential,
                "time_to_first_revenue": o.time_to_first_revenue,
                "recurring_potential": o.recurring_potential,
                "competition": o.competition,
                "evidence_quality": o.evidence_quality,
                "unknowns": o.unknowns,
                "contradicting_evidence": o.contradicting_evidence,
                "failure_modes": o.failure_modes,
                "regulatory_considerations": o.regulatory_complexity,
                "validation_experiment": o.recommended_experiment,
            }
            for o in opps
        ],
    }


@router.post("/jobs/run")
async def run_manual_research_job(
    payload: OpportunityResearchRequest,
    db: AsyncSession = Depends(get_db),
):
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
async def list_opportunities(
    business_id: str | None = None,
    opportunity_family: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Opportunity).order_by(Opportunity.created_at.desc())
    if business_id:
        stmt = stmt.where(Opportunity.business_id == business_id)
    if opportunity_family:
        stmt = stmt.where(Opportunity.opportunity_family == opportunity_family.upper())
    result = await db.execute(stmt)
    opps = result.scalars().all()
    return [
        {
            "id": o.id,
            "business_id": o.business_id,
            "title": o.title,
            "opportunity_family": o.opportunity_family,
            "customer": o.customer,
            "problem": o.problem,
            "solution": o.solution,
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
            "recurring_potential": o.recurring_potential,
            "competition": o.competition,
            "geography": o.geography,
            "regulatory_complexity": o.regulatory_complexity,
            "platform_dependency": o.platform_dependency,
            "uncertainty": o.uncertainty,
            "evidence_quality": o.evidence_quality,
            "risk_level": o.risk_level,
            "evidence": o.evidence,
            "findings": o.findings,
            "assumptions": o.assumptions,
            "unknowns": o.unknowns,
            "failure_modes": o.failure_modes,
            "contradicting_evidence": o.contradicting_evidence,
            "reality_check": o.reality_check,
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
        "opportunity_family": opp.opportunity_family,
        "customer": opp.customer,
        "problem": opp.problem,
        "solution": opp.solution,
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
        "recurring_potential": opp.recurring_potential,
        "competition": opp.competition,
        "geography": opp.geography,
        "regulatory_complexity": opp.regulatory_complexity,
        "platform_dependency": opp.platform_dependency,
        "uncertainty": opp.uncertainty,
        "evidence_quality": opp.evidence_quality,
        "risk_level": opp.risk_level,
        "evidence": opp.evidence,
        "findings": opp.findings,
        "assumptions": opp.assumptions,
        "unknowns": opp.unknowns,
        "failure_modes": opp.failure_modes,
        "contradicting_evidence": opp.contradicting_evidence,
        "reality_check": opp.reality_check,
        "recommended_experiment": opp.recommended_experiment,
        "status": opp.status,
        "created_at": opp.created_at,
    }
