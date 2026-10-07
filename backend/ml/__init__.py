"""
SecurePay AI — Machine Learning Subsystem
Establishes the architecture for unsupervised transaction anomaly detection:
- Preprocessing: RobustScaler transformation
- Novelty Baseline: Legitimate transaction distribution modeling (Class == 0)
- Algorithms: Isolation Forest & Local Outlier Factor (LOF)
- Evaluation: Precision, Recall, F1, PR curves, Contamination experiments
- Serialization: Joblib artifact export for real-time inference
"""
