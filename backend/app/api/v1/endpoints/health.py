from fastapi import APIRouter
from backend.app.core.config import settings
from backend.app.services.model_service import ModelService
from backend.app.models.domain import ModelName, ModelStatus

router = APIRouter()

@router.get("/health", summary="System Health & Status")
async def health_check():
    dataset_exists = settings.DATA_PATH.exists()
    if_status = ModelService.get_model_status(ModelName.ISOLATION_FOREST)
    lof_status = ModelService.get_model_status(ModelName.LOCAL_OUTLIER_FACTOR)
    return {
        "status": "healthy",
        "phase": "Phase 4 (Threshold Calibration Complete)",
        "version": settings.VERSION,
        "dataset": {
            "path": str(settings.DATA_PATH.name),
            "exists": dataset_exists,
            "expected_rows": 284807 if dataset_exists else None
        },
        "ml_engine": {
            "isolation_forest_status": if_status.value,
            "lof_status": lof_status.value,
            "training_phase": (
                "Phase 4 (Threshold Calibration Complete)"
                if if_status == ModelStatus.READY and lof_status == ModelStatus.READY
                else "Phase 4 (Threshold Calibration)"
            )
        }
    }
