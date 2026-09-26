"""
VECTIS TRADE — Multi-Document Parser & Sample Docket Generator
Parses raw JSON/dict payloads into typed trade dataclasses and creates sample dockets in company/inbox/.
"""

import json
import os
try:
    from vectis_core import (
        LetterOfCredit,
        CommercialInvoice,
        PackingList,
        BillOfLading,
        CertificateOfOrigin
    )
except ImportError:
    from company.vectis_core import (
        LetterOfCredit,
        CommercialInvoice,
        PackingList,
        BillOfLading,
        CertificateOfOrigin
    )

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INBOX_DIR = os.path.join(BASE_DIR, "inbox")

def parse_docket_dict(data: dict):
    """
    Converts a structured trade docket dictionary into validated dataclass instances.
    """
    lc = LetterOfCredit(**data["lc"])
    invoice = CommercialInvoice(**data["invoice"])
    packing_list = PackingList(**data["packing_list"])
    bl = BillOfLading(**data["bl"])
    coo = CertificateOfOrigin(**data["coo"]) if data.get("coo") else None
    return lc, invoice, packing_list, bl, coo

def generate_sample_dockets():
    """
    Generates realistic trade dockets in company/inbox/ for testing and live autonomous daemon execution.
    """
    os.makedirs(INBOX_DIR, exist_ok=True)

    # 1. Clean Peenya CNC Auto Parts Export Docket
    docket_clean = {
        "lc": {
            "lc_number": "LC-PEENYA-2027-889",
            "issuing_bank": "Deutsche Bank AG, Frankfurt",
            "applicant": "Muller Automobiltechnik GmbH",
            "beneficiary": "Precision Auto Machining Pvt Ltd",
            "amount": 180000.0,
            "currency": "EUR",
            "tolerance_pct": 5.0,
            "latest_shipment_date": "2027-04-15",
            "expiry_date": "2027-05-05",
            "port_of_loading": "Chennai Port, India",
            "port_of_discharge": "Hamburg, Germany",
            "description_of_goods": "CNC Machined Transmission Flanges Grade 316 as per PO 88412"
        },
        "invoice": {
            "invoice_number": "PAM/EXP/2027/099",
            "invoice_date": "2027-04-02",
            "beneficiary": "Precision Auto Machining Pvt Ltd",
            "applicant": "Muller Automobiltechnik GmbH",
            "amount": 180000.0,
            "currency": "EUR",
            "description_of_goods": "CNC Machined Transmission Flanges Grade 316 as per PO 88412",
            "incoterms": "CIF Hamburg"
        },
        "packing_list": {
            "packing_list_number": "PL/2027/099",
            "invoice_number": "PAM/EXP/2027/099",
            "total_packages": 14,
            "package_type": "Wooden Pallets",
            "gross_weight_kg": 15400.0,
            "net_weight_kg": 14900.0,
            "shipping_marks": "MULLER/HAMBURG/1-14"
        },
        "bl": {
            "bl_number": "MEDUCN9921401",
            "carrier_name": "Mediterranean Shipping Company (MSC)",
            "shipper": "Precision Auto Machining Pvt Ltd",
            "consignee": "To Order of Deutsche Bank AG, Frankfurt",
            "notify_party": "Muller Automobiltechnik GmbH",
            "port_of_loading": "Chennai Port, India",
            "port_of_discharge": "Hamburg, Germany",
            "shipped_on_board_date": "2027-04-08",
            "freight_status": "Freight Prepaid",
            "clean_on_board": True,
            "total_packages": 14,
            "gross_weight_kg": 15400.0,
            "shipping_marks": "MULLER/HAMBURG/1-14"
        },
        "coo": {
            "coo_number": "COO-FIEO-2027-991",
            "issuing_authority": "Federation of Indian Export Organisations (FIEO)",
            "exporter": "Precision Auto Machining Pvt Ltd",
            "consignee": "Muller Automobiltechnik GmbH",
            "origin_country": "India",
            "gross_weight_kg": 15400.0,
            "invoice_number": "PAM/EXP/2027/099"
        }
    }

    # 2. Flawed Tirupur Garment Export Docket (Weight mismatch + Description typo)
    docket_flawed = {
        "lc": {
            "lc_number": "LC-TIRUPUR-2027-104",
            "issuing_bank": "BNP Paribas, Paris",
            "applicant": "Galeries de Mode SAS",
            "beneficiary": "Tirupur Premier Apparel Exports",
            "amount": 95000.0,
            "currency": "EUR",
            "tolerance_pct": 5.0,
            "latest_shipment_date": "2027-03-30",
            "expiry_date": "2027-04-20",
            "port_of_loading": "Tuticorin Port, India",
            "port_of_discharge": "Le Havre, France",
            "description_of_goods": "100% Organic Combed Cotton Knitted T-Shirts Style TK-90"
        },
        "invoice": {
            "invoice_number": "TPA/2027/412",
            "invoice_date": "2027-03-25",
            "beneficiary": "Tirupur Premier Apparel Exports",
            "applicant": "Galeries de Mode SAS",
            "amount": 95000.0,
            "currency": "EUR",
            "description_of_goods": "Cotton Knitted T-Shirts Style TK-90",  # Omitted "100% Organic Combed"
            "incoterms": "FOB Tuticorin"
        },
        "packing_list": {
            "packing_list_number": "PL/2027/412",
            "invoice_number": "TPA/2027/412",
            "total_packages": 120,
            "package_type": "Corrugated Cartons",
            "gross_weight_kg": 6200.0,
            "net_weight_kg": 5800.0,
            "shipping_marks": "GDM/LEHAVRE/1-120"
        },
        "bl": {
            "bl_number": "MAEU88192031",
            "carrier_name": "Maersk Line",
            "shipper": "Tirupur Premier Apparel Exports",
            "consignee": "To Order of BNP Paribas",
            "notify_party": "Galeries de Mode SAS",
            "port_of_loading": "Tuticorin Port, India",
            "port_of_discharge": "Le Havre, France",
            "shipped_on_board_date": "2027-03-28",
            "freight_status": "Freight Collect",
            "clean_on_board": True,
            "total_packages": 120,
            "gross_weight_kg": 6850.0,  # Conflict: 6,850 kg vs 6,200 kg in PL
            "shipping_marks": "GDM/LEHAVRE/1-120"
        }
    }

    f1 = os.path.join(INBOX_DIR, "docket_peenya_clean.json")
    f2 = os.path.join(INBOX_DIR, "docket_tirupur_flawed.json")

    with open(f1, "w", encoding="utf-8") as f:
        json.dump(docket_clean, f, indent=2)
    with open(f2, "w", encoding="utf-8") as f:
        json.dump(docket_flawed, f, indent=2)

    print(f"Sample dockets generated in: {INBOX_DIR}")
    print(f"  - {f1}")
    print(f"  - {f2}")

if __name__ == "__main__":
    generate_sample_dockets()
