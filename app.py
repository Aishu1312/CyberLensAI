import streamlit as st

from modules.upload import upload_file
from modules.timeline import create_timeline
from modules.threat_detection import detect_threat

st.set_page_config(
    page_title="CyberLens AI",
    layout="wide"
)

st.title("🛡 CyberLens AI")

df = upload_file()

if df is not None:

    for msg in df["Message"]:

        score, level, words = detect_threat(msg)

        st.write(msg)
        st.write(level)
    st.dataframe(df)
