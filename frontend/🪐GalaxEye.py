import streamlit as st
from utils.ui_components import set_professional_style, sidebar_branding

# Page Configuration
st.set_page_config(
    page_title="GalaxEye | Home",
    page_icon="🌌",
    layout="wide"
)

# Apply Global UI
set_professional_style()
sidebar_branding()

# --- HERO SECTION ---
st.title("🌌 GalaxEye: Autonomous Celestial Classifier")
st.subheader("High-Precision Multimodal Analysis of Deep Sky Objects")

st.markdown("""
    Welcome to the **GalaxEye Research Portal**. This platform leverages advanced machine learning 
    to classify astronomical sources—**Stars, Galaxies, and Quasars (QSOs)**—using multi-band 
    photometric data and automated cross-matching with global catalogs.
""")

st.divider()

# --- CORE FEATURES ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔭 Explorer")
    st.write("""
        Real-time target acquisition. Resolve objects via **Simbad**, 
        view interactive sky previews, and run instant classification 
        on manual photometric inputs.
    """)

with col2:
    st.markdown("### 📂 Batch Engine")
    st.write("""
        Process large-scale sky surveys. Upload CSV catalogs for 
        automated labeling, high-speed inference, and 
        data export for research use.
    """)

with col3:
    st.markdown("### 🔬 Insights")
    st.write("""
        Model explainability (XAI). Analyze feature importance 
        across the **u, g, r, i, z** and **WISE IR** bands to 
        understand the physics behind the prediction.
    """)

st.divider()

# --- TECHNICAL ARCHITECTURE ---
with st.expander("🛠️ System Architecture & Model Specifications"):
    st.write("""
        * **Engine:** FastAPI (Asynchronous Backend)
        * **Interface:** Streamlit (Reactive Frontend)
        * **Classifier:** Random Forest Ensemble (100+ Estimators)
        * **Data Sources:** SDSS Photometry & WISE Infrared Cross-matching
        * **Deployment:** Containerized via Docker & Railway.app
    """)

# --- CALL TO ACTION ---
st.info("💡 **Getting Started:** Use the sidebar to navigate to the **Explorer** and enter an object name like 'M31' or custom coordinates.")