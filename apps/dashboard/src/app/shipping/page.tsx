import React from "react";
import Link from "next/link";

export default function ShippingPolicyPage() {
  return (
    <div className="max-w-4xl mx-auto py-12 px-4 space-y-8 text-slate-300">
      <div className="space-y-2">
        <Link href="/store" className="text-xs text-indigo-400 hover:text-indigo-300">← Back to Store</Link>
        <h1 className="text-3xl font-extrabold text-white">Shipping and Delivery Policy</h1>
        <p className="text-xs text-slate-500">Last updated: October 18, 2026</p>
      </div>

      <div className="space-y-6 text-sm leading-relaxed border-t border-slate-800 pt-6">
        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">1. Digital Delivery Model</h2>
          <p>
            AI Business OS offers 100% electronic digital goods, compliance kits, and software templates. We do <strong>NOT</strong> dispatch physical parcels or require courier shipping.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">2. Delivery Timelines</h2>
          <p>
            - <strong>Instant Web Download:</strong> Immediately upon successful payment verification via UPI, Netbanking, or Cards, you are redirected to the order fulfillment page with an instant one-click download button.
          </p>
          <p>
            - <strong>Email Confirmation:</strong> A backup download link and tax invoice receipt are dispatched to your provided email address within 5 to 15 minutes of payment completion.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">3. Shipping Fees</h2>
          <p>
            Since all products are delivered electronically via high-speed cloud networks, <strong>Shipping Charges are ₹0 (Free)</strong> across all product tiers and geographies.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-lg font-bold text-white">4. Assistance with Downloads</h2>
          <p>
            If you encounter any difficulty accessing your download link, please email us with your Order ID or Payment Reference at <code>support@ai-business-os.in</code>, and our technical team will regenerate and re-send your files within 2 to 4 business hours.
          </p>
        </section>
      </div>
    </div>
  );
}
