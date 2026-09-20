"use client";

export default function SettingsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">System Settings & Governance</h1>
        <p className="text-sm text-slate-400">Configure runtime autonomy levels, safety thresholds, and financial limits.</p>
      </div>

      <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
        <h2 className="text-base font-semibold text-white">Autonomy Hierarchy (Section 12)</h2>
        <div className="space-y-3">
          {[
            { level: "LEVEL_0_OBSERVE", desc: "Pure observation and read-only telemetry. No actions or executions permitted." },
            { level: "LEVEL_1_ASSIST (Active)", desc: "Default mode. Autonomous research, analysis, and draft proposals. Sensitive actions require explicit human sign-off." },
            { level: "LEVEL_2_CONTROLLED_AUTONOMY", desc: "Routine operations execute within pre-authorized budget caps. Escalates on failure or policy deviations." },
            { level: "LEVEL_3_HIGH_AUTONOMY", desc: "Fully automated operational execution with real-time risk supervision." },
          ].map((item) => (
            <div key={item.level} className="p-4 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
              <div>
                <p className="font-mono text-sm text-indigo-400 font-semibold">{item.level}</p>
                <p className="text-xs text-slate-400 mt-0.5">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="p-6 rounded-xl bg-slate-900 border border-slate-800 space-y-4">
        <h2 className="text-base font-semibold text-white">Prohibited Operations (Section 28)</h2>
        <div className="p-4 rounded-lg bg-red-950/20 border border-red-900/40 text-xs text-red-300 space-y-1">
          <p className="font-semibold text-red-200">Strictly Blocked by Autonomous Core:</p>
          <ul className="list-disc pl-4 space-y-0.5 text-slate-400">
            <li>Creation or usage of fake accounts, fake identities, or fabricated documents</li>
            <li>Deceptive customer acquisition or falsified advertising claims</li>
            <li>Manipulation of government benefit or subsidy schemes</li>
            <li>Refund abuse or artificial reward loops</li>
            <li>Bypassing platform or security controls</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
