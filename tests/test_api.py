from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "triage_pipeline" in data["loaded_models"]

def test_predict_triage_valid():
    payload = {
        "subject": "Cannot access Jira after upgrading to 8.20",
        "body": "The Jira service throws a 503 error after our recent upgrade. This is blocking all engineering teams.",
        "answer": "Checked container logs, service is unresponsive."
    }
    response = client.post("/predict/triage", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Verify response schema keys
    assert "suggested_queue" in data
    assert "suggested_priority" in data
    assert isinstance(data["suggested_queue"], str)
    assert isinstance(data["suggested_priority"], str)

def test_predict_triage_missing_fields():
    # Missing 'body' field should fail Pydantic validation
    payload = {
        "subject": "Incomplete ticket request"
    }
    response = client.post("/predict/triage", json=payload)
    assert response.status_code == 422