import streamlit as st
from utils import inject_css, section_header, risk_badge, quick_analyze_heuristic, RISK_COLORS

def render():
    inject_css()
    section_header(
        "Quick Analyze",
        "Instantly evaluate text, emails, or messages for threat vectors without creating a full investigation.",
        "⚡",
    )

    col_input, col_result = st.columns([3, 2], gap="large")

    with col_input:
        st.markdown(
            '<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:12px;overflow:hidden;">'
            '<div style="background:#0A1020;border-bottom:1px solid #1E2D4A;padding:0.8rem 1.2rem;">'
            '<span style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:#64748B;font-weight:700;">Raw Input Buffer</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        text = st.text_area(
            label="text_input",
            label_visibility="collapsed",
            placeholder="Paste suspicious content here for immediate evaluation…",
            height=380,
            key="quick_analyze_text",
        )

        st.markdown(
            '<div style="background:#0A1020;border-top:1px solid #1E2D4A;padding:0.8rem 1.2rem;">'
            '</div></div>',
            unsafe_allow_html=True,
        )

        use_ai = st.checkbox(
            "🤖 Use OpenAI (more accurate, uses API key)",
            value=True,
            key="use_ai_toggle",
        )

        btn_col, clear_col = st.columns([3, 1])
        with btn_col:
            scan_clicked = st.button("🔬 Scan Text", use_container_width=True, key="scan_btn")
        with clear_col:
            if st.button("🗑 Clear", use_container_width=True, key="clear_btn"):
                st.session_state.quick_analyze_text = ""
                st.session_state.pop("quick_result", None)
                st.rerun()

        if scan_clicked:
            if not text or len(text.strip()) < 10:
                st.error("Please enter at least 10 characters.")
            else:
                if use_ai:
                    with st.spinner("🧠 Analysing semantics & threat vectors…"):
                        from utils import analyze_with_openai
                        try:
                            result = analyze_with_openai(text.strip(), "quick_scan.txt")
                            st.session_state.quick_result = result
                        except Exception as exc:
                            st.error(f"OpenAI error: {exc}. Falling back to heuristic.")
                            st.session_state.quick_result = quick_analyze_heuristic(text.strip())
                else:
                    import time; time.sleep(0.4)
                    st.session_state.quick_result = quick_analyze_heuristic(text.strip())
                st.rerun()

    with col_result:
        st.markdown(
            '<h3 style="font-weight:700;font-size:1.05rem;margin-bottom:1rem;">👁 Analysis Output</h3>',
            unsafe_allow_html=True,
        )

        result = st.session_state.get("quick_result")

        if not result:
            st.markdown(
                '<div style="border:2px dashed #1E2D4A;border-radius:16px;padding:3rem;'
                'text-align:center;background:#0D1526;">'
                '<div style="font-size:2.5rem;margin-bottom:0.8rem;opacity:0.3;">🛡️</div>'
                '<p style="color:#475569;font-weight:600;">Awaiting Input</p>'
                '<p style="color:#334155;font-size:0.82rem;margin-top:0.4rem;">'
                'Enter text and scan to view threat intelligence.</p>'
                '</div>',
                unsafe_allow_html=True,
            )
        else:
            score = int(result.get("riskScore", 0))
            level = result.get("riskLevel", "low")
            bar_color, bg_color = RISK_COLORS.get(level, ("#64748B", "#1E2D4A"))

            # Big score card
            st.markdown(
                f'<div style="background:{bg_color};border:1px solid {bar_color}40;'
                f'border-radius:12px 12px 0 0;padding:2rem;text-align:center;'
                f'position:relative;overflow:hidden;">'
                f'<div style="position:absolute;inset:0;background:radial-gradient(circle at center,{bar_color}15,transparent);"></div>'
                f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:5rem;font-weight:900;'
                f'color:{bar_color};line-height:1;">{score}</div>'
                f'<div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.15em;'
                f'color:#64748B;font-weight:700;margin:0.4rem 0 1rem;">Risk Score</div>'
                f'{risk_badge(level)}'
                f'</div>',
                unsafe_allow_html=True,
            )

            threats = result.get("threatTypes", [])
            keywords = result.get("keywords", [])
            entities = result.get("entities", [])
            sentiment = result.get("sentiment", "neutral")
            summary = result.get("summary", "")
            recs = result.get("recommendations", [])

            st.markdown(
                '<div style="background:#0D1526;border:1px solid #1E2D4A;border-top:none;'
                'border-radius:0 0 12px 12px;padding:1.4rem;">',
                unsafe_allow_html=True,
            )

            st.markdown(
                '<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
                'letter-spacing:0.1em;color:#64748B;margin-bottom:0.5rem;">Classification</div>',
                unsafe_allow_html=True,
            )
            if threats:
                badges = " ".join(
                    f'<code style="background:#1E2D4A;color:#F1F5F9;padding:3px 8px;border-radius:6px;font-size:0.78rem;">{t}</code>'
                    for t in threats
                )
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.markdown('<code style="color:#22C55E;">✅ None Detected</code>', unsafe_allow_html=True)

            if keywords:
                st.markdown(
                    '<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
                    'letter-spacing:0.1em;color:#64748B;margin:1rem 0 0.5rem;">Extracted Vectors</div>',
                    unsafe_allow_html=True,
                )
                kw_html = " ".join(
                    f'<span style="background:#0A1020;color:#94A3B8;border:1px solid #1E2D4A;'
                    f'padding:2px 8px;border-radius:4px;font-family:\'JetBrains Mono\',monospace;font-size:0.75rem;">{k}</span>'
                    for k in keywords
                )
                st.markdown(kw_html, unsafe_allow_html=True)

            if entities:
                st.markdown(
                    '<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
                    'letter-spacing:0.1em;color:#64748B;margin:1rem 0 0.5rem;">Entities</div>',
                    unsafe_allow_html=True,
                )
                ent_html = " ".join(
                    f'<code style="background:#1A0A2A;color:#A78BFA;padding:2px 8px;'
                    f'border-radius:4px;font-size:0.75rem;">{e}</code>'
                    for e in entities[:8]
                )
                st.markdown(ent_html, unsafe_allow_html=True)

            st.markdown(
                f'<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:0.1em;color:#64748B;margin:1rem 0 0.5rem;">Intelligence Summary</div>'
                f'<div style="background:#060B18;border:1px solid #1E2D4A;border-radius:8px;'
                f'padding:0.9rem;font-size:0.85rem;color:#CBD5E1;line-height:1.6;">{summary}</div>',
                unsafe_allow_html=True,
            )

            if recs:
                st.markdown(
                    '<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
                    'letter-spacing:0.1em;color:#64748B;margin:1rem 0 0.5rem;">Recommendations</div>',
                    unsafe_allow_html=True,
                )
                for r in recs:
                    st.markdown(f"→ {r}")

            st.markdown('</div>', unsafe_allow_html=True)

            # Sentiment chip
            sent_colors = {
                "suspicious":"#EF4444","negative":"#F97316",
                "neutral":"#64748B","positive":"#22C55E",
            }
            sc = sent_colors.get(sentiment, "#64748B")
            st.markdown(
                f'<div style="margin-top:0.8rem;text-align:right;">'
                f'<span style="font-size:0.72rem;color:{sc};font-weight:700;text-transform:uppercase;'
                f'background:{sc}15;border:1px solid {sc}30;padding:3px 10px;border-radius:999px;">'
                f'Sentiment: {sentiment}</span></div>',
                unsafe_allow_html=True,
            )
