from fastapi import FastAPI
from backend.schemas.observation import CelestialObject, ClassificationResult
from backend.services.classifier import predict_object

app = FastAPI(title="GalaxEye API", version="1.0")

@app.get("/")
def home():
    return {"message": "GalaxEye Backend is running"}

@app.post("/classify", response_model=ClassificationResult)
def classify_celestial_object(data: CelestialObject):
    # 1. Receive data
    print(f"Received query: RA={data.ra}, DEC={data.dec}")
    
    # 2. Process data (Run ML Model)
    result = predict_object(data.ra, data.dec)
    
    # 3. Return result
    return result

# To run this: uvicorn backend.main:app --reload