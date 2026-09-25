"""
OMNIMONEY OS: The Global Economic Opportunity, Income, Business, Deal, Career, AI, Capital & Ownership Intelligence System
"""

from .omnimoney_engine import OmniMoneyEngine, Opportunity, EconomicAction, calculate_opportunity_score
from .b2b_sales_engine import B2BSalesEngine, Prospect, LeadStatus
from .prospect_miner import ProspectMiner

__all__ = [
    "OmniMoneyEngine",
    "Opportunity",
    "EconomicAction",
    "calculate_opportunity_score",
    "B2BSalesEngine",
    "Prospect",
    "LeadStatus",
    "ProspectMiner",
]
