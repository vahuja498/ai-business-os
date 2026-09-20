from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.models.audit_log import AuditLog
from database.models.opportunity import Opportunity
from database.models.validation import (
    Assumption,
    EvidenceUpdate,
    ExperimentResult,
    ValidationApproval,
    ValidationBudget,
    ValidationExperiment,
    ValidationPlan,
)
from agents.validation.engine import ValidationEngine
from agents.validation.integrity import ValidationIntegrityError

router = APIRouter(prefix="/validation", tags=["Validation Engine"])


# Request / Response Schemas
class RunExperimentRequest(BaseModel):
    outcome: str = Field(default="PASS", description="PASS, FAIL, or INCONCLUSIVE")
    metric_observed: str = Field(..., description="Observed quantitative outcome")
    cost_spent: float = Field(default=0.0, description="Cost spent in INR (must be <= experiment budget and <= 500)")
    evidence_artifacts: list[Any] = Field(default_factory=list, description="Evidence logs or artifacts")
    notes: str = Field(default="", description="Operational observations")
    is_simulation: bool = Field(default=True, description="Must remain True")
    update_assumption_to: str | None = Field(default=None, description="Optional target classification for linked assumption")
    justification: str = Field(default="", description="Mandatory justification if updating to VERIFIED")


class ApprovalDecisionRequest(BaseModel):
    action: str = Field(..., description="APPROVE or REJECT")
    decided_by: str = Field(default="HumanReviewer", description="Actor making the decision")
    rejection_reason: str | None = Field(default=None, description="Reason if rejected")


class CreateResultRequest(BaseModel):
    experiment_id: str
    outcome: str
    metric_observed: str
    cost_spent: float = 0.0
    evidence_artifacts: list[Any] = Field(default_factory=list)
    notes: str = ""
    is_simulation: bool = True
    update_assumption_to: str | None = None
    justification: str = ""


# -----------------------------------------------------------------------------
# 1. /validation (Plans List & Sync)
# -----------------------------------------------------------------------------
@router.get("")
async def list_validation_plans(
    status_filter: str | None = Query(None, alias="status"),
    family: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """List all validation plans with opportunity metadata, confidence scores, and budget metrics."""
    query = (
        select(ValidationPlan, Opportunity)
        .join(Opportunity, ValidationPlan.opportunity_id == Opportunity.id)
        .order_by(desc(ValidationPlan.confidence_score))
    )

    if status_filter:
        query = query.where(ValidationPlan.status == status_filter)
    if family and family != "ALL":
        query = query.where(Opportunity.opportunity_family == family)

    result = await db.execute(query)
    rows = result.all()

    plans_list = []
    for plan, opp in rows:
        plans_list.append({
            "id": plan.id,
            "opportunity_id": opp.id,
            "opportunity_title": opp.title,
            "opportunity_family": opp.opportunity_family,
            "customer": opp.customer,
            "status": plan.status,
            "confidence_score": plan.confidence_score,
            "total_budget_allocated": plan.total_budget_allocated,
            "total_budget_spent": plan.total_budget_spent,
            "material_assumptions_count": plan.material_assumptions_count,
            "high_risk_assumptions_count": plan.high_risk_assumptions_count,
            "completed_experiments_count": plan.completed_experiments_count,
            "regulatory_approval_required": plan.regulatory_approval_required,
            "created_at": plan.created_at.isoformat() if plan.created_at else None,
        })

    return plans_list


@router.post("/sync")
async def sync_validation_plans(db: AsyncSession = Depends(get_db)):
    """Convert or refresh validation plans for all 24 Phase 4 opportunities in the database."""
    try:
        sync_result = await ValidationEngine.sync_all_opportunities(db)
        return {"status": "SUCCESS", "message": "Validation plans synced successfully", "data": sync_result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync validation plans: {str(e)}",
        )


# -----------------------------------------------------------------------------
# 2. /validation/experiments & /validation/approvals & /validation/results
# (Defined before /{opportunity_id} to avoid path collision)
# -----------------------------------------------------------------------------
@router.get("/experiments")
async def list_validation_experiments(
    plan_id: str | None = Query(None),
    execution_status: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """List validation experiments across plans."""
    query = (
        select(ValidationExperiment, ValidationPlan, Opportunity)
        .join(ValidationPlan, ValidationExperiment.validation_plan_id == ValidationPlan.id)
        .join(Opportunity, ValidationPlan.opportunity_id == Opportunity.id)
        .order_by(ValidationExperiment.created_at.asc())
    )

    if plan_id:
        query = query.where(ValidationExperiment.validation_plan_id == plan_id)
    if execution_status:
        query = query.where(ValidationExperiment.execution_status == execution_status)

    result = await db.execute(query)
    rows = result.all()

    items = []
    for exp, plan, opp in rows:
        items.append({
            "id": exp.id,
            "validation_plan_id": exp.validation_plan_id,
            "opportunity_id": opp.id,
            "opportunity_title": opp.title,
            "opportunity_family": opp.opportunity_family,
            "assumption_id": exp.assumption_id,
            "title": exp.title,
            "hypothesis": exp.hypothesis,
            "methodology": exp.methodology,
            "pass_criteria": exp.pass_criteria,
            "fail_criteria": exp.fail_criteria,
            "inconclusive_criteria": exp.inconclusive_criteria,
            "budget": exp.budget,
            "duration_days": exp.duration_days,
            "required_evidence": exp.required_evidence,
            "automated_tasks": exp.automated_tasks,
            "human_tasks": exp.human_tasks,
            "regulatory_requirements": exp.regulatory_requirements,
            "approval_status": exp.approval_status,
            "execution_status": exp.execution_status,
            "is_simulation": exp.is_simulation,
            "created_at": exp.created_at.isoformat() if exp.created_at else None,
        })
    return items


@router.get("/experiments/{experiment_id}")
async def get_validation_experiment(
    experiment_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve detailed information on a single validation experiment."""
    stmt = (
        select(ValidationExperiment, ValidationPlan, Opportunity)
        .join(ValidationPlan, ValidationExperiment.validation_plan_id == ValidationPlan.id)
        .join(Opportunity, ValidationPlan.opportunity_id == Opportunity.id)
        .where(ValidationExperiment.id == experiment_id)
    )
    res = await db.execute(stmt)
    row = res.first()
    if not row:
        raise HTTPException(status_code=404, detail="Validation experiment not found")

    exp, plan, opp = row

    # Fetch results
    stmt_res = (
        select(ExperimentResult)
        .where(ExperimentResult.experiment_id == exp.id)
        .order_by(desc(ExperimentResult.executed_at))
    )
    results = (await db.execute(stmt_res)).scalars().all()

    # Fetch linked assumption
    linked_asm = None
    if exp.assumption_id:
        stmt_asm = select(Assumption).where(Assumption.id == exp.assumption_id)
        linked_asm = (await db.execute(stmt_asm)).scalar_one_or_none()

    return {
        "id": exp.id,
        "validation_plan_id": exp.validation_plan_id,
        "opportunity_id": opp.id,
        "opportunity_title": opp.title,
        "assumption": {
            "id": linked_asm.id,
            "category": linked_asm.category,
            "statement": linked_asm.statement,
            "classification": linked_asm.classification,
        } if linked_asm else None,
        "title": exp.title,
        "hypothesis": exp.hypothesis,
        "methodology": exp.methodology,
        "pass_criteria": exp.pass_criteria,
        "fail_criteria": exp.fail_criteria,
        "inconclusive_criteria": exp.inconclusive_criteria,
        "budget": exp.budget,
        "duration_days": exp.duration_days,
        "required_evidence": exp.required_evidence,
        "automated_tasks": exp.automated_tasks,
        "human_tasks": exp.human_tasks,
        "regulatory_requirements": exp.regulatory_requirements,
        "approval_status": exp.approval_status,
        "execution_status": exp.execution_status,
        "is_simulation": exp.is_simulation,
        "results": [
            {
                "id": r.id,
                "outcome": r.outcome,
                "metric_observed": r.metric_observed,
                "cost_spent": r.cost_spent,
                "notes": r.notes,
                "simulated": r.simulated,
                "executed_at": r.executed_at.isoformat() if r.executed_at else None,
            }
            for r in results
        ],
    }


@router.post("/experiments/{experiment_id}/run")
async def run_validation_experiment(
    experiment_id: str,
    req: RunExperimentRequest,
    db: AsyncSession = Depends(get_db),
):
    """Executes a simulated dry-run of a validation experiment and safely records results."""
    try:
        result = await ValidationEngine.record_experiment_result(
            session=db,
            experiment_id=experiment_id,
            outcome=req.outcome,
            metric_observed=req.metric_observed,
            cost_spent=req.cost_spent,
            evidence_artifacts=req.evidence_artifacts,
            notes=req.notes,
            is_simulation=req.is_simulation,
            update_assumption_to=req.update_assumption_to,
            justification=req.justification,
        )
        return {
            "status": "SUCCESS",
            "result_id": result.id,
            "outcome": result.outcome,
            "cost_spent": result.cost_spent,
            "simulated": result.simulated,
        }
    except ValidationIntegrityError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/approvals")
async def list_validation_approvals(
    status_filter: str | None = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
):
    """List validation approvals requiring human authorization."""
    query = (
        select(ValidationApproval, ValidationPlan, Opportunity)
        .join(ValidationPlan, ValidationApproval.validation_plan_id == ValidationPlan.id)
        .join(Opportunity, ValidationPlan.opportunity_id == Opportunity.id)
        .order_by(desc(ValidationApproval.created_at))
    )

    if status_filter:
        query = query.where(ValidationApproval.status == status_filter)

    result = await db.execute(query)
    rows = result.all()

    items = []
    for apprv, plan, opp in rows:
        items.append({
            "id": apprv.id,
            "validation_plan_id": apprv.validation_plan_id,
            "opportunity_id": opp.id,
            "opportunity_title": opp.title,
            "experiment_id": apprv.experiment_id,
            "approval_type": apprv.approval_type,
            "description": apprv.description,
            "risk_level": apprv.risk_level,
            "status": apprv.status,
            "requested_amount": apprv.requested_amount,
            "approved_by": apprv.approved_by,
            "approved_at": apprv.approved_at.isoformat() if apprv.approved_at else None,
            "rejection_reason": apprv.rejection_reason,
            "created_at": apprv.created_at.isoformat() if apprv.created_at else None,
        })
    return items


@router.post("/approvals/{approval_id}/decide")
async def decide_validation_approval(
    approval_id: str,
    req: ApprovalDecisionRequest,
    db: AsyncSession = Depends(get_db),
):
    """Approve or reject a validation approval gate."""
    stmt = select(ValidationApproval).where(ValidationApproval.id == approval_id)
    approval = (await db.execute(stmt)).scalar_one_or_none()
    if not approval:
        raise HTTPException(status_code=404, detail="Validation approval not found")

    decision = req.action.upper()
    if decision not in ("APPROVE", "REJECT"):
        raise HTTPException(status_code=400, detail="Action must be APPROVE or REJECT")

    from datetime import datetime, timezone

    if decision == "APPROVE":
        approval.status = "APPROVED"
        approval.approved_by = req.decided_by
        approval.approved_at = datetime.now(timezone.utc)

        # If plan-level approval, update plan status to IN_PROGRESS
        stmt_plan = select(ValidationPlan).where(ValidationPlan.id == approval.validation_plan_id)
        plan = (await db.execute(stmt_plan)).scalar_one_or_none()
        if plan and plan.status == "DRAFT":
            plan.status = "IN_PROGRESS"
    else:
        approval.status = "REJECTED"
        approval.rejection_reason = req.rejection_reason or "Declined by human reviewer"

    # Audit log
    audit = AuditLog(
        actor=req.decided_by,
        action=f"DECIDE_VALIDATION_APPROVAL_{decision}",
        target=approval.id,
        result="SUCCESS",
        metadata_json={
            "approval_id": approval.id,
            "decision": decision,
            "rejection_reason": approval.rejection_reason,
        },
    )
    db.add(audit)
    await db.commit()
    return {"status": "SUCCESS", "approval_id": approval.id, "decision": approval.status}


@router.get("/results")
async def list_validation_results(
    db: AsyncSession = Depends(get_db),
):
    """List historical experiment results and associated evidence updates."""
    stmt_res = (
        select(ExperimentResult, ValidationExperiment, ValidationPlan, Opportunity)
        .join(ValidationExperiment, ExperimentResult.experiment_id == ValidationExperiment.id)
        .join(ValidationPlan, ValidationExperiment.validation_plan_id == ValidationPlan.id)
        .join(Opportunity, ValidationPlan.opportunity_id == Opportunity.id)
        .order_by(desc(ExperimentResult.executed_at))
    )
    result = await db.execute(stmt_res)
    rows = result.all()

    results_list = []
    for res_item, exp, plan, opp in rows:
        results_list.append({
            "id": res_item.id,
            "experiment_id": exp.id,
            "experiment_title": exp.title,
            "opportunity_id": opp.id,
            "opportunity_title": opp.title,
            "outcome": res_item.outcome,
            "metric_observed": res_item.metric_observed,
            "evidence_artifacts": res_item.evidence_artifacts,
            "cost_spent": res_item.cost_spent,
            "notes": res_item.notes,
            "simulated": res_item.simulated,
            "executed_at": res_item.executed_at.isoformat() if res_item.executed_at else None,
        })
    return results_list


@router.post("/results")
async def submit_experiment_result(
    req: CreateResultRequest,
    db: AsyncSession = Depends(get_db),
):
    """Submit experiment execution result and enforce classification integrity rules."""
    try:
        res = await ValidationEngine.record_experiment_result(
            session=db,
            experiment_id=req.experiment_id,
            outcome=req.outcome,
            metric_observed=req.metric_observed,
            cost_spent=req.cost_spent,
            evidence_artifacts=req.evidence_artifacts,
            notes=req.notes,
            is_simulation=req.is_simulation,
            update_assumption_to=req.update_assumption_to,
            justification=req.justification,
        )
        return {
            "status": "SUCCESS",
            "result_id": res.id,
            "outcome": res.outcome,
            "cost_spent": res.cost_spent,
        }
    except ValidationIntegrityError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# -----------------------------------------------------------------------------
# 3. /validation/{opportunity_id} (Detailed Validation Plan)
# -----------------------------------------------------------------------------
@router.get("/{opportunity_id}")
async def get_validation_plan_by_opportunity(
    opportunity_id: str,
    db: AsyncSession = Depends(get_db),
):
    """Retrieve detailed validation plan for a specific opportunity."""
    # Find opportunity
    stmt_opp = select(Opportunity).where(Opportunity.id == opportunity_id)
    opp = (await db.execute(stmt_opp)).scalar_one_or_none()
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    # Find or auto-initialize validation plan
    stmt_plan = select(ValidationPlan).where(ValidationPlan.opportunity_id == opp.id)
    plan = (await db.execute(stmt_plan)).scalar_one_or_none()
    if not plan:
        plan = await ValidationEngine.create_or_update_validation_plan(db, opp)
        await db.commit()

    # Load Assumptions
    stmt_asm = (
        select(Assumption)
        .where(Assumption.validation_plan_id == plan.id)
        .order_by(desc(Assumption.is_highest_risk), Assumption.category.asc())
    )
    assumptions = (await db.execute(stmt_asm)).scalars().all()

    # Load Experiments
    stmt_exp = (
        select(ValidationExperiment)
        .where(ValidationExperiment.validation_plan_id == plan.id)
        .order_by(ValidationExperiment.created_at.asc())
    )
    experiments = (await db.execute(stmt_exp)).scalars().all()

    # Load Budget
    stmt_budget = select(ValidationBudget).where(ValidationBudget.validation_plan_id == plan.id)
    budget = (await db.execute(stmt_budget)).scalar_one_or_none()

    # Load Approvals
    stmt_apprv = (
        select(ValidationApproval)
        .where(ValidationApproval.validation_plan_id == plan.id)
        .order_by(desc(ValidationApproval.created_at))
    )
    approvals = (await db.execute(stmt_apprv)).scalars().all()

    # Load Audit logs for this plan or opportunity
    stmt_audit = (
        select(AuditLog)
        .where(
            (AuditLog.target == plan.id)
            | (AuditLog.target == opp.id)
        )
        .order_by(desc(AuditLog.created_at))
        .limit(20)
    )
    audits = (await db.execute(stmt_audit)).scalars().all()

    return {
        "id": plan.id,
        "opportunity": {
            "id": opp.id,
            "title": opp.title,
            "opportunity_family": opp.opportunity_family,
            "customer": opp.customer,
            "problem": opp.problem,
            "solution": opp.solution,
            "revenue_model": opp.revenue_model,
            "estimated_startup_cost": opp.estimated_startup_cost,
            "estimated_margin": opp.estimated_margin,
            "automation_potential": opp.automation_potential,
            "time_to_first_revenue": opp.time_to_first_revenue,
            "regulatory_complexity": opp.regulatory_complexity,
            "platform_dependency": opp.platform_dependency,
            "pursue_status": opp.pursue_status,
        },
        "plan": {
            "status": plan.status,
            "confidence_score": plan.confidence_score,
            "summary": plan.summary,
            "total_budget_allocated": plan.total_budget_allocated,
            "total_budget_spent": plan.total_budget_spent,
            "material_assumptions_count": plan.material_assumptions_count,
            "high_risk_assumptions_count": plan.high_risk_assumptions_count,
            "completed_experiments_count": plan.completed_experiments_count,
            "regulatory_approval_required": plan.regulatory_approval_required,
            "regulatory_approval_notes": plan.regulatory_approval_notes,
            "created_at": plan.created_at.isoformat() if plan.created_at else None,
        },
        "budget": {
            "max_budget": budget.max_budget if budget else 2500.0,
            "allocated_amount": budget.allocated_amount if budget else 0.0,
            "spent_amount": budget.spent_amount if budget else 0.0,
            "currency": budget.currency if budget else "INR",
            "is_locked": budget.is_locked if budget else False,
        } if budget else None,
        "assumptions": [
            {
                "id": a.id,
                "category": a.category,
                "statement": a.statement,
                "classification": a.classification,
                "risk_level": a.risk_level,
                "is_highest_risk": a.is_highest_risk,
                "evidence_notes": a.evidence_notes,
                "initial_classification": a.initial_classification,
            }
            for a in assumptions
        ],
        "experiments": [
            {
                "id": e.id,
                "assumption_id": e.assumption_id,
                "title": e.title,
                "hypothesis": e.hypothesis,
                "methodology": e.methodology,
                "pass_criteria": e.pass_criteria,
                "fail_criteria": e.fail_criteria,
                "inconclusive_criteria": e.inconclusive_criteria,
                "budget": e.budget,
                "duration_days": e.duration_days,
                "required_evidence": e.required_evidence,
                "automated_tasks": e.automated_tasks,
                "human_tasks": e.human_tasks,
                "regulatory_requirements": e.regulatory_requirements,
                "approval_status": e.approval_status,
                "execution_status": e.execution_status,
                "is_simulation": e.is_simulation,
            }
            for e in experiments
        ],
        "approvals": [
            {
                "id": ap.id,
                "approval_type": ap.approval_type,
                "description": ap.description,
                "risk_level": ap.risk_level,
                "status": ap.status,
                "requested_amount": ap.requested_amount,
                "approved_by": ap.approved_by,
                "approved_at": ap.approved_at.isoformat() if ap.approved_at else None,
            }
            for ap in approvals
        ],
        "audit_trail": [
            {
                "id": au.id,
                "actor": au.actor,
                "action": au.action,
                "target": au.target,
                "result": au.result,
                "details": au.metadata_json,
                "timestamp": au.created_at.isoformat() if au.created_at else None,
            }
            for au in audits
        ],
    }
