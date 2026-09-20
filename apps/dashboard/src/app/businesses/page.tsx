"use client";

import { useEffect, useState } from "react";
import { api, BusinessItem } from "@/lib/api";

export default function BusinessesPage() {
  const [businesses, setBusinesses] = useState<BusinessItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [moduleName, setModuleName] = useState("solar_leads");
  const [objectiveInput, setObjectiveInput] = useState<{ [id: string]: string }>({});
  const [runningObjective, setRunningObjective] = useState<string | null>(null);

  const loadBusinesses = async () => {
    try {
      setLoading(true);
      const res = await api.getBusinesses();
      setBusinesses(res);
    } catch (err: any) {
      alert(`Error loading businesses: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBusinesses();
  }, []);

  const handleCreateBusiness = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    try {
      await api.createBusiness({ name, description, module_name: moduleName });
      setName("");
      setDescription("");
      loadBusinesses();
    } catch (err: any) {
      alert(`Error creating business: ${err.message}`);
    }
  };

  const handleExecuteObjective = async (businessId: string) => {
    const objective = objectiveInput[businessId] || "Investigate rooftop solar lead generation in urban centers";
    try {
      setRunningObjective(businessId);
      const res = await api.executeObjective(businessId, objective);
      alert(`Objective executed! Result status: ${res.status}. Check Approvals and Opportunities.`);
      loadBusinesses();
    } catch (err: any) {
      alert(`Execution failed: ${err.message}`);
    } finally {
      setRunningObjective(null);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Business Modules</h1>
        <p className="text-sm text-slate-400">Manage autonomous business entities and dispatch objectives to the AI CEO.</p>
      </div>

      {/* Register Business Form */}
      <div className="p-6 rounded-xl bg-slate-900 border border-slate-800">
        <h2 className="text-base font-semibold text-white mb-4">Register New Business</h2>
        <form onSubmit={handleCreateBusiness} className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Business Name (e.g. Solar Leads Express)"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-md text-sm text-white focus:outline-none focus:border-indigo-500"
            required
          />
          <input
            type="text"
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-md text-sm text-white focus:outline-none focus:border-indigo-500"
          />
          <select
            value={moduleName}
            onChange={(e) => setModuleName(e.target.value)}
            className="px-3 py-2 bg-slate-950 border border-slate-800 rounded-md text-sm text-white focus:outline-none focus:border-indigo-500"
          >
            <option value="solar_leads">solar_leads (Draft)</option>
            <option value="core">core (Generic)</option>
          </select>
          <button
            type="submit"
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 font-medium text-sm text-white rounded-md transition shadow"
          >
            Create Business
          </button>
        </form>
      </div>

      {/* Business List */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-white">Configured Businesses</h2>
        {loading ? (
          <p className="text-slate-400 text-sm">Loading businesses...</p>
        ) : businesses.length === 0 ? (
          <p className="text-slate-500 text-sm p-6 bg-slate-900 border border-slate-800 rounded-xl">
            No businesses registered yet. Create your first business above.
          </p>
        ) : (
          businesses.map((biz) => (
            <div key={biz.id} className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-3">
                    <h3 className="text-lg font-bold text-white">{biz.name}</h3>
                    <span className="text-xs px-2 py-0.5 rounded font-mono bg-slate-800 text-indigo-300">
                      Module: {biz.module_name}
                    </span>
                    <span className="text-xs px-2 py-0.5 rounded font-mono bg-amber-950 text-amber-300 border border-amber-800">
                      {biz.status}
                    </span>
                  </div>
                  <p className="text-sm text-slate-400 mt-1">{biz.description || "No description provided."}</p>
                </div>
              </div>

              {/* CEO Objective Trigger */}
              <div className="pt-3 border-t border-slate-800 flex items-center gap-3">
                <input
                  type="text"
                  placeholder="Enter strategic objective for AI CEO (e.g. Research rooftop solar viability)"
                  value={objectiveInput[biz.id] || ""}
                  onChange={(e) => setObjectiveInput({ ...objectiveInput, [biz.id]: e.target.value })}
                  className="flex-1 px-3 py-2 bg-slate-950 border border-slate-800 rounded-md text-xs text-white focus:outline-none focus:border-indigo-500"
                />
                <button
                  onClick={() => handleExecuteObjective(biz.id)}
                  disabled={runningObjective === biz.id}
                  className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 text-xs font-semibold text-white rounded-md transition shadow"
                >
                  {runningObjective === biz.id ? "CEO Processing..." : "Dispatch to AI CEO"}
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
