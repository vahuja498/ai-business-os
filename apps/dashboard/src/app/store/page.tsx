"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api, ProductCatalog } from "@/lib/api";

export default function StorefrontCatalogPage() {
  const [catalog, setCatalog] = useState<ProductCatalog | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadCatalog() {
      try {
        const data = await api.getProducts();
        setCatalog(data);
      } catch (err) {
        console.error("Failed to load product catalog", err);
      } finally {
        setLoading(false);
      }
    }
    loadCatalog();
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-8 pb-12">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-emerald-950 via-slate-900 to-indigo-950 border border-emerald-500/30 rounded-2xl p-8 relative overflow-hidden shadow-2xl">
        <div className="max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            <span>🇮🇳</span>
            <span>Commercial Storefront • India Live Rails</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight">
            Indian Statutory Compliance &amp; Digital B2B Toolkits
          </h1>
          <p className="text-slate-300 text-sm md:text-base leading-relaxed">
            Audit-ready legal templates, tax disallowance trackers, and standard operating procedures
            engineered for Indian SMEs, CFOs, and Chartered Accountants.
          </p>
          <div className="flex flex-wrap gap-4 pt-2 text-xs text-slate-300 font-medium">
            <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
              ⚡ Instant Digital ZIP Delivery
            </span>
            <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
              💳 UPI &amp; Cards via Razorpay
            </span>
            <span className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
              🧾 Automated GST Tax Invoices
            </span>
          </div>
        </div>
      </div>

      {/* Featured Business Products */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white">Active Product Modules</h2>
            <p className="text-xs text-slate-400">Validated high-margin solutions deployed for immediate revenue generation.</p>
          </div>
          <span className="text-xs font-mono bg-indigo-500/10 text-indigo-400 px-3 py-1 rounded border border-indigo-500/20">
            Candidate #19: Digital Products
          </span>
        </div>

        {/* Featured Card */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 hover:border-slate-700 transition shadow-lg">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
            <div className="space-y-3 max-w-2xl">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">
                  Statutory Mandate AY 2024-25
                </span>
                <span className="text-xs text-slate-400">Income Tax Act Section 43B(h)</span>
              </div>
              <h3 className="text-2xl font-bold text-white">
                MSME Section 43B(h) 45-Day Payment Compliance &amp; Audit Toolkit
              </h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Prevent 100% tax disallowance on overdue vendor bills. Includes the official Vendor Udyam
                Declaration Form, legal 45-day PO Addendum, Tally/SAP columnar disallowance tracking worksheet,
                and Section 16 penal compound interest calculator.
              </p>
              <div className="flex flex-wrap gap-2 pt-1 text-xs">
                <span className="bg-slate-800 text-slate-300 px-2.5 py-1 rounded">5 Core Legal &amp; Audit Templates</span>
                <span className="bg-slate-800 text-slate-300 px-2.5 py-1 rounded">Pre-filled with Indian Legal Precedents</span>
                <span className="bg-slate-800 text-slate-300 px-2.5 py-1 rounded">3x RBI Rate SOP</span>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row lg:flex-col gap-3 min-w-[240px]">
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 text-center">
                <span className="text-xs text-slate-400 block mb-1">Starting from</span>
                <div className="text-3xl font-extrabold text-emerald-400 font-mono">₹1,999</div>
                <span className="text-[11px] text-slate-500 block mt-0.5">One-time purchase • Zero recurring fees</span>
              </div>
              <Link
                href="/store/msme-43bh"
                className="w-full text-center bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-3 px-4 rounded-lg shadow-lg hover:shadow-indigo-500/20 transition text-sm flex items-center justify-center gap-2"
              >
                <span>View Product &amp; Calculator</span>
                <span>→</span>
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Pricing Slabs Quick View */}
      {catalog && catalog.tiers && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
          {catalog.tiers.map((tier) => (
            <div
              key={tier.sku}
              className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 flex flex-col justify-between"
            >
              <div className="space-y-4">
                <div className="flex justify-between items-start">
                  <div>
                    <span className="text-xs font-mono text-indigo-400">{tier.sku}</span>
                    <h4 className="text-lg font-bold text-white mt-1">{tier.name}</h4>
                  </div>
                  <div className="text-right">
                    <span className="text-2xl font-extrabold font-mono text-emerald-400">
                      ₹{tier.price_inr.toLocaleString("en-IN")}
                    </span>
                  </div>
                </div>
                <p className="text-xs text-slate-400">{tier.description}</p>
                <div className="border-t border-slate-800 pt-3">
                  <span className="text-xs font-semibold text-slate-300 block mb-2">Included Deliverables:</span>
                  <ul className="space-y-1.5 text-xs text-slate-400">
                    {tier.deliverables.map((d, i) => (
                      <li key={i} className="flex items-start gap-2">
                        <span className="text-emerald-400">✓</span>
                        <span>{d}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
              <div className="pt-6">
                <Link
                  href={`/store/msme-43bh?sku=${tier.sku}`}
                  className="block w-full text-center py-2.5 px-4 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-medium text-xs border border-slate-700 transition"
                >
                  Configure &amp; Purchase
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

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
