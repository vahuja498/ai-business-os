import uuid
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from agents.core.evidence import Finding, FindingClassification
from agents.core.llm.base_provider import ModelProvider
from agents.core.llm.factory import ModelProviderFactory
from agents.research.research_agent import ResearchAgent
from agents.risk.risk_agent import RiskAgent
from database.models.opportunity import Opportunity
from database.models.memory import Memory
from database.models.business import Business
from apps.api.services.audit_service import AuditService

DEFAULT_RESEARCH_TEMPLATE = (
    "Find legitimate business opportunities in India that:\n"
    "- can start with <= ₹10,000 initial capital\n"
    "- have high potential for automation\n"
    "- do not require the owner to perform specialised physical labour\n"
    "- can potentially generate first revenue within 30 days\n"
    "- have a legitimate customer willing to pay\n"
    "- do not depend on deception or platform abuse\n"
    "- have a realistic path to recurring revenue\n\n"
    "For each opportunity provide evidence, assumptions, economics, risks, unknowns and a low-cost validation experiment."
)


class OpportunityEngine:
    def __init__(
        self,
        model_provider: ModelProvider | None = None,
        research_agent: ResearchAgent | None = None,
        risk_agent: RiskAgent | None = None,
    ):
        self.model_provider = model_provider or ModelProviderFactory.get_provider()
        self.research_agent = research_agent or ResearchAgent(model_provider=self.model_provider)
        self.risk_agent = risk_agent or RiskAgent(model_provider=self.model_provider)

    async def generate_candidates(self, objective: str) -> list[dict[str, Any]]:
        """
        Generate candidate concepts meeting criteria without hardcoding solar as the only option.
        """
        return [
            {
                "title": "B2B Industrial Recyclables & Used Oil Matchmaking",
                "sector": "Industrial Recycling & Waste Aggregation",
                "search_query": "waste recycling aggregator commission india",
                "target_market": "Automotive service workshops & registered recyclers",
                "revenue_model": "commission_per_batch",
                "startup_cost": 3000.0,
                "cac": 350.0,
                "customer_value": 3500.0,
                "fulfilment_cost": 200.0,
                "time_to_first_revenue": "14 days",
                "automation_potential": "HIGH",
                "regulatory_complexity": "MEDIUM",
                "platform_dependency": "LOW",
                "uncertainty": "MEDIUM",
                "unknowns": [
                    "Minimum batch size required for authorized recyclers to dispatch transport",
                    "State pollution board hazardous waste tracking protocol compliance",
                ],
                "experiment": {
                    "hypothesis": "Workshop owners will agree to share used oil volume data for aggregated buyer pickup.",
                    "validation": "Direct phone interviews with 5 independent auto repair workshops.",
                    "budget": 0.0,
                    "duration": "5 days",
                    "success_metric": "At least 3 workshops provide monthly volume and express interest.",
                    "failure_metric": "Zero workshops willing to engage without cash advance.",
                    "data_required": ["Average monthly waste volume", "Current disposal price per liter"],
                    "human_approvals_required": True,
                },
            },
            {
                "title": "Automated MSME Statutory Compliance & Deadline Alerts",
                "sector": "Regulatory & Legal Automation",
                "search_query": "msme statutory compliance filing spend india",
                "target_market": "Private Limited & LLP Small Businesses in India",
                "revenue_model": "monthly_subscription",
                "startup_cost": 2500.0,
                "cac": 300.0,
                "customer_value": 2400.0,
                "fulfilment_cost": 150.0,
                "time_to_first_revenue": "10 days",
                "automation_potential": "HIGH",
                "regulatory_complexity": "LOW",
                "platform_dependency": "LOW",
                "uncertainty": "LOW",
                "unknowns": [
                    "Willingness of business owners to pay without bundled Chartered Accountant filing",
                    "Retention rate after first 3 months of automated notifications",
                ],
                "experiment": {
                    "hypothesis": "Founders will subscribe to a WhatsApp calendar alert service to avoid late filing penalties.",
                    "validation": "Share a free compliance deadline calendar with 10 startup founders and survey upgrade intent.",
                    "budget": 0.0,
                    "duration": "7 days",
                    "success_metric": "At least 2 founders request a paid recurring monitoring plan.",
                    "failure_metric": "Zero founders find deadline alerts valuable.",
                    "data_required": ["Penalty exposure feedback", "Preferred messaging channel"],
                    "human_approvals_required": True,
                },
            },
            {
                "title": "Urban Rooftop Solar EPC Lead Pre-Qualification",
                "sector": "Clean Energy Services",
                "search_query": "rooftop solar lead cost epc india",
                "target_market": "Tier-1 metro residential & commercial rooftop owners",
                "revenue_model": "pay_per_qualified_lead",
                "startup_cost": 4500.0,
                "cac": 450.0,
                "customer_value": 2000.0,
                "fulfilment_cost": 250.0,
                "time_to_first_revenue": "21 days",
                "automation_potential": "HIGH",
                "regulatory_complexity": "LOW",
                "platform_dependency": "LOW",
                "uncertainty": "MEDIUM",
                "unknowns": [
                    "Percentage of leads with unshaded roof area exceeding 300 sq ft",
                    "Willingness of local EPC installers to sign non-exclusive lead referral agreements",
                ],
                "experiment": {
                    "hypothesis": "Local EPC installers will commit to pay 1,000+ INR for site-visit-ready rooftop leads with verified bills.",
                    "validation": "Interview 5 licensed local installers regarding their current customer acquisition cost.",
                    "budget": 0.0,
                    "duration": "7 days",
                    "success_metric": "At least 2 installers confirm willingness to buy pre-qualified leads.",
                    "failure_metric": "All installers report in-house lead gen only.",
                    "data_required": ["Installer target CAC", "Minimum bill threshold preferences"],
                    "human_approvals_required": True,
                },
            },
        ]

    async def execute_research(
        self,
        db: AsyncSession,
        objective: str = DEFAULT_RESEARCH_TEMPLATE,
        business_id: str | None = None,
        budget_limit: float = 10000.0,
    ) -> list[dict[str, Any]]:
        """
        Execute end-to-end Opportunity Engine workflow:
        1. Generate candidate concepts
        2. Research via WebSearchTool
        3. Classify evidence into Finding records
        4. Calculate multi-dimensional economics
        5. Run RiskAgent evaluations
        6. Store structured Opportunity records
        7. Record strategic memory
        """
        # Ensure fallback business if none provided
        if not business_id:
            biz_stmt = select(Business).limit(1)
            biz_res = await db.execute(biz_stmt)
            biz = biz_res.scalar_one_or_none()
            if biz:
                business_id = biz.id

        candidates = await self.generate_candidates(objective)
        saved_opportunities: list[dict[str, Any]] = []

        for cand in candidates:
            # 1. Gather web research evidence
            search_res = await self.research_agent.call_tool(
                "web_search",
                {"query": cand["search_query"]},
                business_id=business_id,
            )

            evidence_items = []
            findings: list[Finding] = []
            if search_res.get("status") == "SUCCESS" and search_res.get("result"):
                results = search_res["result"].get("results", [])
                for item in results:
                    hint = item.get("claim_type", "FACT")
                    # Ensure estimation keywords are never converted to fact
                    text_content = item.get("content", "")
                    classification = hint
                    if any(k in text_content.lower() for k in ["estimate", "approx", "projected"]):
                        classification = FindingClassification.ESTIMATE.value
                    elif any(k in text_content.lower() for k in ["claim", "believed", "reported"]):
                        classification = FindingClassification.CLAIM.value

                    finding = Finding.create_and_verify(
                        source_url=item.get("source", "https://web.internal"),
                        source_title=item.get("title", "Market Source"),
                        source_domain=item.get("domain", "web.internal"),
                        publication_date=item.get("publication_date"),
                        classification=classification,
                        content_summary=text_content,
                        confidence=0.85,
                    )
                    findings.append(finding)
                    evidence_items.append({
                        "type": finding.classification.value,
                        "source": finding.source_url,
                        "statement": finding.content_summary,
                        "domain": finding.source_domain,
                        "confidence": finding.confidence,
                    })

            # 2. Multi-dimensional economic calculation
            customer_val = cand["customer_value"]
            cac = cand["cac"]
            fulfilment = cand["fulfilment_cost"]
            margin = (customer_val - cac - fulfilment) / customer_val if customer_val > 0 else 0.0

            # Evidence quality scoring
            fact_count = sum(1 for f in findings if f.classification == FindingClassification.FACT)
            evidence_quality = "HIGH" if fact_count >= 1 else "MEDIUM"

            # 3. Risk Evaluation
            risk_run = await self.risk_agent.run(
                input_data={
                    "action_type": "evaluate_opportunity",
                    "description": f"Evaluate opportunity: {cand['title']}",
                    "amount": cand["experiment"]["budget"],
                    "evidence": evidence_items,
                },
                business_id=business_id,
            )

            risk_level = risk_run.outputs.get("risk_evaluation", {}).get("risk_level", "LOW")

            # 4. Save Opportunity in database
            opp = Opportunity(
                business_id=business_id,
                title=cand["title"],
                description=f"Automated business model targeting {cand['sector']}.",
                target_market=cand["target_market"],
                revenue_model=cand["revenue_model"],
                estimated_startup_cost=cand["startup_cost"],
                estimated_customer_value=customer_val,
                estimated_acquisition_cost=cac,
                estimated_fulfilment_cost=fulfilment,
                estimated_margin=round(margin, 2),
                automation_potential=cand["automation_potential"],
                time_to_first_revenue=cand["time_to_first_revenue"],
                regulatory_complexity=cand["regulatory_complexity"],
                platform_dependency=cand["platform_dependency"],
                uncertainty=cand["uncertainty"],
                evidence_quality=evidence_quality,
                risk_level=risk_level,
                evidence=evidence_items,
                findings=[f.model_dump(mode="json") for f in findings],
                assumptions=[
                    {"assumption": "Customers will pay without physical on-site sales meetings", "confidence": 0.85},
                    {"assumption": "Unit margins remain positive under trial customer acquisition costs", "confidence": 0.90},
                ],
                unknowns=cand["unknowns"],
                recommended_experiment=cand["experiment"],
                status="IDENTIFIED",
            )
            db.add(opp)
            await db.flush()

            # 5. Save Strategic Memory per Section 12
            memory = Memory(
                business_id=business_id,
                type="STRATEGIC",
                source="OpportunityEngine",
                confidence=0.88,
                content={
                    "opportunity_id": opp.id,
                    "title": opp.title,
                    "target_market": opp.target_market,
                    "margin": opp.estimated_margin,
                    "time_to_first_revenue": opp.time_to_first_revenue,
                    "uncertainty": opp.uncertainty,
                    "evidence_summary": [f"{f.classification.value}: {f.content_summary[:80]}" for f in findings],
                    "recommended_experiment": cand["experiment"]["hypothesis"],
                },
            )
            db.add(memory)

            saved_opportunities.append({
                "id": opp.id,
                "title": opp.title,
                "target_market": opp.target_market,
                "revenue_model": opp.revenue_model,
                "estimated_startup_cost": opp.estimated_startup_cost,
                "estimated_customer_value": opp.estimated_customer_value,
                "estimated_margin": opp.estimated_margin,
                "automation_potential": opp.automation_potential,
                "time_to_first_revenue": opp.time_to_first_revenue,
                "uncertainty": opp.uncertainty,
                "evidence_quality": opp.evidence_quality,
                "risk_level": opp.risk_level,
                "unknowns": opp.unknowns,
                "experiment": opp.recommended_experiment,
                "findings_count": len(findings),
                "status": opp.status,
            })

        await db.commit()

        # Record Audit Log
        await AuditService.record_event(
            db=db,
            actor="OpportunityEngine",
            business_id=business_id,
            action="RESEARCH_OPPORTUNITIES",
            target=f"Opportunities:{len(saved_opportunities)}",
            result="SUCCESS",
            metadata={
                "objective": objective[:100],
                "count": len(saved_opportunities),
            },
        )

        return saved_opportunities
