from sqlalchemy import Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base, TimestampMixin, UUIDMixin


class Opportunity(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "opportunities"

    business_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("businesses.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    target_market: Mapped[str] = mapped_column(String(255), nullable=True)
    revenue_model: Mapped[str] = mapped_column(String(100), nullable=True)
    estimated_startup_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_customer_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_acquisition_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_fulfilment_cost: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    estimated_margin: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    automation_potential: Mapped[str] = mapped_column(String(50), default="MEDIUM", nullable=False)
    regulatory_complexity: Mapped[str] = mapped_column(String(50), default="LOW", nullable=False)
    platform_dependency: Mapped[str] = mapped_column(String(50), default="LOW", nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), default="LOW", nullable=False)
    evidence: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    assumptions: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    recommended_experiment: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="IDENTIFIED", nullable=False, index=True)
