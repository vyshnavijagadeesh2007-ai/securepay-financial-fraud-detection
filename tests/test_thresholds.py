"""
Unit Tests for Phase 4 Dynamic Threshold Calibration & Operating Points
Validates threshold calibration protocol, validation-to-test integrity,
cost calculations, metric calculations, and artifact completeness.
"""

import pytest
import json
import numpy as np
import pandas as pd
from pathlib import Path
from backend.ml.evaluation.metrics import AnomalyEvaluator


@pytest.fixture(scope="module")
def threshold_artifacts():
    """Loads threshold calibration summary and operating points artifacts."""
    thresh_dir = Path("outputs/thresholds")
    op_path = thresh_dir / "selected_operating_points.json"
    cost_path = thresh_dir / "business_cost_analysis.json"
    if_sweep_path = thresh_dir / "isolation_forest_thresholds.csv"
    lof_sweep_path = thresh_dir / "lof_thresholds.csv"
    
    return {
        "operating_points": json.load(open(op_path)) if op_path.exists() else None,
        "business_cost": json.load(open(cost_path)) if cost_path.exists() else None,
        "if_sweep": pd.read_csv(if_sweep_path) if if_sweep_path.exists() else None,
        "lof_sweep": pd.read_csv(lof_sweep_path) if lof_sweep_path.exists() else None,
    }


def test_threshold_artifacts_exist(threshold_artifacts):
    """Verifies that all Phase 4 CSV and JSON threshold artifacts exist."""
    assert threshold_artifacts["operating_points"] is not None
    assert threshold_artifacts["business_cost"] is not None
    assert threshold_artifacts["if_sweep"] is not None
    assert threshold_artifacts["lof_sweep"] is not None
    assert len(threshold_artifacts["if_sweep"]) >= 100
    assert len(threshold_artifacts["lof_sweep"]) >= 100


def test_figures_exist():
    """Verifies that all 7 required Phase 4 figures are generated in outputs/figures/."""
    fig_dir = Path("outputs/figures")
    required_figures = [
        "validation_pr_curves.png",
        "validation_f1_threshold.png",
        "validation_precision_recall.png",
        "validation_fpr_recall.png",
        "validation_business_cost.png",
        "test_operating_points.png",
        "final_model_comparison.png"
    ]
    for fig_name in required_figures:
        fig_path = fig_dir / fig_name
        assert fig_path.exists(), f"Missing required figure: {fig_path}"
        assert fig_path.stat().st_size > 1000, f"Figure file too small: {fig_path}"


def test_operating_points_structure(threshold_artifacts):
    """Validates that all canonical operating modes are identified for both models."""
    op_data = threshold_artifacts["operating_points"]
    required_modes = ["low_false_alarm", "balanced", "high_recall", "low_fpr", "cost_optimal"]
    
    for model_key in ["isolation_forest", "local_outlier_factor"]:
        assert model_key in op_data
        val_points = op_data[model_key]["validation_selected_thresholds"]
        test_eval = op_data[model_key]["untouched_test_evaluation"]
        
        for mode in required_modes:
            assert mode in val_points
            assert "threshold" in val_points[mode]
            assert "val_precision" in val_points[mode]
            assert "val_recall" in val_points[mode]
            assert "val_f1" in val_points[mode]
            
            assert mode in test_eval
            # Exact threshold from validation must be used for test evaluation
            assert np.isclose(val_points[mode]["threshold"], test_eval[mode]["threshold"])


def test_test_evaluation_uses_exact_validation_thresholds(threshold_artifacts):
    """
    Critical Protocol Verification:
    Thresholds used to evaluate the test set must be identical to the validation-selected thresholds.
    Test set is evaluated once with fixed thresholds; test performance is not used to tune thresholds.
    """
    op_data = threshold_artifacts["operating_points"]
    for model_key in ["isolation_forest", "local_outlier_factor"]:
        val_thresh = op_data[model_key]["validation_selected_thresholds"]["balanced"]["threshold"]
        test_thresh = op_data[model_key]["untouched_test_evaluation"]["balanced"]["threshold"]
        assert val_thresh == test_thresh


def test_metric_and_cost_calculations_correctness():
    """Validates mathematical correctness of confusion matrix, precision, recall, F1, FPR, and cost."""
    # Synthetic ground truth & predictions
    y_true = np.array([1, 1, 0, 0, 0, 1, 0, 0, 0, 0])  # 3 positives, 7 negatives
    y_pred = np.array([1, 0, 1, 0, 0, 1, 0, 0, 0, 0])  # 2 TP, 1 FP, 1 FN, 6 TN
    
    metrics = AnomalyEvaluator.evaluate(y_true, y_pred)
    assert metrics["true_positives"] == 2
    assert metrics["false_positives"] == 1
    assert metrics["false_negatives"] == 1
    assert metrics["true_negatives"] == 6
    
    # Precision: 2 / (2 + 1) = 2/3 ≈ 0.666667
    assert np.isclose(metrics["precision"], 2/3)
    # Recall: 2 / (2 + 1) = 2/3 ≈ 0.666667
    assert np.isclose(metrics["recall"], 2/3)
    # F1: 2/3 ≈ 0.666667
    assert np.isclose(metrics["f1_score"], 2/3)
    # FPR: FP / (FP + TN) = 1 / (1 + 6) = 1/7 ≈ 0.142857
    assert np.isclose(metrics["false_positive_rate"], 1/7)
    
    # Cost check: FP*1 + FN*10 = 1*1 + 1*10 = 11
    cost_fp = 1.0
    cost_fn = 10.0
    total_cost = metrics["false_positives"] * cost_fp + metrics["false_negatives"] * cost_fn
    assert total_cost == 11.0


def test_business_cost_analysis_scenario_structure(threshold_artifacts):
    """Validates structure and calculations in business_cost_analysis.json."""
    cost_data = threshold_artifacts["business_cost"]
    assert "scenarios" in cost_data
    assert len(cost_data["scenarios"]) == 3
    
    for sc in cost_data["scenarios"]:
        assert "scenario" in sc
        assert "cost_fp" in sc
        assert "cost_fn" in sc
        assert "isolation_forest" in sc
        assert "local_outlier_factor" in sc
        assert sc["isolation_forest"]["test_cost"] > 0
        assert sc["local_outlier_factor"]["test_cost"] > 0


def test_continuous_scores_convention():
    """
    Verifies that continuous anomaly scores are used and higher score means more anomalous.
    Isolation Forest: score = -score_samples(X) (higher = more anomalous)
    Local Outlier Factor: score = -negative_outlier_factor_ (higher = more anomalous)
    """
    from backend.app.services.model_service import ModelService
    from backend.app.schemas.prediction import PredictionRequest
    from backend.app.models.domain import ModelName

    # Normal sample vs synthetic extreme outlier
    normal_req = PredictionRequest(
        transaction={
            "Time": 0.0, "Amount": 50.0,
            **{f"V{i}": 0.0 for i in range(1, 29)}
        },
        model=ModelName.ISOLATION_FOREST,
        operating_mode="balanced"
    )
    extreme_req = PredictionRequest(
        transaction={
            "Time": 0.0, "Amount": 10000.0,
            **{f"V{i}": 20.0 for i in range(1, 29)}  # Extreme perturbation
        },
        model=ModelName.ISOLATION_FOREST,
        operating_mode="balanced"
    )
    
    resp_normal = ModelService.predict(normal_req)
    resp_extreme = ModelService.predict(extreme_req)
    
    assert resp_normal.anomaly_score is not None
    assert resp_extreme.anomaly_score is not None
    # Higher score = more anomalous
    assert resp_extreme.anomaly_score > resp_normal.anomaly_score
    assert resp_extreme.is_anomaly is True


def test_api_operating_points_endpoint():
    """Verifies that the API exposes calibrated operating points and cost analysis."""
    from fastapi.testclient import TestClient
    from backend.app.main import app

    client = TestClient(app)
    response = client.get("/api/threshold/operating-points")
    assert response.status_code == 200
    data = response.json()
    assert "operating_points" in data
    assert "business_cost_analysis" in data
    assert "isolation_forest" in data["operating_points"]
    assert "local_outlier_factor" in data["operating_points"]
    
    # Check threshold endpoint with operating points
    resp_thresh = client.get("/api/threshold?model=Isolation Forest")
    assert resp_thresh.status_code == 200
    thresh_data = resp_thresh.json()
    assert thresh_data["operating_points"] is not None
    assert thresh_data["pr_auc"] is not None


def test_api_predict_with_operating_modes():
    """Verifies that /api/predict respects operating_mode and custom_threshold."""
    from fastapi.testclient import TestClient
    from backend.app.main import app

    client = TestClient(app)
    payload_balanced = {
        "transaction": {
            "Time": 406.0, "Amount": 149.62,
            **{f"V{i}": 0.0 for i in range(1, 29)}
        },
        "model": "Isolation Forest",
        "operating_mode": "balanced"
    }
    resp = client.post("/api/predict", json=payload_balanced)
    assert resp.status_code == 200
    data = resp.json()
    assert data["operating_mode"] == "balanced"
    assert data["threshold"] == pytest.approx(0.622447, abs=1e-4)

    payload_low_fa = {
        "transaction": {
            "Time": 406.0, "Amount": 149.62,
            **{f"V{i}": 0.0 for i in range(1, 29)}
        },
        "model": "Isolation Forest",
        "operating_mode": "low_false_alarm"
    }
    resp_fa = client.post("/api/predict", json=payload_low_fa)
    assert resp_fa.status_code == 200
    data_fa = resp_fa.json()
    assert data_fa["operating_mode"] == "low_false_alarm"
    assert data_fa["threshold"] == pytest.approx(0.672168, abs=1e-4)

