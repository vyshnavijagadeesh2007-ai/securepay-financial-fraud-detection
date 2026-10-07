from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class TransactionInput(BaseModel):
    """
    Standard transaction feature payload.
    Corresponds to the 30 raw input features from the dataset.
    Note: 'Class' is the evaluation label and is strictly prohibited in inference input.
    """
    Time: float = Field(..., description="Seconds elapsed since the initial transaction")
    Amount: float = Field(..., ge=0.0, description="Transaction monetary amount")
    V1: float = Field(...)
    V2: float = Field(...)
    V3: float = Field(...)
    V4: float = Field(...)
    V5: float = Field(...)
    V6: float = Field(...)
    V7: float = Field(...)
    V8: float = Field(...)
    V9: float = Field(...)
    V10: float = Field(...)
    V11: float = Field(...)
    V12: float = Field(...)
    V13: float = Field(...)
    V14: float = Field(...)
    V15: float = Field(...)
    V16: float = Field(...)
    V17: float = Field(...)
    V18: float = Field(...)
    V19: float = Field(...)
    V20: float = Field(...)
    V21: float = Field(...)
    V22: float = Field(...)
    V23: float = Field(...)
    V24: float = Field(...)
    V25: float = Field(...)
    V26: float = Field(...)
    V27: float = Field(...)
    V28: float = Field(...)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "Time": 406.0,
                "Amount": 149.62,
                "V1": -2.31,
                "V2": 1.95,
                "V3": -1.61,
                "V4": 3.99,
                "V5": -0.52,
                "V6": -1.43,
                "V7": -2.54,
                "V8": 1.39,
                "V9": -2.77,
                "V10": -2.77,
                "V11": 3.20,
                "V12": -2.90,
                "V13": -0.60,
                "V14": -4.29,
                "V15": 0.39,
                "V16": -1.14,
                "V17": -2.83,
                "V18": -0.01,
                "V19": 0.42,
                "V20": 0.13,
                "V21": 0.52,
                "V22": -0.04,
                "V23": -0.47,
                "V24": 0.32,
                "V25": 0.04,
                "V26": 0.18,
                "V27": 0.26,
                "V28": -0.14
            }
        }
    )

class BatchTransactionInput(BaseModel):
    transactions: List[TransactionInput] = Field(..., max_length=1000)

class TransactionRecord(BaseModel):
    id: int
    Time: float
    Amount: float
    anomaly_score: Optional[float] = None
    status: Optional[str] = "PENDING_INFERENCE"

class TransactionQueryResponse(BaseModel):
    total: int
    page: int
    page_size: int
    records: List[TransactionRecord]
