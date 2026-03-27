from fastapi import APIRouter, UploadFile, File, HTTPException
from core.config import settings
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
import io
import numpy as np
import os

router = APIRouter()

# Helper function to load the model
def get_model():
    try:
        return joblib.load(settings.MODEL_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model not found: {e}")
    
# --- FR02: Single Object Classification ---
@router.post("/classify")
async def classify_object(data: dict):
    model = get_model()
    
    # 1. Feature Engineering (Must match your training exactly)
    # We create the color indices from the raw mags sent by the frontend
    try:
        u, g, r = data['u'], data['g'], data['r']
        i, z, w1, w2 = data['i'], data['z'], data['w1'], data['w2']
        
        features = np.array([[
            u - g,  # u_g
            g - r,  # g_r
            r - i,  # r_i
            i - z,  # i_z
            z - w1, # z_w1
            w1,     # w1
            w2      # w2
        ]])
        
        # 2. Prediction
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0].tolist()
        confidence = max(probabilities)
        
        return {
            "prediction": str(prediction),
            "confidence": float(confidence),
            "probabilities": probabilities
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Data processing error: {e}")

# --- FR05: Batch Processing ---
@router.post("/batch-upload")
async def batch_classify(file: UploadFile = File(...)):
    try:
        # 1. Read the content
        content = await file.read()
        
        # 2. Check if we actually got data
        if not content:
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")

        # 3. Use BytesIO to turn the raw bytes into a file-like object for pandas
        df = pd.read_csv(io.BytesIO(content))
        
        # 4. Standardize columns (Important for your test_batch.csv)
        df.columns = df.columns.str.strip().str.lower()

        # 5. Load the model inside the function to ensure it's fresh
        model = joblib.load(settings.MODEL_PATH)

        # 6. Feature Engineering (Color Indices)
        # Based on your test_batch.csv: u,g,r,i,z,w1,w2
        X = pd.DataFrame()
        X['u_g'] = df['u'] - df['g']
        X['g_r'] = df['g'] - df['r']
        X['r_i'] = df['r'] - df['i']
        X['i_z'] = df['i'] - df['z']
        X['z_w1'] = df['z'] - df['w1']
        X['w1'] = df['w1']
        X['w2'] = df['w2']

        # 7. Predict
        df['prediction'] = model.predict(X)
        probs = model.predict_proba(X)
        df['confidence'] = [round(max(p) * 100, 2) for p in probs]

        return df.to_dict(orient="records")

    except Exception as e:
        # This will now show the actual error in the Streamlit UI
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await file.close() # Clean up the temp file

@router.post("/retrain")
async def retrain_model(file: UploadFile = File(...)):
    try:
        # 1. Load existing data
        # Ensure settings.DATA_PATH exists, otherwise create a new DF
        if os.path.exists(settings.DATA_PATH):
            current_df = pd.read_csv(settings.DATA_PATH)
        else:
            current_df = pd.DataFrame()

        # 2. Read new data
        content = await file.read()
        new_df = pd.read_csv(io.BytesIO(content))
        
        # CLEANING: Standardize column names
        new_df.columns = new_df.columns.str.strip().str.lower()
        
        # VALIDATION: Check for the label column
        # If your CSV uses 'class' instead of 'class_label', fix it here:
        if 'class' in new_df.columns:
            new_df = new_df.rename(columns={'class': 'class_label'})
            
        if 'class_label' not in new_df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain a 'class_label' column for retraining.")

        # 3. Ingest & Save Dataset
        combined_df = pd.concat([current_df, new_df], ignore_index=True)
        combined_df.to_csv(settings.DATA_PATH, index=False)
        
        # 4. Feature Engineering
        X = pd.DataFrame()
        X['u_g'] = combined_df['u'] - combined_df['g']
        X['g_r'] = combined_df['g'] - combined_df['r']
        X['r_i'] = combined_df['r'] - combined_df['i']
        X['i_z'] = combined_df['i'] - combined_df['z']
        X['z_w1'] = combined_df['z'] - combined_df['w1']
        X['w1'] = combined_df['w1']
        X['w2'] = combined_df['w2']
        y = combined_df['class_label']
        
        # 5. Train
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X, y)
        
        # 6. Save Model (Ensure directory exists)
        os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
        joblib.dump(model, settings.MODEL_PATH)
        
        return {"message": f"Successfully retrained on {len(combined_df)} total records"}

    except Exception as e:
        # This will send the ACTUAL error message to the admin page
        raise HTTPException(status_code=500, detail=str(e))