from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.connection import get_db
from database.models.opportunity import Opportunity

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


@router.get("")
async def list_opportunities(business_id: str | None = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Opportunity).order_by(Opportunity.created_at.desc())
    if business_id:
        stmt = stmt.where(Opportunity.business_id == business_id)
    result = await db.execute(stmt)
    opps = result.scalars().all()
    return [
        {
            "id": o.id,
            "business_id": o.business_id,
            "title": o.title,
            "description": o.description,
            "target_market": o.target_market,
            "revenue_model": o.revenue_model,
            "estimated_startup_cost": o.estimated_startup_cost,
            "estimated_customer_value": o.estimated_customer_value,
            "estimated_acquisition_cost": o.estimated_acquisition_cost,
            "estimated_fulfilment_cost": o.estimated_fulfilment_cost,
            "estimated_margin": o.estimated_margin,
            "automation_potential": o.automation_potential,
            "regulatory_complexity": o.regulatory_complexity,
            "platform_dependency": o.platform_dependency,
            "risk_level": o.risk_level,
            "evidence": o.evidence,
            "assumptions": o.assumptions,
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
        "description": opp.description,
        "target_market": opp.target_market,
        "revenue_model": opp.revenue_model,
        "estimated_startup_cost": opp.estimated_startup_cost,
        "estimated_customer_value": opp.estimated_customer_value,
        "estimated_acquisition_cost": opp.estimated_acquisition_cost,
        "estimated_fulfilment_cost": opp.estimated_fulfilment_cost,
        "estimated_margin": opp.estimated_margin,
        "automation_potential": opp.automation_potential,
        "regulatory_complexity": opp.regulatory_complexity,
        "platform_dependency": opp.platform_dependency,
        "risk_level": opp.risk_level,
        "evidence": opp.evidence,
        "assumptions": opp.assumptions,
        "recommended_experiment": opp.recommended_experiment,
        "status": opp.status,
        "created_at": opp.created_at,
    }
