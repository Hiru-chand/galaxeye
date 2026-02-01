from fastapi import FastAPI, HTTPException
from backend.schemas.observation import CelestialObject, ClassificationResult
from backend.services.classifier import predict_object
from backend.services.data_fetcher import fetch_sdss_data # <--- IMPORT THIS

app = FastAPI(title="GalaxEye API", version="1.0")

@app.post("/classify", response_model=ClassificationResult)
def classify_celestial_object(data: CelestialObject):
    print(f"1. Received query: RA={data.ra}, DEC={data.dec}")
    
    # 2. Fetch Real Data from SDSS
    sdss_data = fetch_sdss_data(data.ra, data.dec)
    
    if not sdss_data:
        # If SDSS has no data, we cannot classify it
        raise HTTPException(status_code=404, detail="Object not found in SDSS Database")
    
    print(f"2. Fetched Data: u={sdss_data['u']}, g={sdss_data['g']}")

    # 3. Run ML Model (We pass the fetched data, not just coordinates)
    # Note: We will update predict_object later to actually use u,g,r,i,z
    result = predict_object(data.ra, data.dec)
    
    # 4. Return result
    return result