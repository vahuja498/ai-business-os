from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base, TimestampMixin, UUIDMixin


class Agent(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agents"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    capabilities: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    allowed_tools: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    system_policy: Mapped[str] = mapped_column(Text, nullable=True)
    business_scope: Mapped[str] = mapped_column(String(100), nullable=True)
    execution_mode: Mapped[str] = mapped_column(String(50), default="AUTONOMOUS", nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), default="LOW", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="IDLE", nullable=False)

    runs: Mapped[list["AgentRun"]] = relationship("AgentRun", back_populates="agent", cascade="all, delete-orphan")


class AgentRun(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "agent_runs"

    agent_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("agents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id: Mapped[str] = mapped_column(String(36), nullable=True, index=True)
    business_id: Mapped[str] = mapped_column(String(36), nullable=True, index=True)
    input_data: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    actions: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    tool_calls: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    outputs: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    errors: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    approval_requests: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    final_status: Mapped[str] = mapped_column(String(50), default="PENDING", nullable=False, index=True)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    agent: Mapped["Agent"] = relationship("Agent", back_populates="runs")
