import streamlit as st

def set_professional_style():
    st.markdown("""
        <style>
        /* 1. GLOBAL APP & SIDEBAR DARKNESS */
        /* This targets the main app and the sidebar container directly */
        .stApp, [data-testid="stSidebar"], section[data-testid="stSidebar"] > div {
            background-color: #0b0e14 !important;
            color: #e0e6ed !important;
        }

        /* 2. SIDEBAR NAVIGATION TEXT (Fixes image 1) */
        /* Targets the page names in the sidebar */
        [data-testid="stSidebarNav"] span {
            color: #ffffff !important;
            font-size: 1rem !important;
        }
        
        /* Targets the 'Deep Sky Classification' caption in sidebar */
        [data-testid="stSidebar"] .stMarkdown p, 
        [data-testid="stSidebar"] .stCaption {
            color: #ffffff !important;
            opacity: 0.8;
        }

        /* 3. RADIO BUTTON LABELS (Fixes image 2) */
        /* This specifically targets the text 'Coordinates' and 'Object Name' */
        div[data-testid="stRadio"] label div p {
            color: #ffffff !important;
        }
        
        /* Targets the 'Search Method' title above radio buttons */
        div[data-testid="stRadio"] label p {
            color: #ffffff !important;
            font-weight: bold !important;
        }

        /* 4. TABS VISIBILITY */
        .stTabs [data-baseweb="tab"] p {
            color: rgba(255, 255, 255, 0.6) !important;
        }
        .stTabs [aria-selected="true"] p {
            color: #3b82f6 !important;
        }

        /* 5. METRICS & WIDGET TITLES */
        [data-testid="stMetricLabel"] p, 
        [data-testid="stWidgetLabel"] p {
            color: #ffffff !important;
        }

        /* 6. SIDEBAR DIVIDER LINE */
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.2) !important;
        }

        /* 7. INPUT BOXES TEXT COLOR */
        /* Ensures text typed into boxes is dark enough to read or light enough for dark boxes */
        input {
            color: #000000 !important; /* Keep text inside white boxes black for readability */
        }
        </style>
    """, unsafe_allow_html=True)

def sidebar_branding():
    """
    Standardizes the sidebar header across all pages.
    """
    with st.sidebar:
        st.markdown("# 🪐 GalaxEye")
        st.caption("Deep Sky Classification System v1.2")
        st.markdown("---")