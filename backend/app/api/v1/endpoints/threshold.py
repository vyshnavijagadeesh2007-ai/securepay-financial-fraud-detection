from fastapi import APIRouter, Query
from backend.app.schemas.metrics import ThresholdAnalysisResponse
from backend.app.services.model_service import ModelService
from backend.app.models.domain import ModelName

router = APIRouter()

@router.get("/threshold", response_model=ThresholdAnalysisResponse, summary="Threshold & Contamination Experiments")
async def get_threshold_analysis(
    model: ModelName = Query(
        default=ModelName.ISOLATION_FOREST,
        description="Target model for threshold and contamination experiments"
    )
):
    """
    Returns threshold calibration curves and contamination experiments.
    In Phase 4, includes dense validation sweep operating points and PR-AUC.
    """
    return ModelService.get_threshold_analysis(model)

@router.get("/threshold/operating-points", summary="Calibrated Operating Points & Cost Analysis")
async def get_operating_points():
    """
    Returns calibrated operating points selected on the validation partition
    and evaluated on the untouched test partition, including business cost analysis.
    """
    points = ModelService._load_operating_points()
    cost = ModelService._load_business_cost()
    return {
        "operating_points": points,
        "business_cost_analysis": cost
    }
