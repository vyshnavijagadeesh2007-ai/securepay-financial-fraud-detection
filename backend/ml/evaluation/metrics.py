"""
Evaluation Subsystem for SecurePay AI
Calculates Precision, Recall, F1, Confusion Matrices, and PR Curves for anomaly models.
Enforces strict focus on minority positive class (Fraud = 1) rather than overall Accuracy.
"""

from typing import Dict, Any, Tuple
import numpy as np
from sklearn.metrics import precision_recall_curve, auc, roc_auc_score


class AnomalyEvaluator:
    """
    Evaluation Engine Interface for Anomaly & Fraud Detection.
    
    Terminology & Binary Mapping:
    - Positive Class (1): Fraudulent / Anomalous event
    - Negative Class (0): Legitimate / Normal event
    - True Positive (TP): Fraud correctly identified as anomalous
    - False Positive (FP): Legitimate transaction falsely flagged as anomalous
    - True Negative (TN): Legitimate transaction correctly treated as normal
    - False Negative (FN): Fraudulent transaction missed by the detector
    """

    @staticmethod
    def evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, Any]:
        """
        Computes comprehensive anomaly detection evaluation metrics.
        
        Args:
            y_true: Binary ground-truth labels (0 for normal, 1 for fraud).
            y_pred: Binary predictions (0 for normal, 1 for anomaly).
            
        Returns:
            Dictionary containing TP, FP, TN, FN, precision, recall, f1, and rates.
        """
        y_true = np.asarray(y_true, dtype=int)
        y_pred = np.asarray(y_pred, dtype=int)
        
        if y_true.shape != y_pred.shape:
            raise ValueError(f"Shape mismatch: y_true {y_true.shape} vs y_pred {y_pred.shape}")

        tp = int(np.sum((y_true == 1) & (y_pred == 1)))
        fp = int(np.sum((y_true == 0) & (y_pred == 1)))
        tn = int(np.sum((y_true == 0) & (y_pred == 0)))
        fn = int(np.sum((y_true == 1) & (y_pred == 0)))

        precision = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        recall = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        f1 = float(2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
        
        fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
        fnr = float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0
        
        total_anomalies_predicted = tp + fp
        total_samples = len(y_true)
        anomaly_rate = float(total_anomalies_predicted / total_samples) if total_samples > 0 else 0.0

        return {
            "total_samples": total_samples,
            "actual_frauds": int(np.sum(y_true == 1)),
            "actual_legitimate": int(np.sum(y_true == 0)),
            "predicted_anomalies": total_anomalies_predicted,
            "predicted_anomaly_rate": round(anomaly_rate, 6),
            "true_positives": tp,
            "false_positives": fp,
            "true_negatives": tn,
            "false_negatives": fn,
            "precision": round(precision, 6),
            "recall": round(recall, 6),
            "f1_score": round(f1, 6),
            "false_positive_rate": round(fpr, 6),
            "false_negative_rate": round(fnr, 6)
        }

    @staticmethod
    def compute_pr_curve(y_true: np.ndarray, scores: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, float]:
        """
        Computes Precision-Recall curve coordinates and Area Under PR Curve (PR-AUC).
        
        Args:
            y_true: Binary ground-truth labels (0 for normal, 1 for fraud).
            scores: Continuous anomaly scores (higher = more anomalous).
            
        Returns:
            Tuple of (precisions, recalls, thresholds, pr_auc)
        """
        y_true = np.asarray(y_true, dtype=int)
        scores = np.asarray(scores, dtype=float)
        
        precisions, recalls, thresholds = precision_recall_curve(y_true, scores)
        pr_auc = float(auc(recalls, precisions))
        
        return precisions, recalls, thresholds, round(pr_auc, 6)
