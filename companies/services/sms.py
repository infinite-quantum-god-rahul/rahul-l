from django.conf import settings

def send_sms(msisdn: str, text: str) -> bool:
    if not (getattr(settings, "SML_FEATURES", {}) or {}).get("SMS", False):
        return False
    # TODO: plug real SMS vendor
    print(f"[SMS] {msisdn}: {text}")
    return True
