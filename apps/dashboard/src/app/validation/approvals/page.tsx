"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api, ValidationApprovalItem } from "@/lib/api";

export default function ValidationApprovalsPage() {
  const [approvals, setApprovals] = useState<ValidationApprovalItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState<string>("ALL");
  const [actingId, setActingId] = useState<string | null>(null);

  const loadApprovals = async () => {
    try {
      setLoading(true);
      const data = await api.getValidationApprovals(filterStatus);
      setApprovals(data);
    } catch (err: any) {
      alert(`Error loading validation approvals: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadApprovals();
  }, [filterStatus]);

  const handleDecision = async (approvalId: string, action: "APPROVE" | "REJECT") => {
    let reason: string | undefined = undefined;
    if (action === "REJECT") {
      const input = prompt("Please provide a rejection reason:");
      if (input === null) return; // User cancelled
      reason = input || "Declined by human reviewer";
    }

    try {
      setActingId(approvalId);
      await api.decideValidationApproval(approvalId, action, "HumanReviewer", reason);
      alert(`Approval ${action === "APPROVE" ? "granted" : "rejected"} successfully.`);
      loadApprovals();
    } catch (err: any) {
      alert(`Decision error: ${err.message}`);
    } finally {
      setActingId(null);
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
            <span className="text-slate-200">Validation Approvals Gate</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">Validation Approvals Gate</h1>
          <p className="text-sm text-slate-400">
            Mandatory human authorization gate for validation budget allocations and regulatory clearance checks.
          </p>
        </div>

        <Link
          href="/validation"
          className="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 rounded-lg border border-slate-700 transition"
        >
          &larr; Back to Validation Plans
        </Link>
      </div>

      {/* Filter Bar */}
      <div className="flex items-center justify-between p-3 bg-slate-900 rounded-xl border border-slate-800 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-slate-400">Filter:</span>
          {["ALL", "PENDING", "APPROVED", "REJECTED"].map((st) => (
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
        <span className="text-slate-400 font-mono text-[11px]">{approvals.length} approvals</span>
      </div>

      {/* Approvals List */}
      {loading ? (
        <p className="text-slate-400 text-sm">Loading validation approvals...</p>
      ) : approvals.length === 0 ? (
        <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-500">
          No validation approvals found.
        </div>
      ) : (
        <div className="space-y-4">
          {approvals.map((apprv) => (
            <div key={apprv.id} className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3 text-xs">
              <div className="flex flex-col md:flex-row md:items-start justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="font-mono text-[10px] px-2 py-0.5 rounded font-bold bg-indigo-950 text-indigo-300 border border-indigo-800">
                      {apprv.approval_type}
                    </span>
                    <span
                      className={`font-mono text-[10px] px-2 py-0.5 rounded font-bold ${
                        apprv.risk_level === "HIGH"
                          ? "bg-rose-950 text-rose-300 border border-rose-800"
                          : "bg-amber-950 text-amber-300 border border-amber-800"
                      }`}
                    >
                      RISK: {apprv.risk_level}
                    </span>
                    <Link
                      href={`/validation/${apprv.opportunity_id}`}
                      className="font-bold text-white hover:text-indigo-400 text-sm transition"
                    >
                      {apprv.opportunity_title}
                    </Link>
                  </div>
                  <p className="text-slate-300 text-xs mt-1">{apprv.description}</p>
                </div>

                <div className="flex items-center gap-2">
                  <span
                    className={`font-mono text-[10px] px-2.5 py-1 rounded font-bold ${
                      apprv.status === "APPROVED"
                        ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                        : apprv.status === "REJECTED"
                        ? "bg-rose-950 text-rose-300 border border-rose-800"
                        : "bg-amber-950 text-amber-300 border border-amber-800"
                    }`}
                  >
                    {apprv.status}
                  </span>
                </div>
              </div>

              {/* Action Controls if PENDING */}
              {apprv.status === "PENDING" && (
                <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
                  <span className="text-[11px] text-slate-500 font-mono">
                    Requested Budget: ₹{(apprv.requested_amount || 0).toFixed(2)}
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleDecision(apprv.id, "REJECT")}
                      disabled={actingId === apprv.id}
                      className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-rose-400 hover:text-rose-300 font-semibold rounded transition"
                    >
                      Reject
                    </button>
                    <button
                      onClick={() => handleDecision(apprv.id, "APPROVE")}
                      disabled={actingId === apprv.id}
                      className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-500 disabled:bg-slate-800 text-white font-semibold rounded transition shadow"
                    >
                      {actingId === apprv.id ? "Processing..." : "Approve Plan Execution"}
                    </button>
                  </div>
                </div>
              )}

              {/* Decision Metadata if Decided */}
              {apprv.status !== "PENDING" && (
                <div className="pt-2 border-t border-slate-800 text-[11px] text-slate-500 flex flex-wrap items-center justify-between">
                  <span>
                    Decided by: <strong className="text-slate-300">{apprv.approved_by || "System"}</strong> on{" "}
                    {apprv.approved_at || apprv.created_at}
                  </span>
                  {apprv.rejection_reason && (
                    <span className="text-rose-400 font-medium">Reason: {apprv.rejection_reason}</span>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
