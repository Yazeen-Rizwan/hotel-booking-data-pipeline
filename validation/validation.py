# Data validation logic
import pandas as pd
import os
from config.config import STAGING_FILE, ERROR_LOG, REQUIRED_COLUMNS

print("Starting Validation...")

# Load staging data
df = pd.read_csv(STAGING_FILE)

errors = []

# ----------------------------------------
# 1. Schema Validation
# ----------------------------------------
missing_columns = []

for column in REQUIRED_COLUMNS:
    if column not in df.columns:
        missing_columns.append(column)

if missing_columns:
    errors.append({
        "Error": "Missing Columns",
        "Details": ",".join(missing_columns)
    })

# ----------------------------------------
# 2. Null Validation
# ----------------------------------------
for column in REQUIRED_COLUMNS:
    if column in df.columns:
        null_count = df[column].isnull().sum()

        if null_count > 0:
            errors.append({
                "Error": "Null Values",
                "Details": f"{column}: {null_count}"
            })

# ----------------------------------------
# 3. Outlier Detection
# ADR should never be negative
# ----------------------------------------
if "adr" in df.columns:

    outliers = df[df["adr"] < 0]

    if len(outliers) > 0:
        errors.append({
            "Error": "Negative ADR",
            "Details": len(outliers)
        })

# ----------------------------------------
# Save Error Log
# ----------------------------------------
os.makedirs("logs", exist_ok=True)

if errors:
    error_df = pd.DataFrame(errors)
    error_df.to_csv(ERROR_LOG, index=False)

    print("Validation completed with errors.")
    print(error_df)

else:
    print("Validation Successful.")
    print("No Errors Found.")