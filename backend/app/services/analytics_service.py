from typing import Optional, Dict, Any
import pandas as pd
from backend.app.core.config import settings
from backend.app.schemas.analytics import (
    AnalyticsSummaryResponse,
    ClassDistribution,
    FeatureDescriptiveStats
)
from backend.app.schemas.dashboard import DashboardSummary

class AnalyticsService:
    """
    Service responsible for verified dataset-level descriptive statistics.
    Inspects creditcard.csv in a read-only manner without fabricating ML metrics.
    """
    _cached_summary: Optional[AnalyticsSummaryResponse] = None

    @classmethod
    def get_dataset_summary(cls) -> AnalyticsSummaryResponse:
        if cls._cached_summary is not None:
            return cls._cached_summary

        metrics_file = settings.METRICS_DIR / "dataset_summary.json"
        if metrics_file.exists():
            import json
            with open(metrics_file, "r") as f:
                data = json.load(f)
            amount_ov = data["amount_statistics"]["overall"]
            time_st = data["time_statistics"]
            cls._cached_summary = AnalyticsSummaryResponse(
                dataset_name=data.get("dataset_name", "creditcard.csv"),
                total_observations=data["total_rows"],
                total_features=data["total_columns"],
                feature_names=data["columns"],
                class_distribution=ClassDistribution(
                    legitimate_count=data["class_distribution"]["legitimate_count"],
                    fraud_count=data["class_distribution"]["fraud_count"],
                    fraud_percentage=data["class_distribution"]["fraud_percentage"],
                    imbalance_ratio=data["class_distribution"]["imbalance_ratio"]
                ),
                amount_statistics=FeatureDescriptiveStats(
                    mean=amount_ov["mean"],
                    std=amount_ov["std"],
                    min=amount_ov["min"],
                    q25=amount_ov["q25"],
                    median=amount_ov["median"],
                    q75=amount_ov["q75"],
                    max=amount_ov["max"]
                ),
                time_statistics=FeatureDescriptiveStats(
                    mean=time_st["mean"],
                    std=time_st["std"],
                    min=time_st["min"],
                    q25=time_st["q25"],
                    median=time_st["median"],
                    q75=time_st["q75"],
                    max=time_st["max"]
                ),
                duplicates_count=data["duplicate_analysis"]["total_duplicate_rows_excluding_first"],
                null_values_count=data["missing_values_total"],
                pca_features_count=28,
                pca_status="COMPUTED_ON_DEMAND",
                status="VERIFIED"
            )
            return cls._cached_summary

        if not settings.DATA_PATH.exists():
            raise FileNotFoundError(f"Dataset not found at {settings.DATA_PATH}")

        # Fallback to direct read-only CSV inspection
        df = pd.read_csv(settings.DATA_PATH)
        
        class_counts = df["Class"].value_counts().to_dict()
        legit_count = int(class_counts.get(0, 0))
        fraud_count = int(class_counts.get(1, 0))
        total_obs = len(df)
        fraud_pct = round((fraud_count / total_obs) * 100, 5) if total_obs > 0 else 0.0

        amount_stats = FeatureDescriptiveStats(
            mean=round(float(df["Amount"].mean()), 2),
            std=round(float(df["Amount"].std()), 2),
            min=round(float(df["Amount"].min()), 2),
            q25=round(float(df["Amount"].quantile(0.25)), 2),
            median=round(float(df["Amount"].median()), 2),
            q75=round(float(df["Amount"].quantile(0.75)), 2),
            max=round(float(df["Amount"].max()), 2)
        )

        time_stats = FeatureDescriptiveStats(
            mean=round(float(df["Time"].mean()), 2),
            std=round(float(df["Time"].std()), 2),
            min=round(float(df["Time"].min()), 2),
            q25=round(float(df["Time"].quantile(0.25)), 2),
            median=round(float(df["Time"].median()), 2),
            q75=round(float(df["Time"].quantile(0.75)), 2),
            max=round(float(df["Time"].max()), 2)
        )

        duplicates = int(df.duplicated().sum())

        cls._cached_summary = AnalyticsSummaryResponse(
            dataset_name="creditcard.csv",
            total_observations=total_obs,
            total_features=len(df.columns),
            feature_names=df.columns.tolist(),
            class_distribution=ClassDistribution(
                legitimate_count=legit_count,
                fraud_count=fraud_count,
                fraud_percentage=fraud_pct,
                imbalance_ratio=f"1 : {round(legit_count / fraud_count, 1)}" if fraud_count > 0 else "N/A"
            ),
            amount_statistics=amount_stats,
            time_statistics=time_stats,
            duplicates_count=duplicates,
            null_values_count=int(df.isnull().sum().sum()),
            pca_features_count=28,
            pca_status="COMPUTED_ON_DEMAND",
            status="VERIFIED"
        )
        return cls._cached_summary

    @classmethod
    def get_dashboard_summary(cls) -> DashboardSummary:
        """
        Returns Phase 0 dashboard metrics.
        Actual dataset observations are shown, while all ML model metrics
        (precision, recall, f1, detected anomalies) are strictly None ('--').
        """
        summary = cls.get_dataset_summary()
        return DashboardSummary(
            total_transactions=summary.total_observations,
            legitimate_transactions=summary.class_distribution.legitimate_count,
            fraud_transactions=summary.class_distribution.fraud_count,
            detected_anomalies=None,  # Not trained yet
            fraud_percentage=summary.class_distribution.fraud_percentage,
            current_model="Isolation Forest",
            model_status="NOT TRAINED",
            precision=None,  # Strictly None during Phase 0
            recall=None,     # Strictly None during Phase 0
            f1_score=None    # Strictly None during Phase 0
        )
