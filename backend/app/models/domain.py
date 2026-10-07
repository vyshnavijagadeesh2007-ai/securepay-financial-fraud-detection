from enum import Enum

class ModelName(str, Enum):
    ISOLATION_FOREST = "Isolation Forest"
    LOCAL_OUTLIER_FACTOR = "Local Outlier Factor"

class ModelStatus(str, Enum):
    NOT_TRAINED = "NOT TRAINED"
    TRAINING = "TRAINING"
    READY = "READY"
    ERROR = "ERROR"

class PredictionStatus(str, Enum):
    NORMAL = "NORMAL"
    ANOMALY = "POTENTIAL ANOMALY"
