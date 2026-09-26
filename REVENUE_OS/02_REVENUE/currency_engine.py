"""
Currency Engine for REVENUE OS
Adheres strictly to Directives 59, 60, 61.
Provides normalized FX conversions across INR, USD, EUR, GBP, AED, SGD.
"""

from typing import Dict

class CurrencyEngine:
    """
    Handles multi-currency conversions normalized to base INR.
    """
    # Normalized conversion factors (Value of 1 Unit of Currency in INR)
    FX_TO_INR: Dict[str, float] = {
        "INR": 1.0,
        "USD": 87.0,
        "EUR": 92.0,
        "GBP": 110.0,
        "AED": 23.7,
        "SGD": 65.0
    }

    def convert(self, amount: float, from_curr: str, to_curr: str) -> float:
        from_curr = from_curr.upper()
        to_curr = to_curr.upper()
        
        if from_curr not in self.FX_TO_INR:
            raise ValueError(f"Unsupported source currency: {from_curr}")
        if to_curr not in self.FX_TO_INR:
            raise ValueError(f"Unsupported target currency: {to_curr}")
            
        if from_curr == to_curr:
            return float(amount)
            
        # Convert from source to INR, then INR to target
        amount_in_inr = amount * self.FX_TO_INR[from_curr]
        target_amount = amount_in_inr / self.FX_TO_INR[to_curr]
        return round(target_amount, 2)

    def format_amount(self, amount: float, currency: str) -> str:
        currency = currency.upper()
        if currency == "INR":
            return f"₹{amount:,.2f}"
        elif currency == "USD":
            return f"${amount:,.2f}"
        elif currency == "EUR":
            return f"€{amount:,.2f}"
        elif currency == "GBP":
            return f"£{amount:,.2f}"
        elif currency == "AED":
            return f"AED {amount:,.2f}"
        elif currency == "SGD":
            return f"S${amount:,.2f}"
        return f"{amount:,.2f} {currency}"
