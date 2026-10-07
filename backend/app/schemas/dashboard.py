from typing import Optional
from pydantic import BaseModel

class DashboardSummary(BaseModel):
    """
    High-level dashboard overview statistics.
    In Phase 0, ML performance metrics (precision, recall, f1) remain None ('--'),
    while dataset ground-truth statistics reflect the verified creditcard.csv properties.
    """
    total_transactions: Optional[int] = None
    legitimate_transactions: Optional[int] = None
    fraud_transactions: Optional[int] = None
    detected_anomalies: Optional[int] = None
    fraud_percentage: Optional[float] = None
    current_model: str = "Isolation Forest"
    model_status: str = "NOT TRAINED"
    precision: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
