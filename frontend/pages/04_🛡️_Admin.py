import streamlit as st
import requests
import os
from utils.api_client import BACKEND_URL
from utils.ui_components import set_professional_style, sidebar_branding

st.set_page_config(page_title="GalaxEye | Admin", page_icon="🛡️", layout="wide")

# Apply the global UI loop
set_professional_style()
sidebar_branding()

# --- ADMIN AUTHENTICATION ---
if "admin_authenticated" not in st.session_state:
    st.session_state["admin_authenticated"] = False

if not st.session_state["admin_authenticated"]:
    st.title("🛡️ Admin Login")
    # You can change 'admin123' to whatever password you like
    password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if password == "admin123":
            st.session_state["admin_authenticated"] = True
            st.success("Access Granted!")
            st.rerun()
        else:
            st.error("Invalid Credentials")
    st.stop()  # Prevents the rest of the page from loading

st.title("🛡️ System Administration")
if st.button("Logout"):
    st.session_state["admin_authenticated"] = False
    st.rerun()
st.markdown("---")

# Section 1: Model Health
st.subheader("📊 Model Status")
col1, col2, col3 = st.columns(3)
col1.metric("Model Version", "v1.0.4-Stable")
col2.metric("Architecture", "RandomForest")
col3.metric("Backend Status", "🟢 Online" if requests.get(f"{BACKEND_URL.replace('/classify', '')}/docs").status_code == 200 else "🔴 Offline")

st.markdown("---")

# Section 2: Model Retraining (FR09)
st.subheader("🔄 Retrain Classifier")
st.info("Upload a new CSV dataset to update the model's weights. The backend will merge this with existing data and perform a full retrain.")

uploaded_file = st.file_uploader("Select Training Dataset (CSV)", type="csv")

if st.button("🚀 Execute Retrain Sequence", type="primary"):
    if uploaded_file:
        with st.status("Initializing retraining engine...", expanded=True) as status:
            try:
                # Prepare the file for the POST request
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
                
                # Pointing to the /retrain endpoint on the backend
                # Note: We ensure the URL is correct (http://backend:8000/retrain)
                response = requests.post(f"http://backend:8000/retrain", files=files)
                
                if response.status_code == 200:
                    status.update(label="Retraining Complete!", state="complete")
                    st.success(response.json().get('message', "Model updated successfully."))
                else:
                    status.update(label="Retraining Failed", state="error")
                    st.error(f"Backend Error: {response.text}")
            except Exception as e:
                st.error(f"Could not connect to Backend: {e}")
    else:
        st.warning("Please upload a CSV file before attempting to retrain.")

# Section 3: System Logs
with st.expander("📄 View System Logs"):
    st.code("DEBUG: Model loaded from model_artifacts/astro_classifier_model.pkl\nINFO: API listening on port 8000\nSUCCESS: Connection established to frontend-gateway")