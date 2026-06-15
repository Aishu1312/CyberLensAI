from fastapi import FastAPI
from pydantic import BaseModel
import spacy
import re

app = FastAPI(title="CyberLensAI Backend Engine")

# Load the NLP model (Ensure you run: python -m spacy download en_core_web_sm before deploying)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class EvidenceRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(req: EvidenceRequest):
    doc = nlp(req.text)
    
    # AI Entity Extraction (Names, Orgs, Dates, Money)
    entities = [{"entity": ent.text, "category": ent.label_} for ent in doc.ents]
    
    # Pattern-based Extraction (IP Addresses & Emails)
    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', req.text)
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', req.text)
    
    return {
        "nlp_entities": entities,
        "network_ips": list(set(ips)),
        "suspect_emails": list(set(emails)),
        "status": "Analysis Complete"
    }
