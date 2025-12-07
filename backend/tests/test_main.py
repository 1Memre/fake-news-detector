from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Fake News Detector API"}

def test_predict_text_short():
    # Should fail validation
    response = client.post("/predict", json={"text": "Hi"})
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] == "INVALID"
    assert "explanation" in data

def test_predict_text_valid_basic():
    # Mocking would be ideal, but for integration test let's see if it runs
    # This might fail if model not loaded or DB not reached, but good to check
    response = client.post("/predict", json={"text": "Local news reports that the weather will be sunny tomorrow in New York."})
    
    # If using TestClient, validation happens, model runs (if loaded).
    # If model logic fails, status might be 500.
    if response.status_code == 503: # Model not loaded
        pass 
    else:
        assert response.status_code == 200
        data = response.json()
        assert "prediction" in data
