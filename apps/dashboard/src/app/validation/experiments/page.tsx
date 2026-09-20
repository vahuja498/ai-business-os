"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, ValidationExperimentItem } from "@/lib/api";

export default function ExperimentsPage() {
  const [experiments, setExperiments] = useState<ValidationExperimentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<string>("ALL");
  const [executingId, setExecutingId] = useState<string | null>(null);

  const loadExperiments = async () => {
    try {
      setLoading(true);
      const data = await api.getValidationExperiments(undefined, filterStatus);
      setExperiments(data);
    } catch (err: any) {
      alert(`Error loading experiments: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadExperiments();
  }, [filterStatus]);

  const handleQuickSimulate = async (expId: string) => {
    try {
      setExecutingId(expId);
      await api.runValidationExperiment(expId, {
        outcome: "PASS",
        metric_observed: "Simulated inquiry test yielded 3/10 positive responses.",
        cost_spent: 100.0,
        evidence_artifacts: ["sim_log_quick.json"],
        notes: "Quick simulation run from Experiments Desk.",
        is_simulation: true,
      });
      alert("Experiment executed in simulation mode!");
      loadExperiments();
    } catch (err: any) {
      alert(`Execution error: ${err.message}`);
    } finally {
      setExecutingId(null);
    }
  };

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
            <span className="text-slate-200">Experiments Desk</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Validation Experiments Desk</h1>
          <p className="text-sm text-slate-400">
            Centrally monitor and simulate validation experiments with strict &lt;= ₹500 spending controls.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            href="/validation"
            className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 transition"
          >
            &larr; Back to Validation Plans
          </Link>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="flex items-center justify-between p-3 bg-slate-900 rounded-xl border border-slate-800 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-slate-400">Execution Status:</span>
          {["ALL", "PENDING", "COMPLETED"].map((st) => (
            <button
              key={st}
              onClick={() => setFilterStatus(st)}
              className={`px-2.5 py-1 rounded-md transition ${
                filterStatus === st
                  ? "bg-indigo-600 text-white font-semibold"
                  : "bg-slate-950 text-slate-400 hover:text-white border border-slate-800"
              }`}
            >
              {st}
            </button>
          ))}
        </div>
        <span className="text-slate-400 font-mono text-[11px]">{experiments.length} experiments listed</span>
      </div>

      {/* Experiments List */}
      {loading ? (
        <p className="text-slate-400 text-sm">Loading experiments...</p>
      ) : experiments.length === 0 ? (
        <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-500">
          No experiments found matching current filters.
        </div>
      ) : (
        <div className="space-y-4">
          {experiments.map((exp) => (
            <div key={exp.id} className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-3 text-xs">
              <div className="flex flex-col md:flex-row md:items-start justify-between gap-2">
                <div>
                  <h2 className="text-sm font-bold text-white">{exp.title}</h2>
                  <p className="text-slate-400 text-[11px] mt-0.5">
                    Opportunity:{" "}
                    <Link
                      href={`/validation/${exp.opportunity_id}`}
                      className="text-indigo-400 hover:underline font-semibold"
                    >
                      {exp.opportunity_title}
                    </Link>{" "}
                    ({exp.opportunity_family})
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <span className="font-mono text-emerald-400 font-bold bg-emerald-950/50 px-2 py-0.5 rounded border border-emerald-900/50">
                    Budget: ₹{exp.budget.toFixed(2)}
                  </span>
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
                    onClick={() => handleQuickSimulate(exp.id)}
                    disabled={executingId === exp.id}
                    className="px-3 py-1 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-white font-semibold rounded transition"
                  >
                    {executingId === exp.id ? "Simulating..." : "Simulate Run"}
                  </button>
                </div>
              </div>

              <div className="p-3 bg-slate-950 rounded-lg border border-slate-800 space-y-1.5 text-slate-300">
                <p>
                  <strong className="text-slate-400">Hypothesis:</strong> {exp.hypothesis}
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2 pt-1 text-[11px]">
                  <div>
                    <span className="text-emerald-400 font-semibold block">PASS:</span>
                    <span className="text-slate-300">{exp.pass_criteria}</span>
                  </div>
                  <div>
                    <span className="text-red-400 font-semibold block">FAIL:</span>
                    <span className="text-slate-300">{exp.fail_criteria}</span>
                  </div>
                  <div>
                    <span className="text-amber-400 font-semibold block">INCONCLUSIVE:</span>
                    <span className="text-slate-300">{exp.inconclusive_criteria}</span>
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between text-[11px] text-slate-500 pt-1">
                <span>
                  Automation: <strong className="text-slate-400">{exp.automated_tasks}</strong>
                </span>
                <span className="font-mono text-indigo-400">SAFETY: SIMULATION MODE ENFORCED</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
