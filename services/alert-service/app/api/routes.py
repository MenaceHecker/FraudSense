from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.alert import (
    AlertCreate,
    AlertListResponse,
    AlertResponse,
    AlertStatusUpdate,
    DashboardStatsResponse,
)
from app.services.alert_store import alert_store

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "alert-service"}


@router.get("/alerts", response_model=AlertListResponse)
def list_alerts(
    status: Optional[str] = Query(default=None),
    severity: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> AlertListResponse:
    alerts = alert_store.list_alerts(db, status=status, severity=severity)
    return AlertListResponse(alerts=alerts, total=len(alerts))


@router.get("/alerts/{alert_id}", response_model=AlertResponse)
def get_alert(
    alert_id: str,
    db: Session = Depends(get_db),
) -> AlertResponse:
    alert = alert_store.get_alert(db, alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )
    return AlertResponse(**alert)


@router.get("/alerts/transaction/{transaction_id}", response_model=AlertListResponse)
def get_alerts_by_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
) -> AlertListResponse:
    alerts = alert_store.get_alerts_by_transaction(db, transaction_id)
    return AlertListResponse(alerts=alerts, total=len(alerts))


@router.post("/alerts", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(
    payload: AlertCreate,
    db: Session = Depends(get_db),
) -> AlertResponse:
    alert = alert_store.create_alert(db, payload)
    return AlertResponse(**alert)


@router.patch("/alerts/{alert_id}/status", response_model=AlertResponse)
def update_alert_status(
    alert_id: str,
    payload: AlertStatusUpdate,
    db: Session = Depends(get_db),
) -> AlertResponse:
    alert = alert_store.update_status(db, alert_id, payload)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found",
        )
    return AlertResponse(**alert)


@router.get("/stats/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    db: Session = Depends(get_db),
) -> DashboardStatsResponse:
    stats = alert_store.get_dashboard_stats(db)
    return DashboardStatsResponse(**stats)