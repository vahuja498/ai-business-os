"use client";

import { useEffect, useState } from "react";
import { api, OpportunityItem } from "@/lib/api";

const DEFAULT_OBJECTIVE =
  "Find legitimate business opportunities in India that can start with <= ₹10,000 initial capital, have high automation potential, generate first revenue in <= 30 days, and have paying customers.";

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<OpportunityItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [researching, setResearching] = useState(false);
  const [objectivePrompt, setObjectivePrompt] = useState(DEFAULT_OBJECTIVE);
  const [showPromptBox, setShowPromptBox] = useState(false);
  const [selectedOpp, setSelectedOpp] = useState<OpportunityItem | null>(null);

  // Filters and Sorts
  const [filterUncertainty, setFilterUncertainty] = useState<string>("ALL");
  const [sortBy, setSortBy] = useState<string>("margin_desc");

  const loadOpportunities = async () => {
    try {
      setLoading(true);
      const res = await api.getOpportunities();
      setOpportunities(res);
    } catch (err: any) {
      alert(`Error loading opportunities: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOpportunities();
  }, []);

  const handleTriggerResearch = async () => {
    try {
      setResearching(true);
      const res = await api.triggerOpportunityResearch({ objective: objectivePrompt });
      alert(`Opportunity Engine completed research! Generated ${res.count} structured candidates.`);
      setShowPromptBox(false);
      loadOpportunities();
    } catch (err: any) {
      alert(`Research failed: ${err.message}`);
    } finally {
      setResearching(false);
    }
  };

  const handleApproveExperiment = async (oppId: string) => {
    try {
      await api.requestExperimentApproval(oppId);
      alert("Experiment sign-off requested! Check the Human Approval Gate.");
      loadOpportunities();
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    }
  };

  // Filter & Sort Logic
  const filteredOpps = opportunities
    .filter((o) => (filterUncertainty === "ALL" ? true : o.uncertainty === filterUncertainty))
    .sort((a, b) => {
      if (sortBy === "margin_desc") return b.estimated_margin - a.estimated_margin;
      if (sortBy === "startup_asc") return a.estimated_startup_cost - b.estimated_startup_cost;
      return 0;
    });

  return (
    <div className="space-y-6">
      {/* Top Banner & Header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Opportunity Engine</h1>
          <p className="text-sm text-slate-400">
            Autonomous multi-dimensional research platform. Exposes unit economics, evidence classification, and fail-fast experiments.
          </p>
        </div>
        <button
          onClick={() => setShowPromptBox(!showPromptBox)}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 font-semibold text-xs text-white rounded-lg shadow-md transition"
        >
          {showPromptBox ? "Hide Objective" : "+ New Research Run"}
        </button>
      </div>

      {/* Safety Guardrail Notice */}
      <div className="p-3 bg-amber-950/20 border border-amber-900/40 rounded-lg text-xs text-amber-300 flex items-center justify-between">
        <span>
          <strong>Phase 2 Governance:</strong> Real customer contact and financial outflows are disabled. Approving an experiment registers human authorization without external execution.
        </span>
        <span className="font-mono text-[11px] bg-amber-900/50 px-2 py-0.5 rounded border border-amber-700/50">SAFEGUARD ACTIVE</span>
      </div>

      {/* Research Objective Box */}
      {showPromptBox && (
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
          <h2 className="text-sm font-semibold text-white">Strategic Objective Prompt (Section 8 Template)</h2>
          <textarea
            value={objectivePrompt}
            onChange={(e) => setObjectivePrompt(e.target.value)}
            rows={4}
            className="w-full p-3 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white font-mono focus:outline-none focus:border-indigo-500"
          />
          <div className="flex justify-end gap-2">
            <button
              onClick={() => setShowPromptBox(false)}
              className="px-3 py-1.5 text-xs text-slate-400 hover:text-white"
            >
              Cancel
            </button>
            <button
              onClick={handleTriggerResearch}
              disabled={researching}
              className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 text-xs font-semibold text-white rounded-md transition shadow"
            >
              {researching ? "Opportunity Engine Researching..." : "Launch Opportunity Engine"}
            </button>
          </div>
        </div>
      )}

      {/* Filter and Sort Bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 bg-slate-900 rounded-xl border border-slate-800 text-xs">
        <div className="flex items-center gap-3">
          <span className="text-slate-400">Uncertainty:</span>
          {["ALL", "LOW", "MEDIUM", "HIGH"].map((u) => (
            <button
              key={u}
              onClick={() => setFilterUncertainty(u)}
              className={`px-2.5 py-1 rounded-md transition ${
                filterUncertainty === u
                  ? "bg-indigo-600 text-white font-medium"
                  : "bg-slate-950 text-slate-400 hover:text-white border border-slate-800"
              }`}
            >
              {u}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <span className="text-slate-400">Sort By:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-slate-950 border border-slate-800 px-3 py-1 rounded-md text-xs text-slate-200"
          >
            <option value="margin_desc">Highest Margin</option>
            <option value="startup_asc">Lowest Startup Cost</option>
          </select>
        </div>
      </div>

      {/* Opportunities List */}
      {loading ? (
        <p className="text-slate-400 text-sm">Loading opportunities...</p>
      ) : filteredOpps.length === 0 ? (
        <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-500">
          No opportunities found. Click &quot;+ New Research Run&quot; above to discover viable business concepts.
        </div>
      ) : (
        <div className="space-y-6">
          {filteredOpps.map((opp) => (
            <div key={opp.id} className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
              {/* Header */}
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-3">
                    <h2 className="text-lg font-bold text-white">{opp.title}</h2>
                    <span className="text-xs px-2 py-0.5 rounded font-mono bg-indigo-950 text-indigo-300 border border-indigo-800">
                      {opp.revenue_model}
                    </span>
                    <span
                      className={`text-xs px-2 py-0.5 rounded font-mono border ${
                        opp.uncertainty === "LOW"
                          ? "bg-emerald-950 text-emerald-300 border-emerald-800"
                          : opp.uncertainty === "MEDIUM"
                          ? "bg-amber-950 text-amber-300 border-amber-800"
                          : "bg-purple-950 text-purple-300 border-purple-800"
                      }`}
                    >
                      Uncertainty: {opp.uncertainty}
                    </span>
                    <span className="text-xs px-2 py-0.5 rounded font-mono bg-slate-800 text-slate-300 border border-slate-700">
                      Evidence: {opp.evidence_quality}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 mt-1">{opp.description}</p>
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

              {/* Multi-dimensional Economics Grid */}
              <div className="grid grid-cols-2 md:grid-cols-6 gap-3 p-4 bg-slate-950 rounded-lg border border-slate-800 text-xs">
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

              {/* Low-cost Validation Experiment (Section 6) */}
              {opp.recommended_experiment && (
                <div className="p-4 rounded-lg bg-slate-950/80 border border-indigo-950/70 space-y-2 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-indigo-300">
                      Recommended Validation Experiment (Section 6):
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

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-2 border-t border-slate-800/80 text-xs">
                <button
                  onClick={() => setSelectedOpp(selectedOpp?.id === opp.id ? null : opp)}
                  className="text-indigo-400 hover:text-indigo-300 font-medium"
                >
                  {selectedOpp?.id === opp.id ? "Hide Evidence & Unknowns" : "View Classified Evidence & Unknowns &rarr;"}
                </button>

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

              {/* Extended Details Drawer */}
              {selectedOpp?.id === opp.id && (
                <div className="p-4 rounded-lg bg-slate-950 border border-slate-800 space-y-4 text-xs mt-3">
                  {/* Unknowns */}
                  {opp.unknowns && opp.unknowns.length > 0 && (
                    <div>
                      <h4 className="font-semibold text-amber-300 mb-1">Identified Unknowns & Risks:</h4>
                      <ul className="list-disc pl-4 space-y-0.5 text-slate-300">
                        {opp.unknowns.map((u, idx) => (
                          <li key={idx}>{u}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Evidence Table */}
                  <div>
                    <h4 className="font-semibold text-indigo-300 mb-2">Classified Evidence (Section 3):</h4>
                    <div className="space-y-2">
                      {opp.evidence.map((ev, idx) => (
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
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
