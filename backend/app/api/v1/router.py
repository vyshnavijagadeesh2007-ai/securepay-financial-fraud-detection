from fastapi import APIRouter
from backend.app.api.v1.endpoints import (
    health,
    dashboard,
    analytics,
    models,
    threshold,
    transactions
)

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(dashboard.router, tags=["Dashboard"])
api_router.include_router(analytics.router, tags=["Analytics"])
api_router.include_router(models.router, tags=["Models"])
api_router.include_router(threshold.router, tags=["Threshold & Contamination"])
api_router.include_router(transactions.router, tags=["Transactions & Inference"])
