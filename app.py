import streamlit as st
from views import home, dashboard, investigations, upload, analyze, reports, about
from utils import inject_css, init_state

# ─────────────────────────────────────────────────────────────
# 1. Page Config (Must be the very first Streamlit command)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CyberLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded", 
)

# ─────────────────────────────────────────────────────────────
# 2. Initialize App State
# ─────────────────────────────────────────────────────────────
inject_css()
init_state()

# ─────────────────────────────────────────────────────────────
# 3. CSS for Sidebar Styling & Locking
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* 1. HIDE THE DEFAULT STREAMLIT MULTI-PAGE NAVIGATION LIST */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* 2. PREVENT ACCIDENTAL CLOSING: Hide the "<<" collapse button */
    [data-testid="stSidebarCollapseButton"] {
        display: none !important;
    }
    
    /* 3. SAFETY NET: If somehow closed, ensure the ">" expand button is visible */
    [data-testid="collapsedControl"] {
        display: flex !important;
    }

    /* Hide the bottom footer */
    footer { visibility: hidden !important; }

    /* CUSTOM STYLING FOR YOUR NAVIGATION BUTTONS */
    [data-testid="stSidebar"] div.stButton > button {
        background-color: #1E293B !important;
        color: #F8FAFC !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 1rem !important;
        display: flex !important;
        justify-content: flex-start !important; 
        width: 100% !important;
        margin-bottom: 8px !important;
        transition: all 0.2s ease-in-out !important;
        font-weight: 500 !important;
    }

    /* Hover effect */
    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #334155 !important;
        color: white !important;
    }
    
    /* Active/Clicked effect */
    [data-testid="stSidebar"] div.stButton > button:active,
    [data-testid="stSidebar"] div.stButton > button:focus {
        background-color: #3B82F6 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# 4. Session State for Routing
# ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ─────────────────────────────────────────────────────────────
# 5. Build the Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    
    # Custom Title
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:30px; margin-top:10px;">
            <span style="font-size:32px;">🎯</span>
            <span style="font-size:24px; font-weight:700; color:white;">CyberLens AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation Menu
    navigation_map = {
        "🏠  Home": "Home",
        "📊  Command Center": "Dashboard",
        "🔍  Investigations": "Investigations",
        "📤  Ingest Evidence": "Upload",
        "⚡  Quick Analyze": "Analyze",
        "📄  Reports": "Reports",
        "ℹ️  About": "About",
    }

    # Generate the custom buttons
    for label, page_key in navigation_map.items():
        if st.button(label, use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.rerun()

# ─────────────────────────────────────────────────────────────
# 6. View Router Logic
# ─────────────────────────────────────────────────────────────
page_renderers = {
    "Home": home.render,
    "Dashboard": dashboard.render,
    "Investigations": investigations.render,
    "Upload": upload.render,
    "Analyze": analyze.render,
    "Reports": reports.render,
    "About": about.render,
}

try:
    if st.session_state.page in page_renderers:
        page_renderers[st.session_state.page]()
    else:
        st.error("Page not found.")
except Exception as e:
    st.error(f"Error loading the {st.session_state.page} page: {e}")
