import pytest
from agents.validation.integrity import (
    ensure_simulation_mode,
    validate_classification_transition,
    validate_experiment_budget,
    validate_experiment_cost,
    ValidationIntegrityError,
)


def test_transition_unknown_to_verified_without_evidence_rejected():
    """Enforce integrity rule: UNKNOWN cannot become VERIFIED without empirical evidence."""
    with pytest.raises(ValidationIntegrityError, match="Integrity violation"):
        validate_classification_transition(
            previous_classification="UNKNOWN",
            new_classification="VERIFIED",
            evidence_payload=None,
            justification="",
        )

    with pytest.raises(ValidationIntegrityError, match="Integrity violation"):
        validate_classification_transition(
            previous_classification="UNKNOWN",
            new_classification="VERIFIED",
            evidence_payload={},
            justification="I think it works",
        )


def test_transition_not_tested_to_verified_without_evidence_rejected():
    """Enforce integrity rule: NOT_TESTED cannot become VERIFIED without empirical evidence."""
    with pytest.raises(ValidationIntegrityError, match="Integrity violation"):
        validate_classification_transition(
            previous_classification="NOT_TESTED",
            new_classification="VERIFIED",
            evidence_payload={"notes": "No data"},
            justification="looks fine",
        )


def test_transition_with_valid_evidence_succeeds():
    """Transitioning to VERIFIED succeeds when empirical data and justification are provided."""
    valid_payload = {
        "artifact_type": "survey_logs",
        "empirical_data": {"responses": 10, "positive": 5},
        "metric_observed": "50% conversion in simulated trial",
    }
    # Should not raise
    validate_classification_transition(
        previous_classification="UNKNOWN",
        new_classification="VERIFIED",
        evidence_payload=valid_payload,
        justification="Verified through empirical intake survey responses with 50% confirmation rate.",
    )


def test_experiment_budget_guardrail():
    """Verify that experiment budgets exceeding ₹500 are rejected."""
    # Under or at limit
    validate_experiment_budget(500.0, max_allowed=500.0)
    validate_experiment_budget(250.0, max_allowed=500.0)
    validate_experiment_budget(0.0, max_allowed=500.0)

    # Exceeding limit
    with pytest.raises(ValidationIntegrityError, match="Spending guardrail"):
        validate_experiment_budget(501.0, max_allowed=500.0)

    with pytest.raises(ValidationIntegrityError, match="Spending guardrail"):
        validate_experiment_budget(1000.0, max_allowed=500.0)


def test_experiment_cost_guardrail():
    """Verify that actual cost spent cannot exceed allocated budget or ₹500 cap."""
    # Within budget
    validate_experiment_cost(250.0, experiment_budget=300.0, max_allowed=500.0)

    # Exceeds allocated budget
    with pytest.raises(ValidationIntegrityError, match="Spending guardrail"):
        validate_experiment_cost(350.0, experiment_budget=300.0, max_allowed=500.0)

    # Exceeds max cap even if budget was wrongly set high
    with pytest.raises(ValidationIntegrityError, match="Spending guardrail"):
        validate_experiment_cost(600.0, experiment_budget=600.0, max_allowed=500.0)


def test_simulation_safety_enforced():
    """Verify that non-simulation real-world execution is blocked."""
    # Simulation allowed
    ensure_simulation_mode(True)

    # Real world disabled
    with pytest.raises(ValidationIntegrityError, match="Safety invariant"):
        ensure_simulation_mode(False)
