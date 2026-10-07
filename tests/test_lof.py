"""
Unit Tests for Local Outlier Factor (LOF) Subsystem
Validates initialization, training, scoring direction, predictions, and serialization.
"""

import pytest
import numpy as np
from pathlib import Path
from backend.ml.lof.model import LocalOutlierFactorDetector


@pytest.fixture
def synthetic_data():
    """Generates synthetic normal baseline and controlled anomalies."""
    rng = np.random.RandomState(42)
    # Dense cluster of normal instances
    X_normal = rng.normal(loc=0.0, scale=1.0, size=(200, 30))
    # Extreme outliers placed far from normal cluster
    X_outliers = rng.normal(loc=20.0, scale=1.0, size=(10, 30))
    return X_normal, X_outliers


def test_lof_initialization():
    """Validates default initialization parameters."""
    detector = LocalOutlierFactorDetector(
        n_neighbors=20,
        contamination=0.002,
        novelty=True
    )
    assert detector.n_neighbors == 20
    assert detector.contamination == 0.002
    assert detector.novelty is True
    assert detector.is_fitted is False
    assert detector.model is None


def test_lof_requires_novelty():
    """Validates that novelty=False raises ValueError."""
    with pytest.raises(ValueError, match="novelty=True"):
        LocalOutlierFactorDetector(novelty=False)


def test_lof_training_synthetic(synthetic_data):
    """Validates fitting on valid 2D array."""
    X_normal, _ = synthetic_data
    detector = LocalOutlierFactorDetector(n_neighbors=15, contamination=0.05)
    detector.fit(X_normal)
    
    assert detector.is_fitted is True
    assert detector.model is not None
    assert detector.offset_ is not None
    assert detector.threshold_ is not None
    assert np.isclose(detector.threshold_, -detector.offset_)


def test_lof_prediction_and_score_shape(synthetic_data):
    """Validates shape and dtype of predictions and anomaly scores."""
    X_normal, X_outliers = synthetic_data
    detector = LocalOutlierFactorDetector(n_neighbors=15, contamination=0.05)
    detector.fit(X_normal)
    
    X_eval = np.vstack([X_normal[:20], X_outliers])
    preds = detector.predict(X_eval)
    scores = detector.score_samples(X_eval)
    
    assert preds.shape == (30,)
    assert preds.dtype in [np.int32, np.int64, int]
    assert set(np.unique(preds)).issubset({0, 1})
    
    assert scores.shape == (30,)
    assert scores.dtype in [np.float32, np.float64, float]


def test_lof_scoring_direction(synthetic_data):
    """
    Validates standardized scoring convention:
    Higher anomaly score MUST denote higher abnormality.
    Extreme outliers must receive higher anomaly scores than inliers.
    """
    X_normal, X_outliers = synthetic_data
    detector = LocalOutlierFactorDetector(n_neighbors=15, contamination=0.05)
    detector.fit(X_normal)
    
    scores_normal = detector.score_samples(X_normal[:50])
    scores_outliers = detector.score_samples(X_outliers)
    
    # Median outlier score must be substantially higher than inlier score
    assert np.median(scores_outliers) > np.median(scores_normal)


def test_lof_binary_prediction_behavior(synthetic_data):
    """Validates that distant outliers are detected as anomalies (1)."""
    X_normal, X_outliers = synthetic_data
    detector = LocalOutlierFactorDetector(n_neighbors=15, contamination=0.05)
    detector.fit(X_normal)
    
    preds_outliers = detector.predict(X_outliers)
    # At least 80% of extreme outliers should be flagged as anomaly (1)
    assert np.mean(preds_outliers == 1) >= 0.8


def test_lof_predict_with_scores(synthetic_data):
    """Validates combined predict_with_scores convenience method."""
    X_normal, _ = synthetic_data
    detector = LocalOutlierFactorDetector(n_neighbors=15, contamination=0.05)
    detector.fit(X_normal)
    
    preds, scores = detector.predict_with_scores(X_normal[:10])
    direct_preds = detector.predict(X_normal[:10])
    direct_scores = detector.score_samples(X_normal[:10])
    
    assert np.array_equal(preds, direct_preds)
    assert np.allclose(scores, direct_scores)


def test_lof_invalid_input_handling(synthetic_data):
    """Validates proper error raising on unfitted calls or bad dimensions."""
    X_normal, _ = synthetic_data
    detector = LocalOutlierFactorDetector(n_neighbors=15)
    
    # Must raise RuntimeError if called prior to fitting
    with pytest.raises(RuntimeError, match="has not been fitted"):
        detector.predict(X_normal)
        
    with pytest.raises(RuntimeError, match="has not been fitted"):
        detector.score_samples(X_normal)
        
    # Must raise ValueError on 1D input
    with pytest.raises(ValueError, match="Expected 2D array"):
        detector.fit(np.array([1.0, 2.0, 3.0]))


def test_lof_serialization_roundtrip(synthetic_data, tmp_path):
    """Validates joblib save and load persistence and numerical fidelity."""
    X_normal, X_outliers = synthetic_data
    detector = LocalOutlierFactorDetector(n_neighbors=15, contamination=0.05)
    detector.fit(X_normal)
    
    save_file = tmp_path / "test_lof.joblib"
    detector.save(save_file)
    assert save_file.exists()
    
    loaded = LocalOutlierFactorDetector.load(save_file)
    assert loaded.is_fitted is True
    assert loaded.n_neighbors == detector.n_neighbors
    assert np.isclose(loaded.offset_, detector.offset_)
    
    test_sample = X_outliers[:5]
    orig_preds, orig_scores = detector.predict_with_scores(test_sample)
    loaded_preds, loaded_scores = loaded.predict_with_scores(test_sample)
    
    assert np.array_equal(orig_preds, loaded_preds)
    assert np.allclose(orig_scores, loaded_scores)


def test_lof_get_params():
    """Validates get_params dictionary."""
    detector = LocalOutlierFactorDetector(n_neighbors=25, contamination=0.005)
    params = detector.get_params()
    assert params["n_neighbors"] == 25
    assert params["contamination"] == 0.005
    assert params["novelty"] is True
    assert params["is_fitted"] is False
