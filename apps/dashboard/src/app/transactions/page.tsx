"use client";

export default function TransactionsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white">Financial Ledger & Guardrails</h1>
        <p className="text-sm text-slate-400">Enforces hard spending limits, reserve requirements, and human sign-offs for all capital outflows.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
          <span className="text-xs text-slate-400 uppercase tracking-wider block">Max Single Transaction</span>
          <span className="text-2xl font-bold font-mono text-emerald-400 mt-1 block">₹1,000.00</span>
          <span className="text-xs text-slate-500 mt-1 block">Amounts exceeding require approval</span>
        </div>
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
          <span className="text-xs text-slate-400 uppercase tracking-wider block">Max Daily Spend</span>
          <span className="text-2xl font-bold font-mono text-indigo-400 mt-1 block">₹500.00</span>
          <span className="text-xs text-slate-500 mt-1 block">Configurable daily allocation</span>
        </div>
        <div className="p-5 rounded-xl bg-slate-900 border border-slate-800">
          <span className="text-xs text-slate-400 uppercase tracking-wider block">Min Target Margin</span>
          <span className="text-2xl font-bold font-mono text-white mt-1 block">20.0%</span>
          <span className="text-xs text-slate-500 mt-1 block">Automated viability threshold</span>
        </div>
      </div>

      <div className="p-8 rounded-xl bg-slate-900 border border-slate-800 text-center text-slate-500">
        <p className="text-sm">No live transactions executed. Financial transactions are locked behind human approval gates in Level 1 autonomy.</p>
      </div>
    </div>
  );
}
