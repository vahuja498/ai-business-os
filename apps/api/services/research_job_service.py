from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from agents.research.opportunity_engine import OpportunityEngine, DEFAULT_RESEARCH_TEMPLATE


class ResearchJobService:
    """
    Architecture for scheduled and on-demand opportunity research jobs (Section 11).
    Autonomous recurring schedules are disabled by default; manual invocation is exposed.
    """

    @classmethod
    async def run_research_job(
        cls,
        db: AsyncSession,
        objective: str = DEFAULT_RESEARCH_TEMPLATE,
        business_id: str | None = None,
        job_type: str = "on-demand",  # on-demand, daily, weekly
    ) -> dict[str, Any]:
        engine = OpportunityEngine()
        opportunities = await engine.execute_research(
            db=db,
            objective=objective,
            business_id=business_id,
        )
        return {
            "status": "COMPLETED",
            "job_type": job_type,
            "objective": objective,
            "opportunities_generated": len(opportunities),
            "opportunities": opportunities,
        }
