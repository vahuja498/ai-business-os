"use client";

import { useEffect, useState } from "react";
import { api, OpportunityItem } from "@/lib/api";

const DEFAULT_OBJECTIVE =
  "Identify legitimate business opportunities available to an entrepreneur operating from India with <= ₹10,000 capital, high automation potential, first revenue in <= 30 days, real paying customers, and no deceptive practices across eight opportunity families.";

const OPPORTUNITY_FAMILIES = [
  "ALL",
  "INFORMATION_ARBITRAGE",
  "LEAD_GENERATION",
  "SERVICE_ARBITRAGE",
  "PROCESS_AUTOMATION",
  "DISTRIBUTION_ARBITRAGE",
  "LEGITIMATE_INCENTIVE_SERVICES",
  "DIGITAL_PRODUCTS",
  "MARKETPLACE_ARBITRAGE",
];

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<OpportunityItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [researching, setResearching] = useState(false);
  const [objectivePrompt, setObjectivePrompt] = useState(DEFAULT_OBJECTIVE);
  const [showPromptBox, setShowPromptBox] = useState(false);
  const [showReportModal, setShowReportModal] = useState(false);
  const [reportMarkdown, setReportMarkdown] = useState<string>("");

  // Filter States
  const [filterFamily, setFilterFamily] = useState<string>("ALL");
  const [filterCapital, setFilterCapital] = useState<number>(10000);
  const [filterRecurring, setFilterRecurring] = useState<string>("ALL");
  const [sortBy, setSortBy] = useState<string>("margin_desc");

  // Expanded Failure Mode Drawers
  const [expandedFailure, setExpandedFailure] = useState<Record<string, boolean>>({});
  const [expandedEvidence, setExpandedEvidence] = useState<Record<string, boolean>>({});
  const [expandedReality, setExpandedReality] = useState<Record<string, boolean>>({});

  const loadOpportunities = async () => {
    try {
      setLoading(true);
      const res = await api.getOpportunities(filterFamily === "ALL" ? undefined : filterFamily);
      setOpportunities(res);
    } catch (err: any) {
      alert(`Error loading opportunities: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOpportunities();
  }, [filterFamily]);

  const handleTriggerCampaign = async () => {
    try {
      setResearching(true);
      const res = await api.triggerOpportunityResearch({
        objective: objectivePrompt,
        capital_limit: filterCapital,
      });
      alert(`Research Campaign Complete! Produced ${res.count} structured candidate opportunities.`);
      setShowPromptBox(false);
      loadOpportunities();
    } catch (err: any) {
      alert(`Research campaign failed: ${err.message}`);
    } finally {
      setResearching(false);
    }
  };

  const handleApproveExperiment = async (oppId: string) => {
    try {
      await api.requestExperimentApproval(oppId);
      alert("Validation experiment sign-off requested! Check the Approvals gate.");
      loadOpportunities();
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    }
  };

  const handleExportReport = async () => {
    try {
      const res = await api.getOpportunityReport(filterFamily === "ALL" ? undefined : filterFamily);
      setReportMarkdown(res.markdown_report);
      setShowReportModal(true);
    } catch (err: any) {
      alert(`Error generating report: ${err.message}`);
    }
  };

  // Filter & Sort Logic
  const filteredOpps = opportunities
    .filter((o) => (filterFamily === "ALL" ? true : o.opportunity_family === filterFamily))
    .filter((o) => o.estimated_startup_cost <= filterCapital)
    .filter((o) => (filterRecurring === "ALL" ? true : o.recurring_potential === filterRecurring))
    .sort((a, b) => {
      if (sortBy === "margin_desc") return b.estimated_margin - a.estimated_margin;
      if (sortBy === "startup_asc") return a.estimated_startup_cost - b.estimated_startup_cost;
      return 0;
    });

  const toggleDrawer = (id: string, drawer: "failure" | "evidence" | "reality") => {
    if (drawer === "failure") {
      setExpandedFailure((prev) => ({ ...prev, [id]: !prev[id] }));
    } else if (drawer === "evidence") {
      setExpandedEvidence((prev) => ({ ...prev, [id]: !prev[id] }));
    } else {
      setExpandedReality((prev) => ({ ...prev, [id]: !prev[id] }));
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner & Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Opportunity Discovery & Validation</h1>
          <p className="text-sm text-slate-400">
            Adversarial opportunity research platform investigating across 8 opportunity families with reality check verification.
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleExportReport}
            className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 transition"
          >
            Export Report
          </button>
          <button
            onClick={() => setShowPromptBox(!showPromptBox)}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 font-semibold text-xs text-white rounded-lg shadow-md transition"
          >
            {showPromptBox ? "Hide Campaign Input" : "+ Run Research Campaign"}
          </button>
        </div>
      </div>

      {/* Safety Guardrail Notice */}
      <div className="p-3 bg-amber-950/20 border border-amber-900/40 rounded-lg text-xs text-amber-300 flex items-center justify-between">
        <span>
          <strong>Phase 3 Governance:</strong> All discovery is research-only. Zero external customer contact, zero vendor execution, and zero financial transactions. The human owner decides which opportunity to pursue.
        </span>
        <span className="font-mono text-[11px] bg-amber-900/50 px-2 py-0.5 rounded border border-amber-700/50">ZERO OUTFLOW ACTIVE</span>
      </div>

      {/* Research Objective Box */}
      {showPromptBox && (
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white">Standard Research Campaign Objective (Section 4)</h2>
          <textarea
            value={objectivePrompt}
            onChange={(e) => setObjectivePrompt(e.target.value)}
            rows={4}
            className="w-full p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white font-mono focus:outline-none focus:border-indigo-500"
          />
          <div className="flex justify-end gap-2">
            <button onClick={() => setShowPromptBox(false)} className="px-3 py-1.5 text-xs text-slate-400 hover:text-white">
              Cancel
            </button>
            <button
              onClick={handleTriggerCampaign}
              disabled={researching}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 text-xs font-semibold text-white rounded-md transition shadow"
            >
              {researching ? "Opportunity Engine Discovering..." : "Execute Discovery Campaign"}
            </button>
          </div>
        </div>
      )}

      {/* Opportunity Families Filter Bar */}
      <div className="space-y-3 p-4 bg-slate-900 rounded-xl border border-slate-800 text-xs">
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          <span className="text-slate-400 font-medium whitespace-nowrap">Family:</span>
          {OPPORTUNITY_FAMILIES.map((fam) => (
            <button
              key={fam}
              onClick={() => setFilterFamily(fam)}
              className={`px-2.5 py-1 rounded-md whitespace-nowrap transition ${
                filterFamily === fam
                  ? "bg-indigo-600 text-white font-semibold"
                  : "bg-slate-950 text-slate-400 hover:text-white border border-slate-800"
              }`}
            >
              {fam.replace(/_/g, " ")}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap items-center justify-between gap-4 pt-2 border-t border-slate-800/60">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="text-slate-400">Capital Limit:</span>
              <select
                value={filterCapital}
                onChange={(e) => setFilterCapital(Number(e.target.value))}
                className="bg-slate-950 border border-slate-800 px-2 py-1 rounded text-slate-200"
              >
                <option value={10000}>All (&lt;= ₹10,000)</option>
                <option value={5000}>&lt;= ₹5,000</option>
                <option value={3000}>&lt;= ₹3,000</option>
              </select>
            </div>

            <div className="flex items-center gap-2">
              <span className="text-slate-400">Recurring:</span>
              <select
                value={filterRecurring}
                onChange={(e) => setFilterRecurring(e.target.value)}
                className="bg-slate-950 border border-slate-800 px-2 py-1 rounded text-slate-200"
              >
                <option value="ALL">All</option>
                <option value="HIGH">High Recurring</option>
                <option value="MEDIUM">Medium</option>
                <option value="LOW">Low</option>
              </select>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-slate-400">Sort By:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
              className="bg-slate-950 border border-slate-800 px-2 py-1 rounded text-slate-200"
            >
              <option value="margin_desc">Highest Margin</option>
              <option value="startup_asc">Lowest Startup Cost</option>
            </select>
          </div>
        </div>
      </div>

      {/* Opportunities List */}
      {loading ? (
        <p className="text-slate-400 text-sm">Loading opportunity campaign portfolio...</p>
      ) : filteredOpps.length === 0 ? (
        <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-500">
          No opportunities found matching selected filters. Click &quot;+ Run Research Campaign&quot; above.
        </div>
      ) : (
        <div className="space-y-6">
          {filteredOpps.map((opp) => (
            <div key={opp.id} className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
              {/* Header */}
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="text-lg font-bold text-white">{opp.title}</h2>
                    <span className="text-xs px-2 py-0.5 rounded font-mono bg-indigo-950 text-indigo-300 border border-indigo-800">
                      {opp.opportunity_family}
                    </span>
                    <span className="text-xs px-2 py-0.5 rounded font-mono bg-slate-800 text-slate-300">
                      {opp.revenue_model}
                    </span>
                    {opp.geography && opp.geography.length > 0 && (
                      <span className="text-xs px-2 py-0.5 rounded font-mono bg-emerald-950/60 text-emerald-300 border border-emerald-800/50">
                        {opp.geography.join(", ")}
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    <strong className="text-slate-300">Customer:</strong> {opp.customer || opp.target_market} &bull;{" "}
                    <strong className="text-slate-300">Recurring:</strong> {opp.recurring_potential || "MEDIUM"}
                  </p>
                  {opp.problem && (
                    <p className="text-xs text-slate-300 mt-1.5">
                      <span className="text-slate-500 font-semibold">Problem:</span> {opp.problem}
                    </p>
                  )}
                </div>

                <span
                  className={`text-xs px-2.5 py-1 rounded font-bold ${
                    opp.status === "APPROVED"
                      ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                      : opp.status === "PENDING_APPROVAL"
                      ? "bg-amber-950 text-amber-300 border border-amber-800"
                      : "bg-slate-800 text-slate-300 border border-slate-700"
                  }`}
                >
                  {opp.status}
                </span>
              </div>

              {/* Multi-Dimensional Metrics Grid */}
              <div className="grid grid-cols-2 md:grid-cols-6 gap-3 p-3.5 bg-slate-950 rounded-lg border border-slate-800 text-xs">
                <div>
                  <span className="text-slate-500 block">Startup Capital</span>
                  <span className="font-mono text-white font-semibold">₹{opp.estimated_startup_cost.toFixed(0)}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Estimated CAC</span>
                  <span className="font-mono text-white font-semibold">₹{opp.estimated_acquisition_cost.toFixed(0)}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Customer Value</span>
                  <span className="font-mono text-white font-semibold">₹{opp.estimated_customer_value.toFixed(0)}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Unit Margin</span>
                  <span className="font-mono text-emerald-400 font-bold">{(opp.estimated_margin * 100).toFixed(0)}%</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Time to Revenue</span>
                  <span className="font-mono text-indigo-300 font-semibold">{opp.time_to_first_revenue}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Automation Level</span>
                  <span className="font-mono text-white font-semibold">{opp.automation_potential}</span>
                </div>
              </div>

              {/* Expandable "Why This May Fail" Box (Section 11) */}
              <div className="p-3.5 rounded-lg bg-red-950/20 border border-red-900/40 text-xs space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-red-300 flex items-center gap-1.5">
                    <span>⚠️</span> Why This May Fail (Adversarial Reality Check):
                  </span>
                  <button
                    onClick={() => toggleDrawer(opp.id, "failure")}
                    className="text-[11px] text-red-400 hover:text-red-300 font-mono underline"
                  >
                    {expandedFailure[opp.id] ? "Hide Failure Risks" : "Inspect Failure Modes & Contradictions"}
                  </button>
                </div>

                {expandedFailure[opp.id] && (
                  <div className="space-y-3 pt-2 border-t border-red-900/40 text-slate-300">
                    <div>
                      <span className="font-semibold text-red-200 block mb-1">Fatal Failure Vectors:</span>
                      <ul className="list-disc pl-4 space-y-1">
                        {(opp.failure_modes || ["Conversion failure in unverified marketing channels."]).map((f, idx) => (
                          <li key={idx}>{f}</li>
                        ))}
                      </ul>
                    </div>

                    {opp.contradicting_evidence && opp.contradicting_evidence.length > 0 && (
                      <div>
                        <span className="font-semibold text-amber-300 block mb-1">Contradicting Evidence & Headwinds:</span>
                        <div className="space-y-1 pl-1">
                          {opp.contradicting_evidence.map((c, idx) => (
                            <div key={idx} className="p-2 bg-slate-950/80 rounded border border-red-950 text-[11px]">
                              <span className="text-amber-400 font-semibold">{c.source || "Industry Source"}:</span>{" "}
                              {c.claim || JSON.stringify(c)}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Low-cost Validation Experiment (Section 6 & 8) */}
              {opp.recommended_experiment && (
                <div className="p-4 rounded-lg bg-slate-950/80 border border-indigo-950/70 space-y-2 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-indigo-300">
                      Low-Cost Validation Experiment:
                    </span>
                    <span className="font-mono text-emerald-400 font-bold">
                      Budget: ₹{opp.recommended_experiment.budget.toFixed(2)} ({opp.recommended_experiment.duration})
                    </span>
                  </div>
                  <p className="text-slate-300">
                    <strong className="text-slate-400">Hypothesis:</strong> {opp.recommended_experiment.hypothesis}
                  </p>
                  <p className="text-slate-300">
                    <strong className="text-slate-400">Validation:</strong> {opp.recommended_experiment.validation}
                  </p>
                  <div className="flex gap-4 pt-1 text-slate-400">
                    <span>
                      <strong className="text-emerald-400">Success:</strong> {opp.recommended_experiment.success_metric}
                    </span>
                    <span>
                      <strong className="text-red-400">Failure:</strong> {opp.recommended_experiment.failure_metric}
                    </span>
                  </div>
                </div>
              )}

              {/* Action Buttons & Drawers */}
              <div className="flex items-center justify-between pt-2 border-t border-slate-800 text-xs">
                <div className="flex items-center gap-4">
                  <button
                    onClick={() => toggleDrawer(opp.id, "evidence")}
                    className="text-indigo-400 hover:text-indigo-300 font-medium"
                  >
                    {expandedEvidence[opp.id] ? "Hide Evidence" : "View Classified Evidence"}
                  </button>
                  <button
                    onClick={() => toggleDrawer(opp.id, "reality")}
                    className="text-slate-400 hover:text-slate-300 font-medium"
                  >
                    {expandedReality[opp.id] ? "Hide Reality Check" : "Reality Check 10-Point Audit"}
                  </button>
                </div>

                <div className="flex items-center gap-2">
                  {opp.status === "IDENTIFIED" && (
                    <button
                      onClick={() => handleApproveExperiment(opp.id)}
                      className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 font-semibold text-white rounded-md transition shadow"
                    >
                      Approve Experiment
                    </button>
                  )}
                  <button
                    onClick={() => alert("Opportunity archived.")}
                    className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-slate-200 rounded-md transition"
                  >
                    Archive
                  </button>
                </div>
              </div>

              {/* Reality Check 10-Point Audit Drawer */}
              {expandedReality[opp.id] && opp.reality_check && (
                <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 space-y-2 text-xs mt-3">
                  <h4 className="font-semibold text-indigo-300 mb-2">RealityCheckAgent Adversarial 10-Point Audit:</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {Object.entries(opp.reality_check).map(([key, check]: any) => (
                      <div key={key} className="p-2 rounded bg-slate-900 border border-slate-800 flex items-start gap-2">
                        <span
                          className={`text-[10px] px-1.5 py-0.5 rounded font-mono font-bold ${
                            check.status === "VERIFIED"
                              ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                              : check.status === "SUPPORTED_ESTIMATE"
                              ? "bg-indigo-950 text-indigo-300 border border-indigo-800"
                              : check.status === "UNKNOWN"
                              ? "bg-purple-950 text-purple-300 border border-purple-800"
                              : "bg-amber-950 text-amber-300 border border-amber-800"
                          }`}
                        >
                          {check.status}
                        </span>
                        <div>
                          <p className="font-semibold text-slate-200">{check.dimension}</p>
                          <p className="text-[11px] text-slate-400">{check.notes}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Evidence Drawer */}
              {expandedEvidence[opp.id] && (
                <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 space-y-3 text-xs mt-3">
                  <h4 className="font-semibold text-indigo-300">Classified Evidence (Primary Sources):</h4>
                  <div className="space-y-2">
                    {(opp.evidence || []).map((ev: any, idx: number) => (
                      <div key={idx} className="p-2.5 rounded bg-slate-900 border border-slate-800 flex items-start gap-3">
                        <span
                          className={`text-[10px] px-2 py-0.5 rounded font-mono font-bold ${
                            ev.type === "FACT"
                              ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                              : ev.type === "ESTIMATE"
                              ? "bg-amber-950 text-amber-300 border border-amber-800"
                              : "bg-purple-950 text-purple-300 border border-purple-800"
                          }`}
                        >
                          {ev.type}
                        </span>
                        <div className="flex-1">
                          <p className="text-slate-200">{ev.statement}</p>
                          <p className="text-[11px] text-slate-500 mt-0.5">
                            Source: <span className="font-mono text-indigo-400">{ev.domain || ev.source}</span>
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Export Report Modal */}
      {showReportModal && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-6 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-xl max-w-4xl w-full max-h-[85vh] flex flex-col p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-bold text-white">Exportable Opportunity Report (Section 10)</h3>
              <button onClick={() => setShowReportModal(false)} className="text-slate-400 hover:text-white text-sm">
                ✕ Close
              </button>
            </div>
            <textarea
              readOnly
              value={reportMarkdown}
              className="flex-1 w-full bg-slate-950 border border-slate-800 rounded-lg p-4 font-mono text-xs text-slate-300 overflow-y-auto focus:outline-none"
            />
            <div className="flex justify-end gap-2 pt-2 border-t border-slate-800">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(reportMarkdown);
                  alert("Markdown report copied to clipboard!");
                }}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold text-white rounded-md transition shadow"
              >
                Copy Markdown
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
