from fastapi import APIRouter, Query, HTTPException
import pandas as pd
from backend.app.schemas.transaction import (
    TransactionQueryResponse,
    TransactionRecord
)
from backend.app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse
)
from backend.app.services.model_service import ModelService
from backend.app.core.config import settings

router = APIRouter()

@router.get("/transactions", response_model=TransactionQueryResponse, summary="Query Raw Transaction Sample Stream")
async def list_transactions(
    page: int = Query(default=1, ge=1, description="Page index"),
    page_size: int = Query(default=25, ge=5, le=100, description="Items per page"),
    sort_by: str = Query(default="Time", description="Sort field ('Time' or 'Amount')")
):
    """
    Returns authentic transaction records from creditcard.csv for exploration.
    Anomaly scores remain uncalculated until Phase 2/3.
    """
    if not settings.DATA_PATH.exists():
        raise HTTPException(status_code=500, detail="Transaction dataset not found on disk.")
    
    # Read lightweight slice
    skip_rows = (page - 1) * page_size
    # Read header and specific slice
    df_slice = pd.read_csv(
        settings.DATA_PATH,
        skiprows=range(1, skip_rows + 1) if skip_rows > 0 else None,
        nrows=page_size
    )
    
    # Count total rows
    # We know the verified total is 284,807
    total_count = 284807
    
    records = []
    for idx, row in df_slice.iterrows():
        records.append(
            TransactionRecord(
                id=skip_rows + idx + 1,
                Time=float(row["Time"]),
                Amount=float(row["Amount"]),
                anomaly_score=None,
                status="PENDING_INFERENCE"
            )
        )
        
    return TransactionQueryResponse(
        total=total_count,
        page=page,
        page_size=page_size,
        records=records
    )

@router.post("/predict", response_model=PredictionResponse, summary="Real-Time Anomaly Inference")
async def predict_transaction(request: PredictionRequest):
    """
    Real-time transaction anomaly detection endpoint.
    In Phase 0: model is NOT_TRAINED, returns explicit status without fabricated predictions.
    """
    return ModelService.predict(request)

@router.post("/predict/batch", response_model=BatchPredictionResponse, summary="Batch Transaction Anomaly Inference")
async def predict_batch(request: BatchPredictionRequest):
    """
    Batch transaction anomaly detection endpoint.
    In Phase 0: returns NOT_TRAINED status.
    """
    return BatchPredictionResponse(
        model=request.model.value,
        total_processed=len(request.transactions),
        predictions=[
            ModelService.predict(
                PredictionRequest(transaction=tx, model=request.model)
            ) for tx in request.transactions
        ],
        status="MODEL_NOT_TRAINED"
    )
