# generate_data.py
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker('en_IN')

# Generate 10,000 records
data = []
for _ in range(10000):
    record = {
        "phone_number": f"+91-{fake.msisdn()[3:]}",
        "email": fake.email(),
        "credit_score": np.random.randint(300, 851),
        "age_group": np.random.choice(["18-25", "26-35", "36-50", "51+"], p=[0.2, 0.4, 0.3, 0.1]),
        "family_background": np.random.choice(["Single", "Married", "Married with Kids"], p=[0.3, 0.4, 0.3]),
        "income": np.random.randint(100000, 1000001),
        "employment_status": np.random.choice(["Employed", "Self-Employed", "Unemployed"], p=[0.7, 0.2, 0.1]),
        "property_type": np.random.choice(["Residential", "Commercial", "Land"], p=[0.6, 0.3, 0.1]),
        "location_tier": np.random.choice(["Tier 1", "Tier 2", "Tier 3"], p=[0.5, 0.3, 0.2]),
        "prior_inquiries": np.random.randint(0, 11),
        "comments": np.random.choice(["Urgent need", "Just browsing", "Need ASAP", "Not interested", ""], p=[0.1, 0.3, 0.1, 0.1, 0.4])
    }
    data.append(record)

df = pd.DataFrame(data)
df.to_csv("lead_data.csv", index=False)