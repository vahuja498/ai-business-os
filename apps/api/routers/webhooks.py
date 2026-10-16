import json
import uuid
from typing import Any
from fastapi import APIRouter, Depends, Header, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import get_db
from database.models.audit_log import AuditLog
from database.models.core_stubs import Order, Transaction
from tools.finance.payment_provider import PaymentProviderFactory

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/razorpay")
async def handle_razorpay_webhook(
    request: Request,
    x_razorpay_signature: str | None = Header(None, alias="X-Razorpay-Signature"),
    db: AsyncSession = Depends(get_db),
):
    """
    Handle incoming Razorpay webhooks for payment capture, auto-fulfillment,
    and ledger reconciliation.
    """
    raw_body = await request.body()
    provider = PaymentProviderFactory.get_provider()

    if not x_razorpay_signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-Razorpay-Signature header",
        )

    # Cryptographic signature verification
    is_valid = provider.verify_webhook_signature(
        webhook_body=raw_body,
        webhook_signature=x_razorpay_signature,
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature",
        )

    try:
        event_data: dict[str, Any] = json.loads(raw_body.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid JSON: {exc}")

    event_type = event_data.get("event", "unknown")

    # We process payment.captured and order.paid
    if event_type in ("payment.captured", "order.paid"):
        payload_data = event_data.get("payload", {})
        payment_entity = payload_data.get("payment", {}).get("entity", {})
        order_entity = payload_data.get("order", {}).get("entity", {})

        rzp_order_id = payment_entity.get("order_id") or order_entity.get("id")
        rzp_payment_id = payment_entity.get("id")
        notes = payment_entity.get("notes", {}) or order_entity.get("notes", {})
        app_order_id = notes.get("app_order_id")

        order = None
        if app_order_id:
            stmt = select(Order).where(Order.id == app_order_id)
            res = await db.execute(stmt)
            order = res.scalars().first()

        if not order and rzp_order_id:
            stmt = select(Order).where(Order.gateway_order_id == rzp_order_id)
            res = await db.execute(stmt)
            order = res.scalars().first()

        if order and order.status != "FULFILLED":
            order.status = "FULFILLED"
            order.gateway_payment_id = rzp_payment_id or order.gateway_payment_id
            if not order.download_token:
                order.download_token = f"dl_{uuid.uuid4().hex}"

            # Add financial transaction to ledger
            tx = Transaction(
                business_id=order.business_id,
                amount=order.amount,
                currency=order.currency,
                type="INFLOW",
                status="COMPLETED",
                reference=rzp_payment_id or rzp_order_id,
            )
            db.add(tx)

            # Audit log
            audit = AuditLog(
                actor="razorpay_webhook",
                business_id=order.business_id,
                action="webhook_payment_captured",
                target=f"order:{order.id}",
                result="SUCCESS",
                metadata_json={
                    "event": event_type,
                    "order_id": order.id,
                    "gateway_order_id": rzp_order_id,
                    "gateway_payment_id": rzp_payment_id,
                    "amount": order.amount,
                },
            )
            db.add(audit)
            await db.commit()

    return {"status": "ok", "event": event_type}
