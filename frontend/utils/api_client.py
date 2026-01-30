import requests

# This assumes your backend runs on port 8000 (default for FastAPI)
BACKEND_URL = "http://127.0.0.1:8000"

def get_prediction(ra, dec):
    try:
        payload = {"ra": ra, "dec": dec}
        response = requests.post(f"{BACKEND_URL}/classify", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.text}"}
            
    except requests.exceptions.ConnectionError:
        return {"error": "Backend is offline. Is FastAPI running?"}