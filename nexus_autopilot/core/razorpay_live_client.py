"""
NEXUS AUTOPILOT - Live Razorpay API Client & Webhook Verifier
Connects to https://api.razorpay.com/v1/payment_links to generate real payment links
and verifies HMAC-SHA256 webhook signatures.
"""
import os
import json
import base64
import hmac
import hashlib
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

class RazorpayLiveClient:
    def __init__(self, key_id: Optional[str] = None, key_secret: Optional[str] = None):
        self.key_id = key_id or os.getenv("RAZORPAY_KEY_ID", "rzp_test_DEMO_KEY")
        self.key_secret = key_secret or os.getenv("RAZORPAY_KEY_SECRET", "DEMO_SECRET")
        self.base_url = "https://api.razorpay.com/v1"

    def create_payment_link(
        self,
        invoice_id: str,
        amount_inr: float,
        customer_name: str,
        customer_phone: str,
        customer_email: str = "customer@example.com",
        description: str = "Tax Invoice Payment"
    ) -> Dict[str, Any]:
        """Creates a payment link via Razorpay API or provides authenticated sandbox simulation."""
        amount_paisa = int(amount_inr * 100)
        payload = {
            "amount": amount_paisa,
            "currency": "INR",
            "accept_partial": False,
            "description": f"{description} - {invoice_id}",
            "customer": {
                "name": customer_name,
                "contact": customer_phone,
                "email": customer_email
            },
            "notify": {
                "sms": True,
                "email": True
            },
            "reminder_enable": True,
            "notes": {
                "invoice_id": invoice_id,
                "platform": "NEXUS_AUTOPILOT"
            }
        }

        # If live keys are present (not default demo key), call Razorpay REST API
        if not self.key_id.startswith("rzp_test_DEMO"):
            try:
                auth_str = f"{self.key_id}:{self.key_secret}"
                auth_b64 = base64.b64encode(auth_str.encode()).decode()
                req = urllib.request.Request(
                    f"{self.base_url}/payment_links",
                    data=json.dumps(payload).encode('utf-8'),
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Basic {auth_b64}"
                    },
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode())
                    return {
                        "status": "SUCCESS_LIVE",
                        "payment_link_id": data.get("id"),
                        "short_url": data.get("short_url"),
                        "amount_inr": amount_inr,
                        "invoice_id": invoice_id
                    }
            except urllib.error.HTTPError as e:
                err_msg = e.read().decode()
                return {"status": "HTTP_ERROR", "code": e.code, "details": err_msg}
            except Exception as e:
                return {"status": "NETWORK_ERROR", "details": str(e)}

        # Deterministic test sandbox response
        return {
            "status": "SANDBOX_GENERATED",
            "payment_link_id": f"plink_test_{invoice_id.lower()}",
            "short_url": f"https://rzp.io/i/{invoice_id.lower()}_mock",
            "amount_inr": amount_inr,
            "invoice_id": invoice_id,
            "customer": customer_name,
            "upi_intent_ready": True
        }

    def verify_webhook_signature(self, body_bytes: bytes, received_signature: str, webhook_secret: str) -> bool:
        """Verifies Razorpay HMAC SHA256 Webhook signature."""
        expected_sig = hmac.new(webhook_secret.encode(), body_bytes, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected_sig, received_signature)

if __name__ == "__main__":
    client = RazorpayLiveClient()
    link = client.create_payment_link("INV-1001", 120000.0, "Ramesh Packaging Distributors", "+919876543210")
    print("[RAZORPAY CLIENT] Generated Link:\n", json.dumps(link, indent=2))
