from typing import Any
from businesses.core.base_module import BusinessMetadata, BusinessModule


class SolarLeadsModule(BusinessModule):
    """
    Solar Lead Generation Business Module.
    Status remains DRAFT until market research, vendor availability,
    and economics are validated. No real customer outreach allowed in DRAFT.
    """

    def __init__(self, metadata: BusinessMetadata):
        super().__init__(metadata)

    async def discover(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "status": "research_required",
            "message": "Solar market discovery initialized. Requires Research Agent validation of local solar tariffs and vendor demand.",
            "target": context.get("target_region", "General India rooftop solar"),
        }

    async def acquire(self, context: dict[str, Any]) -> dict[str, Any]:
        if self.status == "DRAFT":
            return {
                "status": "blocked",
                "message": "Outreach blocked: Solar module is in DRAFT status. Live acquisition requires validation and human approval.",
            }
        return {"status": "active", "channels": self.metadata.acquisition_channels}

    async def qualify(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        # Qualification rule: minimum electricity bill threshold (e.g. > 1500 INR/month)
        bill = lead_data.get("monthly_electricity_bill", 0.0)
        is_qualified = bill >= 1500.0
        return {
            "qualified": is_qualified,
            "score": 80.0 if is_qualified else 30.0,
            "reason": "Bill meets viability threshold" if is_qualified else "Bill too low for solar ROI",
        }
