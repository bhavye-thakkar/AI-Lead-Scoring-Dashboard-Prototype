# AI Lead Scoring Dashboard

## 🚀 Overview
This is a web-based Lead Scoring Dashboard built for a 48-hour solo challenge. It predicts lead intent using a machine learning model and adjusts the score using a rule-based LLM-like reranker, then serves it via a FastAPI backend. The frontend (React-based) allows user inputs and displays the scored leads.

---

## 📁 Project Structure
```
├── backend/
│   ├── main.py              # FastAPI backend code
│   ├── model.pkl            # Trained Gradient Boosting model
│   ├── age_encoder.pkl      # Label encoder for Age Group
│   ├── fam_encoder.pkl      # Label encoder for Family Background
├── data/
│   └── lead_data.csv        # Synthetic dataset (~10,000 rows)
├── frontend/                # React frontend (to be added)
├── report.pdf               # 3-page report with overview, logic, and evaluation
```

---

## 💡 Features
- Gradient Boosting Model for predicting lead intent (0–100)
- Rule-based reranker adjusts score using keywords in comments
- FastAPI backend with input validation and memory storage
- CSV-based synthetic dataset with logical patterns
- Consent checkbox compliance

---

## 🧠 Model Details
- Model: `GradientBoostingClassifier` (scikit-learn)
- Features Used:
  - Credit Score
  - Income
  - Age Group
  - Family Background
- Target: Lead Intent (binary → scaled to 0–100)

---

## 🔄 API Endpoint
**POST** `/score`
### Request JSON
```
{
  "phone_number": "+91-9876543210",
  "email": "john@example.com",
  "credit_score": 720,
  "income": 750000,
  "age_group": "26–35",
  "family_background": "Married",
  "comments": "urgent",
  "consent": true
}
```

### Response JSON
```
{
  "email": "john@example.com",
  "initial_score": 87.3,
  "reranked_score": 97.3,
  "comments": "urgent"
}
```

---

## 🛠️ Local Setup
1. **Clone Repository**
```bash
git clone https://github.com/your-username/lead-scoring-dashboard.git
cd lead-scoring-dashboard/backend
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Run FastAPI Server**
```bash
uvicorn main:app --reload
```

---

## 🧪 Model Training (optional)
Re-run model training from scratch if needed:
```python
python model_training.py  # custom script with dataset and joblib save
```

---

## 📝 Authors & Credits
**Author**: Bhavye Thakkar  
**LinkedIn**: [linkedin.com/in/bhavye-thakkar](https://linkedin.com/in/bhavye-thakkar)  
**GitHub**: [github.com/bhavyethakkar](https://github.com/bhavyethakkar)

---

## 📄 License
This project uses only synthetic and dummy data. No real PII is processed. Compliance with data privacy norms like India's DPDP Bill is simulated.

---

> 🌐 Deployed App: [Link to Netlify App](#)  
> 🧠 API Hosted: [Link to Render/Fly.io FastAPI](#)
