import streamlit as st
import requests

st.set_page_config(page_title="CyberLensAI Dashboard", layout="wide")
st.title("CyberLensAI - Digital Evidence Analyzer")

# Point this to your deployed Cloud Run URL once live
API_URL = "http://localhost:8000/analyze" 

st.markdown("### Upload Digital Evidence")
log_input = st.text_area("Paste raw chat transcripts, server logs, or emails here:", height=200)

if st.button("Run Forensic Analysis"):
    if log_input:
        with st.spinner("AI Engine is scanning for digital artifacts..."):
            try:
                response = requests.post(API_URL, json={"text": log_input})
                if response.status_code == 200:
                    data = response.json()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Network & Comms Artifacts")
                        st.write("**Extracted IPs:**", data["network_ips"] if data["network_ips"] else "None detected")
                        st.write("**Extracted Emails:**", data["suspect_emails"] if data["suspect_emails"] else "None detected")
                    
                    with col2:
                        st.subheader("NLP Extracted Entities")
                        if data["nlp_entities"]:
                            st.dataframe(data["nlp_entities"], use_container_width=True)
                        else:
                            st.write("No contextual entities found.")
                else:
                    st.error("Engine failed to process the evidence.")
            except Exception as e:
                st.error(f"Failed to connect to backend engine: {e}")
    else:
        st.warning("Please input text data to analyze.")
