from typing import Any

CAMPAIGN_CANDIDATES: list[dict[str, Any]] = [
    # =========================================================================
    # 1. INFORMATION_ARBITRAGE
    # =========================================================================
    {
        "title": "Commercial Tariff & Open Access Regulatory Arbitrage",
        "opportunity_family": "INFORMATION_ARBITRAGE",
        "sector": "Industrial Power & Energy Tariffs",
        "customer": "Mid-sized factory owners with >100 kW sanctioned load in Haryana industrial clusters (Faridabad, Gurugram, Manesar). Problem: High peak industrial tariffs (> ₹8.50/kWh) and complex open-access regulations. Existing alternatives: Retaining manual energy auditors at ₹50,000+ upfront or taking no action.",
        "target_market": "Manufacturing units in Faridabad & Gurugram industrial corridors",
        "geography": ["Faridabad", "Haryana", "Delhi-NCR"],
        "problem": "Industrial electricity tariffs exceed ₹8.50/kWh with hidden power factor penalties; factory directors lack visibility into open-access wheeling regulations and group-captive solar tariff arbitrage.",
        "solution": "Automated power bill audit tool extracting consumption profiles, peak hour surcharges, and group captive green power eligibility to generate a cost-savings arbitrage report.",
        "revenue_model": "percentage_of_first_year_savings",
        "startup_cost": 3000.0,
        "cac": 400.0,
        "customer_value": 4000.0,
        "fulfilment_cost": 200.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "OCR intake of DISCOM electricity bills, time-of-day (ToD) tariff analysis, and automated savings report generation.",
            "software_automation": "DISCOM tariff schedule database lookups, savings calculator, and automated lead follow-up emails.",
            "human_only": "In-person signing of commercial agency contracts and client verification calls."
        },
        "competition": "Manual energy auditing firms charging ₹50,000 to ₹100,000 upfront retainers. Acquisition via offline trade bodies; our differentiation is zero upfront risk-free audit.",
        "regulatory_complexity": "MEDIUM",
        "regulatory_considerations": "Regulated by Haryana Electricity Regulatory Commission (HERC) Open Access Regulations. Service acts strictly as tariff information analyst; does not broker electricity or operate transmission infrastructure.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Customer could theoretically negotiate directly with IPPs/generators, but complex cross-subsidy surcharge (CSS) calculation prevents DIY navigation. Aggregator contract binds client to savings fee.",
        "search_query": "open access solar tariff haryana commercial regulations",
        "evidence_for": [
            "HERC industrial tariff orders establish 20% peak-hour surcharges for connected loads above 100 kW.",
            "Commercial industrial parks in Faridabad maintain documented power spends exceeding ₹1.5 lakh monthly."
        ],
        "evidence_against": [
            "DISCOM wheeling approval delays can take 45-90 days, postponing fee collection.",
            "Small industrial units under 100 kW are legally ineligible for third-party open access."
        ],
        "unknowns": [
            "Minimum continuous power consumption threshold mandated by green IPPs for captive delivery.",
            "DISCOM cross-subsidy surcharge (CSS) adjustments for the current fiscal quarter."
        ],
        "failure_modes": [
            "State DISCOM arbitrarily raises wheeling charges, negating projected customer savings.",
            "Factory client bypasses referral agreement after receiving initial tariff slab diagnosis."
        ],
        "experiment": {
            "hypothesis": "At least 3 out of 10 contacted factory owners will share past power bills for a free potential-savings diagnostic.",
            "validation": "Direct phone and WhatsApp outreach to 10 factory owners in Faridabad Sector 24.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "3 owners provide past bills and sign consent for savings diagnostic.",
            "failure_metric": "Zero owners willing to share power bill data without non-disclosure agreement.",
            "data_required": ["Sanctioned load", "Monthly power expenditure", "ToD meter reading logs"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Haryana Electricity Regulatory Commission (HERC) Tariff Order",
                "source_url": "https://herc.gov.in/tariff-regulations-2024",
                "source_domain": "herc.gov.in",
                "publication_date": "2024-01-10",
                "classification": "FACT",
                "confidence": 0.95
            },
            {
                "source_title": "Clean Energy India Open Access Analysis",
                "source_url": "https://cleanenergyindia.org/reports/haryana-open-access",
                "source_domain": "cleanenergyindia.org",
                "publication_date": "2024-02-15",
                "classification": "ESTIMATE",
                "confidence": 0.88
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Industrial Hazardous Waste & Scrap Metal Compliance Price Index",
        "opportunity_family": "INFORMATION_ARBITRAGE",
        "sector": "Industrial Secondary Raw Materials",
        "customer": "Auto-ancillary and machining factories in Faridabad generating metal turnings, swarf, and spent oil. Problem: Local scrap dealers underquote true market scrap prices by 20-30%. Existing alternatives: Selling to informal kabadiwalas without hazardous waste compliance documentation.",
        "target_market": "500+ small-scale engineering and casting workshops in Faridabad Industrial Area",
        "geography": ["Faridabad", "Haryana"],
        "problem": "Machine shops lose ₹15,000 to ₹50,000 monthly due to opaque local scrap pricing and face CPCB penalties for unmanifested spent oil transfers.",
        "solution": "Weekly SMS and WhatsApp benchmark bulletin publishing certified ingot rates, scrap yard bid levels, and verified CPCB/HSPCB authorized recyclers.",
        "revenue_model": "monthly_subscription",
        "startup_cost": 3000.0,
        "cac": 350.0,
        "customer_value": 3000.0,
        "fulfilment_cost": 150.0,
        "time_to_first_revenue": "10 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Automated ingestion and synthesis of commodity yard auctions and Mandi metal rates.",
            "software_automation": "Scheduled WhatsApp broadcast engine, subscription payment gateway, and subscriber verification.",
            "human_only": "Quarterly physical verification of CPCB recycler consent certificates."
        },
        "competition": "Informal unorganized scrap cartels and trade word-of-mouth with zero digital analytics or compliance guarantees.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Publication of market price information is non-regulated. Service does not take physical possession of hazardous waste; strictly publishes benchmark analytics.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Low risk; pricing data changes weekly across Mandi Gobindgarh and local yards, creating recurring subscription necessity.",
        "search_query": "hazardous waste disposal scrap metal price index faridabad haryana",
        "evidence_for": [
            "CPCB Hazardous and Other Wastes Rules 2016 require digital manifest tracking for all recyclable oil and metal waste.",
            "Secondary steel Mandi prices fluctuate up to 12% monthly, making real-time price tracking high value."
        ],
        "evidence_against": [
            "Traditional factory supervisors often take cash kickbacks from informal scrap buyers, resisting formal market benchmarking."
        ],
        "unknowns": [
            "Proportion of small factory owners willing to pay online subscription via UPI vs demand credit billing."
        ],
        "failure_modes": [
            "Scrap cartels pressure factory managers to ignore published transparent benchmarks.",
            "Subscribers pirate and share the weekly bulletin on unmonitored WhatsApp groups."
        ],
        "experiment": {
            "hypothesis": "At least 5 out of 15 machine shop owners in Sector 58 will pay ₹299 for a 1-month trial of weekly verified scrap price benchmarks.",
            "validation": "Distribute a free 1-week sample benchmark sheet to 15 machine shops and measure paid conversion.",
            "budget": 0.0,
            "duration": "7 days",
            "success_metric": "5 machine shops convert to paid monthly trial.",
            "failure_metric": "Fewer than 2 shops convert to paid subscription.",
            "data_required": ["Current scrap sale frequency", "Primary metal alloys machined"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Central Pollution Control Board Hazardous Waste Manifest Guidelines",
                "source_url": "https://cpcb.nic.in/hazardous-waste-rules",
                "source_domain": "cpcb.nic.in",
                "publication_date": "2023-11-01",
                "classification": "FACT",
                "confidence": 0.94
            },
            {
                "source_title": "B2B Metal Scrap Market Rate Survey",
                "source_url": "https://industry-scrap-market.in/lead-pricing-benchmarks",
                "source_domain": "industry-scrap-market.in",
                "publication_date": "2024-01-18",
                "classification": "ESTIMATE",
                "confidence": 0.88
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Central & Haryana State Industrial Subsidies Notification Radar",
        "opportunity_family": "INFORMATION_ARBITRAGE",
        "sector": "Government Incentive Information",
        "customer": "MSME factory directors seeking capital subsidies under Haryana Enterprise & Employment Policy (HEEP). Problem: Subsidy budget windows open and exhaust quickly; owners miss deadlines. Alternatives: Local Chartered Accountants who focus primarily on GST/Income tax filings.",
        "target_market": "Haryana manufacturing MSMEs",
        "geography": ["Haryana", "Pan-India"],
        "problem": "State and central capital investment and green audit subsidies lapse unutilized because small manufacturers are notified months after scheme funds are disbursed.",
        "solution": "Curated weekly alert bulletin tracking official Directorate of Industries Haryana circulars and subsidy allocation budgets.",
        "revenue_model": "subscription_quarterly",
        "startup_cost": 2500.0,
        "cac": 300.0,
        "customer_value": 2500.0,
        "fulfilment_cost": 100.0,
        "time_to_first_revenue": "7 days",
        "recurring_potential": "MEDIUM",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Web scraping of state industry gazettes, PDF text extraction, and scheme eligibility summarization.",
            "software_automation": "Subscriber notification dispatch via email/WhatsApp, renewal billing.",
            "human_only": "None required once scraping pipeline is calibrated."
        },
        "competition": "Industry trade associations sharing delayed circulars; informal chartered accountant networks.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Purely informational newsletter. Strictly no professional claim of filing or government influence.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Customers can check government websites directly, but rarely have time to inspect 5 different portals weekly.",
        "search_query": "haryana enterprise employment policy subsidy circulars 2024",
        "evidence_for": [
            "Haryana Enterprise and Employment Policy 2020 has disbursed over ₹1,000 Cr in capital subsidies across registered industrial blocks.",
            "State portals publish sudden subsidy window closures once annual fiscal allocations are hit."
        ],
        "evidence_against": [
            "Many MSME owners expect the service to perform the actual application filing rather than just provide notifications."
        ],
        "unknowns": [
            "Willingness to pay for notification alone when trade associations sometimes circulate notices for free."
        ],
        "failure_modes": [
            "Subscribers fail to secure subsidies due to pre-existing fiscal paperwork defects and blame the notification radar.",
            "Government consolidates all notifications onto a single national portal with automated push alerts."
        ],
        "experiment": {
            "hypothesis": "At least 4 out of 20 surveyed factory directors will pay ₹499/quarter for an early-alert subsidy radar.",
            "validation": "Share a PDF sample of upcoming Q3 Haryana MSME green technology subsidy windows with 20 MSMEs.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "At least 4 commitments for paid quarterly radar.",
            "failure_metric": "Less than 2 commitments; owners demand application execution rather than info.",
            "data_required": ["Factory MSME Udyam category", "Current capital expansion plans"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Haryana Industries Department HEEP Scheme Portal",
                "source_url": "https://haryanaindustries.gov.in/heep-guidelines",
                "source_domain": "haryanaindustries.gov.in",
                "publication_date": "2024-01-05",
                "classification": "FACT",
                "confidence": 0.95
            }
        ],
        "pursue_status": "DO_NOT_PURSUE_YET",
        "do_not_pursue_reason": "High risk of client dissatisfaction: Small factory owners consistently demand end-to-end filing assistance rather than standalone alerts. Standalone willingness to pay remains unproven without packaging full filing services."
    },

    # =========================================================================
    # 2. LEAD_GENERATION
    # =========================================================================
    {
        "title": "Commercial HVAC & Chiller Maintenance Lead Sourcing",
        "opportunity_family": "LEAD_GENERATION",
        "sector": "Commercial Facility Services",
        "customer": "Independent commercial HVAC service and maintenance agencies in NCR. Problem: Facility managers struggle with unreliable AMC providers; quality contractors have no digital lead acquisition. Alternatives: Indiamart leads where 10 vendors fight for the same inquiry.",
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
        "automation_breakdown": {
            "ai_automation": "Parsing facility tonnage specs, screening building chiller history, and matching contractor capabilities.",
            "software_automation": "Automated qualification intake web form, calendar booking for inspection, SMS reminder dispatch.",
            "human_only": "Initial onboarding interview of HVAC service agency to verify technician certifications."
        },
        "competition": "Facility management conglomerates with high overheads and delayed emergency response.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Lead generation is unconstrained. Contractors must hold standard electrical safety licenses and GST registration.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Facility managers and contractors could contract directly for renewals; protected via pay-per-inspection fee model where lead fee is collected upfront prior to meeting.",
        "search_query": "commercial hvac chiller amc rates delhi ncr",
        "evidence_for": [
            "Commercial complexes require quarterly chiller efficiency audits, with AMCs averaging ₹1,200 to ₹2,500 per TR.",
            "ISHRAE surveys indicate commercial buildings spend >35% of total power on chiller operations."
        ],
        "evidence_against": [
            "Over 70% of large commercial buildings in NCR have multi-year contracts locked with OEM vendors (Carrier, Daikin, Blue Star)."
        ],
        "unknowns": [
            "Typical contract value for mid-size (50-200 TR) standalone commercial chiller AMCs in NCR.",
            "Contractor willingness to pay for pre-qualified site inspection meetings."
        ],
        "failure_modes": [
            "Long corporate procurement cycles (60+ days) delay lead monetization.",
            "Facility managers bound by existing multi-year vendor contracts."
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
        "sources": [
            {
                "source_title": "ISHRAE Commercial Chiller Maintenance Standards",
                "source_url": "https://ishrae.in/commercial-chiller-maintenance-rates",
                "source_domain": "ishrae.in",
                "publication_date": "2024-01-10",
                "classification": "FACT",
                "confidence": 0.91
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Industrial Effluent & Sewage Treatment Plant (ETP/STP) AMC Matchmaker",
        "opportunity_family": "LEAD_GENERATION",
        "sector": "Environmental Engineering Services",
        "customer": "CPCB/HSPCB accredited environmental engineering contractors. Problem: Factory owners face HSPCB inspection notices for malfunctioning ETPs but don't know reliable AMC vendors. Alternatives: Cold calls or generic Indiamart directories.",
        "target_market": "Electroplating, chemical, dyeing, and food processing factories in Faridabad & Sonipat",
        "geography": ["Faridabad", "Haryana"],
        "problem": "Factory owners face closure orders due to uncalibrated pH/BOD effluent discharge; environmental AMC vendors struggle to locate factories with immediate remediation needs.",
        "solution": "Pre-qualified lead matching connecting factories facing HSPCB compliance deadlines with certified ETP/STP maintenance teams.",
        "revenue_model": "pay_per_audit_lead",
        "startup_cost": 3500.0,
        "cac": 450.0,
        "customer_value": 3500.0,
        "fulfilment_cost": 300.0,
        "time_to_first_revenue": "21 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Automated analysis of industrial effluent parameters (BOD, COD, TDS) and matching with compliant vendor tech.",
            "software_automation": "Digital intake checklist, automated notification to nearest certified vendor, calendar booking.",
            "human_only": "Confirmation that factory holds a valid HSPCB consent application number."
        },
        "competition": "Individual unorganized environmental consultants operating without service level agreements (SLAs).",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Lead broker does not handle effluent or certify compliance. Partner contractors must possess valid CPCB laboratory certifications.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Mitigated by billing the contractor upfront for the site inspection audit lead rather than trailing commissions.",
        "search_query": "industrial etp stp plant amc cost faridabad haryana",
        "evidence_for": [
            "HSPCB mandates continuous online effluent monitoring systems (OCEMS) for Red category industries.",
            "Mid-size industrial units spend ₹25,000 to ₹60,000 monthly on third-party ETP maintenance AMCs."
        ],
        "evidence_against": [
            "Many factory managers only seek ETP maintenance right after receiving a regulatory penalty notice."
        ],
        "unknowns": [
            "Conversion rate from preliminary site audit into an annual maintenance contract."
        ],
        "failure_modes": [
            "HSPCB enforcement holidays reduce urgency for factory owners to maintain operational ETPs.",
            "Contractors fail to fulfill service standards, leading to disputed lead fees."
        ],
        "experiment": {
            "hypothesis": "3 out of 6 ETP maintenance contractors will commit ₹2,000 for a pre-scheduled factory site audit with verified effluent issues.",
            "validation": "Interview 6 environmental engineering contractors in Faridabad Industrial Area.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "3 contractors agree in writing to pay for validated site audits.",
            "failure_metric": "Fewer than 2 contractors willing to pay for lead without guaranteed AMC.",
            "data_required": ["Contractor minimum plant capacity handled (KLD)", "Standard AMC charges"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Haryana State Pollution Control Board Consent Guidelines",
                "source_url": "https://hspcb.gov.in/consent-management-guidelines-2024",
                "source_domain": "hspcb.gov.in",
                "publication_date": "2024-02-15",
                "classification": "FACT",
                "confidence": 0.96
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Industrial Rooftop Solar EPC Lead Pre-Qualification",
        "opportunity_family": "LEAD_GENERATION",
        "sector": "Commercial Solar Power",
        "customer": "Licensed commercial rooftop solar EPC contractors. Problem: Solar installers waste 70% of engineering survey hours on unqualified prospects with shaded roofs or leased factory premises. Alternatives: Generic bulk leads from Justdial.",
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
        "automation_breakdown": {
            "ai_automation": "Automated satellite roof area estimation, shading analysis from coordinates, and electricity bill load extraction.",
            "software_automation": "Lead validation engine, CRM dispatch to contracted EPC, automated invoicing.",
            "human_only": "Verifying that the lead contact is the registered title owner or managing partner of the factory."
        },
        "competition": "Generic lead brokers (Indiamart, Justdial) selling unverified raw inquiries to multiple bidders.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Lead qualification is non-regulated. EPC partner executes all DISCOM grid connectivity filings.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Lead is sold exclusively to one pre-vetted EPC contractor per cluster; contractor pays upon delivery of verified satellite audit package.",
        "search_query": "solar epc lead generation cost india installer survey",
        "evidence_for": [
            "Clean Energy India reports EPCs spend ₹1,000 to ₹2,200 per validated rooftop lead with verifiable power bills.",
            "Average commercial rooftop system size in NCR is 50 kW to 250 kW with contract values exceeding ₹20 lakh."
        ],
        "evidence_against": [
            "EPCs report high fatigue with third-party digital leads due to past experiences with low-intent inquiries."
        ],
        "unknowns": [
            "Average sales closing cycle duration for 50 kW systems in Haryana (typically 60-120 days)."
        ],
        "failure_modes": [
            "Installers dispute lead quality when factory owners delay CAPEX decisions.",
            "Customer acquisition costs for acquiring factory leads via digital ads exceed ₹1,000."
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
        "sources": [
            {
                "source_title": "Clean Energy India Solar EPC Acquisition Analysis",
                "source_url": "https://cleanenergyindia.org/reports/epc-acquisition-costs",
                "source_domain": "cleanenergyindia.org",
                "publication_date": "2024-03-10",
                "classification": "ESTIMATE",
                "confidence": 0.90
            }
        ],
        "pursue_status": "DO_NOT_PURSUE_YET",
        "do_not_pursue_reason": "Severe EPC buyer fatigue: Solar EPC contractors in NCR report extensive disillusionment with digital lead sellers; requiring guaranteed project closure rather than paying for site audits. Unit economics unviable until high-touch trust is established."
    },

    # =========================================================================
    # 3. SERVICE_ARBITRAGE
    # =========================================================================
    {
        "title": "Factory Pollution Control (HSPCB) Consent-to-Operate Administrative Filing Desk",
        "opportunity_family": "SERVICE_ARBITRAGE",
        "sector": "Environmental Compliance Administration",
        "customer": "Green and Orange category small manufacturing workshops in Faridabad. Problem: Navigating the OCMMS (Online Consent Management and Monitoring System) portal is complex; missing submissions trigger heavy fines. Existing alternatives: Informal liaison agents charging ₹30,000+ with zero transparency.",
        "target_market": "Small fabrication, plastics, and casting units in Faridabad",
        "geography": ["Faridabad", "Haryana"],
        "problem": "Factory owners lack specialized staff to prepare mandatory CTE/CTO online documentation, risk show-cause notices and electricity disconnection.",
        "solution": "Standardized administrative document compilation and referral desk linking factory records with certified environmental testing laboratories.",
        "revenue_model": "administrative_service_fee",
        "startup_cost": 3500.0,
        "cac": 450.0,
        "customer_value": 3500.0,
        "fulfilment_cost": 300.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Extracting machinery lists, DG set capacity, and raw material inputs from factory purchase bills into standard HSPCB annexures.",
            "software_automation": "Portal document upload packaging, reminder triggers for annual CTO renewal dates.",
            "human_only": "Review of the final application package with factory owner before formal OCMMS submission."
        },
        "competition": "Traditional local liaison touts operating offline with zero digital tracking or transparent pricing.",
        "regulatory_complexity": "MEDIUM",
        "regulatory_considerations": "Strictly administrative assistance and document preparation. Platform clearly disclaims legal/environmental counsel and refers stack monitoring to NABL-accredited labs.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Factory owners prefer outsourcing repetitive annual compliance paperwork to save management time; recurring annual renewals protect relationship.",
        "search_query": "hspcb consent to operate documentation cost faridabad",
        "evidence_for": [
            "HSPCB mandates online consent filings for all manufacturing units operating in notified industrial areas.",
            "Penalty for delayed CTO renewal includes 100% additional consent fee and potential power disconnection notices."
        ],
        "evidence_against": [
            "Certain factory owners expect informal regulatory influence rather than compliant digital documentation."
        ],
        "unknowns": [
            "Turnaround time of HSPCB regional office for approving green-category renewals submitted digitally."
        ],
        "failure_modes": [
            "Portal policy changes requiring biometric or physical verification by authorized factory partner.",
            "Factory fails to rectify underlying non-compliant emissions and blames documentation assistant."
        ],
        "experiment": {
            "hypothesis": "3 out of 10 small factory owners in Sector 24 will pay ₹2,500 for a pre-audit document readiness check for their upcoming CTO renewal.",
            "validation": "Review upcoming CTO renewal dates of 10 local units via public HSPCB portal registers and offer document compilation.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "3 factory owners commission document preparation.",
            "failure_metric": "Less than 2 factory owners express interest.",
            "data_required": ["Sanctioned factory power load", "DG set acoustic enclosure certificate"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "HSPCB Consent Management Guidelines",
                "source_url": "https://hspcb.gov.in/consent-management-guidelines-2024",
                "source_domain": "hspcb.gov.in",
                "publication_date": "2024-02-15",
                "classification": "FACT",
                "confidence": 0.95
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "CNC Machine Precision Tooling & Spare Parts Sourcing Concierge",
        "opportunity_family": "SERVICE_ARBITRAGE",
        "sector": "Industrial Machine Tooling",
        "customer": "CNC lathe, VMC, and auto-part machine shop operators in Faridabad. Problem: Urgent machine breakdowns due to broken carbide inserts, collets, or spindle belts cause production stoppages. Alternatives: Owner drives 3 hours to Delhi Chawri Bazar wholesale markets.",
        "target_market": "Over 1,200 CNC job shops across Faridabad and Ballabgarh",
        "geography": ["Faridabad", "Delhi-NCR"],
        "problem": "Machine shops lose ₹3,000 to ₹8,000 per hour during machine breakdowns while searching for specialized cutting tools and replacement spares.",
        "solution": "WhatsApp-based emergency tooling concierge identifying distributor inventory across NCR and arranging same-day bike courier dispatch.",
        "revenue_model": "sourcing_markup",
        "startup_cost": 3000.0,
        "cac": 350.0,
        "customer_value": 3000.0,
        "fulfilment_cost": 250.0,
        "time_to_first_revenue": "10 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Image recognition of broken tool markings, carbide grade translation, and equivalent specification matching.",
            "software_automation": "Automated stock check inquiry to NCR wholesale tooling distributors via WhatsApp API.",
            "human_only": "Dispatch coordination with local on-demand bike courier (Porter/Borzo)."
        },
        "competition": "Local retail hardware stores with limited specialized CNC inventory and slow ordering lead times.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Standard B2B trade of industrial goods with GST invoicing. No specialized licensing needed.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Distributors in Delhi do not service individual small emergency orders from Faridabad workshops directly due to transport friction; concierge aggregates volume.",
        "search_query": "cnc tooling spare parts distributor procurement delhi faridabad",
        "evidence_for": [
            "TAGMA reports small machine workshops experience tooling delivery delays of 3-7 days, paying 15-25% spot premiums for emergency orders.",
            "CNC job shops operate on tight production delivery penalties with automotive OEMs."
        ],
        "evidence_against": [
            "Machine shop owners may attempt to contact the matched distributor directly on subsequent orders."
        ],
        "unknowns": [
            "Average monthly emergency tooling order frequency per machine shop."
        ],
        "failure_modes": [
            "Incorrect tool specification delivered resulting in part damage and refund dispute.",
            "Courier delay during peak transit hours across NCR border."
        ],
        "experiment": {
            "hypothesis": "At least 4 machine shop owners will place an emergency sourcing request when offered guaranteed 4-hour delivery of standard carbide inserts.",
            "validation": "Survey 12 machine shop supervisors in Sector 6 Faridabad.",
            "budget": 0.0,
            "duration": "4 days",
            "success_metric": "4 supervisors save concierge WhatsApp contact and request price quote.",
            "failure_metric": "Fewer than 2 shops interested in delivery service.",
            "data_required": ["Common insert grades (e.g., CNMG, WNMG)", "Monthly tooling expenditure"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "TAGMA Tooling Procurement Index",
                "source_url": "https://tagma-india.org/tooling-procurement-index-2024",
                "source_domain": "tagma-india.org",
                "publication_date": "2024-02-18",
                "classification": "ESTIMATE",
                "confidence": 0.90
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "NABL Accredited Lab Calibration & Material Testing Booking Desk",
        "opportunity_family": "SERVICE_ARBITRAGE",
        "sector": "Industrial Quality & Metrology",
        "customer": "Export-oriented auto-component manufacturers in Haryana needing periodic ISO calibration for micrometers, verniers, and tensile test certificates. Problem: Contacting multiple testing labs to compare lead times is time-consuming. Alternatives: Manual sample dispatch with slow turnaround.",
        "target_market": "Tier 2 and Tier 3 automotive component suppliers in Haryana",
        "geography": ["Haryana", "Delhi-NCR"],
        "problem": "Delays in obtaining NABL-accredited calibration certificates hold up customer shipments and ISO/IATF 16949 audit compliance.",
        "solution": "Digital calibration dispatch desk aggregating testing capacity across accredited metrology labs to guarantee 48-hour certificate turnaround.",
        "revenue_model": "lab_referral_and_booking_fee",
        "startup_cost": 2500.0,
        "cac": 300.0,
        "customer_value": 2500.0,
        "fulfilment_cost": 200.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Extracting instrument serial numbers and required tolerance grades from customer audit sheets.",
            "software_automation": "Routing test batches to lowest-backlog accredited lab, tracking certificate download status.",
            "human_only": "Handling instrument handover and fragile logistics insurance."
        },
        "competition": "Individual accredited labs with slow sales desks and zero integrated logistics support.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Service acts purely as booking and logistics coordinator. Partner laboratories must hold valid NABL accreditation ISO/IEC 17025.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Labs welcome aggregated volume and provide 15-20% commission; manufacturers benefit from single contact point for multiple test types (chemical, mechanical, dimensional).",
        "search_query": "nabl accredited calibration lab testing booking fee haryana",
        "evidence_for": [
            "Automotive Tier 1 clients mandate annual NABL calibration certificates for all measuring gauges used in production.",
            "Over 60 accredited testing labs in Delhi-NCR operate with irregular capacity utilization."
        ],
        "evidence_against": [
            "Large manufacturers often have in-house standard rooms for basic gauge calibration."
        ],
        "unknowns": [
            "Tolerance for third-party courier handling of high-precision optical or electronic gauges."
        ],
        "failure_modes": [
            "Laboratory certificate delay beyond promised 48-hour window due to instrument failure.",
            "Damage to precision gauge during third-party transit."
        ],
        "experiment": {
            "hypothesis": "3 quality managers will route their next batch of gauge calibrations through the desk upon guarantee of 48-hour turnaround.",
            "validation": "Interview 8 quality control managers in Faridabad auto-component cluster.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "3 quality managers provide list of gauges due for renewal.",
            "failure_metric": "Managers refuse to use non-OEM calibration channels.",
            "data_required": ["Gauge calibration cycle", "Annual calibration budget"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Quality Council of India NABL Directory",
                "source_url": "https://nabl-india.org/accredited-laboratories-directory",
                "source_domain": "nabl-india.org",
                "publication_date": "2024-01-20",
                "classification": "FACT",
                "confidence": 0.96
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },

    # =========================================================================
    # 4. PROCESS_AUTOMATION
    # =========================================================================
    {
        "title": "Wholesale Trader E-Way Bill & Transit Expiry Pre-Check Bot",
        "opportunity_family": "PROCESS_AUTOMATION",
        "sector": "Wholesale Trade Logistics",
        "customer": "Wholesale commodity, hardware, and automotive parts distributors in Haryana dispatching 5+ inter-state trucks daily. Problem: Vehicle breakdowns or traffic delays lead to expired E-Way bills, resulting in 100% tax penalties by state GST flying squads. Alternatives: Manual tracking by busy dispatch clerks.",
        "target_market": "Traders and logistics dispatchers in Haryana and Delhi-NCR",
        "geography": ["Faridabad", "Haryana", "Delhi-NCR"],
        "problem": "Goods vehicles get impounded with massive tax penalties due to clerical errors on E-Way bill validity expiry and HSN codes.",
        "solution": "Automated WhatsApp pre-dispatch verification bot checking vehicle numbers and transit time validity before truck departure.",
        "revenue_model": "monthly_subscription",
        "startup_cost": 3000.0,
        "cac": 350.0,
        "customer_value": 2800.0,
        "fulfilment_cost": 200.0,
        "time_to_first_revenue": "10 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "OCR extraction of transporter copy invoice and E-Way bill barcode from WhatsApp photos.",
            "software_automation": "API verification of GST E-Way bill validity, distance-to-expiry calculation, automated WhatsApp alert.",
            "human_only": "Initial onboarding setup of trader's GST credentials on secure local token."
        },
        "competition": "Enterprise ERPs (SAP, Tally Prime) that generate bills but lack proactive real-time driver WhatsApp transit tracking.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Complies with GST rules; does not alter tax liability. Read-only validation tool with end-to-end data encryption.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Traders lack software engineering capacity to build custom WhatsApp bot integrations; strong retention once integrated into daily dispatch flow.",
        "search_query": "eway bill validity expiry penalty gst haryana wholesale",
        "evidence_for": [
            "GST Section 129 mandates penalty equal to 200% of tax payable for goods transported with expired or erroneous E-Way bills.",
            "Over 10,000 inter-state commercial vehicles transit Haryana border check-posts daily."
        ],
        "evidence_against": [
            "Commercial tax authorities hold the transporter and consignor strictly liable regardless of software verification."
        ],
        "unknowns": [
            "Frequency with which small wholesale traders extend E-Way bills during transit breakdowns."
        ],
        "failure_modes": [
            "WhatsApp Business API policy restrictions on transactional messaging templates.",
            "Driver fails to check phone alerts when vehicle is delayed."
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
        "sources": [
            {
                "source_title": "GST Council E-Way Bill Rules and Notifications",
                "source_url": "https://ewaybillgst.gov.in/rules-circulars",
                "source_domain": "ewaybillgst.gov.in",
                "publication_date": "2024-01-01",
                "classification": "FACT",
                "confidence": 0.95
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "B2B Manufacturer Section 43B(h) MSME Supplier Payment Tracker",
        "opportunity_family": "PROCESS_AUTOMATION",
        "sector": "Corporate Financial Operations",
        "customer": "Mid-sized manufacturing companies with 50+ vendors. Problem: Finance Act amendment Section 43B(h) disallows tax deductions for amounts owed to MSE suppliers past 45 days. Alternatives: Manual Excel spreadsheets or expensive ERP modifications.",
        "target_market": "Mid-market manufacturing firms across India",
        "geography": ["Pan-India", "Online"],
        "problem": "Companies face unexpected corporate income tax liabilities due to delayed payments to registered Micro and Small enterprises.",
        "solution": "Lightweight Google Sheets / Excel cloud add-in that checks vendor MSME Udyam status via API and flags invoices approaching day 30 and 40.",
        "revenue_model": "monthly_saas_subscription",
        "startup_cost": 4000.0,
        "cac": 500.0,
        "customer_value": 3500.0,
        "fulfilment_cost": 250.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Parsing vendor invoices to detect Udyam registration numbers and classify supplier enterprise size (Micro vs Small vs Medium).",
            "software_automation": "Automated payment aging dashboard, daily escalation alerts to accounts payable via email/Slack.",
            "human_only": "None required post-onboarding."
        },
        "competition": "Large accounting firms offering manual one-time MSME vendor classification audits at ₹75,000+.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Purely analytical tracker tool. Not a chartered accountant audit opinion; includes standard accounting software disclaimer.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Software runs locally or in cloud sheet; clients rely on ongoing automated Udyam API verification and aging calculations.",
        "search_query": "section 43bh msme 45 days payment tracker excel software india",
        "evidence_for": [
            "CBIC guidelines confirm Section 43B(h) applicability from FY 2023-24, disallowing deductions for delayed MSE payments on accrual basis.",
            "MSME Ministry reports over 2 crore registered Udyam units eligible for statutory 45-day settlement."
        ],
        "evidence_against": [
            "Many large corporate buyers pressure suppliers to give declarations waiving or disputing micro-enterprise status."
        ],
        "unknowns": [
            "Willingness of mid-size accounts departments to install third-party spreadsheet add-ins vs manual calculations."
        ],
        "failure_modes": [
            "Government extends compliance deadlines or relaxes enforcement under industry lobbying pressure.",
            "Client fails to input purchase invoices on time, rendering 45-day alerts ineffective."
        ],
        "experiment": {
            "hypothesis": "3 out of 10 finance managers at mid-size manufacturing units will subscribe to a ₹1,999/month automated 43B(h) aging dashboard.",
            "validation": "Share a 1-click free trial demo spreadsheet with 10 finance heads in Gurgaon/Faridabad.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "3 finance managers request integration with their vendor database.",
            "failure_metric": "Finance heads report their CA has already resolved this manually.",
            "data_required": ["Active vendor count", "Existing accounting software used"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "CBIC Section 43B(h) Guidance Note",
                "source_url": "https://cbic.gov.in/guidelines-section-43bh",
                "source_domain": "cbic.gov.in",
                "publication_date": "2024-04-10",
                "classification": "FACT",
                "confidence": 0.94
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Transporter Toll & Fastag Reconciliation Anomaly Alert Desk",
        "opportunity_family": "PROCESS_AUTOMATION",
        "sector": "Commercial Fleet Logistics",
        "customer": "Commercial fleet operators with 5 to 25 trucks operating on NH-48 and Western Peripheral Expressway (WPE). Problem: Toll plazas frequently double-deduct or incorrectly charge higher axle classes, costing ₹3,000 to ₹10,000 per truck monthly. Alternatives: Manual Fastag bank statement review.",
        "target_market": "Fleet operators in Haryana and NCR",
        "geography": ["Haryana", "Delhi-NCR"],
        "problem": "Fleet owners lose significant operating margin to erroneous electronic toll deductions that expire past the 15-day dispute window.",
        "solution": "Automated Fastag deduction scraper matching GPS vehicle trip logs against toll deductions to automatically draft refund dispute tickets.",
        "revenue_model": "percentage_of_recovered_refunds",
        "startup_cost": 3500.0,
        "cac": 400.0,
        "customer_value": 3000.0,
        "fulfilment_cost": 250.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Matching trip route coordinates with toll plaza geofences to detect phantom or incorrect plaza charges.",
            "software_automation": "Automated dispute ticket submission to issuing Fastag bank API / NPCI portal.",
            "human_only": "Escalation to NHAI nodal officer for unresolved disputes."
        },
        "competition": "Enterprise telematics providers charging ₹800/month/truck with hardware lock-in.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Dispute filing is authorized by NPCI / NHAI Fastag consumer dispute mechanisms.",
        "platform_dependency": "MEDIUM",
        "disintermediation_analysis": "Fleet owners lack time to manually file 30+ dispute tickets per month across multiple banks (ICICI, PayTM, IDFC).",
        "search_query": "fastag wrong deduction refund dispute time limit fleet haryana",
        "evidence_for": [
            "IHMCL guidelines mandate Fastag dispute resolution within 30 days of ticket logging.",
            "Commercial trucks on NCR highways incur between ₹15,000 and ₹40,000 in monthly electronic toll transactions."
        ],
        "evidence_against": [
            "Issuing banks often take 45 to 60 days to credit dispute refunds, delaying success fee collection."
        ],
        "unknowns": [
            "Historical percentage of wrong-deduction tickets successfully resolved in cash refunds vs rejected."
        ],
        "failure_modes": [
            "Bank dispute APIs become inaccessible or require physical OTP authentication from fleet owner.",
            "Refund cycle exceeds 60 days, straining operating cash flows."
        ],
        "experiment": {
            "hypothesis": "At least 3 fleet owners with 10+ trucks will grant statement access for a 50% split on all recovered toll overcharges.",
            "validation": "Interview 5 transport managers in Faridabad Transport Nagar.",
            "budget": 0.0,
            "duration": "4 days",
            "success_metric": "3 fleet owners provide Fastag statements for automated audit.",
            "failure_metric": "Fleet owners unwilling to share statement data.",
            "data_required": ["Fleet size", "Primary Fastag issuing bank"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Indian Highway Management Company Limited (IHMCL) Fastag Guidelines",
                "source_url": "https://ihmcl.co.in/dispute-resolution-policy",
                "source_domain": "ihmcl.co.in",
                "publication_date": "2024-01-15",
                "classification": "FACT",
                "confidence": 0.93
            }
        ],
        "pursue_status": "DO_NOT_PURSUE_YET",
        "do_not_pursue_reason": "Severe settlement cycle friction: Issuing banks and NPCI take 45-60+ days to credit disputed toll charges. A success-fee revenue model cannot achieve first revenue within 30 days without carrying upfront financial exposure."
    },

    # =========================================================================
    # 5. DISTRIBUTION_ARBITRAGE
    # =========================================================================
    {
        "title": "Commercial 20L Bulk Water Jar & Dispenser Supply Contract Matcher",
        "opportunity_family": "DISTRIBUTION_ARBITRAGE",
        "sector": "Commercial Facility Supplies",
        "customer": "Factory, warehouse, and office administrative managers in Faridabad industrial zones. Problem: Summer water shortages and erratic deliveries by local unbranded water jar suppliers. Alternatives: Paying high spot prices or purchasing single-use bottles.",
        "target_market": "Factories and commercial offices in Faridabad",
        "geography": ["Faridabad", "Haryana"],
        "problem": "Factories suffer frequent summer supply stockouts of drinking water jars, impacting worker productivity and labor compliance.",
        "solution": "Digital contract aggregation connecting factory procurement with certified BIS/FSSAI-licensed water bottling plants for scheduled automated daily replenishment.",
        "revenue_model": "per_jar_recurring_commission",
        "startup_cost": 2500.0,
        "cac": 300.0,
        "customer_value": 2500.0,
        "fulfilment_cost": 150.0,
        "time_to_first_revenue": "7 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Forecasting daily factory water consumption based on worker headcount and ambient temperature forecasts.",
            "software_automation": "Automated dispatch route generation, daily digital delivery slip confirmation via WhatsApp.",
            "human_only": "Physical delivery handled entirely by partner bottling plant logistics trucks."
        },
        "competition": "Unorganized local water delivery boys with poor hygiene records and frequent unannounced supply failures.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Distributor partner plants must possess FSSAI and BIS IS 14543 certifications. Service acts as contract aggregator and billing coordinator.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Bottling plants prefer guaranteed monthly institutional accounts and happily pay ₹10-15 margin per jar; factories prefer centralized digital invoicing.",
        "search_query": "commercial 20l water jar supplier contract faridabad",
        "evidence_for": [
            "Factories Act Section 18 mandates factory provision of cool wholesome drinking water for all industrial workers.",
            "Industrial factories in Faridabad consume an average of 15 to 40 twenty-liter jars daily during summer months."
        ],
        "evidence_against": [
            "Unlicensed local informal water suppliers dump non-purified water jars at predatory rates of ₹20-25 per jar."
        ],
        "unknowns": [
            "Willingness of small factory managers to pay ₹40-50 per jar for verified BIS certified water vs cheap unbranded jars."
        ],
        "failure_modes": [
            "Bottling plant vehicle breakdown causes delivery failure during heatwaves.",
            "Factory defaults on monthly consolidated water supply invoices."
        ],
        "experiment": {
            "hypothesis": "At least 4 factory managers will switch to a reliable BIS-certified water supplier on a 1-week paid trial with zero dispenser deposit.",
            "validation": "Pitch trial supply to 10 factory managers in Sector 59 Faridabad.",
            "budget": 0.0,
            "duration": "4 days",
            "success_metric": "4 factories agree to 1-week test delivery.",
            "failure_metric": "Less than 2 factories interested; managers satisfied with existing informal vendors.",
            "data_required": ["Current daily jar consumption", "Current price paid per jar"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Food Safety and Standards Authority of India (FSSAI) Packaged Water Regulations",
                "source_url": "https://fssai.gov.in/packaged-drinking-water-standards",
                "source_domain": "fssai.gov.in",
                "publication_date": "2023-10-12",
                "classification": "FACT",
                "confidence": 0.95
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Corrugated Box & Surplus Industrial Packaging Material Matchmaker",
        "opportunity_family": "DISTRIBUTION_ARBITRAGE",
        "sector": "Industrial Packaging & Logistics Materials",
        "customer": "Manufacturing workshops and online sellers with irregular order batches. Problem: Box manufacturers require minimum order quantities (MOQs) of 1,000+ units with 14-day lead times. Alternatives: Paying 40-50% markups at retail packing stores.",
        "target_market": "Small manufacturers and e-commerce shippers in Faridabad",
        "geography": ["Faridabad", "Haryana"],
        "problem": "Small businesses cannot afford custom corrugated box runs and must overpay for retail packing materials, while large converters hold surplus overruns.",
        "solution": "Surplus packaging clearinghouse indexing overrun box inventories from local corrugators and matching them to small factory shippers.",
        "revenue_model": "brokerage_margin",
        "startup_cost": 3000.0,
        "cac": 350.0,
        "customer_value": 2800.0,
        "fulfilment_cost": 200.0,
        "time_to_first_revenue": "10 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Dimensional tolerance matching (length, width, height, ply strength) between surplus stock and buyer requirements.",
            "software_automation": "Real-time inventory listing bot on WhatsApp, automated purchase order generation.",
            "human_only": "Verification of box moisture and bursting strength on initial warehouse intake."
        },
        "competition": "Local retail packaging stores with high markups and no dimension matching software.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Standard trading of commercial paper goods with GST invoices.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Corrugators do not want retail customers walking into large manufacturing plants; they prefer an intermediary liquidating surplus lots.",
        "search_query": "corrugated box surplus manufacturer inventory faridabad",
        "evidence_for": [
            "FIPI reports secondary packaging boxes and overruns have a liquidation velocity of under 10 days in automotive clusters.",
            "Corrugated box converters routinely generate 3-5% overrun batches on custom customer orders."
        ],
        "evidence_against": [
            "Buyer products may require precise bespoke printing that generic surplus boxes cannot fulfill."
        ],
        "unknowns": [
            "Average warehouse storage time before surplus box lots are fully liquidated."
        ],
        "failure_modes": [
            "Buyer rejects surplus boxes due to branding or printing mismatches.",
            "Moisture damage to stored surplus boxes during monsoon season."
        ],
        "experiment": {
            "hypothesis": "3 corrugators will list their surplus/overrun box inventory, and 3 small shippers will purchase lots at 25% discount to retail.",
            "validation": "Catalog surplus inventory from 3 packaging converters in Faridabad.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "At least 1 matched transaction completed within 5 days.",
            "failure_metric": "Zero buyers willing to purchase unprinted/overrun dimensions.",
            "data_required": ["Surplus box dimensions", "Ply rating (3-ply vs 5-ply)"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Federation of Indian Packaging Industry Market Bulletin",
                "source_url": "https://fipi.org.in/industrial-packaging-circular-economy",
                "source_domain": "fipi.org.in",
                "publication_date": "2024-03-05",
                "classification": "ESTIMATE",
                "confidence": 0.89
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Industrial Safety Equipment & PPE Bulk Restocking Coordinator",
        "opportunity_family": "DISTRIBUTION_ARBITRAGE",
        "sector": "Industrial Safety & Hygiene",
        "customer": "Factory safety officers and procurement clerks in Faridabad industrial estates. Problem: Spot replenishment of ISI safety shoes, helmets, cut-resistant gloves, and earplugs from retail shops costs 25-30% more than wholesale. Alternatives: Direct manufacturer orders that require large MOQs.",
        "target_market": "Automotive ancillary and casting factories in Faridabad",
        "geography": ["Faridabad", "Haryana"],
        "problem": "Factory safety audits trigger urgent restocking requirements that retail hardware vendors exploit with predatory spot markups.",
        "solution": "Scheduled monthly PPE replenishment subscription aggregating orders across 15 factories to negotiate master distributor wholesale pricing.",
        "revenue_model": "distributor_margin_spread",
        "startup_cost": 3500.0,
        "cac": 400.0,
        "customer_value": 3200.0,
        "fulfilment_cost": 250.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Predicting monthly glove and mask consumption based on factory worker shift counts.",
            "software_automation": "Consolidated procurement order generation, automated distributor RFQ matching, delivery tracking.",
            "human_only": "Initial safety officer meeting to approve certified PPE product samples."
        },
        "competition": "Local retail hardware traders and generic e-commerce sites with delayed industrial delivery.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "PPE products must conform to Bureau of Indian Standards (BIS) safety norms. Trade requires standard GST registration.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Distributors require consolidated ₹50,000+ order sizes to give wholesale discounts; small factories ordering ₹5,000/month cannot buy directly.",
        "search_query": "industrial ppe safety shoes gloves wholesale supplier faridabad",
        "evidence_for": [
            "Factories Act 1948 Section 32 & 41 mandates mandatory provision of protective footwear, goggles, and gloves for hazardous processes.",
            "Auto component factories replace worker gloves every 7-14 days, creating dependable recurring replenishment demand."
        ],
        "evidence_against": [
            "Factories frequently delay monthly invoice payments for PPE by 60-90 days."
        ],
        "unknowns": [
            "Willingness of safety officers to commit to automated monthly reordering instead of ad-hoc spot buying."
        ],
        "failure_modes": [
            "Wholesale distributor experiences stockouts of specific certified safety shoe sizes.",
            "Factory defaults on payment following product delivery."
        ],
        "experiment": {
            "hypothesis": "3 factory safety officers will agree to a recurring monthly safety glove and helmet replenishment plan at a 15% discount to retail.",
            "validation": "Quote monthly glove rates to 8 factory safety officers in Sector 25 Faridabad.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "3 safety officers place a test replenishment order.",
            "failure_metric": "Less than 2 safety officers interested in changing vendors.",
            "data_required": ["Monthly glove pairs consumed", "Target safety shoe brands"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Directorate General Factory Advice Service and Labour Institutes (DGFASLI)",
                "source_url": "https://dgfasli.gov.in/occupational-safety-regulations",
                "source_domain": "dgfasli.gov.in",
                "publication_date": "2024-01-10",
                "classification": "FACT",
                "confidence": 0.94
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },

    # =========================================================================
    # 6. LEGITIMATE_INCENTIVE_SERVICES
    # =========================================================================
    {
        "title": "Rooftop Solar PM Surya Ghar Subsidy Application Navigation Desk",
        "opportunity_family": "LEGITIMATE_INCENTIVE_SERVICES",
        "sector": "Residential Renewable Energy Subsidies",
        "customer": "Homeowners and Resident Welfare Associations (RWAs) applying for up to ₹78,000 central subsidy under PM Surya Ghar Muft Bijli Yojana. Problem: Applicants face rejection due to electricity bill name mismatches or incorrect DISCOM consumer numbers. Alternatives: Confusing government national portal.",
        "target_market": "Homeowners and residential societies in Haryana and Delhi-NCR",
        "geography": ["Haryana", "Delhi-NCR"],
        "problem": "Eligible homeowners struggle with the technical documentation, vendor empanelment selection, and inspection tracking required to release subsidies.",
        "solution": "Step-by-step administrative navigation desk providing document pre-validation, DISCOM name alignment guidance, and subsidy release tracking.",
        "revenue_model": "fixed_navigation_service_fee",
        "startup_cost": 2000.0,
        "cac": 250.0,
        "customer_value": 1500.0,
        "fulfilment_cost": 150.0,
        "time_to_first_revenue": "7 days",
        "recurring_potential": "LOW",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Automated OCR checking of Aadhaar vs electricity bill name spelling and roof ownership document validation.",
            "software_automation": "Portal status scraping, automated SMS progress alerts to applicant on DISCOM net-meter inspection.",
            "human_only": "None required; applicant submits their own verified package using the generated checklist."
        },
        "competition": "Rooftop solar installers who promise to handle paperwork but deprioritize administrative follow-ups once hardware is paid for.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Strictly administrative navigation assistance. Does not represent the Ministry or guarantee subsidy disbursal; client retains full control of government login.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Applicants can apply directly for free on pmsuryaghar.gov.in, but over 40% experience application query defects; they happily pay ₹1,000-1,500 for error-free submission guidance.",
        "search_query": "pm surya ghar subsidy application guidelines haryana dhbvn",
        "evidence_for": [
            "Ministry of New and Renewable Energy launched PM Surya Ghar with ₹75,000 Cr outlay providing ₹30,000/kW up to ₹78,000 for 3kW systems.",
            "DHBVN and UHBVN have approved simplified net metering procedures for residential consumers in Haryana."
        ],
        "evidence_against": [
            "Installers sometimes claim they provide free paperwork, though consumer complaints highlight post-installation abandonment."
        ],
        "unknowns": [
            "Average time between net-meter installation and central subsidy direct bank transfer in Haryana."
        ],
        "failure_modes": [
            "DISCOM net-metering meter shortages delay final commissioning by 3+ months.",
            "Applicant's roof structure fails DISCOM shadow or load-bearing inspection."
        ],
        "experiment": {
            "hypothesis": "At least 5 homeowners planning solar installation will pay ₹999 for complete pre-validation and subsidy tracking assistance.",
            "validation": "Offer document pre-audit assistance on 2 local Faridabad homeowner WhatsApp groups.",
            "budget": 0.0,
            "duration": "4 days",
            "success_metric": "5 homeowners engage and book pre-validation audit.",
            "failure_metric": "Homeowners refuse to pay for government portal assistance.",
            "data_required": ["Monthly electricity units consumed", "Roof ownership type"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "PM Surya Ghar National Portal Guidelines",
                "source_url": "https://pmsuryaghar.gov.in/scheme-guidelines",
                "source_domain": "pmsuryaghar.gov.in",
                "publication_date": "2024-02-15",
                "classification": "FACT",
                "confidence": 0.98
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "MSME ZED (Zero Defect Zero Effect) Certification Grant Navigation Desk",
        "opportunity_family": "LEGITIMATE_INCENTIVE_SERVICES",
        "sector": "Industrial Quality Certification Subsidies",
        "customer": "Manufacturing MSMEs eligible for up to 80% subsidy on certification fees and ₹5 lakh handholding consultancy grants under the Ministry of MSME. Problem: Extensive 20-parameter self-assessment requirements cause small factory owners to abandon applications. Alternatives: Expensive ISO consultants charging ₹50,000+.",
        "target_market": "Registered Micro and Small manufacturing units in Haryana",
        "geography": ["Haryana", "Pan-India"],
        "problem": "MSMEs miss out on government financial grants of up to ₹5 lakh and 0.5% interest rate concessions on bank loans due to difficulty navigating ZED portal audits.",
        "solution": "Self-assessment gap analysis desk helping factory managers collect and upload mandatory evidence parameters for Bronze/Silver ZED certification.",
        "revenue_model": "preparation_service_fee",
        "startup_cost": 3000.0,
        "cac": 400.0,
        "customer_value": 3500.0,
        "fulfilment_cost": 250.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "MEDIUM",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Evaluating factory safety policies, calibration records, and scrap reduction measures against ZED 20-parameter rubric.",
            "software_automation": "Evidence packaging into standardized ZED audit upload format, automated deadline alerts.",
            "human_only": "Onboarding review of factory machinery photos and safety gear compliance."
        },
        "competition": "Traditional ISO consulting agencies charging ₹40,000 to ₹100,000 without leveraging government subsidy reimbursements.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Administrative guidance and evidence formatting. Does not perform official accreditation; official audit is performed exclusively by QCI empaneled assessors.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "MSMEs rely on the structured preparation toolkit to pass the QCI desktop audit without failing on missing parameter attachments.",
        "search_query": "msme zed certification scheme subsidy eligibility guidelines",
        "evidence_for": [
            "Ministry of MSME provides 80% subsidy for Micro, 60% for Small, and 50% for Medium enterprises on ZED certification fees.",
            "State Bank of India and SIDBI offer 0.5% interest rate concessions to ZED-certified units."
        ],
        "evidence_against": [
            "Factory owners must physically implement waste management and safety measures before passing desk audit."
        ],
        "unknowns": [
            "Average time required for QCI desktop assessment approval after application submission."
        ],
        "failure_modes": [
            "Factory fails remote desktop audit due to fabricated or inadequate on-site photographs.",
            "Government subsidy budget for ZED consultancy grants is temporarily exhausted."
        ],
        "experiment": {
            "hypothesis": "3 small machine shop owners will pay ₹2,500 for a ZED Bronze pre-audit gap assessment to claim up to ₹5 lakh in government financial assistance.",
            "validation": "Present ZED subsidy opportunity to 8 factory managers in Faridabad.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "3 factory managers commission the pre-audit assessment.",
            "failure_metric": "Zero managers interested in government certification schemes.",
            "data_required": ["MSME Udyam registration certificate", "Current ISO status"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Ministry of MSME ZED Scheme Portal",
                "source_url": "https://zed.msme.gov.in/guidelines",
                "source_domain": "msme.gov.in",
                "publication_date": "2024-03-01",
                "classification": "FACT",
                "confidence": 0.95
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Haryana Apprenticeship & Local Candidate Employment Subsidy Navigation",
        "opportunity_family": "LEGITIMATE_INCENTIVE_SERVICES",
        "sector": "Workforce Statutory Subsidies",
        "customer": "Industrial factories with >30 workers required to maintain apprentices under the Apprenticeship Act. Problem: Eligible for ₹1,500/month stipend reimbursement under NAPS (National Apprenticeship Promotion Scheme), but paperwork delays cause claims to lapse. Alternatives: Factory HR doing manual portal entries.",
        "target_market": "Manufacturing units in Haryana",
        "geography": ["Haryana"],
        "problem": "Industrial employers lose ₹18,000 per apprentice annually in unclaimed government stipend reimbursements due to confusing portal filing workflows.",
        "solution": "Administrative filing desk preparing and submitting monthly NAPS attendance and stipend reimbursement claims on behalf of industrial employers.",
        "revenue_model": "per_apprentice_monthly_fee",
        "startup_cost": 2500.0,
        "cac": 350.0,
        "customer_value": 2400.0,
        "fulfilment_cost": 150.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Validating apprentice contract documents, Aadhaar linkage, and bank account seeding against portal format.",
            "software_automation": "Automated monthly payroll-to-stipend reconciliation, bulk attendance upload formatting.",
            "human_only": "None once employer authorization is registered on the portal."
        },
        "competition": "General payroll processing software that lacks dedicated NAPS government reimbursement claim workflows.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Portal filing assistance authorized by designated employer representative. Purely administrative clerical execution.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Employers lack administrative bandwidth to follow up on monthly reimbursement delays with state apprenticeship advisers.",
        "search_query": "naps apprenticeship stipend reimbursement haryana portal",
        "evidence_for": [
            "NAPS guidelines provide 25% of prescribed stipend up to ₹1,500 per month per apprentice directly to the employer or apprentice.",
            "Apprenticeship Act mandates factories with 30 or more employees to engage 2.5% to 15% apprentices of total workforce."
        ],
        "evidence_against": [
            "State apprenticeship advisory portals frequently experience payment disbursement backlogs of 6 to 9 months."
        ],
        "unknowns": [
            "Average processing time for central NAPS DBT reimbursement into employer bank accounts in Haryana."
        ],
        "failure_modes": [
            "Apprentice drops out before completion of training period, disqualifying reimbursement claim.",
            "Government portal updates create prolonged system downtime during monthly claim windows."
        ],
        "experiment": {
            "hypothesis": "At least 3 factory HR heads with >10 apprentices will hire the desk at ₹300/month/apprentice to handle all NAPS claim submissions.",
            "validation": "Interview 6 industrial HR heads in Sector 24 Faridabad.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "3 HR heads agree to trial filing service.",
            "failure_metric": "HR heads report government stipend reimbursements are too delayed to justify hiring assistance.",
            "data_required": ["Active apprentice headcount", "Apprenticeship portal login status"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "National Apprenticeship Promotion Scheme (NAPS) Guidelines",
                "source_url": "https://apprenticeshipindia.gov.in/naps-scheme",
                "source_domain": "apprenticeshipindia.gov.in",
                "publication_date": "2024-01-10",
                "classification": "FACT",
                "confidence": 0.94
            }
        ],
        "pursue_status": "DO_NOT_PURSUE_YET",
        "do_not_pursue_reason": "Severe government payment backlog: State NAPS stipend reimbursement disbursements in Haryana frequently lag by 6 to 9 months. Employers become frustrated and withhold service fees when government subsidies are delayed."
    },

    # =========================================================================
    # 7. DIGITAL_PRODUCTS
    # =========================================================================
    {
        "title": "Indian MSME Factory Statutory Compliance & Audit Checklist Toolkit",
        "opportunity_family": "DIGITAL_PRODUCTS",
        "sector": "Industrial Legal & Safety Templates",
        "customer": "Factory managers, workshop directors, and HR executives across India. Problem: Complying with Factories Act, State Pollution Control rules, and PF/ESI documentation is complex; annual retainers cost ₹60,000+. Alternatives: Generic blog posts or costly legal consultancies.",
        "target_market": "Over 50,000 registered manufacturing MSMEs across Indian industrial belts",
        "geography": ["Pan-India", "Online"],
        "problem": "Small factory owners are unprepared for surprise labor and safety factory inspections, resulting in corruption, show-cause notices, and fines.",
        "solution": "Digital downloadable toolkit containing self-audit checklists, statutory register templates (Form 11, 14, 25), and step-by-step inspection readiness protocols.",
        "revenue_model": "one_time_digital_purchase",
        "startup_cost": 2000.0,
        "cac": 200.0,
        "customer_value": 1499.0,
        "fulfilment_cost": 50.0,
        "time_to_first_revenue": "3 days",
        "recurring_potential": "LOW",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Dynamic tailoring of statutory checklist based on factory worker count, horsepower installed, and industrial state.",
            "software_automation": "Instant PDF/DOCX generation, automated payment gateway integration, email delivery.",
            "human_only": "None required once templates are authored and reviewed."
        },
        "competition": "Legal tech firms focused on corporate tech startups; unorganized offline compliance clerks.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Sold strictly as standardized informational documentation templates. Explicitly disclaims legal counsel.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Product is a self-contained digital asset delivered immediately via Razorpay/Stripe; zero disintermediation risk.",
        "search_query": "factories act compliance checklist templates msme india download",
        "evidence_for": [
            "Factories Act 1948 mandates over 14 distinct statutory registers and safety logbooks for any unit employing 10+ workers with power.",
            "Over 400,000 registered MSMEs in India pay retainer fees for regulatory advice."
        ],
        "evidence_against": [
            "Some small business owners prefer delegating all compliance to an offline 'fixer' rather than implementing self-audit tools."
        ],
        "unknowns": [
            "Customer acquisition cost via organic LinkedIn and WhatsApp professional groups."
        ],
        "failure_modes": [
            "Free unauthorized sharing of template PDF packs across unmonitored industry forums.",
            "State amendments to labor codes alter register formats, requiring quarterly template updates."
        ],
        "experiment": {
            "hypothesis": "At least 3 factory managers will purchase the compliance toolkit for ₹999 within 7 days of organic promotion in manufacturing groups.",
            "validation": "Create landing page preview with 1 free sample register and measure paid checkout conversion.",
            "budget": 250.0,
            "duration": "7 days",
            "success_metric": "3 paid digital downloads achieved.",
            "failure_metric": "Zero sales generated from landing page visits.",
            "data_required": ["Landing page visitor conversion rate", "Cart abandonment rate"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Ministry of Labour and Employment Factories Act Rules",
                "source_url": "https://labour.gov.in/factories-act-rules",
                "source_domain": "labour.gov.in",
                "publication_date": "2023-12-01",
                "classification": "FACT",
                "confidence": 0.95
            },
            {
                "source_title": "MSME Compliance Spend Survey",
                "source_url": "https://smb-survey-india.org/compliance-spend",
                "source_domain": "smb-survey-india.org",
                "publication_date": "2024-02-12",
                "classification": "ESTIMATE",
                "confidence": 0.89
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "NCR Contract Labour Law & Minimum Wage Calculator Toolkit",
        "opportunity_family": "DIGITAL_PRODUCTS",
        "sector": "Industrial HR & Labor Compliance Software",
        "customer": "Manpower supply contractors, security agencies, and factory HR executives operating across Haryana, Delhi, and UP borders. Problem: Minimum wage rates and VDA (Variable Dearness Allowance) differ drastically across borders and revise twice annually. Alternatives: Error-prone manual Excel spreadsheets.",
        "target_market": "Manpower contractors and HR managers across Delhi-NCR",
        "geography": ["Delhi-NCR", "Online"],
        "problem": "Contractors quote unviable bids or underpay minimum wages due to border confusion, triggering labor commissioner recovery notices and license cancellations.",
        "solution": "Automated Excel and web calculator embedding live Haryana, Delhi, and UP minimum wage notification schedules, PF/ESI caps, and overtime rules.",
        "revenue_model": "digital_license_with_update_pack",
        "startup_cost": 1500.0,
        "cac": 150.0,
        "customer_value": 1999.0,
        "fulfilment_cost": 50.0,
        "time_to_first_revenue": "3 days",
        "recurring_potential": "MEDIUM",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Scraping state labor department gazettes for semi-annual VDA minimum wage revisions.",
            "software_automation": "Automated spreadsheet macro updates, automated update notification emails to licensees.",
            "human_only": "None required once calculator formulas are validated against state gazette notifications."
        },
        "competition": "Generic labor law consultancy blogs providing static tables without interactive wage costing models.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Software calculation utility. Includes explicit disclaimer that contractor is responsible for verifying wage rates against official state gazette.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Buyers purchase the software license directly; recurring revenue generated via bi-annual wage notification update packs.",
        "search_query": "minimum wage notification haryana delhi ncr calculator excel",
        "evidence_for": [
            "Haryana Labour Department issues mandatory bi-annual VDA notifications (effective May and November) altering minimum wage rates for unskilled to highly skilled workers.",
            "Contract Labour (Regulation and Abolition) Act mandates strict contractor compliance to retain state licensing."
        ],
        "evidence_against": [
            "Contractors operating in informal unorganized labor markets frequently ignore statutory wage rates."
        ],
        "unknowns": [
            "Annual repeat subscription rate for bi-annual wage schedule updates."
        ],
        "failure_modes": [
            "Spreadsheet macro corrupted by user formula modifications.",
            "Delay in official state gazette publication creates customer confusion on revision effective dates."
        ],
        "experiment": {
            "hypothesis": "At least 4 manpower contractors will purchase the calculator for ₹1,499 within 5 days when presented with an automated border wage comparison demo.",
            "validation": "Demonstrate the calculator spreadsheet to 8 manpower contractors in Gurgaon and Faridabad.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "4 contractors purchase license.",
            "failure_metric": "Fewer than 2 contractors willing to pay for wage calculation tools.",
            "data_required": ["Contractor total deployed worker count", "Current spreadsheet used"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Haryana Labour Department Minimum Wage Gazettes",
                "source_url": "https://hrylabour.gov.in/wage-notifications",
                "source_domain": "hrylabour.gov.in",
                "publication_date": "2024-05-01",
                "classification": "FACT",
                "confidence": 0.98
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Standard Operating Procedure (SOP) Templates for Small CNC & Tooling Workshops",
        "opportunity_family": "DIGITAL_PRODUCTS",
        "sector": "Manufacturing Quality Engineering",
        "customer": "First-generation machine shop owners aiming to qualify for Tier-2 automotive vendor audits (ISO 9001 / IATF 16949). Problem: Auto OEMs require documented machine maintenance and tooling calibration SOPs; hiring consultants costs ₹40,000+. Alternatives: Spending months drafting documents manually.",
        "target_market": "Small CNC and machining job shops across India",
        "geography": ["Pan-India", "Online"],
        "problem": "Small machine shops fail Tier-1 automotive customer quality audits due to missing machine calibration, tool changeover, and first-piece inspection SOPs.",
        "solution": "Comprehensive, editable library of 35 production and maintenance SOP templates customized specifically for CNC lathes, milling machines, and surface grinders.",
        "revenue_model": "one_time_digital_bundle",
        "startup_cost": 2000.0,
        "cac": 200.0,
        "customer_value": 2499.0,
        "fulfilment_cost": 50.0,
        "time_to_first_revenue": "5 days",
        "recurring_potential": "LOW",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Customizing SOP document headers, logo placeholders, and machine model numbers to the buyer's workshop specs.",
            "software_automation": "Instant ZIP archive packaging, automated delivery upon payment completion.",
            "human_only": "None required once templates are validated by a seasoned manufacturing engineer."
        },
        "competition": "Generic corporate ISO consulting packages that lack machining-specific technical workflows (e.g., backlash inspection, coolant concentration checks).",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Informational engineering documentation templates. Non-regulated commercial product.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Instant digital fulfillment directly to buyer; completely self-contained.",
        "search_query": "cnc machine shop sop templates iso 9001 download india",
        "evidence_for": [
            "Automotive Tier-1 OEM audit manuals mandate written SOPs for CNC tool offset validation and machine preventive maintenance.",
            "TAGMA surveys indicate over 65% of small machine shops have unwritten, informal maintenance procedures."
        ],
        "evidence_against": [
            "Shop floor operators frequently operate via tribal knowledge and resist maintaining formal paper logs."
        ],
        "unknowns": [
            "Buyer preference for Microsoft Word editable format vs cloud PDF software."
        ],
        "failure_modes": [
            "Customer complains templates require too much customization for unusual custom machinery.",
            "Pirated sharing of template bundle on industrial telegram channels."
        ],
        "experiment": {
            "hypothesis": "At least 3 machine shop owners will buy the SOP bundle for ₹1,999 after reviewing a free downloadable CNC tool changeover SOP sample.",
            "validation": "Distribute free tool changeover sample SOP to 15 machine shop owners on WhatsApp and measure upgrade conversions.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "3 owners purchase complete 35-SOP bundle.",
            "failure_metric": "Zero owners purchase; owners state they do not need written SOPs.",
            "data_required": ["Number of CNC machines installed", "Upcoming customer audit date"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Automotive Industry Action Group (AIAG) Quality Standards",
                "source_url": "https://aiag.org/quality-management-guidelines",
                "source_domain": "aiag.org",
                "publication_date": "2023-11-15",
                "classification": "FACT",
                "confidence": 0.92
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },

    # =========================================================================
    # 8. MARKETPLACE_ARBITRAGE
    # =========================================================================
    {
        "title": "Surplus Industrial Corrugated Pallet & Crate Exchange",
        "opportunity_family": "MARKETPLACE_ARBITRAGE",
        "sector": "Industrial Logistics Packaging Materials",
        "customer": "Heavy machinery fabricators, casting exporters, and auto-component shippers in Faridabad. Problem: Ordering new heat-treated (ISPM-15) wooden and heavy-duty plastic pallets costs ₹800 to ₹1,400 per unit with 7-day delays. Alternatives: Buying damaged scrap pallets.",
        "target_market": "Manufacturing exporters and fabricators in Faridabad",
        "geography": ["Faridabad", "Haryana"],
        "problem": "Exporters overspend on fresh packaging pallets while local warehousing and FMCG logistics centers discard once-used certified pallets at scrap prices.",
        "solution": "Digital inventory matchmaker connecting warehouse surplus pallet liquidation lots directly with export fabricators, saving buyers 40% on packaging costs.",
        "revenue_model": "margin_per_pallet",
        "startup_cost": 4000.0,
        "cac": 450.0,
        "customer_value": 3500.0,
        "fulfilment_cost": 300.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Image-based grading of pallet condition (Grade A vs Grade B), dimension confirmation (1200x1000mm vs Euro size).",
            "software_automation": "Real-time lot availability alerts on WhatsApp, automated invoice generation.",
            "human_only": "Physical batch inspection of heat-treatment stamp (ISPM-15) prior to dispatch for export buyers."
        },
        "competition": "Scrap timber traders who break pallets down into firewood or raw lumber rather than preserving high-value re-usable structures.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Exporters require valid ISPM-15 phytosanitary treatment marks on timber pallets for international shipping. Trading requires standard GST.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Warehouses prefer clearing 500+ pallet lots quickly to clear floor space and will not deal with small 50-pallet retail orders; the exchange handles aggregation.",
        "search_query": "used wooden plastic pallets supplier faridabad haryana",
        "evidence_for": [
            "FMCG and retail distribution centers in NCR generate over 20,000 once-used wooden pallets monthly.",
            "Export packaging guidelines strictly enforce heat-treated pallet usage, creating consistent replacement demand."
        ],
        "evidence_against": [
            "Logistics transport costs for moving bulky, low-density wooden pallets across town can erode arbitrage margins."
        ],
        "unknowns": [
            "Maximum economical road haulage radius for secondary pallets in NCR (typically under 25 km)."
        ],
        "failure_modes": [
            "Buyer export shipment rejected at port due to counterfeit or faded ISPM-15 treatment stamps.",
            "Warehouse changes disposal contractor and revokes supply access."
        ],
        "experiment": {
            "hypothesis": "An exporter will purchase a test lot of 50 Grade-A used pallets at ₹450/pallet within 3 days of being offered certified ISPM-15 stamps.",
            "validation": "Secure supply commitment of 50 surplus pallets from a warehouse and quote 4 exporters in Sector 58 Faridabad.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "1 exporter issues purchase order for 50 pallets.",
            "failure_metric": "Zero buyers interested; exporters demand brand-new lumber pallets.",
            "data_required": ["Required pallet dimensions", "Target load capacity (static vs dynamic kg)"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Directorate of Plant Protection, Quarantine & Storage (ISPM-15 Norms)",
                "source_url": "https://plantquarantineindia.nic.in/ispm15-standards",
                "source_domain": "plantquarantineindia.nic.in",
                "publication_date": "2023-09-10",
                "classification": "FACT",
                "confidence": 0.95
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Dead-Stock Industrial Fasteners & Tooling Liquidation Clearinghouse",
        "opportunity_family": "MARKETPLACE_ARBITRAGE",
        "sector": "Industrial Hardware & Machine Components",
        "customer": "Auto-ancillary fastener distributors and fabrication workshops holding slow-moving inventory (metric high-tensile bolts, nuts, carbide endmills). Problem: Capital tied up in slow-moving stock; scrapping high-grade alloy components yields only ₹35/kg instead of ₹180/kg component value. Alternatives: Letting dead-stock rust in warehouses.",
        "target_market": "Industrial hardware distributors and fabrication shops in Faridabad and NCR",
        "geography": ["Faridabad", "Delhi-NCR"],
        "problem": "Hardware distributors tie up ₹5 to ₹20 lakh in dead-stock fastener sizes that maintenance workshops are actively looking for at retail shops.",
        "solution": "Digital clearance exchange matching dead-stock fastener and tool inventories at 40% discount to retail with local equipment repair workshops.",
        "revenue_model": "clearinghouse_commission",
        "startup_cost": 3500.0,
        "cac": 400.0,
        "customer_value": 3200.0,
        "fulfilment_cost": 250.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Standardizing fastener specs (grade 8.8, 10.9, pitch, coating) from seller dead-stock Excel sheets into searchable catalog.",
            "software_automation": "Automated matching against buyer maintenance part requests, escrow payment release.",
            "human_only": "Sample thread gauge inspection on initial lot intake."
        },
        "competition": "Traditional metal scrap traders who melt down precision hardware for scrap weight.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "Commercial trading of industrial goods with standard GST billing. Non-regulated.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Distributors holding dead-stock prefer selling through a neutral clearinghouse rather than publicizing distress discounts to their existing regular customer base.",
        "search_query": "dead stock industrial fasteners bolts liquidation delhi ncr",
        "evidence_for": [
            "Industrial hardware distributors maintain an estimated 8-12% non-moving dead-stock ratio across specialized fastener SKUs.",
            "Small equipment maintenance contractors pay up to 100% retail markups for spot single-box fastener purchases."
        ],
        "evidence_against": [
            "Dead-stock inventory can suffer from surface rust if stored improperly in humid warehouse conditions."
        ],
        "unknowns": [
            "Speed of matching niche fastener thread pitches with active local repair projects."
        ],
        "failure_modes": [
            "Seller misidentifies tensile grade (e.g. shipping grade 4.6 instead of high-tensile 8.8).",
            "Inventory already rusted beyond acceptable industrial cleaning threshold."
        ],
        "experiment": {
            "hypothesis": "At least 2 hardware distributors will list ₹50,000+ in dead-stock fasteners at 40% discount, and 2 repair workshops will purchase lots within 7 days.",
            "validation": "Catalog dead-stock lists from 3 hardware distributors in Faridabad Old Market.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "1 liquidation transaction successfully matched.",
            "failure_metric": "Distributors refuse to discount inventory below book value.",
            "data_required": ["List of slow-moving SKUs", "Current book value vs scrap value"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Fasteners Manufacturers Association of India Market Report",
                "source_url": "https://fmai.in/fastener-market-benchmarks",
                "source_domain": "fmai.in",
                "publication_date": "2024-02-10",
                "classification": "ESTIMATE",
                "confidence": 0.88
            }
        ],
        "pursue_status": "VIABLE_NOW",
        "do_not_pursue_reason": ""
    },
    {
        "title": "Idle CNC & Machine Shop Off-Shift Capacity Booking Desk",
        "opportunity_family": "MARKETPLACE_ARBITRAGE",
        "sector": "Precision Machining Capacity",
        "customer": "Machine shops with rush order overflows needing temporary VMC/CNC lathe milling capacity, and machine shops with idle night shifts. Problem: Machine owners invest ₹35 lakh in machinery that sits idle 12 hours a day; rush contractors turn down orders. Alternatives: Subcontracting to unverified job workers.",
        "target_market": "CNC and machine job shops in Faridabad industrial belt",
        "geography": ["Faridabad", "Haryana"],
        "problem": "Capital-intensive machine shops operate at 50% capacity on single shifts, while peer workshops turn down rush orders due to capacity bottlenecks.",
        "solution": "Off-shift machine capacity booking desk matching vetted idle night-shift CNC capacity with overflow production orders.",
        "revenue_model": "hourly_machine_booking_fee",
        "startup_cost": 3000.0,
        "cac": 450.0,
        "customer_value": 3500.0,
        "fulfilment_cost": 300.0,
        "time_to_first_revenue": "14 days",
        "recurring_potential": "HIGH",
        "automation_potential": "HIGH",
        "automation_breakdown": {
            "ai_automation": "Matching machine technical specs (spindle speed, bed size, 3-axis vs 4-axis) with client CAD drawings and job tolerance limits.",
            "software_automation": "Shift calendar scheduling, milestone escrow payment processing.",
            "human_only": "CMM dimensional inspection of first-piece sample before production run."
        },
        "competition": "Informal peer-to-peer job work without written quality guarantees or automated capacity discovery.",
        "regulatory_complexity": "LOW",
        "regulatory_considerations": "B2B subcontract manufacturing agreement. Standard GST invoicing. Clear IP non-disclosure protections for client engineering drawings.",
        "platform_dependency": "LOW",
        "disintermediation_analysis": "Extreme disintermediation risk: Once a machine owner and overflow contractor are introduced and complete the first production run, they exchange contact details and contract directly for all future shifts to avoid paying platform commission.",
        "search_query": "cnc vmc machine shop idle capacity job work faridabad",
        "evidence_for": [
            "Over 40% of small machine shops in Faridabad operate exclusively on single 8-10 hour daytime shifts.",
            "Average hourly machining charge for a 3-axis VMC in NCR ranges from ₹350 to ₹600/hour."
        ],
        "evidence_against": [
            "Machining job-shop owners exhibit severe trust deficits regarding tool breakage and material scrap rates during unsupervised off-shifts."
        ],
        "unknowns": [
            "Dispute rate for machined parts failing dimensional tolerance during off-shift contracts."
        ],
        "failure_modes": [
            "Client and host shop bypass platform immediately after first successful batch.",
            "Night-shift operator damages machine spindle or tooling, sparking multi-party liability disputes."
        ],
        "experiment": {
            "hypothesis": "At least 2 machine shops with idle night shifts will agree to host a 20-hour trial machining batch for a verified peer workshop.",
            "validation": "Interview 5 machine shop owners with idle night shifts in Sector 24 Faridabad.",
            "budget": 0.0,
            "duration": "5 days",
            "success_metric": "2 shops sign up with verified machine specifications.",
            "failure_metric": "Shops refuse to run customer jobs on night shifts without owner on-site presence.",
            "data_required": ["Machine model and controller (Fanuc/Siemens)", "Available shift hours"],
            "human_approvals_required": True,
        },
        "sources": [
            {
                "source_title": "Tool and Gauge Manufacturers Association Machining Survey",
                "source_url": "https://tagma-india.org/capacity-utilization-report",
                "source_domain": "tagma-india.org",
                "publication_date": "2024-02-15",
                "classification": "ESTIMATE",
                "confidence": 0.88
            }
        ],
        "pursue_status": "DO_NOT_PURSUE_YET",
        "do_not_pursue_reason": "Fatal disintermediation vulnerability: Machine shop owners in localized industrial clusters invariably bypass the platform after the first introduction, establishing direct commercial ties. High risk of tool damage disputes makes intermediary role unviable without on-site supervision."
    }
]
