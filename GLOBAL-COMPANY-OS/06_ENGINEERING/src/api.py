import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from src.models import (
    CommercialInvoice,
    ComplianceAuditReport,
    PackingReconciliationRequest,
    ReconciliationReport,
    IntegratedDocketAuditReport,
    DocketTextRequest
)
from src.compliance_auditor import ComplianceAuditor
from src.hs_engine import HSCatalog

UI_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ui", "index.html"))

app = FastAPI(
    title="TradeNexus AI Compliance Engine",
    description="Autonomous Customs Docket Verification & HS-Code Intelligence for Indian Exporters",
    version="1.0.0"
)

@app.get("/")
def get_ui():
    if os.path.exists(UI_PATH):
        return FileResponse(UI_PATH)
    return {"message": "TradeNexus AI API active. UI index not found."}


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "TradeNexus Compliance Core",
        "rules_active": len(HSCatalog.DATABASE),
        "version": "1.0.0"
    }

@app.post("/api/v1/audit/docket", response_model=ComplianceAuditReport)
def audit_export_docket(invoice: CommercialInvoice):
    try:
        report = ComplianceAuditor.audit_invoice(invoice)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/classify/hs")
def classify_product(description: str):
    res = HSCatalog.classify(description)
    return res

@app.post("/api/v1/invoice/parse-text", response_model=CommercialInvoice)
def parse_raw_invoice(raw_text: str):
    from src.invoice_parser import CommercialInvoiceParser
    try:
        return CommercialInvoiceParser.parse_invoice_text(raw_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse invoice text: {str(e)}")

@app.post("/api/v1/cbam/generate-xml")
def generate_cbam_declaration(
    declaration_id: str,
    quarter: str,
    declarant_eori: str,
    installation_name: str,
    un_locode: str,
    cn_code: str,
    goods_description: str,
    net_mass_tonnes: float,
    direct_emissions: float,
    indirect_emissions: float,
    carbon_price_due_eur: float
):
    from src.cbam_xml_generator import CBAMDeclarationGenerator, InstallationData, CBAMEmissionsItem
    try:
        inst = InstallationData(
            installation_name=installation_name,
            country_code="IN",
            un_locode=un_locode,
            latitude=12.9716,
            longitude=77.5946
        )
        items = [
            CBAMEmissionsItem(
                item_id="ITM-01",
                cn_code=cn_code,
                goods_description=goods_description,
                net_mass_tonnes=net_mass_tonnes,
                production_route="Electric Arc Furnace",
                direct_embedded_emissions=direct_emissions,
                indirect_embedded_emissions=indirect_emissions,
                carbon_price_due_eur=carbon_price_due_eur
            )
        ]
        xml_str = CBAMDeclarationGenerator.generate_declaration_xml(
            declaration_id=declaration_id,
            quarter=quarter,
            declarant_eori=declarant_eori,
            installation=inst,
            items=items
        )
        return {"declaration_id": declaration_id, "xml_content": xml_str}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/icegate/generate-flatfile")
def generate_icegate_flatfile(invoice: CommercialInvoice, job_number: str = None):
    from src.icegate_edi_generator import ICEGATEEDIGenerator
    try:
        res = ICEGATEEDIGenerator.generate_shipping_bill_flatfile(invoice, job_number=job_number)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate ICEGATE flatfile: {str(e)}")

@app.post("/api/v1/icegate/validate-invoice")
def validate_icegate_invoice(invoice: CommercialInvoice):
    from src.icegate_edi_generator import ICEGATEEDIGenerator
    try:
        return ICEGATEEDIGenerator.validate_icegate_payload(invoice)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to validate ICEGATE payload: {str(e)}")

@app.post("/api/v1/reconcile/packing-list", response_model=ReconciliationReport)
def reconcile_packing_list(req: PackingReconciliationRequest):
    from src.packing_reconciler import PackingListReconciler
    try:
        return PackingListReconciler.reconcile(req.invoice, req.packing_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reconcile packing list: {str(e)}")

@app.post("/api/v1/docket/audit-text", response_model=IntegratedDocketAuditReport)
def audit_composite_docket_text(req: DocketTextRequest):
    from src.document_ingestion import DocumentIngestionPipeline
    try:
        return DocumentIngestionPipeline.process_composite_docket(req.raw_docket_text)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process composite docket: {str(e)}")

@app.post("/api/v1/docket/audit-structured", response_model=IntegratedDocketAuditReport)
def audit_composite_docket_structured(req: PackingReconciliationRequest):
    from src.document_ingestion import DocumentIngestionPipeline
    try:
        return DocumentIngestionPipeline.process_structured_docket(req.invoice, req.packing_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process structured docket: {str(e)}")

# ---------------------------------------------------------
# OMNIVERSE BUSINESS OS: GLOBAL INTELLIGENCE ENDPOINTS
# ---------------------------------------------------------
@app.get("/api/v1/os/summary")
def get_omniverse_summary():
    from src.omniverse_service import OmniverseService
    return OmniverseService.get_summary()

@app.get("/api/v1/os/opportunities")
def get_omniverse_opportunities(sector: str = None, min_score: float = None, limit: int = 100):
    from src.omniverse_service import OmniverseService
    return OmniverseService.get_opportunities(sector=sector, min_score=min_score, limit=limit)

@app.get("/api/v1/os/problems")
def get_omniverse_problems(industry: str = None, severity: str = None, limit: int = 100):
    from src.omniverse_service import OmniverseService
    return OmniverseService.get_problems(industry=industry, severity=severity, limit=limit)

@app.get("/api/v1/os/automations")
def get_omniverse_automations(functional_area: str = None, min_level: int = None, limit: int = 100):
    from src.omniverse_service import OmniverseService
    return OmniverseService.get_automations(functional_area=functional_area, min_level=min_level, limit=limit)

@app.get("/api/v1/os/winner")
def get_omniverse_winner():
    from src.omniverse_service import OmniverseService
    return OmniverseService.get_winner_dossier()


