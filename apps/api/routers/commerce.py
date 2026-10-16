import uuid
from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from businesses.core.registry import BusinessRegistry
from businesses.msme_compliance.config import MSMEComplianceConfig
from businesses.msme_compliance.module import MSMEComplianceModule
from businesses.msme_compliance.toolkit_generator import MSMEToolkitGenerator
from database.connection import get_db
from database.models.audit_log import AuditLog
from database.models.business import Business, BusinessConfig
from database.models.core_stubs import Customer, Order, Transaction
from tools.finance.payment_provider import PaymentProviderFactory

router = APIRouter(prefix="/public", tags=["Commerce & Storefront"])


class CheckoutRequest(BaseModel):
    sku: str = Field(default="MSME-43BH-STARTER", description="Product SKU to purchase")
    customer_name: str = Field(..., min_length=2, max_length=255)
    customer_email: str = Field(..., min_length=5, max_length=255)
    customer_phone: Optional[str] = Field(default=None, max_length=50)
    company_name: Optional[str] = Field(default=None, max_length=255)
    gstin: Optional[str] = Field(default=None, max_length=20)


class VerifyPaymentRequest(BaseModel):
    order_id: str
    gateway_order_id: str
    gateway_payment_id: str
    gateway_signature: str


async def _get_or_create_msme_business(db: AsyncSession) -> Business:
    """Ensure the MSME Compliance business row exists in the database."""
    stmt = select(Business).where(Business.module_name == "msme_compliance")
    result = await db.execute(stmt)
    biz = result.scalars().first()

    if not biz:
        config_obj = MSMEComplianceConfig()
        biz = Business(
            id="biz_msme_compliance_43bh",
            name="MSME Section 43B(h) Compliance Toolkit",
            description="Statutory payment compliance and audit toolkit for Indian enterprises.",
            status="ACTIVE",
            module_name="msme_compliance",
        )
        db.add(biz)
        await db.flush()

        b_config = BusinessConfig(
            business_id=biz.id,
            target_customer=config_obj.target_customer,
            pricing={t.sku: t.price_inr for t in config_obj.pricing_tiers},
            acquisition_channels=["organic_b2b_seo", "chartered_accountant_communities"],
            sales_process={"model": "instant_self_checkout", "gateway": "razorpay_upi"},
            fulfilment_process={"model": "instant_digital_delivery", "format": "zip_bundle"},
            revenue_model={"type": "one_time_digital_product_sale", "margin_target": 0.92},
            cost_model={"gateway_fee_percent": 2.0, "hosting_and_delivery_inr": 10.0},
            kpis=[{"metric": k, "target": "industry_benchmark"} for k in config_obj.kpis],
            policies={"max_daily_marketing_spend_inr": 500.0},
            approval_rules={"marketing_spend_above_inr": 500.0},
        )
        db.add(b_config)
        await db.flush()

    return biz


@router.get("/products")
async def list_products():
    """List commercial product tiers available for purchase."""
    config = MSMEComplianceConfig()
    manifest = MSMEToolkitGenerator.get_template_manifest()
    return {
        "status": "active",
        "business": {
            "name": "MSME Section 43B(h) Compliance & Audit Engine",
            "statutory_reference": config.statutory_reference,
            "target_geography": config.target_geography,
        },
        "tiers": [tier.model_dump() for tier in config.pricing_tiers],
        "deliverables_manifest": manifest,
        "payment_rails": ["UPI (Google Pay, PhonePe, Paytm, BHIM)", "Credit/Debit Cards", "Netbanking"],
    }


@router.post("/checkout")
async def create_checkout_session(payload: CheckoutRequest, db: AsyncSession = Depends(get_db)):
    """
    Create a verified checkout session and payment order for MSME compliance products.
    """
    config = MSMEComplianceConfig()
    selected_tier = next((t for t in config.pricing_tiers if t.sku.upper() == payload.sku.upper()), None)
    if not selected_tier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid SKU '{payload.sku}'. Valid SKUs: {[t.sku for t in config.pricing_tiers]}",
        )

    biz = await _get_or_create_msme_business(db)

    # Find or create customer
    stmt_cust = select(Customer).where(
        Customer.business_id == biz.id,
        Customer.email == payload.customer_email,
    )
    res_cust = await db.execute(stmt_cust)
    cust = res_cust.scalars().first()

    cust_metadata = {
        "company_name": payload.company_name or payload.customer_name,
        "gstin": payload.gstin,
        "source": "storefront_checkout",
    }

    if not cust:
        cust = Customer(
            business_id=biz.id,
            name=payload.customer_name,
            email=payload.customer_email,
            phone=payload.customer_phone,
            status="ACTIVE",
            metadata_json=cust_metadata,
        )
        db.add(cust)
        await db.flush()
    else:
        cust.phone = payload.customer_phone or cust.phone
        cust.metadata_json = {**cust.metadata_json, **cust_metadata}

    # Create Order
    order_id = str(uuid.uuid4())
    provider = PaymentProviderFactory.get_provider()

    payment_order = await provider.create_order(
        amount_inr=selected_tier.price_inr,
        currency="INR",
        receipt=order_id[:16],
        notes={
            "app_order_id": order_id,
            "sku": selected_tier.sku,
            "buyer_email": payload.customer_email,
            "company_name": payload.company_name or payload.customer_name,
        },
    )

    order = Order(
        id=order_id,
        business_id=biz.id,
        customer_id=cust.id,
        status="PENDING",
        amount=selected_tier.price_inr,
        currency="INR",
        items=[selected_tier.model_dump()],
        gateway=payment_order.gateway,
        gateway_order_id=payment_order.id,
        metadata_json={
            "sku": selected_tier.sku,
            "tier_name": selected_tier.name,
            "company_name": payload.company_name or payload.customer_name,
            "gstin": payload.gstin,
            "customer_name": payload.customer_name,
            "customer_email": payload.customer_email,
        },
    )
    db.add(order)
    await db.commit()
    await db.refresh(order)

    return {
        "order_id": order.id,
        "gateway": payment_order.gateway,
        "gateway_order_id": payment_order.id,
        "key_id": payment_order.key_id,
        "amount": selected_tier.price_inr,
        "amount_paise": payment_order.amount_paise,
        "currency": "INR",
        "sku": selected_tier.sku,
        "product_name": selected_tier.name,
        "customer": {
            "name": payload.customer_name,
            "email": payload.customer_email,
            "phone": payload.customer_phone,
            "company_name": payload.company_name,
        },
    }


@router.post("/verify-payment")
async def verify_payment(payload: VerifyPaymentRequest, db: AsyncSession = Depends(get_db)):
    """
    Verify payment signature from client checkout modal, record transaction,
    fulfill digital deliverables, and generate secure download token.
    """
    stmt = select(Order).where(Order.id == payload.order_id)
    res = await db.execute(stmt)
    order = res.scalars().first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    provider = PaymentProviderFactory.get_provider()
    is_valid = provider.verify_payment_signature(
        gateway_order_id=payload.gateway_order_id,
        gateway_payment_id=payload.gateway_payment_id,
        gateway_signature=payload.gateway_signature,
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment signature verification failed. Untrusted transaction.",
        )

    # Idempotent handling: if already fulfilled, return existing token
    if order.status in ("PAID", "FULFILLED") and order.download_token:
        return {
            "success": True,
            "order_id": order.id,
            "status": order.status,
            "download_token": order.download_token,
            "download_url": f"/api/public/orders/download?token={order.download_token}",
        }

    download_token = f"dl_{uuid.uuid4().hex}"
    order.status = "FULFILLED"
    order.gateway_payment_id = payload.gateway_payment_id
    order.gateway_signature = payload.gateway_signature
    order.download_token = download_token

    # Create Transaction record
    tx = Transaction(
        business_id=order.business_id,
        amount=order.amount,
        currency=order.currency,
        type="INFLOW",
        status="COMPLETED",
        reference=payload.gateway_payment_id,
    )
    db.add(tx)

    # Log to AuditLog
    audit_entry = AuditLog(
        actor="checkout_verify",
        business_id=order.business_id,
        action="payment_verified_and_fulfilled",
        target=f"order:{order.id}",
        result="SUCCESS",
        metadata_json={
            "order_id": order.id,
            "amount": order.amount,
            "gateway_order_id": payload.gateway_order_id,
            "gateway_payment_id": payload.gateway_payment_id,
            "sku": order.metadata_json.get("sku"),
        },
    )
    db.add(audit_entry)

    await db.commit()
    await db.refresh(order)

    return {
        "success": True,
        "order_id": order.id,
        "status": order.status,
        "download_token": order.download_token,
        "download_url": f"/api/public/orders/download?token={order.download_token}",
        "message": "Payment verified and compliance toolkit unlocked.",
    }


@router.get("/orders/{order_id}/status")
async def get_order_status(order_id: str, db: AsyncSession = Depends(get_db)):
    """Check status of an order."""
    stmt = select(Order).where(Order.id == order_id)
    res = await db.execute(stmt)
    order = res.scalars().first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    return {
        "order_id": order.id,
        "status": order.status,
        "amount": order.amount,
        "currency": order.currency,
        "gateway": order.gateway,
        "has_download": bool(order.download_token and order.status in ("PAID", "FULFILLED")),
        "download_url": f"/api/public/orders/download?token={order.download_token}" if order.download_token else None,
    }


@router.get("/orders/download")
async def download_toolkit(token: str = Query(..., description="Secure one-time download token"), db: AsyncSession = Depends(get_db)):
    """
    Secure endpoint providing instant delivery of the MSME Section 43B(h) Compliance Toolkit ZIP archive.
    """
    stmt = select(Order).where(Order.download_token == token)
    res = await db.execute(stmt)
    order = res.scalars().first()

    if not order or order.status not in ("PAID", "FULFILLED"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or unauthorized download token.",
        )

    company_name = order.metadata_json.get("company_name", "Enterprise Buyer")
    zip_bytes = MSMEToolkitGenerator.generate_zip_bundle(company_name=company_name)

    safe_name = "".join(c for c in company_name if c.isalnum() or c in ("-", "_")).strip() or "Enterprise"
    filename = f"MSME_Section_43Bh_Compliance_Toolkit_{safe_name}.zip"

    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Cache-Control": "no-store, no-cache, must-revalidate",
        },
    )
