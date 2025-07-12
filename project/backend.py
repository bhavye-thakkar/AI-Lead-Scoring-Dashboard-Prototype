# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import joblib
import numpy as np
import re
import pandas as pd

app = FastAPI()

# Load model
model = joblib.load('lead_model.pkl')
preprocessor = joblib.load('preprocessor.pkl')

# In-memory storage
leads = []

# Keyword scoring rules
KEYWORD_RULES = {
    r'\burgen(t|cy)\b': 15,
    r'\basap\b': 10,
    r'\bimmediate(ly)?\b': 10,
    r'\bnot interested\b': -20,
    r'\bjust looking\b': -15,
    r'\bbrowse\b': -10
}

class Lead(BaseModel):
    phone_number: str
    email: EmailStr
    credit_score: int
    age_group: str
    family_background: str
    income: int
    employment_status: str
    property_type: str
    location_tier: str
    prior_inquiries: int
    comments: str = ""
    consent: bool

def apply_keyword_adjustment(comment: str) -> int:
    adjustment = 0
    for pattern, score in KEYWORD_RULES.items():
        if re.search(pattern, comment, re.IGNORECASE):
            adjustment += score
    return adjustment

@app.post("/score")
async def score_lead(lead: Lead):
    if not lead.consent:
        raise HTTPException(status_code=400, detail="Consent required")
    
    # Prepare data for model
    input_data = {
        'credit_score': [lead.credit_score],
        'age_group': [lead.age_group],
        'family_background': [lead.family_background],
        'income': [lead.income],
        'employment_status': [lead.employment_status],
        'property_type': [lead.property_type],
        'location_tier': [lead.location_tier],
        'prior_inquiries': [lead.prior_inquiries]
    }
    
    # Preprocess and predict
    processed = preprocessor.transform(pd.DataFrame(input_data))
    proba = model.predict_proba(processed)[0][1]
    initial_score = int(proba * 100)
    
    # Apply keyword adjustment
    adjustment = apply_keyword_adjustment(lead.comments)
    reranked_score = min(max(initial_score + adjustment, 0), 100)
    
    # Store lead
    lead_record = lead.dict()
    lead_record.update({
        "initial_score": initial_score,
        "reranked_score": reranked_score,
        "id": len(leads) + 1
    })
    leads.append(lead_record)
    
    return {
        "initial_score": initial_score,
        "reranked_score": reranked_score,
        "id": lead_record["id"]
    }

@app.get("/leads")
async def get_leads():
    return leads