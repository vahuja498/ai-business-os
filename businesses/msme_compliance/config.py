from typing import Any
from pydantic import BaseModel, Field


class MSMECompliancePricingTier(BaseModel):
    sku: str
    name: str
    price_inr: float
    description: str
    deliverables: list[str]


class MSMEComplianceConfig(BaseModel):
    module_name: str = "msme_compliance"
    version: str = "1.0.0"
    status: str = "ACTIVE"
    target_geography: str = "India (Delhi-NCR, Faridabad, Haryana, Pan-India MSME & Corporate Hubs)"
    target_customer: str = (
        "SME Founders, CFOs, Accounts Heads, and Practicing Chartered Accountants "
        "managing payments to micro and small vendors under Section 43B(h) of the Income Tax Act."
    )
    statutory_reference: str = (
        "Section 43B(h) of Income Tax Act, 1961 read with Section 15 and 16 of the MSMED Act, 2006."
    )
    pricing_tiers: list[MSMECompliancePricingTier] = Field(
        default_factory=lambda: [
            MSMECompliancePricingTier(
                sku="MSME-43BH-STARTER",
                name="MSME 43B(h) Enterprise Compliance Toolkit (Single Firm)",
                price_inr=1999.0,
                description="Complete audit-ready compliance package for corporate buyers and SMEs.",
                deliverables=[
                    "Vendor Udyam Classification & Declaration Template",
                    "45-Day Payment Term Written Agreement Addendum",
                    "Section 43B(h) Audit & Disallowance Tracking Sheet (Excel/CSV)",
                    "Statutory Interest Calculator SOP under Section 16 MSMED Act",
                    "CFO Action Guide: FY 2024-25 Tax Disallowance Prevention",
                ],
            ),
            MSMECompliancePricingTier(
                sku="MSME-43BH-PRO-CA",
                name="Chartered Accountant Multi-Client Audit & Advisory License",
                price_inr=3999.0,
                description="Commercial re-use license for CAs and Tax Consultants advising multiple corporate clients.",
                deliverables=[
                    "All deliverables in Starter Edition",
                    "Multi-Client Audit Checklist & Client Onboarding SOP",
                    "Customizable Firm Letterhead Templates",
                    "Tax Audit Report Form 3CD Clause 22 Disclosure Guide",
                    "Vendor Verification Script & Automation Workflow",
                ],
            ),
        ]
    )
    kpis: list[str] = Field(
        default_factory=lambda: [
            "organic_conversion_rate",
            "average_order_value_inr",
            "fulfilment_latency_seconds",
            "refund_rate",
            "net_contribution_margin",
        ]
    )
