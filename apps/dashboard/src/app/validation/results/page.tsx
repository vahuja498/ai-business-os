"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, ExperimentResultItem } from "@/lib/api";

export default function ValidationResultsPage() {
  const [results, setResults] = useState<ExperimentResultItem[]>([]);
  const [loading, setLoading] = useState(true);

  const loadResults = async () => {
    try {
      setLoading(true);
      const data = await api.getValidationResults();
      setResults(data);
    } catch (err: any) {
      alert(`Error loading validation results: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadResults();
  }, []);

  const totalSpent = results.reduce((acc, r) => acc + (r.cost_spent || 0), 0);
  const passCount = results.filter((r) => r.outcome === "PASS").length;
  const failCount = results.filter((r) => r.outcome === "FAIL").length;
  const inconclusiveCount = results.filter((r) => r.outcome === "INCONCLUSIVE").length;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs text-slate-400 mb-1">
            <Link href="/validation" className="hover:text-white transition">
              Validation Engine
            </Link>
            <span>/</span>
            <span className="text-slate-200">Results & Evidence</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Validation Results & Empirical Evidence</h1>
          <p className="text-sm text-slate-400">
            Immutable log of experiment outcomes and verified empirical artifacts enforcing anti-fabrication integrity.
          </p>
        </div>

        <Link
          href="/validation"
          className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 transition"
        >
          &larr; Back to Validation Plans
        </Link>
      </div>

      {/* Summary Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="p-4 bg-slate-900 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-500 block">Total Experiments Run</span>
          <span className="text-2xl font-bold font-mono text-white mt-1 block">{results.length}</span>
          <span className="text-[11px] text-slate-400">Simulated test runs</span>
        </div>
        <div className="p-4 bg-slate-900 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-500 block">PASS Outcomes</span>
          <span className="text-2xl font-bold font-mono text-emerald-400 mt-1 block">{passCount}</span>
          <span className="text-[11px] text-slate-400">Validated hypotheses</span>
        </div>
        <div className="p-4 bg-slate-900 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-500 block">FAIL Outcomes</span>
          <span className="text-2xl font-bold font-mono text-rose-400 mt-1 block">{failCount}</span>
          <span className="text-[11px] text-slate-400">Falsified assumptions</span>
        </div>
        <div className="p-4 bg-slate-900 rounded-xl border border-slate-800">
          <span className="text-xs text-slate-500 block">Total Incurred Cost</span>
          <span className="text-2xl font-bold font-mono text-indigo-400 mt-1 block">₹{totalSpent.toFixed(2)}</span>
          <span className="text-[11px] text-slate-400">Avg &lt;= ₹500/run cap</span>
        </div>
      </div>

      {/* Results Log */}
      {loading ? (
        <p className="text-slate-400 text-sm">Loading experiment results...</p>
      ) : results.length === 0 ? (
        <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-500">
          No experiment results recorded yet. Run a simulated dry-run from an Opportunity Validation Plan or the Experiments Desk.
        </div>
      ) : (
        <div className="space-y-4">
          {results.map((res) => (
            <div key={res.id} className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3 text-xs">
              <div className="flex flex-col md:flex-row md:items-start justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span
                      className={`font-mono text-[10px] px-2.5 py-0.5 rounded font-bold ${
                        res.outcome === "PASS"
                          ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                          : res.outcome === "FAIL"
                          ? "bg-rose-950 text-rose-300 border border-rose-800"
                          : "bg-amber-950 text-amber-300 border border-amber-800"
                      }`}
                    >
                      {res.outcome}
                    </span>
                    <span className="font-mono text-[10px] px-2 py-0.5 rounded bg-indigo-950/50 text-indigo-300 border border-indigo-900/50">
                      SIMULATION
                    </span>
                    <Link
                      href={`/validation/${res.opportunity_id}`}
                      className="font-bold text-white hover:text-indigo-400 transition"
                    >
                      {res.opportunity_title}
                    </Link>
                  </div>
                  <h3 className="text-slate-300 font-semibold text-xs mt-1">{res.experiment_title}</h3>
                </div>

                <div className="text-right">
                  <span className="font-mono text-emerald-400 font-bold block">₹{res.cost_spent.toFixed(2)}</span>
                  <span className="text-[10px] text-slate-500 font-mono">{res.executed_at}</span>
                </div>
              </div>

              {/* Observed Metric & Evidence */}
              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1.5">
                <div>
                  <span className="text-slate-500 block text-[11px]">Observed Metric:</span>
                  <p className="text-slate-200 font-medium">{res.metric_observed}</p>
                </div>

                {res.notes && (
                  <div>
                    <span className="text-slate-500 block text-[11px]">Notes:</span>
                    <p className="text-slate-400">{res.notes}</p>
                  </div>
                )}

                {res.evidence_artifacts && res.evidence_artifacts.length > 0 && (
                  <div className="pt-1 border-t border-slate-900">
                    <span className="text-slate-500 block text-[11px]">Evidence Artifacts:</span>
                    <div className="flex flex-wrap gap-1.5 mt-0.5">
                      {res.evidence_artifacts.map((art: any, idx: number) => (
                        <span
                          key={idx}
                          className="font-mono text-[10px] px-2 py-0.5 rounded bg-slate-900 text-slate-300 border border-slate-800"
                        >
                          📄 {typeof art === "string" ? art : JSON.stringify(art)}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
