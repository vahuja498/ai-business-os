"use client";

import { useEffect, useState } from "react";
import { api, AuditItem } from "@/lib/api";

export default function AuditPage() {
  const [logs, setLogs] = useState<AuditItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await api.getAuditLogs();
        setLogs(res);
      } catch (err: any) {
        alert(`Error: ${err.message}`);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Append-Only Audit Trail</h1>
        <p className="text-sm text-slate-400">Cryptographically verifiable log of every agent action, tool invocation, and human approval decision.</p>
      </div>

      {loading ? (
        <p className="text-slate-400 text-sm">Loading audit events...</p>
      ) : logs.length === 0 ? (
        <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-500">
          No audit logs recorded yet.
        </div>
      ) : (
        <div className="space-y-2">
          {logs.map((log) => (
            <div key={log.id} className="p-4 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between text-xs">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-indigo-400">{log.actor}</span>
                  <span className="text-slate-500">&rarr;</span>
                  <span className="font-mono text-white">{log.action}</span>
                  {log.target && <span className="text-slate-400">({log.target})</span>}
                </div>
                {log.metadata && Object.keys(log.metadata).length > 0 && (
                  <p className="text-slate-500 font-mono text-[11px] truncate max-w-2xl">
                    {JSON.stringify(log.metadata)}
                  </p>
                )}
              </div>
              <div className="text-right">
                <span className={`px-2 py-0.5 rounded font-mono font-bold ${
                  log.result === "APPROVED" || log.result === "SUCCESS"
                    ? "text-emerald-400 bg-emerald-950/60 border border-emerald-800/40"
                    : log.result === "REJECTED"
                    ? "text-red-400 bg-red-950/60 border border-red-800/40"
                    : "text-amber-400 bg-amber-950/60 border border-amber-800/40"
                }`}>
                  {log.result}
                </span>
                <p className="text-slate-500 text-[10px] mt-1">{new Date(log.created_at).toLocaleString()}</p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
