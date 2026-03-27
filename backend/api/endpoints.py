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

# @router.post("/retrain")
# async def retrain_model(file: UploadFile = File(...)):
#     try:
#         # 1. Load existing data
#         # Ensure settings.DATA_PATH exists, otherwise create a new DF
#         if os.path.exists(settings.DATA_PATH):
#             current_df = pd.read_csv(settings.DATA_PATH)
#         else:
#             current_df = pd.DataFrame()

#         # 2. Read new data
#         content = await file.read()
#         new_df = pd.read_csv(io.BytesIO(content))
        
#         # CLEANING: Standardize column names
#         new_df.columns = new_df.columns.str.strip().str.lower()
        
#         # VALIDATION: Check for the label column
#         # If your CSV uses 'class' instead of 'class_label', fix it here:
#         if 'class' in new_df.columns:
#             new_df = new_df.rename(columns={'class': 'class_label'})
            
#         if 'class_label' not in new_df.columns:
#             raise HTTPException(status_code=400, detail="CSV must contain a 'class_label' column for retraining.")

#         # 3. Ingest & Save Dataset
#         combined_df = pd.concat([current_df, new_df], ignore_index=True)
#         combined_df.to_csv(settings.DATA_PATH, index=False)
        
#         # 4. Feature Engineering
#         X = pd.DataFrame()
#         X['u_g'] = combined_df['u'] - combined_df['g']
#         X['g_r'] = combined_df['g'] - combined_df['r']
#         X['r_i'] = combined_df['r'] - combined_df['i']
#         X['i_z'] = combined_df['i'] - combined_df['z']
#         X['z_w1'] = combined_df['z'] - combined_df['w1']
#         X['w1'] = combined_df['w1']
#         X['w2'] = combined_df['w2']
#         y = combined_df['class_label']
        
#         # 5. Train
#         model = RandomForestClassifier(n_estimators=100, random_state=42)
#         model.fit(X, y)
        
#         # 6. Save Model (Ensure directory exists)
#         os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
#         joblib.dump(model, settings.MODEL_PATH)
        
#         return {"message": f"Successfully retrained on {len(combined_df)} total records"}

#     except Exception as e:
#         # This will send the ACTUAL error message to the admin page
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/retrain")
async def retrain_model(file: UploadFile = File(...)):
    try:
        # 1. Load existing data
        if os.path.exists(settings.DATA_PATH):
            current_df = pd.read_csv(settings.DATA_PATH)
        else:
            current_df = pd.DataFrame()

        # 2. Read new data
        content = await file.read()
        
        if not content:
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")
        
        new_df = pd.read_csv(io.BytesIO(content))
        
        # CLEANING: Standardize column names
        new_df.columns = new_df.columns.str.strip().str.lower()
        
        # 3. Check for required columns
        required_columns = ['u', 'g', 'r', 'i', 'z', 'w1', 'w2']
        missing_columns = [col for col in required_columns if col not in new_df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {missing_columns}. Required: {required_columns}"
            )
        
        # 4. Handle class label column
        if 'class' in new_df.columns:
            new_df = new_df.rename(columns={'class': 'class_label'})
            
        if 'class_label' not in new_df.columns:
            raise HTTPException(
                status_code=400, 
                detail="CSV must contain a 'class_label' or 'class' column for retraining."
            )
        
        # 5. VALIDATION: Check class labels
        valid_classes = ['GALAXY', 'QSO', 'STAR']
        unique_classes = new_df['class_label'].unique()
        
        # Check for invalid class names
        invalid_classes = [cls for cls in unique_classes if cls not in valid_classes]
        if invalid_classes:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid class labels found: {invalid_classes}. "
                       f"Valid classes are: {valid_classes}"
            )
        
        # 6. CRITICAL: Ensure we have exactly 3 classes in the NEW data
        if len(unique_classes) < 3:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot retrain with only {len(unique_classes)} class(es). "
                       f"Found classes: {unique_classes.tolist()}. "
                       f"Training data must contain ALL THREE classes: GALAXY, QSO, STAR. "
                       f"Missing classes: {[cls for cls in valid_classes if cls not in unique_classes]}"
            )
        
        # 7. Check minimum samples per class in new data
        class_counts = new_df['class_label'].value_counts()
        min_samples = 10  # Minimum samples required per class
        
        for class_name in valid_classes:
            if class_counts[class_name] < min_samples:
                raise HTTPException(
                    status_code=400,
                    detail=f"Insufficient samples for class '{class_name}' in new data: {class_counts[class_name]} samples. "
                           f"Minimum required: {min_samples} samples per class."
                )
        
        # 8. Optional: Check for NaN values
        if new_df[required_columns].isnull().any().any():
            null_counts = new_df[required_columns].isnull().sum()
            raise HTTPException(
                status_code=400,
                detail=f"NaN values found in uploaded data: {null_counts[null_counts > 0].to_dict()}"
            )
        
        # 9. Combine with existing data
        combined_df = pd.concat([current_df, new_df], ignore_index=True)
        
        # 10. Remove duplicates if any (optional)
        feature_cols = required_columns + ['class_label']
        combined_df = combined_df.drop_duplicates(subset=feature_cols, keep='last')
        
        # 11. Save the combined dataset
        combined_df.to_csv(settings.DATA_PATH, index=False)
        
        # 12. Feature Engineering
        X = pd.DataFrame()
        X['u_g'] = combined_df['u'] - combined_df['g']
        X['g_r'] = combined_df['g'] - combined_df['r']
        X['r_i'] = combined_df['r'] - combined_df['i']
        X['i_z'] = combined_df['i'] - combined_df['z']
        X['z_w1'] = combined_df['z'] - combined_df['w1']
        X['w1'] = combined_df['w1']
        X['w2'] = combined_df['w2']
        y = combined_df['class_label']
        
        # 13. Check for NaN in features after engineering
        if X.isnull().any().any():
            null_counts = X.isnull().sum()
            raise HTTPException(
                status_code=400,
                detail=f"NaN values found after feature engineering: {null_counts[null_counts > 0].to_dict()}"
            )
        
        # 14. Final validation: Check total classes in combined dataset
        total_classes = y.unique()
        if len(total_classes) < 3:
            raise HTTPException(
                status_code=400,
                detail=f"Combined dataset has only {len(total_classes)} class(es): {total_classes.tolist()}. "
                       f"Must have all three classes (GALAXY, QSO, STAR) to train a valid model."
            )
        
        # 15. Train the model
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import cross_val_score
        
        # Configure RandomForest with better parameters
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        # Optional: Perform cross-validation to check model quality
        try:
            cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()
            print(f"Cross-validation accuracy: {cv_mean:.3f} (+/- {cv_std:.3f})")
            
            # Warn if cross-validation accuracy is too low
            if cv_mean < 0.7:
                print(f"Warning: Low cross-validation accuracy ({cv_mean:.3f}). Model may not perform well.")
        except Exception as e:
            print(f"Warning: Cross-validation failed: {e}")
        
        # Train the final model
        model.fit(X, y)
        
        # 16. Final validation: Ensure model has exactly 3 classes
        if len(model.classes_) != 3:
            raise HTTPException(
                status_code=500,
                detail=f"Model trained with {len(model.classes_)} classes, but expected 3. "
                       f"Classes: {model.classes_.tolist()}"
            )
        
        # 17. Create backup of existing model before saving
        if os.path.exists(settings.MODEL_PATH):
            import shutil
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{settings.MODEL_PATH}.backup_{timestamp}"
            shutil.copy2(settings.MODEL_PATH, backup_path)
            print(f"Created backup at: {backup_path}")
        
        # 18. Save the new model
        os.makedirs(os.path.dirname(settings.MODEL_PATH), exist_ok=True)
        joblib.dump(model, settings.MODEL_PATH)
        
        # 19. Return comprehensive response
        return {
            "message": "Successfully retrained model with 3 classes!",
            "details": {
                "total_records": len(combined_df),
                "new_records": len(new_df),
                "existing_records": len(current_df),
                "class_distribution": class_counts.to_dict(),
                "model_classes": model.classes_.tolist(),
                "cross_validation_accuracy": cv_mean if 'cv_mean' in locals() else None,
                "backup_created": backup_path if 'backup_path' in locals() else None
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        # This will send the ACTUAL error message to the admin page
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")
    finally:
        await file.close()