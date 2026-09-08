import os
import pandas as pd

from config.config import (
    STAGING_FILE,
    FINAL_DATA
)

print("Starting Idempotent Load...")

# Read staging data
staging_df = pd.read_csv(STAGING_FILE)

# Create warehouse folder
os.makedirs("warehouse", exist_ok=True)

# First load
if not os.path.exists(FINAL_DATA):

    staging_df.to_csv(
        FINAL_DATA,
        index=False
    )

    print(
        f"Created warehouse with {len(staging_df)} records."
    )

else:

    # Read existing warehouse
    warehouse_df = pd.read_csv(FINAL_DATA)

    before = len(warehouse_df)

    # Add new records
    merged = pd.concat(
        [warehouse_df, staging_df],
        ignore_index=True
    )

    # Remove exact duplicates
    merged = merged.drop_duplicates()

    after = len(merged)

    duplicates_removed = (
        before
        + len(staging_df)
        - after
    )

    merged.to_csv(
        FINAL_DATA,
        index=False
    )

    print("Warehouse Updated Successfully")
    print(f"Records before merge : {before}")
    print(f"New staging records  : {len(staging_df)}")
    print(f"Duplicates removed   : {duplicates_removed}")
    print(f"Final warehouse rows : {after}")