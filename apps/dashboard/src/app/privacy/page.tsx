import React from "react";
import Link from "next/link";

export default function PrivacyPage() {
  return (
    <div className="max-w-4xl mx-auto py-12 px-4 space-y-8 text-slate-300">
      <div className="space-y-2">
        <Link href="/store" className="text-xs text-indigo-400 hover:text-indigo-300">← Back to Store</Link>
        <h1 className="text-3xl font-extrabold text-white">Privacy Policy</h1>
        <p className="text-xs text-slate-500">Last updated: October 18, 2026</p>
      </div>

      <div className="space-y-6 text-sm leading-relaxed border-t border-slate-800 pt-6">
        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">1. Information We Collect</h2>
          <p>
            When you purchase a product or register an inquiry on AI Business OS, we collect:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-slate-400">
            <li>Name and Contact Information (Email address, phone number).</li>
            <li>Company / Firm Name and GSTIN (for tax invoicing).</li>
            <li>Transaction references provided by our payment gateway partners.</li>
          </ul>
          <p>
            <strong>Note:</strong> We do NOT store your credit card numbers, CVVs, or UPI MPINs. All payment processing is handled on 256-bit encrypted servers by PCI-DSS certified payment gateways (Razorpay).
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">2. Purpose of Data Collection</h2>
          <p>We use your personal and business data strictly to:</p>
          <ul className="list-disc pl-5 space-y-1 text-slate-400">
            <li>Deliver your purchased digital products and generate secure download links.</li>
            <li>Issue statutory GST tax invoices and accounting receipts.</li>
            <li>Provide customer support, product updates, and regulatory notices.</li>
          </ul>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">3. Data Protection and Confidentiality</h2>
          <p>
            We implement strict technical and organizational security measures to protect your information against unauthorized access, alteration, or disclosure. We do not sell, rent, or trade your data to third parties.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">4. Compliance with Indian IT Laws</h2>
          <p>
            This Privacy Policy adheres to the Information Technology Act, 2000 and the Digital Personal Data Protection (DPDP) Act, 2023 of India.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">5. Contact Information</h2>
          <p>
            If you have questions regarding this Privacy Policy or wish to request data erasure, contact us at <code>support@ai-business-os.in</code> or visit our <Link href="/contact" className="text-indigo-400 underline">Contact Page</Link>.
          </p>
        </section>
      </div>
    </div>
  );
}
