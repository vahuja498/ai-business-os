from abc import ABC, abstractmethod
from typing import Any
from pydantic import BaseModel, Field


class BusinessMetadata(BaseModel):
    business_id: str
    name: str
    description: str
    status: str = "DRAFT"
    configuration: dict[str, Any] = Field(default_factory=dict)
    pricing: dict[str, Any] = Field(default_factory=dict)
    target_customer: str = ""
    acquisition_channels: list[str] = Field(default_factory=list)
    sales_process: dict[str, Any] = Field(default_factory=dict)
    fulfilment_process: dict[str, Any] = Field(default_factory=dict)
    revenue_model: dict[str, Any] = Field(default_factory=dict)
    cost_model: dict[str, Any] = Field(default_factory=dict)
    kpis: list[dict[str, Any]] = Field(default_factory=list)
    policies: dict[str, Any] = Field(default_factory=dict)
    approval_rules: dict[str, Any] = Field(default_factory=dict)


class BusinessModule(ABC):
    def __init__(self, metadata: BusinessMetadata):
        self.metadata = metadata

    @property
    def business_id(self) -> str:
        return self.metadata.business_id

    @property
    def name(self) -> str:
        return self.metadata.name

    @property
    def status(self) -> str:
        return self.metadata.status

    # Standard business capability hooks (default implementations allow opt-in)
    async def discover(self, context: dict[str, Any]) -> dict[str, Any]:
        """Market discovery, opportunity identification, competitive research."""
        return {"status": "not_implemented", "capability": "discover"}

    async def acquire(self, context: dict[str, Any]) -> dict[str, Any]:
        """Lead generation and customer acquisition."""
        return {"status": "not_implemented", "capability": "acquire"}

    async def qualify(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        """Lead scoring and qualification."""
        return {"status": "not_implemented", "capability": "qualify"}

    async def sell(self, opportunity_data: dict[str, Any]) -> dict[str, Any]:
        """Closing, proposal, and checkout."""
        return {"status": "not_implemented", "capability": "sell"}

    async def fulfil(self, order_data: dict[str, Any]) -> dict[str, Any]:
        """Product or service delivery."""
        return {"status": "not_implemented", "capability": "fulfil"}

    async def collect(self, transaction_data: dict[str, Any]) -> dict[str, Any]:
        """Billing, invoicing, and payment collection."""
        return {"status": "not_implemented", "capability": "collect"}

    async def support(self, inquiry_data: dict[str, Any]) -> dict[str, Any]:
        """Customer service and issue resolution."""
        return {"status": "not_implemented", "capability": "support"}

    async def measure(self, metrics_context: dict[str, Any]) -> dict[str, Any]:
        """KPI reporting and performance tracking."""
        return {"status": "not_implemented", "capability": "measure"}

    async def optimise(self, feedback_data: dict[str, Any]) -> dict[str, Any]:
        """Continuous improvement and experimentation."""
        return {"status": "not_implemented", "capability": "optimise"}
