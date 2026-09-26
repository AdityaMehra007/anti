"""
System Configuration for REVENUE OS
Adheres strictly to the master specification:
- Single human founder: Aditya Mehra
- Base: India (INR primary accounting)
- Markets: India + Global Internet (INR, USD, EUR, GBP, AED, SGD)
- Zero unverified credentials, Least-Privilege architecture.
"""

from dataclasses import dataclass, field
from pathlib import Path
import os
from typing import Dict, List

ROOT_DIR = Path(__file__).resolve().parent.parent

@dataclass
class RevenueOSConfig:
    founder_name: str = "Aditya Mehra"
    base_country: str = "India"
    initial_market: str = "India + Global Internet"
    root_dir: Path = ROOT_DIR
    db_path: Path = ROOT_DIR / "database" / "revenue_os.db"
    
    # Supported Currencies (Directive 60)
    supported_currencies: List[str] = field(default_factory=lambda: [
        "INR", "USD", "EUR", "GBP", "AED", "SGD"
    ])
    
    # Base FX Rates (Normalized to 1 INR base)
    # 1 USD ~ 87.0 INR, 1 EUR ~ 92.0 INR, 1 GBP ~ 110.0 INR, 1 AED ~ 23.7 INR, 1 SGD ~ 65.0 INR
    fx_rates_to_inr: Dict[str, float] = field(default_factory=lambda: {
        "INR": 1.0,
        "USD": 87.0,
        "EUR": 92.0,
        "GBP": 110.0,
        "AED": 23.7,
        "SGD": 65.0,
    })
    
    # Operating Constraints (Directive 5 & Directive 14)
    require_human_approval_for_spend: bool = True
    max_autonomous_spend_usd: float = 0.0  # Zero autonomous spend allowed
    
    # Revenue Milestones (Directive 10)
    milestones: Dict[str, float] = field(default_factory=lambda: {
        "first_rupee": 1.0,
        "first_thousand": 1000.0,
        "first_ten_thousand": 10000.0,
        "first_lakh": 100000.0,
        "first_ten_lakh": 1000000.0,
        "first_crore_arr": 10000000.0,
        "first_global_10k_usd": 870000.0,      # $10,000 USD in INR
        "first_global_100k_usd_arr": 8700000.0, # $100,000 USD ARR in INR
    })
    
    # Server & Dashboard Settings
    dashboard_host: str = "127.0.0.1"
    dashboard_port: int = 8765

def get_config() -> RevenueOSConfig:
    """Return singleton system configuration instance."""
    return RevenueOSConfig()
