from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.api.config import settings
from database.connection import get_db
from database.models.agent import AgentRun
from database.models.approval import Approval
from database.models.business import Business
from database.models.opportunity import Opportunity

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary")
async def get_dashboard_summary(db: AsyncSession = Depends(get_db)):
    # 1. Active businesses count
    active_biz_count = (
        await db.execute(select(func.count(Business.id)).where(Business.status.in_(["ACTIVE", "DRAFT"])))
    ).scalar() or 0

    # 2. Open opportunities count
    open_opps_count = (
        await db.execute(
            select(func.count(Opportunity.id)).where(Opportunity.status.in_(["IDENTIFIED", "PENDING_APPROVAL", "APPROVED"]))
        )
    ).scalar() or 0

    # 3. Pending approvals count
    pending_approvals_count = (
        await db.execute(select(func.count(Approval.id)).where(Approval.status == "PENDING"))
    ).scalar() or 0

    # 4. Recent agent runs
    runs_res = await db.execute(select(AgentRun).order_by(AgentRun.started_at.desc()).limit(5))
    recent_runs = runs_res.scalars().all()

    # 5. Pending approvals list
    approvals_res = await db.execute(
        select(Approval).where(Approval.status == "PENDING").order_by(Approval.requested_at.desc()).limit(5)
    )
    pending_approvals = approvals_res.scalars().all()

    # 6. Opportunities list
    opps_res = await db.execute(select(Opportunity).order_by(Opportunity.created_at.desc()).limit(5))
    opportunities = opps_res.scalars().all()

    return {
        "metrics": {
            "active_businesses": active_biz_count,
            "open_opportunities": open_opps_count,
            "pending_approvals": pending_approvals_count,
            "simulated_revenue": 0.0,
            "simulated_expenses": 0.0,
            "system_health": "OPTIMAL",
        },
        "guardrails": {
            "max_daily_spend": settings.MAX_DAILY_SPEND,
            "max_transaction_amount": settings.MAX_TRANSACTION_AMOUNT,
            "max_monthly_spend": settings.MAX_MONTHLY_SPEND,
            "min_margin": settings.MIN_MARGIN,
        },
        "recent_runs": [
            {
                "id": r.id,
                "agent_id": r.agent_id,
                "final_status": r.final_status,
                "started_at": r.started_at,
                "completed_at": r.completed_at,
            }
            for r in recent_runs
        ],
        "pending_approvals": [
            {
                "id": a.id,
                "business_id": a.business_id,
                "action_type": a.action_type,
                "description": a.description,
                "risk_level": a.risk_level,
                "amount": a.amount,
                "requested_at": a.requested_at,
            }
            for a in pending_approvals
        ],
        "recent_opportunities": [
            {
                "id": o.id,
                "title": o.title,
                "margin": o.estimated_margin,
                "risk_level": o.risk_level,
                "status": o.status,
            }
            for o in opportunities
        ],
    }
