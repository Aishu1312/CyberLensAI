import pandas as pd
import streamlit as st

def upload_file():
    uploaded_file = st.file_uploader(
        "Upload Evidence File",
        type=["csv"]
    )

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        return df

    return None
