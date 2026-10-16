import io
import zipfile
from typing import Any


class MSMEToolkitGenerator:
    """
    Generates customized, audit-ready compliance assets for Section 43B(h)
    of the Income Tax Act, 1961.
    """

    @classmethod
    def get_template_manifest(cls) -> list[dict[str, str]]:
        return [
            {
                "file_name": "01_CFO_Action_Guide_Section_43Bh.md",
                "title": "CFO & Finance Head Action Guide: Section 43B(h) Compliance",
                "format": "Markdown / Document",
                "category": "Advisory",
            },
            {
                "file_name": "02_Vendor_MSME_Status_Declaration_Form.txt",
                "title": "Vendor Udyam Registration & Category Declaration Form",
                "format": "Text / Word Template",
                "category": "Vendor Communication",
            },
            {
                "file_name": "03_Vendor_Written_Agreement_45Day_Addendum.txt",
                "title": "Purchase Order Addendum for 45-Day Payment Term (Section 15 MSMED Act)",
                "format": "Legal Addendum",
                "category": "Contracts",
            },
            {
                "file_name": "04_Section_43Bh_Audit_Disallowance_Tracker.csv",
                "title": "Section 43B(h) Disallowance & Audit Tracker Worksheet",
                "format": "CSV / Excel Template",
                "category": "Accounting & Audit",
            },
            {
                "file_name": "05_Section_16_MSMED_Compound_Interest_Calculator_SOP.md",
                "title": "SOP for Section 16 Penal Interest Calculation (3x RBI Bank Rate)",
                "format": "Markdown / SOP",
                "category": "Statutory Calculation",
            },
        ]

    @classmethod
    def get_document_content(cls, file_name: str, company_name: str = "Enterprise Buyer") -> str:
        if file_name == "01_CFO_Action_Guide_Section_43Bh.md":
            return f"""# SECTION 43B(h) EXECUTIVE ACTION GUIDE FOR {company_name.upper()}
## Compliance Mandate under the Finance Act, 2023 & MSMED Act, 2006

### 1. Executive Summary
Section 43B(h) of the Income Tax Act, 1961 disallows business deductions for any sum payable to a Micro or Small enterprise if not paid within the time limit specified under Section 15 of the Micro, Small and Medium Enterprises Development (MSMED) Act, 2006.

### 2. Time Limits for Payment (Section 15 MSMED Act)
- **With Written Agreement:** Maximum 45 calendar days from date of acceptance or deemed acceptance.
- **Without Written Agreement:** Maximum 15 calendar days from delivery of goods/services.
- **Objection Clause:** If buyer raises an objection in writing within 15 days of delivery, day-count begins when objection is resolved.

### 3. Applicable Entities
- **Covered Suppliers:** MICRO and SMALL enterprises registered with valid Udyam Registration.
- **Exempted Suppliers:**
  - Medium enterprises (Investment > ₹10 Cr or Turnover > ₹50 Cr).
  - Traders / Wholesalers / Retailers (NIC Codes 45, 46, 47) as per OM No. 5/2(2)/2021-E/P & G/Policy dated 02/07/2021.
  - Suppliers without valid Udyam certificate.
  - Purchases made before suppliers obtain Udyam.

### 4. Consequences of Non-Compliance
1. **Income Tax Disallowance:** Entire unpaid invoice value is added back to taxable business profits for the Assessment Year. (Deduction allowed only in subsequent FY when payment is actually released).
2. **Compound Penal Interest:** Buyer liable to pay compound interest with monthly rests at THREE TIMES the RBI Bank Rate from appointed day under Section 16 of MSMED Act.
3. **Interest Inadmissible:** Interest paid to MSME under Section 16 cannot be claimed as tax-deductible expense under Section 23 of MSMED Act.

### 5. Standard Operating Procedure (SOP)
1. Dispatch Vendor MSME Declaration Form to 100% active suppliers.
2. Verify Udyam Registration Numbers on the official MSME Udyam Portal.
3. Execute the 45-Day Payment Term Written Agreement Addendum on all purchase orders.
4. Flag MSME invoices in ERP (Tally / SAP / Zoho Books) with strict 45-day payment aging alarms.
5. Settle all outstanding FY payments to Micro and Small vendors on or before March 31.
"""

        elif file_name == "02_Vendor_MSME_Status_Declaration_Form.txt":
            return f"""ANNUAL VENDOR MSME STATUS DECLARATION FORM
(To be executed on Vendor's Letterhead)

To:
Finance & Accounts Department
{company_name}

Subject: Declaration of Enterprise Category under MSMED Act, 2006 & Section 43B(h) of Income Tax Act

Dear Sir/Madam,

We hereby declare our enterprise status as under the Micro, Small and Medium Enterprises Development Act, 2006:

1. Vendor Legal Name: _____________________________________________
2. PAN Number: ____________________________________________________
3. GSTIN: _________________________________________________________
4. Registered with Udyam? [ ] YES  [ ] NO
5. Udyam Registration Certificate Number: _________________________
6. Enterprise Classification:
   [ ] MICRO Enterprise (Investment <= 1 Cr AND Turnover <= 5 Cr)
   [ ] SMALL Enterprise (Investment <= 10 Cr AND Turnover <= 50 Cr)
   [ ] MEDIUM Enterprise (Investment <= 50 Cr AND Turnover <= 250 Cr)
   [ ] NOT APPLICABLE / LARGE
7. Major Activity Registered:
   [ ] Manufacturing
   [ ] Service
   [ ] Trading / Retail (Note: Retail/Wholesale traders are excluded from Section 43B(h))

We enclose herewith a self-attested copy of our valid Udyam Registration Certificate.
We undertake to notify {company_name} immediately in writing in the event of any change in our enterprise classification or cancellation of Udyam registration.

Authorized Signatory Name: ________________________________________
Designation: _____________________________________________________
Date: ________________________
Official Stamp / Seal:
"""

        elif file_name == "03_Vendor_Written_Agreement_45Day_Addendum.txt":
            return f"""ADDENDUM TO PURCHASE ORDER / MASTER SUPPLY AGREEMENT
REGARDING CREDIT TERMS PURSUANT TO SECTION 15 OF MSMED ACT, 2006

This Addendum is entered between:
{company_name} (hereinafter referred to as the "Buyer")
AND
The Supplier / Vendor identified in the Purchase Order (hereinafter referred to as the "Supplier").

WHEREAS:
Under Section 15 of the Micro, Small and Medium Enterprises Development Act, 2006, parties may agree in writing upon a credit period not exceeding forty-five (45) days.

IT IS HEREBY AGREED AS FOLLOWS:
1. Agreed Payment Period:
Buyer and Supplier explicitly agree in writing that the credit period for all invoices raised by the Supplier shall be forty-five (45) calendar days from the date of physical receipt and verification of goods/services ("Date of Acceptance").

2. Inspection & Dispute Notice:
Buyer shall have fifteen (15) calendar days from delivery to inspect supplies and notify any defects, discrepancies, or quality issues in writing. In case of an objection, the 45-day cycle shall begin only once the dispute is formally resolved.

3. Statutory Compliance:
This agreement is executed to satisfy the statutory requirements of Section 15 of the MSMED Act, 2006 and Section 43B(h) of the Income Tax Act, 1961.

For {company_name}                                For Supplier
Authorized Signatory                              Authorized Signatory
"""

        elif file_name == "04_Section_43Bh_Audit_Disallowance_Tracker.csv":
            return """Invoice_No,Invoice_Date,Vendor_Name,PAN,GSTIN,Udyam_No,Enterprise_Type,Is_Trading_Only,Goods_Receipt_Date,Dispute_Raised_Date,Dispute_Resolved_Date,Agreed_Days,Due_Date,Payment_Date,Invoice_Amount_INR,Paid_On_Time,Section_43Bh_Disallowance_INR,Section_16_Penal_Interest_INR,Audit_Notes
INV-2024-001,2024-04-10,Alpha Precision Dies,AAACA1234F,07AAACA1234F1Z1,UDYAM-HR-03-0012345,MICRO,No,2024-04-12,,,45,2024-05-27,2024-05-20,185000.00,YES,0.00,0.00,Compliant - Paid within 45 days
INV-2024-002,2024-05-02,Beta Polymer Packers,BBBBP5678K,06BBBBP5678K1Z5,UDYAM-HR-02-0056789,SMALL,No,2024-05-03,,,45,2024-06-17,2024-07-05,420000.00,NO,0.00,4325.00,Paid in same FY but late; Penal interest applies
INV-2024-003,2025-02-14,Gamma CNC Tech,CCCCG9012M,06CCCCG9012M1Z8,UDYAM-HR-04-0090123,MICRO,No,2025-02-15,,,45,2025-03-31,,275000.00,NO,275000.00,1850.00,DISALLOWED: Unpaid as on March 31; Tax add-back triggered
"""

        elif file_name == "05_Section_16_MSMED_Compound_Interest_Calculator_SOP.md":
            return f"""# SECTION 16 MSMED ACT STATUTORY PENAL INTEREST SOP

### Statutory Formula
Under Section 16 of the MSMED Act, 2006:
$$\\text{{Statutory Interest Rate}} = 3 \\times \\text{{RBI Bank Rate}}$$

Compounding frequency: **Monthly rests** (compound interest calculated at the end of each calendar month).

### Current Benchmark Parameters (FY 2024-25)
- **RBI Bank Rate:** ~6.75% per annum
- **Section 16 Statutory Rate:** $3 \\times 6.75\\% = 20.25\\%$ per annum
- **Monthly Compounding Factor:**
  $$A = P \\times \\left(1 + \\frac{{r}}{{12}}\\right)^n$$
  where $r = 0.2025$ and $n$ is number of overdue months.

### Non-Deductibility Mandate
Under Section 23 of MSMED Act:
> *"Notwithstanding anything contained in the Income-tax Act, 1961, the amount of interest payable or paid by any buyer, under or in accordance with the provisions of this Act, shall not, for the purposes of computation of income under the Income-tax Act, 1961, be allowed as deduction."*

### Prevention Checklist for {company_name}
1. Never delay micro/small vendor payouts beyond the 45-day window.
2. Flag invoices with pending dispute notices promptly within 15 days.
3. If interest is computed, account for it separately under inadmissible expenses.
"""
        return "File not found"

    @classmethod
    def generate_zip_bundle(cls, company_name: str = "Enterprise Buyer") -> bytes:
        """Assembles all toolkit files into a downloadable ZIP archive in memory."""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for item in cls.get_template_manifest():
                fname = item["file_name"]
                content = cls.get_document_content(fname, company_name=company_name)
                zf.writestr(fname, content.encode("utf-8"))
        buffer.seek(0)
        return buffer.getvalue()
