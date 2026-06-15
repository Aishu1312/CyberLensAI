import streamlit as st
from views import home, dashboard, investigations, upload, analyze, reports, about
from utils import inject_css, init_state

# ─────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CyberLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# Initialize App
# ─────────────────────────────────────────────────────────────
inject_css()
init_state()

# ─────────────────────────────────────────────────────────────
# Custom CSS for Navigation & UI
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] { display: none !important; }
    #MainMenu, footer, header { visibility: hidden; }
    
    section[data-testid="stSidebar"] {
        background-color: #07132B;
        border-right: 1px solid #1E293B;
    }
    
    /* Active button styling */
    div.stButton > button:active {
        border: 1px solid #3B82F6;
        background-color: #1E293B;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:25px;">
            <span style="font-size:34px;">🎯</span>
            <span style="font-size:24px; font-weight:700; color:white;">CyberLens AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    navigation_map = {
        "🏠 Home": "Home",
        "📊 Command Center": "Dashboard",
        "🔍 Investigations": "Investigations",
        "📤 Ingest Evidence": "Upload",
        "⚡ Quick Analyze": "Analyze",
        "📄 Reports": "Reports",
        "ℹ️ About": "About",
    }

    for label, page_key in navigation_map.items():
        if st.sidebar.button(label, use_container_width=True, key=f"btn_{page_key}"):
            st.session_state.page = page_key
            st.rerun()

    st.markdown("---")
    st.markdown(
        """<div style="text-align:center; color:#94A3B8; font-size:12px;">
            SDG 16 • SDG 9<br>© 2025 CyberLens AI</div>""",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# Router
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
    # Execute the render function based on session state
    if st.session_state.page in page_renderers:
        page_renderers[st.session_state.page]()
except Exception as e:
    st.error(f"Error loading page: {e}")
