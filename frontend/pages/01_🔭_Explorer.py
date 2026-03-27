# import streamlit as st
# import pandas as pd
# import numpy as np
# from utils.api_client import get_prediction

# st.set_page_config(page_title="Object Explorer", layout="wide")

# # --- CSS for Professional Styling (Consistent with your app.py) ---
# st.markdown("""
#     <style>
#     .block-container {
#         background: rgba(16, 20, 30, 0.6); 
#         backdrop-filter: blur(10px); 
#         border-radius: 20px;
#         padding: 2rem;
#     }
#     .stButton>button {
#         background: linear-gradient(90deg, #0d6efd 0%, #0dcaf0 100%);
#         color: white;
#         font-weight: bold;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# st.title("🔭 Celestial Explorer")
# st.caption("Identify Target and Run Photometric Analysis")

# # Initialize session state for coordinates if not present 
# if 'ra' not in st.session_state:
#     st.session_state['ra'] = 10.6847  # Default: M31
# if 'dec' not in st.session_state:
#     st.session_state['dec'] = 41.2687

# col_input, col_vis = st.columns([1, 1.2], gap="large")

# # --- SECTION 1: TARGET ACQUISITION (FR01) ---
# with col_input:
#     with st.container(border=True):
#         st.subheader("1. Identify Target")
        
#         # Method selection from your updated UI 
#         input_method = st.radio("Search Method", ["Coordinates", "Object Name"], horizontal=True)
        
#         if input_method == "Object Name":
#             obj_name = st.text_input("Simbad Resolver", placeholder="e.g. M31 or Andromeda")
#             if st.button("Resolve Target"):
#                 # In the new architecture, we call the backend or use local utility 
#                 from astropy.coordinates import SkyCoord
#                 try:
#                     coord = SkyCoord.from_name(obj_name)
#                     st.session_state.ra = coord.ra.deg
#                     st.session_state.dec = coord.dec.deg
#                     st.success(f"Target Locked: {obj_name}")
#                 except:
#                     st.error("Could not resolve name via Simbad.")
        
#         c1, c2 = st.columns(2)
#         ra = c1.number_input("Right Ascension", value=st.session_state.ra, format="%.4f")
#         dec = c2.number_input("Declination", value=st.session_state.dec, format="%.4f")
        
#         # Save to session state for the interactive map page
#         st.session_state['ra'] = ra
#         st.session_state['dec'] = dec
        
#         if st.button("Fetch Sky Preview (FR07)"):
#             # Static visualization URL from your logic 
#             img_url = f"https://www.legacysurvey.org/viewer/cutout.jpg?ra={ra}&dec={dec}&layer=ls-dr10&pixscale=0.5&size=400"
#             st.image(img_url, caption="Target Visual Acquisition", use_container_width=True)

# # --- SECTION 2: CLASSIFICATION (FR02, FR04, FR11) ---
# with col_vis:
#     with st.container(border=True):
#         st.subheader("2. Photometric Data")
#         st.info("Input SDSS (Optical) & WISE (Infrared) Magnitudes")
        
#         # Input grid exactly as per your uploaded app.py 
#         m1, m2, m3 = st.columns(3)
#         u_mag = m1.number_input("u-mag", value=19.0)
#         g = m2.number_input("g-mag", value=18.5)
#         r = m3.number_input("r-mag", value=18.0)
        
#         m4, m5, m6, m7 = st.columns(4)
#         i = m4.number_input("i-mag", value=17.5)
#         z = m5.number_input("z-mag", value=17.0)
#         w1 = m6.number_input("W1 (IR)", value=16.0)
#         w2 = m7.number_input("W2 (IR)", value=15.5)

#         if st.button("Run Classification Analysis", type="primary"):
#             # Prepare payload for the Backend API
#             payload = {
#                 "u": u_mag, "g": g, "r": r, 
#                 "i": i, "z": z, "w1": w1, "w2": w2
#             }
            
#             try:
#                 # Call the API Client 
#                 result = get_prediction(payload)
                
#                 st.divider()
#                 res_col1, res_col2 = st.columns(2)
                
#                 with res_col1:
#                     st.metric("Predicted Class", result['prediction'])
#                 with res_col2:
#                     st.metric("Confidence Score", f"{result['confidence'] * 100:.2f}%")
                
#                 # Anomaly Detection Logic (FR11) 
#                 if (result['confidence'] * 100) < 50:
#                     st.warning("⚠️ **ANOMALY DETECTED:** The model is unsure. This may be a Variable Star, Supernova, or Data Artifact.")
                
#                 # Confidence chart 
#                 prob_data = pd.DataFrame({
#                     'Class': ['GALAXY', 'QSO', 'STAR'], # Order depends on your model classes
#                     'Confidence': result['probabilities']
#                 })
#                 st.bar_chart(prob_data.set_index('Class'))
                
#             except Exception as e:
#                 st.error(f"Backend Connection Error. Ensure the FastAPI service is running. Details: {e}")


#========================2nd========================================

# import streamlit as st
# import pandas as pd
# import numpy as np
# import streamlit.components.v1 as components
# from utils.api_client import get_prediction
# from astropy.coordinates import SkyCoord

# st.set_page_config(page_title="GalaxEye | Explorer", page_icon="🔭", layout="wide")

# # --- CSS for Professional Styling ---
# st.markdown("""
#     <style>
#     .block-container {
#         background: rgba(16, 20, 30, 0.6); 
#         backdrop-filter: blur(10px); 
#         border-radius: 20px;
#         padding: 2rem;
#     }
#     .stButton>button {
#         background: linear-gradient(90deg, #0d6efd 0%, #0dcaf0 100%);
#         color: white;
#         font-weight: bold;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# st.title("🔭 Celestial Explorer")
# st.caption("Identify Target and Run Photometric Analysis")

# # Initialize session state for coordinates
# if 'ra' not in st.session_state:
#     st.session_state['ra'] = 10.6847  # Default: M31
# if 'dec' not in st.session_state:
#     st.session_state['dec'] = 41.2687

# # --- TABS DEFINITION ---
# tab_input, tab_map, tab_insights = st.tabs(["📝 Classification & Target", "🗺️ Interactive Explorer", "🔬 Model Explainability"])

# # --- TAB 1: CLASSIFICATION & TARGET ACQUISITION ---
# with tab_input:
#     col_target, col_photo = st.columns([1, 1.2], gap="large")

#     with col_target:
#         with st.container(border=True):
#             st.subheader("1. Identify Target (FR01)")
#             input_method = st.radio("Search Method", ["Coordinates", "Object Name"], horizontal=True)
            
#             if input_method == "Object Name":
#                 obj_name = st.text_input("Simbad Resolver", placeholder="e.g. M31 or Andromeda")
#                 if st.button("Resolve Target"):
#                     try:
#                         coord = SkyCoord.from_name(obj_name)
#                         st.session_state.ra = coord.ra.deg
#                         st.session_state.dec = coord.dec.deg
#                         st.success(f"Target Locked: {obj_name}")
#                         st.rerun() # Refresh to update number inputs
#                     except:
#                         st.error("Could not resolve name via Simbad.")
            
#             c1, c2 = st.columns(2)
#             ra = c1.number_input("Right Ascension", value=st.session_state.ra, format="%.4f", key="ra_input")
#             dec = c2.number_input("Declination", value=st.session_state.dec, format="%.4f", key="dec_input")
            
#             # Update global session state
#             st.session_state['ra'] = ra
#             st.session_state['dec'] = dec
            
#             if st.button("Fetch Sky Preview (FR07)"):
#                 img_url = f"https://www.legacysurvey.org/viewer/cutout.jpg?ra={ra}&dec={dec}&layer=ls-dr10&pixscale=0.5&size=400"
#                 st.image(img_url, caption="Target Visual Acquisition", use_container_width=True)

#     with col_photo:
#         with st.container(border=True):
#             st.subheader("2. Photometric Data (FR02)")
#             st.info("Input SDSS (Optical) & WISE (Infrared) Magnitudes")
            
#             m1, m2, m3 = st.columns(3)
#             u_mag = m1.number_input("u-mag", value=19.43)
#             g_mag = m2.number_input("g-mag", value=19.03)
#             r_mag = m3.number_input("r-mag", value=18.87)
            
#             m4, m5, m6, m7 = st.columns(4)
#             i_mag = m4.number_input("i-mag", value=18.61)
#             z_mag = m5.number_input("z-mag", value=18.58)
#             w1_mag = m6.number_input("W1 (IR)", value=14.80)
#             w2_mag = m7.number_input("W2 (IR)", value=14.01)

#             if st.button("Run Classification Analysis", type="primary", use_container_width=True):
#                 payload = {
#                     "u": u_mag, "g": g_mag, "r": r_mag, 
#                     "i": i_mag, "z": z_mag, "w1": w1_mag, "w2": w2_mag
#                 }
                
#                 try:
#                     result = get_prediction(payload)
#                     st.divider()
#                     res_col1, res_col2 = st.columns(2)
                    
#                     with res_col1:
#                         st.metric("Predicted Class", result['prediction'])
#                     with res_col2:
#                         # Ensure confidence is handled as float 0-1 or 0-100
#                         conf_val = result['confidence'] * 100 if result['confidence'] <= 1 else result['confidence']
#                         st.metric("Confidence Score", f"{conf_val:.2f}%")
                    
#                     # Anomaly Detection Logic (FR11)
#                     if conf_val < 50:
#                         st.warning("⚠️ **ANOMALY DETECTED:** Model uncertainty is high.")
                    
#                     # Store results in session state for Tab 3
#                     st.session_state['last_result'] = result
                    
#                 except Exception as e:
#                     st.error(f"Backend Connection Error: {e}")

#========================3rd========================================

# import streamlit as st
# import pandas as pd
# import numpy as np
# import streamlit.components.v1 as components
# from utils.api_client import get_prediction
# from astropy.coordinates import SkyCoord
# from utils.ui_components import set_professional_style, sidebar_branding

# st.set_page_config(page_title="GalaxEye | Explorer", page_icon="🔭", layout="wide")

# # Apply the global UI loop
# set_professional_style()
# sidebar_branding()

# # --- CSS for Professional Styling ---
# st.markdown("""
#     <style>
#     .block-container { background: rgba(16, 20, 30, 0.6); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; }
#     .stButton>button { background: linear-gradient(90deg, #0d6efd 0%, #0dcaf0 100%); color: white; font-weight: bold; width: 100%; }
#     </style>
#     """, unsafe_allow_html=True)

# st.title("🔭 Celestial Explorer")

# # Initialize session state
# if 'ra' not in st.session_state: st.session_state['ra'] = 10.6847
# if 'dec' not in st.session_state: st.session_state['dec'] = 41.2687
# if 'prediction_result' not in st.session_state: st.session_state['prediction_result'] = None

# tab_input, tab_map = st.tabs(["📝 Classification & Target", "🗺️ Interactive Explorer"])

# with tab_input:
#     col_target, col_photo = st.columns([1, 1.2], gap="large")

#     with col_target:
#         with st.container(border=True):
#             st.subheader("1. Identify Target")
#             input_method = st.radio("Search Method", ["Coordinates", "Object Name"], horizontal=True)
            
#             if input_method == "Object Name":
#                 obj_name = st.text_input("Simbad Resolver", placeholder="e.g. M31")
#                 if st.button("Resolve Target"):
#                     try:
#                         # Adding a timeout and clearing any whitespace
#                         coord = SkyCoord.from_name(obj_name.strip())
#                         st.session_state.ra = coord.ra.deg
#                         st.session_state.dec = coord.dec.deg
#                         st.success(f"Target Locked: {obj_name}")
#                         st.rerun()
#                     except Exception as e:
#                         st.error(f"Simbad Error: Ensure your Docker container has internet access. (Details: {e})")
            
#             c1, c2 = st.columns(2)
#             ra = c1.number_input("Right Ascension", value=st.session_state.ra, format="%.4f")
#             dec = c2.number_input("Declination", value=st.session_state.dec, format="%.4f")
#             st.session_state.ra, st.session_state.dec = ra, dec
            
#             if st.button("Fetch Sky Preview"):
#                 img_url = f"https://www.legacysurvey.org/viewer/cutout.jpg?ra={ra}&dec={dec}&layer=ls-dr10&pixscale=0.5&size=400"
#                 st.image(img_url, caption="Target Visual Acquisition")

#     with col_photo:
#         with st.container(border=True):
#             st.subheader("2. Photometric Data")
#             m1, m2, m3 = st.columns(3)
#             u = m1.number_input("u-mag", value=19.43)
#             g = m2.number_input("g-mag", value=19.03)
#             r = m3.number_input("r-mag", value=18.87)
            
#             m4, m5, m6, m7 = st.columns(4)
#             i, z = m4.number_input("i-mag", value=18.61), m5.number_input("z-mag", value=18.58)
#             w1, w2 = m6.number_input("W1 (IR)", value=14.80), m7.number_input("W2 (IR)", value=14.01)

#             if st.button("Run Classification Analysis", type="primary"):
#                 try:
#                     res = get_prediction({"u": u, "g": g, "r": r, "i": i, "z": z, "w1": w1, "w2": w2})
#                     st.session_state['prediction_result'] = res
#                 except Exception as e:
#                     st.error(f"Backend Offline: {e}")

#         #--- RESULTS & ANOMALY DETECTION (FR11) ---
#         if st.session_state['prediction_result']:
#             res = st.session_state['prediction_result']
#             st.divider()
            
#             # 1. Calculation
#             # Standardize confidence to 0-100
#             conf_val = res['confidence'] * 100 if res['confidence'] <= 1 else res['confidence']
            
#             # 2. Display Metrics
#             r1, r2 = st.columns(2)
#             r1.metric("Predicted Class", res['prediction'])
#             r2.metric("Confidence Score", f"{conf_val:.2f}%")

#             # 3. ANOMALY DETECTION LOGIC (FR11)
#             # If confidence is low, or if the gap between top 2 classes is small
#             if conf_val < 50:
#                 st.warning("""
#                     ⚠️ **ANOMALY DETECTED** The model's confidence is below the 50% threshold. This object may be:
#                     * A rare transient (Supernova/Variable Star)
#                     * An out-of-distribution data artifact
#                     * An overlapping/blended source
#                 """)
#             elif res['prediction'] == "QSO" and conf_val < 70:
#                 st.info("💡 **Note:** Quasars (QSO) often mimic Star-like profiles in optical data.")

#             #4. Confidence Chart
#             st.write("### 📊 Probability Distribution")
#             chart_data = pd.DataFrame({
#                 'Class': ['GALAXY', 'QSO', 'STAR'],
#                 'Probability': [round(p * 100, 2) for p in res['probabilities']]
#             }).set_index('Class')
#             st.write("DEBUG - Raw Backend Response:", res)
#             st.bar_chart(chart_data)

# with tab_map:
#     components.iframe(f"https://www.legacysurvey.org/viewer/?ra={st.session_state.ra}&dec={st.session_state.dec}&layer=ls-dr10&zoom=13", height=700)

#========================4th========================================

import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
from utils.api_client import get_prediction
from astropy.coordinates import SkyCoord
from utils.ui_components import set_professional_style, sidebar_branding

st.set_page_config(page_title="GalaxEye | Explorer", page_icon="🔭", layout="wide")

# Apply the global UI loop
set_professional_style()
sidebar_branding()

# --- CSS for Professional Styling ---
st.markdown("""
    <style>
    .block-container { background: rgba(16, 20, 30, 0.6); backdrop-filter: blur(10px); border-radius: 20px; padding: 2rem; }
    .stButton>button { background: linear-gradient(90deg, #0d6efd 0%, #0dcaf0 100%); color: white; font-weight: bold; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔭 Celestial Explorer")

# Initialize session state
if 'ra' not in st.session_state: st.session_state['ra'] = 10.6847
if 'dec' not in st.session_state: st.session_state['dec'] = 41.2687
if 'prediction_result' not in st.session_state: st.session_state['prediction_result'] = None

tab_input, tab_map = st.tabs(["📝 Classification & Target", "🗺️ Interactive Explorer"])

with tab_input:
    col_target, col_photo = st.columns([1, 1.2], gap="large")

    with col_target:
        with st.container(border=True):
            st.subheader("1. Identify Target")
            input_method = st.radio("Search Method", ["Coordinates", "Object Name"], horizontal=True)
            
            if input_method == "Object Name":
                obj_name = st.text_input("Simbad Resolver", placeholder="e.g. M31")
                if st.button("Resolve Target"):
                    try:
                        coord = SkyCoord.from_name(obj_name.strip())
                        st.session_state.ra = coord.ra.deg
                        st.session_state.dec = coord.dec.deg
                        st.success(f"Target Locked: {obj_name}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Simbad Error: Ensure your Docker container has internet access. (Details: {e})")
            
            c1, c2 = st.columns(2)
            ra = c1.number_input("Right Ascension", value=st.session_state.ra, format="%.4f")
            dec = c2.number_input("Declination", value=st.session_state.dec, format="%.4f")
            st.session_state.ra, st.session_state.dec = ra, dec
            
            if st.button("Fetch Sky Preview"):
                img_url = f"https://www.legacysurvey.org/viewer/cutout.jpg?ra={ra}&dec={dec}&layer=ls-dr10&pixscale=0.5&size=400"
                st.image(img_url, caption="Target Visual Acquisition")

    with col_photo:
        with st.container(border=True):
            st.subheader("2. Photometric Data")
            m1, m2, m3 = st.columns(3)
            u = m1.number_input("u-mag", value=19.43)
            g = m2.number_input("g-mag", value=19.03)
            r = m3.number_input("r-mag", value=18.87)
            
            m4, m5, m6, m7 = st.columns(4)
            i, z = m4.number_input("i-mag", value=18.61), m5.number_input("z-mag", value=18.58)
            w1, w2 = m6.number_input("W1 (IR)", value=14.80), m7.number_input("W2 (IR)", value=14.01)

            if st.button("Run Classification Analysis", type="primary"):
                try:
                    res = get_prediction({"u": u, "g": g, "r": r, "i": i, "z": z, "w1": w1, "w2": w2})
                    st.session_state['prediction_result'] = res
                except Exception as e:
                    st.error(f"Backend Offline: {e}")

        #--- RESULTS & ANOMALY DETECTION (FR11) ---
        if st.session_state['prediction_result']:
            res = st.session_state['prediction_result']
            st.divider()
            
            # 1. Calculation
            conf_val = res['confidence'] * 100 if res['confidence'] <= 1 else res['confidence']
            
            # 2. Display Metrics
            r1, r2 = st.columns(2)
            r1.metric("Predicted Class", res['prediction'])
            r2.metric("Confidence Score", f"{conf_val:.2f}%")

            # 3. ANOMALY DETECTION LOGIC (FR11)
            if conf_val < 50:
                st.warning("""
                    ⚠️ **ANOMALY DETECTED** The model's confidence is below the 50% threshold. This object may be:
                    * A rare transient (Supernova/Variable Star)
                    * An out-of-distribution data artifact
                    * An overlapping/blended source
                """)
            elif res['prediction'] == "QSO" and conf_val < 70:
                st.info("💡 **Note:** Quasars (QSO) often mimic Star-like profiles in optical data.")

            # 4. FIXED: Confidence Chart with proper length handling
            st.write("### 📊 Probability Distribution")
            
            # Get the actual class labels from the backend or define them based on your model
            # First, let's check what the backend is returning
            st.write("DEBUG - Raw Backend Response:", res)
            
            # Define the expected class order based on your model
            # Update these labels to match exactly what your model outputs
            expected_classes = ['GALAXY', 'QSO', 'STAR']
            probabilities = res.get('probabilities', [])
            
            # Debug: Show lengths
            st.write(f"DEBUG - Expected classes length: {len(expected_classes)}")
            st.write(f"DEBUG - Probabilities length: {len(probabilities)}")
            
            # Check if lengths match
            if len(probabilities) != len(expected_classes):
                st.warning(f"⚠️ Class count mismatch: Model returned {len(probabilities)} probabilities but expected {len(expected_classes)} classes.")
                st.info("Using available data for visualization...")
                
                # If the probabilities array has different length, we need to adapt
                # Option 1: If probabilities is shorter, pad with zeros
                # Option 2: If probabilities is longer, trim or use class labels from backend if available
                
                # Try to get class labels from the backend response
                if 'class_labels' in res:
                    # Use the labels from backend
                    class_labels = res['class_labels']
                    prob_values = probabilities
                else:
                    # Generate generic labels if we don't have proper ones
                    class_labels = [f"Class_{i}" for i in range(len(probabilities))]
                    prob_values = probabilities
            else:
                # All good, use the expected classes
                class_labels = expected_classes
                prob_values = probabilities
            
            # Convert probabilities to percentages for display
            prob_percentages = [p * 100 if p <= 1 else p for p in prob_values]
            
            # Create the DataFrame with matching lengths
            chart_data = pd.DataFrame({
                'Class': class_labels,
                'Probability': prob_percentages
            }).set_index('Class')
            
            # Display the bar chart
            st.bar_chart(chart_data)
            
            # Add explanation
            st.caption("The chart shows the raw probability distribution for each celestial class.")

with tab_map:
    components.iframe(f"https://www.legacysurvey.org/viewer/?ra={st.session_state.ra}&dec={st.session_state.dec}&layer=ls-dr10&zoom=13", height=700)