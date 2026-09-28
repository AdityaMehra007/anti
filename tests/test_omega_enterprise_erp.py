"""
Tests for OMEGA INFINITY — MNC Enterprise ERP, P&L, Balance Sheet, and Order Platform.
Enforces Ind AS / GAAP financial accounting, CRM client directory, and OMS integrity.
"""

import os
import sys
import json
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from omega_infinity.omega_infinity_core import get_kernel
from omega_infinity.omega_enterprise_erp import (
    get_erp,
    EnterpriseERPEngine,
    EnterpriseClient,
    EnterpriseOrder,
    FinancialStatement
)


class TestEnterpriseERP:

    @pytest.fixture(autouse=True)
    def setup_erp(self):
        self.kernel = get_kernel()
        self.erp = get_erp()

    def test_erp_initialization(self):
        assert len(self.erp.clients) >= 5, "ERP should have seeded at least 5 industrial clients"
        assert len(self.erp.orders) >= 5, "ERP should have seeded at least 5 export orders"
        assert "ACC-BLR-001" in self.erp.clients
        assert "ORD-2027-001" in self.erp.orders

    def test_pnl_financial_statement_accuracy(self):
        fin: FinancialStatement = self.erp.generate_financial_statement()

        # Revenue checks
        assert fin.gross_saas_revenue_inr > 0
        assert fin.audit_transaction_fees_inr > 0
        assert fin.cbam_consulting_revenue_inr > 0
        assert fin.total_gross_revenue_inr == (
            fin.gross_saas_revenue_inr + fin.audit_transaction_fees_inr + fin.cbam_consulting_revenue_inr
        )

        # COGS & Gross Profit
        assert fin.total_cogs_inr > 0
        assert fin.gross_profit_inr == fin.total_gross_revenue_inr - fin.total_cogs_inr
        assert fin.gross_margin_pct >= 95.0, f"Gross margin should exceed 95%, got {fin.gross_margin_pct}%"

        # OPEX & EBITDA
        assert fin.total_opex_inr > 0
        assert fin.ebitda_inr == fin.gross_profit_inr - fin.total_opex_inr
        assert fin.ebitda_margin_pct >= 85.0, f"EBITDA margin should exceed 85%, got {fin.ebitda_margin_pct}%"

        # Tax Exemption (Section 80-IAC)
        assert fin.tax_rate_pct == 0.0, "Section 80-IAC must provide 0% tax holiday"
        assert fin.tax_expense_inr == 0.0, "Tax expense must be zero under 3-year exemption"
        assert fin.net_income_inr == fin.ebit_inr, "Net income must equal EBIT when tax is zero"

    def test_balance_sheet_reconciliation(self):
        fin = self.erp.generate_financial_statement()
        # Balance Sheet fundamental law: Total Assets == Total Liabilities + Shareholder Equity
        reconciled_equity_and_liabilities = fin.accounts_payable_inr + fin.total_equity_inr
        assert abs(fin.total_assets_inr - reconciled_equity_and_liabilities) < 1.0, (
            f"Assets ({fin.total_assets_inr}) must equal Liabilities + Equity ({reconciled_equity_and_liabilities})"
        )
        assert fin.cash_and_reserves_inr >= 5000000.0, "Must maintain ₹50L minimum cash reserves"

    def test_unit_economics_compounding(self):
        fin = self.erp.generate_financial_statement()
        assert fin.arpu_inr >= 200000.0, "ARPU should reflect B2B enterprise tier pricing"
        assert fin.cac_inr <= 25000.0, "CAC should be lean due to direct founder/LinkedIn motion"
        assert fin.ltv_cac_ratio >= 10.0, f"Top-1% LTV/CAC ratio must exceed 10x, got {fin.ltv_cac_ratio}x"
        assert fin.runway_months >= 100.0, f"Runway must be massive, got {fin.runway_months} months"

    def test_add_client_and_audit_event(self):
        import time
        unique_client_id = f"ACC-TEST-{time.time_ns()}"
        initial_count = len(self.erp.clients)
        test_client = EnterpriseClient(
            account_id=unique_client_id,
            company_name="Bangalore Test Hydraulics Pvt Ltd",
            hub_location="Doddaballapur Industrial Area, Bengaluru",
            industry_sector="High-Pressure Hydraulic Valves",
            export_turnover_annual_eur=1500000.0,
            decision_maker_name="Test Director",
            decision_maker_title="Managing Director",
            contract_tier="GROWTH",
            mrr_inr=30000.0,
            arr_inr=360000.0,
            status="ACTIVE",
            payment_terms="Net 30 Days",
            credit_rating="AA",
            joined_date="2027-04-20"
        )
        res = self.erp.add_client(test_client)
        assert res["success"] is True
        assert len(self.erp.clients) == initial_count + 1
        assert self.erp.clients[unique_client_id].company_name == "Bangalore Test Hydraulics Pvt Ltd"

    def test_create_order_and_sha256_audit_seal(self):
        import time
        unique_order_id = f"ORD-TEST-{time.time_ns()}"
        initial_orders = len(self.erp.orders)
        test_order = EnterpriseOrder(
            order_id=unique_order_id,
            client_id="ACC-BLR-001",
            client_name="Precision Auto Machining Pvt Ltd",
            buyer_counterparty="Bosch Rexroth AG",
            buyer_country="Germany",
            consignment_value_eur=220000.0,
            currency="EUR",
            platform_fee_inr=28000.0,
            lc_number="LC-TEST-9991",
            docket_status="AUDITED_PASSED",
            cbam_required=False,
            cbam_tariff_eur=0.0,
            sha256_audit_seal="abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            created_at="2027-04-22T10:00:00"
        )
        res = self.erp.create_order(test_order)
        assert res["success"] is True
        assert len(self.erp.orders) == initial_orders + 1
        assert self.erp.orders[unique_order_id].buyer_counterparty == "Bosch Rexroth AG"

    def test_generate_markdown_reports(self):
        reports = self.erp.generate_markdown_reports()
        assert "financial_report" in reports
        assert "portfolio_report" in reports

        assert os.path.exists(reports["financial_report"])
        assert os.path.exists(reports["portfolio_report"])

        with open(reports["financial_report"], "r", encoding="utf-8") as f:
            fin_text = f.read()
            assert "STATEMENT OF PROFIT & LOSS" in fin_text.upper()
            assert "BALANCE SHEET" in fin_text.upper()
            assert "SECTION 80-IAC" in fin_text.upper()

        with open(reports["portfolio_report"], "r", encoding="utf-8") as f:
            ord_text = f.read()
            assert "ENTERPRISE CLIENT CRM" in ord_text.upper()
            assert "LIVE EXPORT ORDER MANAGEMENT LEDGER" in ord_text.upper()
            assert "PEENYA" in ord_text.upper()

    def test_portfolio_summary_metrics(self):
        summary = self.erp.get_portfolio_summary()
        assert summary["total_clients"] >= 5
        assert summary["active_clients"] >= 5
        assert summary["total_arr_inr"] >= 2700000.0
        assert summary["total_consignment_value_eur"] >= 1400000.0
        assert summary["total_platform_fees_earned_inr"] >= 180000.0
