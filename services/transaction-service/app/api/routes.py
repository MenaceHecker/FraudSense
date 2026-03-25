from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.transaction import (
    TransactionCreate,
    TransactionListResponse,
    TransactionResponse,
)
from app.services.transaction_store import transaction_store

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "transaction-service"}


@router.get("/transactions", response_model=TransactionListResponse)
def list_transactions(
    flagged_only: bool = Query(default=False),
) -> TransactionListResponse:
    transactions = transaction_store.list_transactions(flagged_only=flagged_only)
    return TransactionListResponse(transactions=transactions, total=len(transactions))


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: str) -> TransactionResponse:
    transaction = transaction_store.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    return TransactionResponse(**transaction)


@router.get("/transactions/user/{user_id}", response_model=TransactionListResponse)
def get_transactions_by_user(user_id: str) -> TransactionListResponse:
    transactions = transaction_store.get_transactions_by_user(user_id)
    return TransactionListResponse(transactions=transactions, total=len(transactions))


@router.post(
    "/transactions",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_transaction(payload: TransactionCreate) -> TransactionResponse:
    transaction = transaction_store.create_transaction(payload)
    return TransactionResponse(**transaction)