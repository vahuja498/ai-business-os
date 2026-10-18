import React from "react";
import Link from "next/link";

export default function TermsPage() {
  return (
    <div className="max-w-4xl mx-auto py-12 px-4 space-y-8 text-slate-300">
      <div className="space-y-2">
        <Link href="/store" className="text-xs text-indigo-400 hover:text-indigo-300">← Back to Store</Link>
        <h1 className="text-3xl font-extrabold text-white">Terms and Conditions</h1>
        <p className="text-xs text-slate-500">Last updated: October 18, 2026</p>
      </div>

      <div className="space-y-6 text-sm leading-relaxed border-t border-slate-800 pt-6">
        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">1. Introduction</h2>
          <p>
            Welcome to AI Business OS (operated by Vaibhav Ahuja, Faridabad, Haryana). By accessing our website, purchasing our digital products, or using our compliance toolkits, you agree to be bound by these Terms and Conditions.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">2. Nature of Services and Digital Goods</h2>
          <p>
            We provide pre-formulated digital templates, spreadsheet audit trackers, and informational standard operating procedures (SOPs) concerning statutory frameworks like Section 43B(h) of the Income Tax Act, 1961 and the MSMED Act, 2006.
          </p>
          <p>
            <strong>Disclaimer:</strong> The materials provided are for operational compliance and internal audit assistance and do not constitute formal legal counsel or statutory audit certification. Users should review final filings with their appointed Chartered Accountant or Legal Counsel.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">3. Commercial License and Usage Rights</h2>
          <p>
            - <strong>Starter License (Single Firm):</strong> Grants a non-exclusive license to use the compliance templates for one corporate entity or partnership firm.
          </p>
          <p>
            - <strong>CA Multi-Client License:</strong> Grants practicing Chartered Accountants and consultants the right to customize and utilize the templates for their client advisory portfolio.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">4. Payment Terms &amp; Taxes</h2>
          <p>
            All fees are quoted in Indian Rupees (INR). Payments are processed securely via authorized Reserve Bank of India (RBI) regulated payment aggregators (including Razorpay, UPI, credit/debit cards, and netbanking). Applicable Goods and Services Tax (GST) is computed and billed in accordance with Indian tax laws.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">5. Governing Law and Jurisdiction</h2>
          <p>
            These terms shall be governed by and construed in accordance with the laws of India. Any disputes arising out of or in connection with these terms shall be subject to the exclusive jurisdiction of the courts in Faridabad / Delhi-NCR, India.
          </p>
        </section>
      </div>
    </div>
  );
}
