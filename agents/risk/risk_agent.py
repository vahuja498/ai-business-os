from datetime import datetime, timezone
from typing import Any
from agents.core.base_agent import BaseAgent
from agents.core.models import AgentMetadata, AgentRunRecord
from policies.autonomy import AutonomyLevel
from policies.guardrails import FinancialGuardrails
from policies.risk_rules import RiskEvaluator, RiskLevel


class RiskAgent(BaseAgent):
    def __init__(self, model_provider=None, guardrails: FinancialGuardrails | None = None):
        metadata = AgentMetadata(
            name="RiskAgent",
            description="Evaluates proposed actions against legal, platform, fraud, and financial guardrails.",
            capabilities=["risk_assessment", "compliance_check", "fraud_detection", "financial_limits"],
            allowed_tools=["database"],
            system_policy="Zero tolerance for fraud, deceptive identities, or platform abuse. Enforce human approvals.",
            risk_level=RiskLevel.LOW,
            autonomy_level=AutonomyLevel.LEVEL_1_ASSIST,
        )
        super().__init__(metadata=metadata, model_provider=model_provider)
        self.guardrails = guardrails or FinancialGuardrails()

    async def run(
        self,
        input_data: dict[str, Any],
        business_id: str | None = None,
        task_id: str | None = None,
    ) -> AgentRunRecord:
        record = AgentRunRecord(
            agent_id=self.agent_id,
            business_id=business_id,
            task_id=task_id,
            input_data=input_data,
        )

        action_type = input_data.get("action_type", "evaluate_opportunity")
        text_content = input_data.get("description", "")
        amount = input_data.get("amount")

        record.actions.append(f"Evaluating risk for action '{action_type}'")

        # 1. Evaluate against anti-fraud and risk policies
        eval_result = RiskEvaluator.evaluate_text_and_action(
            action_type=action_type,
            text_content=text_content,
            amount=amount,
            max_auto_amount=self.guardrails.max_transaction_amount,
        )

        record.outputs["risk_evaluation"] = eval_result.model_dump()

        if eval_result.risk_level == RiskLevel.BLOCKED:
            record.errors.append(f"Blocked action: {', '.join(eval_result.reasons)}")
            record.final_status = "FAILED"
            record.completed_at = datetime.now(timezone.utc)
            return record

        # 2. Check if an approval request is required
        # For business opportunities, starting an experiment with budget requires human sign-off
        requires_approval = eval_result.requires_approval or (amount is not None and amount > 0) or action_type == "launch_experiment"

        if requires_approval:
            approval_request = {
                "business_id": business_id,
                "agent_id": self.agent_id,
                "task_id": task_id,
                "action_type": action_type,
                "description": f"Approval requested for {action_type}: {text_content}",
                "risk_level": eval_result.risk_level.value if eval_result.risk_level != RiskLevel.LOW else "HIGH",
                "amount": amount,
                "reason": "Action involves financial budget allocation or elevated operational risk.",
                "evidence": input_data.get("evidence", []),
                "status": "PENDING",
            }
            record.approval_requests.append(approval_request)
            record.outputs["requires_human_approval"] = True
            record.outputs["approval_request"] = approval_request
            record.actions.append("Generated human approval request.")
        else:
            record.outputs["requires_human_approval"] = False
            record.actions.append("Action cleared automatically under LOW/MEDIUM risk policy.")

        record.completed_at = datetime.now(timezone.utc)
        record.final_status = "SUCCESS"
        return record
