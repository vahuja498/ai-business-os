"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, ValidationPlanItem } from "@/lib/api";

const FAMILIES = [
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

const STATUSES = ["ALL", "DRAFT", "IN_PROGRESS", "COMPLETED", "PAUSED"];

export default function ValidationPage() {
  const [plans, setPlans] = useState<ValidationPlanItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [filterFamily, setFilterFamily] = useState<string>("ALL");
  const [filterStatus, setFilterStatus] = useState<string>("ALL");

  const loadPlans = async () => {
    try {
      setLoading(true);
      const data = await api.getValidationPlans(filterFamily, filterStatus);
      setPlans(data);
    } catch (err: any) {
      alert(`Error loading validation plans: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPlans();
  }, [filterFamily, filterStatus]);

  const handleSyncPlans = async () => {
    try {
      setSyncing(true);
      const res = await api.syncValidationPlans();
      alert(`Validation plans synced! ${res.data.created} created, ${res.data.updated} updated.`);
      loadPlans();
    } catch (err: any) {
      alert(`Sync failed: ${err.message}`);
    } finally {
      setSyncing(false);
    }
  };

  const totalBudgetSpent = plans.reduce((acc, p) => acc + (p.total_budget_spent || 0), 0);
  const totalBudgetAllocated = plans.reduce((acc, p) => acc + (p.total_budget_allocated || 0), 0);
  const avgConfidence = plans.length > 0 ? plans.reduce((acc, p) => acc + p.confidence_score, 0) / plans.length : 0;
  const totalHighRisk = plans.reduce((acc, p) => acc + (p.high_risk_assumptions_count || 0), 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Validation Engine</h1>
          <p className="text-sm text-slate-400">
            Falsification and structured experimentation engine testing the 24 Phase 4 opportunities before capital commitment.
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Link
            href="/validation/experiments"
            className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 transition"
          >
            Experiments Desk
          </Link>
          <Link
            href="/validation/approvals"
            className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 transition"
          >
            Validation Approvals
          </Link>
          <Link
            href="/validation/results"
            className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 transition"
          >
            Results & Evidence
          </Link>
          <button
            onClick={handleSyncPlans}
            disabled={syncing}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 font-semibold text-xs text-white rounded-lg shadow-md transition"
          >
            {syncing ? "Syncing Plans..." : "⚡ Sync Validation Plans"}
          </button>
        </div>
      </div>

      {/* Governance & Safety Notice */}
      <div className="p-3 bg-indigo-950/20 border border-indigo-900/40 rounded-lg text-xs text-indigo-300 flex items-center justify-between">
        <span>
          <strong>Phase 5 Invariant:</strong> Maximum budget ₹500 per experiment. All real-world actions disabled by default. Non-comparative confidence scoring without relative rankings (&quot;BEST&quot; / &quot;#1&quot;).
        </span>
        <span className="font-mono text-[11px] bg-indigo-900/50 px-2 py-0.5 rounded border border-indigo-700/50">
          SPENDING CAP ₹500 ENFORCED
        </span>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-900 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-500 block">Total Validation Plans</span>
          <span className="text-2xl font-bold font-mono text-white mt-1 block">{plans.length}</span>
          <span className="text-[11px] text-slate-400">24 target opportunities</span>
        </div>
        <div className="p-4 bg-slate-900 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-500 block">High-Risk Assumptions</span>
          <span className="text-2xl font-bold font-mono text-rose-400 mt-1 block">{totalHighRisk}</span>
          <span className="text-[11px] text-slate-400">3–7 prioritized per plan</span>
        </div>
        <div className="p-4 bg-slate-900 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-500 block">Total Budget (Allocated / Spent)</span>
          <span className="text-2xl font-bold font-mono text-emerald-400 mt-1 block">
            ₹{totalBudgetSpent.toFixed(0)} / ₹{totalBudgetAllocated.toFixed(0)}
          </span>
          <span className="text-[11px] text-slate-400">Strict &lt;= ₹500/exp cap</span>
        </div>
        <div className="p-4 bg-slate-900 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-500 block">Average Confidence Score</span>
          <span className="text-2xl font-bold font-mono text-indigo-400 mt-1 block">
            {(avgConfidence * 100).toFixed(1)}%
          </span>
          <span className="text-[11px] text-slate-400">Non-comparative ratio</span>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="space-y-3 p-4 bg-slate-900 rounded-xl border border-slate-800 text-xs">
        {/* Families */}
        <div className="flex items-center gap-2 overflow-x-auto pb-1">
          <span className="text-slate-400 font-medium whitespace-nowrap">Family:</span>
          {FAMILIES.map((fam) => (
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

        {/* Status */}
        <div className="flex items-center gap-4 pt-2 border-t border-slate-800/60">
          <div className="flex items-center gap-2">
            <span className="text-slate-400">Status:</span>
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="bg-slate-950 border border-slate-800 px-2 py-1 rounded text-slate-200"
            >
              {STATUSES.map((s) => (
                <option key={s} value={s}>
                  {s}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Validation Plans Grid */}
      {loading ? (
        <p className="text-slate-400 text-sm">Loading validation plans...</p>
      ) : plans.length === 0 ? (
        <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-500">
          No validation plans found. Click &quot;⚡ Sync Validation Plans&quot; above to initialize all 24 Phase 4 opportunities.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {plans.map((p) => (
            <div key={p.id} className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3 flex flex-col justify-between">
              <div>
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h2 className="text-base font-bold text-white hover:text-indigo-400 transition">
                      <Link href={`/validation/${p.opportunity_id}`}>{p.opportunity_title}</Link>
                    </h2>
                    <div className="flex flex-wrap items-center gap-1.5 mt-1">
                      <span className="text-[10px] px-2 py-0.5 rounded font-mono bg-indigo-950 text-indigo-300 border border-indigo-800">
                        {p.opportunity_family}
                      </span>
                      {p.regulatory_approval_required && (
                        <span className="text-[10px] px-2 py-0.5 rounded font-mono bg-amber-950/60 text-amber-300 border border-amber-800/50">
                          REGULATORY REVIEW
                        </span>
                      )}
                    </div>
                  </div>
                  <span
                    className={`text-xs px-2.5 py-0.5 rounded-full font-bold ${
                      p.status === "COMPLETED"
                        ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                        : p.status === "IN_PROGRESS"
                        ? "bg-indigo-950 text-indigo-300 border border-indigo-800"
                        : "bg-slate-800 text-slate-300 border border-slate-700"
                    }`}
                  >
                    {p.status}
                  </span>
                </div>

                <p className="text-xs text-slate-400 mt-2">
                  <strong className="text-slate-300">Customer:</strong> {p.customer || "B2B / Industrial SME"}
                </p>

                {/* Progress & Confidence Metric */}
                <div className="mt-3 pt-3 border-t border-slate-800/70 grid grid-cols-3 gap-2 text-xs">
                  <div>
                    <span className="text-slate-500 block text-[11px]">Confidence</span>
                    <span className="font-mono text-indigo-400 font-bold">
                      {(p.confidence_score * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[11px]">High-Risk Items</span>
                    <span className="font-mono text-rose-400 font-semibold">{p.high_risk_assumptions_count}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[11px]">Budget Spent</span>
                    <span className="font-mono text-emerald-400 font-semibold">
                      ₹{p.total_budget_spent.toFixed(0)} / ₹{p.total_budget_allocated.toFixed(0)}
                    </span>
                  </div>
                </div>
              </div>

              <div className="pt-2 border-t border-slate-800 flex items-center justify-between text-xs">
                <span className="text-[11px] text-slate-500">
                  {p.completed_experiments_count} experiments completed
                </span>
                <Link
                  href={`/validation/${p.opportunity_id}`}
                  className="text-indigo-400 hover:text-indigo-300 font-medium"
                >
                  View Validation Plan &rarr;
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
