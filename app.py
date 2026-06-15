import streamlit as st
from views import home, dashboard, investigations, upload, analyze, reports, about
from utils import inject_css, init_state

# ─────────────────────────────────────────────────────────────
# 1. Page Config (Must be the first command)
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CyberLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# 2. Initialize App State & Global CSS
# ─────────────────────────────────────────────────────────────
inject_css()
init_state()

# ─────────────────────────────────────────────────────────────
# 3. Custom CSS to Match Your Screenshot
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* Force sidebar background color to match your dark theme */
    [data-testid="stSidebar"] {
        background-color: #0B1221 !important;
        border-right: 1px solid #1E293B !important;
        min-width: 280px !important;
    }

    /* HIDE THE REDUNDANT DEFAULT NAVIGATION AT THE TOP */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* Hide system header and footer */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    /* ---------------------------------------------------- */
    /* CUSTOM SIDEBAR BUTTON STYLING (Matches Screenshot)   */
    /* ---------------------------------------------------- */
    [data-testid="stSidebar"] div.stButton > button {
        background-color: #1E293B !important; /* Dark bluish-grey button */
        color: #F8FAFC !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
        height: auto !important;
        display: flex !important;
        justify-content: center !important; /* Centers the icon and text */
        transition: all 0.2s ease-in-out !important;
        margin-bottom: 5px !important;
    }

    /* Hover effect for buttons */
    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #334155 !important;
        color: white !important;
    }
    
    /* Active/Click effect for buttons */
    [data-testid="stSidebar"] div.stButton > button:active,
    [data-testid="stSidebar"] div.stButton > button:focus {
        background-color: #3B82F6 !important; /* Blue highlight */
        color: white !important;
        border-color: #3B82F6 !important;
    }

    /* Typography for buttons */
    [data-testid="stSidebar"] div.stButton > button p {
        font-size: 14px !important;
        font-weight: 500 !important;
        margin: 0 !important;
    }

    /* Title Styling */
    .sidebar-title-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 30px;
        margin-top: -10px;
    }
    .sidebar-icon { font-size: 32px; }
    .sidebar-title {
        font-size: 24px;
        font-weight: 700;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# 4. Session State for Routing
# ─────────────────────────────────────────────────────────────
# I set the default to "Dashboard" so it automatically loads 
# the Command Center screen shown in your screenshot.
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ─────────────────────────────────────────────────────────────
# 5. Sidebar UI
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    # App Title
    st.markdown(
        """
        <div class="sidebar-title-container">
            <span class="sidebar-icon">🎯</span>
            <span class="sidebar-title">CyberLens AI</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation Dictionary
    navigation_map = {
        "🏠 Home": "Home",
        "📊 Command Center": "Dashboard",
        "🔍 Investigations": "Investigations",
        "📤 Ingest Evidence": "Upload",
        "⚡ Quick Analyze": "Analyze",
        "📄 Reports": "Reports",
        "ℹ️ About": "About",
    }

    # Generate Buttons
    for label, page_key in navigation_map.items():
        if st.button(label, use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.page = page_key
            st.rerun()

# ─────────────────────────────────────────────────────────────
# 6. View Router
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
    # Render the selected page based on session state
    if st.session_state.page in page_renderers:
        page_renderers[st.session_state.page]()
    else:
        st.error("Page not found.")
except Exception as e:
    st.error(f"Error loading {st.session_state.page} page: {e}")
