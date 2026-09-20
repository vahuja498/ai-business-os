import pytest
from agents.research.catalog import CAMPAIGN_CANDIDATES
from agents.validation.engine import ValidationEngine
from agents.validation.integrity import calculate_validation_confidence_score


def test_extract_material_assumptions():
    """Verify that material assumptions are extracted across all core pillars."""
    candidate = CAMPAIGN_CANDIDATES[0]
    assumptions = ValidationEngine.extract_material_assumptions(candidate)

    assert len(assumptions) >= 7
    categories = {a["category"] for a in assumptions}
    assert "DEMAND" in categories
    assert "CAC" in categories
    assert "UNIT_ECONOMICS" in categories
    assert "FULFILMENT" in categories
    assert "AUTOMATION" in categories
    assert "REGULATORY" in categories
    assert "DISINTERMEDIATION" in categories

    for a in assumptions:
        assert a["statement"]
        assert a["classification"] in {"VERIFIED", "SUPPORTED_ESTIMATE", "UNKNOWN", "CONTRADICTED", "NOT_TESTED"}
        assert a["risk_level"] in {"HIGH", "MEDIUM", "LOW"}


def test_highest_risk_assumptions_count():
    """Verify that between 3 and 7 highest-risk assumptions are flagged per opportunity."""
    for candidate in CAMPAIGN_CANDIDATES:
        assumptions = ValidationEngine.extract_material_assumptions(candidate)
        high_risk = [a for a in assumptions if a["is_highest_risk"]]
        assert 3 <= len(high_risk) <= 7, f"Candidate {candidate['title']} has {len(high_risk)} high risk assumptions"


def test_generate_experiments_budget_cap_and_criteria():
    """Verify that generated validation experiments have budget <= ₹500 and well-defined criteria."""
    candidate = CAMPAIGN_CANDIDATES[0]
    assumptions = ValidationEngine.extract_material_assumptions(candidate)
    high_risk = [a for a in assumptions if a["is_highest_risk"]]

    experiments = ValidationEngine.generate_experiments_for_high_risk(candidate, high_risk)

    assert len(experiments) == len(high_risk)
    for exp in experiments:
        assert exp["budget"] <= 500.0, f"Budget {exp['budget']} exceeds ₹500 cap"
        assert exp["budget"] >= 0.0
        assert exp["pass_criteria"]
        assert exp["fail_criteria"]
        assert exp["inconclusive_criteria"]
        assert exp["automated_tasks"]
        assert exp["human_tasks"]
        assert exp["is_simulation"] is True
        assert len(exp["required_evidence"]) > 0


def test_non_comparative_confidence_scoring():
    """Verify confidence score calculation is non-comparative and penalizes unknowns."""
    # Fully verified assumptions
    all_verified = [{"classification": "VERIFIED"} for _ in range(5)]
    score_high = calculate_validation_confidence_score(all_verified)
    assert score_high == 1.0

    # Mixed assumptions
    mixed = [
        {"classification": "VERIFIED"},
        {"classification": "SUPPORTED_ESTIMATE"},
        {"classification": "SUPPORTED_ESTIMATE"},
        {"classification": "UNKNOWN"},
        {"classification": "NOT_TESTED"},
    ]
    score_mixed = calculate_validation_confidence_score(mixed)
    assert 0.0 < score_mixed < 1.0

    # Heavily contradicted and unknown
    negative = [
        {"classification": "CONTRADICTED"},
        {"classification": "CONTRADICTED"},
        {"classification": "UNKNOWN"},
        {"classification": "UNKNOWN"},
    ]
    score_low = calculate_validation_confidence_score(negative)
    assert score_low == 0.0
