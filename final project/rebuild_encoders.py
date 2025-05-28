
import pandas as pd
import os
import joblib
from sklearn.preprocessing import LabelEncoder

# Load the original dataset
df = pd.read_csv("Intersection_crashData_Clean_4.27.csv")
df.columns = df.columns.str.strip()

# Define the 6 target columns used in the model
target_columns = [
    'unit_1_direction',
    'unit_1_movement',
    'unit_2_direction',
    'unit_2_movement',
    'unit_at_fault',
    'crash_type'
]

# Create directory for saved encoders
os.makedirs("multihead_saved_encoders", exist_ok=True)

# Fit and save each encoder
for col in target_columns:
    le = LabelEncoder()
    df[col] = df[col].astype(str)  # Ensure text format
    le.fit(df[col])
    joblib.dump(le, f"multihead_saved_encoders/{col}_encoder.pkl")
    print(f"✅ Saved encoder for: {col}")
