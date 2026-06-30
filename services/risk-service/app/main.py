from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base, engine
from app.models.risk_assessment import RiskAssessment  # noqa: F401
from app.services.transaction_client import close_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield
    await close_client()


app = FastAPI(
    title="FraudSense Risk Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)