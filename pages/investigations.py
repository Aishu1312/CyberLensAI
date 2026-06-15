import streamlit as st
from datetime import datetime
from utils import inject_css, section_header, card, risk_badge, status_badge

def render():
    inject_css()

    # ── Detail view ──────────────────────────────────────────────────────────
    if st.session_state.get("viewing_inv_id"):
        _render_detail(st.session_state.viewing_inv_id)
        return

    # ── List view ────────────────────────────────────────────────────────────
    section_header("Investigations", "Manage and track digital forensic cases.", "🔍")

    col_title, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("＋  New Case", use_container_width=True):
            st.session_state.show_new_inv_form = True

    if st.session_state.get("show_new_inv_form"):
        with st.expander("➕ Create New Investigation", expanded=True):
            with st.form("new_inv_form"):
                title = st.text_input("Case Title *", placeholder="e.g. Phishing Campaign Q2 2025")
                desc  = st.text_area("Description", placeholder="Brief summary of the case…", height=80)
                submitted = st.form_submit_button("Create Investigation")
                if submitted:
                    if not title.strip():
                        st.error("Title is required.")
                    else:
                        from utils import add_investigation
                        add_investigation(title.strip(), desc.strip())
                        st.session_state.show_new_inv_form = False
                        st.success("✅ Investigation created!")
                        st.rerun()

    invs = st.session_state.get("investigations", [])

    if not invs:
        st.markdown(
            '<div style="border:2px dashed #1E2D4A;border-radius:16px;padding:4rem;'
            'text-align:center;margin-top:2rem;">'
            '<div style="font-size:3rem;margin-bottom:1rem;">🔍</div>'
            '<h3 style="color:#94A3B8;">No investigations yet</h3>'
            '<p style="color:#475569;">Create your first case to start analysing digital evidence.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(3)
    for i, inv in enumerate(sorted(invs, key=lambda x: x["createdAt"], reverse=True)):
        ars  = [a for a in st.session_state.analysis_results if a["investigationId"] == inv["id"]]
        max_risk = "low"
        if ars:
            order = {"critical":3,"high":2,"medium":1,"low":0}
            max_risk = max(ars, key=lambda a: order.get(a.get("riskLevel","low"),0)).get("riskLevel","low")
        border_color = {"low":"#22C55E","medium":"#EAB308","high":"#F97316","critical":"#EF4444"}.get(max_risk,"#1E2D4A")
        ts = datetime.fromisoformat(inv["createdAt"]).strftime("%b %d, %Y")

        with cols[i % 3]:
            st.markdown(
                f'<div style="background:#0D1526;border:1px solid {border_color}40;'
                f'border-top:3px solid {border_color};border-radius:12px;padding:1.4rem;'
                f'margin-bottom:1rem;">'
                f'<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.8rem;">'
                f'{status_badge(inv["status"])}'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:0.7rem;color:#475569;">#{inv["id"]}</span>'
                f'</div>'
                f'<h4 style="font-weight:700;margin:0.4rem 0 0.3rem;font-size:1rem;">{inv["title"]}</h4>'
                f'<p style="color:#64748B;font-size:0.82rem;margin:0 0 1rem;">{inv.get("description","") or "No description."}</p>'
                f'<div style="display:flex;gap:1.2rem;font-size:0.78rem;color:#94A3B8;margin-bottom:1rem;">'
                f'<span>📂 {inv.get("evidenceCount",0)} evidence</span>'
                f'<span>⚠️ {inv.get("highRiskCount",0)} alerts</span>'
                f'<span>📅 {ts}</span>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            c1, c2 = st.columns(2)
            with c1:
                if st.button("View Details", key=f"view_{inv['id']}", use_container_width=True):
                    st.session_state.viewing_inv_id = inv["id"]
                    st.rerun()
            with c2:
                if st.button("Upload Evidence", key=f"upload_{inv['id']}", use_container_width=True):
                    st.session_state.prefill_inv_id = inv["id"]
                    st.session_state.page = "Upload"
                    st.rerun()


def _render_detail(inv_id: int):
    inject_css()
    inv = next((i for i in st.session_state.investigations if i["id"] == inv_id), None)
    if not inv:
        st.error("Investigation not found.")
        st.session_state.viewing_inv_id = None
        return

    if st.button("← Back to Investigations"):
        st.session_state.viewing_inv_id = None
        st.rerun()

    from utils import risk_badge, status_badge, RISK_COLORS
    import plotly.graph_objects as go

    evs = [e for e in st.session_state.evidence_items if e["investigationId"] == inv_id]
    ars = [a for a in st.session_state.analysis_results if a["investigationId"] == inv_id]

    st.markdown(
        f'<div style="margin:1rem 0 1.5rem;">'
        f'<h1 style="font-weight:800;font-size:1.8rem;margin-bottom:0.4rem;">{inv["title"]}</h1>'
        f'<div style="display:flex;align-items:center;gap:1rem;">'
        f'{status_badge(inv["status"])}'
        f'<span style="color:#64748B;font-size:0.85rem;">{inv.get("description","")}</span>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Evidence", "Timeline", "Network"])

    # ── Overview ─────────────────────────────────────────────────────────────
    with tab1:
        if not ars:
            st.info("No analysis results yet. Upload and analyse evidence to see results here.")
        for a in ars:
            ev = next((e for e in evs if e["id"] == a["evidenceId"]), {})
            score = int(a.get("riskScore", 0))
            level = a.get("riskLevel", "low")
            bar_color = RISK_COLORS.get(level, ("#64748B", "#1E2D4A"))[0]
            st.markdown(
                f'<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:12px;padding:1.2rem;margin-bottom:1rem;">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.8rem;">'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:0.85rem;color:#94A3B8;">'
                f'📄 {ev.get("fileName","Unknown")}</span>'
                f'{risk_badge(level)}'
                f'</div>'
                f'<div style="background:#1E2D4A;border-radius:4px;height:6px;margin-bottom:0.8rem;">'
                f'<div style="background:{bar_color};height:6px;border-radius:4px;width:{score}%;"></div></div>'
                f'<div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#64748B;margin-bottom:0.8rem;">'
                f'<span>Risk Score</span><span style="font-family:\'JetBrains Mono\',monospace;font-weight:700;color:{bar_color};">{score}/100</span>'
                f'</div>'
                f'<p style="color:#94A3B8;font-size:0.85rem;line-height:1.6;">{a.get("summary","")}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
            threats = a.get("threatTypes", [])
            if threats:
                st.markdown(
                    "**Threat types:** " + "  ".join(
                        f'<code>{t}</code>' for t in threats
                    ),
                    unsafe_allow_html=True,
                )
            recs = a.get("recommendations", [])
            if recs:
                with st.expander("📋 Recommendations"):
                    for r in recs:
                        st.markdown(f"- {r}")

    # ── Evidence ──────────────────────────────────────────────────────────────
    with tab2:
        if not evs:
            st.info("No evidence attached. Upload evidence from the sidebar.")
        for ev in evs:
            ar = next((a for a in ars if a["evidenceId"] == ev["id"]), None)
            col_info, col_action = st.columns([3, 1])
            with col_info:
                status_color = {"analyzed":"#22C55E","pending":"#EAB308","failed":"#EF4444"}.get(ev["analysisStatus"],"#64748B")
                st.markdown(
                    f'<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:10px;padding:1rem;margin-bottom:0.5rem;">'
                    f'<div style="display:flex;align-items:center;gap:0.8rem;">'
                    f'<span style="font-size:1.2rem;">📄</span>'
                    f'<div><div style="font-weight:600;">{ev["fileName"]}</div>'
                    f'<div style="font-size:0.75rem;color:#64748B;">'
                    f'{ev["fileType"].upper()} · '
                    f'<span style="color:{status_color};">{ev["analysisStatus"].upper()}</span></div></div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
            with col_action:
                if not ar:
                    if st.button("🔬 Analyse", key=f"analyse_{ev['id']}", use_container_width=True):
                        with st.spinner("Running AI analysis…"):
                            from utils import analyze_with_openai, add_analysis
                            try:
                                result = analyze_with_openai(ev["content"], ev["fileName"])
                            except Exception as exc:
                                st.error(f"OpenAI error: {exc}")
                                result = None
                            if result:
                                add_analysis(ev["id"], ev["investigationId"], result)
                                st.success("Analysis complete!")
                                st.rerun()
                else:
                    st.markdown(
                        f'<div style="padding:0.5rem;text-align:center;font-size:0.8rem;color:#22C55E;">✅ Analysed</div>',
                        unsafe_allow_html=True,
                    )

    # ── Timeline ──────────────────────────────────────────────────────────────
    with tab3:
        all_events = []
        for a in ars:
            for ev in a.get("timelineEvents", []):
                all_events.append(ev)

        if not all_events:
            st.info("No timeline events extracted yet.")
        else:
            all_events.sort(key=lambda e: str(e.get("date", "")))
            for ev in all_events:
                sev = ev.get("severity", "low")
                color = {"low":"#22C55E","medium":"#EAB308","high":"#EF4444"}.get(sev,"#64748B")
                st.markdown(
                    f'<div style="border-left:3px solid {color};padding:0.7rem 1rem;'
                    f'margin-bottom:0.8rem;background:#0D1526;border-radius:0 10px 10px 0;">'
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.75rem;color:#64748B;">{ev.get("date","")}</div>'
                    f'<div style="font-size:0.9rem;color:#F1F5F9;margin-top:2px;">{ev.get("description","")}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

    # ── Network graph ─────────────────────────────────────────────────────────
    with tab4:
        all_nodes, all_edges = [], []
        for a in ars:
            all_nodes.extend(a.get("networkNodes", []))
            all_edges.extend(a.get("networkEdges", []))

        if not all_nodes:
            st.info("No network entities extracted yet.")
        else:
            import math
            n = len(all_nodes)
            pos = {}
            for idx, node in enumerate(all_nodes):
                angle = 2 * math.pi * idx / n
                pos[node["id"]] = (math.cos(angle), math.sin(angle))

            edge_x, edge_y = [], []
            for e in all_edges:
                if e["source"] in pos and e["target"] in pos:
                    x0,y0 = pos[e["source"]]; x1,y1 = pos[e["target"]]
                    edge_x += [x0,x1,None]; edge_y += [y0,y1,None]

            node_x = [pos[n["id"]][0] for n in all_nodes]
            node_y = [pos[n["id"]][1] for n in all_nodes]
            node_labels = [n["label"] for n in all_nodes]
            type_colors = {"sender":"#3B82F6","receiver":"#22C55E","url":"#F97316","domain":"#A78BFA"}
            node_colors = [type_colors.get(n.get("type","sender"),"#64748B") for n in all_nodes]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=edge_x, y=edge_y, mode="lines",
                line=dict(color="#1E2D4A", width=1.5), hoverinfo="none",
            ))
            fig.add_trace(go.Scatter(
                x=node_x, y=node_y, mode="markers+text",
                text=node_labels, textposition="top center",
                textfont=dict(color="#94A3B8", size=11),
                marker=dict(size=14, color=node_colors, line=dict(color="#0D1526", width=2)),
                hoverinfo="text",
            ))
            fig.update_layout(
                paper_bgcolor="#0D1526", plot_bgcolor="#0D1526",
                showlegend=False,
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                margin=dict(l=0, r=0, t=10, b=0), height=400,
            )
            st.plotly_chart(fig, use_container_width=True)
