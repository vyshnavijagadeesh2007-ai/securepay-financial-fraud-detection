from fastapi import APIRouter
from backend.app.schemas.analytics import AnalyticsSummaryResponse
from backend.app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/analytics", response_model=AnalyticsSummaryResponse, summary="Dataset Analytical Summary")
async def get_analytics():
    """
    Returns authentic dataset summary statistics (class distribution, skew,
    feature counts, time & amount quantiles) verified against data/creditcard.csv.
    """
    return AnalyticsService.get_dataset_summary()
