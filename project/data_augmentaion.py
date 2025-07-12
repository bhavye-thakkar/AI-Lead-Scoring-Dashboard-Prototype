import pandas as pd
from faker import Faker
import numpy as np

# Load base dataset
df = pd.read_csv("loan_prediction.csv")

# Initialize Faker for synthetic data
fake = Faker('en_IN')

# Augment to 10,000 rows
augmented = []
for _ in range(10000):
    # Randomly sample from original dataset
    sample = df.sample(1).iloc[0]
    
    # Generate synthetic PII
    phone = f"+91-{fake.msisdn()[3:]}"
    email = fake.email()
    
    # Map credit history to score
    credit_score = np.random.randint(650, 851) if sample['Credit_History'] == 1 else np.random.randint(300, 650)
    
    # Create age groups
    age_bins = ["18-25", "26-35", "36-50", "51+"]
    age_group = np.random.choice(age_bins, p=[0.15, 0.4, 0.35, 0.1])
    
    # Define family background
    if sample['Married'] == 'Yes':
        family = "Married with Kids" if int(sample['Dependents'].rstrip('+')) > 0 else "Married"
    else:
        family = "Single"
    
    # Generate comments with intent keywords
    comments = ""
    if np.random.rand() > 0.7:
        keywords = ["urgent", "ASAP", "immediately", "quick", "emergency"]
        comments = f"Need funds {np.random.choice(keywords)} for {fake.word()}"

    augmented.append({
        'phone_number': phone,
        'email': email,
        'credit_score': credit_score,
        'age_group': age_group,
        'family_background': family,
        'income': sample['ApplicantIncome'] + sample['CoapplicantIncome'],
        'employment_status': f"{sample['Education']}/{sample['Self_Employed']}",
        'property_type': np.random.choice(["Residential", "Commercial", "Land"]),
        'location_tier': sample['Property_Area'],
        'prior_inquiries': np.random.randint(0, 6),
        'comments': comments,
        'high_intent': 1 if sample['Loan_Status'] == 'Y' else 0
    })

# Create final dataset
final_df = pd.DataFrame(augmented)
final_df.to_csv("lead_scoring_dataset.csv", index=False)