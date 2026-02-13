import mercadopago
import requests
import os
import logging

logger = logging.getLogger(__name__)

# Hardcoded fallback for demo if env vars missing
MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN", "TEST-000000")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "TEST")
PAYPAL_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "TEST")
PAYPAL_MODE = os.getenv("PAYPAL_MODE", "sandbox")

class MercadoPagoGateway:
    def __init__(self):
        self.sdk = mercadopago.SDK(MP_ACCESS_TOKEN)

    def create_preference(self, items, payer, back_urls):
        preference_data = {
            "items": items,
            "payer": payer,
            "back_urls": back_urls,
            "auto_return": "approved",
        }
        try:
            result = self.sdk.preference().create(preference_data)
            if result["status"] == 201:
                return result["response"]
        except Exception as e:
            logger.error(f"MP Error: {e}")
        return None

class PayPalGateway:
    def __init__(self):
        self.base_url = "https://api-m.sandbox.paypal.com" if PAYPAL_MODE == "sandbox" else "https://api-m.paypal.com"

    def _get_token(self):
        auth = (PAYPAL_CLIENT_ID, PAYPAL_SECRET)
        resp = requests.post(f"{self.base_url}/v1/oauth2/token", auth=auth, data={"grant_type": "client_credentials"})
        return resp.json().get("access_token") if resp.status_code == 200 else None

    def create_order(self, amount, currency="USD", return_url="", cancel_url=""):
        token = self._get_token()
        if not token: return None
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        json_data = {
            "intent": "CAPTURE",
            "purchase_units": [{"amount": {"currency_code": currency, "value": str(amount)}}],
            "application_context": {"return_url": return_url, "cancel_url": cancel_url}
        }
        resp = requests.post(f"{self.base_url}/v2/checkout/orders", json=json_data, headers=headers)
        return resp.json() if resp.status_code == 201 else None