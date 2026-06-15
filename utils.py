import streamlit as st
import openai
import json
import os
import re
from datetime import datetime

# ── Shared CSS injected on every page ──────────────────────────────────────
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background-color: #060B18 !important;
    color: #F1F5F9 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="stSidebar"] {
    background-color: #0D1526 !important;
    border-right: 1px solid #1E2D4A !important;
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] a:hover { color: #3B82F6 !important; }
section[data-testid="stSidebar"] > div { padding-top: 1.5rem !important; }

/* Cards */
div[data-testid="stMetric"] {
    background: #0D1526;
    border: 1px solid #1E2D4A;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
}
div[data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; font-size: 2.4rem !important; font-weight: 800 !important; }
div[data-testid="stMetricLabel"] { font-size: 0.7rem !important; text-transform: uppercase; letter-spacing: 0.08em; color: #64748B !important; }

/* Buttons */
.stButton > button {
    background: #3B82F6 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.5rem !important;
    transition: background 0.2s;
}
.stButton > button:hover { background: #2563EB !important; }
.stButton > button[kind="secondary"] { background: #1E2D4A !important; }

/* Text inputs */
.stTextArea textarea, .stTextInput input, .stSelectbox select {
    background: #0D1526 !important;
    border: 1px solid #1E2D4A !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* Expander */
details { background: #0D1526 !important; border: 1px solid #1E2D4A !important; border-radius: 10px !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #0D1526 !important; border-bottom: 1px solid #1E2D4A !important; }
.stTabs [data-baseweb="tab"] { color: #64748B !important; font-weight: 600 !important; }
.stTabs [aria-selected="true"] { color: #3B82F6 !important; border-bottom: 2px solid #3B82F6 !important; }

/* Hide default streamlit decoration */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; max-width: 1200px !important; }

/* Code blocks */
code { font-family: 'JetBrains Mono', monospace !important; background: #0D1526 !important; color: #3B82F6 !important; padding: 2px 6px; border-radius: 4px; }

/* Progress / risk bar colours applied inline */
</style>
"""

def inject_css():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Risk helpers ────────────────────────────────────────────────────────────
RISK_COLORS = {
    "low":      ("#22C55E", "#052E16"),
    "medium":   ("#EAB308", "#1A1400"),
    "high":     ("#F97316", "#1A0800"),
    "critical": ("#EF4444", "#200000"),
}

def risk_badge(level: str) -> str:
    color, bg = RISK_COLORS.get(level.lower(), ("#64748B", "#1E2D4A"))
    return (
        f'<span style="background:{bg};color:{color};border:1.5px solid {color}50;'
        f'border-radius:6px;padding:3px 10px;font-size:0.7rem;'
        f'font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">{level.upper()}</span>'
    )

def status_badge(status: str) -> str:
    colors = {
        "open":        ("#3B82F6", "#0D1526"),
        "in_progress": ("#EAB308", "#1A1400"),
        "closed":      ("#64748B", "#1E2D4A"),
    }
    color, bg = colors.get(status.lower(), ("#64748B", "#1E2D4A"))
    return (
        f'<span style="background:{bg};color:{color};border:1.5px solid {color}50;'
        f'border-radius:6px;padding:3px 10px;font-size:0.7rem;'
        f'font-weight:700;text-transform:uppercase;letter-spacing:0.1em;">{status.replace("_"," ").upper()}</span>'
    )

def card(content_html: str, padding: str = "1.4rem 1.6rem", extra_style: str = "") -> str:
    return (
        f'<div style="background:#0D1526;border:1px solid #1E2D4A;border-radius:12px;'
        f'padding:{padding};{extra_style}">{content_html}</div>'
    )

def section_header(title: str, subtitle: str = "", icon: str = ""):
    st.markdown(
        f'<h1 style="font-family:\'Space Grotesk\',sans-serif;font-weight:800;'
        f'font-size:2rem;letter-spacing:-0.02em;margin-bottom:0.2rem;">'
        f'{icon} {title}</h1>'
        + (f'<p style="color:#64748B;margin-top:0.2rem;margin-bottom:1.5rem;">{subtitle}</p>' if subtitle else ""),
        unsafe_allow_html=True,
    )

# ── OpenAI threat analysis ──────────────────────────────────────────────────
def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")
    if not api_key:
        st.error("⚠️ OPENAI_API_KEY not found. Add it to Streamlit secrets or your environment.")
        st.stop()
    return openai.OpenAI(api_key=api_key)

def analyze_with_openai(content: str, file_name: str = "evidence.txt") -> dict:
    client = get_openai_client()
    prompt = f"""You are a cybercrime analyst AI. Analyze the following digital evidence content for cyber threats.

File: {file_name}
Content:
{content[:4000]}

Return a JSON object with EXACTLY this structure:
{{
  "riskScore": <integer 0-100>,
  "riskLevel": <"low"|"medium"|"high"|"critical">,
  "threatTypes": [<list of strings: "phishing","scam","fraud","malware","social_engineering">],
  "keywords": [<up to 10 suspicious keywords>],
  "sentiment": <"positive"|"neutral"|"negative"|"suspicious">,
  "entities": [<extracted emails, phone numbers, URLs, names>],
  "summary": "<2-3 sentence analysis>",
  "recommendations": [<2-4 action items>],
  "timelineEvents": [
    {{"date": "YYYY-MM-DD", "description": "event", "severity": "low"|"medium"|"high"}}
  ],
  "networkNodes": [
    {{"id": "n1", "label": "display label", "type": "sender"|"receiver"|"url"|"domain"}}
  ],
  "networkEdges": [
    {{"source": "n1", "target": "n2", "label": "relationship"}}
  ]
}}

Rules:
- riskScore 0-20=low, 21-50=medium, 51-80=high, 81-100=critical
- Detect phishing (urgent account warnings), scam (prize/lottery), fraud (OTP/bank), malware (links/downloads), social_engineering (urgency/trust manipulation)
Return ONLY the JSON object."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    raw = response.choices[0].message.content or "{}"
    return json.loads(raw)

def quick_analyze_heuristic(text: str) -> dict:
    """Fast local heuristic — used for instant preview before OpenAI."""
    lower = text.lower()
    score = 15
    threats, keywords = [], []

    checks = [
        (["password", "verify your account", "account suspended", "login"], 35, "Phishing Attempt", ["password", "verify"]),
        (["urgent", "immediate action", "within 24 hours", "act now"], 20, "Social Engineering", ["urgent"]),
        (["you have won", "lottery", "congratulations", "prize"], 40, "Scam / Fraud", ["prize", "lottery"]),
        (["bank account", "transfer", "otp", "cvv", "swift"], 30, "Financial Fraud", ["bank", "OTP"]),
        (["click here", "http://", "bit.ly", "download now", ".exe"], 25, "Malware / Phishing Link", ["click", "download"]),
    ]
    for patterns, pts, label, kw in checks:
        if any(p in lower for p in patterns):
            score += pts
            threats.append(label)
            keywords.extend(kw)

    score = min(score, 100)
    if score >= 80: level = "critical"
    elif score >= 60: level = "high"
    elif score >= 40: level = "medium"
    else: level = "low"

    sentiment = "suspicious" if score > 40 else "neutral"
    summary = (
        f"The analyzed text presents a **{level}** risk profile. "
        + (f"Markers consistent with {', '.join(threats)} were detected. " if threats else "No obvious malicious patterns were found. ")
        + f"Overall sentiment is classified as {sentiment}."
    )
    return {
        "riskScore": score, "riskLevel": level,
        "threatTypes": threats or ["None Detected"],
        "keywords": list(set(keywords)) or [],
        "sentiment": sentiment, "entities": [],
        "summary": summary, "recommendations": [],
        "timelineEvents": [], "networkNodes": [], "networkEdges": [],
    }

# ── Session-state helpers ───────────────────────────────────────────────────
def init_state():
    defaults = {
        "investigations": [],
        "evidence_items": [],
        "analysis_results": [],
        "reports": [],
        "next_inv_id": 1,
        "next_ev_id": 1,
        "next_ar_id": 1,
        "next_rep_id": 1,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def add_investigation(title: str, description: str = "") -> dict:
    inv = {
        "id": st.session_state.next_inv_id,
        "title": title, "description": description,
        "status": "open", "evidenceCount": 0, "highRiskCount": 0,
        "createdAt": datetime.utcnow().isoformat(),
    }
    st.session_state.investigations.append(inv)
    st.session_state.next_inv_id += 1
    return inv

def add_evidence(investigation_id: int, file_name: str, file_type: str, content: str) -> dict:
    ev = {
        "id": st.session_state.next_ev_id,
        "investigationId": investigation_id,
        "fileName": file_name, "fileType": file_type,
        "content": content, "analysisStatus": "pending",
        "createdAt": datetime.utcnow().isoformat(),
    }
    st.session_state.evidence_items.append(ev)
    st.session_state.next_ev_id += 1
    for inv in st.session_state.investigations:
        if inv["id"] == investigation_id:
            inv["evidenceCount"] = inv.get("evidenceCount", 0) + 1
    return ev

def add_analysis(evidence_id: int, investigation_id: int, result: dict) -> dict:
    ar = {
        "id": st.session_state.next_ar_id,
        "evidenceId": evidence_id, "investigationId": investigation_id,
        **result,
        "createdAt": datetime.utcnow().isoformat(),
    }
    st.session_state.analysis_results.append(ar)
    st.session_state.next_ar_id += 1
    for ev in st.session_state.evidence_items:
        if ev["id"] == evidence_id:
            ev["analysisStatus"] = "analyzed"
    if result.get("riskLevel") in ("high", "critical"):
        for inv in st.session_state.investigations:
            if inv["id"] == investigation_id:
                inv["highRiskCount"] = inv.get("highRiskCount", 0) + 1
    return ar

def add_report(investigation_id: int, title: str, content: str, threat_summary: str, recommendations: list) -> dict:
    rep = {
        "id": st.session_state.next_rep_id,
        "investigationId": investigation_id,
        "title": title, "content": content,
        "threatSummary": threat_summary,
        "recommendations": recommendations,
        "createdAt": datetime.utcnow().isoformat(),
    }
    st.session_state.reports.append(rep)
    st.session_state.next_rep_id += 1
    return rep

def generate_report_with_ai(investigation_id: int, title: str = "") -> dict:
    client = get_openai_client()
    inv = next((i for i in st.session_state.investigations if i["id"] == investigation_id), None)
    if not inv:
        return {}
    analysis_rows = [a for a in st.session_state.analysis_results if a["investigationId"] == investigation_id]
    prompt = f"""You are a cybercrime analyst. Generate a concise investigation report for:

Investigation: {inv['title']}
Description: {inv.get('description', 'N/A')}
Status: {inv['status']}
Evidence analyzed: {len(analysis_rows)}

Analysis summaries:
{chr(10).join(f"{i+1}. Risk: {a['riskLevel']} ({a['riskScore']}/100). Threats: {', '.join(a.get('threatTypes', [])) or 'none'}. {a.get('summary', '')}" for i, a in enumerate(analysis_rows))}

Return JSON: {{"content": "<full report 200-400 words>", "threatSummary": "<1-2 sentence overview>", "recommendations": ["<rec1>", "<rec2>", "<rec3>"]}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini", max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    raw = json.loads(response.choices[0].message.content or "{}")
    final_title = title or f"Investigation Report: {inv['title']}"
    return add_report(
        investigation_id, final_title,
        raw.get("content", ""),
        raw.get("threatSummary", ""),
        raw.get("recommendations", []),
    )
