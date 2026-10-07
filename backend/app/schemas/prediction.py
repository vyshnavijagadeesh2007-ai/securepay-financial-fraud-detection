from typing import Optional, List
from pydantic import BaseModel, Field
from backend.app.schemas.transaction import TransactionInput
from backend.app.models.domain import ModelName

class PredictionRequest(BaseModel):
    transaction: TransactionInput
    model: ModelName = Field(
        default=ModelName.ISOLATION_FOREST,
        description="Select unsupervised anomaly detection algorithm"
    )
    custom_threshold: Optional[float] = Field(
        default=None,
        description="Optional calibrated score cutoff for anomaly boundary"
    )
    operating_mode: Optional[str] = Field(
        default="balanced",
        description="Calibrated operating mode: 'balanced', 'low_false_alarm', 'high_recall', 'low_fpr', 'cost_optimal', or 'custom'"
    )

class PredictionResponse(BaseModel):
    """
    Contract for real-time anomaly inference with dynamic threshold calibration.
    """
    model: str
    anomaly_score: Optional[float] = None
    score: Optional[float] = None
    threshold: Optional[float] = None
    prediction: Optional[int] = None  # 0: Legitimate, 1: Anomaly
    status: str  # NORMAL, POTENTIAL ANOMALY, or MODEL_NOT_TRAINED
    is_anomaly: Optional[bool] = None
    operating_point: Optional[str] = None
    operating_mode: Optional[str] = None
    execution_time_ms: Optional[float] = None
    message: Optional[str] = None

class BatchPredictionRequest(BaseModel):
    transactions: List[TransactionInput]
    model: ModelName = ModelName.ISOLATION_FOREST

class BatchPredictionResponse(BaseModel):
    model: str
    total_processed: int
    predictions: List[PredictionResponse]
    status: str
