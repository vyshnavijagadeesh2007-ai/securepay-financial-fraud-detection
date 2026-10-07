import tempfile
from pathlib import Path
import pytest
import numpy as np
import pandas as pd
from backend.ml.preprocessing.scaler import (
    TransactionPreprocessor,
    CANONICAL_FEATURES,
    PCA_FEATURES,
    TARGET_COLUMN
)


@pytest.fixture
def sample_transaction_df():
    """Generates synthetic dataframe matching creditcard.csv schema."""
    np.random.seed(42)
    n_samples = 25
    data = {
        "Time": np.linspace(0, 1000, n_samples),
        "Amount": np.random.exponential(scale=50, size=n_samples),
        "Class": np.random.choice([0, 1], size=n_samples, p=[0.9, 0.1])
    }
    for i in range(1, 29):
        data[f"V{i}"] = np.random.normal(0, 1, n_samples)
    return pd.DataFrame(data)


def test_preprocessor_initialization():
    preprocessor = TransactionPreprocessor()
    assert preprocessor.is_fitted is False
    assert len(preprocessor.feature_names) == 30
    assert preprocessor.scale_amount is True
    assert preprocessor.scale_time is True


def test_separate_target_exclusion(sample_transaction_df):
    features, target = TransactionPreprocessor.separate_target(sample_transaction_df)
    assert TARGET_COLUMN not in features.columns
    assert len(features.columns) == 30
    assert target is not None
    assert len(target) == len(sample_transaction_df)
    assert target.name == TARGET_COLUMN


def test_missing_required_columns_raises_error(sample_transaction_df):
    preprocessor = TransactionPreprocessor()
    # Drop one PCA feature
    incomplete_df = sample_transaction_df.drop(columns=["V14"])
    with pytest.raises(ValueError, match="missing 1 required feature"):
        preprocessor.fit(incomplete_df)

    # Fit a valid one first, then test transform with missing column
    preprocessor.fit(sample_transaction_df)
    with pytest.raises(ValueError, match="missing 1 required feature"):
        preprocessor.transform(incomplete_df)


def test_expected_feature_ordering(sample_transaction_df):
    preprocessor = TransactionPreprocessor()
    # Scramble column order
    scrambled_cols = list(sample_transaction_df.columns)
    np.random.shuffle(scrambled_cols)
    scrambled_df = sample_transaction_df[scrambled_cols]
    
    preprocessor.fit(scrambled_df)
    transformed = preprocessor.transform(scrambled_df)
    
    # Expected ordering must strictly be [Time, V1..V28, Amount]
    assert transformed.shape == (len(sample_transaction_df), 30)
    # Check that V1 matches column 1 in transformed array (since PCA features are not scaled)
    np.testing.assert_allclose(transformed[:, 1], sample_transaction_df["V1"].to_numpy())
    np.testing.assert_allclose(transformed[:, 28], sample_transaction_df["V28"].to_numpy())


def test_class_column_automatically_excluded_on_fit_and_transform(sample_transaction_df):
    preprocessor = TransactionPreprocessor()
    # sample_transaction_df contains 'Class'
    assert TARGET_COLUMN in sample_transaction_df.columns
    
    preprocessor.fit(sample_transaction_df)
    transformed = preprocessor.transform(sample_transaction_df)
    
    # Transformed must have exactly 30 features, not 31
    assert transformed.shape[1] == 30
    assert preprocessor.is_fitted is True


def test_scaler_fitting_and_transformation_shape(sample_transaction_df):
    preprocessor = TransactionPreprocessor()
    features_only = sample_transaction_df.drop(columns=["Class"])
    
    transformed = preprocessor.fit_transform(features_only)
    assert isinstance(transformed, np.ndarray)
    assert transformed.shape == (25, 30)
    assert transformed.dtype == np.float64
    assert preprocessor.amount_median_ is not None
    assert preprocessor.time_median_ is not None


def test_robust_scaler_mathematical_transformation():
    # Simple deterministic data to verify (x - median) / IQR
    data = {
        "Time": [10.0, 20.0, 30.0, 40.0, 50.0],
        "Amount": [10.0, 20.0, 30.0, 40.0, 50.0]
    }
    for i in range(1, 29):
        data[f"V{i}"] = [0.0] * 5
    df = pd.DataFrame(data)
    
    preprocessor = TransactionPreprocessor()
    transformed = preprocessor.fit_transform(df)
    
    # For [10, 20, 30, 40, 50]: median = 30.0, Q1 = 20.0, Q3 = 40.0, IQR = 20.0
    # Center value 30.0 should scale to 0.0
    # Time is col 0, Amount is col 29
    assert preprocessor.amount_median_ == 30.0
    assert preprocessor.amount_iqr_ == 20.0
    assert transformed[2, 0] == 0.0   # Time median scaled
    assert transformed[2, 29] == 0.0  # Amount median scaled
    assert transformed[0, 29] == (10.0 - 30.0) / 20.0  # -1.0
    assert transformed[4, 29] == (50.0 - 30.0) / 20.0  # 1.0


def test_unfitted_transform_raises_runtime_error(sample_transaction_df):
    preprocessor = TransactionPreprocessor()
    with pytest.raises(RuntimeError, match="has not been fitted yet"):
        preprocessor.transform(sample_transaction_df)


def test_dict_input_handling(sample_transaction_df):
    preprocessor = TransactionPreprocessor()
    preprocessor.fit(sample_transaction_df)
    
    # Single transaction dictionary (similar to API payload)
    single_tx = sample_transaction_df.iloc[0].to_dict()
    transformed_single = preprocessor.transform(single_tx)
    
    assert transformed_single.shape == (1, 30)
    assert isinstance(transformed_single, np.ndarray)


def test_serialization_roundtrip_with_joblib(sample_transaction_df):
    preprocessor = TransactionPreprocessor()
    preprocessor.fit(sample_transaction_df)
    original_transformed = preprocessor.transform(sample_transaction_df)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        artifact_path = Path(tmpdir) / "preprocessor.joblib"
        preprocessor.save(artifact_path)
        assert artifact_path.exists()
        
        loaded = TransactionPreprocessor.load(artifact_path)
        assert loaded.is_fitted is True
        loaded_transformed = loaded.transform(sample_transaction_df)
        
        np.testing.assert_allclose(original_transformed, loaded_transformed)
