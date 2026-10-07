"""
Preprocessing Subsystem for SecurePay AI
Handles robust feature scaling on Time and Amount features, leaving PCA features V1-V28 intact.
Ensures zero data leakage by decoupling target variable 'Class' from model features.
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union, Any
import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler
import joblib

# Canonical 30 input features in standardized ordering
PCA_FEATURES: List[str] = [f"V{i}" for i in range(1, 29)]
CANONICAL_FEATURES: List[str] = ["Time"] + PCA_FEATURES + ["Amount"]
TARGET_COLUMN: str = "Class"


class TransactionPreprocessor:
    """
    RobustScaler Pipeline Interface for Financial Transaction Data.
    
    Architectural & Methodological Specifications:
    - Target Isolation: 'Class' is strictly decoupled and never permitted in the feature space.
    - Outlier-Resistant Scaling: Applies RobustScaler (median & IQR) to 'Amount' and 'Time'.
      Formula: x' = (x - median(x)) / IQR(x)
    - PCA Passthrough: V1 through V28 are already orthogonal, zero-centered PCA components
      and are preserved without redundant transformation.
    - Feature Ordering: Enforces consistent 30-dimensional vector ordering:
      [Time, V1, V2, ..., V28, Amount].
    - Serialization: Fully serializable to disk via joblib for production deployment.
    """

    def __init__(
        self,
        scale_amount: bool = True,
        scale_time: bool = True
    ):
        self.scale_amount = scale_amount
        self.scale_time = scale_time
        
        self.amount_scaler: Optional[RobustScaler] = RobustScaler() if scale_amount else None
        self.time_scaler: Optional[RobustScaler] = RobustScaler() if scale_time else None
        
        self.feature_names: List[str] = list(CANONICAL_FEATURES)
        self.is_fitted: bool = False
        
        # Stored metadata from fitting
        self.amount_median_: Optional[float] = None
        self.amount_iqr_: Optional[float] = None
        self.time_median_: Optional[float] = None
        self.time_iqr_: Optional[float] = None

    @staticmethod
    def separate_target(df: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[pd.Series]]:
        """
        Safely decouples feature attributes from the ground-truth target.
        Guarantees that 'Class' is excluded from input feature matrices to prevent data leakage.
        
        Args:
            df: Input DataFrame containing transaction records.
            
        Returns:
            Tuple of (features_df, target_series_or_none)
        """
        if TARGET_COLUMN in df.columns:
            target = df[TARGET_COLUMN].copy()
            features = df.drop(columns=[TARGET_COLUMN]).copy()
            return features, target
        return df.copy(), None

    def _validate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Validates presence of all 30 canonical features and enforces canonical ordering.
        """
        missing_cols = [col for col in self.feature_names if col not in df.columns]
        if missing_cols:
            raise ValueError(
                f"Input data is missing {len(missing_cols)} required feature(s): {missing_cols}"
            )
        # Return dataframe strictly in canonical column order
        return df[self.feature_names].copy()

    def fit(self, X: Union[pd.DataFrame, np.ndarray, List[Dict[str, Any]]]) -> "TransactionPreprocessor":
        """
        Fits RobustScaler parameters (median and IQR) on training data.
        In the SecurePay AI paradigm, this MUST be fitted strictly on the
        normal baseline partition (Class == 0) to prevent evaluation leakage.
        
        Args:
            X: Input dataset (DataFrame, 2D ndarray, or list of dicts).
            
        Returns:
            self
        """
        if isinstance(X, list):
            X = pd.DataFrame(X)

        if isinstance(X, pd.DataFrame):
            # Ensure target is stripped if present
            if TARGET_COLUMN in X.columns:
                X = X.drop(columns=[TARGET_COLUMN])
            X_df = self._validate_columns(X)
            
            if self.scale_amount and self.amount_scaler is not None:
                self.amount_scaler.fit(X_df[["Amount"]].to_numpy(dtype=np.float64))
                self.amount_median_ = float(self.amount_scaler.center_[0])
                self.amount_iqr_ = float(self.amount_scaler.scale_[0])
                
            if self.scale_time and self.time_scaler is not None:
                self.time_scaler.fit(X_df[["Time"]].to_numpy(dtype=np.float64))
                self.time_median_ = float(self.time_scaler.center_[0])
                self.time_iqr_ = float(self.time_scaler.scale_[0])
                
        elif isinstance(X, np.ndarray):
            if X.ndim != 2 or X.shape[1] != len(self.feature_names):
                raise ValueError(
                    f"Expected 2D numpy array with {len(self.feature_names)} features, got shape {X.shape}"
                )
            # Column 0 is Time, Column 29 is Amount
            time_col = X[:, [0]]
            amount_col = X[:, [-1]]
            
            if self.scale_amount and self.amount_scaler is not None:
                self.amount_scaler.fit(amount_col)
                self.amount_median_ = float(self.amount_scaler.center_[0])
                self.amount_iqr_ = float(self.amount_scaler.scale_[0])
                
            if self.scale_time and self.time_scaler is not None:
                self.time_scaler.fit(time_col)
                self.time_median_ = float(self.time_scaler.center_[0])
                self.time_iqr_ = float(self.time_scaler.scale_[0])
        else:
            raise TypeError(f"Unsupported data type for fitting: {type(X)}")

        self.is_fitted = True
        return self

    def transform(self, X: Union[pd.DataFrame, np.ndarray, Dict[str, Any], List[Dict[str, Any]]]) -> np.ndarray:
        """
        Transforms input transaction data into a normalized 2D numpy array.
        
        Args:
            X: Input transaction records (DataFrame, ndarray, single dict, or list of dicts).
            
        Returns:
            np.ndarray of shape (N, 30) with dtype float64.
        """
        if not self.is_fitted:
            raise RuntimeError(
                "TransactionPreprocessor has not been fitted yet. Call 'fit' before 'transform'."
            )

        # Handle single dictionary (e.g. from real-time API endpoint)
        if isinstance(X, dict):
            X = pd.DataFrame([X])
        elif isinstance(X, list):
            X = pd.DataFrame(X)

        if isinstance(X, pd.DataFrame):
            # Drop Class if passed
            if TARGET_COLUMN in X.columns:
                X = X.drop(columns=[TARGET_COLUMN])
            X_df = self._validate_columns(X)
            
            # Extract components
            time_data = X_df[["Time"]].to_numpy(dtype=np.float64)
            pca_data = X_df[PCA_FEATURES].to_numpy(dtype=np.float64)
            amount_data = X_df[["Amount"]].to_numpy(dtype=np.float64)
            
            scaled_time = (
                self.time_scaler.transform(time_data)
                if (self.scale_time and self.time_scaler is not None)
                else time_data
            )
            scaled_amount = (
                self.amount_scaler.transform(amount_data)
                if (self.scale_amount and self.amount_scaler is not None)
                else amount_data
            )
            
            # Concatenate back in canonical order: [Time, V1..V28, Amount]
            return np.hstack([scaled_time, pca_data, scaled_amount]).astype(np.float64)

        elif isinstance(X, np.ndarray):
            if X.ndim != 2 or X.shape[1] != len(self.feature_names):
                raise ValueError(
                    f"Expected 2D numpy array with {len(self.feature_names)} features, got shape {X.shape}"
                )
            X_copy = X.copy().astype(np.float64)
            
            time_data = X_copy[:, [0]]
            pca_data = X_copy[:, 1:29]
            amount_data = X_copy[:, [-1]]
            
            scaled_time = (
                self.time_scaler.transform(time_data)
                if (self.scale_time and self.time_scaler is not None)
                else time_data
            )
            scaled_amount = (
                self.amount_scaler.transform(amount_data)
                if (self.scale_amount and self.amount_scaler is not None)
                else amount_data
            )
            
            return np.hstack([scaled_time, pca_data, scaled_amount]).astype(np.float64)
        else:
            raise TypeError(f"Unsupported data type for transformation: {type(X)}")

    def fit_transform(self, X: Union[pd.DataFrame, np.ndarray, List[Dict[str, Any]]]) -> np.ndarray:
        """
        Fits on training data and transforms in a single call.
        """
        return self.fit(X).transform(X)

    def save(self, filepath: Union[str, Path]) -> None:
        """
        Serializes fitted preprocessor to disk using joblib.
        """
        if not self.is_fitted:
            raise RuntimeError("Cannot save unfitted preprocessor.")
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: Union[str, Path]) -> "TransactionPreprocessor":
        """
        Loads fitted preprocessor from serialized joblib file.
        """
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Preprocessor artifact not found at {filepath}")
        loaded = joblib.load(filepath)
        if not isinstance(loaded, cls):
            raise TypeError(f"Expected instance of {cls.__name__}, got {type(loaded)}")
        return loaded
