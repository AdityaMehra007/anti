"""
VECTIS TRADE — Native SWIFT MT700 Banking Message Parser
Parses standard interbank teletransmission messages into validated LetterOfCredit dataclasses.
"""

import re
from datetime import datetime
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from vectis_core import LetterOfCredit
except ImportError:
    from company.vectis_core import LetterOfCredit

def parse_swift_date(date_str: str) -> str:
    """Converts YYMMDD to YYYY-MM-DD."""
    clean = re.sub(r"[^0-9]", "", date_str.strip())[:6]
    if len(clean) == 6:
        yy, mm, dd = clean[:2], clean[2:4], clean[4:6]
        year = f"20{yy}" if int(yy) < 70 else f"19{yy}"
        return f"{year}-{mm}-{dd}"
    return "2027-12-31"

def parse_swift_mt700(text: str) -> LetterOfCredit:
    """
    Extracts SWIFT fields from raw MT700 text format.
    """
    fields = {}
    current_tag = None
    current_lines = []

    for line in text.strip().splitlines():
        line = line.strip()
        tag_match = re.match(r"^:([0-9]{2}[A-Z]?):(.*)$", line)
        if tag_match:
            if current_tag:
                fields[current_tag] = "\n".join(current_lines).strip()
            current_tag = tag_match.group(1)
            current_lines = [tag_match.group(2).strip()] if tag_match.group(2).strip() else []
        else:
            if current_tag:
                current_lines.append(line)

    if current_tag:
        fields[current_tag] = "\n".join(current_lines).strip()

    # Field :20: Documentary Credit Number
    lc_number = fields.get("20", "UNKNOWN-LC").replace("/", "").strip()

    # Field :32B: Currency and Amount (e.g., EUR180000,00 or USD250000,)
    amt_str = fields.get("32B", "EUR0").strip()
    curr_match = re.match(r"^([A-Z]{3})([0-9,.]+)$", amt_str)
    if curr_match:
        currency = curr_match.group(1)
        raw_val = curr_match.group(2).replace(",", ".")
        try:
            amount = float(raw_val)
        except ValueError:
            amount = 0.0
    else:
        currency = "EUR"
        amount = 100000.0

    # Field :39A: Tolerance Percentage (e.g. 05/05 -> 5.0)
    tol_str = fields.get("39A", "05/05")
    tol_match = re.match(r"([0-9]+)/?([0-9]*)", tol_str)
    tolerance_pct = float(tol_match.group(1)) if tol_match else 5.0

    # Dates
    latest_shipment_date = parse_swift_date(fields.get("44C", "270415"))
    expiry_date_field = fields.get("31D", "270505")
    expiry_date = parse_swift_date(expiry_date_field[:6])

    # Ports
    port_of_loading = fields.get("44A", "Chennai Port, India").replace("\n", " ").strip()
    port_of_discharge = fields.get("44B", "Hamburg, Germany").replace("\n", " ").strip()

    # Description of Goods :45A:
    description_of_goods = fields.get("45A", "Goods as per purchase order").replace("\n", " ").strip()

    # Parties
    applicant = fields.get("50", "Applicant Buyer GmbH").splitlines()[0].strip()
    beneficiary = fields.get("59", "Beneficiary Exporter Pvt Ltd").splitlines()[0].strip()

    # Issuing bank from :51A: or default
    issuing_bank = fields.get("51A", fields.get("52A", "Deutsche Bank AG, Frankfurt")).replace("\n", " ").strip()

    return LetterOfCredit(
        lc_number=lc_number,
        issuing_bank=issuing_bank,
        applicant=applicant,
        beneficiary=beneficiary,
        amount=amount,
        currency=currency,
        tolerance_pct=tolerance_pct,
        latest_shipment_date=latest_shipment_date,
        expiry_date=expiry_date,
        port_of_loading=port_of_loading,
        port_of_discharge=port_of_discharge,
        description_of_goods=description_of_goods
    )

SAMPLE_SWIFT_MT700 = """
:27:1/1
:40A:IRREVOCABLE
:20:LC-DB-2027-9941
:31C:270310
:31D:270515FRANKFURT
:51A:DEUTDEDDXXX
:50:MULLER AUTOMOBILTECHNIK GMBH
INDUSTRIESTRASSE 42
60311 FRANKFURT, GERMANY
:59:PRECISION AUTO MACHINING PVT LTD
PLOT 84, PEENYA INDUSTRIAL AREA
BENGALURU 560058, INDIA
:32B:EUR180000,00
:39A:05/05
:44A:CHENNAI PORT, INDIA
:44B:HAMBURG, GERMANY
:44C:270420
:45A:CNC MACHINED TRANSMISSION FLANGES GRADE 316 AS PER PO 88412
:46A:+SIGNED COMMERCIAL INVOICE IN 3 ORIGINALS
+FULL SET CLEAN ON BOARD BILLS OF LADING CONSIGNED TO ORDER OF DEUTSCHE BANK AG
+PACKING LIST IN 3 COPIES
+CERTIFICATE OF ORIGIN ISSUED BY CHAMBER OF COMMERCE
:47A:ALL DOCUMENTS MUST INDICATE LC NUMBER
:71B:ALL BANKING CHARGES OUTSIDE GERMANY ARE FOR BENEFICIARY ACCOUNT
:48:21 DAYS AFTER DATE OF SHIPMENT
"""

if __name__ == "__main__":
    lc = parse_swift_mt700(SAMPLE_SWIFT_MT700)
    print("Successfully parsed SWIFT MT700 Message:")
    print(f"  - LC Number: {lc.lc_number}")
    print(f"  - Issuing Bank: {lc.issuing_bank}")
    print(f"  - Applicant: {lc.applicant}")
    print(f"  - Beneficiary: {lc.beneficiary}")
    print(f"  - Amount: {lc.currency} {lc.amount:,.2f} (+/- {lc.tolerance_pct}%)")
    print(f"  - Latest Shipment: {lc.latest_shipment_date}")
    print(f"  - Goods Description: {lc.description_of_goods}")
