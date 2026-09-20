from policies.guardrails import FinancialGuardrails
from policies.risk_rules import RiskEvaluator, RiskLevel


def test_blocked_fraud_patterns():
    blocked_examples = [
        ("generate_leads", "Use a fake identity to scrape portal listings"),
        ("document_creation", "Generate a fabricated document for verification"),
        ("claim_incentive", "Perform manipulation of government subsidy benefit"),
        ("checkout", "Execute refund abuse on merchant accounts"),
        ("security_action", "Bypass platform security controls to accelerate delivery"),
    ]

    for action_type, text in blocked_examples:
        res = RiskEvaluator.evaluate_text_and_action(action_type=action_type, text_content=text)
        assert res.risk_level == RiskLevel.BLOCKED
        assert res.requires_approval is False
        assert len(res.prohibited_matches) > 0


def test_high_risk_actions():
    high_risk_actions = [
        "financial_transaction",
        "contract",
        "refund",
        "new_vendor",
        "legal_agreement",
    ]

    for action in high_risk_actions:
        res = RiskEvaluator.evaluate_text_and_action(action_type=action, text_content="Standard transaction")
        assert res.risk_level == RiskLevel.HIGH
        assert res.requires_approval is True


def test_financial_guardrails():
    guardrails = FinancialGuardrails(max_transaction_amount=1000.0, min_margin=0.20)

    # Valid transaction
    allowed, reason = guardrails.validate_transaction(500.0)
    assert allowed is True
    assert reason is None

    # Exceeding transaction
    allowed, reason = guardrails.validate_transaction(1500.0)
    assert allowed is False
    assert "exceeds max single transaction limit" in reason

    # Margin check
    margin_ok, m_reason = guardrails.validate_margin(0.35)
    assert margin_ok is True

    margin_low, m_reason = guardrails.validate_margin(0.12)
    assert margin_low is False
    assert "below minimum required margin" in m_reason
