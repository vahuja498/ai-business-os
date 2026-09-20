import logging
from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.opportunity import Opportunity
from database.models.validation import (
    Assumption,
    EvidenceUpdate,
    ExperimentResult,
    ValidationApproval,
    ValidationBudget,
    ValidationExperiment,
    ValidationPlan,
)
from database.models.audit_log import AuditLog
from agents.validation.integrity import (
    calculate_validation_confidence_score,
    ensure_simulation_mode,
    validate_classification_transition,
    validate_experiment_budget,
    validate_experiment_cost,
    ValidationIntegrityError,
)

logger = logging.getLogger(__name__)


class ValidationEngine:
    """Core validation engine for Phase 5.

    Converts opportunities into structured validation plans, classifies material assumptions,
    identifies the 3-7 highest-risk assumptions, generates micro-experiments (budget <= ₹500),
    and enforces strict non-comparative confidence scoring and evidence integrity.
    """

    @classmethod
    def extract_material_assumptions(cls, opp: Opportunity | dict[str, Any]) -> list[dict[str, Any]]:
        """Extracts 7-10 material assumptions spanning the 7 core business pillars."""
        title = opp.title if isinstance(opp, Opportunity) else opp.get("title", "Business Opportunity")
        customer = (opp.customer if isinstance(opp, Opportunity) else opp.get("customer")) or "Target SME clients"
        unknowns = (opp.unknowns if isinstance(opp, Opportunity) else opp.get("unknowns")) or []
        failure_modes = (opp.failure_modes if isinstance(opp, Opportunity) else opp.get("failure_modes")) or []
        contradicting = (
            opp.contradicting_evidence if isinstance(opp, Opportunity) else opp.get("contradicting_evidence")
        ) or []
        breakdown = (opp.automation_breakdown if isinstance(opp, Opportunity) else opp.get("automation_breakdown")) or {}
        disinter = (
            opp.disintermediation_analysis if isinstance(opp, Opportunity) else opp.get("disintermediation_analysis")
        ) or ""
        reg_notes = (
            opp.regulatory_considerations if isinstance(opp, Opportunity) else opp.get("regulatory_considerations")
        ) or ""

        assumptions: list[dict[str, Any]] = [
            # 1. Demand & Willingness to Pay
            {
                "category": "DEMAND",
                "statement": f"{customer} will pay for {title} rather than using internal staff or free informal options.",
                "classification": "SUPPORTED_ESTIMATE",
                "risk_level": "HIGH",
                "is_highest_risk": True,
                "evidence_notes": "Corroborated by initial search volume and pain point frequency, but unvalidated at scale.",
            },
            # 2. Customer Acquisition Cost
            {
                "category": "CAC",
                "statement": f"Target customers can be acquired at an average CAC <= ₹{getattr(opp, 'estimated_acquisition_cost', 500):.0f} via direct non-paid channels.",
                "classification": "SUPPORTED_ESTIMATE",
                "risk_level": "HIGH",
                "is_highest_risk": True,
                "evidence_notes": "Estimated from standard B2B WhatsApp/email conversion rates in industrial clusters.",
            },
            # 3. Unit Economics & Contribution Margin
            {
                "category": "UNIT_ECONOMICS",
                "statement": f"Fulfilment cost will not exceed ₹{getattr(opp, 'estimated_fulfilment_cost', 300):.0f}, sustaining a unit contribution margin >= {(getattr(opp, 'estimated_margin', 0.7) * 100):.0f}%.",
                "classification": "VERIFIED",
                "risk_level": "MEDIUM",
                "is_highest_risk": False,
                "evidence_notes": "Software delivery costs and template synthesis exhibit negligible variable compute costs.",
            },
            # 4. Fulfilment Burden (Zero physical labor for owner)
            {
                "category": "FULFILMENT",
                "statement": "The business owner will not be required to perform manual physical labor or frequent in-person site visits for fulfilment.",
                "classification": "VERIFIED",
                "risk_level": "LOW",
                "is_highest_risk": False,
                "evidence_notes": f"Operational design mandates digital dispatch and remote desk synthesis: {breakdown.get('human_only', 'Administrative spot checks only')}",
            },
            # 5. Automation Feasibility
            {
                "category": "AUTOMATION",
                "statement": f"At least 70% of the operational workflow can be automated via AI agents and software bots ({getattr(opp, 'automation_potential', 'HIGH')}).",
                "classification": "SUPPORTED_ESTIMATE",
                "risk_level": "MEDIUM",
                "is_highest_risk": False,
                "evidence_notes": f"AI: {breakdown.get('ai_automation', 'N/A')} | Software: {breakdown.get('software_automation', 'N/A')}",
            },
            # 6. Conservative Regulatory Compliance
            {
                "category": "REGULATORY",
                "statement": f"The workflow qualifies strictly as administrative assistance/referral and will not trigger licensing under statutory legal, CA, or broking acts.",
                "classification": "VERIFIED",
                "risk_level": "HIGH",
                "is_highest_risk": True,
                "evidence_notes": reg_notes or "Service restricted to administrative document compilation.",
            },
            # 7. Disintermediation Defensibility
            {
                "category": "DISINTERMEDIATION",
                "statement": f"Buyers and suppliers will not bypass the platform after the first transaction.",
                "classification": "UNKNOWN" if len(disinter) < 20 else "SUPPORTED_ESTIMATE",
                "risk_level": "HIGH",
                "is_highest_risk": True,
                "evidence_notes": disinter or "Disintermediation mechanics require empirical retention testing.",
            },
        ]

        # Add Unknowns as explicit UNKNOWN assumptions
        for idx, unk in enumerate(unknowns[:3]):
            assumptions.append({
                "category": "UNKNOWN_FACTOR",
                "statement": f"Critical Unknown: {unk}",
                "classification": "UNKNOWN",
                "risk_level": "HIGH",
                "is_highest_risk": True,
                "evidence_notes": "Identified as an unverified dependency during Phase 4 discovery.",
            })

        # Add Contradictions / Failure Vectors as CONTRADICTED or HIGH risk assumptions
        for idx, fl in enumerate(failure_modes[:2]):
            assumptions.append({
                "category": "FATAL_FAILURE_RISK",
                "statement": f"Platform can survive the potential failure mode: {fl}",
                "classification": "NOT_TESTED",
                "risk_level": "HIGH",
                "is_highest_risk": True,
                "evidence_notes": "Adversarial failure vector requiring empirical stress testing.",
            })

        # Ensure we flag between 3 and 7 highest-risk assumptions
        high_risk_count = sum(1 for a in assumptions if a["is_highest_risk"])
        if high_risk_count < 3:
            for a in assumptions:
                if not a["is_highest_risk"]:
                    a["is_highest_risk"] = True
                    a["risk_level"] = "HIGH"
                    high_risk_count += 1
                    if high_risk_count >= 3:
                        break
        elif high_risk_count > 7:
            # Demote excess lowest priority items
            demoted = 0
            for a in reversed(assumptions):
                if a["is_highest_risk"] and a["classification"] not in ("UNKNOWN", "CONTRADICTED"):
                    a["is_highest_risk"] = False
                    demoted += 1
                    if (high_risk_count - demoted) <= 7:
                        break

        return assumptions

    @classmethod
    def generate_experiments_for_high_risk(
        cls, opp: Opportunity | dict[str, Any], high_risk_assumptions: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """Generates realistic micro-experiments for highest-risk assumptions with budgets <= ₹500."""
        title = opp.title if isinstance(opp, Opportunity) else opp.get("title", "Opportunity")
        family = opp.opportunity_family if isinstance(opp, Opportunity) else opp.get("opportunity_family", "BUSINESS")
        rec_exp = (opp.recommended_experiment if isinstance(opp, Opportunity) else opp.get("recommended_experiment")) or {}

        experiments: list[dict[str, Any]] = []

        for idx, asm in enumerate(high_risk_assumptions):
            cat = asm.get("category", "GENERAL")
            statement = asm.get("statement", "")

            # Tailor budget strictly <= ₹500
            budget_val = min(float(rec_exp.get("budget", 250.0) or 250.0), 500.0)
            if idx > 0:
                budget_val = round(max(0.0, min(350.0, 100.0 * (idx + 1))), 2)

            validate_experiment_budget(budget_val, max_allowed=500.0)

            exp_item = {
                "title": f"Exp-{idx + 1}: Validate {cat} for {title[:35]}",
                "hypothesis": f"If presented with a clear diagnostic or initial sample, prospective users will confirm: {statement[:120]}",
                "methodology": (
                    f"Conduct a simulated 5-day structured outreach across 10-15 prospective {family} test entities "
                    f"using standard templated inquiry forms without live commercial billing."
                ),
                "pass_criteria": "At least 30% of contacts confirm interest and complete the preliminary intake form.",
                "fail_criteria": "Zero contacts respond or more than 70% cite fatal compliance/switching barriers.",
                "inconclusive_criteria": "10-25% of contacts respond with conditional or ambiguous feedback requiring secondary follow-up.",
                "budget": budget_val,
                "duration_days": 7,
                "required_evidence": [
                    "Simulated response logs",
                    "Completed intake checklist",
                    "Customer friction notes",
                ],
                "automated_tasks": "Automated email/form dispatch, response logging, and keyword classification.",
                "human_tasks": "Manual review of inbound edge cases and review of regulatory disclaimers.",
                "regulatory_requirements": "Mandatory administrative disclaimer: 'Informational analysis only; not statutory legal/tax counsel'.",
                "approval_status": "NOT_REQUESTED",
                "execution_status": "PENDING",
                "is_simulation": True,
            }
            experiments.append(exp_item)

        return experiments

    @classmethod
    async def create_or_update_validation_plan(
        cls, session: AsyncSession, opp: Opportunity
    ) -> ValidationPlan:
        """Constructs a complete ValidationPlan with assumptions, experiments, and budget for an opportunity."""
        # Check if plan already exists
        stmt = select(ValidationPlan).where(ValidationPlan.opportunity_id == opp.id)
        res = await session.execute(stmt)
        plan = res.scalar_one_or_none()

        assumptions_data = cls.extract_material_assumptions(opp)
        high_risk = [a for a in assumptions_data if a.get("is_highest_risk")]
        experiments_data = cls.generate_experiments_for_high_risk(opp, high_risk)

        confidence_score = calculate_validation_confidence_score(assumptions_data)
        total_budget_allocated = sum(e["budget"] for e in experiments_data)

        if not plan:
            plan = ValidationPlan(
                opportunity_id=opp.id,
                status="DRAFT",
                confidence_score=confidence_score,
                total_budget_allocated=total_budget_allocated,
                total_budget_spent=0.0,
                material_assumptions_count=len(assumptions_data),
                high_risk_assumptions_count=len(high_risk),
                completed_experiments_count=0,
                summary=f"Validation plan for '{opp.title}' covering {len(assumptions_data)} material assumptions and {len(experiments_data)} validation experiments.",
                regulatory_approval_required=opp.regulatory_complexity in ("MEDIUM", "HIGH"),
                regulatory_approval_notes=opp.regulatory_considerations or "Standard administrative disclaimer required.",
            )
            session.add(plan)
            await session.flush()

            # Create ValidationBudget
            budget = ValidationBudget(
                validation_plan_id=plan.id,
                max_budget=2500.0,
                allocated_amount=total_budget_allocated,
                spent_amount=0.0,
                currency="INR",
                is_locked=False,
            )
            session.add(budget)
            await session.flush()

            # Create Assumptions
            assumption_models: list[Assumption] = []
            for asm in assumptions_data:
                model = Assumption(
                    validation_plan_id=plan.id,
                    category=asm["category"],
                    statement=asm["statement"],
                    classification=asm["classification"],
                    risk_level=asm["risk_level"],
                    is_highest_risk=asm["is_highest_risk"],
                    evidence_notes=asm["evidence_notes"],
                    initial_classification=asm["classification"],
                )
                session.add(model)
                assumption_models.append(model)
            await session.flush()

            # Create Experiments
            for idx, exp in enumerate(experiments_data):
                linked_asm_id = assumption_models[idx].id if idx < len(assumption_models) else None
                exp_model = ValidationExperiment(
                    validation_plan_id=plan.id,
                    assumption_id=linked_asm_id,
                    title=exp["title"],
                    hypothesis=exp["hypothesis"],
                    methodology=exp["methodology"],
                    pass_criteria=exp["pass_criteria"],
                    fail_criteria=exp["fail_criteria"],
                    inconclusive_criteria=exp["inconclusive_criteria"],
                    budget=exp["budget"],
                    duration_days=exp["duration_days"],
                    required_evidence=exp["required_evidence"],
                    automated_tasks=exp["automated_tasks"],
                    human_tasks=exp["human_tasks"],
                    regulatory_requirements=exp["regulatory_requirements"],
                    approval_status=exp["approval_status"],
                    execution_status=exp["execution_status"],
                    is_simulation=exp["is_simulation"],
                )
                session.add(exp_model)
            await session.flush()

            # Create ValidationApproval if regulatory or budget requires it
            if plan.regulatory_approval_required or total_budget_allocated > 0:
                approval = ValidationApproval(
                    validation_plan_id=plan.id,
                    approval_type="PLAN_EXECUTION",
                    description=f"Validation approval required for '{opp.title}': budget ₹{total_budget_allocated:.2f} and regulatory compliance check.",
                    risk_level="HIGH" if plan.regulatory_approval_required else "MEDIUM",
                    status="PENDING",
                    requested_amount=total_budget_allocated,
                )
                session.add(approval)
                await session.flush()

            # Audit Log entry
            audit = AuditLog(
                actor="ValidationEngine",
                action="CREATE_VALIDATION_PLAN",
                target=plan.id,
                result="SUCCESS",
                metadata_json={
                    "opportunity_id": opp.id,
                    "title": opp.title,
                    "assumptions_count": len(assumptions_data),
                    "high_risk_count": len(high_risk),
                    "confidence_score": confidence_score,
                    "allocated_budget": total_budget_allocated,
                },
            )
            session.add(audit)
        else:
            # Plan exists; recalculate confidence and refresh counts
            plan.confidence_score = confidence_score
            plan.material_assumptions_count = len(assumptions_data)
            plan.high_risk_assumptions_count = len(high_risk)
            plan.total_budget_allocated = total_budget_allocated
            await session.flush()

        return plan

    @classmethod
    async def sync_all_opportunities(cls, session: AsyncSession) -> dict[str, Any]:
        """Syncs all opportunities in the database into structured validation plans."""
        stmt = select(Opportunity)
        res = await session.execute(stmt)
        opps = res.scalars().all()

        created_count = 0
        updated_count = 0
        plans_summary = []

        for opp in opps:
            stmt_check = select(ValidationPlan).where(ValidationPlan.opportunity_id == opp.id)
            existing = (await session.execute(stmt_check)).scalar_one_or_none()

            plan = await cls.create_or_update_validation_plan(session, opp)
            if existing is None:
                created_count += 1
            else:
                updated_count += 1

            plans_summary.append({
                "plan_id": plan.id,
                "opportunity_id": opp.id,
                "title": opp.title,
                "confidence_score": plan.confidence_score,
                "status": plan.status,
                "high_risk_assumptions": plan.high_risk_assumptions_count,
            })

        await session.commit()
        return {
            "total_synced": len(opps),
            "created": created_count,
            "updated": updated_count,
            "plans": plans_summary,
        }

    @classmethod
    async def record_experiment_result(
        cls,
        session: AsyncSession,
        experiment_id: str,
        outcome: str,
        metric_observed: str,
        cost_spent: float,
        evidence_artifacts: list[Any],
        notes: str = "",
        is_simulation: bool = True,
        update_assumption_to: str | None = None,
        justification: str = "",
    ) -> ExperimentResult:
        """Records the execution result of an experiment, validates spending,

        enforces simulation safety, and safely updates linked assumption status.
        """
        # Safety checks
        ensure_simulation_mode(is_simulation)

        stmt_exp = select(ValidationExperiment).where(ValidationExperiment.id == experiment_id)
        exp_res = await session.execute(stmt_exp)
        experiment = exp_res.scalar_one_or_none()
        if not experiment:
            raise ValidationIntegrityError(f"ValidationExperiment '{experiment_id}' not found.")

        # Spending guardrail
        validate_experiment_cost(cost_spent, experiment.budget, max_allowed=500.0)

        result = ExperimentResult(
            experiment_id=experiment.id,
            outcome=outcome.upper(),
            metric_observed=metric_observed,
            evidence_artifacts=evidence_artifacts or [],
            cost_spent=cost_spent,
            notes=notes,
            simulated=is_simulation,
        )
        session.add(result)
        await session.flush()

        # Update experiment execution status
        experiment.execution_status = "COMPLETED"

        # Update ValidationPlan budget and completed experiments count
        stmt_plan = select(ValidationPlan).where(ValidationPlan.id == experiment.validation_plan_id)
        plan = (await session.execute(stmt_plan)).scalar_one_or_none()
        if plan:
            plan.completed_experiments_count += 1
            plan.total_budget_spent += cost_spent

            # Update linked budget record
            stmt_b = select(ValidationBudget).where(ValidationBudget.validation_plan_id == plan.id)
            budget = (await session.execute(stmt_b)).scalar_one_or_none()
            if budget:
                budget.spent_amount += cost_spent

        # If an assumption status update was requested, enforce integrity
        if update_assumption_to and experiment.assumption_id:
            stmt_asm = select(Assumption).where(Assumption.id == experiment.assumption_id)
            assumption = (await session.execute(stmt_asm)).scalar_one_or_none()
            if assumption:
                evidence_payload = {
                    "experiment_id": experiment.id,
                    "result_id": result.id,
                    "outcome": outcome,
                    "metric_observed": metric_observed,
                    "evidence_artifacts": evidence_artifacts,
                }
                validate_classification_transition(
                    previous_classification=assumption.classification,
                    new_classification=update_assumption_to,
                    evidence_payload=evidence_payload,
                    justification=justification or f"Updated following experiment outcome: {outcome}",
                )

                update_log = EvidenceUpdate(
                    assumption_id=assumption.id,
                    experiment_result_id=result.id,
                    previous_classification=assumption.classification,
                    new_classification=update_assumption_to,
                    evidence_payload=evidence_payload,
                    justification=justification or f"Result of experiment '{experiment.title}': {outcome}",
                    verified_by="ValidationEngine",
                )
                session.add(update_log)
                await session.flush()

                assumption.classification = update_assumption_to
                assumption.last_evidence_update_id = update_log.id

                # Recalculate plan confidence score
                stmt_all_asm = select(Assumption).where(Assumption.validation_plan_id == plan.id)
                all_asms = (await session.execute(stmt_all_asm)).scalars().all()
                plan.confidence_score = calculate_validation_confidence_score(all_asms)

        # Audit log
        audit = AuditLog(
            actor="ValidationEngine",
            action="RECORD_EXPERIMENT_RESULT",
            target=result.id,
            result="SUCCESS",
            metadata_json={
                "experiment_id": experiment.id,
                "outcome": outcome,
                "cost_spent": cost_spent,
                "simulated": is_simulation,
            },
        )
        session.add(audit)
        await session.commit()
        return result
