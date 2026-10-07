import os
from pathlib import Path
from pydantic import BaseModel, Field

def _allowed_origins() -> list[str]:
    development_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    origins_setting = os.environ.get("ALLOWED_ORIGINS", "")
    configured_origins = [
        origin.strip()
        for origin in origins_setting.split(",")
        if origin.strip()
    ]
    if not configured_origins:
        return development_origins
    if "*" in configured_origins:
        raise ValueError("ALLOWED_ORIGINS must not contain '*' when credentials are enabled.")
    return list(dict.fromkeys(configured_origins))

class Settings(BaseModel):
    PROJECT_NAME: str = "SecurePay AI — Real-Time Anomaly Detection API"
    VERSION: str = "0.1.0-phase4"
    API_V1_PREFIX: str = "/api"
    DESCRIPTION: str = (
        "REST API serving inference, metrics, and analytics for financial "
        "transaction anomaly detection using unsupervised ML (Isolation Forest, LOF)."
    )
    
    # Root and project directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent.parent
    DATA_PATH: Path = BASE_DIR / "data" / "creditcard.csv"
    MODELS_DIR: Path = BASE_DIR / "outputs" / "models"
    FIGURES_DIR: Path = BASE_DIR / "outputs" / "figures"
    METRICS_DIR: Path = BASE_DIR / "outputs" / "metrics"
    
    # CORS
    ALLOWED_ORIGINS: list[str] = Field(default_factory=_allowed_origins)

settings = Settings()
