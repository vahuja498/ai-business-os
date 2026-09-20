from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.models.task import Task

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("")
async def list_tasks(business_id: str | None = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Task).order_by(Task.created_at.desc())
    if business_id:
        stmt = stmt.where(Task.business_id == business_id)
    res = await db.execute(stmt)
    tasks = res.scalars().all()
    return [
        {
            "id": t.id,
            "business_id": t.business_id,
            "parent_task_id": t.parent_task_id,
            "title": t.title,
            "description": t.description,
            "assigned_agent_id": t.assigned_agent_id,
            "status": t.status,
            "retry_count": t.retry_count,
            "max_retries": t.max_retries,
            "escalation_reason": t.escalation_reason,
            "created_at": t.created_at,
        }
        for t in tasks
    ]
