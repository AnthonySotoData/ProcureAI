from pathlib import Path

import fitz


OUTPUT_PATH = Path("data/documents/apex_supplier_agreement.pdf")


PAGE_ONE = """
APEX MANUFACTURING SUPPLIER AGREEMENT

Contract Number: AM-2026-0042

This Supplier Agreement is entered into between Apex Manufacturing LLC,
referred to as the Supplier, and Northstar Aerospace Corporation, referred
to as the Buyer.

1. EFFECTIVE DATE AND TERM

This Agreement becomes effective on August 1, 2026, and remains in effect
through July 31, 2028, unless terminated earlier under this Agreement.

2. SCOPE OF SERVICES

The Supplier will manufacture and deliver precision-machined aluminum
components according to the technical specifications and purchase orders
issued by the Buyer.

3. DELIVERY REQUIREMENTS

The Supplier must deliver the first production batch no later than
September 15, 2026.

Subsequent deliveries must occur according to the schedule included in
each purchase order.

The Supplier must notify the Buyer in writing within two business days
after identifying any condition that may delay delivery.

4. QUALITY REQUIREMENTS

All components must satisfy the Buyer's engineering drawings, inspection
criteria, and applicable ISO 9001 quality-management requirements.

The Buyer may reject components that fail inspection or do not conform to
the applicable technical specifications.
"""


PAGE_TWO = """
APEX MANUFACTURING SUPPLIER AGREEMENT

5. PRICING AND PAYMENT

The initial unit price is $425 per component.

The Supplier may not increase pricing during the first twelve months of
the Agreement.

After the first twelve months, proposed price increases require at least
sixty days of written notice and written approval from the Buyer.

The Buyer will pay undisputed invoices within forty-five days after the
Buyer receives and approves a complete and accurate invoice.

Invoices must include the purchase-order number, contract number,
delivery date, quantity delivered, and unit price.

6. BUYER RESPONSIBILITIES

The Buyer must provide current technical drawings, purchase orders, and
delivery instructions.

The Buyer must inspect delivered products within ten business days after
receipt.

7. CONFIDENTIALITY

The Supplier must protect all technical drawings, pricing information,
forecasts, and other confidential information received from the Buyer.

Confidential information may not be disclosed to another party without
the Buyer's prior written approval.
"""


PAGE_THREE = """
APEX MANUFACTURING SUPPLIER AGREEMENT

8. CYBERSECURITY AND DATA PROTECTION

The Supplier must maintain reasonable administrative, technical, and
physical safeguards for Buyer information.

The Supplier must notify the Buyer within twenty-four hours after
discovering a confirmed or suspected cybersecurity incident involving
Buyer information.

9. TERMINATION

Either party may terminate this Agreement for material breach if the
breaching party fails to correct the breach within thirty days after
receiving written notice.

The Buyer may terminate the Agreement immediately for repeated quality
failures, unauthorized disclosure of confidential information, or failure
to report a cybersecurity incident.

10. RECORD RETENTION AND AUDIT

The Supplier must retain quality, delivery, and invoice records for seven
years after the applicable transaction.

The Buyer may audit relevant records after providing ten business days of
written notice.

11. INSURANCE

The Supplier must maintain appropriate commercial general liability and
workers' compensation insurance.

The Agreement does not specify minimum liability coverage amounts.

12. GOVERNING LAW

This Agreement is governed by the laws of the Commonwealth of
Pennsylvania.
"""


def create_pdf() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    document = fitz.open()

    for page_text in (PAGE_ONE, PAGE_TWO, PAGE_THREE):
        page = document.new_page(width=612, height=792)

        page.insert_textbox(
            fitz.Rect(50, 50, 562, 742),
            page_text.strip(),
            fontsize=10,
            fontname="helv",
            lineheight=1.3,
        )

    document.save(OUTPUT_PATH)
    document.close()

    print(f"Created sample contract: {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    create_pdf()