"""
Isolation Forest Subsystem for SecurePay AI
Tree-based unsupervised anomaly detection via recursive spatial partitioning.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib


class IsolationForestDetector:
    """
    Isolation Forest Anomaly Detection Wrapper.
    
    Mathematical Principles & Scoring Conventions:
    - Anomalies require fewer random recursive splits to isolate than normal points,
      resulting in shorter average path lengths h(x) across ensemble trees.
    - Continuous Anomaly Scoring:
      * Scikit-learn's `score_samples(X)` returns negative values where lower indicates
        higher abnormality.
      * Standardized representation in SecurePay AI:
        `anomaly_score(x) = -score_samples(x)`
        In this representation, HIGHER scores denote MORE ANOMALOUS behavior.
    - Binary Predictions:
      * Scikit-learn returns +1 (inlier) and -1 (outlier).
      * SecurePay AI maps this to:
        0 = Normal (Legitimate)
        1 = Anomaly (Potential Fraud)
    """

    def __init__(
        self,
        n_estimators: int = 200,
        contamination: Union[float, str] = 0.0017,
        max_samples: Union[int, float, str] = "auto",
        random_state: int = 42,
        n_jobs: int = -1
    ):
        self.n_estimators = n_estimators
        self.contamination = contamination
        self.max_samples = max_samples
        self.random_state = random_state
        self.n_jobs = n_jobs
        
        self.model: Optional[IsolationForest] = None
        self.is_fitted: bool = False
        self.offset_: Optional[float] = None

    def fit(self, X: np.ndarray) -> "IsolationForestDetector":
        """
        Fits Isolation Forest ensemble on input training data.
        In the SecurePay AI framework, X MUST represent the legitimate baseline (Class == 0).
        
        Args:
            X: 2D numpy array of shape (N, n_features).
            
        Returns:
            self
        """
        X = np.asarray(X, dtype=np.float64)
        if X.ndim != 2:
            raise ValueError(f"Expected 2D array for training, got {X.ndim}D array")

        self.model = IsolationForest(
            n_estimators=self.n_estimators,
            contamination=self.contamination,
            max_samples=self.max_samples,
            random_state=self.random_state,
            n_jobs=self.n_jobs
        )
        self.model.fit(X)
        self.is_fitted = True
        self.offset_ = float(self.model.offset_)
        return self

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """
        Direct access to scikit-learn's decision_function.
        Returns shifted anomaly score relative to offset (negative = outlier, positive = inlier).
        """
        if not self.is_fitted or self.model is None:
            raise RuntimeError("Model has not been fitted yet.")
        X = np.asarray(X, dtype=np.float64)
        return self.model.decision_function(X)

    def score_samples(self, X: np.ndarray) -> np.ndarray:
        """
        Computes standardized continuous anomaly score where HIGHER = MORE ANOMALOUS.
        Formula: anomaly_score = -model.score_samples(X)
        
        Args:
            X: 2D numpy array of shape (N, n_features).
            
        Returns:
            1D numpy array of anomaly scores.
        """
        if not self.is_fitted or self.model is None:
            raise RuntimeError("Model has not been fitted yet.")
        X = np.asarray(X, dtype=np.float64)
        # Invert so higher score represents higher anomaly probability
        return -self.model.score_samples(X)

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Produces binary classification predictions:
        0 = Normal (Legitimate)
        1 = Anomaly (Potential Fraud)
        
        Args:
            X: 2D numpy array of shape (N, n_features).
            
        Returns:
            1D numpy array of binary predictions (0 or 1).
        """
        if not self.is_fitted or self.model is None:
            raise RuntimeError("Model has not been fitted yet.")
        X = np.asarray(X, dtype=np.float64)
        sklearn_preds = self.model.predict(X)
        # Map: -1 (outlier) -> 1, +1 (inlier) -> 0
        return np.where(sklearn_preds == -1, 1, 0).astype(int)

    def predict_with_scores(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Returns both binary predictions and continuous anomaly scores in one pass.
        
        Returns:
            Tuple of (binary_predictions, continuous_anomaly_scores)
        """
        return self.predict(X), self.score_samples(X)

    def get_params(self) -> Dict[str, Any]:
        """Returns configured hyperparameter dictionary."""
        return {
            "n_estimators": self.n_estimators,
            "contamination": self.contamination,
            "max_samples": self.max_samples,
            "random_state": self.random_state,
            "n_jobs": self.n_jobs,
            "is_fitted": self.is_fitted,
            "offset_": self.offset_
        }

    def save(self, filepath: Union[str, Path]) -> None:
        """Serializes fitted detector to disk using joblib."""
        if not self.is_fitted or self.model is None:
            raise RuntimeError("Cannot save unfitted model.")
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: Union[str, Path]) -> "IsolationForestDetector":
        """Loads fitted detector from joblib artifact."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Model artifact not found at {filepath}")
        loaded = joblib.load(filepath)
        if not isinstance(loaded, cls):
            raise TypeError(f"Expected instance of {cls.__name__}, got {type(loaded)}")
        return loaded
