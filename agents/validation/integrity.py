from typing import Any


class ValidationIntegrityError(Exception):
    """Raised when an operation violates validation engine safety or integrity rules."""
    pass


def validate_classification_transition(
    previous_classification: str,
    new_classification: str,
    evidence_payload: dict[str, Any] | None,
    justification: str = "",
) -> None:
    """Enforces the integrity invariant:

    Never convert UNKNOWN or NOT_TESTED into VERIFIED without new, verifiable empirical evidence.
    """
    prev = (previous_classification or "NOT_TESTED").upper()
    nxt = (new_classification or "NOT_TESTED").upper()

    valid_classifications = {"VERIFIED", "SUPPORTED_ESTIMATE", "UNKNOWN", "CONTRADICTED", "NOT_TESTED"}
    if nxt not in valid_classifications:
        raise ValidationIntegrityError(
            f"Invalid target classification '{nxt}'. Must be one of {valid_classifications}."
        )

    # Core integrity rule: UNKNOWN, NOT_TESTED, or unverified states cannot become VERIFIED without empirical evidence
    if nxt == "VERIFIED" and prev != "VERIFIED":
        if not evidence_payload or not isinstance(evidence_payload, dict) or len(evidence_payload) == 0:
            raise ValidationIntegrityError(
                f"Integrity violation: Cannot transition assumption from '{prev}' to 'VERIFIED' without new empirical evidence."
            )
        # Check that evidence payload contains meaningful non-empty empirical content
        has_empirical_evidence = (
            bool(evidence_payload.get("evidence_artifacts"))
            or bool(evidence_payload.get("empirical_data"))
            or bool(evidence_payload.get("sources"))
            or bool(evidence_payload.get("data_points"))
            or bool(evidence_payload.get("artifact_type"))
        )
        if not has_empirical_evidence:
            raise ValidationIntegrityError(
                "Integrity violation: Evidence payload must contain verified empirical data points, sources, or evidence artifacts."
            )
        if not justification or len(justification.strip()) < 10:
            raise ValidationIntegrityError(
                "Integrity violation: Transitioning to VERIFIED requires a comprehensive justification (>= 10 characters)."
            )

    # Cannot transition CONTRADICTED to VERIFIED without detailed empirical rebuttal
    if nxt == "VERIFIED" and prev == "CONTRADICTED":
        if not evidence_payload or "rebuttal_evidence" not in evidence_payload:
            raise ValidationIntegrityError(
                "Integrity violation: Cannot resolve a CONTRADICTED assumption to VERIFIED without explicit rebuttal evidence."
            )


def validate_experiment_budget(budget: float, max_allowed: float = 500.0) -> None:
    """Enforces experiment-level spending limit of <= ₹500."""
    if budget is None or budget < 0.0:
        raise ValidationIntegrityError("Experiment budget must be a non-negative number.")
    if budget > max_allowed:
        raise ValidationIntegrityError(
            f"Spending guardrail triggered: Experiment budget ₹{budget:.2f} exceeds maximum allowed limit of ₹{max_allowed:.2f}."
        )


def validate_experiment_cost(cost: float, experiment_budget: float, max_allowed: float = 500.0) -> None:
    """Enforces that actual experiment expenditure does not exceed budget or ₹500 cap."""
    if cost is None or cost < 0.0:
        raise ValidationIntegrityError("Experiment cost cannot be negative.")
    effective_limit = min(experiment_budget, max_allowed)
    if cost > effective_limit:
        raise ValidationIntegrityError(
            f"Spending guardrail triggered: Incurred cost ₹{cost:.2f} exceeds allocated experiment budget ₹{effective_limit:.2f}."
        )


def ensure_simulation_mode(is_simulation: bool) -> None:
    """Safety guardrail: Real-world external execution is disabled by default."""
    if not is_simulation:
        raise ValidationIntegrityError(
            "Safety invariant: Real-world external customer/vendor execution is disabled. Experiments must run in simulation mode."
        )


def calculate_validation_confidence_score(assumptions: list[Any]) -> float:
    """Calculates non-comparative validation confidence score (0.0 to 1.0).

    Formulation depends strictly on this specific opportunity's internal assumptions:
    - VERIFIED: +1.0
    - SUPPORTED_ESTIMATE: +0.6
    - NOT_TESTED: +0.1
    - UNKNOWN: -0.25 (penalty on denominator)
    - CONTRADICTED: -0.50 (heavy penalty)

    Never ranks or compares opportunities against each other.
    """
    if not assumptions:
        return 0.0

    n_verified = 0
    n_supported = 0
    n_not_tested = 0
    n_unknown = 0
    n_contradicted = 0
    n_total = len(assumptions)

    for item in assumptions:
        cls_val = getattr(item, "classification", None) or (
            item.get("classification") if isinstance(item, dict) else "NOT_TESTED"
        )
        cls_val = (cls_val or "NOT_TESTED").upper()
        if cls_val == "VERIFIED":
            n_verified += 1
        elif cls_val == "SUPPORTED_ESTIMATE":
            n_supported += 1
        elif cls_val == "UNKNOWN":
            n_unknown += 1
        elif cls_val == "CONTRADICTED":
            n_contradicted += 1
        else:
            n_not_tested += 1

    pos_score = (1.0 * n_verified) + (0.6 * n_supported) + (0.1 * n_not_tested)
    penalty = (0.5 * n_contradicted) + (0.25 * n_unknown)
    effective_denom = n_total + (0.5 * n_unknown)

    if effective_denom <= 0:
        return 0.0

    raw_score = (pos_score - penalty) / effective_denom
    clamped = max(0.0, min(1.0, raw_score))
    return round(clamped, 3)
