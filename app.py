import streamlit as st
from views import home, dashboard, investigations, upload, analyze, reports, about
from utils import inject_css, init_state

# ─────────────────────────────────────────────────────────────
# 1. Page Config
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CyberLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",  # Forces sidebar to start expanded
)

# ─────────────────────────────────────────────────────────────
# 2. Initialize App
# ─────────────────────────────────────────────────────────────
inject_css()
init_state()

# ─────────────────────────────────────────────────────────────
# 3. Enhanced CSS for Sidebar Persistence
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Hide default Streamlit multi-page nav */
    [data-testid="stSidebarNav"] { display: none !important; }
    
    /* Hide the collapse/expand button so it cannot be closed */
    [data-testid="stSidebarCollapseButton"] { display: none !important; }
    
    /* Hide other UI elements */
    #MainMenu, footer, header { visibility: hidden; }
    
    /* Sidebar container styling */
    section[data-testid="stSidebar"] {
        background-color: #07132B !important;
        border-right: 1px solid #1E293B !important;
        width: 300px !important; /* Fixed width for stability */
    }
    
    /* Ensure sidebar content padding */
    section[data-testid="stSidebar"] > div { padding-top: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# 4. Session State
# ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ─────────────────────────────────────────────────────────────
# 5. Sidebar Navigation
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
        if st.button(label, use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.rerun()

    st.markdown("---")
    st.markdown(
        """<div style="text-align:center; color:#94A3B8; font-size:12px;">
            SDG 16 • SDG 9<br>© 2025 CyberLens AI</div>""",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# 6. Router
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
except Exception as e:
    st.error(f"Error loading page: {e}")
