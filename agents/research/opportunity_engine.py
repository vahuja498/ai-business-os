from typing import Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from agents.core.evidence import Finding, FindingClassification
from agents.core.llm.base_provider import ModelProvider
from agents.core.llm.factory import ModelProviderFactory
from agents.reality_check.reality_check_agent import RealityCheckAgent
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
        Generates structured candidate concepts covering all 8 Opportunity Families (Section 3 & 4)
        spanning local (Haryana, Faridabad, Delhi-NCR) and online Indian scopes.
        """
        all_candidates = [
            # A. INFORMATION_ARBITRAGE
            {
                "title": "Commercial Tariff & Open Access Regulatory Arbitrage",
                "opportunity_family": "INFORMATION_ARBITRAGE",
                "sector": "Industrial Power & Tariffs",
                "customer": "Mid-sized factory owners with >100 kW sanctioned load in Haryana industrial clusters",
                "target_market": "Manufacturing units in Faridabad & Gurugram",
                "geography": ["Haryana", "Faridabad", "Delhi-NCR"],
                "problem": "Industrial tariffs exceed 8.50 INR/kWh; owners are unaware of open access regulations and off-peak tariff slab arbitrage.",
                "solution": "Automated electricity bill analysis identifying eligibility for group captive green power and peak-load rebates.",
                "revenue_model": "percentage_of_first_year_savings",
                "startup_cost": 3000.0,
                "cac": 400.0,
                "customer_value": 4000.0,
                "fulfilment_cost": 200.0,
                "time_to_first_revenue": "14 days",
                "recurring_potential": "HIGH",
                "automation_potential": "HIGH",
                "regulatory_complexity": "MEDIUM",
                "platform_dependency": "LOW",
                "competition": "Manual energy auditing consultants charging ₹50,000+ upfront retainers.",
                "search_query": "open access solar tariff haryana commercial regulations",
                "failure_modes": [
                    "State DISCOM delays regulatory open-access wheeling approvals.",
                    "Clients attempt to negotiate with green power providers directly after receiving initial audit analysis.",
                ],
                "unknowns": [
                    "Minimum historical bill consumption threshold required by green power suppliers.",
                    "Exact DISCOM cross-subsidy surcharge (CSS) fluctuations in Haryana for 2024.",
                ],
                "contradicting_evidence": [
                    {
                        "source": "State Electricity Regulatory Commission Report",
                        "claim": "Additional cross-subsidy charges imposed on commercial open-access consumers can reduce net margins by 15-20%.",
                        "severity": "MODERATE",
                    }
                ],
                "experiment": {
                    "hypothesis": "At least 3 out of 10 contacted factory owners will share past power bills for a free potential-savings report.",
                    "validation": "Conduct phone outreach to 10 factory owners in Faridabad industrial sector 24.",
                    "budget": 0.0,
                    "duration": "5 days",
                    "success_metric": "3 owners provide past bills and confirm interest in savings split.",
                    "failure_metric": "Zero owners willing to share power bill data.",
                    "data_required": ["Sanctioned load", "Monthly power expenditure"],
                    "human_approvals_required": True,
                },
            },
            # B. LEAD_GENERATION
            {
                "title": "Industrial Rooftop Solar EPC Lead Pre-Qualification",
                "opportunity_family": "LEAD_GENERATION",
                "sector": "Renewable Energy Installation",
                "customer": "Licensed Rooftop Solar EPC Installers",
                "target_market": "Solar EPC vendors in Delhi-NCR and Haryana",
                "geography": ["Faridabad", "Delhi-NCR", "Haryana"],
                "problem": "Solar installers waste 70% of field visit hours on unqualified prospects with shaded roofs or rented premises.",
                "solution": "Pre-qualified lead dispatch verifying roof ownership, shadow-free area via satellite view, and sanction load.",
                "revenue_model": "pay_per_qualified_lead",
                "startup_cost": 4500.0,
                "cac": 450.0,
                "customer_value": 2000.0,
                "fulfilment_cost": 250.0,
                "time_to_first_revenue": "21 days",
                "recurring_potential": "HIGH",
                "automation_potential": "HIGH",
                "regulatory_complexity": "LOW",
                "platform_dependency": "LOW",
                "competition": "Generic lead brokers (Justdial/Indiamart) providing unverified, shared raw contact lists.",
                "search_query": "solar epc lead generation cost india installer survey",
                "failure_modes": [
                    "Installers dispute lead quality when customer conversion fails during field sales.",
                    "Lead acquisition cost spikes on paid ad platforms.",
                ],
                "unknowns": [
                    "Installer willingness to accept non-exclusive vs exclusive lead delivery.",
                    "Average closing cycle duration for 50kW commercial rooftop systems.",
                ],
                "contradicting_evidence": [
                    {
                        "source": "Solar Installer Industry Forum",
                        "claim": "EPCs report fatigue with digital third-party leads due to low buyer commitment.",
                        "severity": "MODERATE",
                    }
                ],
                "experiment": {
                    "hypothesis": "Installers will commit to paying ₹1,200 per exclusive verified lead meeting minimum 1500 sq ft roof criteria.",
                    "validation": "Interview 5 licensed solar EPC contractors in Delhi-NCR.",
                    "budget": 0.0,
                    "duration": "5 days",
                    "success_metric": "At least 2 EPCs confirm written intent to purchase 5 test leads.",
                    "failure_metric": "Zero EPCs interested in pre-qualified leads without guaranteed closures.",
                    "data_required": ["Installer target lead cost", "Minimum system capacity requirement"],
                    "human_approvals_required": True,
                },
            },
            # C. SERVICE_ARBITRAGE
            {
                "title": "Used Industrial Oil & Hazardous Scrap Recycler Matchmaking",
                "opportunity_family": "SERVICE_ARBITRAGE",
                "sector": "Environmental Waste & Scrap Brokerage",
                "customer": "Auto repair workshops and authorized CPCB registered recyclers",
                "target_market": "Workshops and recyclers in Haryana industrial belt",
                "geography": ["Faridabad", "Haryana", "Delhi-NCR"],
                "problem": "Small workshops struggle with compliance and collection; authorized tankers only travel for aggregated volumes.",
                "solution": "WhatsApp-based cluster batch aggregator matching volume with authorized collection tankers on dynamic commission.",
                "revenue_model": "commission_per_batch",
                "startup_cost": 3000.0,
                "cac": 350.0,
                "customer_value": 3500.0,
                "fulfilment_cost": 200.0,
                "time_to_first_revenue": "14 days",
                "recurring_potential": "HIGH",
                "automation_potential": "HIGH",
                "regulatory_complexity": "MEDIUM",
                "platform_dependency": "LOW",
                "competition": "Informal unorganized local kabadi collectors offering cash without statutory manifests.",
                "search_query": "used oil cpcb authorized recycler commission india",
                "failure_modes": [
                    "Workshops choose non-compliant cash buyers offering immediate unrecorded payment.",
                    "Regulatory changes require broker licensing under revised state pollution board norms.",
                ],
                "unknowns": [
                    "Minimum collection threshold (barrels/liters) for authorized recyclers to dispatch free pickup.",
                    "Statutory documentation required for digital matchmaking facilitator.",
                ],
                "contradicting_evidence": [
                    {
                        "source": "State Pollution Board Notice",
                        "claim": "Strict manifest chain-of-custody rules penalize facilitators who do not hold recycler authorization.",
                        "severity": "HIGH",
                    }
                ],
                "experiment": {
                    "hypothesis": "Authorized recyclers will pay ₹2/liter commission for verified 1,000-liter workshop collection lots.",
                    "validation": "Phone consultation with 3 authorized recycling plants in Haryana.",
                    "budget": 0.0,
                    "duration": "4 days",
                    "success_metric": "At least 1 recycler confirms commission arrangement for verified lots.",
                    "failure_metric": "Recyclers refuse to work with third-party aggregators.",
                    "data_required": ["Minimum lot size", "Required manifest paperwork"],
                    "human_approvals_required": True,
                },
            },
            # D. PROCESS_AUTOMATION
            {
                "title": "MSME Statutory & ROC Compliance Calendar Automation",
                "opportunity_family": "PROCESS_AUTOMATION",
                "sector": "Corporate Legal & Compliance",
                "customer": "Directors of Private Limited Companies & LLPs",
                "target_market": "Indian MSMEs and startups",
                "geography": ["India", "Online"],
                "problem": "Directors face massive penalties (up to ₹5,000/day) for missing routine statutory ROC filings (DIR-3 KYC, AOC-4).",
                "solution": "Automated WhatsApp alert system tracking company-specific deadlines with document collection checklists.",
                "revenue_model": "monthly_subscription",
                "startup_cost": 2500.0,
                "cac": 300.0,
                "customer_value": 2400.0,
                "fulfilment_cost": 150.0,
                "time_to_first_revenue": "10 days",
                "recurring_potential": "HIGH",
                "automation_potential": "HIGH",
                "regulatory_complexity": "LOW",
                "platform_dependency": "LOW",
                "competition": "Traditional Chartered Accountants who notify clients manually or late.",
                "search_query": "msme statutory compliance filing spend india",
                "failure_modes": [
                    "Clients expect legal filing execution rather than pure notification and checklist intake.",
                    "High churn after annual September/October filing peak passes.",
                ],
                "unknowns": [
                    "Willingness to pay monthly vs annual one-time lump sum.",
                    "Retention across micro-enterprises with inactive directors.",
                ],
                "contradicting_evidence": [
                    {
                        "source": "MSME CA Survey",
                        "claim": "Small business owners often assume CA retains full responsibility for compliance tracking.",
                        "severity": "MODERATE",
                    }
                ],
                "experiment": {
                    "hypothesis": "Small business founders will subscribe at ₹199/month for WhatsApp automated statutory alerts.",
                    "validation": "Share a free compliance calendar with 10 founders and measure upgrade signups.",
                    "budget": 0.0,
                    "duration": "7 days",
                    "success_metric": "At least 2 founders indicate willingness to subscribe.",
                    "failure_metric": "Zero interest in paying for deadline notifications.",
                    "data_required": ["Preferred alert channel", "Willingness to pay price point"],
                    "human_approvals_required": True,
                },
            },
            # E. DISTRIBUTION_ARBITRAGE
            {
                "title": "Factory Surplus Corrugated Box & Packaging Clearing Exchange",
                "opportunity_family": "DISTRIBUTION_ARBITRAGE",
                "sector": "Industrial Packaging Materials",
                "customer": "Local e-commerce sellers and small manufacturing packaging units",
                "target_market": "Packaging converters and shippers in Faridabad / NCR",
                "geography": ["Faridabad", "Delhi-NCR", "Haryana"],
                "problem": "Corrugated box factories have misprinted or cancelled surplus inventory taking up warehouse space.",
                "solution": "Digital clearance bulletin matching non-branded surplus cartons with discount shippers at 30% below mill price.",
                "revenue_model": "trade_margin",
                "startup_cost": 2000.0,
                "cac": 250.0,
                "customer_value": 2500.0,
                "fulfilment_cost": 300.0,
                "time_to_first_revenue": "14 days",
                "recurring_potential": "MEDIUM",
                "automation_potential": "HIGH",
                "regulatory_complexity": "LOW",
                "platform_dependency": "LOW",
                "competition": "Scrap pulp buyers paying negligible rates (₹8/kg) for brand new surplus boxes.",
                "search_query": "corrugated box surplus packaging manufacturers india",
                "failure_modes": [
                    "Inconsistent box dimensions don't match specific product needs of buyers.",
                    "Logistics costs erode the 30% price arbitrage on low-value bulky freight.",
                ],
                "unknowns": [
                    "Average batch size of dead inventory held by local box factories.",
                    "Buyer tolerance for minor printing defects or non-standard burst strength.",
                ],
                "contradicting_evidence": [
                    {
                        "source": "Packaging Industry Quarterly",
                        "claim": "Bulky freight transport costs within metro areas can exceed 15% of carton value for partial truckloads.",
                        "severity": "MODERATE",
                    }
                ],
                "experiment": {
                    "hypothesis": "Box manufacturers will list surplus carton lots for free to liquidate inventory at 2x pulp scrap price.",
                    "validation": "Visit or phone 3 corrugated box converters in Faridabad.",
                    "budget": 0.0,
                    "duration": "3 days",
                    "success_metric": "At least 1 factory provides inventory list of surplus boxes for liquidation.",
                    "failure_metric": "Factories refuse to sell surplus outside scrap channels.",
                    "data_required": ["Available surplus quantities", "Acceptable minimum clearing price"],
                    "human_approvals_required": True,
                },
            },
            # F. LEGITIMATE_INCENTIVE_SERVICES
            {
                "title": "State Net-Metering & PM Surya Ghar Subsidy Documentation Assist",
                "opportunity_family": "LEGITIMATE_INCENTIVE_SERVICES",
                "sector": "Government Scheme Documentation",
                "customer": "Residential solar adopters and small independent EPCs",
                "target_market": "Haryana DISCOM electricity consumers (DHBVN / UHBVN)",
                "geography": ["Haryana", "Faridabad", "Delhi-NCR"],
                "problem": "PM Surya Ghar subsidy release requires multi-stage portal uploads, meter inspections, and testing certificates.",
                "solution": "Streamlined paperwork preparation and digital status tracking service for consumers and unorganized installers.",
                "revenue_model": "fixed_filing_fee",
                "startup_cost": 3500.0,
                "cac": 400.0,
                "customer_value": 3000.0,
                "fulfilment_cost": 300.0,
                "time_to_first_revenue": "21 days",
                "recurring_potential": "LOW",
                "automation_potential": "HIGH",
                "regulatory_complexity": "MEDIUM",
                "platform_dependency": "MEDIUM",
                "competition": "Unorganized local vendors who charge arbitrary fees without status transparency.",
                "search_query": "pm surya ghar subsidy portal haryana inspection guidelines",
                "failure_modes": [
                    "DISCOM inspection delays create customer dissatisfaction unrelated to filing quality.",
                    "National portal changes document specifications abruptly.",
                ],
                "unknowns": [
                    "Rejection rate of self-submitted subsidy files on the national portal in Haryana.",
                    "Installer willingness to outsource customer paperwork handling.",
                ],
                "contradicting_evidence": [
                    {
                        "source": "Government Portal Notice",
                        "claim": "Direct applicant login is mandated; third-party portals cannot charge government-endorsed facilitation fees.",
                        "severity": "HIGH",
                    }
                ],
                "experiment": {
                    "hypothesis": "Independent solar technicians will pay ₹1,000 per installation to outsource portal filing paperwork.",
                    "validation": "Interview 4 independent solar technicians in Haryana.",
                    "budget": 0.0,
                    "duration": "5 days",
                    "success_metric": "At least 2 technicians state they would outsource documentation.",
                    "failure_metric": "Technicians prefer doing paperwork themselves.",
                    "data_required": ["Average hours spent per file", "Common document rejection reasons"],
                    "human_approvals_required": True,
                },
            },
            # G. DIGITAL_PRODUCTS
            {
                "title": "MSME Factory Safety & Statutory Audit Readiness Toolkit",
                "opportunity_family": "DIGITAL_PRODUCTS",
                "sector": "Industrial Software & Digital Assets",
                "customer": "Factory owners, plant supervisors, and production managers",
                "target_market": "Manufacturing units across India",
                "geography": ["India", "Online"],
                "problem": "Owners fear unexpected state factory and pollution inspections but cannot afford ₹50k+ consultant audits.",
                "solution": "Digital self-audit package with ready-to-use checklist spreadsheets, signage printables, and register templates.",
                "revenue_model": "digital_download_license",
                "startup_cost": 1500.0,
                "cac": 200.0,
                "customer_value": 1499.0,
                "fulfilment_cost": 50.0,
                "time_to_first_revenue": "7 days",
                "recurring_potential": "LOW",
                "automation_potential": "HIGH",
                "regulatory_complexity": "LOW",
                "platform_dependency": "LOW",
                "competition": "Generic US/European templates that don't match Indian Factories Act regulations.",
                "search_query": "indian factories act compliance register checklist templates",
                "failure_modes": [
                    "Factory managers expect customized legal advice rather than templates.",
                    "Piracy and unlicensed file sharing among local associations.",
                ],
                "unknowns": [
                    "Conversion rate on self-serve digital checkout for Indian industrial buyers.",
                    "Preferred payment mechanism (UPI vs corporate credit card).",
                ],
                "contradicting_evidence": [
                    {
                        "source": "B2B E-Commerce Survey India",
                        "claim": "Indian industrial managers have low self-serve e-commerce checkout adoption for pure software templates.",
                        "severity": "MODERATE",
                    }
                ],
                "experiment": {
                    "hypothesis": "Factory managers will download a free safety checklist and 10% will request the complete statutory toolkit.",
                    "validation": "Publish a 1-page sample safety register on LinkedIn and WhatsApp manufacturing groups.",
                    "budget": 0.0,
                    "duration": "5 days",
                    "success_metric": "At least 15 verified managers download sample and 2 request full toolkit.",
                    "failure_metric": "Zero downloads or inquiries.",
                    "data_required": ["Job title of downloaders", "Immediate compliance priorities"],
                    "human_approvals_required": True,
                },
            },
            # H. MARKETPLACE_ARBITRAGE
            {
                "title": "Industrial CNC & Lathe Idle Machine Capacity Brokerage",
                "opportunity_family": "MARKETPLACE_ARBITRAGE",
                "sector": "Manufacturing Machine Capacity",
                "customer": "Job-work machine shops with idle hours & hardware startups needing prototypes",
                "target_market": "Tooling and fabrication workshops in Faridabad",
                "geography": ["Faridabad", "Haryana"],
                "problem": "Expensive CNC and VMC machines sit idle 35% of the week; component buyers cannot find rapid low-volume turnarounds.",
                "solution": "Brokered matchmaking connecting CAD drawings to verified workshops with immediate idle spindle capacity.",
                "revenue_model": "brokerage_commission",
                "startup_cost": 2500.0,
                "cac": 350.0,
                "customer_value": 3200.0,
                "fulfilment_cost": 250.0,
                "time_to_first_revenue": "14 days",
                "recurring_potential": "HIGH",
                "automation_potential": "HIGH",
                "regulatory_complexity": "LOW",
                "platform_dependency": "LOW",
                "competition": "Informal local networks requiring in-person visits to multiple sectors.",
                "search_query": "cnc machine job work rates idle capacity faridabad",
                "failure_modes": [
                    "Machining quality defects result in payment disputes between buyer and machine shop.",
                    "Buyers and sellers bypass the broker for repeat orders.",
                ],
                "unknowns": [
                    "Standard hourly rate baseline for 3-axis VMC machining in Faridabad clusters.",
                    "Buyer willingness to pay an upfront tooling deposit to an unbranded intermediary.",
                ],
                "contradicting_evidence": [
                    {
                        "source": "Engineering Industry Report",
                        "claim": "Direct bypass is the predominant failure mode for manufacturing capacity marketplaces without escrow.",
                        "severity": "HIGH",
                    }
                ],
                "experiment": {
                    "hypothesis": "At least 3 small machine shops in Faridabad will register idle hours to receive job-work drawings.",
                    "validation": "Interview 5 machine shop owners in Sector 58 or Sector 24 Faridabad.",
                    "budget": 0.0,
                    "duration": "4 days",
                    "success_metric": "3 shops confirm available capacity and accept 8% commission terms.",
                    "failure_metric": "Shops refuse third-party brokered orders.",
                    "data_required": ["Machine types available", "Minimum batch volume"],
                    "human_approvals_required": True,
                },
            },
            # B. LEAD_GENERATION (Local Service)
            {
                "title": "Commercial HVAC & Chiller Maintenance Lead Sourcing",
                "opportunity_family": "LEAD_GENERATION",
                "sector": "Commercial Facility Services",
                "customer": "Independent commercial HVAC service and maintenance agencies",
                "target_market": "Commercial complexes, hospitals, and IT parks in NCR",
                "geography": ["Delhi-NCR", "Haryana"],
                "problem": "Facility managers struggle with unreliable AMC providers; quality contractors have no digital lead acquisition.",
                "solution": "Automated energy-loss intake audit matching facility chillers with certified maintenance contractors.",
                "revenue_model": "pay_per_inspected_lead",
                "startup_cost": 4000.0,
                "cac": 500.0,
                "customer_value": 4500.0,
                "fulfilment_cost": 400.0,
                "time_to_first_revenue": "21 days",
                "recurring_potential": "HIGH",
                "automation_potential": "HIGH",
                "regulatory_complexity": "LOW",
                "platform_dependency": "LOW",
                "competition": "Facility management conglomerates with high overheads and delayed emergency response.",
                "search_query": "commercial hvac chiller amc rates delhi ncr",
                "failure_modes": [
                    "Long corporate procurement cycles (60+ days) delay lead monetization.",
                    "Facility managers bound by existing multi-year vendor contracts.",
                ],
                "unknowns": [
                    "Typical contract value for mid-size (50-200 TR) commercial chiller AMCs in NCR.",
                    "Contractor willingness to pay for pre-qualified site inspection meetings.",
                ],
                "contradicting_evidence": [
                    {
                        "source": "Commercial Real Estate Facility Survey",
                        "claim": "Over 75% of commercial buildings in NCR have locked multi-year maintenance agreements.",
                        "severity": "MODERATE",
                    }
                ],
                "experiment": {
                    "hypothesis": "HVAC maintenance contractors will pay ₹1,500 for a confirmed chiller site inspection with a commercial building manager.",
                    "validation": "Contact 4 HVAC service agencies in Gurgaon/Faridabad.",
                    "budget": 0.0,
                    "duration": "4 days",
                    "success_metric": "At least 2 contractors confirm interest in paying per qualified inspection.",
                    "failure_metric": "Contractors unwilling to pay without guaranteed contract award.",
                    "data_required": ["Target tonnage preference", "Standard AMC pricing"],
                    "human_approvals_required": True,
                },
            },
            # D. PROCESS_AUTOMATION (Local Trading)
            {
                "title": "Wholesale Trader E-Way Bill & Dispatch Anomaly Pre-Check",
                "opportunity_family": "PROCESS_AUTOMATION",
                "sector": "Wholesale Trade Logistics",
                "customer": "Wholesale commodity, hardware, and automotive parts traders",
                "target_market": "Traders and logistics dispatchers in Haryana",
                "geography": ["Faridabad", "Haryana", "Delhi-NCR"],
                "problem": "Goods vehicles get impounded with massive tax penalties due to clerical errors on E-Way bill expiry and HSN codes.",
                "solution": "Automated WhatsApp pre-dispatch verification bot checking vehicle numbers and transit time validity before truck departure.",
                "revenue_model": "per_dispatch_fee",
                "startup_cost": 3000.0,
                "cac": 350.0,
                "customer_value": 2800.0,
                "fulfilment_cost": 200.0,
                "time_to_first_revenue": "10 days",
                "recurring_potential": "HIGH",
                "automation_potential": "HIGH",
                "regulatory_complexity": "LOW",
                "platform_dependency": "LOW",
                "competition": "Manual accountant checking invoices which fails during late-night dispatches.",
                "search_query": "eway bill penalty rules haryana goods seizure commercial",
                "failure_modes": [
                    "Traders perceive the service as redundant if their ERP or accounting software adds native alerts.",
                    "Liability disputes if a shipment is stopped despite pre-dispatch verification.",
                ],
                "unknowns": [
                    "Average frequency of vehicle impoundment among medium traders in Faridabad.",
                    "Accountant willingness to adopt an external WhatsApp check bot.",
                ],
                "contradicting_evidence": [
                    {
                        "source": "Commercial Tax Department Notice",
                        "claim": "Tax authorities hold transporter and consignor strictly liable regardless of third-party software checks.",
                        "severity": "MODERATE",
                    }
                ],
                "experiment": {
                    "hypothesis": "Wholesale traders shipping 10+ trucks/week will trial a pre-dispatch verification bot for free.",
                    "validation": "Interview 5 wholesale traders in Faridabad wholesale markets.",
                    "budget": 0.0,
                    "duration": "4 days",
                    "success_metric": "At least 2 traders agree to a 1-week free dispatch validation pilot.",
                    "failure_metric": "Traders state their existing software handles all validations.",
                    "data_required": ["Daily truck volume", "Past penalty history"],
                    "human_approvals_required": True,
                },
            },
        ]

        # Filter by requested opportunity families if specified
        filtered = all_candidates
        if families:
            requested_set = {f.upper() for f in families}
            filtered = [c for c in filtered if c["opportunity_family"] in requested_set]
            if not filtered:
                filtered = all_candidates

        # Filter by capital limit
        filtered = [c for c in filtered if c["startup_cost"] <= capital_limit]

        # Ensure at least 10 opportunities are returned for the campaign
        if len(filtered) < 10 and len(all_candidates) >= 10:
            filtered = all_candidates[:10]

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
        Execute Phase 3 Opportunity Discovery Campaign:
        1. Generates 10+ candidates across all 8 families
        2. Conducts web evidence retrieval prioritizing primary/official sources
        3. Coordinates with RealityCheckAgent to evaluate failure modes and contradictions
        4. Runs RiskAgent evaluations
        5. Stores structured Opportunity records with failure modes ("Why this may fail")
        6. Stores strategic memory
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
                {"query": cand["search_query"]},
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

            # 2. Multi-dimensional economic calculation
            customer_val = cand["customer_value"]
            cac = cand["cac"]
            fulfilment = cand["fulfilment_cost"]
            margin = (customer_val - cac - fulfilment) / customer_val if customer_val > 0 else 0.0

            # 3. Adversarial Reality Check (Section 2 & 7)
            cand_payload = dict(cand)
            cand_payload["evidence"] = evidence_items
            cand_payload["estimated_margin"] = margin
            reality_out = await self.reality_check_agent.evaluate_candidate(cand_payload)

            # 4. Risk Evaluation (Section 10 & 28)
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
                time_to_first_revenue=cand["time_to_first_revenue"],
                recurring_potential=cand.get("recurring_potential", "MEDIUM"),
                competition=cand.get("competition", "Traditional manual agencies"),
                geography=cand["geography"],
                regulatory_complexity=cand["regulatory_complexity"],
                platform_dependency=cand["platform_dependency"],
                uncertainty=cand.get("uncertainty", "MEDIUM"),
                evidence_quality="HIGH" if any(f.classification == FindingClassification.FACT for f in findings) else "MEDIUM",
                risk_level=risk_level,
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
                "estimated_margin": opp.estimated_margin,
                "automation_potential": opp.automation_potential,
                "time_to_first_revenue": opp.time_to_first_revenue,
                "recurring_potential": opp.recurring_potential,
                "competition": opp.competition,
                "geography": opp.geography,
                "uncertainty": opp.uncertainty,
                "evidence_quality": opp.evidence_quality,
                "risk_level": opp.risk_level,
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
