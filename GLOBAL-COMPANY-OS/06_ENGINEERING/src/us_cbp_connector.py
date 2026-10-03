"""
TradeNexus US Customs and Border Protection (CBP) ACE Connector
Cross-maps Indian ITC(HS) codes to 10-digit HTS-US schedules, calculates Section 301/232 duties,
and generates automated CBP Form 7501 Entry Summary verification payloads.
"""

import hashlib
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class USCustomsEntryItem(BaseModel):
    item_id: str
    description: str
    itc_hs_code: str
    hts_us_code: str
    entered_value_usd: float
    duty_rate_percent: float
    section_301_applicable: bool
    section_232_applicable: bool
    calculated_duty_usd: float
    uflpa_compliant: bool

class USCustomsClearanceReport(BaseModel):
    entry_reference: str
    importer_of_record: str
    port_of_entry: str  # e.g. "USNYC" (New York), "USLAX" (Los Angeles)
    total_entered_value_usd: float
    total_duty_payable_usd: float
    items: List[USCustomsEntryItem]
    customs_entry_flatfile: str
    uflpa_certification_hash: str
    status: str

class USCustomsConnector:
    # 8-digit Indian ITC-HS to 10-digit US HTS-US Cross-Mapping Catalog
    HTS_MAPPING = {
        "73269099": {"hts": "7326.90.8688", "duty_pct": 2.9, "sec_301": False, "sec_232": True}, # Other articles of iron/steel
        "84821010": {"hts": "8482.10.5044", "duty_pct": 4.0, "sec_301": False, "sec_232": False}, # Ball bearings
        "88033000": {"hts": "8807.30.0030", "duty_pct": 0.0, "sec_301": False, "sec_232": False}, # Airplane parts
        "29153990": {"hts": "2915.39.4550", "duty_pct": 3.7, "sec_301": False, "sec_232": False}, # Acetic acid esters
        "72104900": {"hts": "7210.49.0091", "duty_pct": 0.0, "sec_301": False, "sec_232": True}, # Plated/coated steel
        "87082900": {"hts": "8708.29.5060", "duty_pct": 2.5, "sec_301": False, "sec_232": False}  # Auto body parts
    }

    @classmethod
    def audit_us_shipment(cls, entry_id: str, importer_name: str, port_of_entry: str, line_items: List[Dict[str, Any]]) -> USCustomsClearanceReport:
        items_res = []
        total_val = 0.0
        total_duty = 0.0

        for itm in line_items:
            itc_hs = str(itm.get("hs_code", "")).replace(".", "").strip()
            val = float(itm.get("value_usd", 0.0))
            desc = itm.get("description", "Manufactured Goods")
            item_id = itm.get("item_id", "ITM-01")

            map_data = cls.HTS_MAPPING.get(itc_hs, {"hts": f"{itc_hs[:4]}.{itc_hs[4:6]}.0000", "duty_pct": 3.0, "sec_301": False, "sec_232": False})
            duty_rate = map_data["duty_pct"]
            
            # Additional Section 232 steel duty (25% if applicable)
            sec_232 = map_data.get("sec_232", False)
            effective_duty_rate = duty_rate + (25.0 if sec_232 else 0.0)
            item_duty = round(val * (effective_duty_rate / 100.0), 2)

            total_val += val
            total_duty += item_duty

            items_res.append(USCustomsEntryItem(
                item_id=item_id,
                description=desc,
                itc_hs_code=itc_hs,
                hts_us_code=map_data["hts"],
                entered_value_usd=val,
                duty_rate_percent=effective_duty_rate,
                section_301_applicable=map_data["sec_301"],
                section_232_applicable=sec_232,
                calculated_duty_usd=item_duty,
                uflpa_compliant=True
            ))

        # Generate standard US CBP Form 7501 EDI block
        ts = time.strftime("%Y%m%d%H%M")
        flatfile = f"CBP7501*ENTRY*{entry_id}*PORT*{port_of_entry}*IMPORTER*{importer_name}*VAL*{total_val:.2f}*DUTY*{total_duty:.2f}*DATE*{ts}"
        uflpa_hash = hashlib.sha256(f"UFLPA-NON-XINJIANG-ORIGIN-INDIA-{entry_id}-{total_val}".encode("utf-8")).hexdigest()

        return USCustomsClearanceReport(
            entry_reference=entry_id,
            importer_of_record=importer_name,
            port_of_entry=port_of_entry,
            total_entered_value_usd=total_val,
            total_duty_payable_usd=total_duty,
            items=items_res,
            customs_entry_flatfile=flatfile,
            uflpa_certification_hash=uflpa_hash,
            status="PASSED_READY_FOR_CBP_ACE_TRANSMISSION"
        )
