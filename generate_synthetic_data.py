import pandas as pd
import numpy as np
import uuid
import random

# Define all categories
genders = ['Male', 'Female', 'Other']
regions = ['Northeast', 'Midwest', 'South', 'West']
visit_types = ['Emergency', 'Primary Care', 'Inpatient', 'Outpatient']
ages = list(range(0, 101))  # Full age range 0 to 100

# Generate robust combinations
records = []
for gender in genders:
    for region in regions:
        for visit_type in visit_types:
            for age in ages:
                cost = round(random.uniform(100, 5000), 2)
                records.append({
                    "member_id": str(uuid.uuid4()),
                    "age": age,
                    "gender": gender,
                    "region": region,
                    "visit_type": visit_type,
                    "service_date": "2024-05-01",
                    "cost": cost,
                    "diagnosis_code": "E11.9",
                    "insurance_paid": round(cost * random.uniform(0.6, 1.0), 2),
                    "member_paid": round(cost * random.uniform(0.0, 0.4), 2)
                })

# Create DataFrame and save
df = pd.DataFrame(records)
df.to_csv("robust_healthcare_costs.csv", index=False)
print("✅ Synthetic data saved to robust_healthcare_costs.csv")
