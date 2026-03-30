from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base, SessionLocal, engine
from app.db.seed import seed_transactions
from app.models.transaction import Transaction  # noqa: F401

app = FastAPI(
    title="FraudSense Transaction Service",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_transactions(db)
    finally:
        db.close()


app.include_router(router)