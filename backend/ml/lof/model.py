"""
Local Outlier Factor (LOF) Subsystem for SecurePay AI
Density-based unsupervised anomaly and novelty detection via k-nearest neighbor reachability.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Tuple, Union
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
import joblib


class LocalOutlierFactorDetector:
    """
    Local Outlier Factor (LOF) Anomaly and Novelty Detector Wrapper.
    
    Mathematical Principles & Theoretical Mechanics:
    - LOF (Breunig et al., 2000) measures the local density deviation of a transaction
      with respect to its k-nearest neighbors.
    - Reachability Distance:
      reach_dist_k(p, o) = max(k-distance(o), d(p, o))
    - Local Reachability Density (lrd):
      lrd_k(p) = |N_k(p)| / sum_{o in N_k(p)} reach_dist_k(p, o)
    - Local Outlier Factor:
      LOF_k(p) = (1 / |N_k(p)|) * sum_{o in N_k(p)} [lrd_k(o) / lrd_k(p)]
      * LOF ≈ 1: Homogeneous cluster density (Legitimate Inlier).
      * LOF < 1: Dense cluster interior (Inlier).
      * LOF > 1: Substantially lower local density than neighbors (Outlier / Anomaly).
      
    Novelty Detection Mode:
    - Set to `novelty=True`. The model is fitted exclusively on legitimate baseline
      cardholder transactions (Class == 0), creating an empirical density topology.
    - New or out-of-sample streaming transactions are then evaluated against this fitted topology.
    
    Continuous Anomaly Scoring Standardization:
    - Scikit-learn's `score_samples(X)` returns "opposite LOF" (values where lower indicates more anomalous).
    - SecurePay AI standardized continuous score convention:
      `anomaly_score(x) = -score_samples(x)`
      Under this convention, HIGHER scores monotonically represent HIGHER ANOMALY likelihood.
      
    Binary Prediction Mapping:
    - Scikit-learn returns +1 (inlier) and -1 (outlier).
    - SecurePay AI maps this to:
      0 = Normal (Legitimate)
      1 = Anomaly (Potential Fraud)
    """

    def __init__(
        self,
        n_neighbors: int = 20,
        contamination: Union[float, str] = 0.002,
        novelty: bool = True,
        metric: str = "minkowski",
        p: int = 2,
        n_jobs: int = -1
    ):
        if not novelty:
            raise ValueError("LocalOutlierFactorDetector requires novelty=True for out-of-sample inference.")
        
        self.n_neighbors = n_neighbors
        self.contamination = contamination
        self.novelty = novelty
        self.metric = metric
        self.p = p
        self.n_jobs = n_jobs
        
        self.model: Optional[LocalOutlierFactor] = None
        self.is_fitted: bool = False
        self.offset_: Optional[float] = None
        self.threshold_: Optional[float] = None

    def fit(self, X: np.ndarray) -> "LocalOutlierFactorDetector":
        """
        Fits Local Outlier Factor index on input training data.
        In the SecurePay AI framework, X MUST represent the legitimate baseline (Class == 0).
        
        Args:
            X: 2D numpy array of shape (N, n_features).
            
        Returns:
            self
        """
        X = np.asarray(X, dtype=np.float64)
        if X.ndim != 2:
            raise ValueError(f"Expected 2D array for training, got {X.ndim}D array")

        self.model = LocalOutlierFactor(
            n_neighbors=self.n_neighbors,
            contamination=self.contamination,
            novelty=True,
            metric=self.metric,
            p=self.p,
            n_jobs=self.n_jobs
        )
        self.model.fit(X)
        self.is_fitted = True
        self.offset_ = float(self.model.offset_)
        # In our standardized scoring (higher = more anomalous), threshold corresponds to -offset_
        self.threshold_ = -self.offset_
        return self

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """
        Scikit-learn decision function: score_samples(X) - offset_.
        Negative indicates outlier, positive indicates inlier.
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
            1D numpy array of continuous anomaly scores.
        """
        if not self.is_fitted or self.model is None:
            raise RuntimeError("Model has not been fitted yet.")
        X = np.asarray(X, dtype=np.float64)
        # Scikit-learn score_samples is opposite LOF (lower is more anomalous).
        # Inverting produces standardized positive LOF metric where higher is more anomalous.
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
            "n_neighbors": self.n_neighbors,
            "contamination": self.contamination,
            "novelty": self.novelty,
            "metric": self.metric,
            "p": self.p,
            "n_jobs": self.n_jobs,
            "is_fitted": self.is_fitted,
            "offset_": self.offset_,
            "threshold_": self.threshold_
        }

    def save(self, filepath: Union[str, Path]) -> None:
        """Serializes fitted LOF detector to disk using joblib."""
        if not self.is_fitted or self.model is None:
            raise RuntimeError("Cannot save unfitted model.")
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: Union[str, Path]) -> "LocalOutlierFactorDetector":
        """Loads fitted LOF detector from joblib artifact."""
        filepath = Path(filepath)
        if not filepath.exists():
            raise FileNotFoundError(f"Model artifact not found at {filepath}")
        loaded = joblib.load(filepath)
        if not isinstance(loaded, cls):
            raise TypeError(f"Expected instance of {cls.__name__}, got {type(loaded)}")
        return loaded
