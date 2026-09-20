from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.models.agent import Agent, AgentRun

router = APIRouter(prefix="/agents", tags=["Agents"])


@router.get("")
async def list_agents(db: AsyncSession = Depends(get_db)):
    stmt = select(Agent).order_by(Agent.name.asc())
    res = await db.execute(stmt)
    agents = res.scalars().all()
    return [
        {
            "id": a.id,
            "name": a.name,
            "description": a.description,
            "capabilities": a.capabilities,
            "allowed_tools": a.allowed_tools,
            "execution_mode": a.execution_mode,
            "risk_level": a.risk_level,
            "status": a.status,
        }
        for a in agents
    ]


@router.get("/runs")
async def list_agent_runs(business_id: str | None = None, db: AsyncSession = Depends(get_db)):
    stmt = select(AgentRun).order_by(AgentRun.started_at.desc())
    if business_id:
        stmt = stmt.where(AgentRun.business_id == business_id)
    res = await db.execute(stmt)
    runs = res.scalars().all()
    return [
        {
            "id": r.id,
            "agent_id": r.agent_id,
            "business_id": r.business_id,
            "task_id": r.task_id,
            "actions": r.actions,
            "final_status": r.final_status,
            "errors": r.errors,
            "started_at": r.started_at,
            "completed_at": r.completed_at,
        }
        for r in runs
    ]
