import streamlit as st
from utils import inject_css, section_header, add_evidence

def render():
    inject_css()
    section_header(
        "Ingest Evidence",
        "Feed raw data, logs, emails, or text fragments into the CyberLens AI engine.",
        "📤",
    )

    invs = st.session_state.get("investigations", [])
    active = [i for i in invs if i["status"] != "closed"]

    if not active:
        st.warning(
            "No active investigations found. "
            "[Create one first →](#investigations)"
        )
        if st.button("➕ Create Investigation"):
            st.session_state.page = "Investigations"
            st.session_state.show_new_inv_form = True
            st.rerun()
        return

    # Pre-fill if navigated from investigation detail
    prefill_id = st.session_state.pop("prefill_inv_id", None)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown(
            '<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:12px;overflow:hidden;">',
            unsafe_allow_html=True,
        )

        tab_text, tab_file = st.tabs(["📝 Raw Text Entry", "📁 Upload File (CSV/JSON/TXT)"])

        with tab_text:
            inv_options = {f"#{i['id']} — {i['title']}": i["id"] for i in active}
            default_idx = 0
            if prefill_id:
                keys = list(inv_options.keys())
                for k, v in inv_options.items():
                    if v == prefill_id:
                        default_idx = keys.index(k)
                        break

            selected_key = st.selectbox(
                "Target Investigation *",
                list(inv_options.keys()),
                index=default_idx,
                key="text_inv_select",
            )
            inv_id = inv_options[selected_key]
            file_name = st.text_input(
                "Reference Name *",
                placeholder="e.g. phishing_email.txt",
                key="text_file_name",
            )
            content = st.text_area(
                "Payload Content *",
                placeholder="Paste suspicious email body, chat logs, or text here…",
                height=320,
                key="text_content",
            )

            st.markdown(
                '<div style="background:#0D0F1A;padding:0.8rem 1rem;border-top:1px solid #1E2D4A;'
                'display:flex;align-items:center;justify-content:space-between;">'
                '<span style="color:#64748B;font-size:0.8rem;">⚡ Submission triggers immediate AI analysis pipeline.</span>'
                '</div>',
                unsafe_allow_html=True,
            )

            col_sub, col_an = st.columns(2)
            with col_sub:
                if st.button("💾 Save Only", use_container_width=True, key="save_text"):
                    if not file_name.strip() or not content.strip():
                        st.error("Reference name and content are required.")
                    else:
                        add_evidence(inv_id, file_name.strip(), "text", content.strip())
                        st.success("✅ Evidence saved!")
            with col_an:
                if st.button("🔬 Save & Analyse", use_container_width=True, key="save_analyse_text"):
                    if not file_name.strip() or not content.strip():
                        st.error("Reference name and content are required.")
                    elif len(content.strip()) < 10:
                        st.error("Content must be at least 10 characters.")
                    else:
                        ev = add_evidence(inv_id, file_name.strip(), "text", content.strip())
                        with st.spinner("Running AI analysis via OpenAI…"):
                            from utils import analyze_with_openai, add_analysis
                            try:
                                result = analyze_with_openai(ev["content"], ev["fileName"])
                                add_analysis(ev["id"], ev["investigationId"], result)
                                st.success("✅ Evidence uploaded and analysed!")
                                st.session_state.viewing_inv_id = inv_id
                                st.session_state.page = "Investigations"
                                st.rerun()
                            except Exception as exc:
                                st.error(f"Analysis failed: {exc}")

        with tab_file:
            inv_options2 = {f"#{i['id']} — {i['title']}": i["id"] for i in active}
            sel2 = st.selectbox("Target Investigation *", list(inv_options2.keys()), key="file_inv_select")
            inv_id2 = inv_options2[sel2]
            fmt = st.selectbox("Data Format", ["CSV", "JSON", "TXT"], key="file_fmt")
            uploaded = st.file_uploader(
                "Upload file",
                type=["csv", "json", "txt"],
                key="file_upload",
            )

            if uploaded:
                file_content = uploaded.read().decode("utf-8", errors="replace")
                st.text_area("Preview (first 500 chars)", file_content[:500], height=120, disabled=True)

                col_s, col_a = st.columns(2)
                with col_s:
                    if st.button("💾 Save Only", use_container_width=True, key="save_file"):
                        add_evidence(inv_id2, uploaded.name, fmt.lower(), file_content)
                        st.success("✅ Evidence saved!")
                with col_a:
                    if st.button("🔬 Save & Analyse", use_container_width=True, key="analyse_file"):
                        ev = add_evidence(inv_id2, uploaded.name, fmt.lower(), file_content)
                        with st.spinner("Running AI analysis…"):
                            from utils import analyze_with_openai, add_analysis
                            try:
                                result = analyze_with_openai(ev["content"], ev["fileName"])
                                add_analysis(ev["id"], ev["investigationId"], result)
                                st.success("✅ Analysed!")
                                st.session_state.viewing_inv_id = inv_id2
                                st.session_state.page = "Investigations"
                                st.rerun()
                            except Exception as exc:
                                st.error(f"Analysis failed: {exc}")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:12px;padding:1.4rem;">'
            '<h4 style="font-weight:700;margin-bottom:0.8rem;">💡 Tips</h4>'
            '<ul style="color:#64748B;font-size:0.85rem;line-height:1.8;padding-left:1.2rem;">'
            '<li>Paste full email headers for best phishing detection.</li>'
            '<li>Include full URLs — shortened links are a red flag.</li>'
            '<li>CSV logs: include headers row for better entity extraction.</li>'
            '<li>JSON dumps: full objects give richer network graph data.</li>'
            '<li>Minimum 10 characters required for analysis.</li>'
            '</ul>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Show recent evidence
        evs = sorted(
            st.session_state.get("evidence_items", []),
            key=lambda e: e["createdAt"],
            reverse=True,
        )[:5]
        if evs:
            st.markdown(
                '<h4 style="font-weight:700;margin-bottom:0.8rem;">Recent Evidence</h4>',
                unsafe_allow_html=True,
            )
            for e in evs:
                sc = {"analyzed":"#22C55E","pending":"#EAB308","failed":"#EF4444"}.get(e["analysisStatus"],"#64748B")
                st.markdown(
                    f'<div style="background:#060B18;border:1px solid #1E2D4A;border-radius:8px;'
                    f'padding:0.7rem;margin-bottom:0.5rem;">'
                    f'<div style="font-size:0.82rem;font-weight:600;">{e["fileName"]}</div>'
                    f'<div style="font-size:0.72rem;color:#475569;margin-top:2px;">'
                    f'{e["fileType"].upper()} · <span style="color:{sc};">{e["analysisStatus"].upper()}</span></div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )
