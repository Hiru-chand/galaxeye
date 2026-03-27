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
# if 'debug_info' not in st.session_state: st.session_state['debug_info'] = None

# tab_input, tab_map, tab_debug = st.tabs(["📝 Classification & Target", "🗺️ Interactive Explorer", "🔧 Debug"])

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
#             i = m4.number_input("i-mag", value=18.61)
#             z = m5.number_input("z-mag", value=18.58)
#             w1 = m6.number_input("W1 (IR)", value=14.80)
#             w2 = m7.number_input("W2 (IR)", value=14.01)

#             if st.button("Run Classification Analysis", type="primary"):
#                 try:
#                     payload = {"u": u, "g": g, "r": r, "i": i, "z": z, "w1": w1, "w2": w2}
#                     res = get_prediction(payload)
#                     st.session_state['prediction_result'] = res
#                     st.session_state['debug_info'] = {
#                         'payload': payload,
#                         'response': res,
#                         'timestamp': pd.Timestamp.now()
#                     }
#                     st.rerun()
#                 except Exception as e:
#                     st.error(f"Backend Offline: {e}")
#                     st.session_state['debug_info'] = {'error': str(e)}

#         #--- RESULTS & ANOMALY DETECTION ---
#         if st.session_state['prediction_result']:
#             res = st.session_state['prediction_result']
#             st.divider()
            
#             # Debug: Show what we received
#             with st.expander("📡 Raw API Response"):
#                 st.json(res)
            
#             # Calculate confidence
#             if isinstance(res.get('confidence'), (int, float)):
#                 conf_val = res['confidence'] * 100 if res['confidence'] <= 1 else res['confidence']
#             else:
#                 conf_val = 0.0
            
#             # Display Metrics
#             r1, r2 = st.columns(2)
#             r1.metric("Predicted Class", res.get('prediction', 'Unknown'))
#             r2.metric("Confidence Score", f"{conf_val:.2f}%")

#             # Anomaly Detection
#             if conf_val < 50:
#                 st.warning("⚠️ **ANOMALY DETECTED:** Model uncertainty is high. This may be a rare transient or data artifact.")
#             elif res.get('prediction') == "QSO" and conf_val < 70:
#                 st.info("💡 **Note:** Quasars (QSO) often mimic Star-like profiles in optical data.")

#             # Handle the probabilities
#             st.write("### 📊 Probability Distribution")
            
#             probabilities = res.get('probabilities', [])
            
#             # Let's check if the probabilities array is actually 3 elements but got truncated in display
#             st.write(f"**Probabilities array length:** {len(probabilities)}")
#             st.write(f"**Probabilities values:** {probabilities}")
            
#             # Try to get class labels if available
#             class_labels = res.get('class_labels', ['GALAXY', 'QSO', 'STAR'])
            
#             # Check if we have a mapping in the response
#             if 'probabilities_dict' in res:
#                 # If the backend sends a dictionary with class names
#                 prob_dict = res['probabilities_dict']
#                 chart_data = pd.DataFrame({
#                     'Class': list(prob_dict.keys()),
#                     'Probability': [v * 100 if v <= 1 else v for v in prob_dict.values()]
#                 }).set_index('Class')
#                 st.bar_chart(chart_data)
#                 st.caption("Probability distribution for each celestial class.")
                
#             elif len(probabilities) == 3:
#                 # Perfect - 3 class classifier
#                 prob_percentages = [p * 100 if p <= 1 else p for p in probabilities]
#                 chart_data = pd.DataFrame({
#                     'Class': class_labels[:3],
#                     'Probability': prob_percentages
#                 }).set_index('Class')
#                 st.bar_chart(chart_data)
#                 st.caption("The chart shows the raw probability distribution for each celestial class.")
                
#             elif len(probabilities) == 2:
#                 # This suggests the model might be outputting logits or something else
#                 st.warning("⚠️ The model returned only 2 probabilities, but we expect 3 classes.")
#                 st.info("This might indicate that the model is outputting logits instead of softmax probabilities, or there's a mismatch in the model output layer.")
                
#                 # Try to interpret - maybe the first value is for the predicted class?
#                 # Let's create a synthetic 3-class distribution based on the prediction
#                 predicted_class = res.get('prediction', 'GALAXY')
#                 prob_map = {'GALAXY': 0, 'QSO': 1, 'STAR': 2}
                
#                 synthetic_probs = [0.0, 0.0, 0.0]
#                 if predicted_class in prob_map:
#                     idx = prob_map[predicted_class]
#                     if len(probabilities) >= 1:
#                         synthetic_probs[idx] = probabilities[0] if probabilities[0] <= 1 else probabilities[0] / 100
#                     if len(probabilities) >= 2:
#                         # Distribute remaining probability
#                         remaining = 1 - synthetic_probs[idx]
#                         for i in range(3):
#                             if i != idx:
#                                 synthetic_probs[i] = remaining / 2
                
#                 prob_percentages = [p * 100 for p in synthetic_probs]
#                 chart_data = pd.DataFrame({
#                     'Class': class_labels[:3],
#                     'Probability': prob_percentages
#                 }).set_index('Class')
#                 st.bar_chart(chart_data)
#                 st.caption("⚠️ **Note:** Synthetic probabilities created from binary output. Check your model configuration.")
                
#             else:
#                 st.error(f"Unexpected probability format. Expected 3 probabilities, got {len(probabilities)}")
#                 st.write("Raw response for debugging:")
#                 st.json(res)
                
#                 # Create dummy data to avoid breaking the UI
#                 chart_data = pd.DataFrame({
#                     'Class': ['GALAXY', 'QSO', 'STAR'],
#                     'Probability': [33.33, 33.33, 33.33]
#                 }).set_index('Class')
#                 st.bar_chart(chart_data)

# with tab_map:
#     components.iframe(f"https://www.legacysurvey.org/viewer/?ra={st.session_state.ra}&dec={st.session_state.dec}&layer=ls-dr10&zoom=13", height=700)

# with tab_debug:
#     st.subheader("🔧 Debug Information")
    
#     if st.session_state.get('debug_info'):
#         debug_info = st.session_state['debug_info']
        
#         if 'error' in debug_info:
#             st.error(f"Error: {debug_info['error']}")
#         else:
#             st.write("**Last Request:**")
#             st.json(debug_info.get('payload', {}))
            
#             st.write("**Last Response:**")
#             st.json(debug_info.get('response', {}))
            
#             st.write("**Timestamp:**", debug_info.get('timestamp', 'N/A'))
            
#             # Check the API endpoint
#             st.write("**API Configuration Check:**")
#             try:
#                 from utils.api_client import API_URL
#                 st.write(f"API_URL: {API_URL}")
#             except:
#                 st.write("Could not import API_URL")
#     else:
#         st.info("Run a classification to see debug information.")
    
#     # Add a section to test API connectivity
#     st.subheader("API Connection Test")
#     if st.button("Test API Connection"):
#         try:
#             from utils.api_client import API_URL, get_prediction
#             test_payload = {"u": 19.43, "g": 19.03, "r": 18.87, "i": 18.61, "z": 18.58, "w1": 14.80, "w2": 14.01}
#             result = get_prediction(test_payload)
#             st.success("✅ API is reachable!")
#             st.write("Response structure:")
#             st.json(result)
#         except Exception as e:
#             st.error(f"❌ API connection failed: {e}")


#=============================5th========================================

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
if 'ra' not in st.session_state: 
    st.session_state['ra'] = 10.6847
if 'dec' not in st.session_state: 
    st.session_state['dec'] = 41.2687
if 'prediction_result' not in st.session_state: 
    st.session_state['prediction_result'] = None

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
                        st.error(f"Could not resolve name via Simbad. Details: {e}")
            
            c1, c2 = st.columns(2)
            ra = c1.number_input("Right Ascension", value=st.session_state.ra, format="%.4f")
            dec = c2.number_input("Declination", value=st.session_state.dec, format="%.4f")
            st.session_state.ra, st.session_state.dec = ra, dec
            
            if st.button("Fetch Sky Preview"):
                img_url = f"https://www.legacysurvey.org/viewer/cutout.jpg?ra={ra}&dec={dec}&layer=ls-dr10&pixscale=0.5&size=400"
                st.image(img_url, caption="Target Visual Acquisition", use_container_width=True)

    with col_photo:
        with st.container(border=True):
            st.subheader("2. Photometric Data")
            st.info("Input SDSS (Optical) & WISE (Infrared) Magnitudes")
            
            m1, m2, m3 = st.columns(3)
            u = m1.number_input("u-mag", value=19.43)
            g = m2.number_input("g-mag", value=19.03)
            r = m3.number_input("r-mag", value=18.87)
            
            m4, m5, m6, m7 = st.columns(4)
            i = m4.number_input("i-mag", value=18.61)
            z = m5.number_input("z-mag", value=18.58)
            w1 = m6.number_input("W1 (IR)", value=14.80)
            w2 = m7.number_input("W2 (IR)", value=14.01)

            if st.button("Run Classification Analysis", type="primary", use_container_width=True):
                try:
                    payload = {"u": u, "g": g, "r": r, "i": i, "z": z, "w1": w1, "w2": w2}
                    res = get_prediction(payload)
                    st.session_state['prediction_result'] = res
                    st.rerun()
                except Exception as e:
                    st.error(f"Backend Connection Error. Ensure the FastAPI service is running. Details: {e}")

        # --- RESULTS & ANOMALY DETECTION ---
        if st.session_state['prediction_result']:
            res = st.session_state['prediction_result']
            st.divider()
            
            # Calculate confidence
            conf_val = res['confidence'] * 100 if res['confidence'] <= 1 else res['confidence']
            
            # Display Metrics
            r1, r2 = st.columns(2)
            r1.metric("Predicted Class", res['prediction'])
            r2.metric("Confidence Score", f"{conf_val:.2f}%")

            # Anomaly Detection Logic
            if conf_val < 50:
                st.warning("""
                    ⚠️ **ANOMALY DETECTED** The model's confidence is below the 50% threshold. This object may be:
                    * A rare transient (Supernova/Variable Star)
                    * An out-of-distribution data artifact
                    * An overlapping/blended source
                """)
            elif res['prediction'] == "QSO" and conf_val < 70:
                st.info("💡 **Note:** Quasars (QSO) often mimic Star-like profiles in optical data.")

            # Confidence Chart
            st.write("### 📊 Probability Distribution")
            
            probabilities = res.get('probabilities', [])
            prob_percentages = [p * 100 if p <= 1 else p for p in probabilities]
            
            chart_data = pd.DataFrame({
                'Class': ['GALAXY', 'QSO', 'STAR'],
                'Probability': prob_percentages
            }).set_index('Class')
            
            st.bar_chart(chart_data)
            st.caption("The chart shows the raw probability distribution for each celestial class.")

with tab_map:
    st.subheader("Interactive Sky Map")
    map_url = f"https://www.legacysurvey.org/viewer/?ra={st.session_state.ra}&dec={st.session_state.dec}&layer=ls-dr10&zoom=13"
    components.iframe(map_url, height=700, scrolling=True)
    st.caption(f"Map centered on RA: {st.session_state.ra:.4f}, DEC: {st.session_state.dec:.4f}")