import joblib
import pandas as pd
import numpy as np
import os

MODEL_PATH = "../model_artifacts/astro_classifier_model.pkl"

def get_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None

def predict_single(data):
    model = get_model()
    # Feature Engineering
    features = {
        'u_g': data.u - data.g, 'g_r': data.g - data.r,
        'r_i': data.r - data.i, 'i_z': data.i - data.z,
        'z_w1': data.z - data.w1, 'w1': data.w1, 'w2': data.w2
    }
    df = pd.DataFrame([features])
    
    pred = model.predict(df)[0]
    probs = model.predict_proba(df)[0]
    return pred, float(np.max(probs)), probs.tolist()

def predict_batch(df):
    model = get_model()
    df.columns = df.columns.str.strip().str.lower()
    
    X = pd.DataFrame()
    X['u_g'] = df['u'] - df['g']
    X['g_r'] = df['g'] - df['r']
    X['r_i'] = df['r'] - df['i']
    X['i_z'] = df['i'] - df['z']
    X['z_w1'] = df['z'] - df['w1']
    X['w1'] = df['w1']
    X['w2'] = df['w2']
    
    df['GalaxEye_Class'] = model.predict(X)
    return df