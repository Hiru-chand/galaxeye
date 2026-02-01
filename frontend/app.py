import streamlit as st
# Since we are inside the 'frontend' folder, we import directly from 'utils'
from utils.api_client import get_prediction

# Page Config
st.set_page_config(page_title="GalaxEye", page_icon="🔭", layout="wide")

# Title and Header
st.title("🔭 GalaxEye: Celestial Object Classifier")
st.markdown("Enter coordinates (RA/DEC) to classify objects as **Star**, **Galaxy**, or **Quasar**.")

# 1. Input Section
col1, col2 = st.columns(2)

with col1:
    ra_input = st.number_input("Right Ascension (RA)", min_value=0.0, max_value=360.0, value=10.5)
with col2:
    dec_input = st.number_input("Declination (DEC)", min_value=-90.0, max_value=90.0, value=41.2)

# Add this helper function to generate the image URL

def get_legacy_survey_image_url(ra, dec):
    """
    Fetches an image from the DESI Legacy Imaging Surveys.
    """
    # layer=ls-dr10: Data Release 10 (most recent)
    # size=400: Image size in pixels
    # pixscale=0.262: Resolution (standard for Legacy Survey)
    return f"https://www.legacysurvey.org/viewer/cutout.jpg?ra={ra}&dec={dec}&layer=ls-dr10&size=400&pixscale=0.262"

st.subheader("Target Visualization")

image_url = get_legacy_survey_image_url(ra_input, dec_input)

st.image(image_url, caption=f"Legacy Survey View (RA: {ra_input}, DEC: {dec_input})", use_container_width=False)

# 2. Action Button
if st.button("Classify Object", type="primary"):
    
    # Show a spinner while waiting (Simulates processing time)
    with st.spinner("Analyzing spectral data..."):
        result = get_prediction(ra_input, dec_input)
    
    # 3. Display Results
    if "error" in result:
        st.error(result["error"])
    else:
        st.success("Classification Complete!")
        
        # Display metrics nicely
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="Predicted Class", value=result['object_class'])
        with res_col2:
            st.metric(label="Confidence Score", value=f"{result['confidence'] * 100}%")

        # Visual enhancement
        if result['object_class'] == "Galaxy":
            st.info("ℹ️ This object shows broadened spectral lines typical of galaxies.")