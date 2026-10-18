import React from "react";
import Link from "next/link";

export default function RefundPolicyPage() {
  return (
    <div className="max-w-4xl mx-auto py-12 px-4 space-y-8 text-slate-300">
      <div className="space-y-2">
        <Link href="/store" className="text-xs text-indigo-400 hover:text-indigo-300">← Back to Store</Link>
        <h1 className="text-3xl font-extrabold text-white">Cancellation and Refund Policy</h1>
        <p className="text-xs text-slate-500">Last updated: October 18, 2026</p>
      </div>

      <div className="space-y-6 text-sm leading-relaxed border-t border-slate-800 pt-6">
        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">1. Cancellation Policy</h2>
          <p>
            Because our compliance toolkits and software files are delivered digitally and unlocked immediately upon transaction confirmation, orders cannot be cancelled once digital download access has been granted.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">2. 7-Day Refund Policy &amp; Guarantee</h2>
          <p>
            We stand behind the quality and statutory accuracy of our compliance assets. You are eligible for a 100% full refund under the following conditions:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-slate-400">
            <li><strong>Technical Defect:</strong> The downloaded file is corrupted or cannot be opened, and our support team is unable to provide a functional replacement within 24 hours.</li>
            <li><strong>Double Billing / Duplicate Payment:</strong> In the event of a network glitch where your account was debited multiple times for a single order.</li>
            <li><strong>Non-Delivery:</strong> If payment was debited but no download link was made available and no confirmation email was received.</li>
          </ul>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">3. How to Request a Refund</h2>
          <p>
            To initiate a refund request, please email <code>support@ai-business-os.in</code> within <strong>7 days of purchase</strong> with:
          </p>
          <ul className="list-disc pl-5 space-y-1 text-slate-400">
            <li>Your Order ID or Transaction Reference ID (from Razorpay / Bank SMS).</li>
            <li>The email address used during checkout.</li>
            <li>A brief description of the issue encountered.</li>
          </ul>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">4. Refund Settlement Timelines</h2>
          <p>
            Once approved, refunds are credited back to the original source of payment (original bank account, UPI VPA, or credit/debit card) within <strong>5 to 7 working days</strong> in accordance with RBI and banking network guidelines.
          </p>
        </section>
      </div>
    </div>
  );
}
