import streamlit as st
from utils import inject_css

def render():
    inject_css()

    # Hero banner
    st.markdown(
        '<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:16px;'
        'padding:3rem 2.5rem;margin-bottom:2.5rem;position:relative;overflow:hidden;">'
        '<div style="position:absolute;inset:0;background:radial-gradient(ellipse at top right,'
        'rgba(59,130,246,0.08),transparent);pointer-events:none;"></div>'
        '<div style="display:inline-flex;align-items:center;gap:8px;'
        'background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.25);'
        'border-radius:999px;padding:4px 14px;margin-bottom:1.2rem;'
        'color:#3B82F6;font-size:0.78rem;font-weight:700;position:relative;z-index:1;">🎯 Mission Brief</div>'
        '<h1 style="font-family:\'Space Grotesk\',sans-serif;font-weight:800;font-size:2.2rem;'
        'margin-bottom:1rem;position:relative;z-index:1;">Democratising Digital Forensics</h1>'
        '<p style="color:#64748B;font-size:1.05rem;line-height:1.7;max-width:680px;'
        'position:relative;z-index:1;">'
        'CyberLens AI was built to equip students, non-profits, and investigators with '
        'enterprise-grade threat detection capabilities. We believe access to digital security '
        'tools is a fundamental requirement in the modern era.'
        '</p></div>',
        unsafe_allow_html=True,
    )

    # Core objectives
    st.markdown(
        '<h2 style="font-weight:700;font-size:1.3rem;border-bottom:1px solid #1E2D4A;'
        'padding-bottom:0.6rem;margin-bottom:1.2rem;">🎯 Core Objectives</h2>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    for col, icon, title, desc in [
        (c1, "🛡️", "Automate Threat Intelligence",
         "Reduce the manual overhead of analysing raw logs, emails, and CSVs. "
         "CyberLens AI automatically extracts entities, scores risk, and classifies threats."),
        (c2, "🔗", "Synthesise Complex Data",
         "Transform disjointed evidence into cohesive narratives. We generate visual timelines, "
         "network graphs, and boardroom-ready reports."),
    ]:
        with col:
            st.markdown(
                f'<div style="background:#060B18;border:1px solid #1E2D4A;border-radius:12px;padding:1.5rem;">'
                f'<div style="font-size:1.8rem;margin-bottom:0.6rem;">{icon}</div>'
                f'<h4 style="font-weight:700;margin-bottom:0.5rem;">{title}</h4>'
                f'<p style="color:#64748B;font-size:0.87rem;line-height:1.6;">{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # SDG alignment
    st.markdown(
        '<h2 style="font-weight:700;font-size:1.3rem;margin-bottom:1.2rem;">🌍 Global Impact Alignment</h2>',
        unsafe_allow_html=True,
    )

    for sdg_num, color, subtitle, title, body in [
        ("16", "#00689D", "Peace, Justice & Strong Institutions",
         "Combating Cybercrime",
         "By providing accessible tools for digital evidence analysis, CyberLens supports the reduction "
         "of illicit financial flows, strengthens recovery of stolen assets, and combats all forms of organised "
         "cybercrime in alignment with UN SDG Target 16.4."),
        ("9", "#FD6925", "Industry, Innovation & Infrastructure",
         "Resilient Security Infrastructure",
         "CyberLens contributes to building resilient infrastructure by deploying advanced AI technologies "
         "to organisations that traditionally lack access to enterprise security operations centres, "
         "supporting SDG Target 9.c."),
    ]:
        col_badge, col_body = st.columns([1, 3])
        with col_badge:
            st.markdown(
                f'<div style="background:{color};color:white;border-radius:12px;padding:1.5rem;'
                f'text-align:center;font-weight:800;">'
                f'<div style="font-size:3rem;line-height:1;">{sdg_num}</div>'
                f'<div style="font-size:0.7rem;text-transform:uppercase;margin-top:0.4rem;'
                f'opacity:0.9;line-height:1.3;">{subtitle}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
        with col_body:
            st.markdown(
                f'<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:12px;'
                f'padding:1.5rem;height:100%;">'
                f'<h4 style="font-weight:700;margin-bottom:0.6rem;">{title}</h4>'
                f'<p style="color:#64748B;font-size:0.9rem;line-height:1.7;">{body}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown("<br>", unsafe_allow_html=True)

    # Tech stack
    st.markdown(
        '<h2 style="font-weight:700;font-size:1.3rem;border-top:1px solid #1E2D4A;'
        'padding-top:1.5rem;margin-top:0.5rem;margin-bottom:1.2rem;">🛠 Technology Stack</h2>',
        unsafe_allow_html=True,
    )
    stack_cols = st.columns(4)
    for col, emoji, name, desc in [
        (stack_cols[0], "🐍", "Python + Streamlit", "Rapid full-stack web UI"),
        (stack_cols[1], "🤖", "OpenAI GPT-4o-mini", "Threat intelligence engine"),
        (stack_cols[2], "📊", "Plotly", "Interactive data visualisations"),
        (stack_cols[3], "🔐", "Zod-style validation", "Input validation & safety"),
    ]:
        with col:
            st.markdown(
                f'<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:10px;'
                f'padding:1.2rem;text-align:center;">'
                f'<div style="font-size:1.6rem;margin-bottom:0.4rem;">{emoji}</div>'
                f'<div style="font-weight:700;font-size:0.88rem;">{name}</div>'
                f'<div style="color:#64748B;font-size:0.78rem;margin-top:0.2rem;">{desc}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # CTA
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;border-top:1px solid #1E2D4A;padding-top:2.5rem;">'
        '<h2 style="font-weight:800;font-size:1.5rem;margin-bottom:0.6rem;">Ready to start?</h2>'
        '<p style="color:#64748B;max-width:480px;margin:0 auto 2rem;">'
        'Start analysing digital evidence with advanced threat detection models today.</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    cc1, cc2, cc3 = st.columns([1, 1, 1])
    with cc2:
        if st.button("🚀 Enter Command Center", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()
