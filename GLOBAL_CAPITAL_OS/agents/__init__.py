"""GLOBAL CAPITAL OS 17 Specialized Financial AI Agents Workforce."""

from .base_agent import BaseFinancialAgent
from .capital_commander import capital_commander, CapitalCommander
from .revenue_commander import revenue_commander, RevenueCommander
from .treasury_commander import treasury_commander, TreasuryCommander
from .cfo_agent import cfo_agent, CFOAgent
from .compliance_agent import compliance_agent, ComplianceAgent
from .security_agent import security_agent, SecurityAgent
from .fx_agent import fx_agent, FXAgent
from .tax_research_agent import tax_research_agent, TaxResearchAgent
from .risk_agent import risk_agent, RiskAgent
from .debt_analyst import debt_analyst, DebtAnalyst
from .credit_monitor import credit_monitor, CreditMonitor
from .investment_research_agent import investment_research_agent, InvestmentResearchAgent
from .portfolio_analyst import portfolio_analyst, PortfolioAnalyst
from .capital_allocation_agent import capital_allocation_agent, CapitalAllocationAgent
from .market_agent import market_agent, MarketAgent
from .global_economics_agent import global_economics_agent, GlobalEconomicsAgent
from .audit_agent import audit_agent, AuditAgent
from .founder_chief_of_staff import founder_chief_of_staff, FounderChiefOfStaff

__all__ = [
    "BaseFinancialAgent",
    "capital_commander", "CapitalCommander",
    "revenue_commander", "RevenueCommander",
    "treasury_commander", "TreasuryCommander",
    "cfo_agent", "CFOAgent",
    "compliance_agent", "ComplianceAgent",
    "security_agent", "SecurityAgent",
    "fx_agent", "FXAgent",
    "tax_research_agent", "TaxResearchAgent",
    "risk_agent", "RiskAgent",
    "debt_analyst", "DebtAnalyst",
    "credit_monitor", "CreditMonitor",
    "investment_research_agent", "InvestmentResearchAgent",
    "portfolio_analyst", "PortfolioAnalyst",
    "capital_allocation_agent", "CapitalAllocationAgent",
    "market_agent", "MarketAgent",
    "global_economics_agent", "GlobalEconomicsAgent",
    "audit_agent", "AuditAgent",
    "founder_chief_of_staff", "FounderChiefOfStaff"
]
