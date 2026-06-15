import streamlit as st
from utils import inject_css, card

def render():
    inject_css()

    # Hero
    st.markdown(
        """
        <div style="text-align:center;padding:3rem 1rem 2rem;
             background:radial-gradient(ellipse at top,rgba(59,130,246,0.12) 0%,transparent 70%);">
          <div style="display:inline-flex;align-items:center;gap:8px;
               background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.25);
               border-radius:999px;padding:5px 16px;margin-bottom:1.5rem;
               color:#3B82F6;font-size:0.8rem;font-weight:600;">
            🛡️ &nbsp; SDG 16: Peace, Justice and Strong Institutions
          </div>
          <h1 style="font-family:'Space Grotesk',sans-serif;font-weight:800;
               font-size:clamp(2.5rem,5vw,4rem);letter-spacing:-0.03em;
               line-height:1.1;margin-bottom:1.2rem;">
            Illuminate digital threats<br>with
            <span style="background:linear-gradient(135deg,#3B82F6,#60A5FA);
                         -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
              precision AI</span>.
          </h1>
          <p style="color:#64748B;font-size:1.1rem;max-width:640px;
               margin:0 auto 2.5rem;line-height:1.7;">
            The command center for digital evidence analysis. Detect phishing, scams, and
            cyber threats instantly to empower investigations and build cybercrime awareness.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀  Start Investigating", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()
    with col3:
        if st.button("ℹ️  Learn More", use_container_width=True):
            st.session_state.page = "About"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature grid
    st.markdown(
        """
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-top:2rem;">
          <div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:16px;padding:2rem;">
            <div style="font-size:2rem;margin-bottom:1rem;">🔍</div>
            <h3 style="font-weight:700;margin-bottom:0.6rem;">Deep Analysis</h3>
            <p style="color:#64748B;font-size:0.9rem;line-height:1.6;">
              Process CSVs, logs, and raw text. Our models identify threat signatures,
              malicious entities, and risk patterns instantly.
            </p>
          </div>
          <div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:16px;padding:2rem;">
            <div style="font-size:2rem;margin-bottom:1rem;">📈</div>
            <h3 style="font-weight:700;margin-bottom:0.6rem;">Visual Timelines</h3>
            <p style="color:#64748B;font-size:0.9rem;line-height:1.6;">
              Map the chronology of an attack. Generate visual timelines and network graphs
              to understand threat propagation.
            </p>
          </div>
          <div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:16px;padding:2rem;">
            <div style="font-size:2rem;margin-bottom:1rem;">🔐</div>
            <h3 style="font-weight:700;margin-bottom:0.6rem;">Threat Reports</h3>
            <p style="color:#64748B;font-size:0.9rem;line-height:1.6;">
              Generate comprehensive, boardroom-ready reports summarising findings,
              risk scores, and actionable recommendations.
            </p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Quick-start steps
    st.markdown(
        '<h2 style="font-weight:700;font-size:1.4rem;margin-bottom:1.2rem;">Get started in 3 steps</h2>',
        unsafe_allow_html=True,
    )
    s1, s2, s3 = st.columns(3)
    for col, num, title, desc in [
        (s1, "01", "Create an Investigation", "Open a new case to group related evidence under one investigation."),
        (s2, "02", "Upload Evidence",          "Paste or upload suspicious emails, logs, or CSV files."),
        (s3, "03", "Get AI Analysis",          "CyberLens scores risk, identifies threats, and generates reports."),
    ]:
        with col:
            st.markdown(
                f'<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:12px;padding:1.4rem;">'
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:2rem;font-weight:800;color:#1E3A5F;">{num}</div>'
                f'<h4 style="font-weight:700;margin:0.4rem 0 0.4rem;">{title}</h4>'
                f'<p style="color:#64748B;font-size:0.85rem;margin:0;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
