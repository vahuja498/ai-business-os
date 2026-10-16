import uuid
from typing import Any
from businesses.core.base_module import BusinessMetadata, BusinessModule
from businesses.msme_compliance.config import MSMEComplianceConfig
from businesses.msme_compliance.toolkit_generator import MSMEToolkitGenerator
from tools.finance.payment_provider import PaymentProviderFactory


class MSMEComplianceModule(BusinessModule):
    """
    Live Production Business Module:
    Candidate #19: MSME Section 43B(h) 45-Day Payment Compliance & Audit Toolkit.
    Offers automated digital audit and legal compliance toolkits for Indian SMEs,
    CFOs, and Chartered Accountants.
    """

    def __init__(self, metadata: BusinessMetadata | None = None):
        if metadata is None:
            config = MSMEComplianceConfig()
            metadata = BusinessMetadata(
                business_id="biz_msme_compliance_43bh",
                name="MSME Section 43B(h) Compliance Toolkit",
                description="Statutory payment compliance and audit toolkit for Indian enterprises and Chartered Accountants.",
                status="ACTIVE",
                configuration=config.model_dump(),
                pricing={
                    "starter_single_firm_inr": 1999.0,
                    "pro_ca_multi_firm_inr": 3999.0,
                    "currency": "INR",
                },
                target_customer=config.target_customer,
                acquisition_channels=[
                    "organic_b2b_seo",
                    "chartered_accountant_communities",
                    "cfo_linkedin_outreach",
                    "google_search_tax_audit_keywords",
                ],
                sales_process={"model": "instant_self_checkout", "gateway": "razorpay_upi"},
                fulfilment_process={"model": "instant_digital_delivery", "format": "zip_bundle"},
                revenue_model={"type": "one_time_digital_product_sale", "margin_target": 0.92},
                cost_model={"gateway_fee_percent": 2.0, "hosting_and_delivery_inr": 10.0},
                kpis=[{"metric": k, "target": "industry_benchmark"} for k in config.kpis],
            )
        super().__init__(metadata)

    async def discover(self, context: dict[str, Any]) -> dict[str, Any]:
        region = context.get("target_region", "India (Delhi-NCR / Haryana / Pan-India)")
        return {
            "status": "market_active",
            "market_size_msme_india": "63+ Million enterprises",
            "statutory_driver": "Income Tax Act Section 43B(h) disallowance mandatory from AY 2024-25 onwards",
            "target_geography": region,
            "demand_urgency": "High during annual tax audit (Sept/Oct) and FY closing (March/April)",
            "competitive_position": "Self-serve ₹1,999 vs. Big 4 / bespoke legal advisory ₹25,000+",
        }

    async def acquire(self, context: dict[str, Any]) -> dict[str, Any]:
        """Customer acquisition plan and active channel metrics."""
        return {
            "status": "active",
            "acquisition_channels": self.metadata.acquisition_channels,
            "campaign_focus": "Section 43B(h) tax disallowance calculator & vendor declaration template",
            "allowed_daily_budget_inr": context.get("daily_budget", 500.0),
        }

    async def qualify(self, lead_data: dict[str, Any]) -> dict[str, Any]:
        """
        Qualify potential buyers:
        - Must be an Indian business entity or practicing tax professional.
        - Turnover > 0 or has micro/small vendors.
        """
        turnover_inr = lead_data.get("annual_turnover_inr", 0.0)
        has_micro_suppliers = lead_data.get("purchases_from_msme", True)
        is_tax_consultant = lead_data.get("is_chartered_accountant", False)

        qualified = has_micro_suppliers or is_tax_consultant or turnover_inr >= 1000000.0
        score = 90.0 if (has_micro_suppliers and turnover_inr > 5000000.0) else (75.0 if qualified else 35.0)

        recommended_tier = "MSME-43BH-PRO-CA" if is_tax_consultant else "MSME-43BH-STARTER"

        return {
            "qualified": qualified,
            "score": score,
            "recommended_sku": recommended_tier,
            "reason": (
                "Entity has MSME vendor exposure and required statutory compliance"
                if qualified
                else "Insufficient exposure to MSME supply chain"
            ),
        }

    async def sell(self, opportunity_data: dict[str, Any]) -> dict[str, Any]:
        """
        Execute digital checkout: initiates a real or mock payment gateway order.
        """
        sku = opportunity_data.get("sku", "MSME-43BH-STARTER")
        price = 3999.0 if "PRO" in sku.upper() else 1999.0
        customer_email = opportunity_data.get("email", "buyer@example.com")
        customer_name = opportunity_data.get("name", "Finance Head")

        provider = PaymentProviderFactory.get_provider()
        receipt_id = f"rcpt_{uuid.uuid4().hex[:8]}"

        order = await provider.create_order(
            amount_inr=price,
            currency="INR",
            receipt=receipt_id,
            notes={
                "business_id": self.business_id,
                "sku": sku,
                "buyer_name": customer_name,
                "buyer_email": customer_email,
            },
        )

        return {
            "status": "checkout_ready",
            "order_id": order.id,
            "amount_inr": order.amount,
            "amount_paise": order.amount_paise,
            "currency": order.currency,
            "gateway": order.gateway,
            "key_id": order.key_id,
            "sku": sku,
            "receipt": order.receipt,
        }

    async def fulfil(self, order_data: dict[str, Any]) -> dict[str, Any]:
        """
        Deliver digital toolkit bundle:
        Generates secure download token and deliverable manifest.
        """
        company_name = order_data.get("company_name", "Corporate Buyer")
        sku = order_data.get("sku", "MSME-43BH-STARTER")
        download_token = f"dl_{uuid.uuid4().hex}"

        manifest = MSMEToolkitGenerator.get_template_manifest()

        return {
            "status": "fulfilled",
            "download_token": download_token,
            "download_endpoint": f"/api/public/orders/download?token={download_token}",
            "sku": sku,
            "company_name": company_name,
            "delivered_files": manifest,
            "message": "Section 43B(h) Audit Compliance Toolkit generated successfully.",
        }

    async def collect(self, transaction_data: dict[str, Any]) -> dict[str, Any]:
        """
        Record financial collection with statutory Indian GST accounting (18% SAC 998311).
        """
        gross_amount = float(transaction_data.get("amount", 1999.0))
        # SAC 998311 Management Consulting / Legal Documents: 18% GST included or added
        gst_rate = 0.18
        base_revenue = round(gross_amount / (1.0 + gst_rate), 2)
        gst_component = round(gross_amount - base_revenue, 2)

        return {
            "status": "recorded",
            "gross_amount_inr": gross_amount,
            "base_revenue_inr": base_revenue,
            "gst_collected_inr": gst_component,
            "gst_sac_code": "998311",
            "transaction_reference": transaction_data.get("reference", f"tx_{uuid.uuid4().hex[:8]}"),
            "ledger_account": "Digital Product Sales - MSME Compliance",
        }
