from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from apps.api.services.audit_service import AuditService
from apps.api.services.orchestration import OrchestrationService
from database.connection import get_db
from database.models.business import Business, BusinessConfig

router = APIRouter(prefix="/businesses", tags=["Businesses"])


class CreateBusinessRequest(BaseModel):
    name: str
    description: str | None = None
    module_name: str = "core"
    target_customer: str = ""
    pricing: dict[str, Any] = Field(default_factory=dict)
    acquisition_channels: list[str] = Field(default_factory=list)
    revenue_model: dict[str, Any] = Field(default_factory=dict)
    cost_model: dict[str, Any] = Field(default_factory=dict)
    kpis: list[dict[str, Any]] = Field(default_factory=list)


class ObjectiveRequest(BaseModel):
    objective: str


@router.post("")
async def create_business(payload: CreateBusinessRequest, db: AsyncSession = Depends(get_db)):
    business = Business(
        name=payload.name,
        description=payload.description,
        module_name=payload.module_name,
        status="DRAFT",
    )
    db.add(business)
    await db.flush()

    config = BusinessConfig(
        business_id=business.id,
        target_customer=payload.target_customer,
        pricing=payload.pricing,
        acquisition_channels=payload.acquisition_channels,
        revenue_model=payload.revenue_model,
        cost_model=payload.cost_model,
        kpis=payload.kpis,
    )
    db.add(config)
    await db.commit()
    await db.refresh(business)

    await AuditService.record_event(
        db=db,
        actor="USER",
        business_id=business.id,
        action="CREATE_BUSINESS",
        target=f"Business:{business.id}",
        result="SUCCESS",
        metadata={"name": business.name, "module": business.module_name},
    )

    return {
        "id": business.id,
        "name": business.name,
        "description": business.description,
        "status": business.status,
        "module_name": business.module_name,
        "created_at": business.created_at,
    }


@router.get("")
async def list_businesses(db: AsyncSession = Depends(get_db)):
    stmt = select(Business).order_by(Business.created_at.desc())
    result = await db.execute(stmt)
    businesses = result.scalars().all()
    return [
        {
            "id": b.id,
            "name": b.name,
            "description": b.description,
            "status": b.status,
            "module_name": b.module_name,
            "created_at": b.created_at,
        }
        for b in businesses
    ]


@router.get("/{business_id}")
async def get_business(business_id: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Business).where(Business.id == business_id)
    res = await db.execute(stmt)
    business = res.scalar_one_or_none()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    cfg_stmt = select(BusinessConfig).where(BusinessConfig.business_id == business_id)
    cfg_res = await db.execute(cfg_stmt)
    config = cfg_res.scalar_one_or_none()

    return {
        "id": business.id,
        "name": business.name,
        "description": business.description,
        "status": business.status,
        "module_name": business.module_name,
        "created_at": business.created_at,
        "config": {
            "target_customer": config.target_customer if config else "",
            "pricing": config.pricing if config else {},
            "acquisition_channels": config.acquisition_channels if config else [],
            "kpis": config.kpis if config else [],
        } if config else None,
    }


@router.post("/{business_id}/objectives")
async def execute_business_objective(
    business_id: str,
    payload: ObjectiveRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await OrchestrationService.execute_objective(
            db=db,
            business_id=business_id,
            objective=payload.objective,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
