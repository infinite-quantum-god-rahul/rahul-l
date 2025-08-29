# companies/services/credit_bureau.py
import json
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, Tuple, Optional
from django.conf import settings

@dataclass
class BureauResponse:
    ok: bool
    score: Optional[int]
    raw: Dict[str, Any]
    provider: str
    message: str = ""

class CreditBureauClient:
    """
    Non-blocking stub client.
    - Preserves contract: never raises, always returns BureauResponse.
    - Feature flag: settings.SML_FEATURES["CREDIT_BUREAU"].
    - Provider config: settings.SML_CREDIT_BUREAU = {
          "PROVIDER": "CIBIL" | "EXPERIAN" | "CRIF" | "EQUIFAX",
          "CIBIL":    {"API_KEY": "...", "ENDPOINT": "...", "LATENCY_MS": 200},
          ...
      }
    - If API_KEY missing or feature OFF → simulated deterministic score.
    """
    def __init__(self) -> None:
        self.flags = getattr(settings, "SML_FEATURES", {}) or {}
        self.cfg = getattr(settings, "SML_CREDIT_BUREAU", {}) or {}
        self.provider = (self.cfg.get("PROVIDER") or "CIBIL").upper()

    # ── helpers ─────────────────────────────────────────────────────
    def enabled(self) -> bool:
        return bool(self.flags.get("CREDIT_BUREAU", False))

    def _provider_cfg(self) -> Tuple[str, Dict[str, Any]]:
        return self.provider, (self.cfg.get(self.provider, {}) or {})

    @staticmethod
    def _mask_pan(pan: str) -> str:
        s = (pan or "").strip().upper()
        if len(s) >= 10:
            return f"{s[:2]}***{s[-3:]}"
        return "***" if s else ""

    @staticmethod
    def _mask_aadhar(aadhar: str) -> str:
        digits = re.sub(r"\D+", "", aadhar or "")
        if len(digits) >= 4:
            return f"**** **** **{digits[-4:]}"
        return "************" if digits else ""

    @staticmethod
    def _norm_inputs(pan: str, aadhar: str, name: str, dob: str) -> Tuple[str, str, str, str]:
        pan_n = (pan or "").strip().upper()
        aadhar_n = re.sub(r"\D+", "", aadhar or "")
        name_n = re.sub(r"\s+", " ", (name or "").strip().upper())
        dob_n = (dob or "").strip()
        return pan_n, aadhar_n, name_n, dob_n

    @staticmethod
    def _stable_score(*parts: str, base: int = 300, span: int = 601) -> int:
        """Deterministic 300–900 score based on inputs."""
        seed = hash(tuple(parts))
        return base + abs(seed) % span

    # ── API ─────────────────────────────────────────────────────────
    def pull_score(self, *, pan: str = "", aadhar: str = "", name: str = "", dob: str = "") -> BureauResponse:
        """
        Stub implementation:
        - If feature OFF: ok=True, score=None, raw explains off.
        - If no API_KEY: ok=True, score from stable hash. Non-blocking.
        - With API_KEY: returns mocked provider response after small latency.
        - Never raises: wraps all errors into ok=False with message.
        """
        prov, pcfg = self._provider_cfg()
        pan_n, aadhar_n, name_n, dob_n = self._norm_inputs(pan, aadhar, name, dob)
        masked = {"pan": self._mask_pan(pan_n), "aadhar": self._mask_aadhar(aadhar_n)}

        if not self.enabled():
            return BureauResponse(
                ok=True,
                score=None,
                raw={"note": "feature_off", "provider": prov, "ids": masked},
                provider=prov,
                message="Credit bureau feature is OFF",
            )

        api_key = (pcfg.get("API_KEY") or "").strip()
        latency_ms = int((pcfg.get("LATENCY_MS") or 200) or 0)

        # No credentials → deterministic simulated score
        if not api_key:
            score = self._stable_score(prov, pan_n, aadhar_n, name_n, dob_n)
            return BureauResponse(
                ok=True,
                score=score,
                raw={"simulated": True, "provider": prov, "ids": masked},
                provider=prov,
                message="Simulated score (no API key)",
            )

        # Mocked real call path (keeps flows intact, time-bounded)
        try:
            time.sleep(max(0, min(latency_ms, 1000)) / 1000.0)
            # provider-specific shaping could go here
            payload = {
                "provider": prov,
                "endpoint": pcfg.get("ENDPOINT", "mock://credit-bureau"),
                "request": {"name": name_n, "dob": dob_n, "ids": masked},
                "response": {"score": 720, "band": "GOOD", "mock": True},
            }
            return BureauResponse(
                ok=True,
                score=payload["response"]["score"],
                raw=payload,
                provider=prov,
                message="Mocked provider response",
            )
        except Exception as e:
            return BureauResponse(
                ok=False,
                score=None,
                raw={"error": str(e), "provider": prov, "ids": masked},
                provider=prov,
                message="Provider error",
            )
