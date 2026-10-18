import React from "react";
import Link from "next/link";

export default function ContactPage() {
  return (
    <div className="max-w-4xl mx-auto py-12 px-4 space-y-8 text-slate-300">
      <div className="space-y-2">
        <Link href="/store" className="text-xs text-indigo-400 hover:text-indigo-300">← Back to Store</Link>
        <h1 className="text-3xl font-extrabold text-white">Contact Us</h1>
        <p className="text-xs text-slate-500">We are here to assist with compliance inquiries, licensing, and technical support.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 border-t border-slate-800 pt-6">
        <div className="space-y-6 text-sm">
          <div className="space-y-2">
            <h2 className="text-base font-bold text-white">Merchant &amp; Operating Entity</h2>
            <p className="text-slate-200 font-medium">Vaibhav Ahuja (AI Business OS)</p>
          </div>

          <div className="space-y-1">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Registered &amp; Operational Address</h3>
            <p className="text-slate-300">2F/25, Faridabad,</p>
            <p className="text-slate-300">Faridabad, Haryana – 121001, India</p>
          </div>

          <div className="space-y-1">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Email Inquiries</h3>
            <p className="text-slate-300">
              General &amp; Support: <a href="mailto:support@ai-business-os.in" className="text-indigo-400 underline">support@ai-business-os.in</a>
            </p>
            <p className="text-slate-300">
              Billing &amp; Tax: <a href="mailto:vaibhavahuja498@gmail.com" className="text-indigo-400 underline">vaibhavahuja498@gmail.com</a>
            </p>
          </div>

          <div className="space-y-1">
            <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Operating Hours</h3>
            <p className="text-slate-300">Monday to Saturday: 9:30 AM – 6:30 PM IST</p>
            <p className="text-slate-400 text-xs">Digital orders and automated downloads operate 24x7.</p>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
          <h3 className="text-base font-bold text-white">Send Us a Direct Message</h3>
          <form className="space-y-3 text-xs" onSubmit={(e) => { e.preventDefault(); alert("Thank you! Your message has been received."); }}>
            <div>
              <label className="block text-slate-300 mb-1">Your Name</label>
              <input type="text" required placeholder="e.g. Finance Team" className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white" />
            </div>
            <div>
              <label className="block text-slate-300 mb-1">Email Address</label>
              <input type="email" required placeholder="e.g. name@company.com" className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white" />
            </div>
            <div>
              <label className="block text-slate-300 mb-1">Message</label>
              <textarea rows={3} required placeholder="Describe your query..." className="w-full bg-slate-950 border border-slate-800 rounded-lg p-2.5 text-white"></textarea>
            </div>
            <button type="submit" className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2.5 rounded-lg transition">
              Submit Message
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
