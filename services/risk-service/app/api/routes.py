from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.schemas.risk import RiskAssessmentResponse
from app.services.risk_store import risk_store
from app.services.transaction_client import fetch_transaction

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "risk-service"}


@router.get("/risk/{transaction_id}", response_model=RiskAssessmentResponse)
def get_risk_assessment(
    transaction_id: str,
    db: Session = Depends(get_db),
) -> RiskAssessmentResponse:
    assessment = risk_store.get(db, transaction_id)
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Risk assessment not found",
        )
    return RiskAssessmentResponse(**assessment)


@router.post("/risk/analyze/{transaction_id}", response_model=RiskAssessmentResponse)
async def analyze_transaction(
    transaction_id: str,
    db: Session = Depends(get_db),
) -> RiskAssessmentResponse:
    existing = risk_store.get(db, transaction_id)
    if existing:
        return RiskAssessmentResponse(**existing)

    transaction = await fetch_transaction(transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found in transaction-service",
        )

    assessment = risk_store.build_assessment(transaction)
    saved = risk_store.save(db, transaction_id, assessment)
    return RiskAssessmentResponse(**saved)