import streamlit as st
from utils.ui_components import set_professional_style, sidebar_branding

st.set_page_config(page_title="GalaxEye Hub", layout="wide")
# Apply the global UI loop
set_professional_style()
sidebar_branding()

st.title("🔭 GalaxEye: Multimodal Celestial Classifier")
st.markdown("""
### Welcome to the GalaxEye Research Portal
Use the sidebar to navigate between single object analysis and batch processing.
- **Explorer:** Search by name or coordinates.
- **Batch:** Upload large catalogs for automated labeling.
""")