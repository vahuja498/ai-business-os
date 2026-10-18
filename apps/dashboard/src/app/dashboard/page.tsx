"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, DashboardSummary, API_BASE } from "@/lib/api";

export default function DashboardPage() {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const res = await api.getDashboardSummary();
      setData(res);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Failed to connect to AI Business OS API");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleApprove = async (id: string) => {
    try {
      await api.approve(id);
      loadData();
    } catch (err: any) {
      alert(`Approval error: ${err.message}`);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-400">
        <p>Connecting to AI Business OS runtime...</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">System Overview</h1>
        <p className="text-sm text-slate-400">Autonomous Business Operating System Mission Control</p>
      </div>

      {error && (
        <div className="p-4 rounded-lg bg-red-950/40 border border-red-800 text-red-300 text-sm">
          <strong>API Offline or Unreachable ({API_BASE}):</strong> {error}. Ensure backend is active and CORS is permitted.
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-sm">
          <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Active Businesses</p>
          <p className="mt-2 text-3xl font-bold text-white">{data?.metrics.active_businesses ?? 0}</p>
          <p className="mt-1 text-xs text-slate-500">Autonomous modules</p>
        </div>

        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-sm">
          <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Discovered Opportunities</p>
          <p className="mt-2 text-3xl font-bold text-indigo-400">{data?.metrics.open_opportunities ?? 0}</p>
          <p className="mt-1 text-xs text-slate-500">Validated by Research Agent</p>
        </div>

        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-sm">
          <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">Pending Approvals</p>
          <p className={`mt-2 text-3xl font-bold ${(data?.metrics.pending_approvals ?? 0) > 0 ? "text-amber-400" : "text-slate-400"}`}>
            {data?.metrics.pending_approvals ?? 0}
          </p>
          <p className="mt-1 text-xs text-slate-500">Awaiting human sign-off</p>
        </div>

        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800 shadow-sm">
          <p className="text-xs font-medium text-slate-400 uppercase tracking-wider">System Health</p>
          <p className="mt-2 text-3xl font-bold text-emerald-400">{data?.metrics.system_health ?? "ONLINE"}</p>
          <p className="mt-1 text-xs text-slate-500">All guardrails active</p>
        </div>
      </div>

      {/* Pending Approvals Section */}
      <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold text-white">Pending Human Approvals</h2>
            <p className="text-xs text-slate-400">High-risk actions, budgets, and contracts require human authorization</p>
          </div>
          <Link href="/approvals" className="text-xs text-indigo-400 hover:text-indigo-300">
            View All &rarr;
          </Link>
        </div>

        {!data?.pending_approvals || data.pending_approvals.length === 0 ? (
          <p className="text-sm text-slate-500 py-4">No pending approvals. System is operating safely within autonomous limits.</p>
        ) : (
          <div className="space-y-3">
            {data.pending_approvals.map((app) => (
              <div key={app.id} className="p-4 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800/50 font-medium">
                      {app.risk_level}
                    </span>
                    <span className="text-sm font-semibold text-white">{app.action_type}</span>
                    {app.amount && (
                      <span className="text-xs font-mono text-emerald-400">₹{app.amount.toFixed(2)}</span>
                    )}
                  </div>
                  <p className="mt-1 text-xs text-slate-300">{app.description}</p>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleApprove(app.id)}
                    className="px-3 py-1.5 text-xs font-medium bg-emerald-600 hover:bg-emerald-500 text-white rounded-md transition shadow"
                  >
                    Approve
                  </button>
                  <Link
                    href={`/approvals`}
                    className="px-3 py-1.5 text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-md transition"
                  >
                    Review
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Two column: Discovered Opportunities & Recent Agent Activity */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Opportunities */}
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">Recent Opportunities</h2>
            <Link href="/opportunities" className="text-xs text-indigo-400 hover:text-indigo-300">
              View All &rarr;
            </Link>
          </div>
          {!data?.recent_opportunities || data.recent_opportunities.length === 0 ? (
            <p className="text-sm text-slate-500 py-4">No opportunities discovered yet. Assign an objective to AI CEO.</p>
          ) : (
            <div className="space-y-3">
              {data.recent_opportunities.map((opp) => (
                <div key={opp.id} className="p-3 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-white">{opp.title}</p>
                    <p className="text-xs text-slate-400">Est. Margin: <span className="text-emerald-400 font-mono">{(opp.margin * 100).toFixed(0)}%</span></p>
                  </div>
                  <span className={`text-xs px-2 py-0.5 rounded font-mono ${opp.status === "APPROVED" ? "bg-emerald-950 text-emerald-300 border border-emerald-800" : "bg-amber-950 text-amber-300 border border-amber-800"}`}>
                    {opp.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Agent Runs */}
        <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white">Agent Execution Stream</h2>
            <Link href="/agents" className="text-xs text-indigo-400 hover:text-indigo-300">
              View All &rarr;
            </Link>
          </div>
          {!data?.recent_runs || data.recent_runs.length === 0 ? (
            <p className="text-sm text-slate-500 py-4">No agent runs recorded.</p>
          ) : (
            <div className="space-y-3">
              {data.recent_runs.map((run) => (
                <div key={run.id} className="p-3 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between text-xs">
                  <div>
                    <span className="font-mono text-indigo-400">{run.agent_id.substring(0, 8)}...</span>
                    <p className="text-slate-400 text-[11px]">{new Date(run.started_at).toLocaleTimeString()}</p>
                  </div>
                  <span className="px-2 py-0.5 rounded font-medium bg-slate-800 text-slate-200">
                    {run.final_status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
