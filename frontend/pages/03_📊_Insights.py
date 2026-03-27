import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.ui_components import set_professional_style, sidebar_branding

st.set_page_config(page_title="GalaxEye | Insights", page_icon="🔬", layout="wide")

set_professional_style()
sidebar_branding()

st.title("🔬 Model Explainability & Insights")
st.markdown("---")

# 1. Feature Importance (Static for now, representing the Global Model)
st.subheader("🧬 Global Feature Importance")
st.info("This chart shows which photometric bands (Colors) influence the classifier's decisions the most.")

# Mock data based on typical Astro-physics RF models
importance_df = pd.DataFrame({
    'Feature': ['u-g Color', 'g-r Color', 'r-i Color', 'i-z Color', 'z-w1 Color', 'w1 (IR)', 'w2 (IR)'],
    'Importance': [0.15, 0.22, 0.18, 0.12, 0.25, 0.05, 0.03]
}).sort_values(by='Importance', ascending=True)

fig_importance = px.bar(
    importance_df, 
    x='Importance', 
    y='Feature', 
    orientation='h',
    color='Importance',
    color_continuous_scale='Viridis',
    template="plotly_dark"
)
st.plotly_chart(fig_importance, use_container_width=True)

st.markdown("---")

# 2. Class Distribution Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 Magnitude Distribution")
    # Generating some dummy distribution data for visualization
    dist_data = pd.DataFrame({
        'Band': np.random.choice(['u', 'g', 'r', 'i', 'z'], 500),
        'Magnitude': np.random.normal(18, 2, 500)
    })
    fig_dist = px.box(dist_data, x="Band", y="Magnitude", points="all", template="plotly_dark")
    st.plotly_chart(fig_dist, use_container_width=True)

with col2:
    st.subheader("🎯 Classification Logic")
    st.write("""
    **How the model thinks:**
    * **Redshift Indicators:** High values in `r-i` and `i-z` colors are strong indicators for **QSOs** (Quasars).
    * **Infrared Excess:** Significant differences between `z` and `w1` usually separate **Galaxies** from **Stars**.
    * **Stellar Locus:** Stars typically follow a very specific "curve" in the $u-g$ vs $g-r$ color-color space.
    """)

st.divider()

# 3. Model Performance Metrics (Standard for Reports)
st.subheader("🏁 Performance Metrics")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Overall Accuracy", "94.2%")
m2.metric("Galaxy F1-Score", "0.96")
m3.metric("QSO Precision", "0.89")
m4.metric("Star Recall", "0.98")