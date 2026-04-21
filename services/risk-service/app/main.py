from fastapi import FastAPI

from app.api.routes import router
from app.db.database import Base, engine
from app.models.risk_assessment import RiskAssessment  

app = FastAPI(
    title="FraudSense Risk Service",
    version="0.1.0",
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(router)