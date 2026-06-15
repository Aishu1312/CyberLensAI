import streamlit as st
from datetime import datetime
from utils import inject_css, section_header, generate_report_with_ai

def render():
    inject_css()
    section_header(
        "Intelligence Reports",
        "Generated briefs summarising evidence analysis and threat findings.",
        "📄",
    )

    col_title, col_btn = st.columns([4, 1])
    with col_btn:
        if st.button("➕ Generate Report", use_container_width=True):
            st.session_state.show_gen_report = True

    # Generate report form
    if st.session_state.get("show_gen_report"):
        invs = st.session_state.get("investigations", [])
        if not invs:
            st.warning("Create an investigation first.")
            st.session_state.show_gen_report = False
        else:
            with st.expander("📝 Generate New Report", expanded=True):
                with st.form("gen_report_form"):
                    inv_options = {f"#{i['id']} — {i['title']}": i["id"] for i in invs}
                    sel = st.selectbox("Source Investigation *", list(inv_options.keys()))
                    custom_title = st.text_input("Custom Title (optional)", placeholder="Leave blank to use investigation name")
                    submitted = st.form_submit_button("🤖 Generate with AI")
                    if submitted:
                        inv_id = inv_options[sel]
                        with st.spinner("Generating AI-powered report…"):
                            try:
                                rep = generate_report_with_ai(inv_id, custom_title.strip())
                                st.success("✅ Report generated!")
                                st.session_state.show_gen_report = False
                                st.rerun()
                            except Exception as exc:
                                st.error(f"Failed to generate report: {exc}")

    reports = st.session_state.get("reports", [])

    if not reports:
        st.markdown(
            '<div style="border:2px dashed #1E2D4A;border-radius:16px;padding:4rem;'
            'text-align:center;margin-top:1.5rem;">'
            '<div style="font-size:3rem;margin-bottom:1rem;">📄</div>'
            '<h3 style="color:#94A3B8;">No reports generated</h3>'
            '<p style="color:#475569;">Select an investigation to compile a formal intelligence brief.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(3)
    for i, rep in enumerate(sorted(reports, key=lambda r: r["createdAt"], reverse=True)):
        with cols[i % 3]:
            ts = datetime.fromisoformat(rep["createdAt"]).strftime("%b %d, %Y")
            st.markdown(
                f'<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:12px;'
                f'padding:1.4rem;margin-bottom:1rem;position:relative;overflow:hidden;">'
                f'<div style="position:absolute;top:0;right:0;width:60px;height:60px;'
                f'background:rgba(59,130,246,0.05);border-radius:0 0 0 999px;pointer-events:none;"></div>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.68rem;'
                f'color:#475569;margin-bottom:0.6rem;">📅 {ts}</div>'
                f'<h4 style="font-weight:700;font-size:0.95rem;margin:0 0 0.3rem;line-height:1.3;">{rep["title"]}</h4>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.7rem;'
                f'color:#3B82F6;margin-bottom:0.8rem;">INV-{str(rep["investigationId"]).zfill(4)}</div>'
                f'<p style="color:#64748B;font-size:0.82rem;line-height:1.5;">'
                f'{(rep.get("threatSummary","") or "Report contains structured evidence analysis.")[:160]}…'
                f'</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

            v_col, d_col = st.columns(2)
            with v_col:
                if st.button("👁 View", key=f"view_rep_{rep['id']}", use_container_width=True):
                    st.session_state.viewing_report_id = rep["id"]

            with d_col:
                # Build text download
                download_text = (
                    f"CyberLens AI — Intelligence Report\n"
                    f"{'='*50}\n\n"
                    f"Title: {rep['title']}\n"
                    f"Investigation: INV-{str(rep['investigationId']).zfill(4)}\n"
                    f"Date: {ts}\n\n"
                    f"THREAT SUMMARY\n{'-'*30}\n{rep.get('threatSummary','')}\n\n"
                    f"FULL REPORT\n{'-'*30}\n{rep.get('content','')}\n\n"
                    f"RECOMMENDATIONS\n{'-'*30}\n"
                    + "\n".join(f"• {r}" for r in rep.get("recommendations", []))
                )
                st.download_button(
                    "⬇ Export",
                    data=download_text,
                    file_name=f"report_{rep['id']}.txt",
                    mime="text/plain",
                    key=f"dl_rep_{rep['id']}",
                    use_container_width=True,
                )

            # Inline viewer
            if st.session_state.get("viewing_report_id") == rep["id"]:
                with st.expander("📖 Full Report", expanded=True):
                    st.markdown(
                        f'<div style="background:#060B18;border:1px solid #1E2D4A;border-radius:8px;'
                        f'padding:1.2rem;font-size:0.88rem;color:#CBD5E1;line-height:1.7;">'
                        f'{rep.get("content","").replace(chr(10),"<br>")}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    recs = rep.get("recommendations", [])
                    if recs:
                        st.markdown("**Recommendations:**")
                        for r in recs:
                            st.markdown(f"→ {r}")
                    if st.button("Close", key=f"close_rep_{rep['id']}"):
                        st.session_state.viewing_report_id = None
                        st.rerun()
