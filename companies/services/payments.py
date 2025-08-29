from django.conf import settings

class PaymentGateway:
    def __init__(self):
        self.cfg = getattr(settings, "SML_PAYMENT", {}) or {}

    def create_order(self, amount_paise: int, receipt: str) -> dict:
        # TODO: integrate Razorpay/Paytm
        return {"id": f"order_{receipt}", "amount": amount_paise}

    def capture(self, payment_id: str, amount_paise: int) -> dict:
        return {"id": payment_id, "captured": True}

    def verify_webhook(self, payload: bytes, signature: str) -> bool:
        return True  # replace with HMAC verification
