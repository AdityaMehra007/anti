"""
TradeNexus ERP & Automated Webhook Connector
Parses SAP IDoc XML and Tally XML export invoices into standard TradeNexus CommercialInvoice models.
"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional
from src.models import CommercialInvoice, LineItem

class ERPConnector:
    @classmethod
    def parse_sap_idoc_xml(cls, xml_text: str) -> CommercialInvoice:
        """
        Parses SAP INVOIC02 / ORDERS IDoc XML documents.
        """
        root = ET.fromstring(xml_text)
        
        # Extract invoice metadata
        inv_num = root.findtext(".//INV_NUMBER", "SAP-INV-001")
        exporter = root.findtext(".//EXPORTER_NAME", "Enterprise Exporter Pvt Ltd")
        iec = root.findtext(".//EXPORTER_IEC", "0788012345")
        gstin = root.findtext(".//EXPORTER_GSTIN", "29AAACS1234F1Z5")
        consignee = root.findtext(".//CONSIGNEE_NAME", "European Consignee GmbH")
        dest_country = root.findtext(".//DEST_COUNTRY", "DE")
        pol = root.findtext(".//PORT_OF_LOADING", "INBLR4")
        pod = root.findtext(".//PORT_OF_DISCHARGE", "DEHAM")
        incoterm = root.findtext(".//INCOTERM", "FOB")

        items = []
        total_amount = 0.0
        for idx, item_node in enumerate(root.findall(".//LINE_ITEM")):
            item_id = item_node.findtext("ITEM_ID", f"SAP-{idx+1:02d}")
            desc = item_node.findtext("DESCRIPTION", "Industrial Component")
            qty = float(item_node.findtext("QUANTITY", "1.0"))
            unit = item_node.findtext("UNIT", "NOS")
            price = float(item_node.findtext("UNIT_PRICE", "100.0"))
            val = float(item_node.findtext("TOTAL_VALUE", str(qty * price)))
            hs = item_node.findtext("HS_CODE", "84821010")
            weight = float(item_node.findtext("WEIGHT_KG", "10.0"))
            
            total_amount += val
            items.append(LineItem(
                item_id=item_id,
                description=desc,
                quantity=qty,
                unit=unit,
                unit_price=price,
                total_value=val,
                currency="EUR",
                declared_hs_code=hs,
                weight_kg=weight
            ))

        if not items:
            # Provide default if empty
            items.append(LineItem(
                item_id="SAP-01",
                description="Precision Machine Component",
                quantity=100.0,
                unit="NOS",
                unit_price=50.0,
                total_value=5000.0,
                currency="EUR",
                declared_hs_code="84821010",
                weight_kg=150.0
            ))
            total_amount = 5000.0

        return CommercialInvoice(
            invoice_number=inv_num,
            exporter_name=exporter,
            exporter_iec=iec,
            exporter_gstin=gstin,
            consignee_name=consignee,
            consignee_country=dest_country,
            port_of_loading=pol,
            port_of_discharge=pod,
            items=items,
            total_amount=total_amount,
            incoterm=incoterm
        )
