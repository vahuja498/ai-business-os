from fastapi import APIRouter, Depends
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.models.agent import AgentRun
from database.models.approval import Approval
from database.models.business import Business

router = APIRouter(tags=["Health & Observability"])


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "ok"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return {
        "status": "ok" if db_status == "ok" else "degraded",
        "system": "AI Business OS",
        "version": "0.1.0",
        "database": db_status,
    }


@router.get("/metrics")
async def metrics(db: AsyncSession = Depends(get_db)):
    # Query system aggregates
    biz_count = (await db.execute(select(func.count(Business.id)))).scalar() or 0
    pending_approvals = (
        await db.execute(select(func.count(Approval.id)).where(Approval.status == "PENDING"))
    ).scalar() or 0
    total_runs = (await db.execute(select(func.count(AgentRun.id)))).scalar() or 0

    return {
        "active_businesses": biz_count,
        "pending_approvals": pending_approvals,
        "total_agent_runs": total_runs,
        "system_status": "ONLINE",
    }
