from typing import Any
from pydantic import BaseModel, Field


class SolarLeadConfig(BaseModel):
    module_name: str = "solar_leads"
    version: str = "0.1.0"
    status: str = "DRAFT"
    target_geography: str = "Unspecified - Requires Research"
    target_customer: str = "Residential and commercial rooftop owners (to be validated)"
    pricing_model: dict[str, Any] = Field(
        default_factory=lambda: {
            "type": "pay_per_qualified_lead",
            "currency": "INR",
            "target_lead_price": None,  # Must be determined via market research
        }
    )
    acquisition_channels: list[str] = Field(
        default_factory=lambda: ["organic_search", "inbound_content", "local_partnerships"]
    )
    kpis: list[str] = Field(
        default_factory=lambda: [
            "cost_per_lead",
            "lead_to_quote_rate",
            "quote_to_install_rate",
            "net_margin",
        ]
    )
