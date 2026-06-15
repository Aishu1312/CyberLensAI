import streamlit as st
from utils import inject_css, init_state, GLOBAL_CSS

st.set_page_config(
    page_title="CyberLens AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Hide ONLY Streamlit default multipage menu
st.markdown("""
<style>

/* Hide app/about/dashboard list */
[data-testid="stSidebarNav"]{
    visibility:hidden;
    height:0px;
}


/* Restore content */
[data-testid="stSidebarContent"]{
    display:block !important;
}

</style>
""", unsafe_allow_html=True)

inject_css()
init_state()

# ── Sidebar navigation ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="display:flex;align-items:center;gap:10px;margin-bottom:2rem;">'
        '<span style="font-size:1.6rem;">🎯</span>'
        '<span style="font-family:\'Space Grotesk\',sans-serif;font-weight:800;font-size:1.2rem;color:#F1F5F9;">CyberLens AI</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    pages = {
        "🏠  Home":                "Home",
        "📊  Command Center":      "Dashboard",
        "🔍  Investigations":      "Investigations",
        "📤  Ingest Evidence":     "Upload",
        "⚡  Quick Analyze":       "Analyze",
        "📄  Reports":             "Reports",
        "ℹ️  About":              "About",
    }

    if "page" not in st.session_state:
        st.session_state.page = "Home"

    for label, key in pages.items():
        active = st.session_state.page == key
        btn_style = (
            "background:#1E2D4A;color:#3B82F6;border-left:3px solid #3B82F6;"
            if active else
            "background:transparent;color:#94A3B8;border-left:3px solid transparent;"
        )
        if st.sidebar.button(
            label,
            key=f"nav_{key}",
            use_container_width=True,
        ):
            st.session_state.page = key
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        '<p style="color:#334155;font-size:0.7rem;text-align:center;">SDG 16 · SDG 9 · © 2025 CyberLens AI</p>',
        unsafe_allow_html=True,
    )

# ── Page router ─────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "Home":
    from pages import home; home.render()
elif page == "Dashboard":
    from pages import dashboard; dashboard.render()
elif page == "Investigations":
    from pages import investigations; investigations.render()
elif page == "Upload":
    from pages import upload; upload.render()
elif page == "Analyze":
    from pages import analyze; analyze.render()
elif page == "Reports":
    from pages import reports; reports.render()
elif page == "About":
    from pages import about; about.render()
