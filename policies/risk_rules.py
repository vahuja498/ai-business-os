import re
from enum import Enum
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    BLOCKED = "BLOCKED"


class RiskEvaluationResult(BaseModel):
    risk_level: RiskLevel
    requires_approval: bool
    reasons: list[str] = Field(default_factory=list)
    prohibited_matches: list[str] = Field(default_factory=list)


# Prohibited keywords and deceptive patterns per Section 10 & 28
PROHIBITED_PATTERNS = [
    r"\bfake\s+(account|identity|document|invoice|review|id|persona|name)\b",
    r"\bfals(e|ify|ified)\s+(claim|document|identity|credential|tax|income|information)\b",
    r"\bfabricat(e|ed|ion|ing)\s+(document|invoice|identity|evidence|data|review)?\b",
    r"\bmanipulat(e|ion|ing)\s+(of\s+)?(government|subsidy|benefit|grant|scheme|incentive)\b",
    r"\b(refund|chargeback)\s+abuse\b",
    r"\b(bypass|circumvent|evade)\s+(platform|security|captcha|auth|control|rule|terms)\b",
    r"\b(unauthorized|hacked|stolen|scam|phishing|fraudulent|fraud)\b",
    r"\bforge(d|ry|ring)\b",
    r"\bdeceptive\s+(activity|marketing|advertising|outreach|practice|claim)\b",
]


class RiskEvaluator:
    @classmethod
    def evaluate_text_and_action(
        cls,
        action_type: str,
        text_content: str = "",
        amount: float | None = None,
        max_auto_amount: float = 0.0,
    ) -> RiskEvaluationResult:
        combined_text = f"{action_type} {text_content}".lower()
        prohibited_matches: list[str] = []

        for pattern in PROHIBITED_PATTERNS:
            if re.search(pattern, combined_text, re.IGNORECASE):
                prohibited_matches.append(pattern)

        if prohibited_matches:
            return RiskEvaluationResult(
                risk_level=RiskLevel.BLOCKED,
                requires_approval=False,
                reasons=["Action triggers prohibited fraud/deception/abuse policy."],
                prohibited_matches=prohibited_matches,
            )

        # High risk actions: financial, contracts, refunds, vendor onboarding, sensitive data
        high_risk_actions = {
            "financial_transaction",
            "contract",
            "refund",
            "new_vendor",
            "high_value_advertising",
            "sensitive_data_access",
            "payment",
            "bank_transfer",
            "legal_agreement",
        }

        reasons: list[str] = []
        is_high = False

        if action_type.lower() in high_risk_actions:
            is_high = True
            reasons.append(f"Action '{action_type}' is designated as HIGH risk.")

        if amount is not None and amount > max_auto_amount:
            is_high = True
            reasons.append(f"Amount {amount} exceeds auto-approval threshold of {max_auto_amount}.")

        if is_high:
            return RiskEvaluationResult(
                risk_level=RiskLevel.HIGH,
                requires_approval=True,
                reasons=reasons,
            )

        # Medium risk actions: routine messaging, marketing content
        medium_risk_actions = {
            "customer_message",
            "marketing_content",
            "low_value_advertising",
            "campaign_launch",
        }
        if action_type.lower() in medium_risk_actions:
            return RiskEvaluationResult(
                risk_level=RiskLevel.MEDIUM,
                requires_approval=False,
                reasons=[f"Action '{action_type}' is classified as MEDIUM risk."],
            )

        # Default to LOW risk
        return RiskEvaluationResult(
            risk_level=RiskLevel.LOW,
            requires_approval=False,
            reasons=["Action is classified as LOW risk (research/analysis/internal update)."],
        )
