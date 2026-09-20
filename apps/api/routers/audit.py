from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.models.audit_log import AuditLog

router = APIRouter(prefix="/audit", tags=["Audit Log"])


@router.get("")
async def list_audit_logs(
    business_id: str | None = None,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    if business_id:
        stmt = stmt.where(AuditLog.business_id == business_id)
    res = await db.execute(stmt)
    logs = res.scalars().all()
    return [
        {
            "id": log.id,
            "actor": log.actor,
            "agent_id": log.agent_id,
            "business_id": log.business_id,
            "action": log.action,
            "target": log.target,
            "result": log.result,
            "approval_id": log.approval_id,
            "metadata": log.metadata_json,
            "created_at": log.created_at,
        }
        for log in logs
    ]
