"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { api, ValidationPlanDetail } from "@/lib/api";

export default function OpportunityValidationPlanPage() {
  const params = useParams();
  const opportunityId = params?.opportunity_id as string;

  const [planDetail, setPlanDetail] = useState<ValidationPlanDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [runningExpId, setRunningExpId] = useState<string | null>(null);
  const [showRunModal, setShowRunModal] = useState<string | null>(null);
  const [simOutcome, setSimOutcome] = useState<string>("PASS");
  const [simMetric, setSimMetric] = useState<string>("3 out of 10 prospective respondents confirmed intent.");
  const [simCost, setSimCost] = useState<number>(150.0);
  const [simNotes, setSimNotes] = useState<string>("Simulated digital inquiry response test completed without live outreach.");
  const [updateClassification, setUpdateClassification] = useState<string>("SUPPORTED_ESTIMATE");
  const [simJustification, setSimJustification] = useState<string>("Evidence gathered from simulated response logs.");

  const loadDetail = async () => {
    if (!opportunityId) return;
    try {
      setLoading(true);
      const data = await api.getValidationPlanByOpportunity(opportunityId);
      setPlanDetail(data);
    } catch (err: any) {
      alert(`Error loading validation plan: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDetail();
  }, [opportunityId]);

  const handleExecuteExperiment = async () => {
    if (!showRunModal) return;
    try {
      setRunningExpId(showRunModal);
      await api.runValidationExperiment(showRunModal, {
        outcome: simOutcome,
        metric_observed: simMetric,
        cost_spent: simCost,
        evidence_artifacts: ["simulated_response_log.json", "intake_sample.pdf"],
        notes: simNotes,
        is_simulation: true,
        update_assumption_to: updateClassification || undefined,
        justification: simJustification,
      });
      alert("Experiment executed in simulation mode! Assumption classification updated safely.");
      setShowRunModal(null);
      loadDetail();
    } catch (err: any) {
      alert(`Execution failed: ${err.message}`);
    } finally {
      setRunningExpId(null);
    }
  };

  if (loading) {
    return <div className="p-8 text-slate-400 text-sm">Loading validation plan detail...</div>;
  }

  if (!planDetail) {
    return (
      <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-400">
        Validation plan not found. <Link href="/validation" className="text-indigo-400 underline">Return to Validation Overview</Link>
      </div>
    );
  }

  const { opportunity: opp, plan, budget, assumptions, experiments, approvals, audit_trail } = planDetail;

  return (
    <div className="space-y-6">
      {/* Breadcrumb Navigation */}
      <div className="flex items-center gap-2 text-xs text-slate-400">
        <Link href="/validation" className="hover:text-white transition">
          Validation Plans
        </Link>
        <span>/</span>
        <span className="text-slate-200 font-medium">{opp.title}</span>
      </div>

      {/* Header Banner */}
      <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-3">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h1 className="text-xl font-bold text-white">{opp.title}</h1>
              <span className="text-xs px-2 py-0.5 rounded font-mono bg-indigo-950 text-indigo-300 border border-indigo-800">
                {opp.opportunity_family}
              </span>
              <span className="text-xs px-2 py-0.5 rounded font-mono bg-slate-800 text-slate-300">
                {opp.revenue_model}
              </span>
              <span
                className={`text-xs px-2 py-0.5 rounded-full font-bold ${
                  opp.pursue_status === "VIABLE_NOW"
                    ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                    : "bg-rose-950 text-rose-300 border border-rose-800"
                }`}
              >
                {opp.pursue_status}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              <strong className="text-slate-300">Target Customer:</strong> {opp.customer || "Industrial SME"} &bull;{" "}
              <strong className="text-slate-300">Startup Capital:</strong> ₹{opp.estimated_startup_cost.toFixed(0)} &bull;{" "}
              <strong className="text-slate-300">Target Margin:</strong> {(opp.estimated_margin * 100).toFixed(0)}%
            </p>
          </div>

          <span
            className={`text-xs px-3 py-1 rounded font-bold self-start ${
              plan.status === "COMPLETED"
                ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                : plan.status === "IN_PROGRESS"
                ? "bg-indigo-950 text-indigo-300 border border-indigo-800"
                : "bg-slate-800 text-slate-300 border border-slate-700"
            }`}
          >
            {plan.status}
          </span>
        </div>

        {/* Confidence & Budget Banner */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 p-3 bg-slate-950 rounded-lg border border-slate-800 text-xs">
          <div>
            <span className="text-slate-500 block text-[11px]">Validation Confidence Score</span>
            <span className="font-mono text-lg font-bold text-indigo-400">
              {(plan.confidence_score * 100).toFixed(1)}%
            </span>
            <span className="text-[10px] text-slate-500 block">Non-comparative internal ratio</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[11px]">Material Assumptions</span>
            <span className="font-mono text-lg font-bold text-white">
              {plan.material_assumptions_count} <span className="text-xs text-rose-400">({plan.high_risk_assumptions_count} high-risk)</span>
            </span>
            <span className="text-[10px] text-slate-500 block">Pillars: Demand, CAC, Regs</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[11px]">Experiments Status</span>
            <span className="font-mono text-lg font-bold text-emerald-400">
              {plan.completed_experiments_count} / {experiments.length}
            </span>
            <span className="text-[10px] text-slate-500 block">Completed in simulation</span>
          </div>
          <div>
            <span className="text-slate-500 block text-[11px]">Validation Budget Spent</span>
            <span className="font-mono text-lg font-bold text-emerald-400">
              ₹{plan.total_budget_spent.toFixed(0)} / ₹{plan.total_budget_allocated.toFixed(0)}
            </span>
            <span className="text-[10px] text-slate-500 block">Cap: ₹500/exp (Pool: ₹{budget?.max_budget || 2500})</span>
          </div>
        </div>
      </div>

      {/* Material Assumptions Section */}
      <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-white flex items-center gap-2">
            <span>📋</span> Material Assumptions ({assumptions.length})
          </h2>
          <span className="text-xs text-slate-400">
            Top {assumptions.filter((a) => a.is_highest_risk).length} highest-risk items prioritized for testing
          </span>
        </div>

        <div className="space-y-2">
          {assumptions.map((asm) => (
            <div
              key={asm.id}
              className={`p-3 rounded-lg border text-xs flex flex-col md:flex-row md:items-center justify-between gap-3 ${
                asm.is_highest_risk
                  ? "bg-rose-950/10 border-rose-900/40"
                  : "bg-slate-950 border-slate-800"
              }`}
            >
              <div className="space-y-1 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">
                    {asm.category}
                  </span>
                  {asm.is_highest_risk && (
                    <span className="font-mono text-[10px] px-1.5 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">
                      HIGH RISK
                    </span>
                  )}
                  <span
                    className={`font-mono text-[10px] px-2 py-0.5 rounded font-bold ${
                      asm.classification === "VERIFIED"
                        ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                        : asm.classification === "SUPPORTED_ESTIMATE"
                        ? "bg-indigo-950 text-indigo-300 border border-indigo-800"
                        : asm.classification === "UNKNOWN"
                        ? "bg-purple-950 text-purple-300 border border-purple-800"
                        : asm.classification === "CONTRADICTED"
                        ? "bg-red-950 text-red-300 border border-red-800"
                        : "bg-slate-800 text-slate-400"
                    }`}
                  >
                    {asm.classification}
                  </span>
                </div>
                <p className="text-slate-200 font-medium">{asm.statement}</p>
                {asm.evidence_notes && (
                  <p className="text-[11px] text-slate-500">
                    <strong className="text-slate-400">Context:</strong> {asm.evidence_notes}
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Validation Experiments Section */}
      <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <span>🔬</span> Micro-Validation Experiments ({experiments.length})
            </h2>
            <p className="text-xs text-slate-400">
              Cheapest realistic tests generating empirical evidence with strict &lt;= ₹500 budget caps.
            </p>
          </div>
        </div>

        <div className="space-y-4">
          {experiments.map((exp) => (
            <div key={exp.id} className="p-4 rounded-xl bg-slate-950 border border-slate-800 space-y-3 text-xs">
              <div className="flex flex-col md:flex-row md:items-start justify-between gap-2">
                <div>
                  <h3 className="text-sm font-bold text-white">{exp.title}</h3>
                  <div className="flex flex-wrap items-center gap-2 mt-1">
                    <span className="font-mono text-emerald-400 font-bold bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-900/50">
                      Budget: ₹{exp.budget.toFixed(2)}
                    </span>
                    <span className="font-mono text-slate-400 bg-slate-900 px-2 py-0.5 rounded">
                      Duration: {exp.duration_days} days
                    </span>
                    <span className="font-mono text-indigo-400 bg-indigo-950/40 px-2 py-0.5 rounded border border-indigo-900/40">
                      SIMULATION ONLY
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <span
                    className={`font-mono text-[10px] px-2 py-0.5 rounded font-bold ${
                      exp.execution_status === "COMPLETED"
                        ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                        : "bg-slate-800 text-slate-300"
                    }`}
                  >
                    {exp.execution_status}
                  </span>
                  <button
                    onClick={() => setShowRunModal(exp.id)}
                    className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 font-semibold text-xs text-white rounded-md transition shadow"
                  >
                    Run Dry-Run
                  </button>
                </div>
              </div>

              {/* Hypothesis & Methodology */}
              <div className="space-y-1 text-slate-300">
                <p>
                  <strong className="text-slate-400">Hypothesis:</strong> {exp.hypothesis}
                </p>
                <p>
                  <strong className="text-slate-400">Methodology:</strong> {exp.methodology}
                </p>
              </div>

              {/* Criteria Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-2 p-2.5 bg-slate-900 rounded-lg border border-slate-800">
                <div>
                  <span className="font-semibold text-emerald-400 block mb-0.5">PASS Criteria:</span>
                  <p className="text-[11px] text-slate-300">{exp.pass_criteria}</p>
                </div>
                <div>
                  <span className="font-semibold text-red-400 block mb-0.5">FAIL Criteria:</span>
                  <p className="text-[11px] text-slate-300">{exp.fail_criteria}</p>
                </div>
                <div>
                  <span className="font-semibold text-amber-400 block mb-0.5">INCONCLUSIVE:</span>
                  <p className="text-[11px] text-slate-300">{exp.inconclusive_criteria}</p>
                </div>
              </div>

              {/* Automation vs Human Breakdown */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] pt-1">
                <div>
                  <span className="text-indigo-300 font-semibold">🤖 Automated Tasks:</span>{" "}
                  <span className="text-slate-400">{exp.automated_tasks}</span>
                </div>
                <div>
                  <span className="text-amber-300 font-semibold">👤 Human Tasks:</span>{" "}
                  <span className="text-slate-400">{exp.human_tasks}</span>
                </div>
              </div>

              {exp.regulatory_requirements && (
                <div className="text-[11px] text-cyan-300 pt-1 border-t border-slate-800/60">
                  <span className="font-semibold">⚖️ Regulatory / Compliance:</span> {exp.regulatory_requirements}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Audit Trail Drawer */}
      {audit_trail && audit_trail.length > 0 && (
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-3 text-xs">
          <h2 className="text-sm font-bold text-white flex items-center gap-2">
            <span>🛡️</span> Validation Audit Trail ({audit_trail.length})
          </h2>
          <div className="space-y-1.5">
            {audit_trail.map((entry) => (
              <div key={entry.id} className="p-2.5 bg-slate-950 rounded border border-slate-800 flex items-center justify-between">
                <div>
                  <span className="font-mono text-indigo-400 font-semibold">{entry.action}</span>{" "}
                  <span className="text-slate-400">by {entry.actor}</span>
                  <p className="text-[11px] text-slate-500 font-mono mt-0.5">{JSON.stringify(entry.details)}</p>
                </div>
                <span className="text-[10px] text-slate-500 font-mono">{entry.timestamp}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Simulated Dry-Run Modal */}
      {showRunModal && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-6 z-50">
          <div className="bg-slate-900 border border-slate-800 rounded-xl max-w-lg w-full p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <h3 className="text-base font-bold text-white">Execute Simulated Validation Dry-Run</h3>
              <button onClick={() => setShowRunModal(null)} className="text-slate-400 hover:text-white text-sm">
                ✕ Close
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div>
                <label className="block text-slate-400 mb-1">Outcome</label>
                <select
                  value={simOutcome}
                  onChange={(e) => setSimOutcome(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 p-2 rounded text-slate-200"
                >
                  <option value="PASS">PASS</option>
                  <option value="FAIL">FAIL</option>
                  <option value="INCONCLUSIVE">INCONCLUSIVE</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Observed Metric</label>
                <input
                  type="text"
                  value={simMetric}
                  onChange={(e) => setSimMetric(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 p-2 rounded text-slate-200"
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Cost Incurred (₹ &lt;= 500)</label>
                <input
                  type="number"
                  max={500}
                  min={0}
                  value={simCost}
                  onChange={(e) => setSimCost(Number(e.target.value))}
                  className="w-full bg-slate-950 border border-slate-800 p-2 rounded text-slate-200"
                />
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Update Assumption Classification To</label>
                <select
                  value={updateClassification}
                  onChange={(e) => setUpdateClassification(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 p-2 rounded text-slate-200"
                >
                  <option value="SUPPORTED_ESTIMATE">SUPPORTED_ESTIMATE</option>
                  <option value="VERIFIED">VERIFIED (Requires Empirical Evidence)</option>
                  <option value="CONTRADICTED">CONTRADICTED</option>
                  <option value="UNKNOWN">UNKNOWN</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-400 mb-1">Justification / Evidence Explanation</label>
                <textarea
                  rows={2}
                  value={simJustification}
                  onChange={(e) => setSimJustification(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 p-2 rounded text-slate-200 font-mono"
                />
              </div>
            </div>

            <div className="flex justify-end gap-2 pt-2 border-t border-slate-800">
              <button
                onClick={() => setShowRunModal(null)}
                className="px-3 py-1.5 text-xs text-slate-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleExecuteExperiment}
                disabled={runningExpId !== null}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-xs font-semibold text-white rounded-md transition shadow"
              >
                {runningExpId ? "Simulating..." : "Confirm & Record Result"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
