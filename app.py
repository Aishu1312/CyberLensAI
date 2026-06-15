import streamlit as st
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
# Hide Streamlit Default UI
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>

    /* Hide default multipage navigation */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }

    [data-testid="stSidebarNavItems"] {
        display: none !important;
    }

    /* Hide Streamlit menu */
    #MainMenu {
        visibility: hidden;
    }

    /* Hide footer */
    footer {
        visibility: hidden;
    }

    /* Hide header */
    header {
        visibility: hidden;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #07132B;
        border-right: 1px solid #1E293B;
    }

    /* Reduce top padding */
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    /* Main content width */
    .block-container {
        padding-top: 2rem;
        max-width: 1400px;
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
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            margin-bottom:25px;
        ">
            <span style="font-size:34px;">🎯</span>
            <span style="
                font-size:28px;
                font-weight:700;
                color:white;
            ">
                CyberLens AI
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    pages = {
        "🏠 Home": "Home",
        "📊 Command Center": "Dashboard",
        "🔍 Investigations": "Investigations",
        "📤 Ingest Evidence": "Upload",
        "⚡ Quick Analyze": "Analyze",
        "📄 Reports": "Reports",
        "ℹ️ About": "About",
    }

    for label, page_key in pages.items():

        if st.button(
            label,
            use_container_width=True,
            key=f"nav_{page_key}",
        ):
            st.session_state.page = page_key
            st.rerun()

    st.markdown("---")

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#94A3B8;
            font-size:12px;
            margin-top:15px;
        ">
            SDG 16 • SDG 9<br>
            © 2025 CyberLens AI
        </div>
        """,
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────────────────────
page = st.session_state.page

try:

    if page == "Home":
        from views import home
        home.render()

    elif page == "Dashboard":
        from views import dashboard
        dashboard.render()

    elif page == "Investigations":
        from views import investigations
        investigations.render()

    elif page == "Upload":
        from views import upload
        upload.render()

    elif page == "Analyze":
        from views import analyze
        analyze.render()

    elif page == "Reports":
        from views import reports
        reports.render()

    elif page == "About":
        from views import about
        about.render()

except Exception as e:
    st.error(f"Error loading page: {e}")
