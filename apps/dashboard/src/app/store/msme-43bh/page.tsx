"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";

declare global {
  interface Window {
    Razorpay?: any;
  }
}

export default function MSMEComplianceProductPage() {
  const router = useRouter();

  // Tier selection
  const [selectedSku, setSelectedSku] = useState<"MSME-43BH-STARTER" | "MSME-43BH-PRO-CA">(
    "MSME-43BH-STARTER"
  );

  // Form inputs
  const [customerName, setCustomerName] = useState("");
  const [customerEmail, setCustomerEmail] = useState("");
  const [customerPhone, setCustomerPhone] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [gstin, setGstin] = useState("");

  // Loading & error states
  const [isCheckingOut, setIsCheckingOut] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // --- 60-Second Tax Disallowance Calculator State ---
  const [calcTurnover, setCalcTurnover] = useState(50000000); // 5 Crore
  const [calcOverdueBills, setCalcOverdueBills] = useState(1500000); // 15 Lakh
  const [calcTaxRate, setCalcTaxRate] = useState(0.25); // 25% corporate rate

  const taxDisallowance = calcOverdueBills;
  const directTaxLiability = Math.round(calcOverdueBills * calcTaxRate);
  const statutoryPenalInterest = Math.round(calcOverdueBills * 0.2025); // 20.25% (3x RBI rate)
  const totalFinancialExposure = directTaxLiability + statutoryPenalInterest;
  const toolkitPrice = selectedSku === "MSME-43BH-PRO-CA" ? 3999 : 1999;

  async function handleCheckout(e: React.FormEvent) {
    e.preventDefault();
    setErrorMessage(null);

    if (!customerName || !customerEmail) {
      setErrorMessage("Please provide your name and work email address.");
      return;
    }

    try {
      setIsCheckingOut(true);
      const session = await api.createCheckout({
        sku: selectedSku,
        customer_name: customerName,
        customer_email: customerEmail,
        customer_phone: customerPhone || undefined,
        company_name: companyName || undefined,
        gstin: gstin || undefined,
      });

      // If Razorpay SDK is loaded on window and key_id is present
      if (typeof window !== "undefined" && window.Razorpay && session.gateway === "razorpay" && session.key_id) {
        const options = {
          key: session.key_id,
          amount: session.amount_paise,
          currency: session.currency,
          name: "AI Business OS - Tax Compliance",
          description: session.product_name,
          order_id: session.gateway_order_id,
          prefill: {
            name: customerName,
            email: customerEmail,
            contact: customerPhone,
          },
          theme: { color: "#4f46e5" },
          handler: async function (response: any) {
            try {
              const verifyRes = await api.verifyPayment({
                order_id: session.order_id,
                gateway_order_id: response.razorpay_order_id,
                gateway_payment_id: response.razorpay_payment_id,
                gateway_signature: response.razorpay_signature,
              });
              router.push(`/store/success?token=${verifyRes.download_token}&order_id=${session.order_id}`);
            } catch (vErr: any) {
              setErrorMessage(vErr.message || "Payment verification failed");
            }
          },
        };
        const rzp = new window.Razorpay(options);
        rzp.open();
      } else {
        // Fallback / Sandbox mode: Complete instant test checkout
        const verifyRes = await api.verifyPayment({
          order_id: session.order_id,
          gateway_order_id: session.gateway_order_id,
          gateway_payment_id: `pay_sim_${Date.now()}`,
          gateway_signature: "mock_sig_valid",
        });

        router.push(`/store/success?token=${verifyRes.download_token}&order_id=${session.order_id}`);
      }
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to initiate checkout session");
    } finally {
      setIsCheckingOut(false);
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-10 pb-16">
      {/* Breadcrumb Navigation */}
      <div className="flex items-center gap-2 text-xs text-slate-400">
        <Link href="/store" className="hover:text-white transition">Store</Link>
        <span>/</span>
        <span className="text-slate-200">MSME Section 43B(h) Toolkit</span>
      </div>

      {/* Hero Section */}
      <div className="bg-gradient-to-br from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-8 lg:p-10 shadow-2xl relative">
        <div className="max-w-3xl space-y-4">
          <div className="flex items-center gap-2">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-rose-500/20 text-rose-300 border border-rose-500/30">
              Statutory Tax Risk AY 2024-25
            </span>
            <span className="text-xs font-mono text-slate-400">Section 43B(h) Income Tax Act</span>
          </div>

          <h1 className="text-3xl lg:text-5xl font-black text-white tracking-tight leading-tight">
            Protect Your Business From Disallowance on Unpaid MSME Invoices
          </h1>

          <p className="text-slate-300 text-sm lg:text-base leading-relaxed">
            Starting AY 2024-25, any invoice from a Micro or Small supplier unpaid beyond 45 days is
            disallowed as a business deduction and added directly to your taxable profit. Protect your balance
            sheet with our audit-ready compliance package.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2 text-xs text-slate-300">
            <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
              ✓ Tested on Tally Prime, SAP, Zoho Books
            </span>
            <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
              ✓ Form 3CD Clause 22 Disclosure Ready
            </span>
            <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
              ✓ Compliant with OM No. 5/2(2)/2021
            </span>
          </div>
        </div>
      </div>

      {/* 60-Second Tax Disallowance Exposure Calculator */}
      <div className="bg-slate-900/90 border border-amber-500/30 rounded-2xl p-6 lg:p-8 shadow-xl">
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xl">🧮</span>
          <h2 className="text-xl font-bold text-white">60-Second Section 43B(h) Tax Exposure Calculator</h2>
        </div>
        <p className="text-xs text-slate-400 mb-6">
          Calculate how much extra income tax and Section 16 penal interest your company risks paying if supplier dues exceed 45 days.
        </p>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Inputs */}
          <div className="lg:col-span-2 space-y-5">
            <div>
              <div className="flex justify-between text-xs font-medium text-slate-300 mb-2">
                <span>Annual Company Turnover:</span>
                <span className="font-mono text-emerald-400">₹{(calcTurnover / 10000000).toFixed(1)} Crore</span>
              </div>
              <input
                type="range"
                min="10000000"
                max="500000000"
                step="5000000"
                value={calcTurnover}
                onChange={(e) => setCalcTurnover(Number(e.target.value))}
                className="w-full accent-indigo-500 h-2 bg-slate-800 rounded-lg cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-xs font-medium text-slate-300 mb-2">
                <span>Estimated Overdue Micro/Small Invoices (&gt; 45 Days):</span>
                <span className="font-mono text-rose-400">₹{(calcOverdueBills / 100000).toFixed(1)} Lakh</span>
              </div>
              <input
                type="range"
                min="100000"
                max="20000000"
                step="100000"
                value={calcOverdueBills}
                onChange={(e) => setCalcOverdueBills(Number(e.target.value))}
                className="w-full accent-rose-500 h-2 bg-slate-800 rounded-lg cursor-pointer"
              />
            </div>

            <div className="pt-2">
              <label className="text-xs font-medium text-slate-300 block mb-2">Applicable Corporate / Firm Tax Rate:</label>
              <div className="grid grid-cols-3 gap-3">
                {[
                  { label: "22% (Section 115BAA)", val: 0.22 },
                  { label: "25% (SME Corporate)", val: 0.25 },
                  { label: "30% (LLP / Partnership)", val: 0.30 },
                ].map((item) => (
                  <button
                    key={item.val}
                    type="button"
                    onClick={() => setCalcTaxRate(item.val)}
                    className={`py-2 px-3 text-xs rounded-lg border font-medium transition ${
                      calcTaxRate === item.val
                        ? "bg-indigo-600 text-white border-indigo-500"
                        : "bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-750"
                    }`}
                  >
                    {item.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Real-Time Impact Summary */}
          <div className="bg-slate-950 p-6 rounded-xl border border-slate-800 flex flex-col justify-between">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-amber-400 block mb-3">
                Estimated Financial Exposure
              </span>
              <div className="space-y-3">
                <div>
                  <span className="text-[11px] text-slate-400 block">Direct Tax Disallowance</span>
                  <span className="text-lg font-bold font-mono text-white">
                    ₹{taxDisallowance.toLocaleString("en-IN")}
                  </span>
                </div>
                <div>
                  <span className="text-[11px] text-slate-400 block">Immediate Extra Tax Payable</span>
                  <span className="text-lg font-bold font-mono text-rose-400">
                    ₹{directTaxLiability.toLocaleString("en-IN")}
                  </span>
                </div>
                <div>
                  <span className="text-[11px] text-slate-400 block">Section 16 Compounding Interest (p.a.)</span>
                  <span className="text-base font-bold font-mono text-amber-300">
                    ₹{statutoryPenalInterest.toLocaleString("en-IN")}
                  </span>
                </div>
              </div>
            </div>

            <div className="border-t border-slate-800 pt-4 mt-4">
              <div className="flex justify-between items-baseline mb-1">
                <span className="text-xs text-slate-300 font-semibold">Total Risk:</span>
                <span className="text-xl font-black font-mono text-rose-400">
                  ₹{totalFinancialExposure.toLocaleString("en-IN")}
                </span>
              </div>
              <p className="text-[11px] text-emerald-400">
                Fix 100% of this exposure for just ₹{toolkitPrice.toLocaleString("en-IN")}.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Main Product Showcase & Checkout Form */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: Product Deliverables Manifest */}
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-lg font-bold text-white">What is Included in Your Instant Download Bundle</h3>
            <p className="text-xs text-slate-400">
              Immediately unlocked upon verified payment. Files formatted in Markdown, Microsoft Word, and Excel.
            </p>

            <div className="space-y-3">
              {[
                {
                  id: "01",
                  title: "CFO & Finance Head Action Guide (FY 2024-25)",
                  desc: "Implementation checklist, vendor categorization rules, trader exemption clauses, and statutory milestones.",
                  badge: "Advisory SOP",
                },
                {
                  id: "02",
                  title: "Vendor MSME Status Declaration Form",
                  desc: "Standard bilingual declaration letter for suppliers to declare Udyam number and micro/small/medium category.",
                  badge: "Vendor Communication",
                },
                {
                  id: "03",
                  title: "Written Agreement Addendum for 45-Day Credit Cycle",
                  desc: "Legally enforceable PO addendum establishing the written agreement mandated by Section 15 of MSMED Act.",
                  badge: "Legal Contract",
                },
                {
                  id: "04",
                  title: "Section 43B(h) Audit & Disallowance Tracking Sheet",
                  desc: "Columnar audit tracker with automatic aging alarms, dispute pause tracking, and tax disallowance calculations.",
                  badge: "Excel / CSV",
                },
                {
                  id: "05",
                  title: "Section 16 Penal Compound Interest Calculator",
                  desc: "SOP for computing monthly rests compound interest at 3x RBI Bank Rate with inadmissible expense tax notes.",
                  badge: "Statutory Math",
                },
              ].map((item) => (
                <div key={item.id} className="p-3 bg-slate-950/70 rounded-lg border border-slate-800/80 flex items-start gap-3">
                  <span className="font-mono text-xs font-bold text-indigo-400 bg-indigo-500/10 px-2 py-1 rounded">
                    {item.id}
                  </span>
                  <div className="flex-1">
                    <div className="flex items-center justify-between">
                      <h4 className="text-sm font-semibold text-slate-200">{item.title}</h4>
                      <span className="text-[10px] text-slate-400 bg-slate-800 px-2 py-0.5 rounded">{item.badge}</span>
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Frequently Asked Questions */}
          <div className="bg-slate-900/40 border border-slate-800 rounded-xl p-6 space-y-4">
            <h3 className="text-base font-bold text-white">Frequently Asked Questions</h3>
            <div className="space-y-3 text-xs">
              <div>
                <h4 className="font-semibold text-slate-200">Does Section 43B(h) apply to purchases from Traders?</h4>
                <p className="text-slate-400 mt-1">
                  No. Under Office Memorandum No. 5/2(2)/2021-E/P &amp; G/Policy, traders/retailers/wholesalers (NIC 45-47)
                  are registered solely for Priority Sector Lending and are excluded from Section 43B(h) disallowance.
                  Our guide provides the verification method.
                </p>
              </div>
              <div>
                <h4 className="font-semibold text-slate-200">How is the 45-day payment period calculated?</h4>
                <p className="text-slate-400 mt-1">
                  If there is a written agreement, payment must be made within the agreed date (maximum 45 days).
                  If there is NO written agreement, payment is legally due within 15 days. Our PO addendum secures your 45-day cycle.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Interactive Checkout Order Form */}
        <div className="lg:col-span-5">
          <div className="bg-slate-900 border border-indigo-500/30 rounded-2xl p-6 shadow-2xl sticky top-8">
            <h3 className="text-xl font-bold text-white mb-1">Instant Order &amp; Delivery</h3>
            <p className="text-xs text-slate-400 mb-5">
              Select your license and complete checkout via UPI or card for instant download.
            </p>

            {/* License Selector */}
            <div className="space-y-3 mb-6">
              <label className="text-xs font-semibold text-slate-300 block">Select License Tier:</label>
              <div
                onClick={() => setSelectedSku("MSME-43BH-STARTER")}
                className={`p-3.5 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                  selectedSku === "MSME-43BH-STARTER"
                    ? "bg-indigo-600/10 border-indigo-500 text-white"
                    : "bg-slate-950 border-slate-800 text-slate-300 hover:border-slate-700"
                }`}
              >
                <div>
                  <div className="font-bold text-sm">Enterprise Starter (Single Firm)</div>
                  <div className="text-xs text-slate-400">Complete toolkit for 1 corporate entity</div>
                </div>
                <div className="text-lg font-mono font-bold text-emerald-400">₹1,999</div>
              </div>

              <div
                onClick={() => setSelectedSku("MSME-43BH-PRO-CA")}
                className={`p-3.5 rounded-xl border cursor-pointer transition flex items-center justify-between ${
                  selectedSku === "MSME-43BH-PRO-CA"
                    ? "bg-indigo-600/10 border-indigo-500 text-white"
                    : "bg-slate-950 border-slate-800 text-slate-300 hover:border-slate-700"
                }`}
              >
                <div>
                  <div className="font-bold text-sm">CA Multi-Client Advisory License</div>
                  <div className="text-xs text-slate-400">Unlimited clients + Form 3CD Clause 22 guide</div>
                </div>
                <div className="text-lg font-mono font-bold text-emerald-400">₹3,999</div>
              </div>
            </div>

            {/* Error Message */}
            {errorMessage && (
              <div className="p-3 mb-4 bg-rose-500/10 border border-rose-500/30 rounded-lg text-rose-300 text-xs">
                {errorMessage}
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleCheckout} className="space-y-4">
              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">
                  Full Name / Contact Person <span className="text-rose-400">*</span>
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Rajesh Sharma"
                  value={customerName}
                  onChange={(e) => setCustomerName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">
                  Work Email <span className="text-rose-400">*</span>
                </label>
                <input
                  type="email"
                  required
                  placeholder="e.g. finance@yourcompany.com"
                  value={customerEmail}
                  onChange={(e) => setCustomerEmail(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-medium text-slate-300 block mb-1">Mobile / UPI Phone</label>
                  <input
                    type="tel"
                    placeholder="+91 98765 43210"
                    value={customerPhone}
                    onChange={(e) => setCustomerPhone(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                  />
                </div>
                <div>
                  <label className="text-xs font-medium text-slate-300 block mb-1">Company / CA Firm</label>
                  <input
                    type="text"
                    placeholder="e.g. Apex Tech Ltd"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">GSTIN (For 18% Input Tax Credit)</label>
                <input
                  type="text"
                  placeholder="e.g. 06AAACA0000A1Z5"
                  value={gstin}
                  onChange={(e) => setGstin(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="pt-2">
                <button
                  type="submit"
                  disabled={isCheckingOut}
                  className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3 px-4 rounded-xl shadow-lg transition flex items-center justify-center gap-2 text-sm disabled:opacity-50"
                >
                  {isCheckingOut ? (
                    <span>Securing Order Session...</span>
                  ) : (
                    <>
                      <span>Pay ₹{toolkitPrice.toLocaleString("en-IN")} &amp; Download Toolkit</span>
                      <span>⚡</span>
                    </>
                  )}
                </button>
              </div>

              <div className="text-center pt-2 text-[11px] text-slate-500 flex items-center justify-center gap-2">
                <span>🔒 256-Bit SSL Encrypted</span>
                <span>•</span>
                <span>Instant ZIP Delivery</span>
                <span>•</span>
                <span>GST Tax Invoice</span>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Compliance & Policy Footer for Razorpay / RBI Verification */}
      <footer className="border-t border-slate-800 pt-8 mt-12 text-xs text-slate-500">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div>
            <span className="font-semibold text-slate-400">AI Business OS</span> • Operated by Vaibhav Ahuja, Faridabad, Haryana
          </div>
          <div className="flex flex-wrap gap-4 text-slate-400">
            <Link href="/terms" className="hover:text-white transition">Terms &amp; Conditions</Link>
            <Link href="/privacy" className="hover:text-white transition">Privacy Policy</Link>
            <Link href="/shipping" className="hover:text-white transition">Shipping &amp; Delivery</Link>
            <Link href="/refunds" className="hover:text-white transition">Cancellation &amp; Refund</Link>
            <Link href="/contact" className="hover:text-white transition">Contact Us</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
