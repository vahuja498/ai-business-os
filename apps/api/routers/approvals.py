from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.api.services.audit_service import AuditService
from database.connection import get_db
from database.models.approval import Approval
from database.models.opportunity import Opportunity

router = APIRouter(prefix="/approvals", tags=["Approvals"])


class ApprovalActionPayload(BaseModel):
    actor: str = "HUMAN_OPERATOR"
    reason: str | None = None


@router.get("")
async def list_approvals(status: str | None = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Approval).order_by(Approval.created_at.desc())
    if status:
        stmt = stmt.where(Approval.status == status.upper())
    res = await db.execute(stmt)
    approvals = res.scalars().all()
    return [
        {
            "id": a.id,
            "business_id": a.business_id,
            "agent_id": a.agent_id,
            "task_id": a.task_id,
            "action_type": a.action_type,
            "description": a.description,
            "risk_level": a.risk_level,
            "amount": a.amount,
            "reason": a.reason,
            "evidence": a.evidence,
            "status": a.status,
            "requested_at": a.requested_at,
            "approved_at": a.approved_at,
            "approved_by": a.approved_by,
            "rejection_reason": a.rejection_reason,
        }
        for a in approvals
    ]


@router.get("/{approval_id}")
async def get_approval(approval_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Approval).where(Approval.id == approval_id)
    res = await db.execute(stmt)
    a = res.scalar_one_or_none()
    if not a:
        raise HTTPException(status_code=404, detail="Approval not found")
    return {
        "id": a.id,
        "business_id": a.business_id,
        "agent_id": a.agent_id,
        "task_id": a.task_id,
        "action_type": a.action_type,
        "description": a.description,
        "risk_level": a.risk_level,
        "amount": a.amount,
        "reason": a.reason,
        "evidence": a.evidence,
        "status": a.status,
        "requested_at": a.requested_at,
        "approved_at": a.approved_at,
        "approved_by": a.approved_by,
        "rejection_reason": a.rejection_reason,
    }


@router.post("/{approval_id}/approve")
async def approve_request(
    approval_id: str,
    payload: ApprovalActionPayload = ApprovalActionPayload(),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Approval).where(Approval.id == approval_id)
    res = await db.execute(stmt)
    approval = res.scalar_one_or_none()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")

    if approval.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail=f"Approval cannot be approved from current status '{approval.status}'",
        )

    approval.status = "APPROVED"
    approval.approved_at = datetime.now(timezone.utc)
    approval.approved_by = payload.actor

    # Update associated opportunity if any
    opp_stmt = (
        select(Opportunity)
        .where(Opportunity.business_id == approval.business_id)
        .order_by(Opportunity.created_at.desc())
    )
    opp_res = await db.execute(opp_stmt)
    opp = opp_res.scalars().first()
    if opp and opp.status == "PENDING_APPROVAL":
        opp.status = "APPROVED"

    await db.commit()
    await db.refresh(approval)

    await AuditService.record_event(
        db=db,
        actor=payload.actor,
        agent_id=approval.agent_id,
        business_id=approval.business_id,
        action="APPROVE_REQUEST",
        target=f"Approval:{approval.id}",
        result="APPROVED",
        approval_id=approval.id,
        metadata={
            "action_type": approval.action_type,
            "amount": approval.amount,
            "reason": payload.reason,
        },
    )

    return {
        "id": approval.id,
        "status": approval.status,
        "approved_by": approval.approved_by,
        "approved_at": approval.approved_at,
    }


@router.post("/{approval_id}/reject")
async def reject_request(
    approval_id: str,
    payload: ApprovalActionPayload = ApprovalActionPayload(),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Approval).where(Approval.id == approval_id)
    res = await db.execute(stmt)
    approval = res.scalar_one_or_none()
    if not approval:
        raise HTTPException(status_code=404, detail="Approval not found")

    if approval.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail=f"Approval cannot be rejected from current status '{approval.status}'",
        )

    approval.status = "REJECTED"
    approval.approved_at = datetime.now(timezone.utc)
    approval.approved_by = payload.actor
    approval.rejection_reason = payload.reason or "Rejected by human reviewer"

    # Update associated opportunity if any
    opp_stmt = (
        select(Opportunity)
        .where(Opportunity.business_id == approval.business_id)
        .order_by(Opportunity.created_at.desc())
    )
    opp_res = await db.execute(opp_stmt)
    opp = opp_res.scalars().first()
    if opp and opp.status == "PENDING_APPROVAL":
        opp.status = "REJECTED"

    await db.commit()
    await db.refresh(approval)

    await AuditService.record_event(
        db=db,
        actor=payload.actor,
        agent_id=approval.agent_id,
        business_id=approval.business_id,
        action="REJECT_REQUEST",
        target=f"Approval:{approval.id}",
        result="REJECTED",
        approval_id=approval.id,
        metadata={
            "action_type": approval.action_type,
            "amount": approval.amount,
            "rejection_reason": approval.rejection_reason,
        },
    )

    return {
        "id": approval.id,
        "status": approval.status,
        "rejection_reason": approval.rejection_reason,
        "approved_by": approval.approved_by,
        "approved_at": approval.approved_at,
    }
