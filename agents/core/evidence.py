import uuid
from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class FindingClassification(str, Enum):
    FACT = "FACT"
    CLAIM = "CLAIM"
    ESTIMATE = "ESTIMATE"
    ASSUMPTION = "ASSUMPTION"
    UNVERIFIED = "UNVERIFIED"


class Finding(BaseModel):
    finding_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    opportunity_id: str | None = None
    source_url: str
    source_title: str
    source_domain: str
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    publication_date: str | None = None
    classification: FindingClassification
    content_summary: str
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        return round(float(v), 3)

    @classmethod
    def create_and_verify(
        cls,
        source_url: str,
        source_title: str,
        source_domain: str,
        classification: FindingClassification | str,
        content_summary: str,
        confidence: float = 0.8,
        publication_date: str | None = None,
        opportunity_id: str | None = None,
    ) -> "Finding":
        if isinstance(classification, str):
            classification = FindingClassification(classification.upper())

        # Section 3 Rule: Never convert estimate/claim into fact
        # If the summary contains estimation keywords, prevent classifying as FACT
        estimate_keywords = ["estimate", "projected", "forecast", "approx", "assume", "claimed", "believed"]
        if classification == FindingClassification.FACT:
            lower_summary = content_summary.lower()
            for kw in estimate_keywords:
                if kw in lower_summary:
                    raise ValueError(
                        f"Integrity error: Cannot classify evidence containing estimate keyword '{kw}' as FACT. Must remain ESTIMATE or CLAIM."
                    )

        return cls(
            opportunity_id=opportunity_id,
            source_url=source_url,
            source_title=source_title,
            source_domain=source_domain,
            publication_date=publication_date,
            classification=classification,
            content_summary=content_summary,
            confidence=confidence,
        )
