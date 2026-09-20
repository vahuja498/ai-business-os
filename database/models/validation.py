from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base, TimestampMixin, UUIDMixin


class ValidationPlan(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "validation_plans"

    opportunity_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False, index=True)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_budget_allocated: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    total_budget_spent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    material_assumptions_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    high_risk_assumptions_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_experiments_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    summary: Mapped[str] = mapped_column(Text, default="", nullable=False)
    regulatory_approval_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    regulatory_approval_notes: Mapped[str] = mapped_column(Text, default="", nullable=False)

    # Relationships
    assumptions: Mapped[list["Assumption"]] = relationship(
        "Assumption", back_populates="validation_plan", cascade="all, delete-orphan"
    )
    experiments: Mapped[list["ValidationExperiment"]] = relationship(
        "ValidationExperiment", back_populates="validation_plan", cascade="all, delete-orphan"
    )
    approvals: Mapped[list["ValidationApproval"]] = relationship(
        "ValidationApproval", back_populates="validation_plan", cascade="all, delete-orphan"
    )
    budget: Mapped["ValidationBudget"] = relationship(
        "ValidationBudget", back_populates="validation_plan", uselist=False, cascade="all, delete-orphan"
    )


class Assumption(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "assumptions"

    validation_plan_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("validation_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    classification: Mapped[str] = mapped_column(
        String(50), default="NOT_TESTED", nullable=False, index=True
    )
    risk_level: Mapped[str] = mapped_column(String(20), default="MEDIUM", nullable=False, index=True)
    is_highest_risk: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, index=True)
    evidence_notes: Mapped[str] = mapped_column(Text, default="", nullable=False)
    initial_classification: Mapped[str] = mapped_column(String(50), default="NOT_TESTED", nullable=False)
    last_evidence_update_id: Mapped[str] = mapped_column(String(36), nullable=True)

    # Relationships
    validation_plan: Mapped["ValidationPlan"] = relationship("ValidationPlan", back_populates="assumptions")
    experiments: Mapped[list["ValidationExperiment"]] = relationship(
        "ValidationExperiment", back_populates="assumption"
    )
    evidence_updates: Mapped[list["EvidenceUpdate"]] = relationship(
        "EvidenceUpdate", back_populates="assumption", cascade="all, delete-orphan"
    )


class ValidationExperiment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "validation_experiments"

    validation_plan_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("validation_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    assumption_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("assumptions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    hypothesis: Mapped[str] = mapped_column(Text, nullable=False)
    methodology: Mapped[str] = mapped_column(Text, nullable=False)
    pass_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    fail_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    inconclusive_criteria: Mapped[str] = mapped_column(Text, nullable=False)
    budget: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, default=7, nullable=False)
    required_evidence: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    automated_tasks: Mapped[str] = mapped_column(Text, default="", nullable=False)
    human_tasks: Mapped[str] = mapped_column(Text, default="", nullable=False)
    regulatory_requirements: Mapped[str] = mapped_column(Text, default="", nullable=False)
    approval_status: Mapped[str] = mapped_column(
        String(50), default="NOT_REQUESTED", nullable=False, index=True
    )
    execution_status: Mapped[str] = mapped_column(
        String(50), default="PENDING", nullable=False, index=True
    )
    is_simulation: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    validation_plan: Mapped["ValidationPlan"] = relationship("ValidationPlan", back_populates="experiments")
    assumption: Mapped["Assumption"] = relationship("Assumption", back_populates="experiments")
    results: Mapped[list["ExperimentResult"]] = relationship(
        "ExperimentResult", back_populates="experiment", cascade="all, delete-orphan"
    )
    approvals: Mapped[list["ValidationApproval"]] = relationship(
        "ValidationApproval", back_populates="experiment"
    )


class ExperimentResult(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "experiment_results"

    experiment_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("validation_experiments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    outcome: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # PASS, FAIL, INCONCLUSIVE
    metric_observed: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_artifacts: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    cost_spent: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    notes: Mapped[str] = mapped_column(Text, default="", nullable=False)
    executed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    simulated: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    experiment: Mapped["ValidationExperiment"] = relationship(
        "ValidationExperiment", back_populates="results"
    )
    evidence_updates: Mapped[list["EvidenceUpdate"]] = relationship(
        "EvidenceUpdate", back_populates="experiment_result"
    )


class EvidenceUpdate(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "evidence_updates"

    assumption_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("assumptions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    experiment_result_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("experiment_results.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    previous_classification: Mapped[str] = mapped_column(String(50), nullable=False)
    new_classification: Mapped[str] = mapped_column(String(50), nullable=False)
    evidence_payload: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    justification: Mapped[str] = mapped_column(Text, nullable=False)
    verified_by: Mapped[str] = mapped_column(String(100), default="ValidationEngine", nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    assumption: Mapped["Assumption"] = relationship("Assumption", back_populates="evidence_updates")
    experiment_result: Mapped["ExperimentResult"] = relationship(
        "ExperimentResult", back_populates="evidence_updates"
    )


class ValidationApproval(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "validation_approvals"

    validation_plan_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("validation_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    experiment_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("validation_experiments.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    approval_type: Mapped[str] = mapped_column(
        String(100), default="EXPERIMENT_BUDGET", nullable=False, index=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), default="HIGH", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="PENDING", nullable=False, index=True)
    requested_amount: Mapped[float] = mapped_column(Float, nullable=True)
    approved_by: Mapped[str] = mapped_column(String(100), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationships
    validation_plan: Mapped["ValidationPlan"] = relationship("ValidationPlan", back_populates="approvals")
    experiment: Mapped["ValidationExperiment"] = relationship("ValidationExperiment", back_populates="approvals")


class ValidationBudget(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "validation_budgets"

    validation_plan_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("validation_plans.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    max_budget: Mapped[float] = mapped_column(Float, default=2500.0, nullable=False)
    allocated_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    spent_amount: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="INR", nullable=False)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    validation_plan: Mapped["ValidationPlan"] = relationship("ValidationPlan", back_populates="budget")
