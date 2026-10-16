import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Business OS - Control Dashboard",
  description: "Autonomous Business Operating System Control Center",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="flex h-screen bg-slate-950 text-slate-100 antialiased">
        {/* Sidebar */}
        <aside className="w-64 border-r border-slate-800 bg-slate-900/50 flex flex-col justify-between p-4">
          <div>
            <div className="flex items-center gap-2 px-2 py-4 mb-4 border-b border-slate-800">
              <div className="h-8 w-8 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-white shadow-lg">
                OS
              </div>
              <div>
                <h1 className="font-semibold text-sm tracking-wide text-white">AI BUSINESS OS</h1>
                <p className="text-xs text-slate-400">Autonomous Core v1</p>
              </div>
            </div>

            <nav className="space-y-1 text-sm font-medium">
              <Link href="/dashboard" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Dashboard</span>
              </Link>
              <Link href="/store" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Storefront</span>
                <span className="ml-auto text-xs bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full border border-emerald-500/30">Live</span>
              </Link>
              <Link href="/approvals" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Approvals</span>
                <span className="ml-auto text-xs bg-amber-500/20 text-amber-300 px-2 py-0.5 rounded-full border border-amber-500/30">Gate</span>
              </Link>
              <Link href="/businesses" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Businesses</span>
              </Link>
              <Link href="/opportunities" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Opportunities</span>
              </Link>
              <Link href="/validation" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Validation Engine</span>
                <span className="ml-auto text-xs bg-indigo-500/20 text-indigo-300 px-2 py-0.5 rounded-full border border-indigo-500/30">Phase 5</span>
              </Link>
              <Link href="/agents" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Agents</span>
              </Link>
              <Link href="/tasks" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Tasks</span>
              </Link>
              <Link href="/transactions" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Transactions</span>
              </Link>
              <Link href="/audit" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Audit Trail</span>
              </Link>
              <Link href="/settings" className="flex items-center gap-3 px-3 py-2 rounded-md hover:bg-slate-800 text-slate-300 hover:text-white transition">
                <span>Settings</span>
              </Link>
            </nav>
          </div>

          <div className="p-3 bg-slate-900 rounded-lg border border-slate-800 text-xs">
            <div className="flex items-center justify-between text-slate-400 mb-1">
              <span>Security Status</span>
              <span className="text-emerald-400 font-mono font-semibold">ENFORCED</span>
            </div>
            <p className="text-slate-500 text-[11px]">Human approval & financial guardrails active</p>
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto bg-slate-950 p-8">
          {children}
        </main>
      </body>
    </html>
  );
}
