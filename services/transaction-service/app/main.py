from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base, SessionLocal, engine
from app.db.seed import seed_transactions
from app.models.transaction import Transaction  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_transactions(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="FraudSense Transaction Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)