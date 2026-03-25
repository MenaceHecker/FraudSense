from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import uuid4


class RiskStore:
    def __init__(self) -> None:
        self._assessments: Dict[str, Dict] = {}

    def get(self, transaction_id: str) -> Optional[Dict]:
        return self._assessments.get(transaction_id)

    def save(self, transaction_id: str, assessment: Dict) -> Dict:
        self._assessments[transaction_id] = assessment
        return assessment

    def build_assessment(self, transaction: Dict) -> Dict:
        amount = float(transaction["amount"])
        category = str(transaction["category"]).lower()
        flags = transaction.get("flags", [])
        rapid_repeat = bool(transaction.get("rapid_repeat", False))
        merchant = transaction.get("merchant", "Unknown merchant")

        score = 5
        key_signals = []

        if amount >= 5000:
            score += 35
            key_signals.append("HIGH_AMOUNT")
        elif amount >= 1000:
            score += 15
            key_signals.append("LARGE_PURCHASE")

        risky_categories = {"crypto", "gift_cards", "wire_transfer"}
        if category in risky_categories:
            score += 25
            key_signals.append("RISKY_CATEGORY")

        if rapid_repeat:
            score += 20
            key_signals.append("RAPID_REPEAT")

        if "ODD_HOUR" in flags:
            score += 10
            key_signals.append("ODD_HOUR")

        score = min(score, 100)

        if score >= 75:
            severity = "high"
            is_suspicious = True
            recommended_action = "block"
        elif score >= 45:
            severity = "medium"
            is_suspicious = True
            recommended_action = "review"
        else:
            severity = "low"
            is_suspicious = False
            recommended_action = "allow"

        if severity == "high":
            reason = (
                f"Transaction shows multiple fraud indicators, including elevated amount "
                f"and risky behavior patterns at merchant {merchant}."
            )
        elif severity == "medium":
            reason = (
                f"Transaction shows moderate fraud signals and should be reviewed before approval."
            )
        else:
            reason = (
                f"Transaction is within low-risk bounds based on current rules."
            )

        return {
            "id": str(uuid4()),
            "transaction_id": transaction["id"],
            "risk_score": score,
            "is_suspicious": is_suspicious,
            "severity": severity,
            "reason": reason,
            "recommended_action": recommended_action,
            "key_signals": sorted(list(set(key_signals))),
            "model_version": "rules-v1",
            "created_at": datetime.now(timezone.utc),
        }


risk_store = RiskStore()