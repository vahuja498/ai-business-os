import hashlib
import hmac
import pytest
from tools.finance.payment_provider import (
    MockPaymentProvider,
    PaymentProviderFactory,
    RazorpayPaymentProvider,
)


@pytest.mark.asyncio
async def test_mock_payment_provider_create_order():
    provider = MockPaymentProvider(key_id="rzp_test_key1", key_secret="secret_abc")
    order = await provider.create_order(
        amount_inr=1999.0,
        currency="INR",
        receipt="rcpt_001",
        notes={"tier": "starter"},
    )
    assert order.id.startswith("order_mock_")
    assert order.amount == 1999.0
    assert order.amount_paise == 199900
    assert order.currency == "INR"
    assert order.receipt == "rcpt_001"
    assert order.gateway == "mock"
    assert order.key_id == "rzp_test_key1"


def test_mock_payment_provider_signatures():
    provider = MockPaymentProvider(key_id="rzp_test_key1", key_secret="secret_abc")
    
    # Valid explicit test signatures
    assert provider.verify_payment_signature("order_1", "pay_1", "mock_sig_valid") is True
    assert provider.verify_payment_signature("order_1", "pay_1", "mock_signature_pass") is True
    assert provider.verify_payment_signature("order_1", "pay_1", "mock_sig_anything") is True
    assert provider.verify_payment_signature("order_1", "pay_1", "invalid_sig") is False
    assert provider.verify_payment_signature("order_1", "pay_1", "") is False

    # Valid computed HMAC
    msg = "order_1|pay_1"
    expected = hmac.new("secret_abc".encode(), msg.encode(), hashlib.sha256).hexdigest()
    assert provider.verify_payment_signature("order_1", "pay_1", expected) is True

    # Webhook signature verification
    assert provider.verify_webhook_signature("body_content", "mock_webhook_valid") is True
    assert provider.verify_webhook_signature("body_content", "invalid_webhook_sig") is False


@pytest.mark.asyncio
async def test_mock_payment_provider_fetch():
    provider = MockPaymentProvider()
    data = await provider.fetch_payment("pay_test_123")
    assert data["id"] == "pay_test_123"
    assert data["status"] == "captured"
    assert data["method"] == "upi"


def test_razorpay_signature_verification():
    key_secret = "rzp_secret_987654"
    provider = RazorpayPaymentProvider(
        key_id="rzp_test_id1",
        key_secret=key_secret,
        webhook_secret="rzp_hook_sec",
    )

    order_id = "order_EMWvkdPtUh0szW"
    payment_id = "pay_EMWw12Svd8W61"
    message = f"{order_id}|{payment_id}"
    valid_signature = hmac.new(key_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()

    assert provider.verify_payment_signature(order_id, payment_id, valid_signature) is True
    assert provider.verify_payment_signature(order_id, payment_id, "forged_sig") is False

    # Webhook HMAC test
    body = '{"event":"payment.captured"}'
    valid_hook_sig = hmac.new("rzp_hook_sec".encode("utf-8"), body.encode("utf-8"), hashlib.sha256).hexdigest()
    assert provider.verify_webhook_signature(body, valid_hook_sig) is True
    assert provider.verify_webhook_signature(body, "bad_sig") is False


def test_payment_provider_factory(monkeypatch):
    PaymentProviderFactory.reset()
    
    # By default without keys, returns MockPaymentProvider
    monkeypatch.delenv("PAYMENT_PROVIDER", raising=False)
    monkeypatch.delenv("RAZORPAY_KEY_ID", raising=False)
    provider = PaymentProviderFactory.get_provider()
    assert isinstance(provider, MockPaymentProvider)

    # When explicit mock
    provider_mock = PaymentProviderFactory.get_provider("mock")
    assert isinstance(provider_mock, MockPaymentProvider)

    # Injected provider
    custom_mock = MockPaymentProvider(key_id="custom_key")
    PaymentProviderFactory.set_provider(custom_mock)
    assert PaymentProviderFactory.get_provider() == custom_mock
    PaymentProviderFactory.reset()
