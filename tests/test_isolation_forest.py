import tempfile
from pathlib import Path
import pytest
import numpy as np

from backend.ml.isolation_forest.model import IsolationForestDetector
from backend.ml.evaluation.metrics import AnomalyEvaluator


@pytest.fixture
def synthetic_training_data():
    """Generates small synthetic normal cluster with 30 dimensions."""
    np.random.seed(42)
    # 200 normal samples centered at 0
    return np.random.normal(loc=0.0, scale=1.0, size=(200, 30))


@pytest.fixture
def synthetic_test_data():
    """Generates 50 normal samples and 10 extreme outliers."""
    np.random.seed(99)
    normal_samples = np.random.normal(loc=0.0, scale=1.0, size=(50, 30))
    # Extreme outliers shifted far away (+10.0 std)
    outlier_samples = np.random.normal(loc=10.0, scale=1.0, size=(10, 30))
    
    X_test = np.vstack([normal_samples, outlier_samples])
    y_test = np.array([0] * 50 + [1] * 10)
    return X_test, y_test


def test_model_initialization():
    detector = IsolationForestDetector(n_estimators=50, contamination=0.05, random_state=42)
    assert detector.is_fitted is False
    assert detector.model is None
    assert detector.n_estimators == 50
    assert detector.contamination == 0.05
    assert detector.offset_ is None


def test_model_training(synthetic_training_data):
    detector = IsolationForestDetector(n_estimators=50, contamination=0.05, random_state=42)
    detector.fit(synthetic_training_data)
    assert detector.is_fitted is True
    assert detector.model is not None
    assert detector.offset_ is not None
    assert isinstance(detector.offset_, float)


def test_binary_predictions_format(synthetic_training_data, synthetic_test_data):
    detector = IsolationForestDetector(n_estimators=50, contamination=0.05, random_state=42)
    detector.fit(synthetic_training_data)
    
    X_test, _ = synthetic_test_data
    preds = detector.predict(X_test)
    
    assert isinstance(preds, np.ndarray)
    assert preds.shape == (60,)
    # Predictions must be binary 0 (normal) or 1 (anomaly)
    unique_vals = set(np.unique(preds))
    assert unique_vals.issubset({0, 1})


def test_continuous_anomaly_scores_direction(synthetic_training_data, synthetic_test_data):
    detector = IsolationForestDetector(n_estimators=50, contamination=0.05, random_state=42)
    detector.fit(synthetic_training_data)
    
    X_test, _ = synthetic_test_data
    scores = detector.score_samples(X_test)
    
    assert isinstance(scores, np.ndarray)
    assert scores.shape == (60,)
    
    # Anomaly scoring convention in SecurePay AI: HIGHER = MORE ANOMALOUS
    # Mean score of outliers (rows 50-59) must be higher than mean score of normal points (rows 0-49)
    normal_scores = scores[:50]
    outlier_scores = scores[50:]
    assert outlier_scores.mean() > normal_scores.mean()


def test_feature_validation_rejects_invalid_dimensions():
    detector = IsolationForestDetector(n_estimators=50)
    # 1D array should fail
    with pytest.raises(ValueError, match="Expected 2D array"):
        detector.fit(np.array([1.0, 2.0, 3.0]))


def test_contamination_configuration(synthetic_training_data):
    det_low = IsolationForestDetector(n_estimators=50, contamination=0.01, random_state=42)
    det_high = IsolationForestDetector(n_estimators=50, contamination=0.10, random_state=42)
    
    det_low.fit(synthetic_training_data)
    det_high.fit(synthetic_training_data)
    
    assert det_low.contamination == 0.01
    assert det_high.contamination == 0.10
    # Higher contamination produces higher anomaly count
    preds_low = det_low.predict(synthetic_training_data)
    preds_high = det_high.predict(synthetic_training_data)
    assert np.sum(preds_high == 1) > np.sum(preds_low == 1)


def test_saved_model_loading_roundtrip(synthetic_training_data, synthetic_test_data):
    detector = IsolationForestDetector(n_estimators=50, contamination=0.05, random_state=42)
    detector.fit(synthetic_training_data)
    
    X_test, _ = synthetic_test_data
    orig_preds, orig_scores = detector.predict_with_scores(X_test)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        model_file = Path(tmpdir) / "test_iforest.joblib"
        detector.save(model_file)
        assert model_file.exists()
        
        loaded = IsolationForestDetector.load(model_file)
        assert loaded.is_fitted is True
        assert loaded.offset_ == detector.offset_
        
        loaded_preds, loaded_scores = loaded.predict_with_scores(X_test)
        np.testing.assert_array_equal(orig_preds, loaded_preds)
        np.testing.assert_allclose(orig_scores, loaded_scores)


def test_unfitted_methods_raise_runtime_error(synthetic_test_data):
    detector = IsolationForestDetector()
    X_test, _ = synthetic_test_data
    
    with pytest.raises(RuntimeError, match="has not been fitted"):
        detector.predict(X_test)
        
    with pytest.raises(RuntimeError, match="has not been fitted"):
        detector.score_samples(X_test)
        
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(RuntimeError, match="Cannot save unfitted"):
            detector.save(Path(tmpdir) / "model.joblib")


def test_anomaly_evaluator_metrics():
    # Deterministic test: 10 samples
    y_true = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
    y_pred = np.array([0, 0, 0, 0, 0, 0, 0, 1, 1, 0])
    
    # TP: 1 (idx 8)
    # FP: 1 (idx 7)
    # TN: 7 (idx 0-6)
    # FN: 1 (idx 9)
    res = AnomalyEvaluator.evaluate(y_true, y_pred)
    assert res["true_positives"] == 1
    assert res["false_positives"] == 1
    assert res["true_negatives"] == 7
    assert res["false_negatives"] == 1
    assert res["precision"] == 0.5
    assert res["recall"] == 0.5
    assert res["f1_score"] == 0.5
