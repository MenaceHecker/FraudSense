from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.risk_assessment import RiskAssessment


class RiskStore:
    def serialize(self, assessment: RiskAssessment) -> Dict:
        return {
            "id": str(assessment.id),
            "transaction_id": str(assessment.transaction_id),
            "risk_score": assessment.risk_score,
            "is_suspicious": assessment.is_suspicious,
            "severity": assessment.severity,
            "reason": assessment.reason,
            "recommended_action": assessment.recommended_action,
            "key_signals": assessment.key_signals or [],
            "model_version": assessment.model_version,
            "created_at": assessment.created_at,
        }

    def get(self, db: Session, transaction_id: str) -> Optional[Dict]:
        row = (
            db.execute(
                select(RiskAssessment).where(
                    RiskAssessment.transaction_id == UUID(transaction_id)
                )
            )
            .scalars()
            .first()
        )
        if not row:
            return None
        return self.serialize(row)

    def save(self, db: Session, transaction_id: str, assessment: Dict) -> Dict:
        existing = (
            db.execute(
                select(RiskAssessment).where(
                    RiskAssessment.transaction_id == UUID(transaction_id)
                )
            )
            .scalars()
            .first()
        )

        if existing:
            existing.risk_score = assessment["risk_score"]
            existing.is_suspicious = assessment["is_suspicious"]
            existing.severity = assessment["severity"]
            existing.reason = assessment["reason"]
            existing.recommended_action = assessment["recommended_action"]
            existing.key_signals = assessment["key_signals"]
            existing.model_version = assessment["model_version"]
            db.commit()
            db.refresh(existing)
            return self.serialize(existing)

        row = RiskAssessment(
            transaction_id=UUID(transaction_id),
            risk_score=assessment["risk_score"],
            is_suspicious=assessment["is_suspicious"],
            severity=assessment["severity"],
            reason=assessment["reason"],
            recommended_action=assessment["recommended_action"],
            key_signals=assessment["key_signals"],
            model_version=assessment["model_version"],
            created_at=assessment["created_at"],
        )

        db.add(row)
        db.commit()
        db.refresh(row)
        return self.serialize(row)

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
            reason = "Transaction shows moderate fraud signals and should be reviewed before approval."
        else:
            reason = "Transaction is within low-risk bounds based on current rules."

        return {
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