"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function AgentsPage() {
  const [agents, setAgents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await api.getAgents();
        setAgents(res);
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
        <h1 className="text-2xl font-bold tracking-tight text-white">Autonomous Agents</h1>
        <p className="text-sm text-slate-400">Specialist agents operating under strict autonomy levels and tool permission boundaries.</p>
      </div>

      {loading ? (
        <p className="text-slate-400 text-sm">Loading agents...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {agents.map((ag) => (
            <div key={ag.id || ag.name} className="p-5 rounded-xl bg-slate-900 border border-slate-800 space-y-3">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-base font-bold text-white">{ag.name}</h3>
                  <p className="text-xs text-slate-400 mt-0.5">{ag.description}</p>
                </div>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800">
                  {ag.status || "ACTIVE"}
                </span>
              </div>

              <div className="text-xs space-y-1 pt-2 border-t border-slate-800">
                <p className="text-slate-400">
                  Allowed Tools: <span className="font-mono text-indigo-300">{(ag.allowed_tools || []).join(", ") || "none"}</span>
                </p>
                <p className="text-slate-400">
                  Risk Tier: <span className="font-mono text-slate-300">{ag.risk_level || "LOW"}</span> | Mode: <span className="font-mono text-slate-300">{ag.execution_mode || "AUTONOMOUS"}</span>
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
