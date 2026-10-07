from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup validation: confirm dataset presence
    if not settings.DATA_PATH.exists():
        print(f"[WARNING] Dataset not found at {settings.DATA_PATH}")
    else:
        print(f"[SECUREPAY-AI] Dataset verified at {settings.DATA_PATH} ({settings.DATA_PATH.stat().st_size:,} bytes)")
    yield
    # Shutdown logic if needed

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.get("/", summary="API Root")
async def root():
    return {
        "service": "SecurePay AI Backend API",
        "phase": "Phase 4 — Threshold Calibration Complete",
        "docs_url": "/docs",
        "health_url": f"{settings.API_V1_PREFIX}/health"
    }
