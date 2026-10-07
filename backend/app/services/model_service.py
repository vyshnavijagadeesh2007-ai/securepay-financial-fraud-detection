"""
Model Service Subsystem for SecurePay AI
Manages model lifecycle, artifact ingestion, comparative benchmarks, and live inference.
"""

from typing import Optional, List, Dict, Any
import time
import json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import numpy as np

from backend.app.core.config import settings
from backend.app.models.domain import ModelName, ModelStatus
from backend.app.schemas.prediction import PredictionRequest, PredictionResponse
from backend.app.schemas.metrics import (
    MetricSummary,
    ModelComparisonResponse,
    ThresholdAnalysisResponse,
    ContaminationExperiment
)
from backend.ml.preprocessing.scaler import TransactionPreprocessor
from backend.ml.isolation_forest.model import IsolationForestDetector
from backend.ml.lof.model import LocalOutlierFactorDetector


class ModelService:
    """
    Service managing Machine Learning models (Isolation Forest, Local Outlier Factor).
    
    Phase 3 Integration:
    - Automatically detects trained Isolation Forest artifact in outputs/models/isolation_forest.joblib.
    - Automatically detects trained Local Outlier Factor artifact in outputs/models/local_outlier_factor.joblib.
    - Exposes empirical metrics from outputs/metrics/ for both architectures.
    - Serves real-time inference via fitted TransactionPreprocessor and selected detector.
    """
    _iforest_detector: Optional[IsolationForestDetector] = None
    _lof_detector: Optional[LocalOutlierFactorDetector] = None
    _preprocessor: Optional[TransactionPreprocessor] = None
    _iforest_summary: Optional[Dict[str, Any]] = None
    _iforest_experiments: Optional[List[Dict[str, Any]]] = None
    _lof_summary: Optional[Dict[str, Any]] = None
    _lof_experiments: Optional[List[Dict[str, Any]]] = None
    _operating_points: Optional[Dict[str, Any]] = None
    _business_cost: Optional[Dict[str, Any]] = None

    @classmethod
    def _load_operating_points(cls) -> Optional[Dict[str, Any]]:
        if cls._operating_points is not None:
            return cls._operating_points
        thresh_path = settings.BASE_DIR / "outputs" / "thresholds" / "selected_operating_points.json"
        if thresh_path.exists():
            with open(thresh_path, "r") as f:
                cls._operating_points = json.load(f)
            return cls._operating_points
        return None

    @classmethod
    def _load_business_cost(cls) -> Optional[Dict[str, Any]]:
        if cls._business_cost is not None:
            return cls._business_cost
        cost_path = settings.BASE_DIR / "outputs" / "thresholds" / "business_cost_analysis.json"
        if cost_path.exists():
            with open(cost_path, "r") as f:
                cls._business_cost = json.load(f)
            return cls._business_cost
        return None

    @classmethod
    def get_model_status(cls, model_name: ModelName) -> ModelStatus:
        """Returns the readiness status of the specified model."""
        if model_name == ModelName.ISOLATION_FOREST:
            model_file = settings.MODELS_DIR / "isolation_forest.joblib"
            return ModelStatus.READY if model_file.exists() else ModelStatus.NOT_TRAINED
        elif model_name == ModelName.LOCAL_OUTLIER_FACTOR:
            model_file = settings.MODELS_DIR / "local_outlier_factor.joblib"
            return ModelStatus.READY if model_file.exists() else ModelStatus.NOT_TRAINED
        return ModelStatus.NOT_TRAINED

    @classmethod
    def _load_iforest_summary(cls) -> Optional[Dict[str, Any]]:
        if cls._iforest_summary is not None:
            return cls._iforest_summary
        summary_path = settings.METRICS_DIR / "isolation_forest_summary.json"
        if summary_path.exists():
            with open(summary_path, "r") as f:
                cls._iforest_summary = json.load(f)
            return cls._iforest_summary
        return None

    @classmethod
    def _load_iforest_experiments(cls) -> List[Dict[str, Any]]:
        if cls._iforest_experiments is not None:
            return cls._iforest_experiments
        csv_path = settings.METRICS_DIR / "isolation_forest_experiments.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            cls._iforest_experiments = df.to_dict(orient="records")
            return cls._iforest_experiments
        return []

    @classmethod
    def _load_lof_summary(cls) -> Optional[Dict[str, Any]]:
        if cls._lof_summary is not None:
            return cls._lof_summary
        summary_path = settings.METRICS_DIR / "lof_summary.json"
        if summary_path.exists():
            with open(summary_path, "r") as f:
                cls._lof_summary = json.load(f)
            return cls._lof_summary
        return None

    @classmethod
    def _load_lof_experiments(cls) -> List[Dict[str, Any]]:
        if cls._lof_experiments is not None:
            return cls._lof_experiments
        csv_path = settings.METRICS_DIR / "lof_experiments.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            cls._lof_experiments = df.to_dict(orient="records")
            return cls._lof_experiments
        return []

    @classmethod
    def _get_or_load_detector(cls) -> Optional[IsolationForestDetector]:
        if cls._iforest_detector is not None:
            return cls._iforest_detector
        model_path = settings.MODELS_DIR / "isolation_forest.joblib"
        if model_path.exists():
            cls._iforest_detector = IsolationForestDetector.load(model_path)
            return cls._iforest_detector
        return None

    @classmethod
    def _get_or_load_lof_detector(cls) -> Optional[LocalOutlierFactorDetector]:
        if cls._lof_detector is not None:
            return cls._lof_detector
        model_path = settings.MODELS_DIR / "local_outlier_factor.joblib"
        if model_path.exists():
            cls._lof_detector = LocalOutlierFactorDetector.load(model_path)
            return cls._lof_detector
        return None

    @classmethod
    def _get_or_load_preprocessor(cls) -> Optional[TransactionPreprocessor]:
        if cls._preprocessor is not None:
            return cls._preprocessor
        prep_path = settings.MODELS_DIR / "preprocessor.joblib"
        if prep_path.exists():
            cls._preprocessor = TransactionPreprocessor.load(prep_path)
            return cls._preprocessor
        return None

    @classmethod
    def predict(cls, request: PredictionRequest) -> PredictionResponse:
        """
        Executes real-time transaction inference with calibrated threshold support.
        Transforms inputs and scores via selected detector (Isolation Forest or LOF).
        """
        start_time = time.perf_counter()
        preprocessor = cls._get_or_load_preprocessor()
        op_points = cls._load_operating_points()

        if request.model == ModelName.ISOLATION_FOREST:
            detector = cls._get_or_load_detector()
            if detector is not None and preprocessor is not None:
                tx_dict = request.transaction.model_dump()
                X = preprocessor.transform(tx_dict)
                
                _, scores = detector.predict_with_scores(X)
                anomaly_score = float(scores[0])

                # Resolve calibrated threshold based on requested operating mode
                threshold = float(detector.offset_) if detector.offset_ is not None else 0.622447
                op_mode = getattr(request, "operating_mode", "balanced") or "balanced"

                if request.custom_threshold is not None:
                    threshold = float(request.custom_threshold)
                    op_mode = "custom"
                elif op_points and "isolation_forest" in op_points:
                    val_ops = op_points["isolation_forest"].get("validation_selected_thresholds", {})
                    if op_mode in val_ops:
                        threshold = float(val_ops[op_mode]["threshold"])
                    elif "balanced" in val_ops:
                        threshold = float(val_ops["balanced"]["threshold"])
                        op_mode = "balanced"

                is_anomaly = bool(anomaly_score >= threshold)
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                
                return PredictionResponse(
                    model=request.model.value,
                    anomaly_score=round(anomaly_score, 6),
                    score=round(anomaly_score, 6),
                    threshold=round(threshold, 6),
                    prediction=1 if is_anomaly else 0,
                    status="POTENTIAL ANOMALY" if is_anomaly else "NORMAL",
                    is_anomaly=is_anomaly,
                    operating_point=op_mode,
                    operating_mode=op_mode,
                    execution_time_ms=round(elapsed_ms, 2),
                    message=(
                        f"Isolation Forest inference under '{op_mode}' mode (threshold={threshold:.4f}). "
                        + ("Structural anomaly detected. Flagged for fraud review." if is_anomaly else "Transaction cleared within nominal cluster.")
                    )
                )

        elif request.model == ModelName.LOCAL_OUTLIER_FACTOR:
            lof_detector = cls._get_or_load_lof_detector()
            if lof_detector is not None and preprocessor is not None:
                tx_dict = request.transaction.model_dump()
                X = preprocessor.transform(tx_dict)
                
                _, scores = lof_detector.predict_with_scores(X)
                anomaly_score = float(scores[0])

                # Resolve calibrated threshold based on requested operating mode
                threshold = float(lof_detector.threshold_) if lof_detector.threshold_ is not None else 2.490138
                op_mode = getattr(request, "operating_mode", "balanced") or "balanced"

                if request.custom_threshold is not None:
                    threshold = float(request.custom_threshold)
                    op_mode = "custom"
                elif op_points and "local_outlier_factor" in op_points:
                    val_ops = op_points["local_outlier_factor"].get("validation_selected_thresholds", {})
                    if op_mode in val_ops:
                        threshold = float(val_ops[op_mode]["threshold"])
                    elif "balanced" in val_ops:
                        threshold = float(val_ops["balanced"]["threshold"])
                        op_mode = "balanced"

                is_anomaly = bool(anomaly_score >= threshold)
                elapsed_ms = (time.perf_counter() - start_time) * 1000.0
                
                return PredictionResponse(
                    model=request.model.value,
                    anomaly_score=round(anomaly_score, 6),
                    score=round(anomaly_score, 6),
                    threshold=round(threshold, 6),
                    prediction=1 if is_anomaly else 0,
                    status="POTENTIAL ANOMALY" if is_anomaly else "NORMAL",
                    is_anomaly=is_anomaly,
                    operating_point=op_mode,
                    operating_mode=op_mode,
                    execution_time_ms=round(elapsed_ms, 2),
                    message=(
                        f"Local Outlier Factor inference under '{op_mode}' mode (threshold={threshold:.4f}). "
                        + ("Local reachability density anomaly detected. Flagged for review." if is_anomaly else "Nominal local density cleared.")
                    )
                )

        # Fallback for untrained models
        return PredictionResponse(
            model=request.model.value,
            anomaly_score=None,
            score=None,
            threshold=None,
            prediction=None,
            status="MODEL_NOT_TRAINED",
            is_anomaly=None,
            operating_point=None,
            operating_mode=None,
            execution_time_ms=None,
            message=f"{request.model.value} model is not yet trained."
        )

    @classmethod
    def get_comparison(cls) -> ModelComparisonResponse:
        """
        Returns model comparison metrics.
        Returns authentic measured metrics for both Isolation Forest and Local Outlier Factor.
        """
        if_summary = cls._load_iforest_summary()
        if_status = cls.get_model_status(ModelName.ISOLATION_FOREST)
        
        if if_status == ModelStatus.READY and if_summary is not None:
            m = if_summary["selected_metrics"]
            p = if_summary["parameters"]
            if_metrics = MetricSummary(
                model_name="Isolation Forest",
                precision=m["precision"],
                recall=m["recall"],
                f1_score=m["f1_score"],
                false_positives=m["false_positives"],
                false_negatives=m["false_negatives"],
                true_positives=m["true_positives"],
                true_negatives=m["true_negatives"],
                execution_time_seconds=m["execution_time_seconds"],
                detected_anomalies=m["anomalies_flagged"],
                contamination=p["contamination"],
                status="READY"
            )
        else:
            if_metrics = MetricSummary(
                model_name="Isolation Forest",
                precision=None, recall=None, f1_score=None,
                false_positives=None, false_negatives=None,
                true_positives=None, true_negatives=None,
                execution_time_seconds=None, detected_anomalies=None,
                contamination=None, status="NOT_TRAINED"
            )

        lof_summary = cls._load_lof_summary()
        lof_status = cls.get_model_status(ModelName.LOCAL_OUTLIER_FACTOR)

        if lof_status == ModelStatus.READY and lof_summary is not None:
            lm = lof_summary["selected_metrics"]
            lp = lof_summary["selected_configuration"]
            lof_metrics = MetricSummary(
                model_name="Local Outlier Factor",
                precision=lm["precision"],
                recall=lm["recall"],
                f1_score=lm["f1_score"],
                false_positives=lm["false_positives"],
                false_negatives=lm["false_negatives"],
                true_positives=lm["true_positives"],
                true_negatives=lm["true_negatives"],
                execution_time_seconds=lm["execution_time_seconds"],
                detected_anomalies=lm["predicted_anomalies"],
                contamination=lp["contamination"],
                status="READY"
            )
        else:
            lof_metrics = MetricSummary(
                model_name="Local Outlier Factor",
                precision=None, recall=None, f1_score=None,
                false_positives=None, false_negatives=None,
                true_positives=None, true_negatives=None,
                execution_time_seconds=None, detected_anomalies=None,
                contamination=None, status="NOT_TRAINED"
            )

        if if_status == ModelStatus.READY and lof_status == ModelStatus.READY:
            comparison_status = "EVALUATED"
            recommendation = (
                "Phase 4 Dynamic Calibration Complete: Local Outlier Factor demonstrates superior overall anomaly "
                "detection power (Test PR-AUC=0.2186 vs 0.1081; Balanced F1=0.3455 with 57.6% recall vs 0.1993 with 29.3% recall), "
                "making it the recommended architecture for asynchronous fraud investigation queues. "
                "Isolation Forest remains the recommended architecture for inline, real-time edge authorization gates "
                "requiring sub-millisecond scoring and bounded false positive alert burdens (44-121 FPs vs 72-174 FPs)."
            )
        elif if_status == ModelStatus.READY:
            comparison_status = "EVALUATED"
            recommendation = f"Isolation Forest established as baseline (F1={if_metrics.f1_score:.4f})."
        else:
            comparison_status = "NOT_TRAINED"
            recommendation = None

        return ModelComparisonResponse(
            models=[if_metrics, lof_metrics],
            recommendation=recommendation,
            status=comparison_status,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    @classmethod
    def get_threshold_analysis(cls, model_name: ModelName) -> ThresholdAnalysisResponse:
        """
        Returns threshold and contamination experiments, enriched with Phase 4 calibrated operating points.
        """
        op_points = cls._load_operating_points()
        if model_name == ModelName.ISOLATION_FOREST:
            experiments = cls._load_iforest_experiments()
            if experiments:
                experiment_objs = []
                for exp in experiments:
                    experiment_objs.append(
                        ContaminationExperiment(
                            contamination=float(exp["contamination"]),
                            detected_anomalies=int(exp["anomalies"]),
                            precision=float(exp["precision"]),
                            recall=float(exp["recall"]),
                            f1_score=float(exp["f1"]),
                            false_positives=int(exp["false_positives"]),
                            execution_time_seconds=float(exp["total_execution_seconds"])
                        )
                    )
                detector = cls._get_or_load_detector()
                offset_val = float(detector.offset_) if (detector and detector.offset_ is not None) else None
                if_ops = op_points.get("isolation_forest") if op_points else None
                pr_auc = op_points.get("metadata", {}).get("isolation_forest_test_pr_auc") if op_points else None
                optimal_thresh = offset_val
                if if_ops and "validation_selected_thresholds" in if_ops:
                    optimal_thresh = float(if_ops["validation_selected_thresholds"]["balanced"]["threshold"])

                return ThresholdAnalysisResponse(
                    selected_model=model_name.value,
                    optimal_threshold=optimal_thresh,
                    default_threshold=offset_val,
                    contamination_experiments=experiment_objs,
                    pr_curve_points=None,
                    operating_points=if_ops,
                    pr_auc=pr_auc,
                    status="EVALUATED"
                )

        elif model_name == ModelName.LOCAL_OUTLIER_FACTOR:
            experiments = cls._load_lof_experiments()
            if experiments:
                experiment_objs = []
                # Filter for default n_neighbors=50 or all unique contaminations
                df_exp = pd.DataFrame(experiments)
                # Take subset for k=50
                k50_exp = df_exp[df_exp["n_neighbors"] == 50] if "n_neighbors" in df_exp else df_exp
                for _, exp in k50_exp.iterrows():
                    experiment_objs.append(
                        ContaminationExperiment(
                            contamination=float(exp["contamination"]),
                            detected_anomalies=int(exp["predicted_anomalies"]),
                            precision=float(exp["precision"]),
                            recall=float(exp["recall"]),
                            f1_score=float(exp["f1"]),
                            false_positives=int(exp["fp"]),
                            execution_time_seconds=float(exp["execution_time_sec"])
                        )
                    )
                lof_detector = cls._get_or_load_lof_detector()
                threshold_val = float(lof_detector.threshold_) if (lof_detector and lof_detector.threshold_ is not None) else None
                lof_ops = op_points.get("local_outlier_factor") if op_points else None
                pr_auc = op_points.get("metadata", {}).get("lof_test_pr_auc") if op_points else None
                optimal_thresh = threshold_val
                if lof_ops and "validation_selected_thresholds" in lof_ops:
                    optimal_thresh = float(lof_ops["validation_selected_thresholds"]["balanced"]["threshold"])

                return ThresholdAnalysisResponse(
                    selected_model=model_name.value,
                    optimal_threshold=optimal_thresh,
                    default_threshold=threshold_val,
                    contamination_experiments=experiment_objs,
                    pr_curve_points=None,
                    operating_points=lof_ops,
                    pr_auc=pr_auc,
                    status="EVALUATED"
                )

        # Default fallback
        return ThresholdAnalysisResponse(
            selected_model=model_name.value,
            optimal_threshold=None,
            default_threshold=None,
            contamination_experiments=[
                ContaminationExperiment(contamination=0.001),
                ContaminationExperiment(contamination=0.002),
                ContaminationExperiment(contamination=0.005),
                ContaminationExperiment(contamination=0.01),
                ContaminationExperiment(contamination=0.02),
                ContaminationExperiment(contamination=0.03),
                ContaminationExperiment(contamination=0.05)
            ],
            pr_curve_points=None,
            status="NOT_TRAINED"
        )
