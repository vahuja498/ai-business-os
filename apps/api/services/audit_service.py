from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.audit_log import AuditLog


class AuditService:
    @staticmethod
    async def record_event(
        db: AsyncSession,
        actor: str,
        action: str,
        result: str,
        target: str | None = None,
        agent_id: str | None = None,
        business_id: str | None = None,
        approval_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditLog:
        audit_entry = AuditLog(
            actor=actor,
            agent_id=agent_id,
            business_id=business_id,
            action=action,
            target=target,
            result=result,
            approval_id=approval_id,
            metadata_json=metadata or {},
        )
        db.add(audit_entry)
        await db.commit()
        await db.refresh(audit_entry)
        return audit_entry
