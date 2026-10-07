from typing import Optional, List
from pydantic import BaseModel

class MetricSummary(BaseModel):
    model_name: str
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    false_positives: Optional[int] = None
    false_negatives: Optional[int] = None
    true_positives: Optional[int] = None
    true_negatives: Optional[int] = None
    execution_time_seconds: Optional[float] = None
    detected_anomalies: Optional[int] = None
    contamination: Optional[float] = None
    status: str = "NOT_TRAINED"

class ModelComparisonResponse(BaseModel):
    models: List[MetricSummary]
    recommendation: Optional[str] = None
    status: str = "NOT_TRAINED"
    timestamp: Optional[str] = None

class ContaminationExperiment(BaseModel):
    contamination: float
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    detected_anomalies: Optional[int] = None

class ThresholdAnalysisResponse(BaseModel):
    selected_model: str
    optimal_threshold: Optional[float] = None
    default_threshold: Optional[float] = None
    contamination_experiments: List[ContaminationExperiment]
    pr_curve_points: Optional[List[dict]] = None
    operating_points: Optional[dict] = None
    pr_auc: Optional[float] = None
    status: str = "NOT_TRAINED"
