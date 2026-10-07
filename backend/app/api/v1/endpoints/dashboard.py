from fastapi import APIRouter
from backend.app.schemas.dashboard import DashboardSummary
from backend.app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/dashboard", response_model=DashboardSummary, summary="Dashboard Overview Statistics")
async def get_dashboard():
    """
    Returns high-level statistics for the dashboard view.
    In Phase 0, dataset ground-truth attributes are derived from creditcard.csv,
    while ML model evaluation metrics (precision, recall, f1) remain None ('--').
    """
    return AnalyticsService.get_dashboard_summary()
