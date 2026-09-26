"""GLOBAL CAPITAL OS Configuration & System Parameters.

Codename: FOUNDER CAPITAL ENGINE
Base Jurisdiction: India (Bengaluru)
Operator / Founder: Aditya Mehra
"""

from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class SystemConfig(BaseSettings):
    # System Identity
    PROJECT_NAME: str = "GLOBAL CAPITAL OS"
    CODENAME: str = "FOUNDER CAPITAL ENGINE"
    FOUNDER_NAME: str = "Aditya Mehra"
    HOME_JURISDICTION: str = "India"
    BASE_CITY: str = "Bengaluru, India"
    
    # Financial Base Settings
    BASE_CURRENCY: str = "INR"
    SUPPORTED_CURRENCIES: list[str] = [
        "INR", "USD", "EUR", "GBP", "AED", "SGD", "JPY", "AUD"
    ]
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = Path("e:/anti/data")
    DB_PATH: Path = BASE_DIR / "global_capital.db"
    AUDIT_LOG_PATH: Path = BASE_DIR / "audit_trail.jsonl"
    
    # Security & Financial Controls
    MAX_UNAPPROVED_SPEND_INR: float = 0.0  # Zero unapproved autonomous money movement
    EMERGENCY_RESERVE_MONTHS: int = 6       # Minimum cash runway requirement
    DEFAULT_TAX_RESERVE_PCT: float = 0.18   # Blended GST / advance tax reservation
    DAILY_TRANSACTION_LIMIT_INR: float = 50000.0
    
    # Foreign Exchange Indicative Reference Rates (INR per unit)
    # Kept dynamically updatable by FX Engine
    DEFAULT_FX_RATES: dict[str, float] = {
        "INR": 1.0,
        "USD": 83.50,
        "EUR": 90.20,
        "GBP": 107.80,
        "AED": 22.75,
        "SGD": 62.50,
        "JPY": 0.58,
        "AUD": 55.40,
    }

    model_config = ConfigDict(arbitrary_types_allowed=True)

settings = SystemConfig()
