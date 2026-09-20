import os
from pydantic import BaseModel, Field


class FinancialGuardrails(BaseModel):
    max_daily_spend: float = Field(
        default_factory=lambda: float(os.getenv("MAX_DAILY_SPEND", 500.0))
    )
    max_transaction_amount: float = Field(
        default_factory=lambda: float(os.getenv("MAX_TRANSACTION_AMOUNT", 1000.0))
    )
    max_monthly_spend: float = Field(
        default_factory=lambda: float(os.getenv("MAX_MONTHLY_SPEND", 10000.0))
    )
    min_margin: float = Field(
        default_factory=lambda: float(os.getenv("MIN_MARGIN", 0.20))
    )
    min_cash_reserve: float = Field(
        default_factory=lambda: float(os.getenv("MIN_CASH_RESERVE", 5000.0))
    )

    def validate_transaction(self, amount: float) -> tuple[bool, str | None]:
        """Returns (is_allowed_automatically, reason_if_not)"""
        if amount > self.max_transaction_amount:
            return False, f"Transaction amount {amount} exceeds max single transaction limit of {self.max_transaction_amount}"
        return True, None

    def validate_margin(self, margin: float) -> tuple[bool, str | None]:
        if margin < self.min_margin:
            return False, f"Estimated margin {margin:.1%} is below minimum required margin of {self.min_margin:.1%}"
        return True, None
