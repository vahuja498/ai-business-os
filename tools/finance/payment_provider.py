import hashlib
import hmac
import os
import uuid
from abc import ABC, abstractmethod
from typing import Any, Optional
import httpx
from pydantic import BaseModel, Field


class PaymentOrder(BaseModel):
    id: str
    amount: float
    amount_paise: int
    currency: str = "INR"
    receipt: str
    status: str = "created"
    gateway: str
    key_id: Optional[str] = None
    checkout_url: Optional[str] = None
    raw_data: dict[str, Any] = Field(default_factory=dict)


class PaymentVerificationResult(BaseModel):
    is_valid: bool
    order_id: str
    payment_id: Optional[str] = None
    signature: Optional[str] = None
    error_message: Optional[str] = None
    event_type: Optional[str] = None


class PaymentProvider(ABC):
    """
    Abstract payment gateway provider interface.
    Supports multi-rail payment flows with India-first capabilities
    (Razorpay, UPI Intent, Netbanking, Cards, automated webhooks).
    """

    @abstractmethod
    async def create_order(
        self,
        amount_inr: float,
        currency: str = "INR",
        receipt: Optional[str] = None,
        notes: Optional[dict[str, Any]] = None,
    ) -> PaymentOrder:
        """Create an order with the payment provider."""
        pass

    @abstractmethod
    def verify_payment_signature(
        self,
        gateway_order_id: str,
        gateway_payment_id: str,
        gateway_signature: str,
    ) -> bool:
        """Verify the signature returned to client upon payment completion."""
        pass

    @abstractmethod
    def verify_webhook_signature(
        self,
        webhook_body: str | bytes,
        webhook_signature: str,
        webhook_secret: Optional[str] = None,
    ) -> bool:
        """Verify the cryptographic authenticity of an inbound payment webhook."""
        pass

    @abstractmethod
    async def fetch_payment(self, payment_id: str) -> dict[str, Any]:
        """Fetch payment details from the gateway."""
        pass


class MockPaymentProvider(PaymentProvider):
    """
    Simulated payment provider for deterministic unit/integration testing
    and zero-risk sandbox development.
    """

    def __init__(self, key_id: str = "rzp_test_mockkey123", key_secret: str = "mock_secret_456"):
        self.key_id = key_id
        self.key_secret = key_secret
        self.recorded_orders: dict[str, PaymentOrder] = {}

    async def create_order(
        self,
        amount_inr: float,
        currency: str = "INR",
        receipt: Optional[str] = None,
        notes: Optional[dict[str, Any]] = None,
    ) -> PaymentOrder:
        receipt_val = receipt or f"rcpt_{uuid.uuid4().hex[:8]}"
        order_id = f"order_mock_{uuid.uuid4().hex[:12]}"
        amount_paise = int(round(amount_inr * 100))

        order = PaymentOrder(
            id=order_id,
            amount=amount_inr,
            amount_paise=amount_paise,
            currency=currency,
            receipt=receipt_val,
            status="created",
            gateway="mock",
            key_id=self.key_id,
            raw_data={
                "id": order_id,
                "entity": "order",
                "amount": amount_paise,
                "amount_paid": 0,
                "amount_due": amount_paise,
                "currency": currency,
                "receipt": receipt_val,
                "status": "created",
                "attempts": 0,
                "notes": notes or {},
            },
        )
        self.recorded_orders[order_id] = order
        return order

    def verify_payment_signature(
        self,
        gateway_order_id: str,
        gateway_payment_id: str,
        gateway_signature: str,
    ) -> bool:
        if not gateway_signature:
            return False
        # Accept valid test signatures
        if gateway_signature in ("mock_sig_valid", "mock_signature_pass"):
            return True
        if gateway_signature.startswith("mock_sig_"):
            return True
        # Compute HMAC using mock secret
        msg = f"{gateway_order_id}|{gateway_payment_id}"
        expected = hmac.new(self.key_secret.encode(), msg.encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, gateway_signature)

    def verify_webhook_signature(
        self,
        webhook_body: str | bytes,
        webhook_signature: str,
        webhook_secret: Optional[str] = None,
    ) -> bool:
        if not webhook_signature:
            return False
        if webhook_signature in ("mock_webhook_valid", "mock_webhook_signature"):
            return True
        secret = webhook_secret or self.key_secret
        body_bytes = webhook_body if isinstance(webhook_body, bytes) else webhook_body.encode("utf-8")
        expected = hmac.new(secret.encode(), body_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, webhook_signature)

    async def fetch_payment(self, payment_id: str) -> dict[str, Any]:
        return {
            "id": payment_id,
            "entity": "payment",
            "amount": 199900,
            "currency": "INR",
            "status": "captured",
            "method": "upi",
            "vpa": "customer@okhdfcbank",
            "email": "customer@msmebiz.in",
            "contact": "+919876543210",
        }


class RazorpayPaymentProvider(PaymentProvider):
    """
    Live/Sandbox Razorpay API integration for India.
    Supports UPI QR, UPI Auto-Collect, Cards, Netbanking, and Wallets.
    Uses standard HTTP basic auth and HMAC-SHA256 signature verification.
    """

    BASE_URL = "https://api.razorpay.com/v1"

    def __init__(
        self,
        key_id: Optional[str] = None,
        key_secret: Optional[str] = None,
        webhook_secret: Optional[str] = None,
        timeout: float = 15.0,
    ):
        self.key_id = key_id or os.getenv("RAZORPAY_KEY_ID", "")
        self.key_secret = key_secret or os.getenv("RAZORPAY_KEY_SECRET", "")
        self.webhook_secret = webhook_secret or os.getenv("RAZORPAY_WEBHOOK_SECRET", "")
        self.timeout = timeout

        if not self.key_id or not self.key_secret:
            raise ValueError(
                "RazorpayPaymentProvider requires RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET environment variables"
            )

    async def create_order(
        self,
        amount_inr: float,
        currency: str = "INR",
        receipt: Optional[str] = None,
        notes: Optional[dict[str, Any]] = None,
    ) -> PaymentOrder:
        receipt_val = receipt or f"rcpt_{uuid.uuid4().hex[:8]}"
        amount_paise = int(round(amount_inr * 100))

        payload = {
            "amount": amount_paise,
            "currency": currency,
            "receipt": receipt_val,
            "notes": notes or {},
            "payment_capture": 1,  # Auto-capture on authorization
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.BASE_URL}/orders",
                json=payload,
                auth=(self.key_id, self.key_secret),
            )
            response.raise_for_status()
            data = response.json()

        return PaymentOrder(
            id=data["id"],
            amount=amount_inr,
            amount_paise=amount_paise,
            currency=currency,
            receipt=receipt_val,
            status=data.get("status", "created"),
            gateway="razorpay",
            key_id=self.key_id,
            raw_data=data,
        )

    def verify_payment_signature(
        self,
        gateway_order_id: str,
        gateway_payment_id: str,
        gateway_signature: str,
    ) -> bool:
        if not gateway_signature or not self.key_secret:
            return False
        msg = f"{gateway_order_id}|{gateway_payment_id}"
        expected = hmac.new(self.key_secret.encode("utf-8"), msg.encode("utf-8"), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, gateway_signature)

    def verify_webhook_signature(
        self,
        webhook_body: str | bytes,
        webhook_signature: str,
        webhook_secret: Optional[str] = None,
    ) -> bool:
        secret = webhook_secret or self.webhook_secret
        if not secret or not webhook_signature:
            return False
        body_bytes = webhook_body if isinstance(webhook_body, bytes) else webhook_body.encode("utf-8")
        expected = hmac.new(secret.encode("utf-8"), body_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, webhook_signature)

    async def fetch_payment(self, payment_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.BASE_URL}/payments/{payment_id}",
                auth=(self.key_id, self.key_secret),
            )
            response.raise_for_status()
            return response.json()


class PaymentProviderFactory:
    """Factory to retrieve active payment provider based on configuration."""

    _override_provider: Optional[PaymentProvider] = None

    @classmethod
    def set_provider(cls, provider: PaymentProvider) -> None:
        """Allow injecting provider instance directly (e.g. for testing)."""
        cls._override_provider = provider

    @classmethod
    def reset(cls) -> None:
        """Reset injected provider."""
        cls._override_provider = None

    @classmethod
    def get_provider(cls, provider_type: Optional[str] = None) -> PaymentProvider:
        if cls._override_provider is not None:
            return cls._override_provider

        ptype = (provider_type or os.getenv("PAYMENT_PROVIDER", "mock")).lower().strip()
        key_id = os.getenv("RAZORPAY_KEY_ID")
        key_secret = os.getenv("RAZORPAY_KEY_SECRET")

        if ptype == "razorpay" and key_id and key_secret:
            return RazorpayPaymentProvider(
                key_id=key_id,
                key_secret=key_secret,
                webhook_secret=os.getenv("RAZORPAY_WEBHOOK_SECRET"),
            )
        # Default safe mock provider
        return MockPaymentProvider()
