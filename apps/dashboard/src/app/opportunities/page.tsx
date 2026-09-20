"use client";

import { useEffect, useState } from "react";
import { api, OpportunityItem } from "@/lib/api";

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState<OpportunityItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await api.getOpportunities();
        setOpportunities(res);
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
        <h1 className="text-2xl font-bold tracking-tight text-white">Discovered Opportunities</h1>
        <p className="text-sm text-slate-400">Validated business opportunities synthesized by Research Agent with classified evidence.</p>
      </div>

      {loading ? (
        <p className="text-slate-400 text-sm">Loading opportunities...</p>
      ) : opportunities.length === 0 ? (
        <div className="p-12 text-center rounded-xl bg-slate-900 border border-slate-800 text-slate-500">
          No opportunities found. Assign an objective to the AI CEO to conduct discovery.
        </div>
      ) : (
        <div className="space-y-6">
          {opportunities.map((opp) => (
            <div key={opp.id} className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-3">
                    <h2 className="text-lg font-bold text-white">{opp.title}</h2>
                    <span className="text-xs px-2 py-0.5 rounded font-mono bg-indigo-950 text-indigo-300 border border-indigo-800">
                      Model: {opp.revenue_model}
                    </span>
                  </div>
                  <p className="text-sm text-slate-300 mt-1">{opp.description}</p>
                </div>
                <span
                  className={`text-xs px-2.5 py-1 rounded font-bold ${
                    opp.status === "APPROVED"
                      ? "bg-emerald-950 text-emerald-300 border border-emerald-800"
                      : "bg-amber-950 text-amber-300 border border-amber-800"
                  }`}
                >
                  {opp.status}
                </span>
              </div>

              {/* Economics Grid */}
              <div className="grid grid-cols-2 md:grid-cols-5 gap-3 p-4 bg-slate-950 rounded-lg border border-slate-800 text-xs">
                <div>
                  <span className="text-slate-500 block">Startup Cost</span>
                  <span className="font-mono text-white font-semibold">₹{opp.estimated_startup_cost.toFixed(2)}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Est. CAC</span>
                  <span className="font-mono text-white font-semibold">₹{opp.estimated_acquisition_cost.toFixed(2)}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Customer Value</span>
                  <span className="font-mono text-white font-semibold">₹{opp.estimated_customer_value.toFixed(2)}</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Gross Margin</span>
                  <span className="font-mono text-emerald-400 font-bold">{(opp.estimated_margin * 100).toFixed(0)}%</span>
                </div>
                <div>
                  <span className="text-slate-500 block">Automation Level</span>
                  <span className="font-mono text-indigo-300 font-semibold">{opp.automation_potential}</span>
                </div>
              </div>

              {/* Target & Compliance */}
              <div className="text-xs text-slate-400 flex gap-6">
                <span>Target Market: <strong className="text-slate-200">{opp.target_market}</strong></span>
                <span>Regulatory: <strong className="text-slate-200">{opp.regulatory_complexity}</strong></span>
                <span>Platform Dependency: <strong className="text-slate-200">{opp.platform_dependency}</strong></span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
