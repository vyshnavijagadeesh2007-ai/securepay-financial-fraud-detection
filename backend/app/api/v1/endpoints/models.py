from fastapi import APIRouter
from backend.app.schemas.metrics import ModelComparisonResponse
from backend.app.services.model_service import ModelService
from backend.app.models.domain import ModelName, ModelStatus

router = APIRouter()

@router.get("/models", summary="List Available Anomaly Detection Models")
async def list_models():
    """
    Returns list of configured model architectures and current training readiness.
    """
    iforest_status = ModelService.get_model_status(ModelName.ISOLATION_FOREST)
    lof_status = ModelService.get_model_status(ModelName.LOCAL_OUTLIER_FACTOR)
    return {
        "models": [
            {
                "id": "isolation_forest",
                "name": ModelName.ISOLATION_FOREST.value,
                "type": "Unsupervised Tree-based Partitioning",
                "status": iforest_status.value,
                "target_phase": "Phase 2 (Trained)" if iforest_status == ModelStatus.READY else "Phase 2"
            },
            {
                "id": "lof",
                "name": ModelName.LOCAL_OUTLIER_FACTOR.value,
                "type": "Unsupervised Density-based k-NN",
                "status": lof_status.value,
                "target_phase": "Phase 3 (Trained)" if lof_status == ModelStatus.READY else "Phase 3"
            }
        ]
    }

@router.get("/models/comparison", response_model=ModelComparisonResponse, summary="Model Evaluation Comparison")
async def get_model_comparison():
    """
    Returns comparative evaluation metrics.
    In Phase 0, all performance metrics are None ('--').
    """
    return ModelService.get_comparison()
