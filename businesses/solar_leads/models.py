from pydantic import BaseModel, Field


class SolarLeadDetails(BaseModel):
    property_type: str | None = None  # residential, commercial, industrial
    roof_area_sqft: float | None = None
    monthly_electricity_bill: float | None = None
    city: str | None = None
    pincode: str | None = None
    is_verified: bool = False
    qualification_score: float = 0.0
    notes: list[str] = Field(default_factory=list)
