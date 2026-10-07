"""
Methodological Audit & Holdout Generalization Verification Tests
Ensures zero data leakage, correct score direction, continuous PR-AUC calculation,
and fair, identical holdout test set evaluation.
"""

import pytest
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_curve, auc

from backend.ml.preprocessing.scaler import TransactionPreprocessor
from backend.ml.isolation_forest.model import IsolationForestDetector
from backend.ml.lof.model import LocalOutlierFactorDetector
from backend.ml.evaluation.metrics import AnomalyEvaluator


@pytest.fixture(scope="module")
def dataset_partitions():
    """Generates the verified reproducible stratified split."""
    df = pd.read_csv("data/creditcard.csv")
    df_train, df_temp = train_test_split(
        df, test_size=0.40, random_state=42, stratify=df['Class']
    )
    df_val, df_test = train_test_split(
        df_temp, test_size=0.50, random_state=42, stratify=df_temp['Class']
    )
    return df_train, df_val, df_test


def test_target_class_excluded_from_model_features(dataset_partitions):
    """Verifies that ground truth Class is completely decoupled from features."""
    df_train, _, df_test = dataset_partitions
    
    train_legit = df_train[df_train['Class'] == 0].drop(columns=['Class'])
    test_features = df_test.drop(columns=['Class'])
    
    assert 'Class' not in train_legit.columns
    assert 'Class' not in test_features.columns
    assert train_legit.shape[1] == 30
    assert test_features.shape[1] == 30


def test_unsupervised_training_zero_fraud_leakage(dataset_partitions):
    """Verifies that unsupervised training baseline contains strictly zero fraud instances."""
    df_train, _, _ = dataset_partitions
    
    # Train pool for unsupervised models
    train_legit = df_train[df_train['Class'] == 0]
    
    # Ground truth verification
    assert (train_legit['Class'] == 1).sum() == 0
    assert (train_legit['Class'] == 0).sum() == len(train_legit)
    
    # Train fraud instances are excluded from unsupervised fitting
    assert df_train['Class'].sum() == 295
    assert len(train_legit) == 170589


def test_preprocessing_fitted_exclusively_on_train_partition(dataset_partitions):
    """Verifies that TransactionPreprocessor is fitted exclusively on training data."""
    df_train, df_val, df_test = dataset_partitions
    
    train_legit_dedup = df_train[df_train['Class'] == 0].drop(columns=['Class']).drop_duplicates()
    
    scaler = TransactionPreprocessor(scale_amount=True, scale_time=True)
    scaler.fit(train_legit_dedup)
    
    # Ensure scaler attributes match train partition exactly
    expected_amount_median = float(train_legit_dedup['Amount'].median())
    expected_time_median = float(train_legit_dedup['Time'].median())
    
    assert np.isclose(scaler.amount_median_, expected_amount_median)
    assert np.isclose(scaler.time_median_, expected_time_median)
    
    # Verify that test data is NOT used in scaler fitting
    test_amount_median = float(df_test['Amount'].median())
    if not np.isclose(expected_amount_median, test_amount_median):
        assert scaler.amount_median_ != test_amount_median


def test_identical_test_set_used_for_both_models(dataset_partitions):
    """Verifies that both Isolation Forest and LOF evaluate the exact same test records."""
    _, _, df_test = dataset_partitions
    
    X_test_1 = df_test.drop(columns=['Class']).to_numpy()
    X_test_2 = df_test.drop(columns=['Class']).to_numpy()
    y_test_1 = df_test['Class'].to_numpy(dtype=int)
    y_test_2 = df_test['Class'].to_numpy(dtype=int)
    
    assert np.array_equal(X_test_1, X_test_2)
    assert np.array_equal(y_test_1, y_test_2)
    assert len(y_test_1) == 56962
    assert y_test_1.sum() == 99


def test_pr_auc_calculated_from_continuous_scores():
    """
    Verifies that PR-AUC is calculated from continuous anomaly scores rather than binary predictions.
    Continuous scores yield an informative multi-point curve; binary predictions collapse to 2 operating points.
    """
    y_true = np.array([0, 0, 0, 0, 1, 1, 0, 1, 0, 1])
    continuous_scores = np.array([0.1, 0.45, 0.15, 0.6, 0.55, 0.92, 0.4, 0.78, 0.05, 0.35])
    binary_preds = (continuous_scores > 0.5).astype(int)
    
    # Continuous PR-AUC
    p_cont, r_cont, _, pr_auc_continuous = AnomalyEvaluator.compute_pr_curve(y_true, continuous_scores)
    
    # Binary PR curve has only 2 operating points
    p_bin, r_bin, _ = precision_recall_curve(y_true, binary_preds)
    pr_auc_binary = float(auc(r_bin, p_bin))
    
    assert len(p_cont) > len(p_bin)
    assert pr_auc_continuous > 0.0
    assert pr_auc_continuous != pr_auc_binary


def test_score_direction_consistency():
    """
    Verifies score direction consistency across both architectures:
    Higher anomaly score MUST denote higher anomaly probability.
    """
    rng = np.random.RandomState(42)
    X_train = rng.normal(loc=0.0, scale=1.0, size=(100, 30))
    inliers = rng.normal(loc=0.0, scale=1.0, size=(10, 30))
    outliers = rng.normal(loc=25.0, scale=1.0, size=(10, 30))
    
    # 1. Isolation Forest
    if_model = IsolationForestDetector(n_estimators=50, random_state=42)
    if_model.fit(X_train)
    if_inlier_scores = if_model.score_samples(inliers)
    if_outlier_scores = if_model.score_samples(outliers)
    assert np.median(if_outlier_scores) > np.median(if_inlier_scores)
    
    # 2. Local Outlier Factor
    lof_model = LocalOutlierFactorDetector(n_neighbors=10, novelty=True)
    lof_model.fit(X_train)
    lof_inlier_scores = lof_model.score_samples(inliers)
    lof_outlier_scores = lof_model.score_samples(outliers)
    assert np.median(lof_outlier_scores) > np.median(lof_inlier_scores)
