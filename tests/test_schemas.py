from backend.app.schemas.dashboard import DashboardSummary
from backend.app.schemas.metrics import MetricSummary
from backend.app.schemas.prediction import PredictionResponse

def test_dashboard_schema_phase0_defaults():
    summary = DashboardSummary()
    # In Phase 0, all ML metrics must strictly default to None ('--')
    assert summary.precision is None
    assert summary.recall is None
    assert summary.f1_score is None
    assert summary.detected_anomalies is None
    assert summary.model_status == "NOT TRAINED"

def test_metric_summary_defaults():
    metric = MetricSummary(model_name="Isolation Forest")
    assert metric.precision is None
    assert metric.recall is None
    assert metric.f1_score is None
    assert metric.status == "NOT_TRAINED"

def test_prediction_response_phase0_contract():
    pred = PredictionResponse(
        model="Isolation Forest",
        anomaly_score=None,
        threshold=None,
        prediction=None,
        status="MODEL_NOT_TRAINED",
        message="Models have not yet been trained."
    )
    assert pred.status == "MODEL_NOT_TRAINED"
    assert pred.prediction is None
    assert pred.anomaly_score is None
