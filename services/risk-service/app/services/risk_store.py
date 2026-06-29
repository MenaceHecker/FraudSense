from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.risk_assessment import RiskAssessment
from app.models.enums import RecommendedAction, Severity
from app.services.risk_config import DEFAULT_RISK_CONFIG, RiskConfig


class RiskStore:
    def serialize(self, assessment: RiskAssessment) -> Dict:
        return {
            "id": str(assessment.id),
            "transaction_id": str(assessment.transaction_id),
            "risk_score": assessment.risk_score,
            "is_suspicious": assessment.is_suspicious,
            "severity": assessment.severity.value,
            "reason": assessment.reason,
            "recommended_action": assessment.recommended_action.value,
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

    def build_assessment(
        self, transaction: Dict, config: RiskConfig = DEFAULT_RISK_CONFIG
    ) -> Dict:
        amount = float(transaction["amount"])
        category = str(transaction["category"]).lower()
        flags = transaction.get("flags", [])
        rapid_repeat = bool(transaction.get("rapid_repeat", False))
        merchant = transaction.get("merchant", "Unknown merchant")

        score = config["initial_score"]
        key_signals: List[str] = []

        # Sort thresholds from high to low to ensure we only apply the highest one
        for th in sorted(
            config["amount_thresholds"], key=lambda x: x["threshold"], reverse=True
        ):
            if amount >= th["threshold"]:
                score += th["component"]["score"]
                key_signals.append(th["component"]["key_signal"])
                break  # Only apply the first (highest) threshold met

        if category in config["risky_categories"]:
            component = config["risky_categories"][category]
            score += component["score"]
            key_signals.append(component["key_signal"])

        if rapid_repeat:
            score += config["rapid_repeat"]["score"]
            key_signals.append(config["rapid_repeat"]["key_signal"])

        if "ODD_HOUR" in flags:
            score += config["odd_hour"]["score"]
            key_signals.append(config["odd_hour"]["key_signal"])

        score = min(score, 100)

        if score >= 75:
            severity = Severity.HIGH
            is_suspicious = True
            recommended_action = RecommendedAction.BLOCK
        elif score >= 45:
            severity = Severity.MEDIUM
            is_suspicious = True
            recommended_action = RecommendedAction.REVIEW
        else:
            severity = Severity.LOW
            is_suspicious = False
            recommended_action = RecommendedAction.ALLOW

        if severity == Severity.HIGH:
            reason = (
                f"Transaction shows multiple fraud indicators, including elevated amount "
                f"and risky behavior patterns at merchant {merchant}."
            )
        elif severity == Severity.MEDIUM:
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