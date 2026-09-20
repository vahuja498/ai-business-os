"use client";

import { useEffect, useState } from "react";
import { api, ApprovalItem } from "@/lib/api";

export default function ApprovalsPage() {
  const [approvals, setApprovals] = useState<ApprovalItem[]>([]);
  const [filter, setFilter] = useState<string>("ALL");
  const [loading, setLoading] = useState(true);

  const loadApprovals = async () => {
    try {
      setLoading(true);
      const res = await api.getApprovals(filter === "ALL" ? undefined : filter);
      setApprovals(res);
    } catch (err: any) {
      alert(`Error loading approvals: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadApprovals();
  }, [filter]);

  const handleApprove = async (id: string) => {
    try {
      await api.approve(id);
      loadApprovals();
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    }
  };

  const handleReject = async (id: string) => {
    const reason = prompt("Enter rejection reason:", "Not approved by operator");
    if (reason === null) return;
    try {
      await api.reject(id, reason);
      loadApprovals();
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Human Approval Gate</h1>
          <p className="text-sm text-slate-400">Strict human authorization for high-risk operations, financial commitments, and contracts.</p>
        </div>
        <div className="flex gap-2">
          {["ALL", "PENDING", "APPROVED", "REJECTED"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 text-xs font-medium rounded-md transition ${
                filter === f
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-900 border border-slate-800 text-slate-400 hover:text-white"
              }`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <p className="text-slate-400 text-sm">Loading approvals...</p>
      ) : approvals.length === 0 ? (
        <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-500">
          No approval records found for filter &quot;{filter}&quot;.
        </div>
      ) : (
        <div className="space-y-4">
          {approvals.map((app) => (
            <div key={app.id} className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs px-2 py-0.5 rounded bg-red-950 text-red-400 border border-red-800/50 font-bold">
                      {app.risk_level} RISK
                    </span>
                    <span className="text-base font-semibold text-white">{app.action_type}</span>
                    {app.amount !== null && (
                      <span className="text-sm font-mono text-emerald-400 font-semibold">₹{app.amount.toFixed(2)}</span>
                    )}
                  </div>
                  <p className="text-sm text-slate-300 mt-1">{app.description}</p>
                </div>
                <span
                  className={`text-xs px-2.5 py-1 rounded font-bold ${
                    app.status === "APPROVED"
                      ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                      : app.status === "REJECTED"
                      ? "bg-red-950 text-red-300 border border-red-800"
                      : "bg-amber-950 text-amber-300 border border-amber-800"
                  }`}
                >
                  {app.status}
                </span>
              </div>

              {app.reason && (
                <div className="p-3 bg-slate-950 rounded-lg border border-slate-800/60 text-xs text-slate-400">
                  <span className="font-semibold text-slate-300">Justification:</span> {app.reason}
                </div>
              )}

              {app.status === "PENDING" && (
                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    onClick={() => handleReject(app.id)}
                    className="px-4 py-2 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-red-400 hover:text-red-300 transition"
                  >
                    Reject Action
                  </button>
                  <button
                    onClick={() => handleApprove(app.id)}
                    className="px-4 py-2 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white shadow-md transition"
                  >
                    Approve & Authorize
                  </button>
                </div>
              )}

              {app.status === "APPROVED" && (
                <p className="text-xs text-slate-500">
                  Approved by <span className="text-slate-300">{app.approved_by}</span> on {new Date(app.approved_at!).toLocaleString()}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
