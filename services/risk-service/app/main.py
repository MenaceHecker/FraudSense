from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base, engine
from app.models.risk_assessment import RiskAssessment
from app.services.transaction_client import close_client

app = FastAPI(
    title="FraudSense Risk Service",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await close_client()


app.include_router(router)