"use client";

import React, { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";
import { api, API_BASE } from "@/lib/api";

function SuccessContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const orderId = searchParams.get("order_id");

  const [orderStatus, setOrderStatus] = useState<any>(null);

  useEffect(() => {
    if (orderId) {
      api.getOrderStatus(orderId)
        .then(setOrderStatus)
        .catch((err) => console.error("Failed to fetch order", err));
    }
  }, [orderId]);

  const downloadUrl = token ? `${API_BASE}/public/orders/download?token=${token}` : null;

  return (
    <div className="max-w-3xl mx-auto space-y-8 py-8">
      {/* Success Hero Card */}
      <div className="bg-slate-900 border border-emerald-500/40 rounded-2xl p-8 text-center space-y-4 shadow-2xl relative overflow-hidden">
        <div className="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center text-3xl mx-auto border border-emerald-500/30">
          ✓
        </div>
        <div className="space-y-1">
          <span className="text-xs uppercase tracking-wider font-semibold text-emerald-400">
            Payment Verified &amp; Transaction Settled
          </span>
          <h1 className="text-3xl font-extrabold text-white">Order Fulfilled Successfully!</h1>
          <p className="text-sm text-slate-300 max-w-lg mx-auto">
            Your MSME Section 43B(h) Compliance &amp; Audit Toolkit is unlocked and ready for immediate download.
          </p>
        </div>

        {/* Order Details Pill */}
        <div className="inline-flex flex-wrap items-center justify-center gap-4 bg-slate-950 px-4 py-2 rounded-xl border border-slate-800 text-xs font-mono text-slate-400">
          <span>Order ID: <strong className="text-white">{orderId ? orderId.slice(0, 13) + "..." : "Confirmed"}</strong></span>
          <span>•</span>
          <span>Status: <strong className="text-emerald-400">FULFILLED</strong></span>
          <span>•</span>
          <span>Delivery: <strong className="text-indigo-400">Instant ZIP</strong></span>
        </div>

        {/* Big Download Button */}
        <div className="pt-4">
          {downloadUrl ? (
            <a
              href={downloadUrl}
              download
              className="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-3.5 px-8 rounded-xl shadow-xl shadow-emerald-900/30 transition text-base"
            >
              <span>Download Full Toolkit (.ZIP)</span>
              <span>⬇️</span>
            </a>
          ) : (
            <div className="text-xs text-slate-500">Generating secure download link...</div>
          )}
        </div>
      </div>

      {/* Package Contents Checklist */}
      <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-6 space-y-4">
        <h3 className="text-base font-bold text-white">Included in Your Download Archive:</h3>
        <div className="space-y-2.5 text-xs">
          {[
            {
              name: "01_CFO_Action_Guide_Section_43Bh.md",
              desc: "Complete implementation SOP for CFOs, finance controllers, and practicing CAs.",
            },
            {
              name: "02_Vendor_MSME_Status_Declaration_Form.txt",
              desc: "Bilingual vendor classification request form with Udyam verification clauses.",
            },
            {
              name: "03_Vendor_Written_Agreement_45Day_Addendum.txt",
              desc: "Legal contract addendum establishing 45-day payment cycle under Section 15 of MSMED Act.",
            },
            {
              name: "04_Section_43Bh_Audit_Disallowance_Tracker.csv",
              desc: "Columnar tracker with aging triggers, dispute dispute freeze, and tax add-back formulas.",
            },
            {
              name: "05_Section_16_MSMED_Compound_Interest_Calculator_SOP.md",
              desc: "Standard operating procedure for 3x RBI Bank Rate compounding interest calculations.",
            },
          ].map((item, idx) => (
            <div key={idx} className="p-3 bg-slate-950 rounded-lg border border-slate-800 flex items-start gap-3">
              <span className="text-emerald-400 font-bold">✓</span>
              <div>
                <span className="font-mono text-slate-200 font-medium">{item.name}</span>
                <p className="text-slate-400 mt-0.5">{item.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Navigation Footer */}
      <div className="flex items-center justify-between pt-4 text-xs">
        <Link href="/store" className="text-slate-400 hover:text-white transition">
          ← Return to Storefront
        </Link>
        <Link href="/dashboard" className="text-indigo-400 hover:text-indigo-300 font-medium transition">
          Open AI Business OS Dashboard →
        </Link>
      </div>
    </div>
  );
}

export default function SuccessPage() {
  return (
    <Suspense fallback={<div className="text-center py-12 text-slate-400 text-xs">Loading fulfillment details...</div>}>
      <SuccessContent />
    </Suspense>
  );
}
