"""Global Money Map - Legitimate International Financial Infrastructure Registry.

Comprehensive directory of verified banks, payment gateways, FX platforms,
and treasury providers across India, USA, UK, EU, UAE, and Singapore.
Enforces: Never bypass jurisdictional controls; operate on legitimate rails.
"""

from typing import Any

GLOBAL_INFRASTRUCTURE = [
    {
        "id": "INFRA-IN-HDFC",
        "name": "HDFC Bank Corporate Current Account",
        "country": "India",
        "institution_type": "Scheduled Commercial Bank",
        "currencies": ["INR"],
        "eligibility": "Sole Proprietorship / Private Limited registered in India",
        "fees": "Zero maintenance with maintainable AQB, minimal NEFT/RTGS fees",
        "regulatory_status": "Regulated by Reserve Bank of India (RBI)",
        "api_access": "HDFC SmartHub / Corporate Banking APIs",
        "primary_purpose": "Operating account for domestic revenue receipts and vendor settlements."
    },
    {
        "id": "INFRA-IN-RAZORPAY",
        "name": "Razorpay Payment Gateway",
        "country": "India",
        "institution_type": "Payment Aggregator",
        "currencies": ["INR", "USD", "EUR", "GBP", "AED"],
        "eligibility": "Indian registered business with verified PAN, GST, and bank account",
        "fees": "2.0% standard domestic; 3.0% international + statutory taxes",
        "regulatory_status": "Licensed Payment Aggregator by RBI",
        "api_access": "Full REST APIs, Webhooks, Python SDK",
        "primary_purpose": "Card payments, UPI, international cards, and automated invoicing."
    },
    {
        "id": "INFRA-GL-WISE",
        "name": "Wise Business (Multi-Currency Vault)",
        "country": "United Kingdom / Global",
        "institution_type": "Licensed Electronic Money Institution / Authorized Dealer Rail",
        "currencies": ["USD", "EUR", "GBP", "SGD", "AUD", "INR"],
        "eligibility": "Indian Sole Proprietorship or Company exporting services globally",
        "fees": "Mid-market exchange rate + transparent 0.35%–0.50% conversion fee",
        "regulatory_status": "Regulated by FCA (UK), FinCEN (USA), and partnered with Authorized Dealer banks in India",
        "api_access": "Robust Webhook & REST API for balance tracking and statement ingestion",
        "primary_purpose": "International B2B customer payments, local ACH/SWIFT collections, and compliant inward remittance with e-FIRC."
    },
    {
        "id": "INFRA-US-STRIPE",
        "name": "Stripe International Payments",
        "country": "United States / Global",
        "institution_type": "Global Payment Infrastructure",
        "currencies": ["USD", "EUR", "GBP", "AUD", "CAD"],
        "eligibility": "Global merchants with verified legal identity and compliant terms of service",
        "fees": "2.9% + 30¢ per successful card charge; 1% currency conversion fee",
        "regulatory_status": "Licensed Money Transmitter in US, FCA regulated in UK/EU",
        "api_access": "Gold-standard REST APIs and Webhook infrastructure",
        "primary_purpose": "International subscription billing, invoice checkout links, and SaaS payment links."
    },
    {
        "id": "INFRA-SG-ASPIRE",
        "name": "Aspire Financial Technologies",
        "country": "Singapore",
        "institution_type": "Fintech Business Account",
        "currencies": ["SGD", "USD", "EUR"],
        "eligibility": "Singapore registered entity or Southeast Asian operating footprint",
        "fees": "Low FX markup (0.4%–0.6%), zero monthly account fees",
        "regulatory_status": "Operates under Major Payment Institution license granted by Monetary Authority of Singapore (MAS)",
        "api_access": "Open API integration",
        "primary_purpose": "Treasury management and vendor payments for APAC regional expansion."
    },
    {
        "id": "INFRA-AE-WIO",
        "name": "Wio Business Platform",
        "country": "United Arab Emirates",
        "institution_type": "Digital Corporate Bank",
        "currencies": ["AED", "USD", "EUR", "GBP"],
        "eligibility": "UAE mainland or free zone entity (e.g. IFZA, DMCC)",
        "fees": "Competitive corporate plans (AED 99/month)",
        "regulatory_status": "Licensed and regulated by Central Bank of the UAE (CBUAE)",
        "api_access": "Developer APIs available",
        "primary_purpose": "Middle East trade hub operations and GCC client collections."
    }
]


class GlobalMoneyMap:
    @staticmethod
    def get_all_infrastructure() -> list[dict[str, Any]]:
        return GLOBAL_INFRASTRUCTURE

    @staticmethod
    def get_rail_by_id(rail_id: str) -> dict[str, Any]:
        for item in GLOBAL_INFRASTRUCTURE:
            if item["id"] == rail_id:
                return item
        raise ValueError(f"Infrastructure rail '{rail_id}' not found.")


global_money_map = GlobalMoneyMap()
