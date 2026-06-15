import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils import inject_css, section_header, card, risk_badge, RISK_COLORS

def render():
    inject_css()
    section_header(
        "Command Center",
        "Real-time overview of digital investigations and threat intelligence.",
        "📊",
    )

    invs = st.session_state.get("investigations", [])
    evs  = st.session_state.get("evidence_items", [])
    ars  = st.session_state.get("analysis_results", [])

    active_inv     = sum(1 for i in invs if i["status"] in ("open", "in_progress"))
    total_inv      = len(invs)
    analyzed_ev    = sum(1 for e in evs if e["analysisStatus"] == "analyzed")
    total_ev       = len(evs)
    high_risk      = sum(1 for a in ars if a["riskLevel"] in ("high", "critical"))
    phishing_scam  = sum(
        1 for a in ars
        if any(t in a.get("threatTypes", []) for t in ("phishing", "Phishing Attempt", "scam", "Scam / Fraud"))
    )

    # ── Stat cards ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Active Investigations", f"{active_inv}", f"/ {total_inv} total")
    with c2:
        st.metric("Analysed Evidence", f"{analyzed_ev}", f"/ {total_ev} total")
    with c3:
        st.metric("High-Risk Detections", high_risk)
    with c4:
        st.metric("Phishing & Scams", phishing_scam)

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart, col_feed = st.columns([2, 1])

    with col_chart:
        st.markdown(
            '<h3 style="font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;">'
            '📈 Threat Detections Over Time</h3>',
            unsafe_allow_html=True,
        )

        # Build daily buckets from real data
        today = datetime.utcnow().date()
        days = [(today - timedelta(days=i)) for i in range(13, -1, -1)]
        labels = [d.strftime("%b %d") for d in days]
        buckets = {d: {"phishing": 0, "scam": 0, "malware": 0, "fraud": 0} for d in days}

        for a in ars:
            try:
                d = datetime.fromisoformat(a["createdAt"]).date()
                if d in buckets:
                    for t in a.get("threatTypes", []):
                        tl = t.lower()
                        if "phishing" in tl: buckets[d]["phishing"] += 1
                        elif "scam" in tl:   buckets[d]["scam"]     += 1
                        elif "malware" in tl: buckets[d]["malware"] += 1
                        elif "fraud" in tl:  buckets[d]["fraud"]    += 1
            except Exception:
                pass

        fig = go.Figure()
        colours = {"phishing": "#3B82F6", "scam": "#F59E0B", "malware": "#EF4444", "fraud": "#A78BFA"}
        for key, colour in colours.items():
            fig.add_trace(go.Scatter(
                x=labels, y=[buckets[d][key] for d in days],
                name=key.capitalize(), mode="lines+markers",
                line=dict(color=colour, width=2),
                marker=dict(size=4),
            ))

        fig.update_layout(
            paper_bgcolor="#0D1526", plot_bgcolor="#0D1526",
            font=dict(color="#94A3B8", family="Space Grotesk"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(gridcolor="#1E2D4A", showline=False, tickfont=dict(size=11)),
            yaxis=dict(gridcolor="#1E2D4A", showline=False, tickfont=dict(size=11), zeroline=False),
            height=300,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_feed:
        st.markdown(
            '<h3 style="font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;">'
            '⚡ System Activity</h3>',
            unsafe_allow_html=True,
        )
        recent = sorted(ars, key=lambda a: a["createdAt"], reverse=True)[:8]
        if not recent:
            st.markdown(
                card('<p style="color:#334155;text-align:center;padding:1rem;">No activity yet.</p>'),
                unsafe_allow_html=True,
            )
        else:
            for a in recent:
                color = RISK_COLORS.get(a["riskLevel"], ("#64748B", "#1E2D4A"))[0]
                ts = datetime.fromisoformat(a["createdAt"]).strftime("%b %d %H:%M")
                st.markdown(
                    f'<div style="border-left:3px solid {color};padding:0.5rem 0.8rem;'
                    f'margin-bottom:0.6rem;background:#060F20;border-radius:0 8px 8px 0;">'
                    f'<div style="font-size:0.78rem;color:#F1F5F9;">Evidence analysed — '
                    f'risk: <b>{a["riskLevel"]}</b> ({int(a.get("riskScore",0))}/100)</div>'
                    f'<div style="font-size:0.68rem;color:#475569;margin-top:2px;">{ts}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # ── Risk distribution pie ────────────────────────────────────────────────
    if ars:
        st.markdown("<br>", unsafe_allow_html=True)
        pie_col, bar_col = st.columns(2)

        level_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for a in ars:
            lvl = a.get("riskLevel", "low")
            if lvl in level_counts: level_counts[lvl] += 1

        with pie_col:
            st.markdown(
                '<h3 style="font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;">Risk Distribution</h3>',
                unsafe_allow_html=True,
            )
            fig2 = go.Figure(go.Pie(
                labels=[k.capitalize() for k in level_counts],
                values=list(level_counts.values()),
                marker_colors=["#22C55E", "#EAB308", "#F97316", "#EF4444"],
                hole=0.55,
            ))
            fig2.update_layout(
                paper_bgcolor="#0D1526", font=dict(color="#94A3B8"),
                margin=dict(l=0, r=0, t=10, b=0), height=240,
                showlegend=True,
                legend=dict(font=dict(color="#94A3B8")),
            )
            st.plotly_chart(fig2, use_container_width=True)

        with bar_col:
            threat_counts: dict = {}
            for a in ars:
                for t in a.get("threatTypes", []):
                    tl = t.strip()
                    if tl and tl != "None Detected":
                        threat_counts[tl] = threat_counts.get(tl, 0) + 1

            if threat_counts:
                st.markdown(
                    '<h3 style="font-weight:700;font-size:1.1rem;margin-bottom:0.8rem;">Top Threat Types</h3>',
                    unsafe_allow_html=True,
                )
                sorted_threats = sorted(threat_counts.items(), key=lambda x: x[1], reverse=True)[:6]
                labels_t, vals_t = zip(*sorted_threats)
                fig3 = go.Figure(go.Bar(
                    x=list(vals_t), y=list(labels_t),
                    orientation="h",
                    marker_color="#3B82F6",
                ))
                fig3.update_layout(
                    paper_bgcolor="#0D1526", plot_bgcolor="#0D1526",
                    font=dict(color="#94A3B8"),
                    margin=dict(l=0, r=0, t=10, b=0), height=240,
                    xaxis=dict(gridcolor="#1E2D4A"),
                    yaxis=dict(gridcolor="rgba(0,0,0,0)"),
                )
                st.plotly_chart(fig3, use_container_width=True)
