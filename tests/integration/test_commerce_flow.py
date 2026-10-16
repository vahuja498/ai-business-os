import io
import json
import zipfile
import pytest
from httpx import AsyncClient
from tools.finance.payment_provider import MockPaymentProvider, PaymentProviderFactory


@pytest.mark.asyncio
async def test_public_products_endpoint(async_client: AsyncClient):
    response = await async_client.get("/public/products")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "active"
    assert len(data["tiers"]) >= 2
    skus = [t["sku"] for t in data["tiers"]]
    assert "MSME-43BH-STARTER" in skus
    assert "MSME-43BH-PRO-CA" in skus
    assert len(data["deliverables_manifest"]) >= 5


@pytest.mark.asyncio
async def test_checkout_and_verification_flow(async_client: AsyncClient):
    PaymentProviderFactory.reset()

    # 1. Checkout
    checkout_payload = {
        "sku": "MSME-43BH-STARTER",
        "customer_name": "Vikram Mehta",
        "customer_email": "vikram@mehtaenterprises.in",
        "customer_phone": "+919811223344",
        "company_name": "Mehta Precision Engineering",
        "gstin": "06AAACM1234F1Z9",
    }
    res_checkout = await async_client.post("/public/checkout", json=checkout_payload)
    assert res_checkout.status_code == 200
    checkout_data = res_checkout.json()

    order_id = checkout_data["order_id"]
    gateway_order_id = checkout_data["gateway_order_id"]
    assert order_id is not None
    assert checkout_data["amount"] == 1999.0
    assert checkout_data["currency"] == "INR"

    # 2. Check Order Status (Before payment)
    res_status_1 = await async_client.get(f"/public/orders/{order_id}/status")
    assert res_status_1.status_code == 200
    assert res_status_1.json()["status"] == "PENDING"
    assert res_status_1.json()["has_download"] is False

    # 3. Invalid signature verification attempt (must fail)
    res_invalid_verify = await async_client.post(
        "/public/verify-payment",
        json={
            "order_id": order_id,
            "gateway_order_id": gateway_order_id,
            "gateway_payment_id": "pay_fake_123",
            "gateway_signature": "invalid_forged_sig",
        },
    )
    assert res_invalid_verify.status_code == 400

    # 4. Valid signature verification
    res_valid_verify = await async_client.post(
        "/public/verify-payment",
        json={
            "order_id": order_id,
            "gateway_order_id": gateway_order_id,
            "gateway_payment_id": "pay_mock_success_789",
            "gateway_signature": "mock_sig_valid",
        },
    )
    assert res_valid_verify.status_code == 200
    verify_data = res_valid_verify.json()
    assert verify_data["success"] is True
    assert verify_data["status"] == "FULFILLED"
    download_token = verify_data["download_token"]
    assert download_token.startswith("dl_")

    # 5. Check Order Status (After payment)
    res_status_2 = await async_client.get(f"/public/orders/{order_id}/status")
    assert res_status_2.status_code == 200
    assert res_status_2.json()["status"] == "FULFILLED"
    assert res_status_2.json()["has_download"] is True

    # 6. Download ZIP Deliverables with token
    # Unauthorized attempt
    res_unauthorized = await async_client.get("/public/orders/download?token=fake_dl_token")
    assert res_unauthorized.status_code == 403

    # Authorized download
    res_download = await async_client.get(f"/public/orders/download?token={download_token}")
    assert res_download.status_code == 200
    assert res_download.headers["content-type"] == "application/zip"
    assert "attachment" in res_download.headers.get("content-disposition", "")

    # Validate ZIP content in response
    zip_bytes = res_download.content
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        file_list = zf.namelist()
        assert len(file_list) >= 5
        assert "01_CFO_Action_Guide_Section_43Bh.md" in file_list
        guide_text = zf.read("01_CFO_Action_Guide_Section_43Bh.md").decode("utf-8")
        assert "MEHTA PRECISION ENGINEERING" in guide_text


@pytest.mark.asyncio
async def test_webhook_payment_fulfillment(async_client: AsyncClient):
    PaymentProviderFactory.reset()

    # 1. Create Checkout Order
    res_checkout = await async_client.post(
        "/public/checkout",
        json={
            "sku": "MSME-43BH-PRO-CA",
            "customer_name": "Suresh Gupta FCA",
            "customer_email": "suresh@guptaca.in",
            "company_name": "Gupta & Associates CA Firm",
        },
    )
    assert res_checkout.status_code == 200
    checkout_data = res_checkout.json()
    order_id = checkout_data["order_id"]
    gateway_order_id = checkout_data["gateway_order_id"]

    # 2. Test webhook missing header
    res_no_sig = await async_client.post("/webhooks/razorpay", content=b"{}")
    assert res_no_sig.status_code == 400

    # 3. Test webhook bad signature
    res_bad_sig = await async_client.post(
        "/webhooks/razorpay",
        content=b"{}",
        headers={"X-Razorpay-Signature": "invalid_sig"},
    )
    assert res_bad_sig.status_code == 401

    # 4. Valid Webhook event: payment.captured
    webhook_payload = {
        "event": "payment.captured",
        "payload": {
            "payment": {
                "entity": {
                    "id": "pay_rzp_webhook_999",
                    "order_id": gateway_order_id,
                    "amount": 399900,
                    "currency": "INR",
                    "status": "captured",
                    "notes": {"app_order_id": order_id},
                }
            }
        },
    }
    raw_payload = json.dumps(webhook_payload).encode("utf-8")

    res_webhook = await async_client.post(
        "/webhooks/razorpay",
        content=raw_payload,
        headers={"X-Razorpay-Signature": "mock_webhook_valid"},
    )
    assert res_webhook.status_code == 200
    assert res_webhook.json()["status"] == "ok"

    # 5. Verify order is now FULFILLED and has download token
    res_status = await async_client.get(f"/public/orders/{order_id}/status")
    assert res_status.status_code == 200
    status_data = res_status.json()
    assert status_data["status"] == "FULFILLED"
    assert status_data["has_download"] is True
    assert status_data["download_url"] is not None
