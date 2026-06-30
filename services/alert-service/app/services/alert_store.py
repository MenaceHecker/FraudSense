from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.enums import AlertStatus
from app.schemas.alert import AlertCreate, AlertStatusUpdate


class AlertStore:
    def serialize(self, alert: Alert) -> Dict:
        return {
            "id": str(alert.id),
            "transaction_id": str(alert.transaction_id),
            "user_id": alert.user_id,
            "amount": str(alert.amount),
            "risk_score": alert.risk_score,
            "severity": alert.severity.value,
            "ai_reason": alert.ai_reason,
            "recommended_action": alert.recommended_action.value,
            "status": alert.status.value,
            "analyst_notes": alert.analyst_notes,
            "created_at": alert.created_at,
            "resolved_at": alert.resolved_at,
        }

    def list_alerts(
        self,
        db: Session,
        status: Optional[str] = None,
        severity: Optional[str] = None,
    ) -> List[Dict]:
        stmt = select(Alert)

        if status:
            stmt = stmt.where(Alert.status == status)

        if severity:
            stmt = stmt.where(Alert.severity == severity)

        rows = db.execute(stmt.order_by(Alert.created_at.desc())).scalars().all()
        return [self.serialize(row) for row in rows]

    def get_alert(self, db: Session, alert_id: str) -> Optional[Dict]:
        row = db.get(Alert, UUID(alert_id))
        if not row:
            return None
        return self.serialize(row)

    def get_alerts_by_transaction(self, db: Session, transaction_id: str) -> List[Dict]:
        rows = (
            db.execute(
                select(Alert)
                .where(Alert.transaction_id == UUID(transaction_id))
                .order_by(Alert.created_at.desc())
            )
            .scalars()
            .all()
        )
        return [self.serialize(row) for row in rows]

    def create_alert(self, db: Session, payload: AlertCreate) -> Dict:
        alert = Alert(
            transaction_id=UUID(payload.transaction_id),
            user_id=payload.user_id,
            amount=payload.amount,
            risk_score=payload.risk_score,
            severity=payload.severity,
            ai_reason=payload.ai_reason,
            recommended_action=payload.recommended_action,
            status=AlertStatus.OPEN,
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)
        return self.serialize(alert)

    def update_status(
        self,
        db: Session,
        alert_id: str,
        payload: AlertStatusUpdate,
    ) -> Optional[Dict]:
        alert = db.get(Alert, UUID(alert_id))
        if not alert:
            return None

        alert.status = payload.status
        alert.analyst_notes = payload.analyst_notes

        if payload.status == AlertStatus.RESOLVED:
            alert.resolved_at = datetime.now(timezone.utc)
        else:
            alert.resolved_at = None

        db.commit()
        db.refresh(alert)
        return self.serialize(alert)

    def get_dashboard_stats(self, db: Session) -> Dict:
        stats_query = select(
            func.count(func.distinct(Alert.transaction_id)).label(
                "flagged_transactions"
            ),
            func.sum(case((Alert.severity == "high", 1), else_=0)).label(
                "high_severity_alerts"
            ),
            func.sum(case((Alert.severity == "medium", 1), else_=0)).label(
                "medium_severity_alerts"
            ),
            func.sum(case((Alert.status == "resolved", 1), else_=0)).label(
                "resolved_alerts"
            ),
        )
        result = db.execute(stats_query).first()

        stats = result._asdict() if result else {}
        flagged_transactions = stats.get("flagged_transactions") or 0

        # The alert-service only sees flagged transactions; the gateway overrides
        # total_transactions with the authoritative count from transaction-service.
        return {
            "total_transactions": flagged_transactions,
            "flagged_transactions": flagged_transactions,
            "high_severity_alerts": stats.get("high_severity_alerts") or 0,
            "medium_severity_alerts": stats.get("medium_severity_alerts") or 0,
            "resolved_alerts": stats.get("resolved_alerts") or 0,
        }


alert_store = AlertStore()