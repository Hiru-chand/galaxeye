import streamlit as st
import pandas as pd
from utils.api_client import upload_batch
from utils.ui_components import set_professional_style, sidebar_branding

st.set_page_config(page_title="GalaxEye | Batch Processing", layout="wide", page_icon="📂")

# Apply the global UI loop
set_professional_style()
sidebar_branding()

# --- 1. PROFESSIONAL STYLING (Restored from your app.py) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(5, 10, 20, 0.3), rgba(5, 10, 20, 0.3)), 
                    url('https://pixabay.com/gifs/galaxy-universe-cosmos-sky-3468/');
        background-size: cover; background-attachment: fixed;
    }
    .block-container {
        background: rgba(16, 20, 30, 0.6); backdrop-filter: blur(10px);
        border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📂 Bulk Catalog Processing")
st.caption("High-throughput classification for large astronomical datasets")

with st.container(border=True):
    uploaded_file = st.file_uploader("Drop CSV file here", type="csv")
    
    if uploaded_file:
        try:
            # Load and sanitize columns exactly as in your original code
            batch_df = pd.read_csv(uploaded_file)
            batch_df.columns = batch_df.columns.str.strip().str.lower()
            st.write(f"✅ Loaded {len(batch_df)} objects.")
            
            required_cols = ['u', 'g', 'r', 'i', 'z', 'w1', 'w2']
            missing_cols = [col for col in required_cols if col not in batch_df.columns]
            
            if missing_cols:
                st.error(f"Missing columns: {missing_cols}")
                st.info("Please ensure headers are: u, g, r, i, z, w1, w2")
            else:
                if st.button("Process Batch Queue", type="primary"):
                    # Using the professional status component from your UI
                    with st.status("Analyzing catalog...", expanded=True) as status:
                        try:
                            # Call backend
                            results = upload_batch(uploaded_file)
            
                            # Check if results is actually a list (JSON records)
                            if isinstance(results, list):
                                processed_df = pd.DataFrame(results)
                                status.update(label="Complete!", state="complete")
                                st.dataframe(processed_df)
                            else:
                                st.error(f"Backend returned unexpected data: {results}")
                
                        except Exception as e:
                            st.error(f"Error processing file: {e}")
                        st.write("Extracting feature combinations...")
                        # Call backend API
                        results = upload_batch(uploaded_file)
                        
                        if results:
                            processed_df = pd.DataFrame(results)
                            status.update(label="Classification Complete!", state="complete", expanded=False)
                            
                            st.success("Batch Processing Successful!")
                            st.dataframe(processed_df.head(10), use_container_width=True)
                            
                            csv = processed_df.to_csv(index=False).encode('utf-8')
                            st.download_button("📥 Download Classified Catalog", csv, "galaxeye_results.csv", "text/csv")
        except Exception as e:
            st.error(f"Error processing file: {e}")