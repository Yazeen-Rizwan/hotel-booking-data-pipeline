import os
import shutil
import pandas as pd

from config.config import (
    STAGING_FILE,
    FINAL_DATA,
    BACKUP_DATA
)

print("Starting Atomic Load...")

# Read new processed data
staging_df = pd.read_csv(STAGING_FILE)

# Create warehouse folder
os.makedirs("warehouse", exist_ok=True)

# Create backup
if os.path.exists(FINAL_DATA):

    shutil.copy(
        FINAL_DATA,
        BACKUP_DATA
    )

    print("Backup created.")

try:

    # Read existing warehouse
    if os.path.exists(FINAL_DATA):

        existing_df = pd.read_csv(FINAL_DATA)

    else:

        existing_df = pd.DataFrame()

    # Combine existing + new data
    combined_df = pd.concat(
        [existing_df, staging_df],
        ignore_index=True
    )

    # Remove exact duplicate records
    combined_df = combined_df.drop_duplicates()

    # Temporary file
    temp_file = "warehouse/temp.csv"

    # Write temporary file first
    combined_df.to_csv(
        temp_file,
        index=False
    )

    # Replace final file only after successful write
    os.replace(
        temp_file,
        FINAL_DATA
    )

    print("Atomic Load Successful.")
    print(
        f"Final warehouse rows: {len(combined_df)}"
    )

except Exception as e:

    print("Atomic Load Failed.")
    print(e)

    # Restore backup
    if os.path.exists(BACKUP_DATA):

        shutil.copy(
            BACKUP_DATA,
            FINAL_DATA
        )

        print("Backup Restored.")