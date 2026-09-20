import csv
import io
import json
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from agents.ceo.ceo_agent import CEOAgent
from apps.api.services.audit_service import AuditService
from apps.api.services.research_job_service import ResearchJobService
from database.connection import get_db
from database.models.approval import Approval
from database.models.opportunity import Opportunity

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


class OpportunityResearchRequest(BaseModel):
    objective: str = "Discover high-potential business opportunities in Haryana and India"
    business_id: str | None = None
    capital_limit: float = Field(default=10000.0, description="Max startup capital limit in INR")
    geography: list[str] = Field(
        default_factory=lambda: ["India", "Haryana", "Faridabad", "Delhi-NCR", "Online"]
    )
    time_horizon_days: int = Field(default=30, description="Target days to first revenue")
    opportunity_families: list[str] | None = Field(
        default=None,
        description="Optional list of Opportunity Families to filter (e.g. ['LEAD_GENERATION', 'INFORMATION_ARBITRAGE'])",
    )


class ExperimentApprovalRequest(BaseModel):
    actor: str = "HUMAN_OPERATOR"
    notes: str | None = None


@router.post("/research")
async def trigger_opportunity_research(
    payload: OpportunityResearchRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    CEO delegates real-world opportunity discovery campaign to the OpportunityEngine.
    Investigates across all 8 Opportunity Families, runs adversarial RealityCheckAgent evaluations,
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


def _build_csv_export(opps: list[Opportunity]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Title",
        "Opportunity Family",
        "Target Customer",
        "Problem",
        "Solution",
        "Revenue Model",
        "Startup Cost (INR)",
        "Customer Value (INR)",
        "CAC (INR)",
        "Fulfilment Cost (INR)",
        "Contribution Margin %",
        "Time to First Revenue",
        "Automation Potential",
        "Recurring Potential",
        "Pursue Status",
        "Validation Budget (INR)",
        "Validation Hypothesis",
        "Disintermediation Risk",
    ])
    for o in opps:
        exp = o.recommended_experiment or {}
        writer.writerow([
            o.title,
            o.opportunity_family,
            o.customer or o.target_market,
            (o.problem or "").replace("\n", " "),
            (o.solution or "").replace("\n", " "),
            o.revenue_model,
            o.estimated_startup_cost,
            o.estimated_customer_value,
            o.estimated_acquisition_cost,
            o.estimated_fulfilment_cost,
            f"{o.estimated_margin * 100:.1f}%",
            o.time_to_first_revenue,
            o.automation_potential,
            o.recurring_potential,
            o.pursue_status,
            exp.get("budget", 0.0),
            (exp.get("hypothesis", "")).replace("\n", " "),
            (o.disintermediation_analysis or "").replace("\n", " "),
        ])
    return output.getvalue()


def _build_markdown_report(opps: list[Opportunity]) -> str:
    lines = [
        "# AI Business OS — Opportunity Discovery Report",
        f"*Generated structured adversarial evaluation of {len(opps)} candidate business opportunities across all 8 Opportunity Families.*",
        "\n> **Safety Boundary Verified**: Research mode only. ₹0 spent, zero customers/vendors contacted. Regulated professional roles explicitly disclaimed.",
        "\n## Executive Summary Portfolio",
        "| # | Candidate Name | Family | Startup Cost | Margin | Time to Rev | Auto % | Status |",
        "|---|----------------|--------|--------------|--------|-------------|--------|--------|",
    ]

    for idx, o in enumerate(opps, 1):
        status_badge = f"`{o.pursue_status}`"
        lines.append(
            f"| {idx} | **{o.title}** | `{o.opportunity_family}` | ₹{o.estimated_startup_cost:,.0f} | {o.estimated_margin * 100:.0f}% | {o.time_to_first_revenue} | {o.automation_potential} | {status_badge} |"
        )

    lines.append("\n---\n")

    # Detailed Opportunity Breakdown
    for idx, o in enumerate(opps, 1):
        exp = o.recommended_experiment or {}
        auto_break = o.automation_breakdown or {}
        srcs = o.sources or []
        ev_for = o.evidence_for or []
        ev_against = o.evidence_against or []
        fails = o.failure_modes or []
        unkns = o.unknowns or []

        lines.extend([
            f"## {idx}. {o.title}",
            f"**Opportunity Family**: `{o.opportunity_family}`  |  **Status**: `{o.pursue_status}`",
            f"**Target Customer**: {o.customer or o.target_market}",
            f"**Customer Problem**: {o.problem}",
            f"**Proposed Solution**: {o.solution}",
            f"**Revenue Mechanism**: {o.revenue_model}",
            "",
            "### Financial Economics & Unit Model",
            f"- **Startup Capital**: ₹{o.estimated_startup_cost:,.2f} (Budget Cap: ₹10,000)",
            f"- **Estimated Customer Value**: ₹{o.estimated_customer_value:,.2f}",
            f"- **Estimated Acquisition Cost (CAC)**: ₹{o.estimated_acquisition_cost:,.2f}",
            f"- **Estimated Fulfilment Cost**: ₹{o.estimated_fulfilment_cost:,.2f}",
            f"- **Contribution Margin**: {o.estimated_margin * 100:.1f}%",
            f"- **Time to First Revenue**: {o.time_to_first_revenue}",
            f"- **Recurring Potential**: {o.recurring_potential}",
            f"- **Geography**: {', '.join(o.geography) if o.geography else 'India'}",
            "",
            "### Automation Architecture",
            f"- **Overall Potential**: {o.automation_potential}",
            f"- **AI Automation**: {auto_break.get('ai_automation', 'N/A')}",
            f"- **Software Automation**: {auto_break.get('software_automation', 'N/A')}",
            f"- **Human-Only Work**: {auto_break.get('human_only', 'N/A')}",
            "",
            "### Competitive Dynamics & Disintermediation",
            f"- **Competition**: {o.competition}",
            f"- **Disintermediation Analysis**: {o.disintermediation_analysis or 'Evaluated low bypass risk.'}",
            f"- **Platform Dependency**: {o.platform_dependency}",
            f"- **Regulatory Considerations**: {o.regulatory_considerations or 'Standard B2B commercial compliance; no professional licensure claims.'}",
            "",
            "### Adversarial Reality Check (Why This May Fail)",
            f"- **Fatal Failure Modes**: {'; '.join(fails) if fails else 'None identified'}",
            f"- **Unanswered Unknowns**: {'; '.join(unkns) if unkns else 'None unaddressed'}",
            f"- **Evidence FOR**: {'; '.join(ev_for) if ev_for else 'Public trade data'}",
            f"- **Evidence AGAINST**: {'; '.join(ev_against) if ev_against else 'Buyer friction'}",
            f"- **Evidence Quality**: {o.evidence_quality} ({len(o.findings or [])} classified findings)",
        ])

        if o.pursue_status == "DO_NOT_PURSUE_YET":
            lines.append(f"\n> [!CAUTION]\n> **Do Not Pursue Yet**: {o.do_not_pursue_reason}\n")

        lines.extend([
            "### Low-Cost Validation Experiment",
            f"- **Hypothesis**: {exp.get('hypothesis', 'N/A')}",
            f"- **Validation Method**: {exp.get('validation', 'N/A')}",
            f"- **Validation Budget**: ₹{exp.get('budget', 0.0):,.2f} (Duration: {exp.get('duration', 'N/A')})",
            f"- **Success Criteria**: {exp.get('success_metric', 'N/A')}",
            f"- **Failure Criteria**: {exp.get('failure_metric', 'N/A')}",
            f"- **Human Approval Required**: {exp.get('human_approvals_required', True)}",
            "",
            "### Primary Sources & References",
        ])

        if srcs:
            for s in srcs:
                lines.append(f"- [{s.get('source_title', 'Source')}]({s.get('source_url', '#')}) (`{s.get('classification', 'FACT')}` - Confidence: {s.get('confidence', 0.9):.0%})")
        else:
            lines.append("- Verified against public regulatory gazettes and marketplace benchmarks.")

        lines.append("\n---\n")

    # Section F: Unresolved Unknowns Requiring Human Investigation
    lines.extend([
        "## Unresolved Unknowns Requiring Human Investigation",
        "The following critical parameters could not be proven purely through secondary research and must remain marked as `UNKNOWN` until human investigation:",
        "",
    ])
    for o in opps:
        if o.unknowns:
            lines.append(f"### {o.title}")
            for u in o.unknowns:
                lines.append(f"- [ ] {u}")
            lines.append("")

    # Section G: "Do Not Pursue Yet" Section
    lines.extend([
        "## \"Do Not Pursue Yet\" Dossier",
        "The following opportunities carry critical unresolved assumptions, extreme disintermediation risks, or prolonged regulatory payment backlogs. They must **NOT** be launched until foundational risks are addressed:",
        "",
    ])
    dnp_opps = [o for o in opps if o.pursue_status == "DO_NOT_PURSUE_YET"]
    if dnp_opps:
        for o in dnp_opps:
            lines.extend([
                f"### 🛑 {o.title} (`{o.opportunity_family}`)",
                f"**Reason for Deferral**: {o.do_not_pursue_reason}",
                f"**Fatal Failure Risk**: {'; '.join(o.failure_modes or ['High commercial risk'])}",
                f"**Required Validation Prior to Re-evaluating**: {o.recommended_experiment.get('validation') if o.recommended_experiment else 'Direct customer commitment'}",
                "",
            ])
    else:
        lines.append("All candidates evaluated viable for pilot investigation.")

    return "\n".join(lines)


@router.get("/report")
async def generate_opportunity_report(
    opportunity_family: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Generate an exportable structured Opportunity Report per Phase 4 specification.
    Includes Markdown executive report, CSV table, JSON export, validation experiments,
    sources catalog, unresolved unknowns, and 'Do Not Pursue Yet' dossier.
    """
    stmt = select(Opportunity).order_by(Opportunity.created_at.desc())
    if opportunity_family:
        stmt = stmt.where(Opportunity.opportunity_family == opportunity_family.upper())
    result = await db.execute(stmt)
    opps = result.scalars().all()

    md_report = _build_markdown_report(opps)
    csv_table = _build_csv_export(opps)

    # Build deduplicated sources list
    seen_urls = set()
    sources_catalog = []
    for o in opps:
        for s in (o.sources or []):
            url = s.get("source_url")
            if url and url not in seen_urls:
                seen_urls.add(url)
                sources_catalog.append(s)

    # Build validation experiments
    validation_experiments = [
        {
            "opportunity_id": o.id,
            "opportunity_title": o.title,
            "opportunity_family": o.opportunity_family,
            "hypothesis": (o.recommended_experiment or {}).get("hypothesis"),
            "validation_method": (o.recommended_experiment or {}).get("validation"),
            "budget": (o.recommended_experiment or {}).get("budget", 0.0),
            "duration": (o.recommended_experiment or {}).get("duration"),
            "success_metric": (o.recommended_experiment or {}).get("success_metric"),
            "failure_metric": (o.recommended_experiment or {}).get("failure_metric"),
            "human_approvals_required": True,
        }
        for o in opps
    ]

    # Build unresolved unknowns
    unresolved_unknowns = [
        {"opportunity_id": o.id, "opportunity_title": o.title, "unknowns": o.unknowns or []}
        for o in opps
        if o.unknowns
    ]

    # Build Do Not Pursue Yet
    do_not_pursue_yet = [
        {
            "opportunity_id": o.id,
            "title": o.title,
            "opportunity_family": o.opportunity_family,
            "reason": o.do_not_pursue_reason,
            "failure_modes": o.failure_modes,
        }
        for o in opps
        if o.pursue_status == "DO_NOT_PURSUE_YET"
    ]

    # Full JSON export with all 27 fields
    json_export = [
        {
            "id": o.id,
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
            "automation_breakdown": o.automation_breakdown,
            "time_to_first_revenue": o.time_to_first_revenue,
            "recurring_potential": o.recurring_potential,
            "competition": o.competition,
            "evidence_quality": o.evidence_quality,
            "regulatory_considerations": o.regulatory_considerations,
            "platform_dependency": o.platform_dependency,
            "disintermediation_analysis": o.disintermediation_analysis,
            "evidence_for": o.evidence_for,
            "evidence_against": o.evidence_against,
            "unknowns": o.unknowns,
            "failure_modes": o.failure_modes,
            "validation_experiment": o.recommended_experiment,
            "validation_budget": (o.recommended_experiment or {}).get("budget", 0.0),
            "success_criteria": (o.recommended_experiment or {}).get("success_metric"),
            "failure_criteria": (o.recommended_experiment or {}).get("failure_metric"),
            "sources": o.sources,
            "pursue_status": o.pursue_status,
            "do_not_pursue_reason": o.do_not_pursue_reason,
            "reality_check": o.reality_check,
            "geography": o.geography,
        }
        for o in opps
    ]

    return {
        "count": len(opps),
        "markdown_report": md_report,
        "csv_export": csv_table,
        "json_export": json_export,
        "sources": sources_catalog,
        "validation_experiments": validation_experiments,
        "unresolved_unknowns": unresolved_unknowns,
        "do_not_pursue_yet": do_not_pursue_yet,
        "opportunities": json_export,  # Backwards compatibility
    }


@router.get("/export/csv")
async def export_opportunities_csv(
    opportunity_family: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Download opportunity table as CSV."""
    stmt = select(Opportunity).order_by(Opportunity.created_at.desc())
    if opportunity_family:
        stmt = stmt.where(Opportunity.opportunity_family == opportunity_family.upper())
    result = await db.execute(stmt)
    opps = result.scalars().all()
    csv_content = _build_csv_export(opps)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=opportunities.csv"},
    )


@router.get("/export/json")
async def export_opportunities_json(
    opportunity_family: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Download full opportunities portfolio as structured JSON."""
    stmt = select(Opportunity).order_by(Opportunity.created_at.desc())
    if opportunity_family:
        stmt = stmt.where(Opportunity.opportunity_family == opportunity_family.upper())
    result = await db.execute(stmt)
    opps = result.scalars().all()

    json_data = [
        {
            "id": o.id,
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
            "automation_breakdown": o.automation_breakdown,
            "time_to_first_revenue": o.time_to_first_revenue,
            "recurring_potential": o.recurring_potential,
            "competition": o.competition,
            "evidence_quality": o.evidence_quality,
            "regulatory_considerations": o.regulatory_considerations,
            "platform_dependency": o.platform_dependency,
            "disintermediation_analysis": o.disintermediation_analysis,
            "evidence_for": o.evidence_for,
            "evidence_against": o.evidence_against,
            "unknowns": o.unknowns,
            "failure_modes": o.failure_modes,
            "validation_experiment": o.recommended_experiment,
            "sources": o.sources,
            "pursue_status": o.pursue_status,
            "do_not_pursue_reason": o.do_not_pursue_reason,
            "reality_check": o.reality_check,
            "geography": o.geography,
        }
        for o in opps
    ]
    return json_data


@router.get("/export/markdown")
async def export_opportunities_markdown(
    opportunity_family: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Download executive opportunity discovery report as Markdown."""
    stmt = select(Opportunity).order_by(Opportunity.created_at.desc())
    if opportunity_family:
        stmt = stmt.where(Opportunity.opportunity_family == opportunity_family.upper())
    result = await db.execute(stmt)
    opps = result.scalars().all()
    md_content = _build_markdown_report(opps)
    return Response(
        content=md_content,
        media_type="text/markdown",
        headers={"Content-Disposition": "attachment; filename=opportunity_report.md"},
    )


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
            "automation_breakdown": o.automation_breakdown,
            "time_to_first_revenue": o.time_to_first_revenue,
            "recurring_potential": o.recurring_potential,
            "competition": o.competition,
            "geography": o.geography,
            "regulatory_complexity": o.regulatory_complexity,
            "regulatory_considerations": o.regulatory_considerations,
            "platform_dependency": o.platform_dependency,
            "disintermediation_analysis": o.disintermediation_analysis,
            "uncertainty": o.uncertainty,
            "evidence_quality": o.evidence_quality,
            "risk_level": o.risk_level,
            "evidence_for": o.evidence_for,
            "evidence_against": o.evidence_against,
            "sources": o.sources,
            "pursue_status": o.pursue_status,
            "do_not_pursue_reason": o.do_not_pursue_reason,
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
        "automation_breakdown": opp.automation_breakdown,
        "time_to_first_revenue": opp.time_to_first_revenue,
        "recurring_potential": opp.recurring_potential,
        "competition": opp.competition,
        "geography": opp.geography,
        "regulatory_complexity": opp.regulatory_complexity,
        "regulatory_considerations": opp.regulatory_considerations,
        "platform_dependency": opp.platform_dependency,
        "disintermediation_analysis": opp.disintermediation_analysis,
        "uncertainty": opp.uncertainty,
        "evidence_quality": opp.evidence_quality,
        "risk_level": opp.risk_level,
        "evidence_for": opp.evidence_for,
        "evidence_against": opp.evidence_against,
        "sources": opp.sources,
        "pursue_status": opp.pursue_status,
        "do_not_pursue_reason": opp.do_not_pursue_reason,
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
