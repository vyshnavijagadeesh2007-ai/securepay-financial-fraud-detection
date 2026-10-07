from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ClassDistribution(BaseModel):
    legitimate_count: int
    fraud_count: int
    fraud_percentage: float
    imbalance_ratio: str

class FeatureDescriptiveStats(BaseModel):
    mean: float
    std: float
    min: float
    q25: float
    median: float
    q75: float
    max: float

class AnalyticsSummaryResponse(BaseModel):
    dataset_name: str = "creditcard.csv"
    total_observations: int
    total_features: int
    feature_names: List[str]
    class_distribution: ClassDistribution
    amount_statistics: FeatureDescriptiveStats
    time_statistics: FeatureDescriptiveStats
    duplicates_count: int
    null_values_count: int
    pca_features_count: int
    pca_status: str = "COMPUTED_ON_DEMAND"
    status: str = "VERIFIED"
