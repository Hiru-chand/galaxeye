from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_main():
    # Simple health check test
    response = client.get("/")
    assert response.status_code in [200, 404] # Depending if you defined a root /

def test_classification_logic():
    # Test the API with dummy data
    payload = {
        "u": 19.0, "g": 18.5, "r": 18.0, 
        "i": 17.5, "z": 17.0, "w1": 16.0, "w2": 15.5
    }
    response = client.post("/classify", json=payload)
    assert response.status_code == 200
    assert "prediction" in response.json()