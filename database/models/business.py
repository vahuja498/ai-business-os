from sqlalchemy import ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base, TimestampMixin, UUIDMixin


class Business(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "businesses"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False, index=True)
    module_name: Mapped[str] = mapped_column(String(100), default="core", nullable=False)

    config: Mapped["BusinessConfig"] = relationship(
        "BusinessConfig",
        back_populates="business",
        uselist=False,
        cascade="all, delete-orphan",
    )


class BusinessConfig(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "business_configs"

    business_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_customer: Mapped[str] = mapped_column(Text, nullable=True)
    pricing: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    acquisition_channels: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    sales_process: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    fulfilment_process: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    revenue_model: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    cost_model: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    kpis: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    policies: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    approval_rules: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)

    business: Mapped["Business"] = relationship("Business", back_populates="config")
