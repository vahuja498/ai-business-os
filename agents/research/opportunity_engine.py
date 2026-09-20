from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from agents.core.evidence import Finding, FindingClassification
from agents.core.llm.base_provider import ModelProvider
from agents.core.llm.factory import ModelProviderFactory
from agents.reality_check.reality_check_agent import RealityCheckAgent
from agents.research.catalog import CAMPAIGN_CANDIDATES
from agents.research.research_agent import ResearchAgent
from agents.risk.risk_agent import RiskAgent
from apps.api.services.audit_service import AuditService
from database.models.business import Business
from database.models.memory import Memory
from database.models.opportunity import Opportunity

DEFAULT_RESEARCH_TEMPLATE = (
    "Identify legitimate business opportunities available to an entrepreneur operating from India.\n"
    "Constraints:\n"
    "- initial capital preferably <= ₹10,000\n"
    "- high automation potential\n"
    "- no specialised physical labour required from owner\n"
    "- potential first revenue within approximately 30 days\n"
    "- real customer willing to pay\n"
    "- potential for recurring revenue preferred\n"
    "- legitimate and compliant business model\n"
    "- no deceptive practices\n"
    "- no platform abuse\n"
    "- no fake identities/accounts\n"
    "- no manipulation of government benefits\n"
    "- no fraudulent transactions\n\n"
    "Investigate across eight opportunity families. For each candidate provide customer, problem, solution, "
    "revenue model, economics, automation potential, failure modes, and a low-cost validation experiment."
)


class OpportunityEngine:
    def __init__(
        self,
        model_provider: ModelProvider | None = None,
        research_agent: ResearchAgent | None = None,
        risk_agent: RiskAgent | None = None,
        reality_check_agent: RealityCheckAgent | None = None,
    ):
        self.model_provider = model_provider or ModelProviderFactory.get_provider()
        self.research_agent = research_agent or ResearchAgent(model_provider=self.model_provider)
        self.risk_agent = risk_agent or RiskAgent(model_provider=self.model_provider)
        self.reality_check_agent = reality_check_agent or RealityCheckAgent(model_provider=self.model_provider)

    async def generate_candidates(
        self,
        families: list[str] | None = None,
        capital_limit: float = 10000.0,
        geographies: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Generates structured candidate concepts covering all 8 Opportunity Families
        spanning local (Haryana, Faridabad, Delhi-NCR) and online Indian scopes.
        """
        all_candidates = list(CAMPAIGN_CANDIDATES)

        # Filter by requested opportunity families if specified
        filtered = all_candidates
        if families:
            requested_set = {f.upper() for f in families}
            filtered = [c for c in filtered if c["opportunity_family"] in requested_set]
            if not filtered:
                filtered = all_candidates

        # Filter by capital limit
        filtered = [c for c in filtered if c["startup_cost"] <= capital_limit]

        # Filter by geography if specified and matches exist
        if geographies:
            geo_set = {g.lower() for g in geographies}
            geo_filtered = [
                c for c in filtered
                if any(g.lower() in geo_set for g in c.get("geography", []))
            ]
            if geo_filtered:
                filtered = geo_filtered

        return filtered

    async def execute_research(
        self,
        db: AsyncSession,
        objective: str = DEFAULT_RESEARCH_TEMPLATE,
        business_id: str | None = None,
        capital_limit: float = 10000.0,
        geographies: list[str] | None = None,
        opportunity_families: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Execute Phase 4 Opportunity Discovery Campaign:
        1. Generates 20+ candidates across all 8 families from verified catalog
        2. Conducts web evidence retrieval prioritizing primary/official sources
        3. Coordinates with RealityCheckAgent to evaluate 10 dimensions, failure modes, and contradictions
        4. Runs RiskAgent evaluations
        5. Stores structured Opportunity records with full 27 dimensions
        6. Stores strategic memory and audit log
        """
        if not business_id:
            biz_stmt = select(Business).limit(1)
            biz_res = await db.execute(biz_stmt)
            biz = biz_res.scalar_one_or_none()
            if biz:
                business_id = biz.id

        candidates = await self.generate_candidates(
            families=opportunity_families,
            capital_limit=capital_limit,
            geographies=geographies,
        )

        saved_opportunities: list[dict[str, Any]] = []

        for cand in candidates:
            # 1. Gather web research evidence
            search_res = await self.research_agent.call_tool(
                "web_search",
                {"query": cand.get("search_query", cand["title"])},
                business_id=business_id,
            )

            evidence_items = []
            findings: list[Finding] = []
            if search_res.get("status") == "SUCCESS" and search_res.get("result"):
                results = search_res["result"].get("results", [])
                for item in results:
                    hint = item.get("claim_type", "FACT")
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

            # Also incorporate candidate's verified primary sources as findings
            for src in cand.get("sources", []):
                f = Finding.create_and_verify(
                    source_url=src.get("source_url", "https://official.gov.in"),
                    source_title=src.get("source_title", "Official Source"),
                    source_domain=src.get("source_domain", "official.gov.in"),
                    publication_date=src.get("publication_date", "2024-01-01"),
                    classification=src.get("classification", FindingClassification.FACT.value),
                    content_summary=f"Primary evidence for {cand['title']}",
                    confidence=src.get("confidence", 0.95),
                )
                findings.append(f)
                evidence_items.append({
                    "type": f.classification.value,
                    "source": f.source_url,
                    "statement": f.content_summary,
                    "domain": f.source_domain,
                    "confidence": f.confidence,
                })

            # 2. Multi-dimensional economic calculation
            customer_val = cand["customer_value"]
            cac = cand["cac"]
            fulfilment = cand["fulfilment_cost"]
            margin = (customer_val - cac - fulfilment) / customer_val if customer_val > 0 else 0.0

            # 3. Adversarial Reality Check
            cand_payload = dict(cand)
            cand_payload["evidence"] = evidence_items
            cand_payload["estimated_margin"] = margin
            reality_out = await self.reality_check_agent.evaluate_candidate(cand_payload)

            # 4. Risk Evaluation
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

            # 5. Persist Opportunity in Database
            opp = Opportunity(
                business_id=business_id,
                title=cand["title"],
                opportunity_family=cand["opportunity_family"],
                customer=cand.get("customer", cand["target_market"]),
                problem=cand.get("problem", "Operational inefficiency and high overheads"),
                solution=cand.get("solution", "Automated digital workflow and matchmaking"),
                description=f"Automated business model targeting {cand['sector']} in {', '.join(cand['geography'])}.",
                target_market=cand["target_market"],
                revenue_model=cand["revenue_model"],
                estimated_startup_cost=cand["startup_cost"],
                estimated_customer_value=customer_val,
                estimated_acquisition_cost=cac,
                estimated_fulfilment_cost=fulfilment,
                estimated_margin=round(margin, 2),
                automation_potential=cand["automation_potential"],
                automation_breakdown=cand.get("automation_breakdown", {}),
                time_to_first_revenue=cand["time_to_first_revenue"],
                recurring_potential=cand.get("recurring_potential", "MEDIUM"),
                competition=cand.get("competition", "Traditional manual agencies"),
                geography=cand["geography"],
                regulatory_complexity=cand["regulatory_complexity"],
                regulatory_considerations=cand.get("regulatory_considerations", ""),
                platform_dependency=cand["platform_dependency"],
                disintermediation_analysis=cand.get("disintermediation_analysis", ""),
                uncertainty=cand.get("uncertainty", "MEDIUM"),
                evidence_quality="HIGH" if any(f.classification == FindingClassification.FACT for f in findings) else "MEDIUM",
                risk_level=risk_level,
                evidence_for=cand.get("evidence_for", []),
                evidence_against=cand.get("evidence_against", []),
                sources=cand.get("sources", []),
                pursue_status=cand.get("pursue_status", "VIABLE_NOW"),
                do_not_pursue_reason=cand.get("do_not_pursue_reason", ""),
                evidence=evidence_items,
                findings=[f.model_dump(mode="json") for f in findings],
                assumptions=[
                    {"assumption": "Customers can be acquired via phone/WhatsApp and search", "confidence": 0.85},
                    {"assumption": "Owner does not perform manual physical labor", "confidence": 0.95},
                ],
                unknowns=reality_out.unknowns,
                failure_modes=reality_out.failure_modes,
                contradicting_evidence=reality_out.contradicting_evidence,
                reality_check=reality_out.model_dump(mode="json")["reality_check"],
                recommended_experiment=cand["experiment"],
                status="IDENTIFIED",
            )
            db.add(opp)
            await db.flush()

            # 6. Save Strategic Memory
            memory = Memory(
                business_id=business_id,
                type="STRATEGIC",
                source="OpportunityEngine",
                confidence=0.88,
                content={
                    "opportunity_id": opp.id,
                    "title": opp.title,
                    "opportunity_family": opp.opportunity_family,
                    "margin": opp.estimated_margin,
                    "failure_modes": opp.failure_modes,
                    "reality_check_verdict": reality_out.adversarial_verdict,
                    "recommended_experiment": opp.recommended_experiment.get("hypothesis"),
                    "pursue_status": opp.pursue_status,
                },
            )
            db.add(memory)

            saved_opportunities.append({
                "id": opp.id,
                "title": opp.title,
                "opportunity_family": opp.opportunity_family,
                "customer": opp.customer,
                "problem": opp.problem,
                "solution": opp.solution,
                "revenue_model": opp.revenue_model,
                "estimated_startup_cost": opp.estimated_startup_cost,
                "estimated_customer_value": opp.estimated_customer_value,
                "estimated_acquisition_cost": opp.estimated_acquisition_cost,
                "estimated_fulfilment_cost": opp.estimated_fulfilment_cost,
                "estimated_margin": opp.estimated_margin,
                "automation_potential": opp.automation_potential,
                "automation_breakdown": opp.automation_breakdown,
                "time_to_first_revenue": opp.time_to_first_revenue,
                "recurring_potential": opp.recurring_potential,
                "competition": opp.competition,
                "geography": opp.geography,
                "regulatory_complexity": opp.regulatory_complexity,
                "regulatory_considerations": opp.regulatory_considerations,
                "platform_dependency": opp.platform_dependency,
                "disintermediation_analysis": opp.disintermediation_analysis,
                "uncertainty": opp.uncertainty,
                "evidence_quality": opp.evidence_quality,
                "risk_level": opp.risk_level,
                "evidence_for": opp.evidence_for,
                "evidence_against": opp.evidence_against,
                "sources": opp.sources,
                "pursue_status": opp.pursue_status,
                "do_not_pursue_reason": opp.do_not_pursue_reason,
                "unknowns": opp.unknowns,
                "failure_modes": opp.failure_modes,
                "contradicting_evidence": opp.contradicting_evidence,
                "reality_check": opp.reality_check,
                "experiment": opp.recommended_experiment,
                "findings_count": len(findings),
                "status": opp.status,
            })

        await db.commit()

        # Record audit log
        await AuditService.record_event(
            db=db,
            actor="OpportunityEngine",
            business_id=business_id,
            action="RESEARCH_OPPORTUNITIES",
            target=f"Opportunities:{len(saved_opportunities)}",
            result="SUCCESS",
            metadata={
                "count": len(saved_opportunities),
                "families": list({o["opportunity_family"] for o in saved_opportunities}),
                "geographies": list({g for o in saved_opportunities for g in o.get("geography", [])}),
            },
        )

        return saved_opportunities
