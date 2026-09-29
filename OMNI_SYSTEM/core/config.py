"""
Global configuration settings for OMNI_SYSTEM.
Adheres strictly to Directives 85, 120, and Verified Profile constants.
"""

from pathlib import Path
from dataclasses import dataclass

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

@dataclass(frozen=True)
class OmniSettings:
    FOUNDER_NAME: str = "Aditya Mehra"
    FOUNDER_EMAIL: str = "adityamehra799@gmail.com"
    FOUNDER_PHONE: str = "+91 70034 56624"
    FOUNDER_LOCATION: str = "Bengaluru, India"
    FOUNDER_EDUCATION: str = "Dayananda Sagar University (DSU) BBA International Business '26"
    
    PRIMARY_UPI_ID: str = "adityamehra799@okhdfcbank"
    PRIMARY_BANK: str = "HDFC Bank Corporate Current Account"
    
    REVENUE_OS_PORT: int = 8765
    REVENUE_OS_URL: str = "http://127.0.0.1:8765"
    
    GLOBAL_CAPITAL_OS_PORT: int = 8766
    GLOBAL_CAPITAL_OS_URL: str = "http://127.0.0.1:8766"
    
    DAILY_TARGET_INR: float = 14500.0
    MONTHLY_RUN_RATE_INR: float = 435000.0
    ANNUAL_RUN_RATE_INR: float = 5220000.0
    
    ROOT_PATH: Path = ROOT_DIR
    DATA_PATH: Path = ROOT_DIR / "data"
    APPS_PATH: Path = ROOT_DIR / "apps"
    RESEARCH_PATH: Path = ROOT_DIR / "research"

settings = OmniSettings()
