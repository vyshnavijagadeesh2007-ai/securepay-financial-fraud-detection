from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_api_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "SecurePay AI Backend API" in data["service"]

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["dataset"]["exists"] is True
    assert data["dataset"]["expected_rows"] == 284807
    assert data["ml_engine"]["isolation_forest_status"] in ["NOT TRAINED", "READY"]

def test_dashboard_endpoint():
    response = client.get("/api/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total_transactions"] == 284807
    assert data["legitimate_transactions"] == 284315
    assert data["fraud_transactions"] == 492

def test_models_comparison_endpoint():
    response = client.get("/api/models/comparison")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["NOT_TRAINED", "EVALUATED"]
    assert len(data["models"]) == 2
    assert data["models"][0]["model_name"] == "Isolation Forest"
    assert data["models"][1]["model_name"] == "Local Outlier Factor"
    assert data["models"][1]["status"] in ["NOT_TRAINED", "READY"]

def test_predict_phase0_contract():
    payload = {
        "transaction": {
            "Time": 406.0,
            "Amount": 149.62,
            "V1": 0.0, "V2": 0.0, "V3": 0.0, "V4": 0.0, "V5": 0.0,
            "V6": 0.0, "V7": 0.0, "V8": 0.0, "V9": 0.0, "V10": 0.0,
            "V11": 0.0, "V12": 0.0, "V13": 0.0, "V14": 0.0, "V15": 0.0,
            "V16": 0.0, "V17": 0.0, "V18": 0.0, "V19": 0.0, "V20": 0.0,
            "V21": 0.0, "V22": 0.0, "V23": 0.0, "V24": 0.0, "V25": 0.0,
            "V26": 0.0, "V27": 0.0, "V28": 0.0
        },
        "model": "Isolation Forest"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["MODEL_NOT_TRAINED", "NORMAL", "POTENTIAL ANOMALY"]

def test_analytics_endpoint():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert data["dataset_name"] == "creditcard.csv"
    assert data["total_observations"] == 284807
    assert data["total_features"] == 31
    assert data["class_distribution"]["legitimate_count"] == 284315
    assert data["class_distribution"]["fraud_count"] == 492
    assert data["status"] == "VERIFIED"

def test_models_list_endpoint():
    response = client.get("/api/models")
    assert response.status_code == 200
    data = response.json()
    assert len(data["models"]) == 2
    assert data["models"][0]["name"] == "Isolation Forest"
    assert data["models"][0]["status"] in ["NOT TRAINED", "READY"]
    assert data["models"][1]["name"] == "Local Outlier Factor"
    assert data["models"][1]["status"] in ["NOT TRAINED", "READY"]

def test_threshold_endpoint():
    response = client.get("/api/threshold?model=Isolation Forest")
    assert response.status_code == 200
    data = response.json()
    assert data["selected_model"] == "Isolation Forest"
    assert len(data["contamination_experiments"]) in [5, 7]

def test_transactions_endpoint():
    response = client.get("/api/transactions?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 284807
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["records"]) == 10
    for rec in data["records"]:
        assert rec["anomaly_score"] is None
        assert rec["status"] == "PENDING_INFERENCE"

def test_predict_batch_phase0_contract():
    payload = {
        "transactions": [
            {
                "Time": 0.0, "Amount": 10.0,
                **{f"V{i}": 0.0 for i in range(1, 29)}
            }
        ],
        "model": "Isolation Forest"
    }
    response = client.post("/api/predict/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["total_processed"] == 1
    assert len(data["predictions"]) == 1

def test_predict_lof_contract():
    payload = {
        "transaction": {
            "Time": 406.0,
            "Amount": 149.62,
            "V1": 0.0, "V2": 0.0, "V3": 0.0, "V4": 0.0, "V5": 0.0,
            "V6": 0.0, "V7": 0.0, "V8": 0.0, "V9": 0.0, "V10": 0.0,
            "V11": 0.0, "V12": 0.0, "V13": 0.0, "V14": 0.0, "V15": 0.0,
            "V16": 0.0, "V17": 0.0, "V18": 0.0, "V19": 0.0, "V20": 0.0,
            "V21": 0.0, "V22": 0.0, "V23": 0.0, "V24": 0.0, "V25": 0.0,
            "V26": 0.0, "V27": 0.0, "V28": 0.0
        },
        "model": "Local Outlier Factor"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["MODEL_NOT_TRAINED", "NORMAL", "POTENTIAL ANOMALY"]
    if data["status"] != "MODEL_NOT_TRAINED":
        assert data["anomaly_score"] is not None
        assert data["prediction"] in [0, 1]


